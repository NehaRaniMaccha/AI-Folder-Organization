from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib

# Training filenames
file_names = [
    # Career
    "resume",
    "cv",
    "job application",
    "cover letter",
    "internship application",
    "career plan",
    "interview questions",
    "employment offer",
    "job profile",
    "professional resume",

    # More resume examples
    "accountant resume",
    "professional accountant resume",
    "accounting resume",
    "fresher resume",
    "student resume",
    "BTech resume",
    "AI student resume",
    "career resume",
    "resume document",
    "resume pdf",
    "my resume",
    "updated resume",
    "final resume",
    "black and white resume",
    "minimalist accountant resume",

    # Study
    "python notes",
    "machine learning notes",
    "college notes",
    "exam preparation",
    "study material",
    "lecture notes",
    "assignment",
    "homework",
    "programming notes",
    "math notes",
    "class notes",
    "university notes",

    # Projects
    "project report",
    "college project",
    "ai project",
    "machine learning project",
    "software project",
    "project documentation",
    "final project",
    "folder organization project",
    "project presentation",
    "project work",

    # Personal
    "family photo",
    "vacation photo",
    "birthday photo",
    "personal notes",
    "personal diary",
    "shopping list",
    "family documents",
    "travel memories",
    "personal letter",
    "family picture",

    # Videos
    "movie",
    "birthday video",
    "lecture video",
    "family video",
    "tutorial video",
    "vacation video",
    "recording",
    "college video",
    "travel video",
    "music video"
]

categories = (
    ["Career"] * 25 +
    ["Study"] * 12 +
    ["Projects"] * 10 +
    ["Personal"] * 10 +
    ["Videos"] * 10
)

# Convert filenames into numerical features
vectorizer = TfidfVectorizer(
    ngram_range=(1, 2),
    lowercase=True
)

X = vectorizer.fit_transform(file_names)

# Train AI model
model = LogisticRegression(
    max_iter=1000,
    random_state=42
)

model.fit(X, categories)

# Save trained model
joblib.dump(model, "file_classifier.pkl")
joblib.dump(vectorizer, "file_vectorizer.pkl")

print("AI model trained successfully!")
print("Training examples:", len(file_names))