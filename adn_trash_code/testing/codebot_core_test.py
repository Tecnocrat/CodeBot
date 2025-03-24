#KEYWORD: CodeBot_Tracking

import os
import sys
sys.path.append("C:\\dev\\CodeBot")
import threading
import time
import base64
import zipfile
import keyboard  # pip install keyboard

# --- Global Paths ---
CODEBOT_DIR = os.path.dirname(os.path.abspath(__file__))
ADB_DIR = os.path.join(os.path.dirname(CODEBOT_DIR), "adn_trash_code")
os.makedirs(ADB_DIR, exist_ok=True)

MODULES_DIR = os.path.join(CODEBOT_DIR, "modules")
if MODULES_DIR not in sys.path:
    sys.path.append(MODULES_DIR)

# --- Import from modules ---
from modules.file_manager import setup_project_structure, scan_test_folder
from modules.compression import compress_libraries, decompress_library
from modules.knowledge_base import create_knowledge_archive
from modules.ui_interface import launch_ui, handle_input
from modules.dictionaries import save_wordlists
from modules.summarization import summarize_runtime
from modules.resources import monitor_resources
from modules.functions import generate_symbol_library
from modules.learning import load_python_library
from modules.learning import analyze_library
from modules.learning import copy_core_for_testing

# --- Global Variables ---
conversation_text = """
    Full Copilot conversation copied from Edge browser.
    Paste everything here within triple quotes.
    """
from modules.knowledge_base import export_conversation_log
export_conversation_log(conversation_text)


# ------------------
# CORE FUNCTIONS (processing functions)
# ------------------
def encode_instruction(instruction):
    compressed = instruction.encode("utf-8")
    return base64.b64encode(compressed).decode("utf-8")

def decode_instruction(encoded):
    compressed = base64.b64decode(encoded).decode("utf-8")
    return compressed.replace("(", " ").replace(")", " ").replace("|", " | ")

def generate_code(instruction):
    parts = instruction.split("|")
    if len(parts) != 3:
        return f"# Invalid instruction format: {instruction}"
    func_name = parts[1].strip()
    params = parts[2].strip()
    params_with_spaces = ", ".join(param.strip() for param in params.split(","))
    formatted_return = " + ".join(param.strip() for param in params.split(","))
    return (f"def {func_name}({params_with_spaces}):\n"
            f"    return {formatted_return}\n")

def save_code_to_file(code, filename="dynamic_archive.py"):
    file_path = os.path.join(ADB_DIR, filename)
    with open(file_path, "a") as file:
        file.write(code + "\n\n")
    print(f"Code archived at: {file_path}")

def load_archived_code(filename="dynamic_archive.py"):
    try:
        file_path = os.path.join(ADB_DIR, filename)
        with open(file_path, "r") as file:
            archived_code = file.readlines()
        print(f"Loaded {len(archived_code)} lines of archived code.")
        return archived_code
    except FileNotFoundError:
        print("No archived code found. Starting fresh.")
        return []

def refine_code(generated_code, archived_code):
    refined_code = generated_code.split("\n")
    refined_lines = []
    for line in refined_code:
        is_refined = any("# Refined from archive" in l for l in refined_lines)
        if line.strip() in archived_code and not is_refined:
            refined_lines.append(f"{line.strip()}  # Refined from archive")
        else:
            refined_lines.append(line.strip())
    return "\n".join(refined_lines)

def split_and_save_base64(encoded_text, volume_base="codebot_core_base64_vol", chunk_size=9999):
    volumes = [encoded_text[i:i+chunk_size] for i in range(0, len(encoded_text), chunk_size)]
    volume_files = []
    for index, chunk in enumerate(volumes, start=1):
        filename = f"{volume_base}{index}.txt"
        output_path = os.path.join(ADB_DIR, filename)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(chunk)
        volume_files.append(filename)
        print(f"Saved Volume {index} to {filename}")
    return volume_files

def compress_and_encode_script(script_path=None, zip_name="codebot_core.zip", output_file_base="codebot_core_base64_vol"):
    if script_path is None:
        script_path = os.path.abspath(__file__)
    zip_path = os.path.join(ADB_DIR, zip_name)
    with zipfile.ZipFile(zip_path, "w") as zipf:
        zipf.write(script_path, arcname="codebot_core.py")
    print(f"Script compressed into: {zip_name}")
    with open(zip_path, "rb") as zip_file:
        encoded = base64.b64encode(zip_file.read()).decode("utf-8")
    volume_files = split_and_save_base64(encoded, volume_base=output_file_base, chunk_size=9999)
    print("Base64-encoded script has been split into volumes.")
    return volume_files

