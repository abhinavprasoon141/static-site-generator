# src/test_htmlnode.py

import unittest
from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_single_prop(self):
        node = HTMLNode(
            tag="a",
            props={"href": "https://www.google.com"}
        )
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com"')

    def test_props_to_html_multiple_props(self):
        node = HTMLNode(
            tag="a",
            props={
                "href": "https://www.boot.dev",
                "target": "_blank",
                "rel": "noopener"
            }
        )
        # The order of attributes in the output string might vary depending on Python's dictionary iteration order
        # which is insertion-ordered for Python 3.7+
        # We'll test against both possible orders if necessary, or sort for consistent testing.
        expected1 = ' href="https://www.boot.dev" target="_blank" rel="noopener"'
        expected2 = ' target="_blank" href="https://www.boot.dev" rel="noopener"'
        expected3 = ' rel="noopener" href="https://www.boot.dev" target="_blank"' # etc.

        # A more robust way to test for unordered attributes is to convert to a set of key-value pairs
        # but for this specific output format with leading space, we'll check individual parts.
        # However, for dicts, Python 3.7+ preserves insertion order, so the first expected will likely be consistent.
        actual_output = node.props_to_html()
        self.assertIn(' href="https://www.boot.dev"', actual_output)
        self.assertIn(' target="_blank"', actual_output)
        self.assertIn(' rel="noopener"', actual_output)
        self.assertTrue(actual_output.startswith(' ')) # Check leading space
        self.assertEqual(len(actual_output.split()), 3) # Check number of attributes

    def test_props_to_html_no_props(self):
        node = HTMLNode(tag="p", value="Hello")
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_empty_props_dict(self):
        node = HTMLNode(tag="div", props={})
        self.assertEqual(node.props_to_html(), "")

    def test_repr_method(self):
        node_no_children = HTMLNode(tag="p", value="Hello", props={"class": "my-paragraph"})
        expected_repr_no_children = "HTMLNode(tag='p', value='Hello', children=None, props={'class': 'my-paragraph'})"
        self.assertEqual(repr(node_no_children), expected_repr_no_children)

        node_with_children = HTMLNode(tag="div", children=[HTMLNode(tag="span", value="child")], props={"id": "parent"})
        expected_repr_with_children_start = "HTMLNode(tag='div', value='None', children=[HTMLNode(tag='span', value='child', children=None, props=None)], props={'id': 'parent'})"
        self.assertEqual(repr(node_with_children), expected_repr_with_children_start)

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com" target="_blank">Click me!</a>')

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "This is raw text.")
        self.assertEqual(node.to_html(), "This is raw text.")

    def test_leaf_to_html_empty_props(self):
        node = LeafNode("span", "Just a span.", {})
        self.assertEqual(node.to_html(), "<span>Just a span.</span>")

    def test_leaf_to_html_value_error(self):
        # Test constructor's ValueError
        with self.assertRaises(ValueError):
            LeafNode("div", None)

if __name__ == '__main__':
    unittest.main()
