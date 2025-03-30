import os
import zipfile
import shutil
from datetime import datetime
from modules.file_manager import inject_text

# Base directory for all operations
BASE_DIR = "c:\\dev"
CODEBOT_DIR = os.path.join(BASE_DIR, "CodeBot")
KNOWLEDGE_BASE_DIR = os.path.join(CODEBOT_DIR, "knowledge_base")  # Updated path

def create_knowledge_archive(output_folder="../adn_trash_code"):
    """
    Creates or updates the 'knowledge_archive.zip' file with essential CodeBot resources.
    """
    archive_path = os.path.join(output_folder, "knowledge_archive.zip")
    os.makedirs(output_folder, exist_ok=True)  # Ensure the folder exists

    with zipfile.ZipFile(archive_path, "w") as zipf:
        # Add core CodeBot zip file if it exists
        core_zip_path = os.path.join(output_folder, "codebot_core.zip")
        if os.path.exists(core_zip_path):
            zipf.write(core_zip_path, "codebot_core.zip")
        
        # Add dictionaries folder to the archive
        dictionaries_path = os.path.join(output_folder, "dictionaries")
        if os.path.exists(dictionaries_path):
            for root, _, files in os.walk(dictionaries_path):
                for file in files:
                    full_path = os.path.join(root, file)
                    arcname = os.path.relpath(full_path, output_folder)
                    zipf.write(full_path, arcname)

        print(f"Knowledge archive created/updated at: {archive_path}")


def retrieve_python_concept(concept_name):
    """
    Retrieves a Python concept from the knowledge_base.
    """
    concept_file = os.path.join(KNOWLEDGE_BASE_DIR, f"{concept_name}.txt")
    if os.path.exists(concept_file):
        with open(concept_file, 'r') as file:
            return file.read()
    else:
        return f"Concept '{concept_name}' not found in knowledge_base."


def retrieve_conversation_log(keyword, log_path="C:\\dev\\adn_trash_code\\knowledge_base\\CodeBot_conversation_log.txt"):
    """
    Searches the conversation log for a specific keyword and retrieves matching lines.

    Args:
        keyword (str): The keyword to search for.
        log_path (str): The path to the conversation log file.

    Returns:
        list or str: A list of matching lines or a message if no matches are found.
    """
    if not os.path.exists(log_path):
        return "Conversation log file not found."

    try:
        with open(log_path, "r", encoding="utf-8") as log:
            lines = log.readlines()
            matches = [line for line in lines if keyword.lower() in line.lower()]
            return matches if matches else "No matches found in the conversation log."
    except Exception as e:
        return f"Error reading conversation log: {e}"


def save_conversation_to_log(conversation, log_path="C:\\dev\\adn_trash_code\\knowledge_base\\CodeBot_conversation_log.txt"):
    """
    Saves the current conversation text to a log file for future reference.
    Splits logs by session timestamps for better organization.

    Args:
        conversation (str): The conversation text to save.
        log_path (str): The path to the log file.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    os.makedirs(os.path.dirname(log_path), exist_ok=True)  # Ensure the log directory exists

    try:
        with open(log_path, "a", encoding="utf-8") as log:
            log.write(f"[{timestamp}]\n{conversation}\n")
        print(f"Conversation saved to {log_path}.")
    except Exception as e:
        print(f"Error saving conversation: {e}")


def export_conversation_log(conversation_text, log_path="C:\\dev\\adn_trash_code\\knowledge_base\\CodeBot_conversation_log.txt"):
    """
    Exports conversation text into a log file for persistence.

    Args:
        conversation_text (str): The conversation text to export.
        log_path (str): The path to the log file.
    """
    os.makedirs(os.path.dirname(log_path), exist_ok=True)  # Ensure the log directory exists

    try:
        with open(log_path, "a", encoding="utf-8") as log_file:
            log_file.write(conversation_text + "\n")
        print(f"Conversation exported successfully to {log_path}.")
    except Exception as e:
        print(f"Failed to export conversation: {e}")


def save_knowledge(file_path):
    """
    Saves a file to the knowledge_base directory.
    """
    os.makedirs(KNOWLEDGE_BASE_DIR, exist_ok=True)
    target_path = os.path.join(KNOWLEDGE_BASE_DIR, os.path.basename(file_path))
    shutil.copy(file_path, target_path)
    print(f"Saved knowledge to {target_path}")


# Example usage
if __name__ == "__main__":
    print("\nExample: Save Knowledge")
    file_to_save = input("Enter file path to save knowledge: ")
    knowledge_to_save = input("Enter knowledge to save: ")
    save_knowledge(file_to_save)