# import json
from ..util.parse_objects import parse_object
from .NotionBase import NotionBase
# from yell import yell

class List(NotionBase):
    object = 'list'

    def __init__(self, raw, func_for_next=None):
        if not isinstance(raw, dict):
         if hasattr(raw, 'get_response') or hasattr(raw, 'response'):
            res = raw.get_response()
            raise Exception(f"{res.status_code} - {res._text}")
        self.raw = raw
        self.object = raw.get("object", "list")
        self.results = self.parse(raw.get("results", []))
        self.next_cursor = raw.get("next_cursor")
        self.has_more = raw.get("has_more", False)
        self.func_for_next = func_for_next

    def parse(self, raw_results):
        return [parse_object(r) for r in raw_results]

    def __iter__(self):
        return iter(self.results)

    def __getitem__(self, idx):
        return self.results[idx]

    def __len__(self):
        return len(self.results)
    
    def __repr__(self):
        return f"<List of {len(self.results)} items>"

    def get_next(self):
        if self.func_for_next is not None and self.has_more:
            return self.func_for_next(self.next_cursor)
        else:
            raise ValueError("NotionList: no endpoint provided for pagination.")

    # def to_dict(self):
    #     return [r.to_dict() if hasattr(r, "to_dict") else r for r in self.results]
    #
    # def as_json_safe(self):
    #     return json.dumps(self.to_dict(), indent=2)
