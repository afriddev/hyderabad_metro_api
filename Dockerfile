# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variable to avoid buffering logs
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8000 to be accessible outside the container
EXPOSE 8000

# Run Uvicorn in the background, then keep the container alive using tail
CMD uvicorn main:app --host 0.0.0.0 --port 8000 & tail -f /dev/null
