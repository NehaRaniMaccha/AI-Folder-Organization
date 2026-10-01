import os
import shutil
import joblib

folder_path = "test_files"

print("AI Folder Organizer Started")

# Create category folders
folders = ["Career", "Study", "Projects", "Personal", "Videos"]

for folder in folders:
    os.makedirs(os.path.join(folder_path, folder), exist_ok=True)

# Load AI model
model = joblib.load("file_classifier.pkl")
vectorizer = joblib.load("file_vectorizer.pkl")

# Organize files
for file in os.listdir(folder_path):

    file_path = os.path.join(folder_path, file)

    # Skip folders
    if os.path.isdir(file_path):
        continue

    # Convert filename into AI features
    file_features = vectorizer.transform([file])

    # Predict category
    prediction = model.predict(file_features)[0]

    # Get confidence
    probabilities = model.predict_proba(file_features)[0]
    confidence = max(probabilities)

    print(file, "->", prediction,
          "| Confidence:", round(confidence * 100, 2), "%")

    # Move only if confidence is high enough
    if confidence >= 0.60:
        shutil.move(
            file_path,
            os.path.join(folder_path, prediction, file)
        )
        print("Moved successfully!")

    else:
        print("Skipped - AI is not confident enough.")

print("AI file organization completed!")