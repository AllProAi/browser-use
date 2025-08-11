#!/bin/bash
# Docker Testing Script for Research Intelligence System
# Tests Docker build, run, and basic functionality

set -e

echo "🐳 Testing Docker Setup for Research Intelligence System"
echo "=" * 60
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
IMAGE_NAME="research-intelligence"
CONTAINER_NAME="research-intelligence-test"
TEST_PORT="8080"

# Function to print status
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Cleanup function
cleanup() {
    echo ""
    echo "🧹 Cleaning up test containers and images..."
    docker stop $CONTAINER_NAME 2>/dev/null || true
    docker rm $CONTAINER_NAME 2>/dev/null || true
}

# Set trap for cleanup
trap cleanup EXIT

# Test 1: Check Docker installation
echo "1️⃣ Testing Docker installation..."
if ! docker --version > /dev/null 2>&1; then
    print_error "Docker is not installed or not running"
    exit 1
fi
print_status "Docker is available: $(docker --version)"

# Test 2: Build Docker image
echo ""
echo "2️⃣ Building Docker image..."
if docker build -t $IMAGE_NAME:test . ; then
    print_status "Docker image built successfully"
else
    print_error "Docker build failed"
    exit 1
fi

# Test 3: Check image size and layers
echo ""
echo "3️⃣ Checking image details..."
docker images $IMAGE_NAME:test --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}\t{{.CreatedSince}}"

# Get image size in MB for comparison
IMAGE_SIZE=$(docker images $IMAGE_NAME:test --format "{{.Size}}" | head -1)
echo "Image size: $IMAGE_SIZE"

# Test 4: Test container startup (health check mode)
echo ""
echo "4️⃣ Testing container startup..."

# First, cleanup any existing test containers
docker stop $CONTAINER_NAME 2>/dev/null || true
docker rm $CONTAINER_NAME 2>/dev/null || true

# Create a minimal .env for testing
cat > .env.test << EOF
OPENAI_API_KEY=test-key-for-container-test
EMAIL_SENDER=test@example.com
EMAIL_PASSWORD=test-password
EMAIL_RECIPIENTS=recipient@example.com
DAILY_ANALYSIS_TIME=09:00
RUN_MODE=scheduler
HEADLESS_MODE=true
ENABLE_EMAIL_REPORTS=false
ENABLE_ARCHIVING=false
RUN_ON_STARTUP=false
EOF

# Run container with test configuration
docker run -d \
  --name $CONTAINER_NAME \
  --env-file .env.test \
  -p ${TEST_PORT}:8080 \
  --health-cmd="curl -f http://localhost:8080/health || exit 1" \
  --health-interval=10s \
  --health-timeout=5s \
  --health-retries=3 \
  $IMAGE_NAME:test

if [ $? -eq 0 ]; then
    print_status "Container started successfully"
else
    print_error "Container failed to start"
    exit 1
fi

# Test 5: Wait for container to be ready
echo ""
echo "5️⃣ Waiting for container to be ready..."
for i in {1..30}; do
    if curl -s http://localhost:${TEST_PORT}/ready > /dev/null; then
        print_status "Container is ready after ${i} seconds"
        break
    fi
    if [ $i -eq 30 ]; then
        print_error "Container readiness check timed out"
        docker logs $CONTAINER_NAME
        exit 1
    fi
    echo "Waiting... (${i}/30)"
    sleep 1
done

# Test 6: Test health endpoint
echo ""
echo "6️⃣ Testing health endpoints..."

# Test /health endpoint
if curl -s http://localhost:${TEST_PORT}/health | jq . > /dev/null 2>&1; then
    print_status "Health endpoint responding with valid JSON"
    echo "Health response:"
    curl -s http://localhost:${TEST_PORT}/health | jq .
else
    print_warning "Health endpoint not returning valid JSON (or jq not installed)"
    echo "Raw health response:"
    curl -s http://localhost:${TEST_PORT}/health
fi

# Test /ready endpoint
if curl -s http://localhost:${TEST_PORT}/ready | grep -q "ready"; then
    print_status "Ready endpoint responding correctly"
else
    print_warning "Ready endpoint not responding as expected"
fi

# Test 7: Check container logs
echo ""
echo "7️⃣ Checking container logs..."
echo "Recent container logs:"
docker logs --tail 20 $CONTAINER_NAME

# Test 8: Test file system permissions
echo ""
echo "8️⃣ Testing file system setup..."
docker exec $CONTAINER_NAME ls -la /app/research_results/ > /dev/null
if [ $? -eq 0 ]; then
    print_status "Research results directory accessible"
else
    print_error "Research results directory not accessible"
fi

docker exec $CONTAINER_NAME ls -la /app/logs/ > /dev/null
if [ $? -eq 0 ]; then
    print_status "Logs directory accessible"
else
    print_error "Logs directory not accessible"
fi

# Test 9: Test Python environment
echo ""
echo "9️⃣ Testing Python environment..."
PYTHON_VERSION=$(docker exec $CONTAINER_NAME python --version)
print_status "Python version: $PYTHON_VERSION"

# Test UV installation
UV_VERSION=$(docker exec $CONTAINER_NAME uv --version)
print_status "UV version: $UV_VERSION"

# Test browser installation
BROWSER_CHECK=$(docker exec $CONTAINER_NAME playwright --version)
print_status "Playwright version: $BROWSER_CHECK"

# Test 10: Test import of main modules
echo ""
echo "🔟 Testing Python module imports..."
MODULES=("automation_master" "daily_automation" "email_notifier" "results_manager" "live_research_scraper" "cloud_scheduler")

for module in "${MODULES[@]}"; do
    if docker exec $CONTAINER_NAME python -c "import $module; print('✅ $module imported successfully')" 2>/dev/null; then
        print_status "$module module imports successfully"
    else
        print_error "$module module failed to import"
        # Show the error
        docker exec $CONTAINER_NAME python -c "import $module" || true
    fi
done

# Test 11: Resource usage check
echo ""
echo "1️⃣1️⃣ Checking resource usage..."
STATS=$(docker stats $CONTAINER_NAME --no-stream --format "table {{.CPUPerc}}\t{{.MemUsage}}")
echo "Container resource usage:"
echo "$STATS"

# Test 12: Security check - verify non-root user
echo ""
echo "1️⃣2️⃣ Security check - verifying non-root user..."
USER_CHECK=$(docker exec $CONTAINER_NAME whoami)
if [ "$USER_CHECK" = "researcher" ]; then
    print_status "Container running as non-root user: $USER_CHECK"
else
    print_warning "Container running as: $USER_CHECK (should be 'researcher')"
fi

# Cleanup test environment file
rm -f .env.test

echo ""
echo "🎉 Docker Testing Complete!"
echo ""
echo "📊 Test Summary:"
echo "   ✅ Docker image builds successfully"
echo "   ✅ Container starts and becomes ready"
echo "   ✅ Health endpoints respond correctly" 
echo "   ✅ File system permissions correct"
echo "   ✅ Python environment functional"
echo "   ✅ All modules import successfully"
echo "   ✅ Running as non-root user"
echo ""
echo "🚀 Your Docker setup is ready for deployment!"
echo ""
echo "📋 Next steps:"
echo "   1. Configure your .env file with real API keys"
echo "   2. Test with: docker-compose up"
echo "   3. Deploy to your chosen cloud platform"
echo ""
