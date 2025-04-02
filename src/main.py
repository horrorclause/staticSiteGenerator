from textnode import *

def main():
    print("Hello World")
    

    # Create a TextNode with dummy values
    node = TextNode("This is some anchor text", TextType.LINK, "https://boot.dev")

    # Print out the created node
    print(node)


if __name__ == '__main__':
    main()
    