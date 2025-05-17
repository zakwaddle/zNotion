from yell import yell
from project_package.zNotion.models import NotionBase, Block, List, Children
from project_package.zNotion.client.NotionApiClient import NotionApiClient


class NotionBlock(NotionBase):

    @classmethod
    def get_block(cls, token: str, block_id: str):
        client = NotionApiClient(token=token)
        block = client.blocks.get_block(block_id=block_id)
        yell(f"got block: {block}")
        return cls(client, block)
    
    @staticmethod
    def get_block_children(token: str, block_id: str) -> Children:
        client = NotionApiClient(token=token)
        results: List = client.blocks.get_children(block_id)
        children = Children(results.results, parent_id=block_id, parent_type="block", has_more=results.has_more)
        yell(f"got children: {children}")
        return children
    
    @staticmethod
    def append_blocks(token: str, parent_id: str, *blocks, after=None) -> Children:
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
        client = NotionApiClient(token=token)
        if not isinstance(blocks, Children):
            blocks = Children(blocks=blocks)
        return client.blocks.append_children(parent_id, blocks, after_block=after)
    
    @staticmethod
    def delete_block(token: str, block_id: str):
        client = NotionApiClient(token=token)
        yell(f"deleting block: {block_id}")
        return client.blocks.delete_block(block_id=block_id)
    
    @staticmethod
    def update_block(token: str, block_id: str, new_block:Block):
        client = NotionApiClient(token=token)
        yell(f"updating block:{block_id}",  f"to: {new_block}")
        return client.blocks.update_block(block_id, new_block)
        
        

    def __init__(self, client: NotionApiClient, block):
        self.api = client

        if isinstance(block, dict):
            self.block = Block(block)
        elif isinstance(block, Block):
            self.block = block
        else:
            self.block = None

    def refresh(self):
        data = self.api.blocks.get_block(self.block.id)
        self.block = Block(data)

    @property
    def id(self):
        return self.block.id

    @property
    def type(self):
        return self.block.type

    @property
    def children(self):
        return self.block.children_safe()

    @property
    def text(self):
        return self.block._text


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
        if not self.block.is_container:
            raise TypeError(f"Block type '{self.block.type}' cannot contain children.")
        return self.api.blocks.append_children(self.id, blocks, after_block=after)

    def get_children(self):
        if self.block.is_container and self.block.has_children:
            results: List = self.api.blocks.get_children(self.id)
            self.block.children = Children(results.results, parent_id=self.id, parent_type="block", has_more=results.has_more)
            return self.children

    def update(self, new_block:Block):
        yell("update:", self.block, "to", new_block)
        block = self.api.blocks.update_block(self.id, new_block)
        self.block = block

    def delete(self):
        yell(f"deleting: {self}")
        self.api.blocks.delete_block(self.id)

    def __repr__(self):
        return f"<NotionBlock {self.block.type} {self.block.id}>"

