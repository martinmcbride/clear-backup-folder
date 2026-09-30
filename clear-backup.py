from pathlib import Path
from datetime import datetime, timedelta

# Folder to scan
FOLDER = Path(r"/media/martin/Backup/backup")

# Days of the month to preserve
KEEP_DAYS = {1, 7, 14, 21, 28}

# Set to False to actually delete files
DRY_RUN = False

def delete_old_files(folder):
    # Approximate "2 months" as 60 days.
    cutoff = datetime.now() - timedelta(days=60)
    files = sorted(
        folder.iterdir(),
        key=lambda f: f.stat().st_mtime,
        reverse=True
    )

    for file in files:

        if not file.is_file():
            continue

        # Get last modification time
        modified = datetime.fromtimestamp(file.stat().st_mtime)

        # Ignore files newer than 2 months
        if modified >= cutoff:
            print(f"KEEP (RECENT):   {file} ({modified:%Y-%m-%d})")
            continue

        # Keep files modified on the specified days
        if modified.day in KEEP_DAYS:
            print(f"KEEP (WEEKLY):   {file} ({modified:%Y-%m-%d})")
            continue

        print(f"DELETE: {file} ({modified:%Y-%m-%d})")

        if not DRY_RUN:
            try:
                file.unlink()
            except OSError as e:
                print(f"ERROR: Could not delete {file}: {e}")


if __name__ == "__main__":
    delete_old_files(FOLDER)
