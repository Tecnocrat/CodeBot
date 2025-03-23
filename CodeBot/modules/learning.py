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
    
def copy_core_for_testing(source="C:\\dev\\CodeBot\\codebot_core.py", dest="C:\\dev\\adn_trash_code\\testing\\codebot_core_test.py"):
    """
    Copies the main codebot_core.py file to a testing environment for experimentation
    and sets up a log for tracking modifications.
    """
    try:
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(source, "r") as src, open(dest, "w") as dst:
            dst.write(src.read())
        log_path = os.path.join(os.path.dirname(dest), "modifications.log")
        with open(log_path, "a") as log:
            log.write(f"Created test copy of {source} at {dest}\n")
        print(f"Copied {source} to {dest} for testing. Logged at {log_path}.")
    except FileNotFoundError:
        print(f"Error: Source file '{source}' not found.")

# CodeBot_Tracking
