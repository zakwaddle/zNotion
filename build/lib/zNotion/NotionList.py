from project_package.zNotion.models import List, NotionBase


# |--------------------------------------------------------------------------------| #


class NotionList(NotionBase):
    # def __init__(self, client, raw, model_cls=List, endpoint=None, method="POST", payload=None):
    # def __init__(self, client, raw, endpoint=None, method="POST", payload=None):
    def __init__(self, client, raw):
        self._client = client
        

        self.model = List(raw)

    def __iter__(self):
        return iter(self.model)

    def __getitem__(self, index):
        return self.model[index]

    def __len__(self):
        return len(self.model)

    @property
    def results(self):
        return self.model.results

    @property
    def has_more(self):
        return self.model.has_more

    @property
    def next_cursor(self):
        return self.model.next_cursor

    def fetch_next(self):
        """this doesn't actually work yet"""
        if not self.has_more:
            return []

        if not self.next_cursor:
            raise ValueError("NotionList: no endpoint provided for pagination.")

        updated_payload = dict(self.payload)
        updated_payload["start_cursor"] = self.next_cursor

        next_data = (
            self._client.post(self.endpoint, json=updated_payload)
            if self.method.upper() == "POST"
            else self._client.get(self.endpoint, params={"start_cursor": self.next_cursor})
        )

        # if not hasattr(req, "response") or not req.complete or req.status_code >= 300:
        #     raise RuntimeError(f"Failed to fetch next page: {req}")

        # try:
        #     next_data = req.response.json()
        # except Exception as e:
        #     raise ValueError(f"Pagination response could not be parsed as JSON: {e}")

        next_model = self.model.__class__(next_data)
        self.model.results.extend(next_model.results)
        self.model.next_cursor = next_model.next_cursor
        self.model.has_more = next_model.has_more

        return next_model.results

    def all(self):
        while self.has_more:
            self.fetch_next()
        return self.results


    def as_json_safe(self):
        return self.model.as_json_safe()

    def __repr__(self):
        return f"<NotionList [{len(self.model)} parsed], more={self.has_more}>"



# from .models import parse_object

# class NotionList:
#     def __init__(self, client, raw, endpoint=None, method="POST", payload=None):
#         self.object = raw.get("object", "list")
#         self.results = [parse_object(r) for r in raw.get("results", [])]
#         self.next_cursor = raw.get("next_cursor")
#         self.has_more = raw.get("has_more", False)
#         self._client = client

#         self.endpoint = endpoint  # This is already the route bit (e.g. "blocks/abc/children")
#         self.method = method
#         self.payload = payload or {}

#     def __iter__(self):
#         return iter(self.results)

#     def __getitem__(self, index):
#         return self.results[index]

#     def __len__(self):
#         return len(self.results)

#     def fetch_next(self):
#         if not self.has_more:
#             return []

#         if not self.endpoint:
#             raise ValueError("NotionList: no endpoint provided for pagination.")

#         updated_payload = dict(self.payload)
#         updated_payload["start_cursor"] = self.next_cursor

#         if self.method.upper() == "POST":
#             req = self._client.post(self.endpoint, json=updated_payload)
#         else:
#             req = self._client.get(self.endpoint, params={"start_cursor": self.next_cursor})

#         if not hasattr(req, "response") or not req.complete or req.status_code >= 300:
#             raise RuntimeError(f"Failed to fetch next page: {req}")

#         try:
#             next_data = req.response.json()
#         except Exception as e:
#             raise ValueError(f"Pagination response could not be parsed as JSON: {e}")

#         next_list = NotionList(
#             client=self._client,
#             raw=next_data,
#             endpoint=self.endpoint,
#             method=self.method,
#             payload=self.payload
#         )

#         self.results.extend(next_list.results)
#         self.next_cursor = next_list.next_cursor
#         self.has_more = next_list.has_more
#         return next_list.results


#     def all(self):
#         while self.has_more:
#             self.fetch_next()
#         return self.results

#     def to_dict(self):
#         return [obj.to_dict() if hasattr(obj, "to_dict") else obj for obj in self.results]

#     def as_json_safe(self):
#         import json
#         return json.dumps(self.to_dict(), indent=2)

#     def __repr__(self):
#         return f"<NotionList [{len(self.results)} parsed objects], more={self.has_more}>"