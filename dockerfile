
# # Use Arch Linux base image
# FROM archlinux:latest

# # Set environment to non-interactive
# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1

# # Update system and install required packages
# RUN pacman -Syu --noconfirm \
#     python \
#     python-pip \
#     inotify-tools

# # Set working directory
# WORKDIR /app

# # Copy the Python monitor script
# COPY monitor.py .

# # Set the directory to monitor inside the container
# ENV WATCH_DIR="/watched"

# # Create directory to be monitored
# RUN mkdir -p ${WATCH_DIR}

# # Set the default command to run the monitor
# CMD ["python", "monitor.py"]



FROM archlinux:latest

# Install required packages
RUN pacman -Sy --noconfirm python inotify-tools

WORKDIR /app
COPY monitor.py .

CMD ["python", "monitor.py"]
