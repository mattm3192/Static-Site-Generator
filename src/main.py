#from textnode import *
#from htmlnode import *
#from markdowntotext import *
from markdownblocks import *
import os, shutil, sys

def main():
	basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

	if os.path.exists("docs"):
		shutil.rmtree("docs")
	source = "static"
	target = "docs"
	copy_static(source, target)
	
	from_path = "content"
	template_path = "template.html"
	dest_path = "docs"
	generate_pages_recursive(from_path, template_path, dest_path, basepath)

def copy_static(source_dir, target_dir):
	if os.path.exists(target_dir):
		shutil.rmtree(target_dir)
		print(f"Removed {target_dir} directory and all contents.")

	os.mkdir(target_dir)
	
	if not os.path.exists(source_dir):
		print(f"Error: Source directory '{source_dir}' does not exist!")
		return
	
	contents = os.listdir(source_dir)
	for item in contents:
		src_path = os.path.join(source_dir, item)
		dest_path = os.path.join(target_dir, item)
		if os.path.isfile(src_path):
			shutil.copy(src_path, dest_path)
			print(f"Copied file: {src_path} -> {dest_path}")
		elif os.path.isdir(src_path):
			os.mkdir(dest_path)
			copy_static(src_path, dest_path)

def generate_page(from_path, template_path, dest_path, basepath):
	print(f"Generating page from {from_path} to {dest_path} using {template_path}.\n")
	
	if os.path.exists(from_path):
		if os.path.isfile(from_path) and from_path.endswith(".md"):
			with open(from_path, "r") as f1:
				from_contents_md = f1.read()
		else:
			raise ValueError(f"The file at {from_path} is not a markdown file.\n")
	else:
		raise ValueError(f"{from_path} directory does not exist.\n")
	
	if os.path.exists(template_path):
		if os.path.isfile(template_path) and template_path.endswith(".html"):
			with open(template_path, "r") as f2:
				template_contents_html = f2.read()
		else:
			raise ValueError(f"The file at {template_path} is not a html file.\n")
	else:
		raise ValueError(f"{template_path} directory does not exist.\n")
	
	content_html = markdown_to_html_node(from_contents_md).to_html()
	title = extract_title(from_contents_md)

	template_contents_html = template_contents_html.replace("{{ Title }}", title)
	template_contents_html = template_contents_html.replace("{{ Content }}", content_html)
	

	if ("{{ Title }}" not in template_contents_html and "{{ Content }}" not in template_contents_html) and (title in template_contents_html and content_html in template_contents_html):
		print(f"Title and content tags in {template_path} file were replaced correctly\n")
	else:
		raise Exception("'{{ Title }}' and '{{ Content }}' tags where found in in the html template or the intended replacement strings were not found.\n")
	
	template_contents_html = template_contents_html.replace('href="/', f'href="{basepath}')
	template_contents_html = template_contents_html.replace('src="/', f'src="{basepath}')

	if os.path.dirname(dest_path) != "":
		os.makedirs(os.path.dirname(dest_path), exist_ok=True)

	with open(dest_path, "w") as f_dest:
		f_dest.write(template_contents_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
	local_items = os.listdir(dir_path_content)
	for item in local_items:
		item_full_path = os.path.join(dir_path_content, item)

		if os.path.isfile(item_full_path) and item.endswith(".md"):
			item_html = item.replace(".md", ".html")
			new_dest_dir = os.path.join(dest_dir_path, item_html)

			os.makedirs(os.path.dirname(new_dest_dir), exist_ok=True)

			generate_page(item_full_path, template_path, new_dest_dir, basepath)

		elif os.path.isdir(item_full_path):
			new_dest_dir =os.path.join(dest_dir_path, item)
			generate_pages_recursive(item_full_path, template_path, new_dest_dir, basepath)



main()