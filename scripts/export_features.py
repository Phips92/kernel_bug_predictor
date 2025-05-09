import sys
import os
import csv

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from extract.git_feature_extractor import GitFeatureExtractor


if len(sys.argv) != 3:
    print("Usage: python export_features.py <path_to_git_repo> <output_csv>")
    sys.exit(1)

repo_path = sys.argv[1]
output_file = sys.argv[2]

extractor = GitFeatureExtractor(repo_path)
commits = list(extractor.get_commits())
print(f"Extracting features from {len(commits)} commits...")

with open(output_file, mode="w", newline="") as csvfile:
    writer = None

    for commit in commits:
        features = extractor.get_full_feature_vector(commit)

        # Write headers once
        if writer is None:
            writer = csv.DictWriter(csvfile, fieldnames=features.keys())
            writer.writeheader()

        writer.writerow(features)

print(f"Feature export completed: {output_file}")

