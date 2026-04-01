from textnode import TextNode, TextType
from images_extract import extract_markdown_images, extract_markdown_links
from blocktype import BlockType, block_to_block_type
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode_to_htmlnode import text_node_to_html_node

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_list.append(node)
            continue
        split_nodes = []
        sections = node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_list.extend(split_nodes)
    
    return new_list

def split_nodes_image(old_nodes):
    new_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_list.append(node)
            continue
        split_nodes = []
        images = extract_markdown_images(node.text)

        if images == []:
            new_list.append(node)
            continue
        text = node.text
        
        for i in range(len(images)):
            delimiter = f"![{images[i][0]}]({images[i][1]})"
            sections = text.split(delimiter, 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            text = sections[1]

            if sections[0] != "":
                split_nodes.append(TextNode(sections[0], TextType.TEXT))
            split_nodes.append(TextNode(images[i][0], TextType.IMAGE, images[i][1]))
            
        if text != "":
            split_nodes.append(TextNode(text, TextType.TEXT))

        new_list.extend(split_nodes)
    
    return new_list


def split_nodes_link(old_nodes):
    new_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_list.append(node)
            continue
        split_nodes = []
        links = extract_markdown_links(node.text)

        if links == []:
            new_list.append(node)
            continue
        text = node.text

        for i in range(len(links)):
            delimiter = f"[{links[i][0]}]({links[i][1]})"
            sections = text.split(delimiter, 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            text = sections[1]

            if sections[0] != "":
                split_nodes.append(TextNode(sections[0], TextType.TEXT))
            split_nodes.append(TextNode(links[i][0], TextType.LINK, links[i][1]))

        if text != "":
            split_nodes.append(TextNode(text, TextType.TEXT))

        new_list.extend(split_nodes)
    
    return new_list

def text_to_textnodes(text):
    original_text = [TextNode(text, TextType.TEXT)]
    original_text = split_nodes_delimiter(original_text, "**", TextType.BOLD)
    original_text = split_nodes_delimiter(original_text, "_", TextType.ITALIC)
    original_text = split_nodes_delimiter(original_text, "`", TextType.CODE)
    original_text = split_nodes_image(original_text)
    original_text = split_nodes_link(original_text)
    return original_text

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.OLIST:
        return olist_to_html_node(block)
    if block_type == BlockType.ULIST:
        return ulist_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    raise ValueError("invalid block type")
        

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)

def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])

def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        parts = item.split(". ", 1)
        text = parts[1]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)

def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)

def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)