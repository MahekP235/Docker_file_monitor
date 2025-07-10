# Use the latest official Ubuntu base image
FROM ubuntu:latest

# Prevent user prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install required tools
RUN apt-get update && \
    apt-get install -y python3 python3-pip inotify-tools && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set working directory inside the container
WORKDIR /app

# Copy the monitoring script into the container
COPY monitor.py .

# Run the script
CMD ["python3", "monitor.py"]
