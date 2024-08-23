from pathlib import Path
import subprocess
import os
import yaml

class RepoUtil():
    """
    Wrapper for simple git repository functions
    """

    def __init__(self, config_path:str):
        with open(Path(config_path), 'r') as file:
            config = yaml.safe_load(file)

        self.repo_url = config['repo_url']
        self.clone_dir = config['clone_dir']
        self.repo_owner = config['repo_owner']
        self.repo_name = config['repo_name']
        self.commit_message = config['commit_message']
        self.user_name = config['user_name']
        self.user_email = config['user_email']
        self.reset_head = config.get('reset_head', None)

        subprocess.run(['git', 'config', 'user.name', self.user_name], cwd=self.repo_dir, check=True)
        subprocess.run(['git', 'config', 'user.email', self.user_email], cwd=self.repo_dir, check=True)
    
    @staticmethod
    def get_github_token():
        github_token = os.getenv('GITHUB_TOKEN')
        if not github_token:
            raise ValueError("GitHub token is not set in environment variables.")
        return github_token

    def clone(self):
        auth_repo_url = self.repo_url.replace('https://', f'https://{self.user_name}:{self.get_github_token()}@')
        subprocess.run(['git', 'clone', auth_repo_url, self.clone_dir], check=True)
        return self

    def reset_head_hard(self):
        if self.reset_head == 'HARD':
            subprocess.run(['git', 'reset', '--hard', 'HEAD~1'], cwd=self.clone_dir, check=True)
        return self

    def add(self, file_path):
        subprocess.run(['git', 'add', file_path], cwd=self.repo_dir, check=True)
        return self

    def commit(self, commit_message = None):
        if commit_message is None:
            commit_message = self.commit_message
        subprocess.run(['git', 'commit', '-m', commit_message], cwd=self.repo_dir, check=True)
        return self
    
    def push(self):
        push_command = ['git', 'push', f'https://{self.user_name}:{self.get_github_token()}@github.com/{self.repo_owner}/{self.repo_name}', 'main']
        if self.reset_head == "HARD":
            push_command.append('--force')
    
        subprocess.run(push_command, cwd=self.repo_dir, check=True)
        return self


