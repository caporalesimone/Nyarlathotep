# Nyarlathotep
Web remote workstations monitor 

## Description
This is a simple client, server (web) workstations monitor.

## Quick Start

### Using Docker (Recommended)

#### Option 1: Pull from GitHub Container Registry

**Using docker run:**
```bash
docker run -d \
  --name nyarlathotep \
  -p 80:80 \
  -p 443:443 \
  --restart always \
  ghcr.io/caporalesimone/nyarlathotep:latest
```

**Using docker-compose:**

Create a `docker-compose.yml` file:
```yaml
services:
  nyarlathotep:
    container_name: nyarlathotep
    image: ghcr.io/caporalesimone/nyarlathotep:latest
    ports:
      - "80:80"
      - "443:443"
    restart: unless-stopped
```

Then run:
```bash
docker-compose up -d
```

#### Option 2: Build from source

Clone the repository and build locally:
```bash
git clone https://github.com/caporalesimone/Nyarlathotep.git
cd Nyarlathotep
docker-compose up -d
```

### Access the application

- **HTTP**: http://localhost
- **HTTPS**: https://localhost (accept self-signed certificate warning)

## Architecture

The application runs as a unified Docker container with:
- **nginx**: Reverse proxy handling HTTP (port 80) and HTTPS (port 443)
- **Flask backend**: Python API server on internal port 8080
- **SvelteKit frontend**: Static files served by nginx

All API calls are proxied through nginx with `/api/*` prefix.

## Client aka Agent
It's a python application actually written for windows (will be os Independent)

## Backend Server
Backend server is a flask web server with 2 routes:

- `/client_update` that waits for a POST with the JSON file from the client.
- `/workstations_status` that is an api that return all the workstations information in a JSON array

## Frontend 
Frontend is written using node js, typescript and Svelte framework. 
It requests the `workstations_status` from the backend and does all the presentation

## Screenshots

![home](.docs-files/home.jpg)
![details](.docs-files/details.jpg)