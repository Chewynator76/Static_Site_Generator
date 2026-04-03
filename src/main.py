import sys
from directory_functions import copydir_to_targetdir, generate_page, generate_pages_recursive

def main():
    try:
        basepath = sys.argv[1]
    except:
        basepath = "/"
    copydir_to_targetdir("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)

main()