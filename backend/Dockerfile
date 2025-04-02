# Use an official Python runtime as the base image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --default-timeout=100 --no-cache-dir -r requirements.txt


# Copy the rest of the application files
COPY . .

# Expose the port your Flask app runs on (Hugging Face uses 7860 by default)
EXPOSE 7860

# Run the application
CMD ["python", "app.py"]
