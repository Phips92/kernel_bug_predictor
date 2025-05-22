import git
from typing import Iterator
import time
import re
import io
from unidiff import PatchSet


# Used to assign complexity scores to top-level directories
DIR_COMPLEXITY = {
    "kernel": 9, "mm": 9, "arch": 9, "include": 6.25, "net": 6.25, "fs": 6.25,
    "firmware": 4, "block": 4, "crypto": 4, "security": 4, "virt": 4,
    "certs": 2.25, "init": 2.25, "lib": 2.25, "sound": 2.25, "ipc": 2.25,
    "drivers": 2.25, "Documentation": 2.25, "samples": 2.25,
    "tools": 1, "scripts": 1, "usr": 1, "Kbuild": 1, "Kconfig": 1,
    "COPYING": 0, "CREDITS": 0, "Makefile": 1, "MAINTAINERS": 0,
    ".mailmap": 0, "README": 0, ".gitignore": 0, ".gitattributes": 0,
    ".get_maintainer.ignore": 0, "REPORTING-BUGS": 0, ".cocciconfig": 0,
    "README.md": 0, "null": 0
}

# Scoring for file-level change type
FILE_IMPACT = {
    "new": 5,
    "modified": 2,
    "deleted": 0,
    "huh": 0  # fallback
}



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

        try:
            diff_text = self.repo.git.diff(commit.parents[0].hexsha, commit.hexsha)
            patch = PatchSet(io.StringIO(diff_text))

            added = sum(hunk.added for f in patch for hunk in f)
            removed = sum(hunk.removed for f in patch for hunk in f)
            if (added + removed) < 5:
                return False

        except Exception as e:
            print(f"Patch parse error for {commit.hexsha[:12]}: {e}")
            return False




        return True

    def get_commits(self, revision_range: str = "v5.18...v6.1") -> Iterator[git.Commit]:
        """
        Retrieve all commits (no merges) in a given revision range.

        Args:
            revision_range (str): Git revision range (e.g. "v4.0...v5.19").

        Returns:
            Iterator over git.Commit objects.
        """
        return (commit for commit in self.repo.iter_commits(revision_range, no_merges=True) if self.is_informative_commit(commit))

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

    def extract_diff_features(self, commit: git.Commit) -> dict:

        """
        Extracts patch-based features from a commit: number of changed files,
        overall impact score, and directory complexity.

        Args:
            commit (git.Commit): A GitPython commit object.

        Returns:
            dict: Dictionary with patch-related features.
        """
        diff_text = self.repo.git.diff(commit.parents[0].hexsha, commit.hexsha)
        patch = PatchSet(io.StringIO(diff_text))

        file_impact_total = 0
        dir_complexity_total = 0
        file_count = 0

        for file in patch:
            file_count += 1

            # Determine file change type
            if file.is_added_file:
                change_type = "new"
            elif file.is_removed_file:
                change_type = "deleted"
            elif file.is_modified_file:
                change_type = "modified"
            else:
                change_type = "huh"

            file_impact_total += FILE_IMPACT.get(change_type, 0)

            # Determine top-level directory
            filepath = file.path
            top_dir = filepath.split("/")[0] if "/" in filepath else filepath
            dir_complexity_total += DIR_COMPLEXITY.get(top_dir, 0)

        return {
            "files_changed": file_count,
            "file_impact": file_impact_total,
            "dir_complexity": dir_complexity_total
        }


    def get_full_feature_vector(self, commit: git.Commit, include_message: bool = False) -> dict:
        """
        Combines metadata, message-based and diff-based features into a full commit feature vector, 
        including a binary bug-fix label. Optionally includes the raw commit message.

        Args:
            commit (git.Commit): A GitPython commit object.
            include_message (bool): Whether to include the raw commit message.

        Returns:
            dict: Combined feature dictionary.
        """
        features = {}
        features.update(self.extract_commit_metadata(commit))
        features.update(self.analyze_commit_message(commit.message))
        features.update(self.extract_diff_features(commit))
        features["label"] = self.label_commit(commit)

        if include_message:
            features["message"] = commit.message.strip()

        return features


    def label_commit(self, commit: git.Commit) -> int:
        """
        Heuristically label a commit as a bug-fix based on its message content.

        Returns:
            int: 1 if likely a bug-fix commit, else 0
        """
        message = commit.message.lower()

        # Common bug-fix indicators
        patterns = [
            r"\bfix(e[ds])?\b",           # fix, fixed, fixes
            r"\bbug(s)?\b",               # bug, bugs
            r"\bregression(s)?\b",        # regression, regressions
            r"\bcorrect(ed|ion)?\b",      # correct, corrected, correction
            r"\bresolve(d)?\b",           # resolve, resolved
            r"cc:.*stable@",              # stable backport indication
            r"\breported-by\b",
            r"\bfixes:\b"
        ]

        for pattern in patterns:
            if re.search(pattern, message):
                return 1

        return 0