def process_request(encoded_request):
    instruction = decode_instruction(encoded_request)
    print(f"Received Instruction: {instruction}")
    generated_code = generate_code(instruction)
    archived_code = load_archived_code()
    refined_code = refine_code(generated_code, archived_code)
    save_code_to_file(refined_code)
    debug_file = os.path.join(ADB_DIR, "debug_results.txt")
    os.makedirs(ADB_DIR, exist_ok=True)
    with open(debug_file, "a") as debug_results:
        debug_results.write(f"Received Instruction: {instruction}\n")
        debug_results.write(f"Generated Code:\n{generated_code}\n")
        debug_results.write(f"Refined Code:\n{refined_code}\n\n")
    compressed_response = encode_instruction(refined_code)
    decoded_response = decode_instruction(compressed_response).replace(" :", ":")
    return compressed_response, decoded_response

def number_counter(filename="number_database.txt", max_iterations=1000):
    file_path = os.path.join(ADB_DIR, filename)
    last_number = 0
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
            if lines:
                last_number = int(lines[-1].strip())
            print(f"Resuming from last number: {last_number}")
    except FileNotFoundError:
        print(f"No database found. Starting fresh from {last_number}.")
    with open(file_path, "a") as file:
        for i in range(1, max_iterations + 1):
            current_number = last_number + i
            file.write(f"{current_number}\n")
        print(f"Counted and saved numbers up to {last_number + max_iterations}.")

def runtime_execution():
    """
    CodeBot waits for user input, responds to greetings, recognizes words from a dictionary,
    suggests similar words, and exits after 60 seconds of inactivity or when 'quit' is typed.
    Includes a standby delay after each interaction to reduce resource usage.
    """
    import time

    print("CodeBot is ready and waiting for your input. Type 'quit' to exit, or greet me!")
    start_time = time.time()  # Track the time when the loop begins

    while True:
        # Calculate elapsed time
        elapsed_time = time.time() - start_time
        if elapsed_time > 60:  # Exit if there's no interaction for 60 seconds
            print("CodeBot: No interaction detected. Goodbye!")
            break

        # Get user input
        user_input = input("You: ").strip().lower()

        # Handle user input
        if user_input in ["hello", "hi", "hey", "greetings"]:
            print("CodeBot: Hello, I'm CodeBot!")
        elif user_input in ["quit"]:
            print("CodeBot: Goodbye!")
            break
        else:
            # Recognize words from the input using the dictionary
            recognized = word_recognition(user_input)
            if recognized:
                print(f"CodeBot: I recognized these words: {', '.join(recognized)}")
                # Suggest similar words for the first recognized word
                suggestions = suggest_word(list(recognized)[0])
                if suggestions:
                    print(f"CodeBot: Here are some word suggestions: {', '.join(suggestions)}")
            else:
                print("CodeBot: I didn't recognize any valid words. Try again!")

        # Standby delay after each user interaction
        time.sleep(0.5)

# ------------------
# PROJECT STRUCTURE AND MODULARIZATION FUNCTIONS
# ------------------
def setup_project_structure(base_folder="CodeBot", modules_folder="modules", target_folder="../adn_trash_code"):
    os.makedirs(base_folder, exist_ok=True)
    modules_path = os.path.join(base_folder, modules_folder)
    os.makedirs(modules_path, exist_ok=True)
    target_path = os.path.join(os.path.dirname(base_folder), "adn_trash_code")
    os.makedirs(target_path, exist_ok=True)
    print(f"Created folders: {modules_path}, {target_path}")
    initial_files = ["functions.py", "summarization.py", "compression.py", "resources.py", "file_manager.py"]
    for file in initial_files:
        file_path = os.path.join(modules_path, file)
        if not os.path.exists(file_path):
            with open(file_path, "w") as f:
                f.write(f"# Placeholder for {file}\n")
            print(f"Created file: {file_path}")
    print("Project structure setup complete!")

