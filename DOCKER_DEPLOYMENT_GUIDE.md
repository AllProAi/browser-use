# 🐳 Docker Deployment Guide - Research Intelligence System

Complete guide for containerizing and deploying your research intelligence system to the cloud.

## 📦 Container Overview

The system is packaged as a Docker container that includes:
- ✅ **Complete Python environment** with UV package manager
- ✅ **Playwright browser** (Chromium) with all dependencies  
- ✅ **Cloud-native scheduler** that works without cron/task scheduler
- ✅ **Health checks** for container orchestration
- ✅ **Persistent storage** for results and logs
- ✅ **Security hardening** with non-root user
- ✅ **Multi-platform support** (AMD64/ARM64)

## 🚀 Quick Start - Local Development

### 1. Build and Test Locally

```bash
# Build the Docker image
docker build -t research-intelligence:latest .

# Test run (configure .env first)
docker-compose up
```

### 2. Configure Environment

Create `.env` file with your settings:
```bash
# Required API Keys
OPENAI_API_KEY=your_openai_key_here
# OR
ANTHROPIC_API_KEY=your_anthropic_key_here

# Required Email Settings
EMAIL_SENDER=your_email@gmail.com
EMAIL_PASSWORD=your_gmail_app_password
EMAIL_RECIPIENTS=recipient1@email.com,recipient2@email.com

# Optional Scheduling
DAILY_ANALYSIS_TIME=09:00
TIMEZONE=America/New_York
```

### 3. Run with Docker Compose

```bash
# Start the system
docker-compose up -d

# Check logs
docker-compose logs -f

# Check health
curl http://localhost:8080/health

# Stop the system
docker-compose down
```

## ☁️ Cloud Deployment Options

### Option 1: AWS ECS Fargate

**Benefits**: Serverless, managed, auto-scaling

```bash
# 1. Build and push to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com

docker build -t research-intelligence .
docker tag research-intelligence:latest YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/research-intelligence:latest
docker push YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/research-intelligence:latest

# 2. Create EFS for persistent storage
aws efs create-file-system --creation-token research-intelligence-efs

# 3. Store secrets in AWS Secrets Manager
aws secretsmanager create-secret --name "research-intelligence/openai-api-key" --secret-string "your-api-key"
aws secretsmanager create-secret --name "research-intelligence/email-sender" --secret-string "your-email@gmail.com"
aws secretsmanager create-secret --name "research-intelligence/email-password" --secret-string "your-app-password"
aws secretsmanager create-secret --name "research-intelligence/email-recipients" --secret-string "recipient@email.com"

# 4. Deploy using ECS task definition
aws ecs register-task-definition --cli-input-json file://deploy/aws-ecs-task.json
aws ecs create-service --cluster research-intelligence --service-name research-intelligence-service --task-definition research-intelligence-task --desired-count 1
```

**Cost**: ~$50-100/month for 24/7 operation

### Option 2: Google Cloud Run

**Benefits**: Pay-per-use, managed, auto-scaling to zero

```bash
# 1. Build and push to Container Registry
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/research-intelligence

# 2. Create secrets in Secret Manager
gcloud secrets create openai-api-key --data-file=-
gcloud secrets create email-sender --data-file=-
gcloud secrets create email-password --data-file=-
gcloud secrets create email-recipients --data-file=-

# 3. Deploy to Cloud Run
gcloud run deploy research-intelligence \
  --image gcr.io/YOUR_PROJECT_ID/research-intelligence \
  --platform managed \
  --region us-central1 \
  --memory 4Gi \
  --cpu 2 \
  --max-instances 1 \
  --min-instances 1 \
  --timeout 3600s \
  --no-allow-unauthenticated

# Alternative: Use Cloud Scheduler for job-based execution
gcloud scheduler jobs create http research-intelligence-daily \
  --schedule="0 9 * * *" \
  --uri=https://YOUR_CLOUD_RUN_URL/run \
  --http-method=POST \
  --oidc-service-account-email=YOUR_SERVICE_ACCOUNT@YOUR_PROJECT.iam.gserviceaccount.com
```

