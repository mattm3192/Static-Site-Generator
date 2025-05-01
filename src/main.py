from textnode import *
from htmlnode import *

def main():
	string = "This is a text node"
	string_type = TextType.BOLD
	url = "https:www.boot.dev"
	node = TextNode(string, string_type, url)
	print(node)

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


main()