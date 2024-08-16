import subprocess
import os
import yaml

def clone_repo(repo_url, clone_dir, github_token, user_name, repo_owner, repo_name):
    auth_repo_url = repo_url.replace('https://', f'https://{user_name}:{github_token}@')
    subprocess.run(['git', 'clone', auth_repo_url, clone_dir], check=True)

def git_add_commit_push(file_path, commit_message, repo_dir, github_token, user_name, user_email, repo_owner, repo_name, reset_head):
    # Setup user configuration
    subprocess.run(['git', 'config', 'user.name', user_name], cwd=repo_dir, check=True)
    subprocess.run(['git', 'config', 'user.email', user_email], cwd=repo_dir, check=True)
    
    # Add the file
    subprocess.run(['git', 'add', file_path], cwd=repo_dir, check=True)
    
    # Commit the changes
    subprocess.run(['git', 'commit', '-m', commit_message], cwd=repo_dir, check=True)
    
    if reset_head == "HARD":
        # Reset HEAD to the previous commit
        subprocess.run(['git', 'reset', '--hard', 'HEAD~1'], cwd=repo_dir, check=True)
    
    # Push the changes (force push if reset_head is HARD)
    push_command = ['git', 'push', f'https://{user_name}:{github_token}@github.com/{repo_owner}/{repo_name}', 'main']
    if reset_head == "HARD":
        push_command.append('--force')
    
    subprocess.run(push_command, cwd=repo_dir, check=True)

def update_repo(config_path):
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)

    github_token = os.getenv('GITHUB_TOKEN')
    if not github_token:
        raise ValueError("GitHub token is not set in environment variables.")

    repo_url = config['repo_url']
    clone_dir = config['clone_dir']
    file_path = os.path.join(clone_dir, config['file_path'])
    repo_owner = config['repo_owner']
    repo_name = config['repo_name']
    new_content = config['new_content']
    commit_message = config['commit_message']
    user_name = config['user_name']
    user_email = config['user_email']
    reset_head = config.get('reset_head', None)

    # Clone the repository
    clone_repo(repo_url, clone_dir, github_token, user_name, repo_owner, repo_name)
    
    # Add, commit, and push the change
    git_add_commit_push(file_path, commit_message, clone_dir, github_token, user_name, user_email, repo_owner, repo_name, reset_head)


# Example usage: (uncomment to use directly or import in another script)
# if __name__ == '__main__':
#     update_repo('config.yaml')