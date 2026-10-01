# AI Folder Organization

## Project Overview

AI Folder Organization is a Python-based project that automatically organizes files into different categories. It uses machine learning to predict the category of a file based on its filename.

## Categories

The project organizes files into:

- Career
- Study
- Projects
- Personal
- Videos

## Technologies Used

- Python
- Scikit-learn
- TF-IDF Vectorization
- Logistic Regression
- Joblib
- VS Code

## How It Works

1. The user places files inside the `test_files` folder.
2. The AI model analyzes the filename.
3. TF-IDF converts the filename into numerical features.
4. Logistic Regression predicts the file category.
5. The confidence score is checked.
6. Files with sufficient confidence are moved to the predicted category.
7. Uncertain files are skipped instead of being moved incorrectly.

## Project Files

- `organizer.py` - Basic extension-based file organizer
- `train_model.py` - Trains the machine learning model
- `ai_organizer.py` - Uses the trained AI model to organize files
- `file_classifier.pkl` - Saved trained classification model
- `file_vectorizer.pkl` - Saved TF-IDF vectorizer
- `test_files` - Folder containing files to organize

## How to Run

### Train the AI model

```bash
uv run python train_model.py
