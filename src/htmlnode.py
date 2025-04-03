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
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, [], props)

    def to_html(self):
        if self.value is None:
            raise ValueError("leaf node must have a value.")
        
        if self.tag is None:
            return self.value
        
        # Get HTML attributes string (like class="intro" href="link")
        props_html = self.props_to_html()
        
        if props_html:
            props_html = " " + props_html

        #Construct and return the full HTML tag
        return f"<{self.tag}{props_html}>{self.value}</{self.tag}>"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("there is no tag.")

        if (self.children is None) or (len(self.children)==0):
            raise ValueError("there are no children")
        
        children_html = ""
        for child in self.children:
            children_html += child.to_html()

        # If props exist, format with them
        props_html = self.props_to_html()
        if props_html:
            props_html = " "+props_html

        return f"<{self.tag}{props_html}>{children_html}</{self.tag}>"