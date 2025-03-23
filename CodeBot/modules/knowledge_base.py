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
