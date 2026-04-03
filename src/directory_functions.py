import os
import shutil
from node_splitter import markdown_to_html_node, extract_title
from htmlnode import HTMLNode, LeafNode, ParentNode

def copydir_to_targetdir(source, target):
    target_path = os.path.abspath(target)
    source_path = os.path.abspath(source)
    target_contents = os.listdir(target_path)
    source_contents = os.listdir(source_path)

    if os.path.exists(source_path) == False:
        return
    if os.path.exists(target_path) == False:
        os.mkdir(target_path)

    for path in target_contents:
        temp = os.path.join(target_path, path)
        if os.path.isfile(temp):
            os.remove(temp)
        else:
            shutil.rmtree(temp)
    
    for path in source_contents:
        temp = os.path.join(source_path, path)
        if os.path.isfile(temp):
            shutil.copy(temp, target)
            continue
        temp2 = os.path.join(target_path, path)
        os.mkdir(temp2)
        copydir_to_targetdir(temp, temp2)
    
def generate_page(from_path, template_path, dest_path):
    print(f"Generating page {from_path} to {dest_path} using {template_path}...")

    abs_from_path = os.path.abspath(from_path)
    abs_template_path = os.path.abspath(template_path)
    abs_dest_path = os.path.abspath(dest_path)
    dest_dir = os.path.dirname(abs_dest_path)

    if os.path.exists(abs_from_path) == False:
        print(f"Failed to generate page because {from_path} doesn't exist")
        return
    if os.path.exists(abs_template_path) == False:
        print(f"Failed to generate page because {template_path} doesn't exist")
        return
    if dest_dir != "":
        if os.path.exists(dest_dir) == False:
            os.makedirs(dest_dir, exist_ok=True)
    
    markdown_file = open(abs_from_path)
    template_file = open(abs_template_path)
    dest_file = open(abs_dest_path, "w")
    markdown = markdown_file.read()
    template = template_file.read()
    html_str = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    template = template.replace("{{ Title }}", title).replace("{{ Content }}", html_str)

    dest_file.write(template)
    markdown_file.close()
    template_file.close()
    dest_file.close()
    print("Successfully generated page")

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    abs_from_path = os.path.abspath(dir_path_content)
    abs_template_path = os.path.abspath(template_path)
    abs_dest_path = os.path.abspath(dest_dir_path)

    markdown_list = os.listdir(abs_from_path)

    for file in markdown_list:
        file_name, file_extension = os.path.splitext(file)
        file_path = os.path.join(abs_from_path, file)
        if os.path.isdir(file_path):
            joined = os.path.join(dir_path_content, file)
            joined_dest = os.path.join(dest_dir_path, file)
            generate_pages_recursive(joined, template_path, joined_dest)
        elif file_extension == ".md":
            new_file = file_name + ".html"
            new_dest_path = os.path.join(dest_dir_path, new_file)
            generate_page(file_path, template_path, new_dest_path)
            
