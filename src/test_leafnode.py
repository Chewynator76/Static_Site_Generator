import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        test_dict_no_target = dict({"href": "https://www.google.com",})
        nodel = LeafNode("p", "Hello, world!")
        nodel2 = LeafNode("a", "Click me!", test_dict_no_target)
        try:
            nodel3 = LeafNode()
        except:
            pass
        self.assertEqual(nodel.to_html(), "<p>Hello, world!</p>")
        self.assertEqual(nodel2.to_html(), '<a href="https://www.google.com">Click me!</a>')



if __name__ == "__main__":
    unittest.main()