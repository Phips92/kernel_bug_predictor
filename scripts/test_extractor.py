import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from extract.git_feature_extractor import GitFeatureExtractor


if len(sys.argv) != 2:
    print("Usage: python test_extractor.py <path_to_git_repo>")
    sys.exit(1)

repo_path = sys.argv[1]
extractor = GitFeatureExtractor(repo_path)

commits = list(extractor.get_commits())
print(f"Found {len(commits)} commits.")

if commits:
    metadata = extractor.extract_commit_metadata(commits[0])
    print("Metadata of first commit:")
    for key, value in metadata.items():
        print(f"  {key}: {value}")

