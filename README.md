# Docker File & Folder Monitor

A Dockerized Python-based monitoring tool that watches **multiple folders** inside a container for the following events:

- File **creation**
- File **deletion**
- File **modification**
- File **move/rename**
- File **permission or metadata changes**
- File **access**
- File **open**
- File **moving**
- File **close**
- File system **unmount**
- **symlink creation**

Logs are printed to `stdout` and can optionally be saved to a file.

---

## Folder Structure



## Prerequisites

- Docker installed on your system (use `ssudo apt-get install docker-ce docker-ce-cli containerd.io containerd.io docker-buildx-plugin docker-compose-plugin` on Ubuntu)
- Your user should have access to Docker or use `sudo`
- Basic terminal knowledge


## Setup & Run

### 1. Clone or create your project structure


`mkdir docker_file_monitor && cd docker_file_monitor`
`mkdir watched1 watched2 logs`

### 2. Save these files:

monitor.py – Python monitoring script
Dockerfile – Builds Arch Linux-based Docker image

### 3. Build the Docker Image

`docker build -t file-watcher .`

### Run the container

`sudo docker run -it --rm   --name file-watcher --privileged -v "$PWD/watched1:/watched1" -v "$PWD/watched2:/watched2" -v "$PWD/logs:/log" -e WATCH_DIRS="/watched1,/watched2" -e LOG_FILE="/log/events.log" file-watcher`

