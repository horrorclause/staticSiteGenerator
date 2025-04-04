
from textnode import *

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
