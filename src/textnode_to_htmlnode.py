from htmlnode import HTMLNode, LeafNode
from textnode import TextNode, TextType

def text_node_to_html_node(text_node):
    if text_node.text_type not in TextType:
        raise Exception("text node does not have a text type")
    text = text_node.text
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode("a", text, dict({"href": text_node.props["href"],}))
    else:
        return LeafNode("img", "", dict({"scr": self.props["href"], "alt": text,}))
    
    