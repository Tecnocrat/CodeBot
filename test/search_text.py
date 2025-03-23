import os

def search_text_in_files(search_text, folder_path="C:\\dev"):
    """
    Searches for the specified text in all files within the folder and its subfolders.
    """
    results = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        for line_num, line in enumerate(f, 1):
                            if search_text in line:
                                results.append(f"{file_path} (Line {line_num}): {line.strip()}")
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
    return results

# Example usage
if __name__ == "__main__":
    text = input("Enter text to search for: ")
    folder = input("Enter folder path (default: C:\\dev): ") or "C:\\dev"
    matches = search_text_in_files(text, folder)
    if matches:
        print("Matches found:")
        for match in matches:
            print(match)
    else:
        print("No matches found.")

# CodeBot_Tracking
