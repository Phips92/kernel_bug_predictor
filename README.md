# Kernel Bug Predictor

This project provides a full pipeline to **predict bugfix commits in the Linux kernel** using machine learning. It includes tooling for **feature extraction from Git history**, **model training and evaluation**, as well as **visual analysis** and **interpretability**.

The goal is to help Developers identify buggy commits based on commit metadata..

## Project Goals

- Extract structured features from Linux kernel Git history
- Train and evaluate ML models to identify bug-prone commits
- Build an object-oriented and maintainable codebase

## Structure

- `src/extract/`: Git commit feature extraction
- `scripts/`: Training, evaluation, prediction, analysis scripts
- `data/`: Intermediate and final datasets
- `models/`: Trained ML models

---

## Scripts Overiew

```text
scripts/
├── export_features.py # Extracts features from Git repository
├── export_ortho_data.py # Adds orthogonal tool indicators to features
├── train_model.py # Trains a model to estimate he probability that a commit is a bugfix
├── predict.py # Applies the trained model to new data
├── evaluate_predictions.py # Analyzes probability distributions and top results
├── evaluate_prediction_quality.py # Generates confusion matrix and classification report
├── visualize_model_evaluation.py # ROC/AUC, model architecture, class-wise histogram
├── shap_analysis.py # SHAP feature importance visualization
├── merge_message_and_predictions.py # Merges commit messages with model predictions
├── merge_predictions_and_labels.py # Joins predictions with true labels
├── compare_predictions_with_labels.py # Focus on perfect-score predictions
├── check_tool_ortho.py # Verifies correlation between model score and tool mention
├── plot_bug_lifetime.py # Shows distribution of bug lifetimes (days)
├── analyze_data.py # Exploratory data analysis and statistics
├── Visualizations_for_thesis.py # Kernel release trends and patch volume
├── test_extractor.py # Verifies feature extractor functionality
scr/
└── extract/git_feature_extractor.py # Core feature extraction class

---

## Core Idea

Identify bugs by:
- Scanning for `"Fixes:"` tags in commit messages
- Extracting commit metadata (author, delay, etc.)
- Analyzing message structure (Signed-off-by, Reviewed-by, etc.)
- Scoring patch impact (file/directory complexity)
- Applying deep learning to predict bug probability

---

## Requirements

Install required Python libraries:

```bash
pip install -r requirements.txt

Dependencies include:

    tensorflow, scikit-learn, joblib

    pandas, numpy, matplotlib, seaborn

    shap, unidiff, GitPython

Dataset Creation

You need a local clone of the Linux kernel repository.

Extract full feature vectors:

python export_features.py <path_to_linux_repo> features.csv

Or include tool-indication for bug fixes:

python export_ortho_data.py <path_to_linux_repo> features_with_tools.csv

Model Training

Train a neural network classifier:

python train_model.py features.csv

Output:

    Trained model -> models/bugfix_model.keras

    Feature scaler -> models/scaler.pkl

Inference

Apply the trained model:

python predict.py features.csv predictions.csv

Each commit receives a probability bug_probability [0, 1].

Evaluation & Analysis

Classification Report

python evaluate_prediction_quality.py features.csv predictions.csv

Includes:

    Confusion matrix

    Precision/recall/F1

    False negatives

Threshold Inspection

python evaluate_predictions.py predictions.csv

Outputs:

    Summary statistics

    Top 5% threshold

    Histogram of predicted probabilities

Visual Tools

ROC & Architecture

python visualize_model_evaluation.py features.csv

Saves:

    roc_curve.png

    model_architecture.png

    prediction_histogram_by_class.png

SHAP Explanation

python shap_analysis.py features.csv models/bugfix_model.keras models/scaler.pkl

Outputs:

    shap_summary_plot.png (Feature importance)

Bug Lifetime Analysis

python plot_bug_lifetime.py <path_to_linux_repo>

Visualizes days between buggy commit and its fix.

Other Utilities

    merge_message_and_predictions.py: Adds commit message for inspection

    check_tool_ortho.py: Compares tool presence in commits above/below threshold

    compare_predictions_with_labels.py: Focuses on predictions with confidence = 1.0 

    analyze_data.py: Visual overview of dataset stats and correlations

    Visualizations_for_thesis.py: Patch volume across kernel versions

Test the Extractor

python test_extractor.py <path_to_linux_repo>

Prints:

    Commit metadata

    Signature counts

    Patch-based features

    Full feature vector for a single commit

Example Workflow

# Step 1: Extract data
python export_features.py ./linux-stable features.csv

# Step 2: Train model
python train_model.py features.csv

# Step 3: Predict
python predict.py features.csv predictions.csv

# Step 4: Evaluate
python evaluate_prediction_quality.py features.csv predictions.csv
python visualize_model_evaluation.py features.csv


## Academic Use

This project was developed as part of a Bachelor thesis in Data Science, focused on applying interpretable machine learning to real-world software engineering data.

---

## License

This project is licensed under the GNU General Public License v3.0

## Author

Philipp (Phips92)

For questions or collaborations, feel free to contact me at [philipp92.mcguire@gmail.com].

