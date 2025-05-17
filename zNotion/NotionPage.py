from .yell import yell
from .client.NotionApiClient import NotionApiClient
from .NotionBlock import NotionBlock
from .models import Page, Properties, Children, Property, List, Block, EmojiIconProperty, NotionBase


class NotionPage(NotionBase):

    @classmethod
    def get_page(cls, token: str, page_id: str):
        client = NotionApiClient(token=token)
        page = client.pages.get(page_id=page_id)
        return cls(client, page)

    @staticmethod
    def trash_page(token: str, page_id: str):
        client = NotionApiClient(token=token)
        client.pages.update_properties(page_id=page_id, in_trash=True)

    def __init__(self, client: NotionApiClient, page: Page):
        self.api = client
        self.page = page

    @property
    def id(self):
        return self.page.id
    
    @property
    def properties(self) -> Properties:
        return self.page.properties
    
    @property
    def children(self) -> Children:
        return self.page.children

    def update_properties(self, new_props: Properties, icon:EmojiIconProperty=None):
        new_page = self.api.pages.update_properties(self.id, properties=new_props, icon=icon)
        self.page = new_page
        yell(f"updated properties", new_page.properties.values())
        return self.properties
        
    def update_property(self, prop_name, new_value):
        prop: Property = self.properties.get_property(prop_name)
        prop.set_value(new_value)
        return self.update_properties(Properties(properties=prop))

    def get_children(self):
        results: List = self.api.blocks.get_children(self.id)
        self.page.children = Children(results.results)
        return self.children
    
    def append_children(self, *blocks, after=None) -> Children:
        """
        blocks can be:
            - an instance of Children(Blocks)
                append_children( Children([block1, block2, block3]) )

            - a list of Blocks 
                append_children( [block1, block2, block3] )
            
            - Blocks as args 
                append_children(block1, block2, block3)

        after can be:
            - string: the id of the block to append children after
            - Block: the Block to append children after
        """
        return self.api.blocks.append_children(self.id, blocks, after_block=after)

    def get_block_at(self, index):
        return self.children[index]

    def append_to_block_at(self, index, *children):
        block = self.children[index]
        block = NotionBlock(self.api, block=block)
        return block.append_children(*children)

    def update_block_at(self, index, new_block:Block):
        block = self.children[index]
        block = NotionBlock(self.api, block=block)
        return block.update_block(new_block=new_block)

    def delete_block_at(self, index):
        block = self.children[index]
        return self.api.blocks.delete_block(block.id)

    def __repr__(self):
        title = self.properties["Title"] if "Title" in self.properties else self.id
        return f"<NotionPage: {title}>"
