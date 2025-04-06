import unittest
from textnode import TextType, TextNode
from extractScripts import *

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

    # -------- Adding Tests for Markdown and Image Links  --------

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    # -------- Adding Tests for Splitnode Links and Images  --------

    def test_basic_image(self):
        node = TextNode("This is an ![image](https://example.com/img.png)", TextType.TEXT)
        result = split_nodes_image([node])
        self.assertListEqual([
            TextNode("This is an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://example.com/img.png")
        ], result)

    def test_multiple_images(self):
        node = TextNode("![First](img1.png) and ![Second](img2.png)", TextType.TEXT)
        result = split_nodes_image([node])
        self.assertListEqual([
            TextNode("First", TextType.IMAGE, "img1.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("Second", TextType.IMAGE, "img2.png")
        ], result)

    def test_no_images(self):
        node = TextNode("Just plain text", TextType.TEXT)
        result = split_nodes_image([node])
        self.assertListEqual([node], result)


if __name__ == '__main__':
    unittest.main()