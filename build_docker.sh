#!/bin/bash
IMAGE_NAME="steelydk/betterlrcapi:latest"

echo "Check for Docker Buildx..."
# Ensure buildx instance exists
docker buildx create --use --name multi-arch-builder --node multi-arch-builder0 2>/dev/null || true

echo "Building and Pushing Multi-Arch Image (linux/amd64, linux/arm64)..."
echo "Target: $IMAGE_NAME"

# Build and push in one step (required for multi-arch manifest)
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t "$IMAGE_NAME" \
  --push \
  .

echo ""
echo "Build and Push Complete!"
echo "You can verify architectures on Docker Hub."
