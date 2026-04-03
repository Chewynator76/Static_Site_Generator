from directory_functions import copydir_to_targetdir, generate_page, generate_pages_recursive

def main():
    copydir_to_targetdir("static", "public")
    generate_pages_recursive("content", "template.html", "public")

main()