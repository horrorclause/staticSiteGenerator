from textnode import TextNode,TextType
from htmlnode import HTMLNode

def main():

    # Create a TextNode with dummy values
    node = TextNode("This is some anchor text", TextType.LINK, "https://boot.dev")

    # Print out the created node
    print(node)

    html_node = HTMLNode("p","this is a text line",None, {"href": "https://www.google.com"})
    print(html_node)

    # Create and print an HTMLNode with nothing
    html_nothing = HTMLNode()
    print("HTMLNode with nothing: ", html_nothing)

    # Create and print an HTMLNode with props
    html_with_props = HTMLNode("p", "This is a text line", None, {"href": "https://www.google.com"})
    print("HTMLNode with props:", html_with_props)

    # Create and print an HTMLNode without props
    html_no_props = HTMLNode("p", "Another text line")
    print("HTMLNode without props:", html_no_props)

    # Create and print an HTMLNode with children
    child1 = HTMLNode("span", "I'm a child span")
    child2 = HTMLNode("b", "I'm a bold child")

if __name__ == '__main__':
    main()
    