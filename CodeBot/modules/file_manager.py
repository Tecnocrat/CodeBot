import os

def setup_project_structure(base_folder="CodeBot", modules_folder="modules", target_folder="../adn_trash_code"):
    """
    Automatically creates the required folders and placeholder module files.
    The target_folder is set to "../adn_trash_code" assuming "CodeBot" is inside your DEV folder.
    """
    # Create the base folder (e.g., "CodeBot")
    os.makedirs(base_folder, exist_ok=True)
    
    # Create the modules folder inside CodeBot
    modules_path = os.path.join(base_folder, modules_folder)
    os.makedirs(modules_path, exist_ok=True)
    
    # Create the runtime artifacts folder outside of CodeBot (e.g., DEV\adn_trash_code)
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
    """
    try:
        return [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    except FileNotFoundError:
        print(f"Error: The folder '{folder_path}' does not exist.")
        return []