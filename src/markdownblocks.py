from enum import Enum

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

	
