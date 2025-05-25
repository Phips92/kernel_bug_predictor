import pandas as pd
import sys
import os
import csv
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from extract.git_feature_extractor import GitFeatureExtractor

if len(sys.argv) != 3:
    print("Usage: python export_ortho_data.py <path_to_git_repo> <output_csv>")
    sys.exit(1)

repo_path = sys.argv[1]
output_csv = sys.argv[2]

extractor = GitFeatureExtractor(repo_path)

fixed_hashes = extractor.find_fixed_commits()
bug_tool_map = extractor.find_fixed_commits_with_tool_indication()



commits = list(extractor.get_commits())
print(f"Extracting features from {len(commits)} commits (with bug/tool labeling)...")

with open(output_csv, mode="w", newline="") as csvfile:
    writer = None

    for commit in commits:
        features = extractor.get_full_feature_vector(
            commit,
            fixed_hashes=fixed_hashes,
            bug_tool_map=bug_tool_map
        )

        row = {
            "commit_hash": features["commit_hash"],
            "label": features["label"],
            "tool_found": features["tool_found"]
        }


        if writer is None:
            writer = csv.DictWriter(csvfile, fieldnames=row.keys())
            writer.writeheader()

        writer.writerow(row)

print(f"Export complete: {output_csv}")
