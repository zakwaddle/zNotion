from project_package.zNotion.models.Parent import Parent
from project_package.zNotion.models.Properties import Properties
from project_package.zNotion.models.Children import Children
from project_package.zNotion.models.NotionBase import NotionBase

class Page(NotionBase):
    object = 'page'

    def __init__(self, raw_response):
        self._raw = raw_response
        if hasattr(self._raw, 'get_response') or hasattr(self._raw, 'response'):
            res = self._raw.get_response()
            raise Exception(f"{res.status_code} - {res._text}")
        
        obj_type = raw_response.get('object')
        if not obj_type or obj_type != 'page':
            raise ValueError("You're trying to make a Page out of a non-Page object.")
        
        self.object = obj_type
        self.id = raw_response.get('id')
        self.cover = raw_response.get("cover")
        self.icon = raw_response.get("icon")
        self.created_time = raw_response.get("created_time")
        self.created_by = raw_response.get("created_by")
        self.last_edited_time = raw_response.get("last_edited_time")
        self.last_edited_by = raw_response.get("last_edited_by")
        self.archived = raw_response.get("archived")
        self.in_trash = raw_response.get("in_trash")
        self.url = raw_response.get("url")
        self.public_url = raw_response.get("public_url")
        self.request_id = raw_response.get("request_id")
        
        self.parent = Parent(raw_response.get("parent"))
        
        props = raw_response.get("properties", {})
        self.properties = Properties(props)
        if self.parent.type == 'page_id':
            try:
                self.title = self.properties['title']
            except KeyError:
                self.title = ""
        else:
            try:
                self.title = self.properties['Title']
            except KeyError:
                self.title = ""
            

        self.children = Children(raw_response.get('children', []), parent_id=self.id, parent_type='page')
        
        
    def __repr__(self):
        return f'<Page: {self.title}>'

    def __str__(self):
        return f'<Page: {self.title}>'
        


