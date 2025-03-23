import os
import zipfile

def create_knowledge_archive(output_folder="../adn_trash_code"):
    """
    Creates an empty 'knowledge_archive.zip' file in the specified folder if it doesn't already exist.
    """
    archive_path = os.path.join(output_folder, "knowledge_archive.zip")
    os.makedirs(output_folder, exist_ok=True)  # Ensure the folder exists
    
    if not os.path.exists(archive_path):
        with zipfile.ZipFile(archive_path, "w") as zipf:
            pass  # Create an empty archive
        print(f"Created empty knowledge archive: {archive_path}")
    else:
        print(f"Knowledge archive already exists: {archive_path}")

def compress_libraries(zip_filename="knowledge_archive.zip", target_folder="../adn_trash_code"):
    """
    Compresses all .txt files in the target folder (including runtime_library.txt) into a zip archive.
    """
    zip_path = os.path.join(target_folder, zip_filename)
    with zipfile.ZipFile(zip_path, "w") as zipf:
        for root, _, files in os.walk(target_folder):
            for file in files:
                if file == "runtime_library.txt" or file.endswith(".txt"):
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, arcname=file)
    print(f"Knowledge libraries compressed into {zip_filename}.")

def decompress_library(zip_filename="knowledge_archive.zip", target_folder="../adn_trash_code", file_to_extract=None):
    """
    Decompresses the specified file (or all files) from the zip archive in the target folder.
    """
    zip_path = os.path.join(target_folder, zip_filename)
    if not os.path.exists(zip_path):
        print(f"{zip_filename} not found in {target_folder}. Nothing to decompress.")
        return
    with zipfile.ZipFile(zip_path, "r") as zipf:
        if file_to_extract:
            try:
                zipf.extract(file_to_extract, target_folder)
                print(f"{file_to_extract} extracted successfully to {target_folder}.")
            except KeyError:
                print(f"{file_to_extract} not found in the archive.")
        else:
            zipf.extractall(target_folder)
            print("All files decompressed successfully.")
