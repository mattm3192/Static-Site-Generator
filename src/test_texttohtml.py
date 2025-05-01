import unittest

from main import text_node_to_html_node
from textnode import *
from htmlnode import *

class TexttoHTMLTests(unittest.TestCase):
	def test_text_text_to_html_raw(self):
		node = TextNode("This is a text node", TextType.NORMAL)
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, None)
		self.assertEqual(html_node.value, "This is a text node")
        
	def test_text_text_to_html_bold(self):
		node = TextNode("This is a bolded text node", TextType.BOLD)
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, "b")
		self.assertEqual(html_node.value, "This is a bolded text node")
        
	def test_text_text_to_html_italic(self):
		node = TextNode("This is an italic text node", TextType.ITALIC)
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, "i")
		self.assertEqual(html_node.value, "This is an italic text node")

	def test_text_text_to_html_code(self):
		node = TextNode("This is a code text node", TextType.CODE)
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, "code")
		self.assertEqual(html_node.value, "This is a code text node")

	def test_text_text_to_html_link(self):
		node = TextNode("This is a link text node", TextType.LINKS, "https://www.google.com")
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, "a")
		self.assertEqual(html_node.value, "This is a link text node")
		self.assertEqual(html_node.props, {"href":"https://www.google.com"})

	def test_text_text_to_html_image(self):
		node = TextNode("This is an image text node", TextType.IMAGES, "https://www.google.com")
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, "img")
		self.assertEqual(html_node.value, "")
		self.assertEqual(html_node.props, {"src":"https://www.google.com", "alt":"This is an image text node" })

if __name__ == "__main__":
    unittest.main()