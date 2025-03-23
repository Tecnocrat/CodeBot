import os
import zipfile

def create_knowledge_archive(output_folder="../adn_trash_code"):
    """
    Creates or updates the 'knowledge_archive.zip' file with essential CodeBot resources.
    """
    archive_path = os.path.join(output_folder, "knowledge_archive.zip")
    os.makedirs(output_folder, exist_ok=True)  # Ensure the folder exists

    with zipfile.ZipFile(archive_path, "w") as zipf:
        # Add core resources, like codebot_core.zip
        core_zip_path = os.path.join(output_folder, "codebot_core.zip")
        if os.path.exists(core_zip_path):
            zipf.write(core_zip_path, "codebot_core.zip")
        
        # Add any other files, such as dictionaries or logs
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
    for file in os.listdir(knowledge_dir):
        if file.endswith(".txt"):
            file_path = os.path.join(knowledge_dir, file)
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
                explanations = {line[1:].strip(): "" for line in lines if line.startswith("#")}
                for line in lines:
                    if line.startswith("#"):
                        current_key = line[1:].strip()
                    elif current_key:
                        explanations[current_key] += line
                if concept.capitalize() in explanations:
                    return explanations[concept.capitalize()]
    return "Concept not found in knowledge base."

# CodeBot_Tracking
