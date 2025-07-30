from typing import List, Dict, Optional

class HTMLNode:
    def __init__(self, tag: str = None, value: str = None, children: list = None, props: dict = None): #type: ignore
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

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

    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value.")

        if self.tag is None:
            return self.value
        else:
            props_str = self.props_to_html() # Get the attributes string
            return f"<{self.tag}{props_str}>{self.value}</{self.tag}>"
