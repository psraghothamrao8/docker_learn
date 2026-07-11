# Use an official Python runtime as a parent/base image (slim version for a smaller container footprint)
FROM python:3.9-slim

# Set the working directory inside the container to /app. All subsequent commands will run here.
WORKDIR /app

# Run pip install to install Flask, which is the library our web application uses
RUN pip install flask

# Copy all files and folders from our local project folder into the /app folder of the container
COPY . .

# Define the default command to execute when the container starts up (runs the web application)
CMD ["python", "app.py"]