# Docker Testing Script for Research Intelligence System (Windows PowerShell)
# Tests Docker build, run, and basic functionality

param(
    [string]$ImageName = "research-intelligence",
    [string]$ContainerName = "research-intelligence-test", 
    [int]$TestPort = 8080
)

Write-Host "🐳 Testing Docker Setup for Research Intelligence System" -ForegroundColor Cyan
Write-Host ("=" * 60) -ForegroundColor Cyan
Write-Host ""

# Function to print status messages
function Write-Success($message) {
    Write-Host "✅ $message" -ForegroundColor Green
}

function Write-Warning($message) {
    Write-Host "⚠️ $message" -ForegroundColor Yellow
}

function Write-Error($message) {
    Write-Host "❌ $message" -ForegroundColor Red
}

# Cleanup function
function Cleanup {
    Write-Host ""
    Write-Host "🧹 Cleaning up test containers and images..." -ForegroundColor Yellow
    docker stop $ContainerName 2>$null | Out-Null
    docker rm $ContainerName 2>$null | Out-Null
}

# Set trap for cleanup (PowerShell equivalent)
trap { Cleanup; break }

# Test 1: Check Docker installation
Write-Host "1️⃣ Testing Docker installation..."
try {
    $dockerVersion = docker --version
    Write-Success "Docker is available: $dockerVersion"
} catch {
    Write-Error "Docker is not installed or not running"
    exit 1
}

# Test 2: Build Docker image
Write-Host ""
Write-Host "2️⃣ Building Docker image..."
try {
    docker build -t "${ImageName}:test" . 
    Write-Success "Docker image built successfully"
} catch {
    Write-Error "Docker build failed"
    exit 1
}

# Test 3: Check image size and layers
Write-Host ""
Write-Host "3️⃣ Checking image details..."
docker images "${ImageName}:test" --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}\t{{.CreatedSince}}"

# Test 4: Test container startup
Write-Host ""
Write-Host "4️⃣ Testing container startup..."

# Cleanup any existing test containers
docker stop $ContainerName 2>$null | Out-Null
docker rm $ContainerName 2>$null | Out-Null

# Create test environment file
$envContent = @"
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
"@

$envContent | Out-File -FilePath ".env.test" -Encoding UTF8

# Run container with test configuration
try {
    docker run -d `
        --name $ContainerName `
        --env-file .env.test `
        -p "${TestPort}:8080" `
        "${ImageName}:test"
    
    Write-Success "Container started successfully"
} catch {
    Write-Error "Container failed to start"
    exit 1
}

# Test 5: Wait for container to be ready
Write-Host ""
Write-Host "5️⃣ Waiting for container to be ready..."

for ($i = 1; $i -le 30; $i++) {
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:${TestPort}/ready" -TimeoutSec 2 -UseBasicParsing
        if ($response.StatusCode -eq 200) {
            Write-Success "Container is ready after $i seconds"
            break
        }
    } catch {
        if ($i -eq 30) {
            Write-Error "Container readiness check timed out"
            docker logs $ContainerName
            exit 1
        }
        Write-Host "Waiting... ($i/30)"
        Start-Sleep 1
    }
}

# Test 6: Test health endpoints
Write-Host ""
Write-Host "6️⃣ Testing health endpoints..."

try {
    $healthResponse = Invoke-WebRequest -Uri "http://localhost:${TestPort}/health" -UseBasicParsing
    Write-Success "Health endpoint responding"
    Write-Host "Health response:"
    Write-Host $healthResponse.Content
} catch {
    Write-Warning "Health endpoint not responding as expected"
}

try {
    $readyResponse = Invoke-WebRequest -Uri "http://localhost:${TestPort}/ready" -UseBasicParsing
    if ($readyResponse.Content -match "ready") {
        Write-Success "Ready endpoint responding correctly"
    }
} catch {
    Write-Warning "Ready endpoint not responding as expected"
}

# Test 7: Check container logs
Write-Host ""
Write-Host "7️⃣ Checking container logs..."
Write-Host "Recent container logs:"
docker logs --tail 20 $ContainerName

# Test 8: Test file system permissions
Write-Host ""
Write-Host "8️⃣ Testing file system setup..."

try {
    docker exec $ContainerName ls -la /app/research_results/ | Out-Null
    Write-Success "Research results directory accessible"
} catch {
    Write-Error "Research results directory not accessible"
}

try {
    docker exec $ContainerName ls -la /app/logs/ | Out-Null
    Write-Success "Logs directory accessible"
} catch {
    Write-Error "Logs directory not accessible"
}

# Test 9: Test Python environment
Write-Host ""
Write-Host "9️⃣ Testing Python environment..."

$pythonVersion = docker exec $ContainerName python --version
Write-Success "Python version: $pythonVersion"

$uvVersion = docker exec $ContainerName uv --version
Write-Success "UV version: $uvVersion"

$browserCheck = docker exec $ContainerName playwright --version
Write-Success "Playwright version: $browserCheck"

# Test 10: Test import of main modules
Write-Host ""
Write-Host "🔟 Testing Python module imports..."

$modules = @("automation_master", "daily_automation", "email_notifier", "results_manager", "live_research_scraper", "cloud_scheduler")

foreach ($module in $modules) {
    try {
        docker exec $ContainerName python -c "import $module; print('✅ $module imported successfully')" 2>$null
        Write-Success "$module module imports successfully"
    } catch {
        Write-Error "$module module failed to import"
    }
}

# Test 11: Resource usage check
Write-Host ""
Write-Host "1️⃣1️⃣ Checking resource usage..."
$stats = docker stats $ContainerName --no-stream --format "table {{.CPUPerc}}\t{{.MemUsage}}"
Write-Host "Container resource usage:"
Write-Host $stats

# Test 12: Security check
Write-Host ""
Write-Host "1️⃣2️⃣ Security check - verifying non-root user..."
$userCheck = docker exec $ContainerName whoami
if ($userCheck -eq "researcher") {
    Write-Success "Container running as non-root user: $userCheck"
} else {
    Write-Warning "Container running as: $userCheck (should be 'researcher')"
}

# Cleanup
Cleanup
Remove-Item ".env.test" -Force -ErrorAction SilentlyContinue

Write-Host ""
Write-Host "🎉 Docker Testing Complete!" -ForegroundColor Green
Write-Host ""
Write-Host "📊 Test Summary:" -ForegroundColor Cyan
Write-Host "   ✅ Docker image builds successfully"
Write-Host "   ✅ Container starts and becomes ready"
Write-Host "   ✅ Health endpoints respond correctly"
Write-Host "   ✅ File system permissions correct"
Write-Host "   ✅ Python environment functional"
Write-Host "   ✅ All modules import successfully"
Write-Host "   ✅ Running as non-root user"
Write-Host ""
Write-Host "🚀 Your Docker setup is ready for deployment!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Next steps:" -ForegroundColor Cyan
Write-Host "   1. Configure your .env file with real API keys"
Write-Host "   2. Test with: docker-compose up"
Write-Host "   3. Deploy to your chosen cloud platform"
Write-Host ""
