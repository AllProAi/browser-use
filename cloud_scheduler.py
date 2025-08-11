"""
Cloud Scheduler for Research Intelligence System

Container-friendly scheduler that works in cloud environments without cron/task scheduler.

@file purpose: Cloud-native scheduling for containerized research intelligence
"""

import asyncio
import os
import signal
import sys
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional
import logging

# Import our automation components
from automation_master import AutomationMaster
from research_config import check_environment_setup


class CloudScheduler:
    """Cloud-native scheduler for research intelligence automation"""
    
    def __init__(self):
        self.master = AutomationMaster()
        self.running = True
        self.last_run_time = None
        self.next_run_time = None
        
        # Configuration from environment variables
        self.schedule_time = os.getenv('DAILY_ANALYSIS_TIME', '09:00')
        self.timezone_str = os.getenv('TIMEZONE', 'UTC')
        self.run_on_startup = os.getenv('RUN_ON_STARTUP', 'false').lower() == 'true'
        self.health_check_port = int(os.getenv('HEALTH_CHECK_PORT', '8080'))
        
        # Setup logging
        self.setup_logging()
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGTERM, self.signal_handler)
        signal.signal(signal.SIGINT, self.signal_handler)
        
        self.logger.info(f"🤖 Cloud Scheduler initialized")
        self.logger.info(f"   Schedule: Daily at {self.schedule_time} {self.timezone_str}")
        self.logger.info(f"   Run on startup: {self.run_on_startup}")
    
    def setup_logging(self):
        """Setup logging for cloud environments"""
        
        # Create logs directory
        log_dir = Path("/app/logs")
        log_dir.mkdir(exist_ok=True)
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(sys.stdout),  # For container logs
                logging.FileHandler(log_dir / "scheduler.log"),  # For persistent logs
            ]
        )
        
        self.logger = logging.getLogger('CloudScheduler')
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        self.logger.info(f"🛑 Received signal {signum}, shutting down gracefully...")
        self.running = False
    
    def calculate_next_run_time(self) -> datetime:
        """Calculate the next run time based on schedule"""
        
        now = datetime.now(timezone.utc)
        hour, minute = map(int, self.schedule_time.split(':'))
        
        # Calculate next run time
        next_run = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        
        # If the time has already passed today, schedule for tomorrow
        if next_run <= now:
            next_run += timedelta(days=1)
        
        return next_run
    
    async def run_analysis_pipeline(self) -> dict:
        """Run the complete research intelligence pipeline"""
        
        self.logger.info("🚀 Starting research intelligence analysis...")
        
        try:
            # Setup the system
            if not self.master.setup_complete_system():
                raise Exception("System setup failed")
            
            # Run the analysis
            result = await self.master.run_full_analysis_pipeline()
            
            self.last_run_time = datetime.now(timezone.utc)
            
            if result.get('success'):
                self.logger.info("✅ Analysis completed successfully")
                self.logger.info(f"   Episodes: {result.get('episodes_analyzed', 'Unknown')}")
                self.logger.info(f"   Duration: {result.get('duration_minutes', 0):.1f} minutes")
                self.logger.info(f"   Email sent: {result.get('email_sent', False)}")
            else:
                self.logger.error(f"❌ Analysis failed: {result.get('error_message', 'Unknown error')}")
            
            return result
            
        except Exception as e:
            self.logger.error(f"❌ Pipeline execution failed: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def save_status(self, status: dict):
        """Save scheduler status to file for monitoring"""
        
        status_file = Path("/app/logs/scheduler_status.json")
        
        try:
            with open(status_file, 'w') as f:
                json.dump(status, f, indent=2, default=str)
        except Exception as e:
            self.logger.error(f"Failed to save status: {e}")
    
    def get_status(self) -> dict:
        """Get current scheduler status"""
        
        status = {
            "running": self.running,
            "last_run_time": self.last_run_time.isoformat() if self.last_run_time else None,
            "next_run_time": self.next_run_time.isoformat() if self.next_run_time else None,
            "schedule_time": self.schedule_time,
            "timezone": self.timezone_str,
            "container_info": {
                "hostname": os.getenv('HOSTNAME', 'unknown'),
                "pod_name": os.getenv('POD_NAME', 'unknown'),
                "node_name": os.getenv('NODE_NAME', 'unknown')
            },
            "environment": {
                "openai_configured": bool(os.getenv('OPENAI_API_KEY')),
                "email_configured": bool(os.getenv('EMAIL_SENDER')),
                "recipients_configured": bool(os.getenv('EMAIL_RECIPIENTS'))
            }
        }
        
        return status
    
    async def health_check_server(self):
        """Simple health check HTTP server for container orchestration"""
        
        try:
            from http.server import HTTPServer, BaseHTTPRequestHandler
            import threading
            
            class HealthHandler(BaseHTTPRequestHandler):
                def do_GET(self):
                    if self.path == '/health':
                        status = self.server.scheduler.get_status()
                        self.send_response(200)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        self.wfile.write(json.dumps(status, default=str).encode())
                    elif self.path == '/ready':
                        # Kubernetes readiness probe
                        self.send_response(200)
                        self.send_header('Content-type', 'text/plain')
                        self.end_headers()
                        self.wfile.write(b'ready')
                    else:
                        self.send_response(404)
                        self.end_headers()
                
                def log_message(self, format, *args):
                    # Suppress default HTTP logging
                    pass
            
            server = HTTPServer(('', self.health_check_port), HealthHandler)
            server.scheduler = self  # Pass scheduler instance to handler
            
            def run_server():
                self.logger.info(f"🏥 Health check server running on port {self.health_check_port}")
                server.serve_forever()
            
            thread = threading.Thread(target=run_server, daemon=True)
            thread.start()
            
        except Exception as e:
            self.logger.warning(f"Failed to start health check server: {e}")
    
    async def run_scheduler_loop(self):
        """Main scheduler loop for cloud environments"""
        
        self.logger.info("🔄 Starting cloud scheduler loop...")
        
        # Start health check server
        await self.health_check_server()
        
        # Run analysis immediately on startup if configured
        if self.run_on_startup:
            self.logger.info("🚀 Running analysis on startup...")
            await self.run_analysis_pipeline()
        
        # Main scheduling loop
        while self.running:
            try:
                # Calculate next run time
                self.next_run_time = self.calculate_next_run_time()
                
                self.logger.info(f"⏰ Next analysis scheduled for: {self.next_run_time.isoformat()}")
                
                # Update status
                status = self.get_status()
                self.save_status(status)
                
                # Wait until next run time
                while self.running and datetime.now(timezone.utc) < self.next_run_time:
                    await asyncio.sleep(60)  # Check every minute
                
                # Run analysis if still running
                if self.running:
                    result = await self.run_analysis_pipeline()
                    
                    # Update status with result
                    status = self.get_status()
                    status['last_result'] = result
                    self.save_status(status)
                
            except Exception as e:
                self.logger.error(f"❌ Scheduler error: {str(e)}")
                # Wait 5 minutes before retrying on error
                await asyncio.sleep(300)
        
        self.logger.info("🛑 Scheduler stopped")
    
    async def run_once_and_exit(self):
        """Run analysis once and exit (useful for job-based deployments)"""
        
        self.logger.info("🎯 Running single analysis and exiting...")
        
        result = await self.run_analysis_pipeline()
        
        if result.get('success'):
            self.logger.info("✅ Single run completed successfully")
            sys.exit(0)
        else:
            self.logger.error("❌ Single run failed")
            sys.exit(1)


def print_cloud_deployment_info():
    """Print information about cloud deployment"""
    
    print("🌥️ Research Intelligence Cloud Deployment")
    print("=" * 50)
    print()
    print("📦 Container Information:")
    print(f"   Hostname: {os.getenv('HOSTNAME', 'unknown')}")
    print(f"   Pod Name: {os.getenv('POD_NAME', 'unknown')}")
    print(f"   Node Name: {os.getenv('NODE_NAME', 'unknown')}")
    print()
    print("⚙️ Configuration:")
    print(f"   Schedule: {os.getenv('DAILY_ANALYSIS_TIME', '09:00')} {os.getenv('TIMEZONE', 'UTC')}")
    print(f"   Run on startup: {os.getenv('RUN_ON_STARTUP', 'false')}")
    print(f"   Health check port: {os.getenv('HEALTH_CHECK_PORT', '8080')}")
    print()
    print("🔑 Environment Status:")
    print(f"   OpenAI API: {'✅ Configured' if os.getenv('OPENAI_API_KEY') else '❌ Missing'}")
    print(f"   Email Sender: {'✅ Configured' if os.getenv('EMAIL_SENDER') else '❌ Missing'}")
    print(f"   Email Recipients: {'✅ Configured' if os.getenv('EMAIL_RECIPIENTS') else '❌ Missing'}")
    print()


async def main():
    """Main function for cloud scheduler"""
    
    print_cloud_deployment_info()
    
    # Check environment setup
    if not check_environment_setup():
        print("❌ Environment setup failed. Check configuration.")
        sys.exit(1)
    
    scheduler = CloudScheduler()
    
    # Check for run mode
    run_mode = os.getenv('RUN_MODE', 'scheduler').lower()
    
    if run_mode == 'once':
        # Run once and exit (good for cron jobs or scheduled tasks)
        await scheduler.run_once_and_exit()
    else:
        # Run continuous scheduler (good for long-running containers)
        await scheduler.run_scheduler_loop()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Scheduler interrupted by user")
    except Exception as e:
        print(f"\n❌ Scheduler failed: {e}")
        sys.exit(1)
