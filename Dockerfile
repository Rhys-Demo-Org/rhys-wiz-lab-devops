# Updates to Dockerfile
# Multi-stage build with vulnerable packages 
# Option 1: Known vulnerabilities (DEFAULT)
FROM python:3.8-alpine AS python-base

WORKDIR /app
COPY ./website/flask-app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./website/flask-app /app

# NGINX stage with vulnerable version
FROM nginx:1.18.0-alpine

# Option 2: Latest versions (uncomment to fix vulnerabilities)
# FROM nginx:alpine

# Install Python and supervisor to run both NGINX and Flask
RUN apk add --no-cache python3 py3-pip supervisor && \
    python3 -m ensurepip && \
    pip3 install --upgrade pip

# Copy Python app from build stage
COPY --from=python-base /usr/local/lib/python3.8/site-packages /usr/local/lib/python3.8/site-packages
COPY --from=python-base /app /app

# Install Flask app dependencies in final stage
COPY ./website/flask-app/requirements.txt /app/
RUN pip3 install --no-cache-dir -r /app/requirements.txt

# Create a server info script that will output system information
RUN echo '#!/bin/sh' > /usr/share/nginx/html/version.txt && \
    echo 'echo "Alpine Version: $(cat /etc/alpine-release)"' >> /usr/share/nginx/html/version.txt && \
    echo 'echo "NGINX Version: $(nginx -v 2>&1 | cut -d/ -f2)"' >> /usr/share/nginx/html/version.txt && \
    echo 'echo "Python Version: $(python3 --version)"' >> /usr/share/nginx/html/version.txt && \
    chmod +x /usr/share/nginx/html/version.txt && \
    /usr/share/nginx/html/version.txt > /usr/share/nginx/html/system-info.txt && \
    chmod -R 755 /usr/share/nginx/html

# Copy our HTML file
COPY ./website/index.html /usr/share/nginx/html/index.html

# Create data directory and copy data files
RUN mkdir -p /usr/share/nginx/html/data
COPY ./website/sample_data.txt /usr/share/nginx/html/data/
COPY ./website/keys.txt /usr/share/nginx/html/data/

# Configure NGINX to proxy Flask app
COPY ./website/nginx.conf /etc/nginx/conf.d/default.conf

# Configure Supervisor
RUN mkdir -p /var/log/supervisor
COPY ./website/supervisord.conf /etc/supervisord.conf

# Expose ports
EXPOSE 80 5000

# Start supervisor to manage both services
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]
