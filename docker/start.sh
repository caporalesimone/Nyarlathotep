#!/bin/sh

# Start Flask backend in background
echo "Starting Flask backend on port 8080..."
python /app/server.py &
FLASK_PID=$!

# Wait a moment for Flask to start
sleep 2

# Start nginx in foreground
echo "Starting nginx on ports 80 (HTTP) and 443 (HTTPS)..."
nginx -g 'daemon off;' &
NGINX_PID=$!

# Function to handle shutdown signals
cleanup() {
    echo "Shutting down services..."
    kill $FLASK_PID 2>/dev/null
    kill $NGINX_PID 2>/dev/null
    exit 0
}

# Trap SIGTERM and SIGINT signals
trap cleanup SIGTERM SIGINT

# Wait for either process to exit
wait -n $FLASK_PID $NGINX_PID

# If one exits, cleanup everything
cleanup
