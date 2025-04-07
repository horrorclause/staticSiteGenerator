
from textnode import *
from enum import Enum
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
    UNORDERED = "unordered_list"
    ORDERED = "ordered_list"


def block_to_block_type(block):
    
    lines = block.splitlines()

    if lines[0].startswith('```') and lines[-1].startswith('```'):
        return BlockType.CODE

    if lines[0].startswith("#"):
        parts = lines[0].split(" ", 1)
        hash_part = parts[0]
        if 1 <= len(hash_part) <= 6 and len(parts) > 1:
            return BlockType.HEADING
        
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED
    
    ordered = True
    expected_number = 1
    for line in lines:
        if not line.startswith(f"{expected_number}. "):
            ordered = False
            break
        expected_number += 1
    if ordered:
        return BlockType.ORDERED
    
    return BlockType.PARAGRAPH