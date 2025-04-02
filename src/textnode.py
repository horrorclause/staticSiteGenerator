from enum import Enum

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():
    def __init__(self,text,text_type,url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    # Checks to see if one node is equal to another
    def __eq__(self, value):
        if not isinstance(value, TextNode):
            return False
        
        return (
                self.text == value.text
                and 
                self.text_type == value.text_type
                and
                self.url == value.url
                )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


    def handle_textType(text,text_type):
        match text_type:
            case TextType.BOLD_TEXT:
                return bold(text)
            case TextType.ITALIC_TEXT:
                return italic(text)
            case TextType.CODE_TEXT(text):
                return code(text)
        
# TODO: Below is for later.
def bold(text):
    return f'<b>{text.strip("**")}</b>'

def italic(text):
    return f'<i>{text.strip("_")}</i>'

def code(text):
    return f"<code>{text.strip('`')}</code>"
