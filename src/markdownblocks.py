from enum import Enum
from htmlnode import *
from textnode import *
from markdowntotext import *

class BlockType(Enum):
	PARAGRAPH = "paragraph"
	HEADING = "heading"
	CODE = "code"
	QUOTE = "quote"
	UNORDERED_LIST = "unordered_list"
	ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
	lines = block.split("\n")
	if len(lines) < 2:
		string = lines[0]
		if (string.startswith("# ") or string.startswith("## ") or 
		string.startswith("### ") or string.startswith("#### ") or
		string.startswith("##### ") or string.startswith("###### ")):
			return BlockType.HEADING
	
	if (block.startswith("```") and block.endswith("```")):
		return BlockType.CODE
	
	for line in lines:
		if not line.startswith("> "):
			break
	else:
		return BlockType.QUOTE
	
	for line in lines:
		if not line.startswith("- "):
			break
	else:
		return BlockType.UNORDERED_LIST
	
	for i in range(1, len(lines)+1):
		if not lines[i-1].startswith(f"{i}. "):
			break
	else:
		return BlockType.ORDERED_LIST

	return BlockType.PARAGRAPH

def markdown_to_blocks(markdown):
	string_blocks = markdown.split("\n\n")
	clean_blocks = []
	for string in string_blocks:
		stripped_string = string.strip()
		if not stripped_string:
			continue
		clean_blocks.append(stripped_string)
	return clean_blocks

def markdown_to_html_node(markdown):
	block_nodes = []
	blocks = markdown_to_blocks(markdown)
	
	for block in blocks:
		block_type = block_to_block_type(block)
		match block_type:
			case BlockType.HEADING:
				count = 0
				for char in block:
					if char == "#":
						count += 1
					if count >= 6:
						break
				value = block[count + 1:]
				heading = ParentNode(f"h{count}", text_to_children(value))
				block_nodes.append(heading)

			case BlockType.CODE:
				lines = block.split("\n")

				start_index = 0
				while start_index < len(lines) and not lines[start_index].strip().startswith("```"):
					start_index += 1
				if start_index < len(lines):
					start_index += 1

				end_index = len(lines) - 1
				while end_index >= 0 and not lines[end_index].strip() == "```":
					end_index -= 1

				code_content = "\n".join(lines[start_index: end_index]) + "\n"

				raw_text = TextNode(code_content, TextType.NORMAL)
				code_node = ParentNode("code", [text_node_to_html_node(raw_text)])
				code_block = ParentNode("pre", [code_node])
				block_nodes.append(code_block)

			case BlockType.QUOTE:
				lines = block.split("\n")
				quote_content = []

				for line in lines:
					if line.strip().startswith(">"):
						i = line.find(">") + 1
						while i < len(line) and line[i].isspace():
							i += 1
						quote_content.append(line[i:])
					else:
						quote_content.append(line)
				quote_text = "\n".join(quote_content)
				quote = ParentNode("blockquote", text_to_children(quote_text))
				block_nodes.append(quote)

			case BlockType.UNORDERED_LIST:
				lines = block.split("\n")
				list_items = []
				for line in lines:
					if not line.strip():
						continue

					start = 0
					for i, char in enumerate(line):
						if char in ["-", "*", "+"] and (i == 0 or line[i-1].isspace()):
							start = i + 1
							while start < len(line) and line[start].isspace():
								start += 1
							break
					item_content = line[start:]
					list_items.append(ParentNode("li", text_to_children(item_content)))
				unordered_list = ParentNode("ul", list_items)
				block_nodes.append(unordered_list)

			case BlockType.ORDERED_LIST:
				lines = block.split("\n")
				list_items = []
				for line in lines:
					if not line.strip():
						continue

					start = 0
					in_digit = False
					for i, char in enumerate(line):
						if char.isdigit():
							in_digit = True
						elif char == "." and in_digit:
							start = i + 1
							while start < len(line) and line[start].isspace():
								start += 1
							break
						elif not char.isspace():
							in_digit = False
					item_content = line[start:]
					list_items.append(ParentNode("li", text_to_children(item_content)))
				ordered_list = ParentNode("ol", list_items)
				block_nodes.append(ordered_list)

			case BlockType.PARAGRAPH:
				lines = block.split("\n")
				paragraph_text = " ".join(lines)
				paragraph = ParentNode("p", text_to_children(paragraph_text))
				block_nodes.append(paragraph)

			case _:
				raise Exception("Unable to determine block type from provided markdown blocks.")
	return ParentNode("div", block_nodes)
		
def text_to_children(text):
	HTML_nodes = []
	text_nodes = text_to_textnodes(text)

	for node in text_nodes:
		HTML_nodes.append(text_node_to_html_node(node))

	return HTML_nodes

def extract_title(markdown):
	blocks = markdown_to_blocks(markdown)
	for block in blocks:
		block_type = block_to_block_type(block)
		if block_type == BlockType.HEADING:
			if block.startswith("# "):
				return block[2:].strip()
	raise ValueError("There was no h1 header in the markdown file.")