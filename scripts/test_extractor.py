import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from extract.git_feature_extractor import GitFeatureExtractor
from pprint import pprint

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


print("\n=== Test: analyze_commit_message ===")
test_message = """
This patch improves something.

Signed-off-by: Phips Developer <phips@dev.com>
Reviewed-by: Senior Dev <senior@dev.com>
Reviewed-by: Bob <bob@kernel.org>
Link: https://kernel.org/r/patch-v1
"""

msg_counts = extractor.analyze_commit_message(test_message)
for key, val in msg_counts.items():
    print(f"{key}: {val}")

print("\n=== Raw commit message ===")
print(repr(commits[0].message))

print("\n=== Test: extract_commit_features (first real commit) ===")
if commits:
    full_features = extractor.extract_commit_features(commits[0])
    for key, value in full_features.items():
        print(f"{key}: {value}")
else:
    print("No commits found to test.")

print("\n=== Test: get_full_feature_vector (first real commit) ===")
if commits:
    full_vector = extractor.get_full_feature_vector(commits[0])
    pprint(full_vector)
else:
    print("No commits found to test.")


