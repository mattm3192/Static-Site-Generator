import unittest

from markdownblocks import *

class Marldowntoblocks(unittest.TestCase):
	def test_markdown_to_blocks(self):
		md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
		blocks = markdown_to_blocks(md)
		self.assertEqual(["This is **bolded** paragraph",
							"This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
							"- This is a list\n- with items"
							], blocks)
		
	def test_md_to_blocks_excesive_newlines(self):
		md = """

Some text here   






Some more text here,
with a second line following it



"""
		blocks = markdown_to_blocks(md)
		self.assertEqual(["Some text here", 
					"Some more text here,\nwith a second line following it",
					], blocks)

	def test_md_to_blocks_excesive_whitespace(self):
		md = """


     
  
The first block of text

   
   
   
     
	 
The second block of text

  

   
   
   
"""
		blocks = markdown_to_blocks(md)
		self.assertEqual(["The first block of text",
					"The second block of text",
					], blocks)

class Blocktoblocktype(unittest.TestCase):
	def test_blocktype_heading(self):
		block = "# Type 1 heading"
		block_type = block_to_block_type(block)
		self.assertEqual(BlockType.HEADING, block_type)

		block = "## Type 2 heading"
		block_type = block_to_block_type(block)
		self.assertEqual(BlockType.HEADING, block_type)

		block = "### Type 3 heading"
		block_type = block_to_block_type(block)
		self.assertEqual(BlockType.HEADING, block_type)

		block = "#### Type 4 heading"
		block_type = block_to_block_type(block)
		self.assertEqual(BlockType.HEADING, block_type)

		block = "##### Type 5 heading"
		block_type = block_to_block_type(block)
		self.assertEqual(BlockType.HEADING, block_type)

		block = "###### Type 6 heading"
		block_type = block_to_block_type(block)
		self.assertEqual(BlockType.HEADING, block_type)

		block = "####### Headings stop at six #'s"
		block_type = block_to_block_type(block)
		self.assertEqual(BlockType.PARAGRAPH, block_type)

		block = "# Type 1 heading\n## Type 2 heading"
		block_type = block_to_block_type(block)
		self.assertEqual(BlockType.PARAGRAPH, block_type)
	
	def test_blocktype_code(self):
		block = "```This is a single line block of code```"
		block_type = block_to_block_type(block)
		self.assertEqual(BlockType.CODE, block_type)

		block = "```This is a multi\nline block of code```"
		block_type = block_to_block_type(block)
		self.assertEqual(BlockType.CODE, block_type)

		block = "```- This is a multi\n> line block of code\n1. with other types```"
		block_type = block_to_block_type(block)
		self.assertEqual(BlockType.CODE, block_type)

		block = "```This is not a block of code``"
		block_type = block_to_block_type(block)
		self.assertEqual(BlockType.PARAGRAPH, block_type)

	def test_blocktype_quote(self):
		block = "> This is a single line qoute"
		block_type = block_to_block_type(block)
		self.assertEqual(BlockType.QUOTE, block_type)

		block = "> This is a multi line qoute\n> The second line\n> The third line"
		block_type = block_to_block_type(block)
		self.assertEqual(BlockType.QUOTE, block_type)

		block = "> This is a multi line qoute\nThat breaks on the second line\n> but then is good again"
		block_type = block_to_block_type(block)
		self.assertEqual(BlockType.PARAGRAPH, block_type)

	def test_blocktype_unordered_list(self):
		block = "- This is a single line unordered list"
		block_type = block_to_block_type(block)
		self.assertEqual(BlockType.UNORDERED_LIST, block_type)

		block = "- This is a multi line unordered list\n- the next item\n- and the next"
		block_type = block_to_block_type(block)
		self.assertEqual(BlockType.UNORDERED_LIST, block_type)

		block = "- This is a multi line unordered list\nthat breaks on line 2\n- but becomes a list again"
		block_type = block_to_block_type(block)
		self.assertEqual(BlockType.PARAGRAPH, block_type)

	def test_blocktype_ordered_list(self):
		block = "1. This is a single line ordered list"
		block_type = block_to_block_type(block)
		self.assertEqual(BlockType.ORDERED_LIST, block_type)

		block = "1. This is a multi line ordered list\n2. The second item\n3. and the third"
		block_type = block_to_block_type(block)
		self.assertEqual(BlockType.ORDERED_LIST, block_type)

		block = "1. This is a multi line ordered list\nThat breaks in on the 2nd item\n3. and tries to repair itself"
		block_type = block_to_block_type(block)
		self.assertEqual(BlockType.PARAGRAPH, block_type)

	def test_blocktype_paragraph(self):
		block = "This shouldn't catch\n> any particular type\n- becuase the types\n1. start in the wrong\n#place\n```and have not real structure```"
		block_type = block_to_block_type(block)
		self.assertEqual(BlockType.PARAGRAPH, block_type)

	def test_markdown_to_html_paragraphs(self):
		md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
		node = markdown_to_html_node(md)
		html = node.to_html()
		self.assertEqual(html, "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>")

	def test_markdown_to_html_codeblock(self):
		md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
		node = markdown_to_html_node(md)
		html = node.to_html()
		self.assertEqual(html, "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>")

	def test_markdown_to_html_headers(self):
		md = """
# Header 1

## Header 2

### Header **number** 3

#### Header _number_ 4

##### Header `number` 5

###### Header 6

####### Header 7 which is actually a paragraph
"""

		node = markdown_to_html_node(md)
		html = node.to_html()
		self.assertEqual(html, "<div><h1>Header 1</h1><h2>Header 2</h2><h3>Header <b>number</b> 3</h3><h4>Header <i>number</i> 4</h4><h5>Header <code>number</code> 5</h5><h6>Header 6</h6><p>####### Header 7 which is actually a paragraph</p></div>")

	def test_markdown_to_html_unordered_lists(self):
		md = """
- Item 1
- Item 2
- Item 3

- item 1 list 2
- item 2 list 2

- item
-items
- item
"""
		node = markdown_to_html_node(md)
		html = node.to_html()
		self.assertEqual(html, "<div><ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul><ul><li>item 1 list 2</li><li>item 2 list 2</li></ul><p>- item -items - item</p></div>")

	def test_markdown_to_html_ordered_lists(self):
		md = """
1. first
2. second
3. third
4. forth
5. fifth
6. sixth
7. seventh
8. eighth
9. nineth
10. tenth

1. first
2. 2nd
3. 3rd

1. one
2 two
3. three
"""
		node = markdown_to_html_node(md)
		html = node.to_html()
		self.assertEqual(html, "<div><ol><li>first</li><li>second</li><li>third</li><li>forth</li><li>fifth</li><li>sixth</li><li>seventh</li><li>eighth</li><li>nineth</li><li>tenth</li></ol><ol><li>first</li><li>2nd</li><li>3rd</li></ol><p>1. one 2 two 3. three</p></div>")

	def test_markdown_to_html_quotes(self):
		md = """
> This is my first **quote**
> This is the _next_ line of that first quote

> This is a second `quote`
> with just a regular second line
"""

		node = markdown_to_html_node(md)
		html = node.to_html()
		self.assertEqual(html, "<div><blockquote>This is my first <b>quote</b>\nThis is the <i>next</i> line of that first quote</blockquote><blockquote>This is a second <code>quote</code>\nwith just a regular second line</blockquote></div>")

	def test_markdown_to_html_paragraph_with_link_and_image(self):
		md = """
This is a [link](https://example.com) and an ![image](img.png)

"""
		node = markdown_to_html_node(md)
		html = node.to_html()
		self.assertEqual(html, '<div><p>This is a <a href="https://example.com">link</a> and an <img src="img.png" alt="image"/></p></div>')

	def test_markdown_to_html_headers_with_link_and_image(self):
		md = """
# Header 1 [link](https://example.com)

## Header 2 ![image](img.png)
"""

		node = markdown_to_html_node(md)
		html = node.to_html()
		self.assertEqual(html, '<div><h1>Header 1 <a href="https://example.com">link</a></h1><h2>Header 2 <img src="img.png" alt="image"/></h2></div>')

	def test_markdwon_extract_title(self):
		md = """
#   Tolkien Fan Club  

![JRR Tolkien sitting](/images/tolkien.png)

Here's the deal, **I like Tolkien**.
"""

		title = extract_title(md)
		self.assertEqual(title, "Tolkien Fan Club")

		md2 = """
## No h1 header here Gandalf

![JRR Tolkien sitting](/images/tolkien.png)

Here's the deal, **I like Tolkien**.
"""

		with self.assertRaises(ValueError) as context:
			extract_title(md2)
		self.assertIn("There was no h1 header", str(context.exception))


if __name__ == "__main__":
    unittest.main()