# Kernel Bug Predictor

A machine learning project to help maintainers identify potentially buggy commits in the Linux kernel.  
It analyzes commit metadata from Git (e.g. diffs, timestamps, message patterns) and uses these features to train a model that predicts whether a commit is likely to contain a bug.

## Project Goals

- Extract structured features from Linux kernel Git history
- Train and evaluate ML models to identify bug-prone commits
- Build an object-oriented and maintainable codebase

## Structure

- `extract/`: Git commit feature extraction
- `scripts/`: Training, evaluation, prediction scripts
- `data/`: Intermediate and final datasets
- `models/`: Trained ML models

