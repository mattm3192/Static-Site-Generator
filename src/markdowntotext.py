import re

from textnode import *
from htmlnode import *

def split_nodes_delimiter(old_nodes, delimiter, text_type):
	new_nodes = []
	for old_node in old_nodes:
		if old_node.text_type != TextType.NORMAL:
			new_nodes.append(old_node)
			continue
		
		text = old_node.text
		parts = text.split(delimiter)

		if len(parts) == 1:
			new_nodes.append(old_node)
			continue

		if len(parts) < 3 or len(parts) % 2 == 0:
			raise Exception(f"Invalid markdown: unbalanced delimiters '{delimiter}'")
		
		if parts[0]:
			new_nodes.append(TextNode(parts[0], TextType.NORMAL))

		for i in range(1, len(parts), 2):
			new_nodes.append(TextNode(parts[i], text_type))
			
			if i + 1 < len(parts) and parts[i + 1]:
				new_nodes.append(TextNode(parts[i + 1], TextType.NORMAL))				

	return new_nodes

def extract_markdown_images(text):
	return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
	return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)