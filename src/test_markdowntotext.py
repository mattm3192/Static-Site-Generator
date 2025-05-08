import unittest

from markdowntotext import *
from textnode import *

class Markdowntotext(unittest.TestCase):
	def test_markdown_to_text_code(self):
		node = TextNode("This is text with a `code block` word", TextType.NORMAL)
		new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
		self.assertEqual(new_nodes[0].text_type, TextType.NORMAL)
		self.assertEqual(new_nodes[1].text_type, TextType.CODE)
		self.assertEqual(new_nodes[2].text_type, TextType.NORMAL)
		self.assertEqual(new_nodes[0].text, "This is text with a ")
		self.assertEqual(new_nodes[1].text, "code block")
		self.assertEqual(new_nodes[2].text, " word")
	
	def test_markdown_to_text_bold(self):
		node = TextNode("This is text with a **bold** word", TextType.NORMAL)
		new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
		self.assertEqual(new_nodes[0].text_type, TextType.NORMAL)
		self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
		self.assertEqual(new_nodes[2].text_type, TextType.NORMAL)
		self.assertEqual(new_nodes[0].text, "This is text with a ")
		self.assertEqual(new_nodes[1].text, "bold")
		self.assertEqual(new_nodes[2].text, " word")

	def test_markdown_to_text_italics(self):
		node = TextNode("This is text with an _italic_ word", TextType.NORMAL)
		new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
		self.assertEqual(new_nodes[0].text_type, TextType.NORMAL)
		self.assertEqual(new_nodes[1].text_type, TextType.ITALIC)
		self.assertEqual(new_nodes[2].text_type, TextType.NORMAL)
		self.assertEqual(new_nodes[0].text, "This is text with an ")
		self.assertEqual(new_nodes[1].text, "italic")
		self.assertEqual(new_nodes[2].text, " word")

	def test_markdown_to_text_oldnodes_multiple(self): #not finished
		old_nodes = []
		old_nodes.append(TextNode("This is text with an _italic_ word", TextType.NORMAL))
		old_nodes.append(TextNode("This is text with a **bold** word", TextType.NORMAL))
		old_nodes.append(TextNode("This is text with an _italic_", TextType.NORMAL))
		new_nodes = split_nodes_delimiter(old_nodes, "_", TextType.ITALIC)
		self.assertEqual(new_nodes[0].text_type, TextType.NORMAL)
		self.assertEqual(new_nodes[1].text_type, TextType.ITALIC)
		self.assertEqual(new_nodes[2].text_type, TextType.NORMAL)
		self.assertEqual(new_nodes[3].text_type, TextType.NORMAL)
		self.assertEqual(new_nodes[4].text_type, TextType.NORMAL)
		self.assertEqual(new_nodes[5].text_type, TextType.ITALIC)
		self.assertEqual(new_nodes[0].text, "This is text with an ")
		self.assertEqual(new_nodes[1].text, "italic")
		self.assertEqual(new_nodes[2].text, " word")
		self.assertEqual(new_nodes[3].text, "This is text with a **bold** word")
		self.assertEqual(new_nodes[4].text, "This is text with an ")
		self.assertEqual(new_nodes[5].text, "italic")
		newer_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
		self.assertEqual(newer_nodes[3].text_type, TextType.NORMAL)
		self.assertEqual(newer_nodes[4].text_type, TextType.BOLD)
		self.assertEqual(newer_nodes[3].text, "This is text with a ")
		self.assertEqual(newer_nodes[4].text, "bold")
		self.assertEqual(len(newer_nodes), 8)

	def test_markdown_to_text_unbalanced(self): #not finished
		node = TextNode("This is text with an **unbalanced delimiter", TextType.NORMAL)

		with self.assertRaises(Exception) as context:
			split_nodes_delimiter([node], "**", TextType.BOLD)

		self.assertTrue("unbalanced" in str(context.exception))

	def test_extract_markdown_images(self):
		text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
		matches = extract_markdown_images(text)
		self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

	def test_extract_markdown_images_multiple(self):
		text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![logo](https://www.google.com)"
		matches = extract_markdown_images(text)
		self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png"), ("logo", "https://www.google.com")], matches)

	def test_extract_markdown_links(self):
		text = "This is text with a link [to boot dev](https://www.boot.dev)"
		matches = extract_markdown_links(text)
		self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)

	def test_extract_markdown_links_multiple(self):
		text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com)"
		matches = extract_markdown_links(text)
		self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com")], matches)

	def test_extract_markdown_no_results_and_erroneous_results(self):
		text = "This is text with a link [to boot dev](https://www.boot.dev and an image [image](https://i.imgur.com/zjjcJKZ.png)"
		link_matches = extract_markdown_links(text)
		image_matches = extract_markdown_images(text)
		self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], link_matches)
		self.assertListEqual([], image_matches)

if __name__ == "__main__":
    unittest.main()