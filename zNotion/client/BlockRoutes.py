from typing import Dict
from project_package.zNotion.client.zWebApiController.base import BaseClient, BaseRequest
from project_package.zNotion.models import Block, Children, List
from project_package.zNotion.util.payload_formatter import PayloadFormatter
from yell import yell


def prep(thing):
    return PayloadFormatter.format(thing)


class BlockRoutes:

    def __init__(self, client: BaseClient.BaseClient):
        self.api = client
   
    def check_response(self, response):
        print(response)
        if isinstance(response, BaseRequest.BaseRequest):
            res = response.get_response()
            raise Exception(f"{res.status_code} - {res._text}")
        if isinstance(response, dict):
            obj = response.get('object')
            if obj == 'block':
                return Block(response)
        return response


    def get_block(self, block_id: str) -> Block:
        """Get a block."""
        yell(f'get_block(block_id={block_id}):')

        response = self.api.get("blocks", block_id)
        # yell(f'response: ', response)
        
        # block = Block(response)
        block = self.check_response(response)
        assert isinstance(block, Block)
        yell(f'block:', block)
        return block
    
    def update_block(self, block_id: str, block: Block) -> Block:
        """
        Update the content or properties of a block.
        """
        yell(f'update_block(block_id={block_id}) to {block}:')

        response = self.api.patch("blocks", block_id, json=prep(block)) 
        yell(f'response: ', response)

        # new_block = Block(response)
        new_block = self.check_response(response)
        assert isinstance(new_block, Block)
        yell(f'new_block:', new_block)
        return new_block

    def delete_block(self, block_id: str) -> Dict:
        """Delete a block from the page."""
        yell(f'delete_block(block_id={block_id})')

        response = self.api.delete("blocks", block_id)
        yell(f'response: ', response)
        return response

    def get_children(self, parent_id: str) -> List:
        """Get the children blocks of a page or block."""
        yell(f'get_children(parent_id={parent_id})')
        
        raw = self.api.get("blocks", parent_id, "children")
        return List(raw)
    
    def append_children(self, parent_id: str, children, after_block=None) -> List:
        """Append child blocks to an existing block or page."""
        yell(f'append_children(parent_id={parent_id}, children={children}, after_block={after_block})')

        anchor_id = after_block
        if isinstance(after_block, Block):
            anchor_id = after_block.id
        after = {"after": anchor_id} if anchor_id is not None else {}
        if isinstance(children, list) and isinstance(children[0], Block):
            children = Children(children)
        children = prep(children)
        
        payload = {
            **children,
            **after,
        }
        # payload = patch_textless_blocks(payload=payload)
        # yell("block_payload:", payload)
        raw = self.api.patch("blocks", parent_id, "children", json=payload)
        return List(raw)