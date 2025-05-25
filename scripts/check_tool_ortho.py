import pandas as pd
import random
import re
import sys

if len(sys.argv) != 2:
    print("Usage: python check_tool_ortho.py <predictions_and_tools_csv>")
    sys.exit(1)

pred_path = sys.argv[1]
df = pd.read_csv(pred_path)

if "tool_found" not in df.columns:
    print("ERROR: 'tool_found' column required in CSV.")
    sys.exit(1)

# parameter
NUM_SAMPLES = 400
THRESHOLD_HIGH = 0.5
THRESHOLD_LOW = 0.25

# high & low grouping
high = df[df["bugfix_probability"] >= THRESHOLD_HIGH].sample(n=NUM_SAMPLES)
low = df[df["bugfix_probability"] < THRESHOLD_LOW].sample(n=NUM_SAMPLES)

def count_tool_flags(df):
    return df["tool_found"].sum()

high_tool_mentions = count_tool_flags(high)
low_tool_mentions = count_tool_flags(low)

print("=== Tool Mention Analysis ===")
print(f"In HIGH group (model flagged as bugfix):")
print(f"{high_tool_mentions} of {NUM_SAMPLES} messages mention known tools.")

print(f"\nIn LOW group (model did NOT flag as bugfix):")
print(f"{low_tool_mentions} of {NUM_SAMPLES} messages mention known tools.")
