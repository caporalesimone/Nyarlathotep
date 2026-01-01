# Multi-stage Dockerfile for Nyarlathotep
# Combines frontend + backend in a single container with nginx

# Stage 1: Build frontend
FROM node:20.17.0-alpine3.20 AS frontend-builder

WORKDIR /app

# Copy frontend package files
COPY nyarlathotep-frontend/package*.json ./
RUN npm install

# Copy frontend source and build
COPY nyarlathotep-frontend/ ./
RUN npm run build

# Stage 2: Setup backend
FROM python:3.12.6-alpine AS backend-setup

WORKDIR /app

# Copy backend requirements and install
COPY nyarlathotep-backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend application files and schema
COPY nyarlathotep-backend/server.py nyarlathotep-backend/versions.py ./
COPY agent_json_schema.json ./

# Stage 3: Runtime with nginx + Flask
FROM python:3.12.6-alpine

WORKDIR /app

# Install nginx and runtime dependencies + create directories
RUN apk add --no-cache nginx openssl && \
    mkdir -p /etc/nginx/ssl /run/nginx

# Generate self-signed certificate for development (do this early to cache properly)
RUN openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /etc/nginx/ssl/nginx.key \
    -out /etc/nginx/ssl/nginx.crt \
    -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"

# Copy nginx configuration
COPY docker/nginx.conf /etc/nginx/nginx.conf

# Copy Python dependencies from backend stage
COPY --from=backend-setup /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages

# Copy backend application
COPY --from=backend-setup /app /app

# Copy built frontend static files
COPY --from=frontend-builder /app/build /var/www/html

# Copy and make start script executable
COPY docker/start.sh /start.sh
RUN chmod +x /start.sh

# Expose HTTP and HTTPS ports
EXPOSE 80 443

CMD ["/start.sh"]
