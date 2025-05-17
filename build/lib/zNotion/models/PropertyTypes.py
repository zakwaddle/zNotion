from project_package.zNotion.models.RichText import RichText
from project_package.zNotion.models.Property import Property, ChildPageTitle
from project_package.zNotion.models.Option import Option
from yell import yell


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

