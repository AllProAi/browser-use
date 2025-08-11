# 🤖 Research Intelligence Automation Setup Guide

Complete guide to setup automated daily research intelligence with email notifications and organized results storage.

## 🎯 What You'll Get

✅ **Daily Automated Analysis** - Runs every day at your chosen time  
✅ **Email Reports** - Professional HTML reports delivered to your inbox  
✅ **Organized Storage** - Automatic file organization and archiving  
✅ **Weekly Summaries** - Weekly trend analysis  
✅ **Error Handling** - Automatic retries and error notifications  
✅ **Cross-Platform** - Works on Windows, Linux, and macOS  

## 📁 System Architecture

```
research_results/
├── daily_reports/          # Daily analysis reports
│   └── 2025-01-08/
│       ├── daily_analysis_20250108_0900.json
│       ├── daily_analysis_20250108_0900_summary.md
│       └── daily_analysis_20250108_0900_metadata.json
├── weekly_summaries/       # Weekly trend summaries
├── monthly_archives/       # Compressed old reports
├── email_reports/          # Email notification logs
└── backup/                 # System backups
```

## 🚀 Quick Setup

### 1. Environment Configuration

Add these settings to your `.env` file:

```bash
# Required: API Keys
OPENAI_API_KEY=your_openai_api_key_here
# OR
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Required: Email Configuration
EMAIL_SENDER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password_here
EMAIL_RECIPIENTS=recipient1@email.com,recipient2@email.com

# Optional: Automation Settings
DAILY_ANALYSIS_TIME=09:00
ENABLE_EMAIL_REPORTS=true
ENABLE_ARCHIVING=true
HEADLESS_MODE=true
```

### 2. Gmail Setup (Recommended)

For Gmail users:

1. **Enable 2-Factor Authentication**
   - Go to Google Account Settings
   - Security → 2-Step Verification

2. **Generate App Password**
   - In 2-Step Verification settings
   - App passwords → Select app: Mail
   - Copy the 16-character password

3. **Update .env file**
   ```bash
   EMAIL_SENDER=yourname@gmail.com
   EMAIL_PASSWORD=your_16_character_app_password
   ```

### 3. Run Setup

```bash
# Test your configuration
uv run python automation_master.py
```

Choose option 6 to test the complete system.

## 📊 Usage Options

### Option 1: Interactive Automation
```bash
# Run the master controller
uv run python automation_master.py

# Choose from menu:
# 1. Run analysis now (test)
# 2. Start daily automation  
# 3. Setup Windows scheduler
# 4. Setup Linux cron job
```

### Option 2: Windows Task Scheduler
```bash
# Setup Windows automation
uv run python automation_master.py
# Choose option 3

# Then follow the printed instructions to setup Windows Task Scheduler
```

### Option 3: Linux Cron Job
```bash
# Setup Linux cron job  
uv run python automation_master.py
# Choose option 4

# Then run: crontab -e
# Add the generated cron line
```

## 📧 Email Report Features

### Daily Reports Include:
- **Executive Summary** with key metrics
- **Research Categories** breakdown 
- **Trending Technologies** list
- **Actionable R&D Recommendations**
- **High-Impact Opportunities**
- **Attached Files** (JSON + Markdown)

### Sample Email Report:
```
Subject: 📊 Daily Research Intelligence Report - 2025-01-08 (127 episodes)

🔬 Research Intelligence Report
Daily Analysis - January 8, 2025

📊 Executive Summary
Episodes Analyzed: 127
Research Categories: 8  
Recommendations: 10

📂 Research Categories
• AI/ML: 38 episodes
• Computer Vision: 24 episodes
• Robotics: 19 episodes
[...]

💡 Top R&D Recommendations
1. Investigate computer vision applications for industrial automation
2. Develop federated learning capabilities for privacy-preserving AI
[...]
```

## 🗂️ File Organization

### Daily Reports
- **JSON**: Complete structured data
- **Markdown**: Executive summary  
- **Metadata**: Report statistics

### Weekly Summaries
- **Trend Analysis**: Week-over-week changes
- **Category Patterns**: Research focus shifts
- **Recommendation Tracking**: Recurring themes

### Monthly Archives
- **Automatic Compression**: Old reports → ZIP files
- **Space Management**: Keep recent data accessible
- **Backup Strategy**: Preserve historical analysis

## ⚡ Automation Features

### Daily Schedule
- **Configurable Time**: Set your preferred analysis time
- **Retry Logic**: Automatic retry on failures
- **Error Notifications**: Email alerts for issues
- **Resource Management**: Cleanup temp files

