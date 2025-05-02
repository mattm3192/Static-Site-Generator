from textnode import *
from htmlnode import *

def split_nodes_delimiter(old_nodes, delimiter, text_type):
	# old nodes are lists, delimiters are single character strings, 
	# text type is the text type enum
	# ** for bold, _ for italics, `for code,
	new_list = []
	for old_node in old_nodes:
		if old_node.text_type != TextType.NORMAL:
			new_list.append(old_node)
		else:
			pass
	pass