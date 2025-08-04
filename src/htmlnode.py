from typing import List, Dict, Optional
SELF_CLOSING_TAGS = ["img", "br", "hr", "input", "link", "meta", "param", "embed", "area", "base", "col", "source", "track", "keygen"]
class HTMLNode:
    def __init__(self, tag: str = None, value: str = None, children: list = None, props: dict = None): #type: ignore
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __eq__(self, other):
            if not isinstance(other, HTMLNode):
                return NotImplemented
            # Compare all relevant attributes for equality
            return (
                self.tag == other.tag and
                self.value == other.value and
                self.children == other.children and
                self.props == other.props
            )

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self):
        if self.props is None:
                   return ""

        html_attributes = []
        for key, value in self.props.items():
            html_attributes.append(f'{key}="{value}"')

        return " " + " ".join(html_attributes) if html_attributes else ""


    def __repr__(self):
        return (
            f"HTMLNode(tag='{self.tag}', value='{self.value}', "
            f"children={self.children}, props={self.props})"
        )

class LeafNode(HTMLNode):
    def __init__(self, tag: Optional[str], value: str, props: Optional[Dict[str, str]] = None): #type: ignore
        super().__init__(tag=tag, value=value, children=None , props=props) #type: ignore
        if self.value is None:
            raise ValueError("All leaf nodes must have a value.")

    def to_html(self) -> str:
            if self.value is None:
                raise ValueError("LeafNode must have a value to render to HTML")

            if self.tag is None:
                return self.value
            else:
                props_str = self.props_to_html()
                # --- FIX: Handle self-closing tags ---
                if self.tag.lower() in SELF_CLOSING_TAGS: # Use .lower() for case-insensitivity
                    return f"<{self.tag}{props_str}>"
                else:
                    return f"<{self.tag}{props_str}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: List[HTMLNode], props: Optional[Dict[str, str]] = None):
        # ParentNode requires tag and children, does not take a value
        # value is implicitly None for ParentNode
        super().__init__(tag=tag, value=None, children=children, props=props) #type: ignore

        if self.tag is None:
            raise ValueError("ParentNode must have tag")
        if self.children is None or len(self.children) == 0:
            raise ValueError("ParentNode must have children")

    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("ParentNode must have a tag to render to HTML")
        if self.children is None or len(self.children) == 0:
            raise ValueError("ParentNode must have children to render to HTML")

        children_html = ""
        for child in self.children:
            children_html += child.to_html()

        props_str = self.props_to_html()
        return f"<{self.tag}{props_str}>{children_html}</{self.tag}>"
