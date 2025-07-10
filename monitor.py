import subprocess
import os
import sys
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
'''
def watch_directory(path):
    path = path.strip()
    if not os.path.exists(path):
        log(f"Directory does not exist: {path}")
        return

    log(f"Monitoring: {path}")
'''


# Inotify events we want to track for forensic purposes
EVENTS = [
    "access",        # File was read
    "open",          # File was opened
    "modify",        # Content changed
    "attrib",        # Metadata (permissions/timestamps) changed
    "close_write",   # File closed after writing
    "close_nowrite", # File closed without writing
    "create",        # File created
    "delete",        # File deleted
    "delete_self",   # Watched file deleted
    "moved_from",    # File moved out
    "moved_to",      # File moved in
    "move_self",     # Watched file itself moved
    "unmount"        # Filesystem unmounted
]

def get_file_info(filepath):
    try:
        file_stat = os.lstat(filepath)  # lstat to catch symlinks
        uid = file_stat.st_uid
        gid = file_stat.st_gid
        is_symlink = stat.S_ISLNK(file_stat.st_mode)
        return uid, gid, is_symlink
    except FileNotFoundError:
        return None, None, False

def watch_directory(path):
    path = path.strip()
    if not os.path.exists(path):
        print(f"[ERROR] Directory does not exist: {path}")
        return

    print(f"[INFO] Monitoring: {path}")

    process = subprocess.Popen(
        [
            "inotifywait",
            "-m",                # Continuous monitoring
            "-r",                # Recursive
            "-e", ",".join(EVENTS),  # Events to watch
            "--format", "%T %e %w%f",  # Format: timestamp event file
            "--timefmt", "%Y-%m-%d %H:%M:%S",
            path
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    try:
        for line in process.stdout:
            line = line.strip()
            parts = line.split(maxsplit=2)
            if len(parts) < 3:
                continue
            timestamp, event, filepath = parts
            uid, gid, is_symlink = get_file_info(filepath)
            extra_info = f" | UID={uid} GID={gid}"
            if "CREATE" in event and is_symlink:
                extra_info += " | [SYMLINK CREATED]"
            print(f"[EVENT] {timestamp} {event} {filepath}{extra_info}")
    except Exception as e:
        print(f"[ERROR] Watching {path}: {e}")
    finally:
        process.terminate()

def main():
    threads = []

    for dir_path in WATCH_DIRS:
        thread = threading.Thread(target=watch_directory, args=(dir_path,))
        thread.start()
        threads.append(thread)

    try:
        for thread in threads:
            thread.join()
    except KeyboardInterrupt:
        print("\n[INFO] Stopping monitor...")

if __name__ == "__main__":
    main()


'''
sudo docker run -it --rm \
  --name file-watcher \
  --privileged \
  -v "$PWD/watched1:/watched1" \
  -v "$PWD/watched2:/watched2" \
  -v "$PWD/logs:/log" \
  -e WATCH_DIRS="/watched1,/watched2" \
  -e LOG_FILE="/log/events.log" \
  file-watcher
'''




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



