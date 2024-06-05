from git import Repo, GitCommandError
import tempfile
import os
import shutil


def clone_repo(link: str, clone_dir: str):
    try:
        if not os.path.exists(clone_dir):
            os.makedirs(clone_dir)
        print(f"Cloning repo from {link} to {clone_dir}")
        repo = Repo.clone_from(link, clone_dir)
        print(f"Repo cloned successfully to {clone_dir}")
        return clone_dir
    except GitCommandError as e:
        print(f"Failed to clone repo: {e}")
        shutil.rmtree(clone_dir)
        raise e
    
    
def cleanup_temp_dir(temp_dir: str):
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)