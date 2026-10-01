import os
import shutil

folder_path = "test_files"

# Create folders
folders = ["Images", "Documents", "Videos", "Others"]

for folder in folders:
    os.makedirs(
        os.path.join(folder_path, folder),
        exist_ok=True
    )

# File extensions
image_extensions = [".jpg", ".jpeg", ".png", ".gif"]
document_extensions = [".pdf", ".docx", ".txt", ".xlsx"]
video_extensions = [".mp4", ".avi", ".mkv"]

# Organize files
for file in os.listdir(folder_path):

    file_path = os.path.join(folder_path, file)

    # Skip folders
    if os.path.isdir(file_path):
        continue

    extension = os.path.splitext(file)[1].lower()

    if extension in image_extensions:
        destination = "Images"

    elif extension in document_extensions:
        destination = "Documents"

    elif extension in video_extensions:
        destination = "Videos"

    else:
        destination = "Others"

    # Move the file
    shutil.move(
        file_path,
        os.path.join(folder_path, destination, file)
    )

    print(file, "->", destination)

print("Files organized successfully!")