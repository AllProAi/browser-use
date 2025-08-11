# 🧪 Research Intelligence System - Testing Checklist

## 📋 Required Setup Before Testing

### 1. 🔑 API Keys (Required)

**Option A: OpenAI (Recommended)**
- **Where to get**: [OpenAI API Keys](https://platform.openai.com/api-keys)
- **Cost**: ~$0.10-0.50 per analysis (using gpt-4o-mini)
- **Models**: gpt-4o-mini (cheaper) or gpt-4o (more accurate)
- **Format**: `sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

**Option B: Anthropic Claude (Alternative)**  
- **Where to get**: [Anthropic Console](https://console.anthropic.com/)
- **Cost**: ~$0.15-0.75 per analysis
- **Models**: claude-3-haiku (cheaper) or claude-3-sonnet (better)
- **Format**: `sk-ant-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

### 2. 📧 Email Configuration (Required for Notifications)

**Gmail Setup (Recommended):**

1. **Enable 2-Factor Authentication**
   - Go to [Google Account Security](https://myaccount.google.com/security)
   - Turn on 2-Step Verification

2. **Generate App Password**
   - In Google Account → Security → 2-Step Verification
   - Click "App passwords" at bottom
   - Select "Mail" and generate password
   - **Important**: Use this 16-character password, NOT your regular Gmail password

3. **Required Information**:
   - **EMAIL_SENDER**: your_email@gmail.com
   - **EMAIL_PASSWORD**: 16-character app password (xxxx xxxx xxxx xxxx)
   - **EMAIL_RECIPIENTS**: recipient1@email.com,recipient2@email.com

### 3. ⚙️ System Requirements (Already Setup)

✅ **Python 3.11+** (You have 3.13.5)  
✅ **UV Package Manager** (Installed)  
✅ **Browser-use Dependencies** (Installed)  
✅ **Playwright Chromium** (Installed)  

## 📝 Configuration Steps

### Step 1: Update .env File

Your `.env` file needs these settings:

```bash
# Required: Choose ONE API key
OPENAI_API_KEY=sk-your-openai-key-here
# OR
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here

# Required: Email Settings  
EMAIL_SENDER=your_email@gmail.com
EMAIL_PASSWORD=your_16_char_app_password_here
EMAIL_RECIPIENTS=recipient1@email.com,recipient2@email.com

# Optional: Automation Settings
DAILY_ANALYSIS_TIME=09:00
TIMEZONE=UTC
ENABLE_EMAIL_REPORTS=true
ENABLE_ARCHIVING=true
HEADLESS_MODE=true
BROWSER_USE_LOGGING_LEVEL=info
```

### Step 2: Verify Configuration

```bash
# Check environment setup
uv run python research_config.py
```

Expected output: All green checkmarks ✅

## 🧪 Testing Sequence

### Test 1: Basic Functionality Test
```bash
uv run python test_setup.py
```
**Expected**: "Basic test successful!" message

### Test 2: Email System Test  
```bash
uv run python email_notifier.py
```
**When prompted, choose**: Send test email (y)
**Expected**: Test email in your inbox

### Test 3: Results Manager Test
```bash  
uv run python results_manager.py
```
**Expected**: Directory structure created in `research_results/`

### Test 4: Simple Demo Test
```bash
uv run python simple_research_demo.py
```
**Choose option**: 1 (Full research analysis)
**Expected**: Complete analysis with results

### Test 5: Full Automation Test
```bash
uv run python automation_master.py
```
**Choose option**: 1 (Run analysis now)
**Expected**: Complete pipeline with email report

### Test 6: Docker Test (Optional)
```bash
# Windows PowerShell
.\test-docker.ps1

# Linux/macOS  
./test-docker.sh
```
**Expected**: All Docker tests pass ✅

## ✅ Success Criteria

### What You Should See:

1. **✅ Environment Setup**
   - All dependencies working
   - API key recognized
   - Email configuration valid

2. **✅ Analysis Results**
   - Episodes analyzed: 100-200+
   - Categories detected: 8+ research domains
   - Recommendations generated: 8-12 actionable items
   - Processing time: 3-5 minutes

3. **✅ Email Reports**
   - Professional HTML email received
   - JSON and Markdown attachments
   - Executive summary with key insights

4. **✅ File Organization**
   ```
   research_results/
   ├── daily_reports/2025-01-08/
   │   ├── daily_analysis_20250108_XXXX.json
   │   ├── daily_analysis_20250108_XXXX_summary.md
   │   └── daily_analysis_20250108_XXXX_metadata.json
   ```

## 🚨 Troubleshooting Common Issues

### Issue: "No API keys found"
**Solution**: 
```bash
# Check your .env file exists and has correct key
Get-Content .env | Select-String "OPENAI_API_KEY"
```

### Issue: "Email authentication failed"  
**Solution**:
- Verify 2FA is enabled on Gmail
- Use App Password, not regular password
- Check EMAIL_SENDER format (must be full email)

### Issue: "Browser installation issues"
**Solution**:
```bash
# Reinstall browser
uv run playwright install chromium --with-deps --force
```

### Issue: "Analysis fails/times out"
**Solution**:
- Check internet connection
- Try with `HEADLESS_MODE=false` to see browser
- Verify Journal Club website is accessible

### Issue: "Permission denied on results folder"
**Solution**:
```bash
# Check/create directory
New-Item -ItemType Directory -Force -Path "research_results"
```

## 📊 Expected Test Results

### Sample Analysis Output:
```
🎯 RESEARCH INTELLIGENCE SUMMARY
============================================================
📊 Episodes Found: 127
📂 Top Categories:
   • AI/ML: 38 episodes
   • Computer Vision: 24 episodes  
   • Robotics: 19 episodes
   • Biotechnology: 16 episodes

🔥 Trending Topics:
   • Multi-Stage Bat Algorithm
   • LS-YOLO for Autonomous Driving
   • Foundation Model for Physics

💡 Top Recommendations:
   1. Investigate computer vision applications for industrial automation
   2. Develop federated learning capabilities for privacy-preserving AI
   3. Research autonomous system applications in agriculture and logistics
```

### Sample Email Report:
- **Subject**: "📊 Daily Research Intelligence Report - 2025-01-08 (127 episodes)"
- **Content**: Professional HTML with charts, categories, recommendations
- **Attachments**: Detailed JSON report + Executive summary PDF

## 🎯 Quick Start Command

**All-in-one test command:**
```bash
# Run the complete system test
uv run python automation_master.py
```
Choose option 1, then wait 3-5 minutes for complete analysis and email delivery.

## 📞 Getting Help

If you encounter issues:

1. **Check Configuration**: `uv run python research_config.py`
2. **View Logs**: Check terminal output for error messages  
3. **Verify Network**: Test internet connection and API access
4. **Test Components**: Run individual test scripts to isolate issues

---

**Ready to test? Start with updating your .env file with the required API keys and email settings!** 🚀