**Cost**: ~$10-30/month (pay-per-use)

### Option 3: Azure Container Instances

**Benefits**: Simple deployment, pay-per-second

```bash
# 1. Build and push to Azure Container Registry
az acr build --registry YOUR_REGISTRY --image research-intelligence:latest .

# 2. Deploy using ARM template
az deployment group create \
  --resource-group research-intelligence-rg \
  --template-file deploy/azure-container-instance.json \
  --parameters openaiApiKey=YOUR_API_KEY \
               emailSender=your-email@gmail.com \
               emailPassword=YOUR_APP_PASSWORD \
               emailRecipients=recipient@email.com
```

**Cost**: ~$40-80/month for continuous operation

### Option 4: Kubernetes (Any Cloud)

**Benefits**: Maximum flexibility, multi-cloud, orchestration features

```bash
# 1. Build and push to your registry
./deploy/build-and-push.sh your-registry.com v1.0.0

# 2. Update Kubernetes manifests
# Edit deploy/kubernetes-deployment.yaml with your image name and secrets

# 3. Deploy to Kubernetes
kubectl apply -f deploy/kubernetes-deployment.yaml

# 4. Check deployment
kubectl get pods -n research-intelligence
kubectl logs -f deployment/research-intelligence-deployment -n research-intelligence
```

## 🔧 Configuration Options

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DAILY_ANALYSIS_TIME` | `09:00` | Daily analysis time (HH:MM) |
| `TIMEZONE` | `UTC` | Timezone for scheduling |
| `RUN_MODE` | `scheduler` | `scheduler` (continuous) or `once` (single run) |
| `RUN_ON_STARTUP` | `false` | Run analysis immediately on container start |
| `HEADLESS_MODE` | `true` | Run browser in headless mode |
| `ENABLE_EMAIL_REPORTS` | `true` | Send email notifications |
| `ENABLE_ARCHIVING` | `true` | Archive old reports |
| `HEALTH_CHECK_PORT` | `8080` | Port for health check endpoints |

### Secrets (Required)

| Secret | Description |
|--------|-------------|
| `OPENAI_API_KEY` | OpenAI API key for GPT models |
| `EMAIL_SENDER` | Gmail address for sending reports |
| `EMAIL_PASSWORD` | Gmail App Password |
| `EMAIL_RECIPIENTS` | Comma-separated email addresses |

### Volume Mounts

| Path | Purpose |
|------|---------|
| `/app/research_results` | Persistent storage for analysis results |
| `/app/logs` | Container logs and status files |

## 📊 Monitoring and Health Checks

### Health Endpoints

- **`/health`** - Detailed health status (JSON)
- **`/ready`** - Kubernetes readiness probe
- **`GET /health`** example response:
```json
{
  "running": true,
  "last_run_time": "2025-01-08T09:00:00Z",
  "next_run_time": "2025-01-09T09:00:00Z",
  "schedule_time": "09:00",
  "environment": {
    "openai_configured": true,
    "email_configured": true
  }
}
```

### Log Monitoring

```bash
# Docker Compose
docker-compose logs -f research-intelligence

# Kubernetes
kubectl logs -f deployment/research-intelligence-deployment -n research-intelligence

# Cloud platforms have built-in log viewers
```

### Performance Metrics

- **Memory Usage**: ~1-2GB during analysis
- **CPU Usage**: ~1-2 cores during analysis  
- **Disk Usage**: ~5-10MB per daily report
- **Network**: Minimal (web scraping only)
- **Analysis Duration**: 3-5 minutes typical

## 🔒 Security Best Practices

### Container Security
```dockerfile
# Non-root user
USER researcher

# Read-only filesystem (optional)
--read-only --tmpfs /tmp

