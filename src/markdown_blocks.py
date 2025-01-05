import re

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_olist = "ordered_list"
block_type_ulist = "unordered_list"


def markdown_to_blocks(markdown):
    # Split based on empty lines
    blocks = re.split(r"\n\s*\n", markdown)
    # Strip leading/trailing whitespace and remove empty blocks
    blocks = [block.strip() for block in blocks if block.strip()]
    return blocks


def block_to_block_type(block):
    heading_regex = r"^[#]{1,6}\s\S+"
    unordered_list_regex = r"^*|-\s"
    ordered_list_regex = r"^\d\.\s"
    if re.search(heading_regex, block):
        return block_type_heading
    if block.startswith("```") and block.endswith("```"):
        return block_type_code
    if all(i.startswith(">") for i in block.splitlines()):
        return block_type_quote
    if all(re.search(unordered_list_regex, i) for i in block.splitlines()):
        return block_type_ulist
    if all(re.search(ordered_list_regex, i) for i in block.splitlines()):
        return block_type_olist
    return block_type_paragraph
