'''
"HTMLNode" class will represent a "node" in an HTML document tree 
(like a <p> tag and its contents, or an <a> tag and its contents).
It can be block level or inline, and is designed to only output HTML.
'''

class HTMLNode():
    def __init__(self,tag=None,value=None,children=None,props=None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")
    
    def props_to_html(self):
        if self.props is None:
            return ""
        
        attributes = []
        for key,value in self.props.items():
            attributes.append(f'{key}="{value}"')
        return " ".join(attributes)
    
    def __repr__(self):
        return f'HTMLNode({repr(self.tag)}, {repr(self.value)}, {repr(self.children)}, {repr(self.props)})'
    
