from .NotionBase import NotionBase
from ..yell import yell
from .PropertyTypes import (
    Property,
    TextProperty, TitleProperty, NumberProperty, RollupProperty,
    SelectProperty, MultiSelectProperty, LastEditedTimeProperty,
    CheckboxProperty, CreatedTimeProperty, EmojiIconProperty, RelationProperty,
    DateProperty, URLProperty, EmailProperty, PhoneNumberProperty, ChildPageTitle
)

class Properties(NotionBase):
    property_map = {
        "emoji": EmojiIconProperty,
        "title" : TitleProperty,
        "rich_text" : TextProperty,
        "number" : NumberProperty,
        "phone_number": PhoneNumberProperty, 
        "date": DateProperty, 
        "url": URLProperty, 
        "email": EmailProperty,
        "select" : SelectProperty,
        "multi_select" : MultiSelectProperty,
        "last_edited_time" : LastEditedTimeProperty,
        "checkbox" : CheckboxProperty,
        "created_time" : CreatedTimeProperty,
        "relation": RelationProperty,
        "rollup": RollupProperty,
        "child_page_title": ChildPageTitle,
    }

    def __init__(self, properties):
        self._raw = properties
        self._instances = self._setup_props()
        self._changed = []
        self._dirty = False


    def _setup_props(self):
        props = {}
    
        yell("starting _setup_props(): ")
        for name, val in self._raw.items():
            # yell(f"in setup props loop", f"name: {name}", is_loop=True, loop_lvl=1)
            if isinstance(val, Property):
                props[name] = val
                continue
            if isinstance(val, str):
                props[name] = val
                continue
            
            prop_type = val.get("type")
            prop_class = self.property_map.get(prop_type)
            # yell("prop_class:", prop_class, is_loop=True, loop_lvl=1)
            if not prop_class:
                raise NotImplementedError(f"Unsupported property type: {prop_type}")
            
            instance = prop_class(val)
            instance.name = name
            props[name] = instance
        yell("final props: ", *props.items(), is_loop=True)
        return props


    def __iter__(self):
        return iter(self._instances.values())
    
    def __getitem__(self, key):
        if key not in self._instances:
            raise KeyError(f"Property '{key}' not found. Cannot set value for undefined property.")
        return self._instances[key].value
    
    def __setitem__(self, key, value):
        if key not in self._instances:
            raise KeyError(f"Property '{key}' not found. Cannot set value for undefined property.")
        self._changed.append(key)
        self._dirty = True
        self._instances[key].set_value(value)
    
    def __hash__(self):
        return hash(tuple(sorted(hash(p) for p in self)))

    def __eq__(self, other):
        if not isinstance(other, Properties):
            return False
        return all(
            self._instances.get(k) == other._instances.get(k)
            for k in set(self._instances.keys()).union(other._instances.keys())
        )

    def get_property(self, key) -> Property:
        if key not in self._instances:
            raise KeyError(f"Property '{key}' not found.")
        return self._instances[key]
    
    def values(self):
        return {key: val.value for key, val in self._instances.items()}

    def keys(self):
        return [key for key in self._instances.keys()]

    def __repr__(self):
        keys = list(self._instances.keys())
        return f"<Properties {len(keys)} fields: {keys}>"

    def make_prop(self, property_type=None, property_name=None, property_value=None):
        yell("make prop with:", property_name, property_type, property_value)
        available_property_types = [key for key in self.property_map.keys()]
        if property_name and property_type in available_property_types:
            yell('making it')
            prop_class = self.property_map.get(property_type)
            prop = prop_class({"name": property_name})
            yell(prop)

            prop.set_value(property_value)
            yell(prop)
            return prop
        return None

    def empty_props(self):
        props = {}
        for name, prop in self._instances.items():
            prop_type = prop.type
            new_prop = self.make_prop(property_type=prop_type, property_name=name, property_value=None)
            props[name] = new_prop
        return props

    def get_changed_properties(self):
        changed = set(self._changed)
        changed_dict = {}
        for i in changed:
            yell(i)
            prop = self.get_property(i)
            # prop.name = i
            yell(prop)
            changed_dict[i] = prop

        return Properties(changed_dict)

    @staticmethod
    def title_field(name, value):
        prop = TitleProperty({"name": name})
        prop.set_value(value)
        return prop

    @staticmethod
    def text_field(name, value):
        prop = TextProperty({"name": name})
        prop.set_value(value)
        return prop

    @staticmethod
    def number_field(name, value):
        prop = NumberProperty({"name": name})
        prop.set_value(value)
        return prop

    @staticmethod
    def checkbox_field(name, value):
        prop = CheckboxProperty({"name": name})
        prop.set_value(value)
        return prop

    @staticmethod
    def select_field(name, value):
        prop = SelectProperty({"name": name})
        prop.set_value(value)
        return prop

    @staticmethod
    def multi_select_field(name, value):
        prop = MultiSelectProperty({"name": name})
        prop.set_value(value)
        return prop


    
