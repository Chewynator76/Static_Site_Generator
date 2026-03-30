from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "<p>"
    HEADING = "<h1>"
    CODE = "<c>"
    QUOTE = '<"">'
    ULIST = "[2, 1]"
    OLIST = "[1, 2]"

def block_to_block_type(block):
    lines = block.split("\n")
    
    if block.startswith("#"):
        return BlockType.HEADING
    if block.startswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        return BlockType.QUOTE
    if block.startswith("-"):
        return BlockType.ULIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.OLIST
    return BlockType.PARAGRAPH
