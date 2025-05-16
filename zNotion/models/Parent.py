from project_package.zNotion.models.NotionBase import NotionBase

class Parent(NotionBase):
    
    def __init__(self, raw):
        self.type = raw.get('type')
        self.id = raw.get(self.type)
    
    def __repr__(self):
        return f"<Parent type='{self.type}' id='{self.id}'>"

class DatabaseParent(Parent):
    def __init__(self, database_id=None):
        self.type = 'database_id'
        self.id = database_id
        super().__init__({"type": self.type, self.type: self.id})

class PageParent(Parent):

    def __init__(self, page_id=None):
        self.type = 'page_id'
        self.id = page_id
        super().__init__({"type": self.type, self.type: self.id})

class BlockParent(Parent):

    def __init__(self, block_id=None):
        self.type = 'block_id'
        self.id = block_id
        super().__init__({"type": self.type, self.type: self.id})

class WorkspaceParent(Parent):

    def __init__(self):
        self.type = 'workspace'
        self.id = True
        super().__init__({"type": self.type, self.type: self.id})

#     @staticmethod
#     def parse(parent_obj):
#         t = parent_obj.get('type')
#         if t == "workspace":
#             return Parent.Workspace()
#         if t == "database_id":
#             return Parent.Database(parent_obj.get('database_id'))
#         if t == "page_id":
#             return Parent.Page(parent_obj.get('page_id'))
#         if t == "block_id":
#             return Parent.Block(parent_obj.get('block_id'))
#         else:
#             return parent_obj
