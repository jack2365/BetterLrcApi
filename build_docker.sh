#!/bin/bash
echo "Building BetterLrcApi Docker image..."
docker build -t betterlrcapi:latest .

echo "Build complete."
echo "To run locally:"
echo "docker run -p 8080:8080 betterlrcapi:latest"

echo ""
echo "To push to Docker Hub:"
echo "docker tag betterlrcapi:latest steelydk/betterlrcapi:latest"
echo "docker push steelydk/betterlrcapi:latest"
