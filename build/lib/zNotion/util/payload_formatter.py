from ..yell import yell
from ..models import RichText, Block, Option, Page, Children, Parent
from ..models.Query import (
    Query, FilterQuery, FilterProperty, FilterCombiner, Sort, NullFilter,
    )
from ..models.Properties import (
    Properties, TitleProperty, TextProperty, NumberProperty, CheckboxProperty,
    SelectProperty, MultiSelectProperty, CreatedTimeProperty, LastEditedTimeProperty,
    EmojiIconProperty, PhoneNumberProperty, URLProperty, EmailProperty, DateProperty, ChildPageTitle
    )

# |--------------------------------------------------------------------------------| #


class PayloadFormatter:
    """Stateless formatter for Notion API payloads."""
    
    @staticmethod
    def format(obj):
        yell("formatting: ", obj)
        if isinstance(obj, dict):
            raise TypeError(f"Error in Formatting - Cant format a dict, must be a zNotion obj")
        if isinstance(obj, ChildPageTitle):
            return 	{"properties": {		
                        "title": [
                            {
                                "text": {
                                    "content": obj.title
                                }
                            }
                        ]
                    }}
        if isinstance(obj, Properties):
            return {"properties": {
                prop.name: PayloadFormatter.format_property(prop)[prop.name]
                for prop in obj
                if prop.value is not None
            }}
        if isinstance(obj, Children):
            yell("formatting children...")
            return {"children" : [
                PayloadFormatter.format_block(block)
                for block in obj._blocks
            ]} if obj._blocks else {}
        if isinstance(obj, Query):
            return PayloadFormatter.format_query(obj)
        for fn in (
            PayloadFormatter.format_object,
            PayloadFormatter.format_property,
        ):
            try:
                return fn(obj)
            except TypeError:
                continue
        raise TypeError(f"Unsupported type: {type(obj)}")


    @staticmethod
    def format_object(obj):
        from ..NotionPage import NotionPage
        from ..NotionBlock import NotionBlock
        if isinstance(obj, NotionPage):
            return PayloadFormatter.format_page(obj.page)
        if isinstance(obj, NotionBlock):
            return PayloadFormatter.format_block(obj.block)
        if isinstance(obj, RichText):
            return PayloadFormatter.format_rich_text(obj)
        if isinstance(obj, Block):
            return PayloadFormatter.format_block(obj)
        if isinstance(obj, Option):
            return PayloadFormatter.format_option(obj)
        if isinstance(obj, Page):
            return PayloadFormatter.format_page(obj)
        if isinstance(obj, Parent):
            return PayloadFormatter.format_parent(obj)
        else:
            raise TypeError(f'unsupported object type: {type(obj)}')
    

    @staticmethod
    def format_property(prop):
        if isinstance(prop, TitleProperty):
            return PayloadFormatter.format_title_prop(prop)
        if isinstance(prop, TextProperty):
            yell("TextProp!")
            return PayloadFormatter.format_text_prop(prop)
        if isinstance(prop, NumberProperty):
            return PayloadFormatter.format_number_prop(prop)
        if isinstance(prop, CheckboxProperty):
            return PayloadFormatter.format_checkbox_prop(prop)
        if isinstance(prop, SelectProperty):
            return PayloadFormatter.format_select_prop(prop)
        if isinstance(prop, MultiSelectProperty):
            return PayloadFormatter.format_multi_select_prop(prop)
        if isinstance(prop, CreatedTimeProperty):
            return PayloadFormatter.format_created_time_prop(prop)
        if isinstance(prop, LastEditedTimeProperty):
            return PayloadFormatter.format_last_edited_time_prop(prop)
        if isinstance(prop, EmojiIconProperty):
            return PayloadFormatter.format_emoji_icon_prop(prop)
        if isinstance(prop, DateProperty):
            return PayloadFormatter.format_date_prop(prop)
        if isinstance(prop, URLProperty):
            return PayloadFormatter.format_url_prop(prop)
        if isinstance(prop, EmailProperty):
            return PayloadFormatter.format_email_prop(prop)
        if isinstance(prop, PhoneNumberProperty):
            return PayloadFormatter.format_phone_number_prop(prop)
        else:
            raise TypeError(f'unsupported property type: {type(prop)}')
    
    @staticmethod
    def format_query_filter(query_filter: FilterQuery):
        
        
        if isinstance(query_filter, FilterCombiner):
            yell(f"is FilterCombiner - {query_filter}")
            return {query_filter.op: [PayloadFormatter.format_query_filter(f) for f in query_filter.filters]}
        
        if isinstance(query_filter, FilterProperty):
            yell(f"is FilterProperty - {query_filter}")
            return {"property": query_filter.key, 
                    query_filter.type: {
                        query_filter.op: query_filter.value
                        }}
    @staticmethod
    def format_query_sort(query_sorts: Sort):
        return {"property":query_sorts.property, "direction": query_sorts.direction}

    @staticmethod
    def format_query(query: Query):
        yell("format_query:", query)
        filters = {}
        if not isinstance(query.filter, NullFilter):
            filters = {"filter": PayloadFormatter.format_query_filter(query.filter)}
        sorts = {"sorts": [PayloadFormatter.format_query_sort(s) for s in query.sorts]} if query.sorts else {}
        limit = {"page_size": query.limit}
        payload = {**filters, **sorts, **limit}
        yell("payload: ", payload)
        return payload
        
    @staticmethod
    def format_parent(parent: Parent):
        return {"parent":
                {"type": parent.type,
                 parent.type: parent.id}}

    @staticmethod
    def format_rich_text(rich_text: RichText):
        yell("in format_rich_text!!", rich_text)
        if isinstance(rich_text, RichText):
            yell("its a RichText...")
            if isinstance(rich_text, list):
                yell("it's a list...")

            link = rich_text.link
            value = rich_text.value
            annotations = rich_text.annotations
            block = {
                "type": "text",
                "text": {
                    "content": value,
                    "link": {"url": link} if link else None
                },
                "annotations": annotations or {}
            }
            if not link:
                del block["text"]["link"]
            return block

    @staticmethod
    def format_option(option: Option):
        name = option.name
        id_ = option.id
        color = option.color
        description = option.description
        return {
            "name": name, 
            "id": id_, 
            "color": color,
            "description": description}

    @staticmethod
    def format_block(block: Block):
        yell("in format_block")
        block_type = block.type
        if block_type in ("link_to_page"):
            page_id = block.meta.get("page_id")
            payblock = {
                # "object": "block",
                "type": block_type,
                block_type: {
                    "type": "page_id",
                    "page_id": page_id
                }
            }
            yell(block_type, payblock)
            return payblock
        if block_type in ("child_database", "child_page"):
            title = block.meta.get("title")
            payblock = {
                # "object": "block",
                "type": block_type,
                block_type: {
                    "title": title
                }
            }
            yell(block_type, payblock)
            return payblock
        if block_type in ("table_of_contents", "divider"):
            color = block.meta.get('color')
            color = {"color": color} if color is not None else {}
            payblock = {
                "object": "block",
                "type": block_type,
                block_type: color
            }
            yell(block_type, payblock)
            return payblock
        yell("block_type:", block_type)
        yell("block.text=", repr(block.text))
        if isinstance(block.text, list) and block.text and isinstance(block.text[0], RichText):
            text = []
            for rt in block.text:
                yell("in the loop, formatting: ", rt, is_loop=True, loop_lvl=2)
                ft = PayloadFormatter.format_rich_text(rt)
                yell("formatted rich_text: ", ft, is_loop=True, loop_lvl=2)
                text.append(ft)
                
        else:
            text = [PayloadFormatter.format(block.text)]

        yell("at this point, text is: ", text)
        yell("block meta:", block.meta)
        meta = block.meta if block.meta else {}
        # children = {}
        yell("format_block:", block)
        # if block.is_container:
            # children = {"children":PayloadFormatter.format(block.children)}
        return {
            "object": "block",
            "type": block_type,
            block_type: {
                "rich_text": text,
                **meta,
                # **children
            }
        }
    
    @staticmethod
    def format_page(page: Page):
        id_=page.id
        title = page.title
        props = {PayloadFormatter.format_property(p) for p in page.properties}
        return {
            "object": "page",
            "id": id_,
            "title": title,
            "properties": props,
            "url": page.url
        }
    
    @staticmethod
    def format_emoji_icon_prop(emoji_prop: EmojiIconProperty):
        value = emoji_prop.value
        return {"icon": {
                    "type": "emoji",
                    "emoji": value
                    }}
    
    @staticmethod
    def format_title_prop(title_prop: TitleProperty):
        name = title_prop.name
        text = title_prop.value
        return {
            name: {
                "title": [{
                    "type": "text",
                    "text": {"content": text}}
                    ]}}

    @staticmethod
    def format_text_prop(text_prop: TextProperty):
        name = text_prop.name
        yell(text_prop.name)
        yell(type(text_prop.value))
        if isinstance(text_prop.value, list):
            yell("Yep, it's a list")
        text = text_prop.value or ""
        yell(name)
        return {
            name: {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": text}
                }]
            }
        }
    
    @staticmethod
    def format_number_prop(number_prop: NumberProperty, add_format=False):
        name = number_prop.name
        number = number_prop.value
        val = {"number": number}
        num_type = number_prop.format
        if add_format and num_type is not None:
            val.update({'format': num_type})
        return {name: val}
    
    @staticmethod
    def format_select_prop(select_prop: SelectProperty):
        option = select_prop.value
        name = select_prop.name
        if not option:
            return {}
        if isinstance(option, Option):
            option = PayloadFormatter.format_option(option)
        return {
            name: {
                "select": {"name": option}
            }
        }
    
    @staticmethod
    def format_multi_select_prop(multi_select_prop: MultiSelectProperty):
        options = multi_select_prop.value
        name = multi_select_prop.name

        def check_option(o):
            return PayloadFormatter.format_option(o) if isinstance(o, Option) else {"name": o}
            
        if not options:
            return {}
        if isinstance(options, list):
            options = [check_option(opt) for opt in options]
        return {
            name: {
                "multi_select": [options] if not isinstance(options, list) else options
            }
        }
    
    @staticmethod
    def format_created_time_prop(_=None):
        return {}  # Notion manages this field automatically
    
    
    @staticmethod
    def format_last_edited_time_prop(_=None):
        return {}  # Notion manages this field automatically
    
    @staticmethod
    def format_checkbox_prop(checkbox_prop: CheckboxProperty):
        name = checkbox_prop.name
        checked = bool(checkbox_prop.value)
        return {
            name: {
                "checkbox": bool(checked)
            }
        }
    
    @staticmethod
    def format_date_prop(date_prop: DateProperty):
        name = date_prop.name
        date = date_prop.value
        return {
            name: {
                "date": date
            }
        }

    @staticmethod
    def format_email_prop(email_prop: EmailProperty):
        name = email_prop.name
        email = email_prop.value or ""
        return {
            name: {
                "email": email
            }
        }

    @staticmethod
    def format_phone_number_prop(phone_prop: PhoneNumberProperty):
        name = phone_prop.name
        number = phone_prop.value or ""
        return {
            name: {
                "phone_number": number
            }
        }

    @staticmethod
    def format_url_prop(url_prop: URLProperty):
        name = url_prop.name
        url = url_prop.value or ""
        return {
            name: {
                "url": url
            }
        }