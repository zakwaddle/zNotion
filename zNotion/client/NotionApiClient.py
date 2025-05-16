from typing import Dict
from project_package.zNotion.client.zWebApiController import WebApiClient, WebApiAuth, WebRequest
from project_package.zNotion.client.DatabaseRoutes import DatabaseRoutes
from project_package.zNotion.client.PageRoutes import PageRoutes
from project_package.zNotion.client.BlockRoutes import BlockRoutes
from project_package.zNotion.models import List
import time
from yell import yell


NOTION_VERSION = "2022-06-28"
NOTION_BASE_URL = "https://api.notion.com/v1"



# |--------------------------------------------------------------------------------| #

class NotionAuth(WebApiAuth):
    """Custom Notion authentication using Bearer token and API versioning."""
    
    def __call__(self, request):
        request.headers.update({
            "Authorization": f"Bearer {self.token}",
            "Notion-Version": NOTION_VERSION,
            "Content-Type": "application/json"
        })
        return request


class YourProblem(Exception):
    pass

class YourError(YourProblem):
    pass

class NotionsError(YourProblem):
    pass

class NotionApiClient(WebApiClient):
    """Client for the Notion v1 API, wrapping zWebApiClient with structured methods."""
    
    def __init__(self, token: str, use_emoji=False, debug=True) -> None:
        super().__init__(NOTION_BASE_URL, NotionAuth(token), debug=debug)
        self.use_emoji = use_emoji
        self.databases = DatabaseRoutes(self)
        self.pages = PageRoutes(self)
        self.blocks = BlockRoutes(self)
        self.debug = debug


    def post_flight(self, req: WebRequest):
        if not req.response:
            return req

        status = req.status_code
        body = req.response.text
            
        def parse():
            try:
                return req.response.json()
            except Exception:
                if hasattr(req.response, "text"):
                    return req.response.text
                return req.response

        if status == 200:
            return parse()
        elif status == 202:
            yell("🔄 Request accepted and processing (202).")
            return parse()
        elif status == 400:
            yell(f"❌ Bad Request (400): Check your payload or parameters.", body)
            raise YourError("Bad Request (400): Check your payload or parameters.")
        elif status == 401:
            yell(f"🔒 Unauthorized (401): Missing or invalid Notion API token.", body)
            raise YourError("Unauthorized (401): Missing or invalid Notion API token.")
        elif status == 403:
            yell(f"🚫 Forbidden (403): Token lacks permission for this resource.", body)
            raise YourError("Forbidden (403): Token lacks permission for this resource.")
        elif status == 404:
            yell(f"📭 Not Found (404): Resource may not exist or is inaccessible.", body)
            raise YourError("Not Found (404): Resource may not exist or is inaccessible.")
        elif status == 409:
            yell(f"⚠️ Conflict (409): Likely a version/edit collision.", body)
            raise YourError("Conflict (409): Likely a version/edit collision.")
            
        elif status == 429:
            retry_after = int(req.response.headers.get("Retry-After", 1))
            yell(f"⏳ Rate Limit (429): Retrying after {retry_after} seconds...")
            time.sleep(retry_after)
            req.send()
        elif status == 500:
            yell(f"🔥 Internal Server Error (500): Something broke on Notion's side.", body)
            raise NotionsError("Internal Server Error (500): Something broke on Notion's side.")
        elif status == 503:
            yell(f"🔌 Service Unavailable (503): Notion API is temporarily offline.", body)
            raise NotionsError(f"🔌 Service Unavailable (503): Notion API is temporarily offline.")
        elif 500 <= status < 600:
            yell(f"🔧 Server error ({status}):", body)
            raise NotionsError(f"🔧 Server error ({status})")
        elif status >= 400:
            yell(f"⚠️ Client error ({status}):", body)
            raise YourError(f"⚠️ Client error ({status})")

        return req

        
# |------------------------------ Search ------------------------------| #
 
    def search(self, query: str = '', **kwargs) -> List:
        """Search for pages, databases, or blocks in a workspace."""
        params = {"query": query} if query else {}
        params.update(kwargs)
        results = self.post("search", json=params)
        return List(results)
 
 # |------------------------------ Comments ------------------------------| #
    """
    - POST /v1/comments — Create a comment
    - GET /v1/comments — Retrieve comments
    """
 # |------------------------------ Users ------------------------------| #

    def get_all_users(self) -> Dict:
        """Get a list of all users in the workspace."""
        return self.get("users")

    def get_user(self, user_id: str) -> Dict:
        """Retrieve a specific user by ID."""
        return self.get("users", user_id)
