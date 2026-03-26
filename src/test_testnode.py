import unittest

from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode
from textnode_to_htmlnode import text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        node3 = TextNode(7, TextType.ITALIC)
        node4 = TextNode("This is a text node", 7)
        node5 = TextNode("This is a text node", TextType.ITALIC, None)
        self.assertEqual(node, node2)
        self.assertNotEqual(node3, node4, node5)
    
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

        node2 = TextNode("This is a text node", TextType.BOLD)
        html_node2 = text_node_to_html_node(node2).to_html()
        self.assertEqual(html_node2, "<b>This is a text node</b>")


if __name__ == "__main__":
    unittest.main()