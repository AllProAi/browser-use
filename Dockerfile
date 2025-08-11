# Research Intelligence Automation System - Production Docker Image
FROM python:3.11-slim

# Set metadata
LABEL maintainer="Daniel Hill - AllPro.Enterprises Novus | Nexum Labs"
LABEL description="Automated Research Intelligence System with Daily Analysis & Email Reports"
LABEL version="1.0.0"

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    UV_NO_CACHE=1 \
    DEBIAN_FRONTEND=noninteractive

# Set working directory
WORKDIR /app

# Install system dependencies required for Playwright and the system
RUN apt-get update && apt-get install -y \
    # Basic system tools
    curl \
    wget \
    git \
    unzip \
    # Dependencies for Playwright browsers
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libatspi2.0-0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libxss1 \
    libasound2 \
    # Additional dependencies
    fonts-liberation \
    libappindicator3-1 \
    xdg-utils \
    # Cleanup
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /tmp/* \
    && rm -rf /var/tmp/*

# Install UV package manager
RUN pip install uv

# Copy dependency files first for better layer caching
COPY pyproject.toml ./
COPY browser_use/ ./browser_use/

# Install Python dependencies with UV
RUN uv venv /opt/venv && \
    . /opt/venv/bin/activate && \
    uv sync --dev --all-extras && \
    # Install Playwright browsers
    playwright install chromium --with-deps && \
    # Cleanup
    uv cache clean

# Activate virtual environment for all subsequent commands
ENV PATH="/opt/venv/bin:$PATH"

# Copy application code
COPY automation_master.py .
COPY daily_automation.py .
COPY email_notifier.py .
COPY results_manager.py .
COPY live_research_scraper.py .
COPY research_intelligence_agent.py .
COPY research_config.py .
COPY simple_research_demo.py .
COPY setup_research_agent.py .
COPY cloud_scheduler.py .

# Copy documentation
COPY README_Research_Intelligence.md .
COPY AUTOMATION_SETUP_GUIDE.md .
COPY SYSTEM_SUMMARY.md .

# Create non-root user for security
RUN useradd -m -u 1000 researcher && \
    chown -R researcher:researcher /app
USER researcher

# Create necessary directories with proper permissions
RUN mkdir -p /app/research_results/{daily_reports,weekly_summaries,monthly_archives,email_reports,topic_analyses,trends_tracking,backup,temp} && \
    mkdir -p /app/logs

# Create volume mount points for persistent data
VOLUME ["/app/research_results", "/app/logs"]

# Expose port for health checks (optional)
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD python -c "import sys; sys.exit(0)" || exit 1

# Set default command
CMD ["python", "cloud_scheduler.py"]