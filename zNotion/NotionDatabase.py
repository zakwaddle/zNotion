from project_package.zNotion.models.NotionBase import NotionBase
from project_package.zNotion.client.NotionApiClient import NotionApiClient
from project_package.zNotion.models.Database import Database
from project_package.zNotion.models.Properties import Properties
from project_package.zNotion.models.Children import Children
from project_package.zNotion.models.Parent import DatabaseParent
from project_package.zNotion.models.Query import Query
from project_package.zNotion.models.PropertyTypes import EmojiIconProperty
from yell import yell


class NotionDatabase(NotionBase):

    @classmethod
    def get_database(cls, token: str, database_id: str):
        client = NotionApiClient(token=token)

        yell(f"getting database: {database_id}")

        database = client.databases.get(database_id=database_id)
        return cls(client, database)
    
    # @NotionApiClient.log_call()
    # @classmethod
    # def create_database_entry(cls, token, database_id, properties: Properties=None, children: Children=None, icon: EmojiIconProperty=None):
    #     """Create a new entry in the database."""
    #     client = NotionApiClient(token=token)
    #     return client.api.pages.create_page(parent=DatabaseParent(database_id=database_id), 
    #                                         properties=properties,
    #                                         children=children,
    #                                         icon=icon)

    @staticmethod
    def query_database(token: str, database_id: str, query: Query, start_cursor:str=None):
        yell(f"query_database: {database_id}", query, f"start_cursor: {start_cursor}")
        client = NotionApiClient(token=token)
        return client.databases.query(database_id, query=query, start_cursor=start_cursor)

    def __init__(self, client: NotionApiClient, database: Database):
        self.api = client
        self.id = database.id
        self.database: Database = database

    @property
    def schema(self):
        return self.database.schema

    @property
    def properties(self):
        return self.database.properties

    def create(self, properties: Properties=None, children: Children=None, icon: EmojiIconProperty=None):
        """Create a new entry in the database."""
        yell("CREATE!!!")
        # yell("CREATE!!!", "properties:", properties)
        # yell("CREATE!!!", "children:", children)
        # yell("CREATE!!!", "icon:", icon)
        return self.api.pages.create(parent=DatabaseParent(self.id), 
                                          properties=properties,
                                          children=children,
                                          icon=icon)
        
    def query(self, query:Query, start_cursor:str=None):
        """Query the database with optional filters."""
        yell(f"query({query})", f"start_cursor: {start_cursor}")
        return self.api.databases.query(self.id, query=query, start_cursor=start_cursor)

    def get_property_filter(self, prop_name):
        return Query.get_property_filter(property_name=prop_name, database_schema=self.schema)
    
    def get_prop_set(self):
        return self.database.get_prop_set()
    
        
