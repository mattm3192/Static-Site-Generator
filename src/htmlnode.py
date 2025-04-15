class HTMLNode:
	def __init__(self, tag=None, value=None, children=None, props=None):
		self.tag = tag
		self.value = value
		self.children = children
		self.props = props

	def to_html(self):
		raise NotImplementedError
	
	def props_to_html(self):
		if self.props is None or len(self.props) == 0:
			return ""
		string = ""
		for key, value in self.props.items():
			string += f' {key}="{value}"'
		return string
	
	def __repr__(self):
		return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
	
class LeafNode(HTMLNode):
	def __init__(self, tag=None, value=None, props=None):
		super().__init__(tag, value, None, props)
	
	def to_html(self):
		if self.value is None:
			raise ValueError
		if self.tag is None or self.tag == "":
			return f"{self.value}"
		if self.tag == "a":
			props_html = super().props_to_html()
			return f"<a{props_html}>{self.value}</a>"
		return f"<{self.tag}>{self.value}</{self.tag}>"
	
class ParentNode(HTMLNode):
	def __init__(self, tag, children, props=None):
		super().__init__(tag, None, children, props)

	def to_html(self):
		if self.tag is None:
			raise ValueError("Object must have a tag.")
		if self.children is None:
			raise ValueError("A parent node must have children.")
		