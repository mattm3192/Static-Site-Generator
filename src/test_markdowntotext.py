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

	def test_markdown_to_text_oldnodes_multiple(self):
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

	def test_markdown_to_text_unbalanced(self): 
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

	def test_split_images(self):
		node = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)", TextType.NORMAL)
		new_nodes = split_nodes_image([node])
		self.assertListEqual([TextNode("This is text with an ", TextType.NORMAL), 
						TextNode("image", TextType.IMAGES, "https://i.imgur.com/zjjcJKZ.png"),
						TextNode(" and another ", TextType.NORMAL),
						TextNode("second image", TextType.IMAGES, "https://i.imgur.com/3elNhQu.png"),
						], new_nodes)
		
	def test_split_images_no_images(self):
		node = TextNode("This is text with no images and one image with incorrect syntax [second image](https://i.imgur.com/3elNhQu.png)", TextType.NORMAL)
		new_nodes = split_nodes_image([node])
		self.assertListEqual([TextNode("This is text with no images and one image with incorrect syntax [second image](https://i.imgur.com/3elNhQu.png)", TextType.NORMAL)], new_nodes)
		
	def test_split_links(self):
		node = TextNode("This is text with a [link to google](https://www.google.com) and a second [link to boots](https://www.boot.dev) with text after.", TextType.NORMAL)
		new_nodes = split_nodes_links([node])
		self.assertListEqual([TextNode("This is text with a ", TextType.NORMAL), 
						TextNode("link to google", TextType.LINKS, "https://www.google.com"),
						TextNode(" and a second ", TextType.NORMAL),
						TextNode("link to boots", TextType.LINKS, "https://www.boot.dev"),
						TextNode(" with text after.", TextType.NORMAL),
						], new_nodes)
		
	def test_split_links_no_links(self):
		node = TextNode("This is text with a non link to google](https://www.google.com) and a second link that's incorrectly formatted as an image ![link to boots](https://www.boot.dev) with text after.", TextType.NORMAL)
		new_nodes = split_nodes_links([node])
		self.assertListEqual([TextNode("This is text with a non link to google](https://www.google.com) and a second link that's incorrectly formatted as an image ![link to boots](https://www.boot.dev) with text after.", TextType.NORMAL)], new_nodes)

	def test_split_links_and_images_multiple_nodes_with_blankspaces(self):
		node = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)     ", TextType.NORMAL)
		node1 = TextNode("This is text with no images and one image with incorrect syntax [second image](https://i.imgur.com/3elNhQu.png)", TextType.NORMAL)
		node2 = TextNode("     [link to google](https://www.google.com) and a second [link to boots](https://www.boot.dev) with text after.", TextType.NORMAL)
		node3 = TextNode("This is a non link to google](https://www.google.com) and a second link that's incorrectly formatted as an image ![link to boots](https://www.boot.dev) with text after.", TextType.NORMAL)
		new_nodes = split_nodes_links([node, node1, node2, node3])
		self.assertListEqual([TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)     ", TextType.NORMAL),
						TextNode("This is text with no images and one image with incorrect syntax ", TextType.NORMAL),
						TextNode("second image", TextType.LINKS, "https://i.imgur.com/3elNhQu.png"),
						TextNode("     ", TextType.NORMAL),
						TextNode("link to google", TextType.LINKS, "https://www.google.com"),
						TextNode(" and a second ", TextType.NORMAL),
						TextNode("link to boots", TextType.LINKS, "https://www.boot.dev"),
						TextNode(" with text after.", TextType.NORMAL),
						TextNode("This is a non link to google](https://www.google.com) and a second link that's incorrectly formatted as an image ![link to boots](https://www.boot.dev) with text after.", TextType.NORMAL)
						], new_nodes)

		newer_nodes = split_nodes_image(new_nodes)
		self.assertListEqual([TextNode("This is text with an ", TextType.NORMAL),
						TextNode("image", TextType.IMAGES, "https://i.imgur.com/zjjcJKZ.png"),
						TextNode(" and another ", TextType.NORMAL),
						TextNode("second image", TextType.IMAGES, "https://i.imgur.com/3elNhQu.png"),
						TextNode("     ", TextType.NORMAL),
						TextNode("This is text with no images and one image with incorrect syntax ", TextType.NORMAL),
						TextNode("second image", TextType.LINKS, "https://i.imgur.com/3elNhQu.png"),
						TextNode("     ", TextType.NORMAL),
						TextNode("link to google", TextType.LINKS, "https://www.google.com"),
						TextNode(" and a second ", TextType.NORMAL),
						TextNode("link to boots", TextType.LINKS, "https://www.boot.dev"),
						TextNode(" with text after.", TextType.NORMAL),
						TextNode("This is a non link to google](https://www.google.com) and a second link that's incorrectly formatted as an image ", TextType.NORMAL),
						TextNode("link to boots", TextType.IMAGES, "https://www.boot.dev"),
						TextNode(" with text after.", TextType.NORMAL),
						], newer_nodes)
		
	def test_text_to_textnode(self):
		text = "This is **bold text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
		new_nodes = text_to_textnodes(text)
		self.assertEqual([TextNode("This is ", TextType.NORMAL),
						TextNode("bold text", TextType.BOLD),
						TextNode(" with an ", TextType.NORMAL),
						TextNode("italic", TextType.ITALIC),
						TextNode(" word and a ", TextType.NORMAL),
						TextNode("code block", TextType.CODE),
						TextNode(" and an ", TextType.NORMAL),
						TextNode("obi wan image", TextType.IMAGES, "https://i.imgur.com/fJRm4Vk.jpeg"),
						TextNode(" and a ", TextType.NORMAL),
						TextNode("link", TextType.LINKS, "https://boot.dev"),
						], new_nodes)


if __name__ == "__main__":
    unittest.main()