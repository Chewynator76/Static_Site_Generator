

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props == None or len(self.props) == 0:
            return ""
        if "href" not in self.props and "target" not in self.props:
            return ""
        if "href" not in self.props:
            return f' target="{self.props['target']}"'
        if "target" not in self.props:
            return f' href="{self.props["href"]}"'
        return f' href="{self.props["href"]}" target="{self.props["target"]}"'
    
    def __repr__(self):
        if self.children == None:
            children_thing = ""
        else:
            children_thing = str(self.children)
        return (f"tag={self.tag}, value={self.value}, children={children_thing}, props={self.props}")
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super(LeafNode, self).__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value == None:
            raise ValueError("no value was found") from None
        if self.tag == None:
            return self.value
        if self.props == None:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        else:
            return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
    
    def __repr__(self):
        return (f"tag={self.tag}, value={self.value}, props={self.props}")

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super(ParentNode, self).__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag == None:
            raise ValueError("no tag was found") from None
        if self.children == None:
            raise ValueError("the parent node has no children, relatable") from None
        children_tag = []
        for child in self.children:
            if self.value == None:
                raise ValueError("no value was found") from None
            if self.tag == None:
                children_tag.append(self.value)
            if self.props == None:
                children_tag.append(f"<{self.tag}>{self.value}</{self.tag}>")
            else:
                children_tag.append(f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>')
        
        nice_string = f"{self.tag}"
        for string in children_tag:
            nice_string += string
        return nice_string + f"/{self.tag}"
