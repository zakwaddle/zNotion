from .NotionBase import NotionBase
# from ..yell import yell


# |--------------------------------------------------------------------------------| #

class Children(NotionBase):
    def __init__(self, blocks=None, parent_id=None, parent_type=None, has_more=False):
        self.parent_id = parent_id
        self.parent_type = parent_type
        self.has_more = has_more
        self.blocks = [self._wrap(b) for b in (blocks or [])]
        self._dirty = False

    @staticmethod
    def _wrap(block):
        from .Block import Block
        return block if isinstance(block, Block) else Block(block)
    
    def __call__(self, *blocks):
        for block in blocks:
            self.add(self._wrap(block=block))

    def __iter__(self):
        return iter(self.blocks)

    def __getitem__(self, index):
        return self.blocks[index]

    def __len__(self):
        return len(self.blocks)
    
    def __hash__(self):
        return hash(tuple(hash(b) for b in self.blocks))

    def __eq__(self, other):
        if not isinstance(other, Children):
            return False
        return self.blocks == other.blocks
    
    def __str__(self):
        return self.__repr__()
    
    def __repr__(self):
            return f"<Children count={len(self.blocks)} dirty={self._dirty}>"
    
    def add(self, block):
        self.blocks.append(self._wrap(block))
        self._dirty = True

    def extend(self, block_list):
        for b in block_list:
            self.add(b)

    def insert(self, index, block):
        self.blocks.insert(index, self._wrap(block))
        self._dirty = True

    def is_dirty(self):
        return self._dirty

    def reset_dirty(self):
        self._dirty = False