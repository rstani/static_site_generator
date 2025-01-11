from textnode import TextNode, TextType
import re


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


def extract_markdown_images(text):
    images_regex = r"\!\[(.*?)\]\((\S*)\)"
    matches = re.findall(images_regex, text)
    return matches


def extract_markdown_links(text):
    links_regex = r"\[(.*?)\]\((\S*)\)"
    matches = re.findall(links_regex, text)
    return matches


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if not extract_markdown_images(node.text):
            new_nodes.append(node)
            continue
        splitted_images = re.split(r"(\!\[.*?\]\(\S*\))", node.text)
        for e in splitted_images:
            if e == "":
                continue
            if "!" in e:
                extracted_image = extract_markdown_images(e)
                new_nodes.append(
                    TextNode(
                        extracted_image[0][0], TextType.IMAGE, extracted_image[0][1]
                    )
                )
            else:
                new_nodes.append(TextNode(e, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if not extract_markdown_links(node.text):
            new_nodes.append(node)
            continue
        splitted_images = re.split(r"(\[.*?\]\(\S*\))", node.text)
        for e in splitted_images:
            if e == "":
                continue
            if "[" in e:
                extracted_image = extract_markdown_links(e)
                new_nodes.append(
                    TextNode(
                        extracted_image[0][0], TextType.LINK, extracted_image[0][1]
                    )
                )
            else:
                new_nodes.append(TextNode(e, TextType.TEXT))
    return new_nodes


def text_to_textnodes(text):
    result = TextNode(text, TextType.TEXT)
    result = split_nodes_image([result])
    result = split_nodes_link(result)
    result = split_nodes_delimiter(result, "**", TextType.BOLD)
    result = split_nodes_delimiter(result, "*", TextType.ITALIC)
    result = split_nodes_delimiter(result, "`", TextType.CODE)
    return result
