from project_package.zNotion.models.NotionBase import NotionBase

class RichText(NotionBase):
    def __init__(self, value=None, **meta):
        self.value = value

        meta = meta or {}
        if isinstance(self.value, dict) and not meta:
            meta = value
            self.value = None
            
        # Extract from Notion API shape if passed
        text_meta = meta.get("text", {})
    
        self.link = meta.get("link")
        self.link = self.link.get('url') if self.link else None
        self._annotations = meta.get("annotations")

        # Fallback annotations
        self.bold = self._annotations.get('bold', False) if self._annotations else False
        self.italic = self._annotations.get('italic', False) if self._annotations else False
        self.strikethrough = self._annotations.get('strikethrough', False) if self._annotations else False
        self.underline = self._annotations.get('underline', False) if self._annotations else False
        self.code = self._annotations.get('code', False) if self._annotations else False
        self.color = self._annotations.get('color', "default") if self._annotations else "default"

        # If no annotations were given, but text content was passed directly
        # try to pull value from raw content if no explicit value
        if self.value is None:
            self.value = text_meta.get("content", "")

    def __str__(self):
        return self.value
    
    def __repr__(self):
        return f'RichText({repr(self.value)})'
    
    def __getitem__(self, index):
        return self.value[index]
    
    def __hash__(self):
        return hash((self.value, self.link, frozenset(self.annotations.items())))

    def __eq__(self, other):
        return (
            isinstance(other, RichText) and
            self.value == other.value and
            self.link == other.link and
            self.annotations == other.annotations
        )

    @property
    def annotations(self):
        return {
            "bold": self.bold,
            "italic": self.italic,
            "strikethrough": self.strikethrough,
            "underline": self.underline,
            "code": self.code,
            "color": self.color
        }
