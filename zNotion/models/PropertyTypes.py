from .RichText import RichText
# from .Property import Property, ChildPageTitle
from .Option import Option
from ..yell import yell
from .NotionBase import NotionBase


def make_hashable(obj):
    if isinstance(obj, dict):
        return frozenset((k, make_hashable(v)) for k, v in obj.items())
    elif isinstance(obj, list):
        return tuple(make_hashable(i) for i in obj)
    return obj


class Property(NotionBase):

    def __init__(self, raw_response):
        self.name = raw_response.pop('name', '')
        try:
            self.id = raw_response.pop('id')
            self.type = raw_response.pop('type')
        except KeyError:
            pass
        self.meta = raw_response
        self.__value = None

    @property
    def value(self):
        return self.__value

    def set_value(self, new_value):
        self.__value = new_value

    def __repr__(self):
        return f"<{self.__class__.__name__}  -  {self.name}: {self.value}>"

    def __hash__(self):
        print(self.meta.items())
        try:
            val = frozenset(self.value)
        except TypeError:
            val = self.value
        return hash((
            self.name,
            self.type,
            val,
            make_hashable(self.meta)
        ))

    def __eq__(self, other):
        return (
                isinstance(other, Property) and
                self.name == other.name and
                self.type == other.type and
                self.value == other.value and
                self.meta == other.meta
        )


class TitleProperty(Property):

    def __init__(self, kwargs):
        super().__init__(kwargs)
        self.title = self.meta.pop('title', [{}])
        text = self.title[0].get('text', {}).get('content', '') if self.title else ''
        self.set_value(text)


class CheckboxProperty(Property):
    def __init__(self, kwargs):
        super().__init__(kwargs)
        yell("checkbox:", kwargs)
        try:
            self.checked = self.meta.pop('checked')
        except KeyError:
            box = self.meta.get("checkbox", {})
            if isinstance(box, bool):
                self.checked = box
            else:
                self.checked = box.get("checkbox")
        self.set_value(self.checked)


class TextProperty(Property):

    def __init__(self, kwargs):
        super().__init__(kwargs)
        rich = self.meta.get('rich_text', [])
        text = ''.join(RichText(r).value for r in rich)
        self.set_value(text)


class NumberProperty(Property):
    def __init__(self, kwargs):
        super().__init__(kwargs)

        self.format = self.meta.pop('format', None)
        self.set_value(self.meta.pop('number', None))


class SelectProperty(Property):
    def __init__(self, kwargs):
        super().__init__(kwargs)
        selection = self.meta.pop('select', None)
        self.options = None
        if selection is not None and isinstance(selection, dict):
            options = selection.get("options")
            if options is not None:
                self.options = [Option(**s) for s in options]
                self.set_value(self.options)
            else:  
                selection = Option(**selection)
                self.set_value(selection)


class MultiSelectProperty(Property):
    def __init__(self, kwargs):
        super().__init__(kwargs)
        self.options = self.meta.pop('multi_select', None)
        if self.options is not None and isinstance(self.options, list):
            self.options = [Option(**o) for o in self.options if isinstance(o, dict)]
        self.set_value(self.options)


class CreatedTimeProperty(Property):
    def __init__(self, kwargs):
        super().__init__(kwargs)
        self.created_time = self.meta.pop('created_time', None)
        self.set_value(self.created_time)


class LastEditedTimeProperty(Property):
    def __init__(self, kwargs):
        super().__init__(kwargs)
        self.last_edited_time = self.meta.pop('last_edited_time', None)
        self.set_value(self.last_edited_time)


class EmojiIconProperty(Property):
    def __init__(self, kwargs):
        super().__init__(kwargs)
        self.name = 'icon'
        self.emoji = self.meta.pop('emoji', None)
        self.set_value(self.emoji)

class DateProperty(Property):
    def __init__(self, kwargs):
        super().__init__(kwargs)
        self.date = self.meta.pop('date', None)
        self.set_value(self.date)

class EmailProperty(Property):
    def __init__(self, kwargs):
        super().__init__(kwargs)
        self.email = self.meta.pop('email', None)
        self.set_value(self.email)

class PhoneNumberProperty(Property):
    def __init__(self, kwargs):
        super().__init__(kwargs)
        self.phone_number = self.meta.pop('phone_number', None)
        self.set_value(self.phone_number)

class URLProperty(Property):
    def __init__(self, kwargs):
        super().__init__(kwargs)
        self.url = self.meta.pop('url', None)
        self.set_value(self.url)


class RelationProperty(Property):
    def __init__(self, kwargs):
        super().__init__(kwargs)
        self.relation = self.meta.pop('relation', [])
        self.set_value(self.relation)


class ChildPageTitle(NotionBase):
    def __init__(self, title):
        self.title = title