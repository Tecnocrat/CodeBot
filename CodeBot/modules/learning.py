import os

def load_python_library(library_path="C:\\dev\\adn_trash_code\\python_libs"):
    """
    Loads Python libraries from the specified directory for CodeBot's learning.
    """
    try:
        libraries = [f for f in os.listdir(library_path) if f.endswith(".py")]
        print(f"Loaded Python libraries: {', '.join(libraries)}")
        return libraries
    except FileNotFoundError:
        print("Error: Python library folder not found.")
        return []

def analyze_library(library_file):
    """
    Analyzes a Python library file and summarizes its contents (e.g., functions and classes).
    """
    try:
        with open(library_file, "r") as f:
            lines = f.readlines()
        
        functions = [line.strip() for line in lines if line.strip().startswith("def ")]
        classes = [line.strip() for line in lines if line.strip().startswith("class ")]
        print(f"Functions: {functions}")
        print(f"Classes: {classes}")
        return functions, classes
    except FileNotFoundError:
        print(f"Error: File '{library_file}' not found.")
        return [], []
