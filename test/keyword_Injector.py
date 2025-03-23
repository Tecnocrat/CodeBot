import os

def inject_keyword(folder_path="C:\\dev", keyword="CodeBot_Tracking"):
    """
    Injects a unique keyword into all Python files in the specified folder tree.
    """
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r+", encoding="utf-8") as f:
                        content = f.read()
                        if keyword not in content:  # Avoid duplicate injections
                            f.write(f"\n# {keyword}\n")
                            print(f"Keyword injected into {file_path}")
                except Exception as e:
                    print(f"Error injecting keyword into {file_path}: {e}")

# Example usage
inject_keyword()
