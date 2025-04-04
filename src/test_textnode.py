import unittest
from textnode import TextType, TextNode
from splitDelimiter import split_node_delimiter

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2= TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node,node2)

    def test_notEqual(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This should be a link", TextType.LINK, "https://example.com")
        self.assertNotEqual(node,node2)
    
    def test_notEqual2(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This should be a link", TextType.TEXT)
        self.assertNotEqual(node,node2)

    def test_eq_url(self):
        node = TextNode("some alt text", TextType.LINK, "http://example.com")
        node2 = TextNode("some alt text", TextType.LINK, "http://example.com")
        self.assertEqual(node, node2)

    def test_not_eq_url(self):
        node = TextNode("some alt text", TextType.LINK, "http://example.com")
        node2 = TextNode("some alt text2", TextType.TEXT, "http://example.com")
        self.assertNotEqual(node, node2)

    # Tests the __repr__ method in textnode
    def text_repr(self):
        node = TextNode("This is a text node", TextType.TEXT, "https://www.example.org")
        self.assertEqual("TextNode(This is a text node, text, https://www.boot.dev)", repr(node))

    # -------- Adding Tests for split_node_delimiter --------

    def test_basic_single_delimiter(self):
        node = TextNode("This is `code`.", TextType.TEXT)
        result = split_node_delimiter([node], "`", TextType.CODE)
        expected_result = [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(".", TextType.TEXT)
        ]

if __name__ == '__main__':
    unittest.main()