# Drop capabilities
--cap-drop=ALL --cap-add=NET_BIND_SERVICE
```

### Secrets Management
- ✅ Use cloud-native secret managers (AWS Secrets Manager, GCP Secret Manager, etc.)
- ✅ Never embed secrets in container images
- ✅ Rotate API keys and passwords regularly
- ✅ Use App Passwords for Gmail (not regular passwords)

### Network Security
```bash
# Restrict network access (example for Kubernetes)
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: research-intelligence-netpol
spec:
  podSelector:
    matchLabels:
      app: research-intelligence
  policyTypes:
  - Egress
  egress:
  - to: []  # Allow all egress for web scraping
```

## 🎯 Deployment Strategies

### Strategy 1: Continuous Container (Recommended)
- **Use Case**: Reliable daily analysis
- **Configuration**: `RUN_MODE=scheduler`
- **Best For**: AWS ECS, GKE Autopilot, Azure Container Instances
- **Cost**: Higher (24/7 running) but most reliable

### Strategy 2: Scheduled Jobs
- **Use Case**: Cost optimization
- **Configuration**: `RUN_MODE=once` 
- **Best For**: Kubernetes CronJobs, Cloud Scheduler + Cloud Run
- **Cost**: Lower (pay-per-execution) but requires job orchestration

### Strategy 3: Hybrid Approach
- **Use Case**: High availability with cost control
- **Setup**: Continuous container + backup scheduled jobs
- **Failover**: If main container fails, backup jobs continue

## 🚨 Troubleshooting

### Common Issues

**Container Won't Start**
```bash
# Check logs
docker logs research-intelligence-container

# Verify environment variables
docker exec -it research-intelligence-container env | grep -E "(OPENAI|EMAIL)"

# Test health endpoint
curl http://container-ip:8080/health
```

**Analysis Fails**
```bash
# Check browser installation
docker exec -it research-intelligence-container playwright --version

# Test API connectivity
docker exec -it research-intelligence-container python -c "import openai; print('OpenAI client works')"

# Check file permissions
docker exec -it research-intelligence-container ls -la /app/research_results/
```

**Email Delivery Issues**
```bash
# Verify Gmail App Password setup
# Test SMTP connection
docker exec -it research-intelligence-container python -c "
import smtplib
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login('$EMAIL_SENDER', '$EMAIL_PASSWORD')
print('SMTP connection successful')
server.quit()
"
```

### Resource Troubleshooting

**Out of Memory**
```bash
# Increase memory limits
# Docker Compose: memory: 4G
# Kubernetes: memory: "4Gi"
# AWS ECS: "memory": "4096"
```

**Disk Space Issues**
```bash
# Enable automatic archiving
ENABLE_ARCHIVING=true

# Or manually clean up
docker exec -it research-intelligence-container find /app/research_results -name "*.json" -mtime +30 -delete
```

## 🎉 Production Checklist

Before deploying to production:

- ✅ **Secrets configured** in cloud secret manager
- ✅ **Persistent storage** configured for results/logs
- ✅ **Health checks** responding correctly
- ✅ **Resource limits** set appropriately
- ✅ **Email delivery** tested and working
- ✅ **Monitoring/alerting** configured
- ✅ **Backup strategy** in place
- ✅ **Cost monitoring** enabled
- ✅ **Log aggregation** configured
- ✅ **Security policies** applied

## 💰 Cost Optimization Tips

1. **Use job-based execution** instead of 24/7 containers for Cloud Run/Functions
2. **Configure auto-scaling** to zero during off hours
3. **Use spot/preemptible instances** where possible
4. **Implement lifecycle policies** for old data archiving
5. **Monitor API usage** to optimize model selection (gpt-4o-mini vs gpt-4o)
6. **Use regional pricing** - deploy in cheaper regions if latency allows

---

**Your research intelligence system is ready for cloud deployment! 🚀☁️**

Choose the deployment option that best fits your needs, budget, and technical requirements.
