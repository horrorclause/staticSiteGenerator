
from textnode import *
from enum import Enum
from htmlnode import *
import re

def split_node_delimiter(old_nodes, delimiter, text_type):
        
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        else:
            split_on_delim = node.text.split(delimiter)
            if len(split_on_delim) % 2 == 0:
                raise ValueError("Mismatched delimiter!")
            
            inside_delimiter = False

            for split in split_on_delim:
                if inside_delimiter:
                    # We're inside, use the given `text_type`
                    new_nodes.append(TextNode(split, text_type))
                else:
                    # We're outside, use `TextType.TEXT`
                    new_nodes.append(TextNode(split, TextType.TEXT))
                # Toggle the flag
                inside_delimiter = not inside_delimiter

    return new_nodes


def extract_markdown_images(text):
    

    matches = re.findall(r"!\[([^\]]+)\]\(([^)]+)\)", text)

    return matches


def extract_markdown_links(text):
    matches = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", text)

    return matches


def split_nodes_image(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        matches = extract_markdown_images(old_node.text)
        if not matches:
            new_nodes.append(old_node)
            continue

        # Need to handle splitting text around images
        remaining_text = old_node.text
        
        for alt_text, url in matches:
            # Split on the first occurrence of this image markdown
            image_markdown = f"![{alt_text}]({url})"
            parts = remaining_text.split(image_markdown, 1)
            
            # Add text before the image if not empty
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
                
            # Add the image node
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
            
            # Update remaining text
            remaining_text = parts[1] if len(parts) > 1 else ""
        
        # Add any remaining text after the last image
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        matches = extract_markdown_links(old_node.text)
        if not matches:
            new_nodes.append(old_node)
            continue

        # Need to handle splitting text around links
        remaining_text = old_node.text
        
        for alt_text, url in matches:
            # Split on the first occurrence of this link markdown
            link_markdown = f"[{alt_text}]({url})"
            parts = remaining_text.split(link_markdown, 1)
            
            # Add text before the link if not empty
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
                
            # Add the link node
            new_nodes.append(TextNode(alt_text, TextType.LINK, url))
            
            # Update remaining text
            remaining_text = parts[1] if len(parts) > 1 else ""
        
        # Add any remaining text after the last link
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    
    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    
    # Apply each splitting function in sequence
    # For delimiters like bold, italic, code
    nodes = split_node_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_node_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_node_delimiter(nodes, "`", TextType.CODE)
    
    # For more complex patterns like images and links
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    
    return nodes


def markdown_to_blocks(markdown):
    fixed = [block.strip() for block in markdown.split("\n\n") if block.strip()!= ""]
    return fixed


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    OLIST = "ordered_list"
    ULIST = "unordered_list"


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks


def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.ULIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.OLIST
    return BlockType.PARAGRAPH


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
        html_node = text_node_to_html(text_node)
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
    child = text_node_to_html(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])


def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
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