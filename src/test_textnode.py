import unittest

from enum import Enum
from textnode import TextNode, TextType, text_node_to_html_node, split_nodes_delimiter
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

class TestInlineMarkdown(unittest.TestCase):
    def test_split_delimiter_single_match(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0], TextNode("This is text with a ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("code block", TextType.CODE))
        self.assertEqual(new_nodes[2], TextNode(" word", TextType.TEXT))

    def test_split_delimiter_multiple_matches(self):
        node = TextNode("This is text with a `code` and another `code`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 5)
        self.assertEqual(new_nodes[0], TextNode("This is text with a ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("code", TextType.CODE))
        self.assertEqual(new_nodes[2], TextNode(" and another ", TextType.TEXT))
        self.assertEqual(new_nodes[3], TextNode("code", TextType.CODE))
        self.assertEqual(new_nodes[4], TextNode("", TextType.TEXT)) # empty string after last delimiter

    def test_split_delimiter_multiple_matches_no_trailing(self):
        node = TextNode("`code` and `more code`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

                # --- FIX: Change the assertion from 4 to 5 ---
        self.assertEqual(len(new_nodes), 5)

        self.assertEqual(new_nodes[0], TextNode("", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("code", TextType.CODE))
        self.assertEqual(new_nodes[2], TextNode(" and ", TextType.TEXT))
        self.assertEqual(new_nodes[3], TextNode("more code", TextType.CODE))
        self.assertEqual(new_nodes[4], TextNode("", TextType.TEXT))


    def test_split_delimiter_no_match(self):
        node = TextNode("This is just plain text.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0], node)

    def test_split_delimiter_bold(self):
        node = TextNode("This is text with a **bold** word.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0], TextNode("This is text with a ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("bold", TextType.BOLD))
        self.assertEqual(new_nodes[2], TextNode(" word.", TextType.TEXT))

    def test_split_delimiter_italic(self):
        node = TextNode("This is text with an _italic_ word.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0], TextNode("This is text with an ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("italic", TextType.ITALIC))
        self.assertEqual(new_nodes[2], TextNode(" word.", TextType.TEXT))

    def test_split_delimiter_mixed_list(self):
        node1 = TextNode("Plain text here.", TextType.TEXT)
        node2 = TextNode("This is text with a `code` section.", TextType.TEXT)
        node3 = TextNode("This node should not be changed.", TextType.BOLD)

        old_nodes = [node1, node2, node3]
        new_nodes = split_nodes_delimiter(old_nodes, "`", TextType.CODE)

        self.assertEqual(len(new_nodes), 5)
        self.assertEqual(new_nodes[0], node1)
        self.assertEqual(new_nodes[1], TextNode("This is text with a ", TextType.TEXT))
        self.assertEqual(new_nodes[2], TextNode("code", TextType.CODE))
        self.assertEqual(new_nodes[3], TextNode(" section.", TextType.TEXT))
        self.assertEqual(new_nodes[4], node3)

    def test_split_delimiter_unmatched_delimiter(self):
        node = TextNode("This is text with a `code block", TextType.TEXT)
        with self.assertRaisesRegex(ValueError, "unmatched delimiter"):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_split_delimiter_delimiter_at_start_and_end(self):
        node = TextNode("`Code block at start and end`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0], TextNode("", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("Code block at start and end", TextType.CODE))
        self.assertEqual(new_nodes[2], TextNode("", TextType.TEXT))


if __name__ == "__main__":
    unittest.main()
