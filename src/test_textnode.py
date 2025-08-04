import unittest

from enum import Enum
from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import HTMLNode, ParentNode, LeafNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text_node_to_html_node_text(self):
        text_node = TextNode("This is plain text", TextType.TEXT)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node, LeafNode(None, "This is plain text"))
        self.assertEqual(html_node.to_html(), "This is plain text")

    def test_text_node_to_html_node_bold(self):
        text_node = TextNode("This is bold text", TextType.BOLD)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node, LeafNode("b", "This is bold text"))
        self.assertEqual(html_node.to_html(), "<b>This is bold text</b>")

    def test_text_node_to_html_node_italic(self):
        text_node = TextNode("This is italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node, LeafNode("i", "This is italic text"))
        self.assertEqual(html_node.to_html(), "<i>This is italic text</i>")

    def test_text_node_to_html_node_code(self):
        text_node = TextNode("This is code", TextType.CODE)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node, LeafNode("code", "This is code"))
        self.assertEqual(html_node.to_html(), "<code>This is code</code>")

    def test_text_node_to_html_node_link(self):
        text_node = TextNode("Google", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node, LeafNode("a", "Google", {"href": "https://www.google.com"}))
        self.assertEqual(html_node.to_html(), '<a href="https://www.google.com">Google</a>')

    def test_text_node_to_html_node_image(self):
        text_node = TextNode("An image alt text", TextType.IMAGE, "https://example.com/image.jpg")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node, LeafNode("img", "", {"src": "https://example.com/image.jpg", "alt": "An image alt text"}))
        self.assertEqual(html_node.to_html(), '<img src="https://example.com/image.jpg" alt="An image alt text">')

    def test_text_node_to_html_node_link_no_url_error(self):
        text_node = TextNode("Google", TextType.LINK, None)
        with self.assertRaisesRegex(ValueError, "Link TextNode must have a URL"):
            text_node_to_html_node(text_node)

    def test_text_node_to_html_node_image_no_url_error(self):
        text_node = TextNode("An image alt text", TextType.IMAGE, None)
        with self.assertRaisesRegex(ValueError, "Image TextNode must have a URL"):
            text_node_to_html_node(text_node)

    def test_text_node_to_html_node_unknown_type_error(self):
        # Create a dummy TextType that's not in our enum for testing
        class UnknownTextType(Enum):
            UNKNOWN = "unknown"

        # Temporarily create a TextNode with this unknown type
        text_node = TextNode("Unknown content", UnknownTextType.UNKNOWN)

        with self.assertRaisesRegex(ValueError, "Unknown TextType: UnknownTextType.UNKNOWN"):
            text_node_to_html_node(text_node)


if __name__ == "__main__":
    unittest.main()
