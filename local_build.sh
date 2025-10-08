#!/bin/bash

# Build Alpine
echo ""
echo "Build from Alpine; Add Content:"
echo "==============================================================="

docker build \
    -f Dockerfile \
    -t alpine-nginx .

# runs on http://localhost:8080 and https://localhost:8443
docker run -d -p 8080:80 alpine-nginx