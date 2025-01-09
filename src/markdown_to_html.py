from markdown_blocks import markdown_to_blocks, block_to_block_type
from htmlnode import HTMLNode, ParentNode, LeafNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node
import re


def markdown_to_html_node(markdown):
    result = []
    splitted_md = markdown_to_blocks(markdown)
    for e in splitted_md:
        block_type_tuple = block_to_block_type(
            e
        )  # e.g., ("heading", "h1") or ("unordered_list", "ul")

        if (
            "ordered_list" in block_type_tuple[0]
            or "unordered_list" in block_type_tuple[0]
        ):
            # Handle lists
            list_items = []
            sanitized_list = e.split("\n")
            for element in sanitized_list:
                if element.strip():  # Skip empty lines
                    sanitized_element = re.sub(r"^\- |^\d+\. ", "", element)
                    text_nodes = text_to_textnodes(sanitized_element)
                    html_nodes = [text_node_to_html_node(node) for node in text_nodes]
                    list_items.append(ParentNode("li", html_nodes))
            # Add the list as a single node to the result
            result.append(ParentNode(block_type_tuple[1], list_items))

        elif block_type_tuple[0] == "heading":
            # Handle headings
            e = re.sub(r"^#+\s*", "", e)  # Remove Markdown heading markers
            text_nodes = text_to_textnodes(e)
            leafs = [text_node_to_html_node(node) for node in text_nodes]
            result.append(ParentNode(block_type_tuple[1], leafs))

        elif block_type_tuple[0] == "quote":
            e = re.sub(r" > |> | >", "", e)  # Remove quotes heading markers
            text_nodes = text_to_textnodes(e)
            leafs = [text_node_to_html_node(node) for node in text_nodes]
            result.append(ParentNode(block_type_tuple[1], leafs))
        else:
            # Non-list, non-heading handling
            text_nodes = text_to_textnodes(e)
            leafs = [text_node_to_html_node(node) for node in text_nodes]
            result.append(ParentNode(block_type_tuple[1], leafs))

    return ParentNode("div", result)
