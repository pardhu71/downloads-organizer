import os
import shutil
import time
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Downloads folder path
downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")

# Desktop folder path
desktop_folder = os.path.join(os.path.expanduser("~"), "Desktop")

# File categories
file_types = {
    "PDFs": [".pdf"],
    "Images": [".jpg", ".jpeg", ".png", ".gif"],
    "Word_Files": [".docx", ".doc"],
    "Videos": [".mp4", ".mkv", ".avi"],
    "Python_Files": [".py"],
}

class DownloadHandler(FileSystemEventHandler):

    def on_modified(self, event):

        # Ignore folders
        if event.is_directory:
            return

        file_path = event.src_path
        file_name = os.path.basename(file_path)

        # Ignore temporary browser files
        if file_name.endswith(".tmp") or file_name.endswith(".crdownload"):
            return

        # Check file exists
        if not os.path.exists(file_path):
            return

        # Wait for download completion
        time.sleep(2)

        # Skip if browser still using file
        if not os.access(file_path, os.W_OK):
            return

        # Create today's date folder
        today_date = datetime.now().strftime("%Y-%m-%d")

        today_folder = os.path.join(desktop_folder, today_date)

        os.makedirs(today_folder, exist_ok=True)

        # Create category folders
        for folder_name in file_types.keys():
            os.makedirs(os.path.join(today_folder, folder_name), exist_ok=True)

        # Create Others folder
        others_folder = os.path.join(today_folder, "Others")
        os.makedirs(others_folder, exist_ok=True)

        moved = False

        # Move based on extension
        for folder_name, extensions in file_types.items():

            if file_name.lower().endswith(tuple(extensions)):

                destination = os.path.join(today_folder, folder_name, file_name)

                # Skip if already moved
                if os.path.exists(destination):
                    return

                try:
                    shutil.move(file_path, destination)
                    print(f"Moved: {file_name} → {folder_name}")

                except Exception as e:
                    print(f"Error moving {file_name}: {e}")

                moved = True
                break

        # Move unknown files
        if not moved:

            destination = os.path.join(others_folder, file_name)

            if os.path.exists(destination):
                return

            try:
                shutil.move(file_path, destination)
                print(f"Moved: {file_name} → Others")

            except Exception as e:
                print(f"Error moving {file_name}: {e}")

# Start watching Downloads folder
event_handler = DownloadHandler()

observer = Observer()
observer.schedule(event_handler, downloads_folder, recursive=False)

observer.start()

print("Watching Downloads folder...")

try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    observer.stop()

observer.join()