#src/main.py
import os
import shutil
import sys
from copystatic import copy_files_recursive
from markdown_blocks import markdown_to_html_node
from extract_title import extract_title

def generate_page(from_path, template_path, dest_path, base_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    # Read markdown content
    with open(from_path, 'r') as f:
        markdown_content = f.read()
    
    # Read template
    with open(template_path, 'r') as f:
        template = f.read()
    
    # Convert markdown to HTML
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()
    
    # Extract title
    title = extract_title(markdown_content)
    
    # Replace placeholders
    full_html = template.replace("{{ Title }}", title).replace("{{ Content }}", html_content)
    
    # Replace paths
    full_html = full_html.replace('href="/', f'href="{base_path}')
    full_html = full_html.replace('src="/', f'src="{base_path}')
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    
    # Write output file
    with open(dest_path, 'w') as f:
        f.write(full_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, base_path):
    for dirpath, dirnames, filenames in os.walk(dir_path_content):
        for filename in filenames:
            if not filename.endswith('.md'):
                continue
                
            # Get the relative path from content directory
            rel_path = os.path.relpath(dirpath, dir_path_content)
            
            # Construct source and destination paths
            if filename == "index.md":
                # For index.md files, keep the directory structure
                dest_filename = "index.html"
            else:
                # For other .md files, replace extension with .html
                dest_filename = filename[:-3] + ".html"
            
            from_path = os.path.join(dirpath, filename)
            if rel_path == '.':
                dest_path = os.path.join(dest_dir_path, dest_filename)
            else:
                dest_path = os.path.join(dest_dir_path, rel_path, dest_filename)
            
            # Generate the page
            generate_page(from_path, template_path, dest_path, base_path)

def main():
    # Get base path from command line argument or default to "/"
    base_path = sys.argv[1] if len(sys.argv) > 1 else "/"
    
    # Use docs directory instead of public
    docs_dir = "docs"
    
    # Delete docs directory if it exists
    if os.path.exists(docs_dir):
        print("Deleting docs directory...")
        shutil.rmtree(docs_dir)
    
    # Copy static files
    print("Copying static files to docs directory...")
    copy_files_recursive("static", docs_dir)
    
    # Generate all pages
    print("Generating pages...")
    generate_pages_recursive("content", "template.html", docs_dir, base_path)

if __name__ == "__main__":
    main()
