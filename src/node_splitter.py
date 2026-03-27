from textnode import TextNode, TextType
from images_extract import extract_markdown_images, extract_markdown_links

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
