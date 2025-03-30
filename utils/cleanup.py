import os
import shutil

def clean_cache_dirs(base_dir):
    """
    Removes __pycache__ and .pytest_cache directories recursively.
    """
    for root, dirs, files in os.walk(base_dir):
        for dir_name in dirs:
            if dir_name in ["__pycache__", ".pytest_cache"]:
                dir_path = os.path.join(root, dir_name)
                print(f"Removing: {dir_path}")
                shutil.rmtree(dir_path)

if __name__ == "__main__":
    base_dir = "c:\\dev"
    clean_cache_dirs(base_dir)
    print("Cleanup completed.")