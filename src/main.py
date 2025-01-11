from markdown_to_html import markdown_to_html_node
import os, shutil, re


def delete_everything_in_path(directory):
    for path in os.listdir(directory):
        file_path = os.path.join(directory, path)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as err:
            print(f"Failed to delete specified path\nPossbile Reason: {err}")


def copy_recursively(src, dst):
    for path in os.listdir(src):
        curr_path = os.path.join(src, path)
        if os.path.isdir(curr_path):
            print("Is Dir")
            os.makedirs(
                os.path.join(dst, f"{curr_path.replace('static/', '')}"), exist_ok=True
            )
            print(f"Copied directory {curr_path}")
            copy_recursively(curr_path, dst)
        elif os.path.isfile(curr_path):
            print("Is file")
            shutil.copy(
                curr_path, os.path.join(dst, f"{curr_path.replace('static/', '')}")
            )
            print(f"Copied file {curr_path}")
    return "Recursively copied all files and dirs from source to destination"


def extract_title(markdown):
    h1_regex = r"^# .+"
    h1_exists = re.findall(h1_regex, markdown)
    if h1_exists:
        return h1_exists[0].replace("#", "").strip()
    raise Exception("h1 not found in Markdown")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page... from {from_path} to {dest_path} using {template_path}")
    markdown = open(from_path, "r")
    md = markdown.read()
    template = open(template_path, "r")
    tpl = template.read()
    extracted_title = extract_title(md)
    converted_md = markdown_to_html_node(md).to_html()
    html_template = tpl.replace(r"{{ Title }}", extracted_title).replace(
        "{{ Content }}", converted_md
    )
    public_index = open(f"{dest_path}/index.html", "w")
    public_index.write(html_template)
    markdown.close()
    template.close()
    public_index.close()


def generate_pages(from_path, template_path, dest_path):
    for path in os.listdir(from_path):
        curr_path = os.path.join(from_path, path)
        if os.path.isdir(curr_path):
            print("Is Dir")
            os.makedirs(
                os.path.join(dest_path, f"{curr_path.replace('content/', '')}"),
                exist_ok=True,
            )
            print(f"Copied directory {curr_path} to {dest_path}")
            generate_pages(curr_path, template_path, dest_path)
        elif os.path.isfile(curr_path):
            sanitize_dest_path = re.sub(
                r"\w+.md", "", curr_path.replace("content/", "public/")
            )
            print("Is file")
            generate_page(curr_path, template_path, sanitize_dest_path)
            print(f"Copied file {curr_path} to {sanitize_dest_path}")
    return "Recursively copied all files and dirs from source to destination"


def main():
    delete_everything_in_path("public")
    copy_recursively("static", "public")
    generate_pages("content", "template.html", "public")


if __name__ == "__main__":
    main()
