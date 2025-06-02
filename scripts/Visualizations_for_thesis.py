import subprocess
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# list of kernel tags 
kernel_tags = [
    "v4.0", "v4.1", "v4.2", "v4.3", "v4.4",
    "v4.5", "v4.6", "v4.7", "v4.8", "v4.9",
    "v4.10", "v4.11", "v4.12", "v4.13", "v4.14",
    "v4.15", "v4.16", "v4.17", "v4.18", "v4.19", "v4.20",
    "v5.0", "v5.1", "v5.2", "v5.3", "v5.4",
    "v5.5", "v5.6", "v5.7", "v5.8", "v5.9",
    "v5.10", "v5.11", "v5.12", "v5.13", "v5.14",
    "v5.15", "v5.16", "v5.17", "v5.18", "v5.19",
    "v6.0", "v6.1", "v6.2", "v6.3", "v6.4", "v6.5", "v6.6", "v6.7"
]

repo_path = "/home/philipp/Desktop/Data_Science_Studium/Bachelor_Thesis/Development/kernel_bug_redictor/linux-stable"

# commits count
data = []
for i in range(len(kernel_tags) - 1):
    tag1 = kernel_tags[i]
    tag2 = kernel_tags[i + 1]

    cmd = ["git", "-C", repo_path, "rev-list", "--count", f"{tag1}..{tag2}"]
    count = int(subprocess.check_output(cmd).decode().strip())

    data.append({"version": f"{tag2}", "patches": count})

df = pd.DataFrame(data)

sns.set(style="whitegrid")
plt.figure(figsize=(12, 6))
plt.fill_between(df["version"], df["patches"], color="skyblue", alpha=0.6)
plt.plot(df["version"], df["patches"], color="steelblue", linewidth=2)

plt.title("Linux Kernel Patch Volume per Release (v4.0 – v6.7)")
plt.xlabel("")
plt.ylabel("Patch Count")
plt.xticks([], []) 


plt.text(
    x=len(df) / 2,
    y=-max(df["patches"]) * 0.08,
    s="Kernel releases from v4.0 to v6.7 (~2015–2024)",
    ha="center",
    fontsize=10
)

plt.grid(axis="y", linestyle="--", alpha=0.5)
plt.tight_layout()
plt.show()
