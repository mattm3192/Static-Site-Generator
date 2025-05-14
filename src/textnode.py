from enum import Enum
from htmlnode import *

class TextType(Enum):
	NORMAL = "normal"
	BOLD = "bold"
	ITALIC = "italic"
	CODE = "code"
	LINKS = "links"
	IMAGES = "images"
	
class TextNode:
	def __init__(self, text, text_type, url=None):
		self.text = text
		self.text_type = text_type
		self.url = url

	def __eq__(self, text_node):
		return self.text == text_node.text and self.text_type == text_node.text_type and self.url == text_node.url
	
	def __repr__(self):
		return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
	
def text_node_to_html_node(text_node):
	match text_node.text_type:
		case TextType.NORMAL:
			return LeafNode(None, text_node.text)
		case TextType.BOLD:
			return LeafNode("b", text_node.text)
		case TextType.ITALIC:
			return LeafNode("i", text_node.text)
		case TextType.CODE:
			return LeafNode("code", text_node.text)
		case TextType.LINKS:
			props = {"href":text_node.url}
			return LeafNode("a", text_node.text, props)
		case TextType.IMAGES:
			props = {"src":text_node.url, "alt":text_node.text}
			return LeafNode("img", "", props)
		case _:
			raise Exception("Text node does not contain a valid text node type!")

	

