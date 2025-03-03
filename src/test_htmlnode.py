import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
	def test_repr(self):
		node = HTMLNode("h1","Title")
		self.assertTrue("h1" in repr(node))
		self.assertTrue("Title" in repr(node))

	def test_props_to_html(self):
		props = {"href": "https://www.google.com","target": "_blank",}
		node = HTMLNode("a", "Here is a link to google.", None, props)
		props_html = node.props_to_html()
		self.assertTrue(' href="https://www.google.com"' in props_html)
		self.assertTrue(' target="_blank"' in props_html)
	
	def test_props_to_html_empty(self):
		node = HTMLNode("p", "A paragraph with no attributes")
		self.assertEqual("", node.props_to_html())

if __name__ == "__main__":
    unittest.main()