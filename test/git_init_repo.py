import os

def initialize_and_push_to_github(local_path, github_username, repo_name, commit_message):
    os.system(f'cd {local_path} && git init')
    os.system(f'cd {local_path} && git add .')
    os.system(f'cd {local_path} && git commit -m "{commit_message}"')
    os.system(f'cd {local_path} && git branch -M main')
    os.system(f'cd {local_path} && git remote add origin https://github.com/{github_username}/{repo_name}.git')
    os.system(f'cd {local_path} && git push -u origin main')

# Example usage:
initialize_and_push_to_github("C:\\Dev", "tecnocrat", "CodeBot", "Initial commit")
