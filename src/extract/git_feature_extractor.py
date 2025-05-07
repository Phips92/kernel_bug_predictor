import git
from typing import Iterator
import time


class GitFeatureExtractor:
    """
    This class provides methods to extract metadata and features from Git commits.
    """

    def __init__(self, repo_path: str):
        """
        Initialize the Git repository for feature extraction.

        Args:
            repo_path (str): Path to the local Git repository.
        """
        self.repo_path = repo_path
        self.repo = git.Repo(repo_path)

    def get_commits(self, revision_range: str = "v4.0...v5.19") -> Iterator[git.Commit]:
        """
        Retrieve all commits in a given revision range.

        Args:
            revision_range (str): Git revision range (e.g. "v4.0...v5.19").

        Returns:
            Iterator over git.Commit objects.
        """
        return self.repo.iter_commits(revision_range)

    def extract_commit_metadata(self, commit: git.Commit) -> dict:
        """
        Extracts basic metadata from a single commit.

        Args:
            commit (git.Commit): A GitPython commit object.

        Returns:
            dict: Dictionary with commit metadata.
        """
        author_name = commit.author.name
        author_date = int(time.mktime(time.gmtime(commit.authored_date)))
        committer_name = commit.committer.name
        commit_date = int(time.mktime(time.gmtime(commit.committed_date)))
        commit_delay = commit_date - author_date
        message_length = len(commit.message.strip())

        return {
            "commit_hash": commit.hexsha[:12],
            "author": author_name,
            "author_date": author_date,
            "committer": committer_name,
            "commit_date": commit_date,
            "commit_delay": commit_delay,
            "message_length": message_length
        }
