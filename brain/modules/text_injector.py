import os

def inject_text(file_path, text, position="append", target_line=None):
    """
    Injects text into a file. Supports append, overwrite, or insertion at specific lines.
    
    Args:
        file_path (str): Path to the file where text should be injected.
        text (str): The text to inject into the file.
        position (str): Injection mode - "append", "overwrite", or "insert".
        target_line (int): Line number for "insert" mode. Ignored otherwise.
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
            
            if target_line < 1 or target_line > len(lines):
                raise ValueError("Invalid target line number.")
            
            lines.insert(target_line - 1, text + "\n")
            with open(file_path, "w", encoding="utf-8") as f:
                f.writelines(lines)
        else:
            raise ValueError("Invalid injection position or missing target line.")

        print(f"Injected text into {file_path} at {position} position.")
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"Error during injection: {e}")

# Example usage
if __name__ == "__main__":
    file_to_modify = input("Enter file path: ")
    injection_mode = input("Enter injection mode (append/overwrite/insert): ")
    text_to_inject = input("Enter text to inject: ")
    line_number = None
    if injection_mode == "insert":
        line_number = int(input("Enter line number for insertion: "))
    inject_text(file_to_modify, text_to_inject, injection_mode, line_number)

# CodeBot_Tracking
