from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode


def main():
    new_text = TextNode("Random String", TextType.BOLD, "https://google.com")
    node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
    print(node.to_html())
    print(new_text)


if __name__ == "__main__":
    main()
