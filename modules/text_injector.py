from modules.file_manager import inject_text

def inject_custom_text(file_path, custom_text, position="append", target_line=None):
    """
    Injects custom text into a file.
    """
    return inject_text(file_path, custom_text, position, target_line)


# Example usage
if __name__ == "__main__":
    print("\n--- Text Injector ---")
    file_to_modify = input("Enter file path: ").strip()
    injection_mode = input("Enter injection mode (append/overwrite/insert): ").strip().lower()
    text_to_inject = input("Enter text to inject: ").strip()
    line_number = None

    if injection_mode == "insert":
        try:
            line_number = int(input("Enter line number for insertion: "))
        except ValueError:
            print("Invalid line number. Please enter a valid integer.")
            exit(1)

    # Inject the text and print the result
    result = inject_custom_text(file_to_modify, text_to_inject, injection_mode, line_number)
    print(result)

# CodeBot_Tracking