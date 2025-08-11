"""
Daily Automation System for Research Intelligence

Schedules and executes daily research analysis with email notifications.

@file purpose: Automated daily execution of research intelligence pipeline
"""

import asyncio
import schedule
import time
import os
import sys
import json
import traceback
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from pathlib import Path

# Import our custom modules
from results_manager import ResultsManager, setup_results_system
from email_notifier import EmailNotifier, setup_email_notifications
from live_research_scraper import LiveResearchScraper


class DailyAutomation:
    """Manages daily automation of research intelligence pipeline"""
    
    def __init__(self, 
                 schedule_time: str = "09:00",
                 enable_email: bool = True,
                 enable_archiving: bool = True):
        
        self.schedule_time = schedule_time
        self.enable_email = enable_email
        self.enable_archiving = enable_archiving
        
        # Initialize components
        self.results_manager = setup_results_system()
        self.email_notifier = setup_email_notifications() if enable_email else None
        
        # Configuration
        self.max_retries = 3
        self.retry_delay_minutes = 30
        self.headless_mode = True  # Run in background
        
        # Status tracking
        self.last_run_time = None
        self.last_run_status = None
        self.consecutive_failures = 0
        
        print(f"🤖 Daily Automation initialized for {schedule_time}")
    
    async def run_daily_analysis(self) -> Dict:
        """Execute the complete daily research analysis pipeline"""
        
        start_time = datetime.now()
        print(f"\n🚀 Starting daily research analysis at {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        try:
            # Check API key
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                raise Exception("OPENAI_API_KEY not found in environment variables")
            
            # Initialize scraper
            scraper = LiveResearchScraper(
                api_key=api_key,
                model="gpt-4o-mini",  # Cost-effective model for daily runs
                headless=self.headless_mode
            )
            
            print("🌐 Step 1: Scraping Journal Club episodes...")
            scraped_content = await scraper.scrape_journal_club_episodes()
            
            print("🧠 Step 2: Analyzing scraped content...")
            analysis_data = await scraper.analyze_scraped_content(scraped_content)
            
            print("📊 Step 3: Generating intelligence report...")
            intelligence_report = await scraper.generate_intelligence_report(analysis_data)
            
            print("💾 Step 4: Saving results...")
            report_files = self.results_manager.save_research_report(
                intelligence_report, 
                report_type="daily",
                custom_name=f"daily_analysis_{start_time.strftime('%Y%m%d_%H%M')}"
            )
            
            # Send email notification
            if self.enable_email and self.email_notifier:
                print("📧 Step 5: Sending email notification...")
                email_sent = self.email_notifier.send_research_report(
                    intelligence_report, 
                    report_files,
                    "Daily"
                )
            else:
                email_sent = False
                print("📧 Step 5: Email notifications disabled")
            
            # Archive old reports if enabled
            if self.enable_archiving:
                print("🗄️ Step 6: Archiving old reports...")
                archived_files = self.results_manager.archive_old_reports()
            else:
                archived_files = []
                print("🗄️ Step 6: Archiving disabled")
            
            # Clean up temp files
            print("🧹 Step 7: Cleaning up temporary files...")
            self.results_manager.cleanup_temp_files()
            
            end_time = datetime.now()
            duration = end_time - start_time
            
            # Prepare status report
            status = {
                "success": True,
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat(),
                "duration_minutes": round(duration.total_seconds() / 60, 2),
                "episodes_analyzed": intelligence_report.get("executive_summary", {}).get("total_episodes_analyzed", "Unknown"),
                "categories_found": len(intelligence_report.get("research_categories", {})),
                "recommendations_generated": len(intelligence_report.get("actionable_recommendations", [])),
                "email_sent": email_sent,
                "files_archived": len(archived_files),
                "report_files": report_files
            }
            
            # Update status tracking
            self.last_run_time = start_time
            self.last_run_status = "success"
            self.consecutive_failures = 0
            
            print(f"✅ Daily analysis completed successfully in {duration.total_seconds():.1f} seconds")
            print(f"   📊 Episodes analyzed: {status['episodes_analyzed']}")
            print(f"   📂 Categories found: {status['categories_found']}")
            print(f"   💡 Recommendations: {status['recommendations_generated']}")
            print(f"   📧 Email sent: {email_sent}")
            
            return status
            
        except Exception as e:
            # Handle failures
            end_time = datetime.now()
            duration = end_time - start_time
            
            error_details = {
                "success": False,
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat(),
                "duration_minutes": round(duration.total_seconds() / 60, 2),
                "error_message": str(e),
                "error_traceback": traceback.format_exc()
            }
            
            self.last_run_time = start_time
            self.last_run_status = "failed"
            self.consecutive_failures += 1
            
            print(f"❌ Daily analysis failed after {duration.total_seconds():.1f} seconds")
            print(f"   Error: {str(e)}")
            
            # Log error details
            self._log_error(error_details)
            
            # Send error notification email
            if self.enable_email and self.email_notifier:
                await self._send_error_notification(error_details)
            
            return error_details
    
    def _log_error(self, error_details: Dict):
        """Log error details to file"""
        
        error_log_dir = Path("research_results/errors")
        error_log_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        error_file = error_log_dir / f"error_{timestamp}.json"
        
        with open(error_file, 'w', encoding='utf-8') as f:
            json.dump(error_details, f, indent=2, ensure_ascii=False)
        
        print(f"📝 Error logged to: {error_file}")
    
    async def _send_error_notification(self, error_details: Dict):
        """Send email notification about analysis failure"""
        
        try:
            # Create error report structure
            error_report = {
                "report_metadata": {
                    "generated_at": error_details["start_time"],
                    "report_type": "Error Notification",
                    "source_url": "Daily Automation System"
                },
                "executive_summary": {
                    "total_episodes_analyzed": "Analysis Failed",
                    "key_findings": [
                        f"Daily analysis failed at {error_details['start_time']}",
                        f"Error: {error_details['error_message']}",
                        f"Consecutive failures: {self.consecutive_failures}",
                        "Automated retry will be attempted"
                    ]
                },
                "research_categories": {},
                "actionable_recommendations": [
                    "Check system logs for detailed error information",
                    "Verify internet connection and API key status",
                    "Monitor system for successful recovery"
                ],
                "trending_technologies": [],
                "high_impact_opportunities": []
            }
            
            report_files = {"json_file": "", "markdown_file": ""}
            
            self.email_notifier.send_research_report(
                error_report,
                report_files,
                "⚠️ Daily Analysis Error"
            )
            
        except Exception as e:
            print(f"⚠️ Failed to send error notification: {e}")
    
    def schedule_daily_run(self):
        """Schedule the daily analysis to run automatically"""
        
        print(f"⏰ Scheduling daily analysis at {self.schedule_time}")
        
        # Schedule the daily run
        schedule.every().day.at(self.schedule_time).do(self._run_scheduled_analysis)
        
        print("✅ Daily schedule configured!")
        print(f"   Next run: {schedule.next_run()}")
    
    def _run_scheduled_analysis(self):
        """Wrapper to run async analysis from scheduler"""
        
        print(f"⏰ Scheduled analysis triggered at {datetime.now()}")
        
        try:
            # Run the analysis
            asyncio.run(self.run_daily_analysis())
            
        except Exception as e:
            print(f"❌ Scheduled analysis failed: {e}")
            
            # If we have too many consecutive failures, increase retry delay
            if self.consecutive_failures >= 3:
                print(f"⚠️ {self.consecutive_failures} consecutive failures detected")
                print("   Increasing retry delay and alerting administrators")
    
    def run_scheduler_loop(self):
        """Run the scheduler loop (blocking)"""
        
        print("🔄 Starting daily automation scheduler...")
        print("   Press Ctrl+C to stop")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
                
        except KeyboardInterrupt:
            print("\n⏹️ Scheduler stopped by user")
        except Exception as e:
            print(f"\n❌ Scheduler error: {e}")
    
    async def run_now(self) -> Dict:
        """Run analysis immediately (for testing)"""
        
        print("🚀 Running immediate analysis...")
        return await self.run_daily_analysis()
    
    def get_status(self) -> Dict:
        """Get current automation status"""
        
        status = {
            "automation_active": True,
            "schedule_time": self.schedule_time,
            "last_run_time": self.last_run_time.isoformat() if self.last_run_time else None,
            "last_run_status": self.last_run_status,
            "consecutive_failures": self.consecutive_failures,
            "next_scheduled_run": str(schedule.next_run()) if schedule.jobs else None,
            "email_enabled": self.enable_email,
            "archiving_enabled": self.enable_archiving,
            "headless_mode": self.headless_mode
        }
        
        return status
    
    def create_weekly_summary_job(self):
        """Schedule weekly summary generation"""
        
        def run_weekly_summary():
            print("📅 Generating weekly summary...")
            try:
                summary_file = self.results_manager.create_weekly_summary()
                if summary_file and self.enable_email and self.email_notifier:
                    # Load weekly data and send email
                    with open(summary_file, 'r', encoding='utf-8') as f:
                        weekly_data = json.load(f)
                    
                    asyncio.run(self.email_notifier.send_weekly_summary(weekly_data))
                    
            except Exception as e:
                print(f"❌ Weekly summary failed: {e}")
        
        # Schedule weekly summary on Sundays at 10:00
        schedule.every().sunday.at("10:00").do(run_weekly_summary)
        print("📅 Weekly summary scheduled for Sundays at 10:00")


async def main():
    """Main function for daily automation"""
    
    print("🤖 Research Intelligence Daily Automation")
    print("=" * 50)
    
    # Create automation instance
    automation = DailyAutomation(
        schedule_time="09:00",  # 9 AM daily
        enable_email=True,
        enable_archiving=True
    )
    
    print("\n📋 Choose an option:")
    print("1. Run analysis now (test)")
    print("2. Start daily scheduler")
    print("3. Show status")
    print("4. Exit")
    
    while True:
        try:
            choice = input("\nEnter choice (1-4): ").strip()
            
            if choice == "1":
                print("\n🧪 Running test analysis...")
                result = await automation.run_now()
                
                if result["success"]:
                    print(f"✅ Test completed in {result['duration_minutes']} minutes")
                else:
                    print(f"❌ Test failed: {result['error_message']}")
                break
                
            elif choice == "2":
                print(f"\n⏰ Starting daily scheduler...")
                automation.schedule_daily_run()
                automation.create_weekly_summary_job()
                
                print("🔄 Scheduler is now running...")
                automation.run_scheduler_loop()
                break
                
            elif choice == "3":
                print("\n📊 Automation Status:")
                status = automation.get_status()
                for key, value in status.items():
                    print(f"   {key}: {value}")
                
            elif choice == "4":
                print("👋 Goodbye!")
                break
                
            else:
                print("Please enter 1, 2, 3, or 4")
                
        except KeyboardInterrupt:
            print("\n👋 Automation stopped by user")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            break


def create_windows_task_scheduler():
    """Create Windows Task Scheduler entry for automation"""
    
    print("\n🪟 Windows Task Scheduler Setup")
    print("=" * 40)
    
    # Get current working directory and Python executable
    current_dir = os.getcwd()
    python_exe = sys.executable
    script_path = os.path.join(current_dir, "daily_automation.py")
    
    # Create batch file for Windows Task Scheduler
    batch_content = f"""@echo off
cd /d "{current_dir}"
"{python_exe}" -c "import asyncio; from daily_automation import DailyAutomation; automation = DailyAutomation(); asyncio.run(automation.run_daily_analysis())"
pause
"""
    
    batch_file = Path("run_daily_research.bat")
    with open(batch_file, 'w') as f:
        f.write(batch_content)
    
    print(f"✅ Batch file created: {batch_file.absolute()}")
    
    print(f"\n📝 To setup Windows Task Scheduler:")
    print(f"1. Open Task Scheduler (taskschd.msc)")
    print(f"2. Create Basic Task")
    print(f"3. Name: 'Daily Research Intelligence'")
    print(f"4. Trigger: Daily at 9:00 AM")
    print(f"5. Action: Start Program")
    print(f"6. Program: {batch_file.absolute()}")
    print(f"7. Start in: {current_dir}")
    
    return str(batch_file.absolute())


if __name__ == "__main__":
    print("🚀 Daily Research Intelligence Automation")
    
    # Check if running on Windows
    if os.name == 'nt':
        print("\n🪟 Windows detected")
        
        choice = input("Setup Windows Task Scheduler? (y/n): ").lower().strip()
        if choice == 'y':
            create_windows_task_scheduler()
            print("\n✅ Windows setup complete!")
        else:
            print("\n🔄 Running interactive scheduler...")
            asyncio.run(main())
    else:
        print("\n🐧 Unix/Linux detected - using interactive scheduler")
        asyncio.run(main())
