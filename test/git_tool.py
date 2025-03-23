import os

def git_tool():
    """
    Simple terminal interface for Git commands: branch, commit, merge.
    """
    while True:
        print("\nGit Tool Options:")
        print("1. Create a new branch")
        print("2. Commit changes")
        print("3. Merge a branch")
        print("4. Exit")

        choice = input("Choose an option (1-4): ").strip()
        if choice == "1":
            branch_name = input("Enter new branch name: ").strip()
            os.system(f"git checkout -b {branch_name}")
            print(f"Branch '{branch_name}' created.")
        elif choice == "2":
            commit_message = input("Enter commit message: ").strip()
            os.system("git add .")
            os.system(f'git commit -m "{commit_message}"')
            os.system("git push")
            print("Changes committed and pushed.")
        elif choice == "3":
            branch_to_merge = input("Enter branch name to merge: ").strip()
            os.system(f"git merge {branch_to_merge}")
            print(f"Branch '{branch_to_merge}' merged.")
        elif choice == "4":
            print("Exiting Git Tool.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    git_tool()
