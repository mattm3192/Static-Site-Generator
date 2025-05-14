from textnode import *
from htmlnode import *
from markdowntotext import *
from markdownblocks import *

def main():
	md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
	node = markdown_to_html_node(md)
	html = node.to_html()
	i = 7

main()