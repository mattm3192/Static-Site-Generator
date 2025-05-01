import unittest

from htmlnode import ParentNode, LeafNode

class TestHTMLNode(unittest.TestCase):
	def test_to_html_with_children(self):
		child_node = LeafNode("span", "child")
		parent_node = ParentNode("div", [child_node])
		self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

	def test_to_html_with_grandchildren(self):
		grandchild_node = LeafNode("b", "grandchild")
		child_node = ParentNode("span", [grandchild_node])
		parent_node = ParentNode("div", [child_node])
		self.assertEqual(
			parent_node.to_html(),
			"<div><span><b>grandchild</b></span></div>",
		)

	def test_to_html_with_greatgrandchildren(self):
		props = {"href": "https://www.greatgrandkids_portfolio.com"}
		great_grandchild_node = LeafNode("a", "Link", props)
		grandchild_node = ParentNode("p", [great_grandchild_node])
		child_node = ParentNode("span", [grandchild_node])
		parent_node = ParentNode("h1", [child_node])
		self.assertEqual(parent_node.to_html(), '<h1><span><p><a href="https://www.greatgrandkids_portfolio.com">Link</a></p></span></h1>')

	def test_to_html_with_multiple_grandchildren(self):
		grandchild_node = LeafNode("b", "grandchild")
		grandchild_node2 = LeafNode("b", "grandchild")
		child_node = ParentNode("span", [grandchild_node])
		child_node2 = ParentNode("span", [grandchild_node2])
		parent_node = ParentNode("div", [child_node, child_node2])
		self.assertEqual(parent_node.to_html(), "<div><span><b>grandchild</b></span><span><b>grandchild</b></span></div>")

if __name__ == "__main__":
    unittest.main()