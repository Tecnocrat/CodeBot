import os
import json
import re

def analyze_folder_structure(base_dir, max_depth=10, current_depth=0):
    if current_depth > max_depth:
        return {"error": "Max depth exceeded"}

    structure = {}
    for item in os.listdir(base_dir):
        item_path = os.path.join(base_dir, item)
        if os.path.isdir(item_path):
            structure[item] = analyze_folder_structure(item_path, max_depth, current_depth + 1)
        else:
            structure[item] = "file"
    return structure

def save_structure_to_json(base_dir, output_dir):
    folder_name = os.path.basename(base_dir)
    output_file = os.path.join(output_dir, f"folder_{folder_name}_structure.json")
    structure = analyze_folder_structure(base_dir)
    with open(output_file, "w") as f:
        json.dump(structure, f, indent=4)
    print(f"Folder structure saved to {output_file}")

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

if __name__ == "__main__":
    base_dir = input("Enter the folder to analyze (e.g., C:\\dev): ").strip()
    output_dir = os.path.join("c:\\dev\\CodeBot", "storage")
    os.makedirs(output_dir, exist_ok=True)
    save_structure_to_json(base_dir, output_dir)

    base_dir = "c:\\dev\\CodeBot"
    knowledge_base_file = os.path.join(base_dir, "knowledge_base.json")
    generate_knowledge_base(base_dir, knowledge_base_file)
    update_imports(base_dir, knowledge_base_file)