from directory_functions import copydir_to_targetdir, generate_page

def main():
    copydir_to_targetdir("static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")

main()