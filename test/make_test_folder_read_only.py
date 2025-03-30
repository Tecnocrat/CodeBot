import os

def make_test_folder_read_only(folder_path):
    """
    Sets the test folder to read-only to prevent CodeBot from modifying its contents.
    """
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            os.chmod(file_path, 0o444)  # Read-only for all users
    print(f"Set {folder_path} to read-only.")

# Usage
make_test_folder_read_only("C:\\dev\\test")

# CodeBot_Tracking
