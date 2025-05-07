import git
from typing import Iterator
import time
import re


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

    def analyze_commit_message(self, message: str) -> dict:
        """
        Analyze commit message to count signature tags like 'Signed-off-by', 'Reviewed-by', etc.

        Args:
            message (str): The full commit message text.

        Returns:
            dict: Count of each signature type found in the message.
        """
        patterns = {
            "signed_off": re.compile(r"^Signed-off-by.*", re.IGNORECASE),
            "reviewed_by": re.compile(r"^Reviewed-by.*", re.IGNORECASE),
            "tested_by": re.compile(r"^Tested-by.*", re.IGNORECASE),
            "reported_by": re.compile(r"^Reported-by.*", re.IGNORECASE),
            "acked_by": re.compile(r"^Acked-by.*", re.IGNORECASE),
            "cc": re.compile(r"^CC:.*", re.IGNORECASE),
            "link": re.compile(r"^Link:.*", re.IGNORECASE),
        }

        counts = {key: 0 for key in patterns}

        for line in message.splitlines():
            for key, regex in patterns.items():
                if regex.match(line.strip()):
                    counts[key] += 1

        counts["by_sum"] = sum(counts.values())
        return counts







