# 1. Base Image: Use an official, pre-built Python runtime image.
# 'slim' means it is a minimal, lightweight Linux system that keeps our container size small.
FROM python:3.9-slim

# 2. Working Directory: Set the active folder inside the container to /app.
# If /app does not exist, Docker will create it. All commands below this line will run inside this folder.
WORKDIR /app

# 3. Dependencies: Run pip (Python's package installer) to download and install Flask.
# This makes sure Flask is available inside the container's Python environment.
RUN pip install flask

# 4. Copy Code: Copy all files from our local project directory (the folder containing this Dockerfile)
# into the active working directory (/app) of the container.
COPY . .

# 5. Default Startup Command: Specify the command to run when the container starts up.
# This runs our Flask application. Unlike RUN commands (which run during build time), 
# CMD only runs when the final container is started up via 'docker run'.
CMD ["python", "app.py"]