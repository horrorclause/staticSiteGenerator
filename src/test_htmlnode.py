import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_eq_props(self):
        node = HTMLNode("p","This will have a link", None, {"href": "https://www.google.com"})
        result = node.props_to_html()

        self.assertEqual(result, 'href="https://www.google.com"')

    def test_not_eq_props(self):
        node = HTMLNode("a",None,None,{"href": "https://www.google.com", "target": "_blank"})
        result = node.props_to_html()
        self.assertNotEqual(result, 'href="https://www.google.com"target="_blank"')

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, World!")
        self.assertEqual(node.to_html(), "<p>Hello, World!</p>")

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, World!")
        self.assertEqual(node.to_html(), "Hello, World!")

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

    def test_parent_with_single_child(self):
        child = LeafNode("b", "text")
        parent = ParentNode("div", [child])
        self.assertEqual(parent.to_html(), "<div><b>text</b></div>")

    def test_parent_with_multiple_children(self):
        child1 = LeafNode("b", "bold")
        child2 = LeafNode("i", "italic")
        parent = ParentNode("p", [child1, child2])
        self.assertEqual(parent.to_html(), "<p><b>bold</b><i>italic</i></p>")

    def test_nested_parents(self):
        grandchild = LeafNode("span", "hello")
        child = ParentNode("div", [grandchild])
        parent = ParentNode("section", [child])
        self.assertEqual(parent.to_html(), "<section><div><span>hello</span></div></section>")

    def test_missing_tag(self):
        with self.assertRaises(ValueError):
            ParentNode(None, [LeafNode("b", "text")]).to_html()

    def test_missing_children(self):
        with self.assertRaises(ValueError):
            ParentNode("div", None).to_html()

if __name__ == '__main__':
    unittest.main()