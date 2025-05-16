from project_package.zNotion.models.NotionBase import NotionBase

class Option(NotionBase):
    def __init__(self, id=None, name=None, color=None, description=None):
        self.id = id
        self._name = name
        self.color = color
        self.description = description

    @property
    def name(self):
        return self._name

    def to_dict(self):
        return {'id': self.id,
                'name': self.name,
                'color': self.color,
                'description': self.description}

    def __str__(self):
        return self.name or ''

    def __repr__(self):
        return f'Option({repr(self.name)})'
    

    def __hash__(self):
        return hash((self.name, self.id, self.color))

    def __eq__(self, other):
        return (
            isinstance(other, Option) and
            self.name == other.name and
            self.id == other.id and
            self.color == other.color
        )
    

