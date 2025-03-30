import os

def setup_project_structure(base_folder="CodeBot", modules_folder="modules", target_folder="../adn_trash_code"):
    """
    Automatically creates the required folders and placeholder module files.
    """
    os.makedirs(base_folder, exist_ok=True)
    modules_path = os.path.join(base_folder, modules_folder)
    os.makedirs(modules_path, exist_ok=True)
    target_path = os.path.join(os.path.dirname(base_folder), "adn_trash_code")
    os.makedirs(target_path, exist_ok=True)
    print(f"Created folders: {modules_path}, {target_path}")
    
    # Create placeholder files for modules
    initial_files = [
        "functions.py", 
        "summarization.py", 
        "compression.py", 
        "resources.py", 
        "file_manager.py"
    ]
    for file in initial_files:
        file_path = os.path.join(modules_path, file)
        if not os.path.exists(file_path):
            with open(file_path, "w") as f:
                f.write(f"# Placeholder for {file}\n")
            print(f"Created file: {file_path}")
    
    print("Project structure setup complete!")


def scan_test_folder(folder_path):
    """
    Scans the specified test folder for available tools and returns a list of files.

    Args:
        folder_path (str): The path to the folder to scan.

    Returns:
        list: A list of file names in the folder.
    """
    try:
        return [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    except FileNotFoundError:
        print(f"Error: The folder '{folder_path}' does not exist.")
        return []


def inject_text(file_path, text, position="append", target_line=None):
    """
    Injects text into a file. Supports append, overwrite, or insertion at specific lines.

    Args:
        file_path (str): Path to the file where text should be injected.
        text (str): The text to inject into the file.
        position (str): Injection mode - "append", "overwrite", or "insert".
        target_line (int): Line number for "insert" mode. Ignored otherwise.

    Returns:
        str: A message indicating the result of the operation.
    """
    try:
        if position == "append":
            with open(file_path, "a", encoding="utf-8") as f:
                f.write(text + "\n")
        elif position == "overwrite":
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(text + "\n")
        elif position == "insert" and target_line is not None:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            if target_line < 1 or target_line > len(lines) + 1:
                raise ValueError("Invalid target line number.")

            lines.insert(target_line - 1, text + "\n")
            with open(file_path, "w", encoding="utf-8") as f:
                f.writelines(lines)
        else:
            raise ValueError("Invalid injection position or missing target line.")

        return f"Text successfully injected into {file_path} at {position} position."
    except FileNotFoundError:
        return f"Error: File '{file_path}' not found."
    except Exception as e:
        return f"Error during injection: {e}"


def list_files_and_metadata(start_path):
    """
    Recursively lists all files and directories starting from the specified path.
    Extracts metadata from Python files (functions, classes, and imports).

    Args:
        start_path (str): The root directory to scan.

    Returns:
        dict: A dictionary containing the structure and metadata of the files.
    """
    structure = {}

    for root, dirs, files in os.walk(start_path):
        dir_name = os.path.basename(root)
        structure[dir_name] = {"files": {}, "subdirectories": dirs}

        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                structure[dir_name]["files"][file] = extract_metadata(file_path)

    return structure


def extract_metadata(file_path):
    """
    Extracts metadata from a Python file: functions, classes, and imports.

    Args:
        file_path (str): The path to the Python file.

    Returns:
        dict: A dictionary containing lists of functions, classes, and imports.
    """
    import ast

    metadata = {"functions": [], "classes": [], "imports": []}

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read(), filename=file_path)
            for node in ast.iter_child_nodes(tree):
                if isinstance(node, ast.FunctionDef):
                    metadata["functions"].append(node.name)
                elif isinstance(node, ast.ClassDef):
                    metadata["classes"].append(node.name)
                elif isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
                    for alias in node.names:
                        metadata["imports"].append(alias.name)
    except Exception as e:
        metadata["error"] = str(e)

    return metadata


# CodeBot_Tracking