"""
Master Automation Controller for Research Intelligence System

Complete automation pipeline integrating scraping, analysis, results management, and notifications.

@file purpose: Master controller for complete research intelligence automation
"""

import asyncio
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

# Import all our components
from results_manager import ResultsManager, setup_results_system
from email_notifier import EmailNotifier, setup_email_notifications  
from daily_automation import DailyAutomation
from live_research_scraper import LiveResearchScraper
from research_config import check_environment_setup, get_research_config


class AutomationMaster:
    """Master controller for the complete research intelligence automation system"""
    
    def __init__(self):
        self.results_manager = None
        self.email_notifier = None
        self.automation = None
        self.config = None
        
        print("🤖 Initializing Research Intelligence Automation Master...")
    
    def setup_complete_system(self) -> bool:
        """Setup the complete automation system"""
        
        print("\n🚀 Setting up complete automation system...")
        
        # 1. Check environment
        print("1️⃣ Checking environment setup...")
        if not check_environment_setup():
            return False
        
        # 2. Setup results management
        print("2️⃣ Setting up results management...")
        self.results_manager = setup_results_system()
        
        # 3. Setup email notifications
        print("3️⃣ Setting up email notifications...")
        self.email_notifier = setup_email_notifications()
        
        # 4. Setup daily automation
        print("4️⃣ Setting up daily automation...")
        schedule_time = os.getenv('DAILY_ANALYSIS_TIME', '09:00')
        enable_email = os.getenv('ENABLE_EMAIL_REPORTS', 'true').lower() == 'true'
        enable_archiving = os.getenv('ENABLE_ARCHIVING', 'true').lower() == 'true'
        
        self.automation = DailyAutomation(
            schedule_time=schedule_time,
            enable_email=enable_email,
            enable_archiving=enable_archiving
        )
        
        print("✅ Complete system setup successful!")
        return True
    
    async def run_full_analysis_pipeline(self) -> Dict:
        """Run the complete analysis pipeline once"""
        
        print("\n🔬 Executing Full Research Intelligence Pipeline")
        print("=" * 55)
        
        start_time = datetime.now()
        
        try:
            # Run the automation pipeline
            result = await self.automation.run_daily_analysis()
            
            # Show detailed results
            if result["success"]:
                print(f"\n🎉 Pipeline completed successfully!")
                print(f"📊 Results Summary:")
                print(f"   • Episodes analyzed: {result['episodes_analyzed']}")
                print(f"   • Categories found: {result['categories_found']}")
                print(f"   • Recommendations: {result['recommendations_generated']}")
                print(f"   • Duration: {result['duration_minutes']} minutes")
                print(f"   • Email sent: {result['email_sent']}")
                print(f"   • Files archived: {result['files_archived']}")
                
                # Show file locations
                print(f"\n📁 Generated Files:")
                for file_type, file_path in result['report_files'].items():
                    if file_path:
                        print(f"   • {file_type}: {file_path}")
            
            else:
                print(f"\n❌ Pipeline failed:")
                print(f"   Error: {result['error_message']}")
            
            return result
            
        except Exception as e:
            print(f"\n❌ Pipeline execution failed: {e}")
            return {"success": False, "error": str(e)}
    
    def start_daily_automation(self):
        """Start the daily automation scheduler"""
        
        print("\n⏰ Starting Daily Automation Scheduler")
        print("=" * 42)
        
        if not self.automation:
            print("❌ Automation not initialized. Run setup first.")
            return
        
        try:
            # Setup daily and weekly schedules
            self.automation.schedule_daily_run()
            self.automation.create_weekly_summary_job()
            
            # Show schedule info
            status = self.automation.get_status()
            print(f"📅 Schedule configured:")
            print(f"   • Daily analysis: {status['schedule_time']}")
            print(f"   • Weekly summary: Sundays at 10:00")
            print(f"   • Email notifications: {status['email_enabled']}")
            print(f"   • Auto-archiving: {status['archiving_enabled']}")
            
            print(f"\n🔄 Scheduler running... Press Ctrl+C to stop")
            
            # Run the scheduler loop
            self.automation.run_scheduler_loop()
            
        except KeyboardInterrupt:
            print("\n⏹️ Daily automation stopped by user")
        except Exception as e:
            print(f"\n❌ Automation error: {e}")
    
    def setup_windows_automation(self) -> str:
        """Setup Windows Task Scheduler automation"""
        
        print("\n🪟 Setting up Windows Task Scheduler")
        print("=" * 40)
        
        # Create PowerShell script for better Windows integration
        current_dir = Path.cwd()
        script_content = f'''# Research Intelligence Automation PowerShell Script
Set-Location "{current_dir}"

# Activate virtual environment if it exists
if (Test-Path ".venv\\Scripts\\Activate.ps1") {{
    .venv\\Scripts\\Activate.ps1
}}

# Run the daily analysis
python -c "import asyncio; from automation_master import AutomationMaster; master = AutomationMaster(); master.setup_complete_system(); asyncio.run(master.run_full_analysis_pipeline())"

# Keep window open on error
if ($LASTEXITCODE -ne 0) {{
    Write-Host "Analysis failed. Press any key to exit..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}}
'''
        
        ps_script = current_dir / "run_research_intelligence.ps1"
        with open(ps_script, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        # Also create batch file as backup
        batch_content = f'''@echo off
cd /d "{current_dir}"
powershell -ExecutionPolicy Bypass -File "{ps_script}"
'''
        
        batch_file = current_dir / "run_research_intelligence.bat"
        with open(batch_file, 'w') as f:
            f.write(batch_content)
        
        print(f"✅ Windows automation files created:")
        print(f"   • PowerShell: {ps_script}")
        print(f"   • Batch file: {batch_file}")
        
        print(f"\n📝 Windows Task Scheduler Setup:")
        print(f"1. Open Task Scheduler (Win+R → taskschd.msc)")
        print(f"2. Create Basic Task...")
        print(f"3. Name: 'Research Intelligence Daily Analysis'")
        print(f"4. Trigger: Daily")
        print(f"5. Time: {os.getenv('DAILY_ANALYSIS_TIME', '09:00')}")
        print(f"6. Action: Start a program")
        print(f"7. Program: {batch_file}")
        print(f"8. Start in: {current_dir}")
        print(f"9. ✅ Finish")
        
        return str(batch_file)
    
    def create_linux_cron_job(self) -> str:
        """Create Linux cron job for automation"""
        
        print("\n🐧 Setting up Linux Cron Job")
        print("=" * 35)
        
        current_dir = Path.cwd()
        python_path = sys.executable
        
        # Create shell script
        shell_script = current_dir / "run_research_intelligence.sh"
        script_content = f'''#!/bin/bash
cd "{current_dir}"

# Activate virtual environment if it exists
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
fi

# Run the analysis
{python_path} -c "import asyncio; from automation_master import AutomationMaster; master = AutomationMaster(); master.setup_complete_system(); asyncio.run(master.run_full_analysis_pipeline())"
'''
        
        with open(shell_script, 'w') as f:
            f.write(script_content)
        
        # Make executable
        os.chmod(shell_script, 0o755)
        
        # Generate cron job command
        schedule_time = os.getenv('DAILY_ANALYSIS_TIME', '09:00')
        hour, minute = schedule_time.split(':')
        cron_command = f"{minute} {hour} * * * {shell_script} >> {current_dir}/research_intelligence.log 2>&1"
        
        print(f"✅ Shell script created: {shell_script}")
        print(f"\n📝 Cron Job Setup:")
        print(f"1. Run: crontab -e")
        print(f"2. Add this line:")
        print(f"   {cron_command}")
        print(f"3. Save and exit")
        print(f"4. Verify with: crontab -l")
        
        return cron_command
    
    def show_system_status(self) -> Dict:
        """Show complete system status"""
        
        print("\n📊 System Status Report")
        print("=" * 30)
        
        status = {}
        
        # Results manager status
        if self.results_manager:
            results_summary = self.results_manager.get_results_summary()
            status["results"] = results_summary
            
            print(f"📁 Results Management:")
            print(f"   • Base directory: {results_summary['directories']['base']}")
            print(f"   • Daily reports: {results_summary['directories']['daily_reports']}")
            print(f"   • Weekly summaries: {results_summary['directories']['weekly_summaries']}")
            print(f"   • Disk usage: {results_summary['disk_usage']['total_size_mb']} MB")
        
        # Email notifier status  
        if self.email_notifier:
            email_configured = bool(self.email_notifier.config.sender_email and 
                                  self.email_notifier.config.recipient_emails)
            status["email"] = {
                "configured": email_configured,
                "sender": self.email_notifier.config.sender_email,
                "recipients": len(self.email_notifier.config.recipient_emails)
            }
            
            print(f"\n📧 Email Notifications:")
            print(f"   • Configured: {email_configured}")
            print(f"   • Sender: {self.email_notifier.config.sender_email}")
            print(f"   • Recipients: {len(self.email_notifier.config.recipient_emails)}")
        
        # Automation status
        if self.automation:
            auto_status = self.automation.get_status()
            status["automation"] = auto_status
            
            print(f"\n🤖 Automation:")
            print(f"   • Schedule time: {auto_status['schedule_time']}")
            print(f"   • Last run: {auto_status['last_run_time'] or 'Never'}")
            print(f"   • Last status: {auto_status['last_run_status'] or 'None'}")
            print(f"   • Consecutive failures: {auto_status['consecutive_failures']}")
        
        return status
    
    async def test_complete_system(self) -> bool:
        """Test all system components"""
        
        print("\n🧪 Testing Complete System")
        print("=" * 32)
        
        tests_passed = 0
        total_tests = 4
        
        # Test 1: Results manager
        print("1️⃣ Testing results manager...")
        try:
            test_data = {"test": "data", "timestamp": datetime.now().isoformat()}
            test_files = self.results_manager.save_research_report(
                test_data, "test", "system_test"
            )
            print("   ✅ Results manager working")
            tests_passed += 1
        except Exception as e:
            print(f"   ❌ Results manager failed: {e}")
        
        # Test 2: Email notifications (if configured)
        print("2️⃣ Testing email notifications...")
        if self.email_notifier and self.email_notifier._validate_config():
            try:
                if await asyncio.to_thread(self.email_notifier.send_test_email):
                    print("   ✅ Email notifications working")
                    tests_passed += 1
                else:
                    print("   ❌ Email test failed")
            except Exception as e:
                print(f"   ❌ Email error: {e}")
        else:
            print("   ⚠️ Email not configured, skipping test")
            tests_passed += 0.5  # Partial credit
        
        # Test 3: Environment configuration
        print("3️⃣ Testing environment...")
        if check_environment_setup():
            print("   ✅ Environment configured correctly")
            tests_passed += 1
        else:
            print("   ❌ Environment issues detected")
        
        # Test 4: File structure
        print("4️⃣ Testing file structure...")
        try:
            required_files = [
                "results_manager.py", "email_notifier.py", 
                "daily_automation.py", "live_research_scraper.py"
            ]
            
            for file_name in required_files:
                if not Path(file_name).exists():
                    raise FileNotFoundError(f"Missing {file_name}")
            
            print("   ✅ All required files present")
            tests_passed += 1
            
        except Exception as e:
            print(f"   ❌ File structure issue: {e}")
        
        success_rate = (tests_passed / total_tests) * 100
        
        print(f"\n📊 Test Results: {tests_passed}/{total_tests} tests passed ({success_rate:.1f}%)")
        
        if success_rate >= 75:
            print("✅ System ready for production use!")
            return True
        else:
            print("⚠️ System needs attention before production use")
            return False


async def main():
    """Main interactive menu for automation master"""
    
    print("🤖 Research Intelligence Automation Master")
    print("=" * 45)
    
    master = AutomationMaster()
    
    # Setup system first
    if not master.setup_complete_system():
        print("❌ System setup failed. Please check configuration.")
        return
    
    while True:
        print(f"\n📋 Choose an option:")
        print(f"1. Run analysis now (test)")
        print(f"2. Start daily automation")
        print(f"3. Setup Windows Task Scheduler")
        print(f"4. Setup Linux Cron Job") 
        print(f"5. Show system status")
        print(f"6. Test complete system")
        print(f"7. Exit")
        
        try:
            choice = input("\nEnter choice (1-7): ").strip()
            
            if choice == "1":
                result = await master.run_full_analysis_pipeline()
                
            elif choice == "2":
                master.start_daily_automation()
                
            elif choice == "3":
                if os.name == 'nt':
                    master.setup_windows_automation()
                else:
                    print("❌ Windows Task Scheduler only available on Windows")
                
            elif choice == "4":
                if os.name != 'nt':
                    master.create_linux_cron_job()
                else:
                    print("❌ Cron jobs only available on Linux/Unix")
                
            elif choice == "5":
                master.show_system_status()
                
            elif choice == "6":
                success = await master.test_complete_system()
                
            elif choice == "7":
                print("👋 Goodbye!")
                break
                
            else:
                print("Please enter 1-7")
                
        except KeyboardInterrupt:
            print("\n👋 Automation master stopped by user")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            continue


if __name__ == "__main__":
    asyncio.run(main())
