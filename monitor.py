import subprocess
import os
import threading
from datetime import datetime

# Get comma-separated directories from env var or default
WATCH_DIRS = os.environ.get("WATCH_DIRS", "/watched").split(",")

# Optional
LOG_FILE = os.environ.get("LOG_FILE", "")  # e.g., "/log/output.log"

def log(message):
    timestamped = f"[{datetime.now()}] {message}"
    print(timestamped)
    if LOG_FILE:
        with open(LOG_FILE, "a") as f:
            f.write(timestamped + "\n")

def watch_directory(path):
    path = path.strip()
    if not os.path.exists(path):
        log(f"Directory does not exist: {path}")
        return

    log(f"👀 Monitoring: {path}")

    # Monitor create, delete, modify, move, and attrib (permission) events
    process = subprocess.Popen(
        ["inotifywait", "-m",
         "-e", "create",
         "-e", "delete",
         "-e", "modify",
         "-e", "move",
         "-e", "attrib",  # permission/metadata change
         path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    try:
        for line in process.stdout:
            parts = line.strip().split()
            if len(parts) < 3:
                continue

            directory, events, filename = parts[0], parts[1], ' '.join(parts[2:])

            if "CREATE" in events:
                log(f"Created: {filename} in {directory}")
            elif "DELETE" in events:
                log(f"Deleted: {filename} from {directory}")
            elif "MODIFY" in events:
                log(f"Modified: {filename} in {directory}")
            elif "MOVED_FROM" in events or "MOVED_TO" in events:
                log(f"Moved: {filename} in {directory} ({events})")
            elif "ATTRIB" in events:
                log(f"Permission/metadata changed: {filename} in {directory}")

    except Exception as e:
        log(f"Error watching {path}: {e}")
    finally:
        process.terminate()

def main():
    threads = []
    for dir_path in WATCH_DIRS:
        thread = threading.Thread(target=watch_directory, args=(dir_path.strip(),))
        thread.start()
        threads.append(thread)

    try:
        for thread in threads:
            thread.join()
    except KeyboardInterrupt:
        log("Stopping monitor.")

if __name__ == "__main__":
    main()






'''
import subprocess
import os
import sys
import threading

# Get directories to watch, comma-separated
WATCH_DIRS = os.environ.get("WATCH_DIRS", "/watched").split(",")

def watch_directory(path):
    path = path.strip()
    if not os.path.exists(path):
        print(f"Directory does not exist: {path}")
        return

    print(f"Monitoring: {path}")

    process = subprocess.Popen(
        ["inotifywait", "-m", "-e", "create", "-e", "delete" path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    try:
        for line in process.stdout:
            line = line.strip()
            if "CREATE" in line:
                print(f"File Created in {path}: {line}")
            elif "DELETE" in line:
                print(f"File Created in {path}: {line}")
    except Exception as e:
        print(f"Error watching {path}: {e}")
    finally:
        process.terminate()

def main():
    threads = []

    for dir_path in WATCH_DIRS:
        thread = threading.Thread(target=watch_directory, args=(dir_path.strip(),))
        thread.start()
        threads.append(thread)

    try:
        for thread in threads:
            thread.join()
    except KeyboardInterrupt:
        print("Stopping monitor.")

if __name__ == "__main__":
    main()
'''


## sudo docker run -it --rm --name file-watcher -v "$(pwd)/watched1:/watched1" -v "$(pwd)/watched2:/watched2" -e WATCH_DIRS="/watched1,/watched2" arch-file-monitor



