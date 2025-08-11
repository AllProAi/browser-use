#!/bin/bash
# Build and Push Script for Research Intelligence System
# Usage: ./build-and-push.sh [registry] [tag]

set -e

# Configuration
DEFAULT_REGISTRY="your-registry.com"
DEFAULT_TAG="latest"
IMAGE_NAME="research-intelligence"

REGISTRY=${1:-$DEFAULT_REGISTRY}
TAG=${2:-$DEFAULT_TAG}
FULL_IMAGE_NAME="$REGISTRY/$IMAGE_NAME:$TAG"

echo "🐳 Building and pushing Research Intelligence Docker image"
echo "=" * 60
echo "Registry: $REGISTRY"
echo "Image: $IMAGE_NAME"
echo "Tag: $TAG"
echo "Full name: $FULL_IMAGE_NAME"
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

# Build the image
echo "🔨 Building Docker image..."
docker build -t $FULL_IMAGE_NAME .

if [ $? -ne 0 ]; then
    echo "❌ Docker build failed"
    exit 1
fi

echo "✅ Docker image built successfully: $FULL_IMAGE_NAME"

# Tag with latest if not already
if [ "$TAG" != "latest" ]; then
    echo "🏷️ Tagging as latest..."
    docker tag $FULL_IMAGE_NAME "$REGISTRY/$IMAGE_NAME:latest"
fi

# Push the image
echo "📤 Pushing Docker image to registry..."
docker push $FULL_IMAGE_NAME

if [ $? -ne 0 ]; then
    echo "❌ Docker push failed"
    echo "💡 Make sure you're logged in to the registry:"
    echo "   docker login $REGISTRY"
    exit 1
fi

echo "✅ Docker image pushed successfully: $FULL_IMAGE_NAME"

# Also push latest if we tagged it
if [ "$TAG" != "latest" ]; then
    echo "📤 Pushing latest tag..."
    docker push "$REGISTRY/$IMAGE_NAME:latest"
fi

echo ""
echo "🎉 Build and push completed!"
echo "📋 Next steps:"
echo "   1. Update your deployment files with: $FULL_IMAGE_NAME"
echo "   2. Deploy to your cloud platform"
echo "   3. Configure secrets/environment variables"
echo ""

# Show image size
echo "📊 Image information:"
docker images $FULL_IMAGE_NAME --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}\t{{.CreatedSince}}"

# Optional: Run security scan if trivy is available
if command -v trivy &> /dev/null; then
    echo ""
    echo "🔒 Running security scan..."
    trivy image --severity HIGH,CRITICAL $FULL_IMAGE_NAME
fi
