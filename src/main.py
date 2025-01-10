from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode
import os, shutil


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


def main():
    delete_everything_in_path("public")
    copy_recursively("static", "public")


if __name__ == "__main__":
    main()
