from textnode import *
def main():
	string = "This is a text node"
	string_type = TextType.BOLD
	url = "https:www.boot.dev"
	node = TextNode(string, string_type, url)
	print(node)

main()