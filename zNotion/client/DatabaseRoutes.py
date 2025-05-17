from zBaseController import BaseClient
from ..models import Query, Database, List, Parent, TitleProperty
from ..util.payload_formatter import PayloadFormatter
from ..yell import yell


def prep(thing):
    return PayloadFormatter.format(thing)

class DatabaseRoutes:
    def __init__(self, client: BaseClient):
        self.api = client

    def create(self, parent:Parent, title:TitleProperty, properties_schema):
        
        database = self.api.post("databases")
        return Database(database)

    def get(self, database_id) -> Database:
        """Retrieve a Notion database by ID."""
        database = self.api.get("databases", database_id)
        return Database(database)
    
    def query(self, database_id: str, query: Query = None, start_cursor=None) -> List:
        """Query a Notion database."""
        q = prep(query)
        if start_cursor is not None:
            q.update({"start_cursor": start_cursor})
        # yell(f"query payload: ", q)
        results = self.api.post("databases", database_id, "query", json=q or {})
        yell("query results:", bool(results))
        if hasattr(results, "response"):
            yell("WebRequest?! -> ", results.response.status_code, results.response._text)
        return List(results)

    def update(self, database_id) -> Database:
        """Retrieve a Notion database by ID."""
        database = self.api.patch("databases", database_id)
        return Database(database)