import os
import sys
import shutil
from datetime import datetime

def backup_files(source_dir, dest_dir):
    # Check if source and destination directories exist
    if not os.path.isdir(source_dir):
        print(f"Source directory does not exist: {source_dir}")
        return

    if not os.path.isdir(dest_dir):
        print(f"Destination directory does not exist: {dest_dir}")
        return

    print(f"Starting backup from:\n  Source: {source_dir}\n  Destination: {dest_dir}\n")

    # Iterate through all files in the source directory
    for filename in os.listdir(source_dir):
        src_file = os.path.join(source_dir, filename)

        # Skip directories; only copy files
        if not os.path.isfile(src_file):
            continue

        dest_file = os.path.join(dest_dir, filename)

        # If file exists in destination, add timestamp to filename
        if os.path.exists(dest_file):
            base, ext = os.path.splitext(filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            new_filename = f"{base}_{timestamp}{ext}"
            dest_file = os.path.join(dest_dir, new_filename)
            print(f"File exists. Renaming to avoid conflict: {new_filename}")

        # Copy file
        try:
            shutil.copy2(src_file, dest_file)
            print(f"Copied: {filename}")
        except Exception as e:
            print(f"Failed to copy {filename}: {e}")

    print("\nBackup complete.")

if __name__ == "__main__":
    # Check for correct number of command-line arguments
    if len(sys.argv) != 3:
        print("Usage: python backup.py /path/to/source /path/to/destination")
        sys.exit(1)

    source_directory = sys.argv[1]
    destination_directory = sys.argv[2]

    backup_files(source_directory, destination_directory)
