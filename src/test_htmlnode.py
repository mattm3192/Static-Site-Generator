import unittest

from htmlnode import HTMLNode, LeafNode

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

	def test_leaf_to_html_p(self):
		node = LeafNode("p", "Hello, world!")
		self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

	def test_leaf_to_html_link(self):
		props = {"href": "https://www.google.com"}
		node = LeafNode("a", "Google time!!", props)
		self.assertEqual(node.to_html(), '<a href="https://www.google.com">Google time!!</a>')

if __name__ == "__main__":
    unittest.main()