# Use a base image with Python 3.12
FROM python:3.12.6-alpine

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file to the working directory
COPY nyarlathotep-backend/requirements.txt .

# Install project dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files and schema in a single layer
COPY nyarlathotep-backend/server.py nyarlathotep-backend/versions.py agent_json_schema.json ./

# Expose port 8080
EXPOSE 8080

# Start the Flask server
CMD ["python", "server.py"]

