from typing import Optional, Dict
from zBaseController import BaseClient, BaseRequest
from ..models import Page, Properties, EmojiIconProperty, Parent, Children
from ..util.payload_formatter import PayloadFormatter
from ..yell import yell

def prep(thing):
    return PayloadFormatter.format(thing)


class PageRoutes:
    def __init__(self, client: BaseClient):
        self.api = client

    @staticmethod
    def check_response(response):
        if isinstance(response, BaseRequest):
            res = response.get_response()
            raise Exception(f"{res.status_code} - {res._text}")
        if isinstance(response, dict):
            obj = response.get('object')
            if obj == 'page':
                return Page(response)
        return response

    def get(self, page_id: str) -> Page:
        """Retrieve a Notion page by ID."""
        yell(f"get page: page_id={page_id}")
        
        response = self.api.get("pages", page_id)
        # page = Page(response)
        page = self.check_response(response)
        assert isinstance(page, Page)
        # yell(f"result: {page}")
        return page

    def create(self, parent: Parent = None, properties: Properties = None, children: Children = None,
               icon: EmojiIconProperty = None, payload: Optional[Dict] = None) -> Page:
        """
        Create a Notion page using either a full payload or a combination of parent and properties.
        """
        yell("CREATE!!!!")
        if not payload:
            if not (parent and properties):
                raise ValueError("Either `payload` or both `parent` and `properties` must be provided.")
            
            parent = prep(parent)
            properties = prep(properties)

            children = prep(children) if children is not None else {}
            icon = prep(icon) if icon is not None else {}

            payload = {
                **parent, 
                **properties,
                **children,
                **icon,
                }
            # yell("payload:", payload)
        response = self.api.post("pages", json=payload)
        # yell("response:", *response.items())
        # page = Page(response)
        page = self.check_response(response)
        assert isinstance(page, Page)
        yell(f"result:", page, page.properties.values())
        return page

    def get_property(self, page_id: str, property_id: str):
        """Get the value of a Notion page property."""
        return self.api.get("pages", page_id, "properties", property_id)

    def update_properties(self, 
                          page_id: str, 
                          properties: Properties=None, 
                          in_trash: bool=False, 
                          icon: EmojiIconProperty=None) -> Page:
        """
        Update the properties of a Notion page.
        This endpoint can be used to update any page icon or cover, 
        and can be used to delete or restore any page.
        """
        if properties is not None:
            try:
                icon = properties.get_property('icon')
            except KeyError:
                pass

        icon = prep(icon) if icon is not None else {}
        properties = prep(properties) if properties is not None else {}

        payload = {
            **properties,
            **icon,
            "in_trash": in_trash,
            }
        response = self.api.patch("pages", page_id, json=payload)
        # page = Page(page)
        page = self.check_response(response)
        assert isinstance(page, Page)
        # yell(page)
        return page
