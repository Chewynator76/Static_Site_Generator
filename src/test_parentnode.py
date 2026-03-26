import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

def test_to_html_with_children(self):
    child_node = LeafNode("span", "child")
    parent_node = ParentNode("div", [child_node])
    self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

def test_to_html_with_grandchildren(self):
    grandchild_node = LeafNode("b", "grandchild")
    child_node = ParentNode("span", [grandchild_node])
    parent_node = ParentNode("div", [child_node])
    self.assertEqual(
        parent_node.to_html(),
        "<div><span><b>grandchild</b></span></div>",
    )

def test_no_children(self):
    try:
        parent_node = ParentNode("This should fail")
        self.assertEqual(parent_node.to_html(), "<This should fail></This should fail>")
    except:
        pass

def test_many_children(self):
    child1 = LeafNode("a", "child1")
    child2 = LeafNode("b", "child2")
    child3 = LeafNode("c", "child3")
    child4 = LeafNode("d", "child4")
    child5 = LeafNode("e", "child5")
    parent = ParentNode("div", [child1, child2, child3, child4, child5])
    self.assertEqual(
        parent.to_html(),
        "<div><a>child1</a><b>child2</b><c>child3</c><d>child4</d><e>child5</d></div>"
    )