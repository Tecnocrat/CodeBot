import os
import json
import re
from genetic.genetic_population import evaluate_population
import sys
import os
from config import KNOWLEDGE_BASE_DIR

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(BASE_DIR)

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
            "ai_behaviors": detect_ai_behaviors(root, files),
        }

    # Evaluate genetic populations for analysis
    genetic_dir = os.path.join(base_dir, "genetic", "populations")
    if os.path.exists(genetic_dir):
        populations_analysis = evaluate_population(genetic_dir)
        code_structure["genetic"] = code_structure.get("genetic", {})
        code_structure["genetic"]["populations_analysis"] = populations_analysis

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

if __name__ == "__main__":
    base_dir = input("Enter the folder to analyze (e.g., C:\\dev): ").strip()
    output_dir = os.path.join("c:\\dev\\CodeBot", "storage")
    os.makedirs(output_dir, exist_ok=True)
    save_structure_to_json(base_dir, output_dir)

    base_dir = "c:\\dev\\CodeBot"
    knowledge_base_file = os.path.join(base_dir, "knowledge_base.json")
    generate_knowledge_base(base_dir, knowledge_base_file)
    update_imports(base_dir, knowledge_base_file)