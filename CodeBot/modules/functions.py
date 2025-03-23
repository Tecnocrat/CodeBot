import os

def generate_symbol_library(filename="symbol_library.txt", max_symbols=256):
    """
    Generates a library of ASCII symbols and writes them to a file.
    """
    target_folder = os.path.join(os.path.dirname(os.getcwd()), "adn_trash_code")
    os.makedirs(target_folder, exist_ok=True)
    file_path = os.path.join(target_folder, filename)
    with open(file_path, "w", encoding="utf-8") as file:
        for i in range(max_symbols):
            try:
                file.write(f"{i}: {chr(i)}\n")
            except UnicodeEncodeError:
                file.write(f"{i}: [Unencodable Character]\n")
    print(f"Symbol library created with up to {max_symbols} entries.")
