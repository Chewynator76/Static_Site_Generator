from textnode import TextNode
from textnode import TextType

def main():
    text_type_text = TextType.LINK
    test = TextNode("This is some anchor text", text_type_text, "https://www.boot.dev")
    print(test)

main()