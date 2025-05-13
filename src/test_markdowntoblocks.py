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

if __name__ == "__main__":
    unittest.main()