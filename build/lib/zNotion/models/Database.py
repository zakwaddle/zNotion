from .RichText import RichText
from .Properties import Properties
from .Parent import Parent
from .NotionBase import NotionBase


class Database(NotionBase):
    object = 'database'

    def __init__(self, raw_response):
        self._raw = raw_response
        self.object = raw_response.get("object")
        self.id = raw_response.get("id")
        
        title = raw_response.get("title")
        self.title = ''.join(RichText(t).value for t in title)
        
        self.cover = raw_response.get("cover")
        self.icon = raw_response.get("icon")
        self.created_time = raw_response.get("created_time")
        self.created_by = raw_response.get("created_by")
        self.last_edited_time = raw_response.get("last_edited_time")
        self.last_edited_by = raw_response.get("last_edited_by")
        self.url = raw_response.get("url")
        self.archived = raw_response.get("archived")
        self.in_trash = raw_response.get("in_trash")
        self.public_url = raw_response.get("public_url")
        self.request_id = raw_response.get("request_id")
        self.description = raw_response.get("description")
        self.is_inline = raw_response.get("is_inline")

        properties = raw_response.get("properties")
        parent = raw_response.get("parent")
        self.properties: Properties = Properties(properties)
        self.parent = Parent(parent)

    @property
    def schema(self):
        return {prop.name: prop.type for prop in self.properties}
    
    def __repr__(self):
        return f'<Database {self.title} - {self.id}>'
    
    def get_prop_set(self):
        prop_map = self.properties.property_map
        props = {}
        for title, prop_type in self.schema.items():
            prop_class = prop_map.get(prop_type)
            field = prop_class({'name': title})
            field.set_value(None)
            props[title] = field
        return Properties(props)
        