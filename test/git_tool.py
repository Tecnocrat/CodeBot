import os

def git_tool():
    """
    Enhanced terminal interface for Git commands:
    - Manages all projects within C:\dev.
    - Supports branch creation, committing, merging, and pushing.
    """
    dev_folder = "C:\\dev"

    while True:
        print("\nGit Tool Options:")
        print("1. Initialize Git in a Folder")
        print("2. Create a New Branch")
        print("3. Commit Changes")
        print("4. Merge a Branch")
        print("5. Push to Remote Repository")
        print("6. Show Git Status")
        print("7. Exit")

        choice = input("Choose an option (1-7): ").strip()

        if choice == "1":
            folder_path = input(f"Enter folder path (default: {dev_folder}): ").strip() or dev_folder
            os.chdir(folder_path)
            os.system("git init")
            print(f"Initialized Git in {folder_path}.")
        elif choice == "2":
            branch_name = input("Enter new branch name: ").strip()
            os.system(f"git checkout -b {branch_name}")
            print(f"Branch '{branch_name}' created.")
        elif choice == "3":
            commit_message = input("Enter commit message: ").strip()
            os.system("git add .")
            os.system(f'git commit -m "{commit_message}"')
            print("Changes committed.")
        elif choice == "4":
            branch_to_merge = input("Enter branch name to merge: ").strip()
            os.system(f"git merge {branch_to_merge}")
            print(f"Branch '{branch_to_merge}' merged.")
        elif choice == "5":
            os.system("git push")
            print("Changes pushed to remote repository.")
        elif choice == "6":
            os.system("git status")
        elif choice == "7":
            print("Exiting Git Tool.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    git_tool()