### Weekly Schedule  
- **Sunday Summaries**: Weekly trend analysis
- **Email Delivery**: Comprehensive weekly reports
- **Data Aggregation**: Combine daily insights

### System Monitoring
- **Status Dashboard**: Current system health
- **Performance Metrics**: Analysis duration tracking
- **Failure Tracking**: Consecutive error monitoring
- **Disk Usage**: Storage management alerts

## 🛠️ Troubleshooting

### Common Issues

**❌ Email Authentication Failed**
```
Solution: Use Gmail App Password instead of regular password
1. Enable 2FA on your Google account
2. Generate App Password: https://myaccount.google.com/apppasswords
3. Use App Password in EMAIL_PASSWORD
```

**❌ Browser Installation Issues**
```bash
# Reinstall Playwright browsers
uv run playwright install chromium --with-deps --force
```

**❌ Analysis Keeps Failing**
```bash
# Check API key
echo $OPENAI_API_KEY

# Test basic functionality
uv run python test_setup.py

# Check internet connection
ping google.com
```

**❌ Results Directory Issues**
```bash
# Run results manager directly
uv run python results_manager.py

# Check permissions
ls -la research_results/
```

### Performance Optimization

**For Speed:**
```bash
# Use faster model
export OPENAI_MODEL="gpt-4o-mini"

# Reduce episodes analyzed  
export MAX_EPISODES=50

# Enable headless mode
export HEADLESS_MODE=true
```

**For Accuracy:**
```bash
# Use more capable model
export OPENAI_MODEL="gpt-4o"

# Analyze more episodes
export MAX_EPISODES=200

# Enable comprehensive analysis
export ANALYSIS_DEPTH="comprehensive"
```

## 🔧 Advanced Configuration

### Custom Analysis Schedule
```python
# In daily_automation.py, modify:
automation = DailyAutomation(
    schedule_time="06:00",  # 6 AM
    enable_email=True,
    enable_archiving=True
)
```

### Custom Email Templates
```python
# In email_notifier.py, modify _generate_email_body()
# Add custom sections, styling, or content
```

### Custom Results Organization
```python
# In results_manager.py, modify directory structure
# Add new categories or change naming conventions
```

## 📈 Monitoring and Analytics

### System Status
```bash
# Check system status
uv run python automation_master.py
# Choose option 5: "Show system status"
```

### Log Analysis
```bash
# View automation logs (Linux/Mac)
tail -f research_intelligence.log

# View error logs
ls research_results/errors/
```

### Performance Metrics
- **Analysis Duration**: Track processing time
- **Episode Coverage**: Monitor data completeness
- **Email Delivery**: Verify notification success
- **Storage Usage**: Manage disk space

## 🔒 Security Best Practices

### API Key Management
- ✅ Use `.env` file for secrets
- ✅ Never commit API keys to git
- ✅ Rotate keys periodically
- ✅ Use read-only keys when possible

### Email Security
- ✅ Use App Passwords for Gmail
- ✅ Enable 2-factor authentication
- ✅ Limit recipient list
- ✅ Monitor for unauthorized access

### System Security
- ✅ Run automation with limited privileges
- ✅ Keep dependencies updated
- ✅ Monitor for suspicious activity
- ✅ Regular backup verification

## 🆘 Support and Maintenance

### Regular Maintenance Tasks

**Weekly:**
- Check email delivery success
- Review analysis quality
- Monitor disk usage

**Monthly:**
- Update dependencies: `uv sync --upgrade`
- Review and clean archives
- Validate API key usage

**Quarterly:**
- Performance optimization review
- Security audit
- Backup strategy verification

### Getting Help

1. **Check Logs**: Look in `research_results/errors/`
2. **Test Components**: Run individual system tests
3. **Verify Configuration**: Use `research_config.py`
4. **Check Documentation**: Review this guide and README files

---

## 🎉 You're All Set!

Your research intelligence system is now configured for:

✅ **Automated Daily Analysis** at your chosen time  
✅ **Professional Email Reports** with actionable insights  
✅ **Organized Data Storage** with automatic archiving  
✅ **Error Handling and Recovery** for reliable operation  
✅ **Cross-Platform Compatibility** for any system  

**Next Steps:**
1. Run a test analysis: `uv run python automation_master.py` → Option 1
2. Setup your preferred automation method (Windows/Linux)
3. Monitor the first few runs to ensure everything works
4. Enjoy your daily research intelligence! 🚀📊

**Happy Automated Research Intelligence! 🤖✨**
