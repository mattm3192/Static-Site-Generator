
def markdown_to_blocks(markdown):
	string_blocks = markdown.split("\n\n")
	clean_blocks = []
	for string in string_blocks:
		stripped_string = string.strip()
		if not stripped_string:
			continue
		clean_blocks.append(stripped_string)
	return clean_blocks

	
