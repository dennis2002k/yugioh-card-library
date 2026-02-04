# Use an official lightweight Python image
FROM python:3.12-slim

# Set environment variables
# Prevents Python from writing .pyc files and keeps stdout/stderr unbuffered
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /YgoWebApp

# Install system dependencies (needed for some Python packages)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# Create an empty images directory so app.mount doesn't crash
RUN mkdir -p /app/images

# Expose the port FastAPI runs on
EXPOSE 8000

# Command to run the application
# We use 0.0.0.0 so it's accessible outside the container
CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "8000"]