import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        test_dict = dict({"href": "https://www.google.com", "target": "_blank",})
        node = HTMLNode("p", "This is a test node")
        node2 = HTMLNode("a", "This is a test node", [node], test_dict)
        node3 = HTMLNode()
        
        self.assertEqual(' href="https://www.google.com" target="_blank"', node2.props_to_html())
        node2.__repr__()
        node3.__repr__()



if __name__ == "__main__":
    unittest.main()