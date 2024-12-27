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

# Expose the port that the FastAPI app will run on
EXPOSE 8000

# Keep the container alive using tail (you can use a health check in your app)
CMD ["tail", "-f", "/dev/null"]
