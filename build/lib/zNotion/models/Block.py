from .RichText import RichText
from .Children import Children
from .NotionBase import NotionBase


class Block(NotionBase):
    # Notion block types that support "children"
    CHILD_SUPPORTED_TYPES = {
        "toggle",
        "paragraph",
        "heading_1",
        "heading_2",
        "heading_3",
        "bulleted_list_item",
        "numbered_list_item"
    }

    def __init__(self, raw_response):
        self._raw = raw_response
        self.id = raw_response.get('id')
        self.type = raw_response.get('type')
        
        text = raw_response.get(self.type) or raw_response.get('text')
        
        if isinstance(text, list) and isinstance(text[0], RichText):
            self.text = text
        elif isinstance(text, dict):
            raw = text.get("rich_text")
            self.text = [RichText(guts) for guts in raw] if raw is not None else []
        else:
            self.text = (
                text if isinstance(text, RichText)
                else RichText(raw_response.get('text'))
            )
        
        self.parent = raw_response.get('parent')  # Used only at the entry/page level
        self.is_container = self.type in self.CHILD_SUPPORTED_TYPES
        self.has_children = raw_response.get('has_children')
        if self.is_container:
            self.children = Children(raw_response.get('children', []), parent_id=self.id, parent_type=self.type)
        self.meta = raw_response.get('meta', {})
        if not self.meta:
            self.meta = raw_response.get(self.type)
        # if self.type == "child_page":
        #     self.meta.update({"title": self._raw.get('child_page')})
        # if self.type == "child_database":
        #     self.meta.update({"title": self._raw.get('child_database')})

    def __hash__(self):
        return hash((
            self.type,
            hash(self.text),
            tuple(hash(c) for c in self.children_safe()),
            frozenset(self.meta.items())
        ))

    def __eq__(self, other):
        return (
            isinstance(other, Block) and
            self.type == other.type and
            self.text == other.text and
            self.children_safe() == other.children_safe() and
            self.meta == other.meta
        )

    def children_safe(self):
        if self.is_container:
            return self.children
        else:
            return []
        
    def __repr__(self):
        parts = [f"<Block:[{self.type}]"]

        if self.text:
            if isinstance(self.text, list):
                text = []
                for t in self.text:
                    if isinstance(t, RichText):
                        text.append(str(t))
                    if isinstance(t, str):
                        text.append(t)
                
                parts.append(f" text='{''.join(text)[:30]}'")
            if isinstance(self.text, RichText):
                parts.append(f" text='{str(self.text)[:30]}'")

        if self.meta:
            parts.append(" meta=✓")

        parts.append(">")
        return "".join(parts)
    
    def __str__(self):
        return self.__repr__()