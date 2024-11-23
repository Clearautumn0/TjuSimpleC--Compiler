import os

def display_tree(dir_path, indent="", exclude_dirs=["__pycache__"], exclude_hidden=True):
    for item in os.listdir(dir_path):
        # Skip hidden files/directories if exclude_hidden is True
        if exclude_hidden and item.startswith("."):
            continue
        item_path = os.path.join(dir_path, item)
        # Skip excluded directories
        if os.path.isdir(item_path) and item in exclude_dirs:
            continue
        # Print the directory or file name
        print(f"{indent}├── {item}")
        # Recursively display subdirectories
        if os.path.isdir(item_path):
            display_tree(item_path, indent + "│   ", exclude_dirs, exclude_hidden)

if __name__ == "__main__":
    # Specify the root directory (current directory)
    root_dir = os.getcwd()
    print(f"Directory tree for: {root_dir}")
    display_tree(root_dir)
