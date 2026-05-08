# Automatic Downloads Organizer

This project automatically organizes downloaded files into folders based on the current date and file type.

## Features
- Watches the Downloads folder in real time
- Creates a new folder on Desktop every day
- Automatically sorts files into:
  - PDFs
  - Images
  - Word_Files
  - Videos
  - Python_Files
  - Others

## Example Folder Structure

Desktop
└── 2026-05-08
    ├── PDFs
    ├── Images
    ├── Word_Files
    ├── Videos
    ├── Python_Files
    └── Others

## Technologies Used
- Python
- watchdog library
- File handling using os and shutil

## How to Run

Install watchdog:

pip install watchdog

Run the script:

python organizer.py
