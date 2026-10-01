from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
import joblib
import shutil

from file_reader import extract_text


app = Flask(__name__)


# ------------------------------------------------
# FOLDERS
# ------------------------------------------------

UPLOAD_FOLDER = "uploads"
ORGANIZED_FOLDER = "test_files"


# ------------------------------------------------
# CATEGORIES
# ------------------------------------------------

categories = [
    "Career",
    "Study",
    "Projects",
    "Personal",
    "Videos"
]


# ------------------------------------------------
# CREATE UPLOAD FOLDER
# ------------------------------------------------

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


# ------------------------------------------------
# LOAD AI MODEL
# ------------------------------------------------

model = joblib.load(
    "file_classifier.pkl"
)

vectorizer = joblib.load(
    "file_vectorizer.pkl"
)


# ------------------------------------------------
# HOME PAGE
# ------------------------------------------------

@app.route("/")
def home():

    organized_files = {}

    for category in categories:

        category_path = os.path.join(
            ORGANIZED_FOLDER,
            category
        )

        if os.path.exists(category_path):

            organized_files[category] = os.listdir(
                category_path
            )

        else:

            organized_files[category] = []

    return render_template(
        "index.html",
        organized_files=organized_files
    )


# ------------------------------------------------
# ORGANIZE UPLOADED FILE
# ------------------------------------------------

@app.route(
    "/organize",
    methods=["POST"]
)
def organize_file():

    # Check whether a file was selected
    if "file" not in request.files:

        return jsonify({
            "error": "No file selected"
        }), 400


    file = request.files["file"]


    if file.filename == "":

        return jsonify({
            "error": "No file selected"
        }), 400


    # ------------------------------------------------
    # MAKE FILENAME SAFE
    # ------------------------------------------------

    filename = secure_filename(
        file.filename
    )


    if not filename:

        return jsonify({
            "error": "Invalid filename"
        }), 400


    filename_lower = filename.lower()


    # ------------------------------------------------
    # SAVE FILE TEMPORARILY
    # ------------------------------------------------

    upload_path = os.path.join(
        UPLOAD_FOLDER,
        filename
    )

    file.save(
        upload_path
    )


    # ------------------------------------------------
    # KEYWORDS
    # ------------------------------------------------

    career_keywords = [
        "resume",
        "cv",
        "curriculum",
        "job",
        "career",
        "internship",
        "application",
        "employment",
        "cover",
        "interview",
        "professional",
        "linkedin"
    ]


    study_keywords = [
        "notes",
        "study",
        "assignment",
        "homework",
        "exam",
        "lecture",
        "class",
        "college notes",
        "university",
        "learning"
    ]


    project_keywords = [
        "project",
        "documentation",
        "project report",
        "final project",
        "presentation",
        "source code"
    ]


    personal_keywords = [
        "personal",
        "family",
        "birthday",
        "vacation",
        "travel",
        "diary",
        "shopping"
    ]


    video_keywords = [
        "video",
        "movie",
        "recording",
        "tutorial video",
        "birthday video",
        "music video"
    ]


    # ------------------------------------------------
    # DEFAULT VALUES
    # ------------------------------------------------

    prediction = None
    confidence = 0.0


    # ------------------------------------------------
    # HIGH-CONFIDENCE KEYWORD DETECTION
    # ------------------------------------------------

    if any(
        keyword in filename_lower
        for keyword in career_keywords
    ):

        prediction = "Career"
        confidence = 0.99


    elif any(
        keyword in filename_lower
        for keyword in study_keywords
    ):

        prediction = "Study"
        confidence = 0.95


    elif any(
        keyword in filename_lower
        for keyword in project_keywords
    ):

        prediction = "Projects"
        confidence = 0.95


    elif any(
        keyword in filename_lower
        for keyword in personal_keywords
    ):

        prediction = "Personal"
        confidence = 0.95


    elif any(
        keyword in filename_lower
        for keyword in video_keywords
    ):

        prediction = "Videos"
        confidence = 0.95


    # ------------------------------------------------
    # AI MODEL FALLBACK
    # ------------------------------------------------

    else:

        features = vectorizer.transform(
            [filename]
        )

        prediction = model.predict(
            features
        )[0]

        probabilities = model.predict_proba(
            features
        )[0]

        confidence = max(
            probabilities
        )


    # ------------------------------------------------
    # CONFIDENCE CHECK
    # ------------------------------------------------

    if confidence < 0.00:

        if os.path.exists(upload_path):

            os.remove(
                upload_path
            )

        return jsonify({

            "filename": filename,

            "category": prediction,

            "confidence": round(
                confidence * 100,
                2
            ),

            "status": "Skipped",

            "message":
                "AI confidence is too low. "
                "File was not moved."

        })


    # ------------------------------------------------
    # CREATE DESTINATION FOLDER
    # ------------------------------------------------

    destination_folder = os.path.join(
        ORGANIZED_FOLDER,
        prediction
    )


    os.makedirs(
        destination_folder,
        exist_ok=True
    )


    # ------------------------------------------------
    # FINAL DESTINATION
    # ------------------------------------------------

    destination = os.path.join(
        destination_folder,
        filename
    )


    # Replace existing file with same name
    if os.path.exists(destination):

        os.remove(
            destination
        )


    # ------------------------------------------------
    # MOVE FILE
    # ------------------------------------------------

    shutil.move(
        upload_path,
        destination
    )


    # ------------------------------------------------
    # EXTRACT FILE CONTENT
    # ------------------------------------------------

    content = extract_text(
        destination
    )


    # ------------------------------------------------
    # SEND RESULT TO WEBSITE
    # ------------------------------------------------

    return jsonify({

        "filename": filename,

        "category": prediction,

        "confidence": round(
            confidence * 100,
            2
        ),

        "status": "Organized",

        "message":
            f"File moved to {prediction} folder.",

        "content": content

    })


# ------------------------------------------------
# START FLASK SERVER
# ------------------------------------------------

if __name__ == "__main__":

    app.run(
        debug=True
    )