def modularize_functions(modules_folder="modules", main_script=None):
    if main_script is None:
        main_script = os.path.abspath(__file__)
    if not os.path.isdir(modules_folder):
        alternative = os.path.join("CodeBot", modules_folder)
        if os.path.isdir(alternative):
            modules_folder = alternative
    module_mapping = {
        "generate_symbol_library": "functions.py",
        "summarize_runtime": "summarization.py",
        "compress_libraries": "compression.py",
        "decompress_library": "compression.py",
        "monitor_resources": "resources.py",
        "setup_project_structure": "file_manager.py"
    }
    print("\nModularizing functions from the main script...")
    try:
        with open(main_script, "r") as main_file:
            main_lines = main_file.readlines()
        for func_name, module_file in module_mapping.items():
            module_path = os.path.join(modules_folder, module_file)
            if os.path.exists(module_path):
                with open(module_path, "r") as module:
                    module_content = module.read()
            else:
                module_content = ""
            with open(module_path, "a") as module:
                for line in main_lines:
                    if f"def {func_name}" in line and f"def {func_name}" not in module_content:
                        module.write(line)
                        print(f"Moved {func_name} to {module_file}")
    except FileNotFoundError:
        print(f"Main script '{main_script}' not found. Cannot modularize functions.")

def compress_and_encode_script(script_path=None, zip_name="codebot_core.zip", output_file_base="codebot_core_base64_vol"):
    if script_path is None:
        script_path = os.path.abspath(__file__)
    zip_path = os.path.join(ADB_DIR, zip_name)
    with zipfile.ZipFile(zip_path, "w") as zipf:
        zipf.write(script_path, arcname="codebot_core.py")
    print(f"Script compressed into: {zip_name}")
    with open(zip_path, "rb") as zip_file:
        encoded = base64.b64encode(zip_file.read()).decode("utf-8")
    volume_files = split_and_save_base64(encoded, volume_base=output_file_base, chunk_size=9999)
    print("Base64-encoded script has been split into volumes.")
    return volume_files

def split_and_save_base64(encoded_text, volume_base="codebot_core_base64_vol", chunk_size=9999):
    volumes = [encoded_text[i:i+chunk_size] for i in range(0, len(encoded_text), chunk_size)]
    volume_files = []
    for index, chunk in enumerate(volumes, start=1):
        filename = f"{volume_base}{index}.txt"
        output_path = os.path.join(ADB_DIR, filename)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(chunk)
        volume_files.append(filename)
        print(f"Saved Volume {index} to {filename}")
    return volume_files

def scan_test_folder(folder_path):
    """
    Scans the test folder for available tools and returns a list of files.
    """
    return [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

def word_recognition(input_text, dictionary_path="C:\\dev\\adn_trash_code\\dictionaries\\english_words.txt"):
    """
    Checks if the input contains valid English words from the dictionary.
    """
    with open(dictionary_path, "r", encoding="utf-8") as f:
        word_list = set(f.read().splitlines())
    
    input_words = set(input_text.lower().split())
    recognized_words = input_words.intersection(word_list)
    
    return recognized_words

def suggest_word(input_word, dictionary_path="C:\\dev\\adn_trash_code\\dictionaries\\english_words.txt"):
    """
    Suggests words from the dictionary that start with the same letters as the input word.
    """
    with open(dictionary_path, "r", encoding="utf-8") as f:
        word_list = [word.strip() for word in f.readlines()]

    suggestions = [word for word in word_list if word.startswith(input_word.lower())]
    return suggestions[:5]  # Return up to 5 suggestions

# ------------------
# MAIN EXECUTION
# ------------------
if __name__ == "__main__":
    print("\nStep 1: Setting up project structure...")
    setup_project_structure()

    print("\nStep 2: Modularizing functions...")
    modularize_functions()

    resource_monitor_thread = threading.Thread(target=monitor_resources, daemon=True)
    resource_monitor_thread.start()

    print("\nStep 3: Launching UI Interface...")
    launch_ui()

    print("\nStep 4: Creating knowledge archive...")
    create_knowledge_archive("../adn_trash_code")

    print("\nStep 5: Compressing libraries...")
    compress_libraries()

    print("\nStep 6: Encoding main script to Base64 and splitting into volumes...")
    volumes_created = compress_and_encode_script()
    print("Volumes created:", volumes_created)

    print("\nStep 7: Testing decompression of runtime library...")
    decompress_library(file_to_extract="runtime_library.txt")

    print("\nStep 8: Scan test folder...")
    test_tools = scan_test_folder("C:\\dev\\test")
    print(f"Available tools in the test folder: {test_tools}")
    
    print("\nStep 9: Generating symbol library...")
    save_wordlists("C:\\dev\\adn_trash_code\\dictionaries")

    print("\nStep 10: Teaching CodeBot Python...")
    python_libs = load_python_library()
    for lib in python_libs:
        analyze_library(os.path.join("C:\\dev\\adn_trash_code\\python_libs", lib), debug=False)

    print("\nStep 11: Creating parallel testing environment...")
    copy_core_for_testing()

    print("\nAll tasks completed successfully.")

# CodeBot_Tracking
