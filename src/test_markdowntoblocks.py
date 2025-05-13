import unittest

from markdowntoblocks import *

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

if __name__ == "__main__":
    unittest.main()