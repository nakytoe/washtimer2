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
    
    @staticmethod
    def get_github_token():
        github_token = os.getenv('GITHUB_TOKEN')
        if not github_token:
            raise ValueError("GitHub token is not set in environment variables.")
        return github_token
    
    def get_clone_dir(self):
        return self.clone_dir
    
    def __oauth_url(self):
        return self.repo_url.replace('https://', f'https://{self.user_name}:{self.get_github_token()}@')

    def clone(self):
        subprocess.run(['git', 'clone', self.__oauth_url(), self.clone_dir], check=True)
        return self

    def reset_head_hard(self):
        if self.reset_head == 'HARD':
            subprocess.run(['git', 'reset', '--hard', 'HEAD~1'], cwd=self.clone_dir, check=True)
        return self

    def add(self, file_path):
        subprocess.run(['git', 'add', file_path], cwd=self.clone_dir, check=True)
        return self

    def commit(self, commit_message = None):
        if commit_message is None:
            commit_message = self.commit_message
        subprocess.run(['git', '-c', f'user.name={self.user_name}', '-c', f'user.email={self.user_email}', 'commit', '-m', commit_message], cwd=self.clone_dir, check=True)
        return self
    
    def push(self):
        push_command = ['git', 'push', self.__oauth_url(), 'main']
        if self.reset_head == "HARD":
            push_command.append('--force')
    
        subprocess.run(push_command, cwd=self.clone_dir, check=True)
        return self
    
    def remove_clone(self):
        subprocess.run(['rm', '-r', self.clone_dir])
        return self


