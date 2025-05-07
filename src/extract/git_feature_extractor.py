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

    def is_informative_commit(self, commit: git.Commit) -> bool:
        """
        Determines whether a commit is useful for ML feature extraction.
        Excludes merge commits and commits without line changes.
    
        Args:
            commit (git.Commit): Git commit to check.
    
        Returns:
            bool: True if commit is suitable for feature extraction.
        """
        if len(commit.parents) != 1:
            return False
    
        stats = commit.stats.total
        if stats.get("lines", 0) == 0:
            return False

        return True

    def get_commits(self, revision_range: str = "v4.0...v5.19") -> Iterator[git.Commit]:
        """
        Retrieve all commits (no merges) in a given revision range.

        Args:
            revision_range (str): Git revision range (e.g. "v4.0...v5.19").

        Returns:
            Iterator over git.Commit objects.
        """
        return (commit for commit in self.repo.iter_commits(revision_range) if self.is_informative_commit(commit))

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

    def extract_commit_features(self, commit: git.Commit) -> dict:
        """
        Extracts a complete feature set from a single commit, including metadata and message analysis.

        Args:
            commit (git.Commit): A GitPython commit object.

        Returns:
            dict: Dictionary of combined commit features.
        """
        # Basic metadata
        features = self.extract_commit_metadata(commit)

        # Message signature features
        message_signatures = self.analyze_commit_message(commit.message)

        # Merge dictionaries
        features.update(message_signatures)

        return features











