from .NotionBase import NotionBase
from ..yell import yell


# |--------------------------------------------------------------------------------| #

class FilterQuery(NotionBase):
    # pass
    def __repr__(self):
        return f"<FilterQuery base type: {type(self).__name__}>"


class FilterProperty(FilterQuery):
    type = None
    DEFAULT = 'equals'

    def __init__(self, key:str, op:str, value):
        self.key = key
        self.op = op
        self.value = value
        yell(f"init: {self.__class__.__name__}", f"key={self.key}", f"op={self.op}", f"value={self.value}")

    def __repr__(self):
        return f"<{self.__class__.__name__} key='{self.key}' op='{self.op}' value={self.value}>"

class NullFilter(FilterProperty):
    def __init__(self):
        super().__init__(None, None, None)
        
class TextFilter(FilterProperty):
    type = "rich_text"
    DEFAULT = 'contains'
    CONTAINS = 'contains'
    EQUALS = 'equals'
    STARTS_WITH = 'starts_with'
    ENDS_WITH = 'ends_with'

    def __init__(self, key: str, op: str, value: str):
        assert op in ("contains", "equals", "starts_with", "ends_with")
        super().__init__(key, op, value)

class SelectFilter(FilterProperty):
    type = "select"
    DEFAULT = "equals"
    EQUALS = 'equals'
    DOES_NOT_EQUAL = 'does_not_equal'
    def __init__(self, key: str, op: str, value: str):
        assert op in ("equals", "does_not_equal")
        super().__init__(key, op, value)

class MultiSelectFilter(FilterProperty):
    type = "multi_select"
    DEFAULT = 'contains'
    CONTAINS = 'contains'
    DOES_NOT_CONTAIN = 'does_not_contain'
    def __init__(self, key: str, op: str, value: str):
        assert op in ("contains", "does_not_contain")
        super().__init__(key, op, value)

class CheckboxFilter(FilterProperty):
    type = "checkbox"
    def __init__(self, key: str, value: bool):
        super().__init__(key, "equals", value)

class NumberFilter(FilterProperty):
    type = "number"
    DEFAULT = "equals"
    GREATER_THAN = "greater_than"
    GREATER_THAN_OR_EQUAL_TO = "greater_than_or_equal_to"
    LESS_THAN = "less_than"
    LESS_THAN_OR_EQUAL_TO = "less_than_or_equal_to"
    DOES_NOT_EQUAL = "does_not_equal"
    EQUALS = "equals"
    IS_EMPTY = "is_empty"
    IS_NOT_EMPTY = "is_not_empty"

    def __init__(self, key: str, op: str, value: str):
        assert op in ("is_not_empty", "is_empty", "equals", 
                      "does_not_equal", "less_than", "less_than_or_equal_to", 
                      "greater_than", "greater_than_or_equal_to")
        super().__init__(key, op, value)

class DateFilter(FilterProperty):
    type = 'date'
    DEFAULT = "equals"
    ON_OR_BEFORE = "on_or_before"
    ON_OR_AFTER = "on_or_after"
    EQUALS = "equals"
    PAST_WEEK = "past_week"
    NEXT_MONTH = "next_month"

    def __init__(self, key: str, op: str, value: str):
        assert op in ("on_or_before", "on_or_after", "equals", "past_week", "next_month")
        super().__init__(key, op, value)

class FilterCombiner(FilterQuery):
    def __init__(self, logical_op:str=None, filters=None):
        assert logical_op in ("and", "or")
        self.op = logical_op
        self.filters = filters
        yell(f"init: {self.__class__.__name__}", f"op='{self.op}'", f"filters={self.filters}")

    def __repr__(self):
        return f"<{self.__class__.__name__} op='{self.op}' filters={len(self.filters)}>"

class AndFilterCombiner(FilterCombiner):
    def __init__(self, filters):
        super().__init__(logical_op='and', filters=filters)

class OrFilterCombiner(FilterCombiner):
    def __init__(self, filters):
        super().__init__(logical_op='or', filters=filters)

class Sort:
    def __init__(self, property_name, direction="ascending"):
        assert direction in ("ascending", "descending")
        self.property = property_name
        self.direction = direction
        yell(f"{self.__class__.__name__}", f"property='{self.property}'", f"direction='{self.direction}'")

    def __repr__(self):
        return f"Sort({self.property!r}, direction={self.direction!r})"
    
class AscendingSort(Sort):
    def __init__(self, property_name):
        super().__init__(property_name, "ascending")
    
class DescendingSort(Sort):
    def __init__(self, property_name):
        super().__init__(property_name, "descending")

class Query:
    filter_map = {
        'and': AndFilterCombiner,
        'or': OrFilterCombiner,
        'rich_text': TextFilter,
        'select': SelectFilter,
        'multi_select': MultiSelectFilter,
        'date': DateFilter,
        'checkbox': CheckboxFilter,
        'number': NumberFilter,
    }
    def __init__(self, filter:FilterQuery, *sorts:Sort, limit=25):
        self.filter = filter
        self.sorts = sorts
        self.limit = limit

    def get_filter(self, key):
        return self.filter_map.get(key)
    
    @staticmethod
    def get_property_filter(property_name:str , database_schema:dict):
        prop_type = database_schema.get(property_name)
        return Query.filter_map.get(prop_type)
    

    @staticmethod
    def make_filter(expr, key_map):
        """
        valid structures:
        - tuple expression:
            ("Title", "contains", "mountains")
            (("Title", "contains", "mountains"), "and", ("Type", "equals", "Vacation"))

        - combiner structure:
            ("or", [("Title", "contains", "mountains"), ("Type", "equals", "Vacation"))])
        """
        # Case: logical combiner syntax ("and", [filters...])
        if isinstance(expr, tuple) and isinstance(expr[0], str) and isinstance(expr[1], list):
            op = expr[0]
            filters = [Query.make_filter(sub_expr, key_map) for sub_expr in expr[1]]
            combiner_class = Query.filter_map[op]
            return combiner_class(*filters)

        # Case: binary-style legacy grammar
        elif isinstance(expr, tuple) and len(expr) == 3:
            one, op, three = expr
            if isinstance(one, tuple):
                return Query.make_filter((op, [one, three]), key_map)

            # Atomic
            key = one
            filter_type = key_map.get(key)
            if not filter_type:
                raise ValueError(f"Unknown property type for key: {key}")
            filter_class = Query.filter_map.get(filter_type)
            return filter_class(key, op, three)

        raise TypeError("Invalid filter structure")

    def __repr__(self):
        return f"<Query filter={self.filter} sorts={len(self.sorts)} limit={self.limit}>"

