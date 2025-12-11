from htmlnode import HTMLNode
from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType
from block_markdown import markdown_to_blocks, block_to_block_type, BlockType

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return HTMLNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return HTMLNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return HTMLNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        return HTMLNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        return HTMLNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return HTMLNode("img", "", {"src": text_node.url, "alt": text_node.text})
    raise ValueError(f"Invalid text node type: {text_node.text_type}")

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(text_node) for text_node in text_nodes]

def paragraph_to_html_node(block):
    return HTMLNode("p", None, text_to_children(block))

def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level == 0:
        raise ValueError("Invalid heading block")
    text = block[level:].strip()
    return HTMLNode(f"h{level}", None, text_to_children(text))

def code_to_html_node(block):
    lines = block.split("\n")
    if len(lines) < 2:
        raise ValueError("Invalid code block")
    
    # Remove first and last lines (```)
    text = "\n".join(lines[1:-1])
    
    code_node = HTMLNode("code", text)
    pre_node = HTMLNode("pre", None, [code_node])
    return pre_node

def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = [line[2:].strip() if line.startswith("> ") else line.strip() for line in lines]
    text = "\n".join(new_lines)
    return HTMLNode("blockquote", None, text_to_children(text))

def unordered_list_to_html_node(block):
    items = block.split("\n")
    item_nodes = []
    for item in items:
        if not item.startswith("- "):
            continue
        text = item[2:].strip()
        item_nodes.append(HTMLNode("li", None, text_to_children(text)))
    return HTMLNode("ul", None, item_nodes)

def ordered_list_to_html_node(block):
    items = block.split("\n")
    item_nodes = []
    for item in items:
        if not any(item.startswith(f"{i}. ") for i in range(1, 10)):
            continue
        text = item[item.find(" ")+1:].strip()
        item_nodes.append(HTMLNode("li", None, text_to_children(text)))
    return HTMLNode("ol", None, item_nodes)

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    if not blocks:
        return HTMLNode("div")
    
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            children.append(paragraph_to_html_node(block))
        elif block_type == BlockType.HEADING:
            children.append(heading_to_html_node(block))
        elif block_type == BlockType.CODE:
            children.append(code_to_html_node(block))
        elif block_type == BlockType.QUOTE:
            children.append(quote_to_html_node(block))
        elif block_type == BlockType.UNORDERED_LIST:
            children.append(unordered_list_to_html_node(block))
        elif block_type == BlockType.ORDERED_LIST:
            children.append(ordered_list_to_html_node(block))
        else:
            raise ValueError(f"Invalid block type: {block_type}")
    
    return HTMLNode("div", None, children)
