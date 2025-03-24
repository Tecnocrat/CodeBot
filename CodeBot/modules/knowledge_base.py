import os
import zipfile
from datetime import datetime

def create_knowledge_archive(output_folder="../adn_trash_code"):
    """
    Creates or updates the 'knowledge_archive.zip' file with essential CodeBot resources.
    """
    archive_path = os.path.join(output_folder, "knowledge_archive.zip")
    os.makedirs(output_folder, exist_ok=True)  # Ensure the folder exists

    with zipfile.ZipFile(archive_path, "w") as zipf:
        core_zip_path = os.path.join(output_folder, "codebot_core.zip")
        if os.path.exists(core_zip_path):
            zipf.write(core_zip_path, "codebot_core.zip")
        
        dictionaries_path = os.path.join(output_folder, "dictionaries")
        for root, dirs, files in os.walk(dictionaries_path):
            for file in files:
                full_path = os.path.join(root, file)
                arcname = os.path.relpath(full_path, output_folder)
                zipf.write(full_path, arcname)

        print(f"Knowledge archive created/updated at: {archive_path}")
def retrieve_python_concept(concept, knowledge_dir="C:\\dev\\adn_trash_code\\knowledge_base\\python"):
    """
    Searches for a Python concept across multiple files in the knowledge directory.
    """
    explanations = {}
    for file in os.listdir(knowledge_dir):
        if file.endswith(".txt"):
            file_path = os.path.join(knowledge_dir, file)
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
                current_key = None
                for line in lines:
                    if line.startswith("#"):
                        current_key = line[1:].strip()
                        explanations[current_key] = ""
                    elif current_key:
                        explanations[current_key] += line
    return explanations.get(concept.capitalize(), "Concept not found.")
def retrieve_conversation_log(keyword, log_path="C:\\dev\\adn_trash_code\\knowledge_base\\CodeBot_conversation_log.txt"):
    """
    Searches the conversation log for a specific keyword and retrieves matching lines.
    """
    try:
        with open(log_path, "r", encoding="utf-8") as log:
            lines = log.readlines()
            matches = [line for line in lines if keyword.lower() in line.lower()]
            return matches if matches else "No matches found in the conversation log."
    except FileNotFoundError:
        return "Conversation log file not found."
def save_conversation_to_log(conversation, log_path="C:\\dev\\adn_trash_code\\knowledge_base\\CodeBot_conversation_log.txt"):
    """
    Saves the current conversation text to a log file for future reference.
    Splits logs by session timestamps for better organization.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(log_path, "a+", encoding="utf-8") as log:
            # Remove legacy placeholders if present
            log.seek(0)
            content = log.read()
            if "Full Copilot conversation copied from Edge browser." in content:
                content = content.replace("Full Copilot conversation copied from Edge browser.\nPaste everything here within triple quotes.\n\n", "")
                log.seek(0)
                log.truncate()
                log.write(content)

            # Add timestamped conversation
            log.write(f"[{timestamp}]\n{conversation}\n")
        print(f"Conversation saved to {log_path}.")
    except Exception as e:
        print(f"Error saving conversation: {e}")
def export_conversation_log(conversation_text, log_path="C:\\dev\\adn_trash_code\\knowledge_base\\CodeBot_conversation_log.txt"):
    """
    Exports conversation text into a log file for persistence.
    """
    try:
        with open(log_path, "a", encoding="utf-8") as log_file:
            log_file.write(conversation_text + "\n")
        print(f"Conversation exported successfully to {log_path}.")
    except Exception as e:
        print(f"Failed to export conversation: {e}")
def inject_text(file_path, text, mode="append"):
    """
    Injects specified text into the given file.
    """
    try:
        with open(file_path, mode, encoding="utf-8") as f:
            f.write(text + "\n")
        return f"Text injected into {file_path}."
    except Exception as e:
        return f"Error injecting text: {e}"
