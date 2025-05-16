from project_package.zNotion.models.NotionBase import NotionBase

def make_hashable(obj):
    if isinstance(obj, dict):
        return frozenset((k, make_hashable(v)) for k, v in obj.items())
    elif isinstance(obj, list):
        return tuple(make_hashable(i) for i in obj)
    return obj


class Property(NotionBase):

    def __init__(self, raw_response):
        self.name = raw_response.pop('name', '')
        try:
            self.id = raw_response.pop('id')
            self.type = raw_response.pop('type')
        except KeyError:
            pass
        self.meta = raw_response
        self.__value = None

    @property
    def value(self):
        return self.__value
    
    def set_value(self, new_value):
        self.__value = new_value
    
    def __repr__(self):
        return f"<{self.__class__.__name__}  -  {self.name}: {self.value}>"
    
    def __hash__(self):
        print(self.meta.items())
        try:
            val = frozenset(self.value)
        except TypeError:
            val = self.value
        return hash((
            self.name,
            self.type,
            val,
            make_hashable(self.meta)
        ))

    def __eq__(self, other):
        return (
            isinstance(other, Property) and
            self.name == other.name and
            self.type == other.type and
            self.value == other.value and
            self.meta == other.meta
        )
    
class ChildPageTitle(NotionBase):

    def __init__(self, title):
        self.title = title