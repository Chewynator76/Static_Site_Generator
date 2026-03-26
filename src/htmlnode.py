

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError("a base HTML node can't become HTML")
    
    def props_to_html(self):
        if self.props is None:
            return ""
        return_string = ""
        for key in self.props:
            return_string += f' {key}="{self.props[key]}"'
        return return_string
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super(LeafNode, self).__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError("no value was found")
        if self.tag is None:
            return self.value
        if self.props is None:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        else:
            return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
    
    def __repr__(self):
        return (f"tag={self.tag}, value={self.value}, props={self.props}")

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super(ParentNode, self).__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag is None:
            raise ValueError("no tag was found")
        if self.children is None:
            raise ValueError("the parent node has no children, relatable")
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
        
        nice_string = f"{self.tag}"
        for string in children_tag:
            nice_string += string
        return nice_string + f"/{self.tag}"
