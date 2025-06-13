import sys
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from extract.git_feature_extractor import GitFeatureExtractor

if len(sys.argv) != 2:
    print("Usage: python plot_bug_lifetime.py <linux-repo-path>")
    sys.exit(1)

repo_path = sys.argv[1]
extractor = GitFeatureExtractor(repo_path)

lifetimes = extractor.extract_bug_lifetimes("v2.6.12...v6.14")  

df = pd.DataFrame(lifetimes, columns=["bug_lifetime_days"])
#df.to_csv("Buglifetime")


# Plot
sns.set(style="whitegrid")
plt.figure(figsize=(12, 6))
sns.histplot(df["bug_lifetime_days"], bins=250, kde=False)
plt.yscale("log")
plt.xlabel("Bug Lifetime (days)")
plt.ylabel("Bugs Count")
plt.title("Distribution of Bug Lifetime(via Fixes-Tags)")
plt.tight_layout()
plt.show()

