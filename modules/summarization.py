import time
import os
import shutil
from modules.compression import compress_libraries

def summarize_runtime(start_time, actions, filename="runtime_summary.txt", library="runtime_library.txt"):
    """
    Summarizes runtime by writing start/end times, elapsed time, and actions taken.
    """
    end_time = time.time()
    elapsed_time = end_time - start_time

    target_folder = os.path.join(os.path.dirname(os.getcwd()), "adn_trash_code")
    os.makedirs(target_folder, exist_ok=True)

    summary_path = os.path.join(target_folder, filename)
    with open(summary_path, "a", encoding="utf-8") as file:
        file.write("Runtime Summary:\n")
        file.write(f"Start Time: {time.ctime(start_time)}\n")
        file.write(f"End Time: {time.ctime(end_time)}\n")
        file.write(f"Elapsed Time: {elapsed_time:.2f} seconds\n")
        file.write("Actions Taken:\n")
        for action in actions:
            file.write(f"- {action}\n")
        file.write("\n")
    
    compress_libraries(target_folder=target_folder)
    print(f"Runtime summary saved to {filename}.")

import os
import shutil

def incremental_backup(src, dest, excluded_folders):
    """
    Perform an incremental backup of files and directories, excluding specific folders.
    """
    for root, dirs, files in os.walk(src):
        # Exclude specified folders
        dirs[:] = [d for d in dirs if d not in excluded_folders]
        for file in files:
            file_path = os.path.join(root, file)
            dest_path = os.path.join(dest, os.path.relpath(file_path, src))
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            # Copy only if the file is new or modified
            if not os.path.exists(dest_path) or os.path.getmtime(file_path) > os.path.getmtime(dest_path):
                shutil.copy2(file_path, dest_path)

if __name__ == "__main__":
    src_directory = "C:\\dev"  # Adjust as needed
    dest_directory = "C:\\dev_backup"
    excluded = {"venv", "OpenChatKit"}

    print(f"Performing incremental backup from {src_directory} to {dest_directory}...\n")
    incremental_backup(src_directory, dest_directory, excluded)
    print("Backup complete!")
