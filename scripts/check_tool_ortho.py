import pandas as pd
import random
import re
import sys

if len(sys.argv) != 2:
    print("Usage: python check_tool_mentions.py <predictions_and_message_csv>")
    sys.exit(1)

pred_path = sys.argv[1]
df = pd.read_csv(pred_path)

if "message" not in df.columns:
    print("ERROR: 'message' column required in CSV.")
    sys.exit(1)

# toolnames
tools = [
    "sparse", "smatch", "clang", "coverity", "checkpatch", "coccinelle",
    "gcc", "cppcheck", "valgrind", "kasan", "kcsan", "ubsan", "lockdep", "syzbot", "syzkaller"
]
tool_pattern = re.compile(r"\b(" + "|".join(tools) + r")\b", flags=re.IGNORECASE)

# parameter
NUM_SAMPLES = 100
THRESHOLD_HIGH = 0.9
THRESHOLD_LOW = 0.5

# high & low grouping
high = df[df["bugfix_probability"] >= THRESHOLD_HIGH].sample(n=NUM_SAMPLES)
low = df[df["bugfix_probability"] < THRESHOLD_LOW].sample(n=NUM_SAMPLES)

def count_tool_mentions(df):
    return sum(bool(tool_pattern.search(msg)) for msg in df["message"].fillna(""))

high_tool_mentions = count_tool_mentions(high)
low_tool_mentions = count_tool_mentions(low)

print("=== Tool Mention Analysis ===")
print(f"In HIGH group (model flagged as bugfix):")
print(f"{high_tool_mentions} of {NUM_SAMPLES} messages mention known tools.")

print(f"\nIn LOW group (model did NOT flag as bugfix):")
print(f"{low_tool_mentions} of {NUM_SAMPLES} messages mention known tools.")
