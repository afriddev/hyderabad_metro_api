# Use Python 3.11 (or 3.10 if you're not using features requiring 3.11+)
FROM python:3.11

# Set the working directory inside the container
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app code from 'all' directory to the container
COPY all/ /app/all/

# Expose the port that FastAPI will run on
EXPOSE 8000

# Run FastAPI with Uvicorn (main.py is located at the root)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
