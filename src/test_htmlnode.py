import unittest
from htmlnode import HTMLNode, LeafNode


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

if __name__ == '__main__':
    unittest.main()