import os

def git_commit_and_push(commit_message, repo_path="C:/dev/CodeBot"):
    """
    Automates git commit and push for the specified repository path.
    """
    try:
        os.chdir(repo_path)  # Change to the repository directory
        os.system("git add .")
        os.system(f'git commit -m "{commit_message}"')
        os.system("git push")
        print("Commit and push completed successfully.")
    except Exception as e:
        print(f"Error during git commit and push: {e}")

# Example usage
if __name__ == "__main__":
    message = input("Enter commit message: ")
    git_commit_and_push(commit_message=message)

# CodeBot_Tracking
