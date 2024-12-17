# Use Python 3.11 (or your desired version)
FROM python:3.11

# Set the working directory inside the container
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all content from the 'app' folder to the container's '/app' folder
COPY app/ /app/

# Expose the port FastAPI will run on
EXPOSE 8000

# Run FastAPI with Uvicorn (main.py is at the root of your project)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
