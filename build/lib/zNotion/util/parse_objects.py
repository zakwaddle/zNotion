from ..models import Page, Database, Block
from ..client.NotionApiClient import WebRequest

def parse_object(data):

    if isinstance(data, WebRequest):
        res = data.get_response()
        raise Exception(f"{res.status_code} - {res._text}")
    if isinstance(data, list):
        return [parse_object(d) for d in data]
    if isinstance(data, dict) and "object" in data:
        t = data["object"]
        if t == "page":
            return Page(data)
        elif t == "database":
            return Database(data)
        elif t == "block":
            return Block(data)
        elif t == "list":
            return data
    # print("parse_object", data)
    return data
