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

def split_nodes_image(old_nodes):
	new_nodes = []
	for old_node in old_nodes:
		text = old_node.text
		extracted_images = extract_markdown_images(text)

		if not text:
			continue
		
		if old_node.text_type != TextType.NORMAL or not extracted_images:
			new_nodes.append(old_node)
			continue

		current_index = 0

		for image in extracted_images:
			image_syntax = f"![{image[0]}]({image[1]})"
			img_start_index = text.find(image_syntax, current_index)
			if img_start_index > current_index:
				new_nodes.append(TextNode(text[current_index:img_start_index], TextType.NORMAL))
			new_nodes.append(TextNode(image[0], TextType.IMAGES, image[1]))
			current_index = img_start_index + len(image_syntax)
		
		if len(text[current_index:]) > 0:
			new_nodes.append(TextNode(text[current_index:], TextType.NORMAL))
	
	return new_nodes


def split_nodes_links(old_nodes):
	new_nodes = []
	for old_node in old_nodes:
		text = old_node.text
		extracted_links = extract_markdown_links(text)

		if not text:
			continue
		
		if old_node.text_type != TextType.NORMAL or not extracted_links:
			new_nodes.append(old_node)
			continue

		current_index = 0

		for link in extracted_links:
			link_syntax = f"[{link[0]}]({link[1]})"
			link_start_index = text.find(link_syntax, current_index)
			if link_start_index > current_index:
				new_nodes.append(TextNode(text[current_index:link_start_index], TextType.NORMAL))
			new_nodes.append(TextNode(link[0], TextType.LINKS, link[1]))
			current_index = link_start_index + len(link_syntax)
		
		if len(text[current_index:]) > 0:
			new_nodes.append(TextNode(text[current_index:], TextType.NORMAL))
	
	return new_nodes

def extract_markdown_images(text):
	return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
	return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)