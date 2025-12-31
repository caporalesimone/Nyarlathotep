# Use a base image with Python 3.12
FROM python:3.12.6-alpine

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file to the working directory
COPY requirements.txt .

# Install project dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY server.py versions.py ./

# Expose port 8080
EXPOSE 8080

# Start the Flask server
CMD ["python", "server.py"]

