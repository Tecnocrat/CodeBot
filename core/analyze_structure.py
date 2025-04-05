import os
import json
import re
import ast
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Add the project root to sys.path
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config import KNOWLEDGE_BASE_DIR

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def analyze_folder_structure(base_dir):
    """
    Recursively analyzes the folder structure and generates metadata.
    """
    structure = {}
    for root, dirs, files in os.walk(base_dir):
        structure[root] = {
            "files": files,
            "subfolders": dirs
        }
    return structure

def save_structure_to_json(base_dir, output_dir):
    """
    Saves the folder structure to a JSON file.
    """
    folder_name = os.path.basename(base_dir)
    output_file = os.path.join(output_dir, f"folder_{folder_name}_structure.json")
    structure = analyze_folder_structure(base_dir)
    with open(output_file, "w") as f:
        json.dump(structure, f, indent=4)
    print(f"Folder structure saved to {output_file}")

def extract_imports(file_path):
    """
    Extracts import statements from a Python file.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    imports = re.findall(r"^import (\S+)|^from (\S+) import", content, re.MULTILINE)
    return [imp[0] or imp[1] for imp in imports]

def generate_knowledge_base(base_dir, output_file):
    """
    Generates a JSON file that tracks all Python files and their imports.
    """
    knowledge_base = {}
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                imports = re.findall(r"^import (\S+)|^from (\S+) import", content, re.MULTILINE)
                imports = [imp[0] or imp[1] for imp in imports]
                relative_path = os.path.relpath(file_path, base_dir)
                knowledge_base[relative_path] = {"imports": imports}
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(knowledge_base, f, indent=4)
    print(f"Knowledge base saved to {output_file}")

def update_imports(base_dir, knowledge_base_file):
    """
    Updates imports in all Python files based on the knowledge base.
    """
    with open(knowledge_base_file, "r", encoding="utf-8") as f:
        knowledge_base = json.load(f)

    for relative_path, data in knowledge_base.items():
        file_path = os.path.join(base_dir, relative_path)
        if not os.path.exists(file_path):
            continue
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        for imp in data["imports"]:
            if imp in knowledge_base:
                new_import = os.path.splitext(knowledge_base[imp]["path"])[0].replace(os.sep, ".")
                content = re.sub(rf"(^import {imp}|^from {imp} import)", f"from {new_import} import", content, flags=re.MULTILINE)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
    print("Imports updated successfully.")

def extract_functions_and_classes(file_path):
    """
    Extracts functions and classes from a Python file.

    Args:
        file_path (str): Path to the Python file.

    Returns:
        dict: A dictionary containing functions and classes.
    """
    try:
        with open(file_path, "r") as f:
            tree = ast.parse(f.read())

        functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
        classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]

        return {"functions": functions, "classes": classes}
    except Exception as e:
        logging.error(f"Error parsing {file_path}: {e}")
        return {"functions": [], "classes": []}

def parse_codebase(base_dir, output_file="c:\\dev\\CodeBot\\storage\\codebot_parsed_structure.json"):
    """
    Analyzes the folder structure and parses high-level behaviors of genetic modules.

    Args:
        base_dir (str): Root directory of the CodeBot project.
        output_file (str): Path to save the JSON representation of the parsed structure.

    Returns:
        dict: JSON representation of the parsed codebase structure and behaviors.
    """
    code_structure = {}
    for root, dirs, files in os.walk(base_dir):
        folder = root.replace(base_dir, "").strip(os.sep)
        code_structure[folder] = {
            "files": files,
            "subfolders": dirs,
            "module_details": {}
        }

        # Extract functions and classes for each Python file
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                code_structure[folder]["module_details"][file] = extract_functions_and_classes(file_path)

    # Save the structure to a JSON file
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w") as f:
        json.dump(code_structure, f, indent=4)
    print(f"Codebase structure saved to {output_file}")

    return code_structure

def detect_ai_behaviors(folder, files):
    """
    Identifies AI-related logic or behaviors based on file patterns.

    Args:
        folder (str): The folder being analyzed.
        files (list): List of files in the folder.

    Returns:
        list: High-level behaviors detected in the folder.
    """
    behaviors = []
    patterns = {
        "genetic": "Genetic Algorithm Detected",
        "self_improvement": "Self-Improvement Logic Detected",
        "ai_engine": "AI Engine Logic Detected",
        "logging": "Logging Detected",
    }

    for file in files:
        if file.endswith(".py"):
            file_path = os.path.join(folder, file)
            try:
                with open(file_path, "r") as f:
                    content = f.read()
                    for keyword, behavior in patterns.items():
                        if keyword in content:
                            behaviors.append(behavior)
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
    return behaviors

def generate_metadata(base_dir, output_file):
    """
    Generates JSON metadata about the codebase, including folder structure, imports, and module definitions.

    Args:
        base_dir (str): The root directory of the CodeBot project.
        output_file (str): Path to save the metadata JSON file.
    """
    metadata = {}
    for root, dirs, files in os.walk(base_dir):
        relative_root = os.path.relpath(root, base_dir)
        metadata[relative_root] = {
            "files": [],
            "subfolders": dirs,
            "modules": {}
        }

        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                try:
                    imports = extract_imports(file_path)
                    definitions = extract_functions_and_classes(file_path)
                    metadata[relative_root]["modules"][file] = {
                        "imports": imports,
                        "definitions": definitions
                    }
                except Exception as e:
                    logging.error(f"Error processing file {file_path}: {e}")
            else:
                metadata[relative_root]["files"].append(file)

    # Save the metadata to a JSON file
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=4)
    logging.info(f"Metadata saved to {output_file}")

if __name__ == "__main__":
    base_dir = input("Enter the folder to analyze (e.g., C:\\dev): ").strip()
    if not os.path.isdir(base_dir):
        print(f"Error: '{base_dir}' is not a valid directory.")
        sys.exit(1)
    output_dir = os.path.join("c:\\dev\\CodeBot", "storage")
    os.makedirs(output_dir, exist_ok=True)
    save_structure_to_json(base_dir, output_dir)

    base_dir = "c:\\dev\\CodeBot"
    knowledge_base_file = os.path.join(base_dir, "knowledge_base.json")
    generate_knowledge_base(base_dir, knowledge_base_file)
    update_imports(base_dir, knowledge_base_file)