import os

import pytesseract
from PIL import Image

from pypdf import PdfReader
from docx import Document


# ------------------------------------------------
# TESSERACT OCR LOCATION
# ------------------------------------------------

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


# ------------------------------------------------
# EXTRACT TEXT FROM FILE
# ------------------------------------------------

def extract_text(file_path):

    extension = os.path.splitext(file_path)[1].lower()


    # ------------------------------------------------
    # PDF
    # ------------------------------------------------

    if extension == ".pdf":

        reader = PdfReader(file_path)

        text = ""

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        return text


    # ------------------------------------------------
    # DOCX
    # ------------------------------------------------

    elif extension == ".docx":

        document = Document(file_path)

        text = ""

        for paragraph in document.paragraphs:

            text += paragraph.text + "\n"

        return text


    # ------------------------------------------------
    # TXT
    # ------------------------------------------------

    elif extension == ".txt":

        with open(
            file_path,
            "r",
            encoding="utf-8",
            errors="ignore"
        ) as file:

            return file.read()


    # ------------------------------------------------
    # IMAGE OCR
    # ------------------------------------------------

    elif extension in [
        ".jpg",
        ".jpeg",
        ".png",
        ".bmp",
        ".webp"
    ]:

        image = Image.open(file_path)

        text = pytesseract.image_to_string(image)

        return text


    # ------------------------------------------------
    # UNSUPPORTED FILE
    # ------------------------------------------------

    else:

        return (
            "Content extraction is not supported "
            "for this file type."
        )