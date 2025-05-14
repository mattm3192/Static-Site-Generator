#from textnode import *
#from htmlnode import *
#from markdowntotext import *
#from markdownblocks import *
import os, shutil

def main():
	source = "static"
	target = "public"
	copy_static(source, target)

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

main()