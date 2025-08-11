"""
Email Notification System for Research Intelligence Reports

Sends automated email notifications with research reports and summaries.

@file purpose: Automated email notifications for research intelligence system
"""

import os
import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass
from pathlib import Path


@dataclass
class EmailConfig:
    """Email configuration settings"""
    smtp_server: str = "smtp.gmail.com"
    smtp_port: int = 587
    sender_email: str = ""
    sender_password: str = ""  # App password for Gmail
    recipient_emails: List[str] = None
    
    # Email settings
    include_attachments: bool = True
    max_attachment_size_mb: int = 10
    send_daily_reports: bool = True
    send_weekly_summaries: bool = True
    
    def __post_init__(self):
        if self.recipient_emails is None:
            self.recipient_emails = []
        
        # Load from environment variables
        self.sender_email = os.getenv('EMAIL_SENDER', self.sender_email)
        self.sender_password = os.getenv('EMAIL_PASSWORD', self.sender_password)
        
        # Load recipients from environment
        env_recipients = os.getenv('EMAIL_RECIPIENTS', '')
        if env_recipients and not self.recipient_emails:
            self.recipient_emails = [email.strip() for email in env_recipients.split(',')]


class EmailNotifier:
    """Handles email notifications for research intelligence reports"""
    
    def __init__(self, config: Optional[EmailConfig] = None):
        self.config = config or EmailConfig()
        self._validate_config()
    
    def _validate_config(self) -> bool:
        """Validate email configuration"""
        
        if not self.config.sender_email:
            print("⚠️ Warning: No sender email configured")
            print("   Set EMAIL_SENDER in .env file")
            return False
        
        if not self.config.sender_password:
            print("⚠️ Warning: No email password configured")
            print("   Set EMAIL_PASSWORD in .env file (use app password for Gmail)")
            return False
        
        if not self.config.recipient_emails:
            print("⚠️ Warning: No recipient emails configured")
            print("   Set EMAIL_RECIPIENTS in .env file (comma-separated)")
            return False
        
        return True
    
    def send_research_report(self, 
                           report_data: Dict, 
                           report_files: Dict[str, str],
                           report_type: str = "Daily") -> bool:
        """Send research intelligence report via email"""
        
        if not self._validate_config():
            print("❌ Email configuration invalid, skipping email notification")
            return False
        
        try:
            # Create email message
            msg = MIMEMultipart()
            msg['From'] = self.config.sender_email
            msg['To'] = ', '.join(self.config.recipient_emails)
            msg['Subject'] = self._generate_subject(report_data, report_type)
            
            # Create email body
            body = self._generate_email_body(report_data, report_type)
            msg.attach(MIMEText(body, 'html'))
            
            # Add attachments if enabled
            if self.config.include_attachments:
                self._attach_files(msg, report_files)
            
            # Send email
            self._send_email(msg)
            
            print(f"✅ {report_type} research report emailed successfully!")
            print(f"   Recipients: {', '.join(self.config.recipient_emails)}")
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to send email: {str(e)}")
            return False
    
    def _generate_subject(self, report_data: Dict, report_type: str) -> str:
        """Generate email subject line"""
        
        date_str = datetime.now().strftime("%Y-%m-%d")
        
        episodes_count = report_data.get("executive_summary", {}).get("total_episodes_analyzed", "Unknown")
        
        if report_type.lower() == "daily":
            return f"📊 Daily Research Intelligence Report - {date_str} ({episodes_count} episodes)"
        elif report_type.lower() == "weekly":
            return f"📈 Weekly Research Intelligence Summary - {date_str}"
        else:
            return f"🔬 Research Intelligence Report - {report_type} - {date_str}"
    
    def _generate_email_body(self, report_data: Dict, report_type: str) -> str:
        """Generate HTML email body"""
        
        # Extract key data
        metadata = report_data.get("report_metadata", {})
        executive = report_data.get("executive_summary", {})
        categories = report_data.get("research_categories", {})
        recommendations = report_data.get("actionable_recommendations", [])
        trending = report_data.get("trending_technologies", [])
        opportunities = report_data.get("high_impact_opportunities", [])
        
        html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .header {{ background-color: #2c3e50; color: white; padding: 20px; text-align: center; }}
        .section {{ margin: 20px 0; padding: 15px; border-left: 4px solid #3498db; }}
        .highlight {{ background-color: #ecf0f1; padding: 10px; border-radius: 5px; }}
        .metric {{ display: inline-block; margin: 10px; padding: 10px; background-color: #f8f9fa; border-radius: 5px; text-align: center; }}
        .recommendation {{ margin: 10px 0; padding: 10px; background-color: #e8f5e8; border-radius: 5px; }}
        .footer {{ margin-top: 30px; padding: 15px; text-align: center; color: #7f8c8d; font-size: 12px; }}
        ul {{ padding-left: 20px; }}
        li {{ margin: 5px 0; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🔬 Research Intelligence Report</h1>
        <h2>{report_type} Analysis - {datetime.now().strftime("%B %d, %Y")}</h2>
    </div>
    
    <div class="section">
        <h2>📊 Executive Summary</h2>
        <div class="highlight">
            <div class="metric">
                <strong>{executive.get('total_episodes_analyzed', 'Unknown')}</strong><br>
                Episodes Analyzed
            </div>
            <div class="metric">
                <strong>{len(categories)}</strong><br>
                Research Categories
            </div>
            <div class="metric">
                <strong>{len(recommendations)}</strong><br>
                Recommendations
            </div>
        </div>
        
        <h3>Key Findings:</h3>
        <ul>
"""
        
        for finding in executive.get("key_findings", []):
            html_body += f"            <li>{finding}</li>\n"
        
        html_body += """
        </ul>
    </div>
    
    <div class="section">
        <h2>📂 Research Categories</h2>
        <ul>
"""
        
        # Sort categories by count
        sorted_categories = sorted(categories.items(), key=lambda x: x[1] if isinstance(x[1], int) else 0, reverse=True)
        for category, count in sorted_categories[:8]:  # Top 8 categories
            category_name = category.replace('_', ' ').title()
            html_body += f"            <li><strong>{category_name}</strong>: {count} episodes</li>\n"
        
        html_body += """
        </ul>
    </div>
    
    <div class="section">
        <h2>🔥 Trending Technologies</h2>
        <ul>
"""
        
        for tech in trending[:10]:
            html_body += f"            <li>{tech}</li>\n"
        
        html_body += """
        </ul>
    </div>
    
    <div class="section">
        <h2>💡 Top R&D Recommendations</h2>
"""
        
        for i, recommendation in enumerate(recommendations[:8], 1):
            html_body += f"""
        <div class="recommendation">
            <strong>{i}.</strong> {recommendation}
        </div>
"""
        
        html_body += """
    </div>
    
    <div class="section">
        <h2>🚀 High-Impact Opportunities</h2>
        <ul>
"""
        
        for opportunity in opportunities[:5]:
            html_body += f"            <li>{opportunity}</li>\n"
        
        html_body += f"""
        </ul>
    </div>
    
    <div class="footer">
        <p>Generated by Research Intelligence Agent on {metadata.get('generated_at', datetime.now().isoformat())}</p>
        <p>Source: <a href="{metadata.get('source_url', 'https://journalclub.io/episodes')}">Journal Club Episodes</a></p>
        <p>This report was automatically generated using browser-use automation and AI analysis.</p>
    </div>
</body>
</html>
"""
        
        return html_body
    
    def _attach_files(self, msg: MIMEMultipart, report_files: Dict[str, str]):
        """Attach report files to email"""
        
        files_to_attach = []
        
        # Add JSON report
        if "json_file" in report_files:
            json_path = Path(report_files["json_file"])
            if json_path.exists() and self._check_file_size(json_path):
                files_to_attach.append(("JSON Report", json_path))
        
        # Add Markdown summary
        if "markdown_file" in report_files:
            md_path = Path(report_files["markdown_file"])
            if md_path.exists() and self._check_file_size(md_path):
                files_to_attach.append(("Summary Report", md_path))
        
        # Attach files
        for description, file_path in files_to_attach:
            try:
                with open(file_path, "rb") as attachment:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())
                
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename= {file_path.name}'
                )
                
                msg.attach(part)
                print(f"📎 Attached: {file_path.name}")
                
            except Exception as e:
                print(f"⚠️ Failed to attach {file_path}: {e}")
    
    def _check_file_size(self, file_path: Path) -> bool:
        """Check if file size is within limits"""
        
        size_mb = file_path.stat().st_size / (1024 * 1024)
        
        if size_mb > self.config.max_attachment_size_mb:
            print(f"⚠️ File {file_path.name} too large ({size_mb:.1f}MB), skipping attachment")
            return False
        
        return True
    
    def _send_email(self, msg: MIMEMultipart):
        """Send the email message"""
        
        # Create SMTP session
        server = smtplib.SMTP(self.config.smtp_server, self.config.smtp_port)
        server.starttls()  # Enable security
        server.login(self.config.sender_email, self.config.sender_password)
        
        # Send email
        text = msg.as_string()
        server.sendmail(self.config.sender_email, self.config.recipient_emails, text)
        server.quit()
    
    def send_test_email(self) -> bool:
        """Send a test email to verify configuration"""
        
        if not self._validate_config():
            return False
        
        try:
            # Create simple test message
            msg = MIMEMultipart()
            msg['From'] = self.config.sender_email
            msg['To'] = ', '.join(self.config.recipient_emails)
            msg['Subject'] = "🧪 Research Intelligence System - Test Email"
            
            body = """
            <html>
            <body>
                <h2>✅ Email Notification Test Successful!</h2>
                <p>This is a test email from your Research Intelligence System.</p>
                <p>If you received this email, your email notifications are configured correctly.</p>
                <p><strong>Configuration:</strong></p>
                <ul>
                    <li>SMTP Server: """ + self.config.smtp_server + """</li>
                    <li>Sender: """ + self.config.sender_email + """</li>
                    <li>Recipients: """ + ', '.join(self.config.recipient_emails) + """</li>
                </ul>
                <p>You can now expect to receive automated research intelligence reports!</p>
                <hr>
                <p><small>Generated by Research Intelligence Agent</small></p>
            </body>
            </html>
            """
            
            msg.attach(MIMEText(body, 'html'))
            
            self._send_email(msg)
            
            print("✅ Test email sent successfully!")
            print(f"   Recipients: {', '.join(self.config.recipient_emails)}")
            
            return True
            
        except Exception as e:
            print(f"❌ Test email failed: {str(e)}")
            print("\n💡 Troubleshooting tips:")
            print("   • For Gmail, use an App Password instead of your regular password")
            print("   • Enable 2-factor authentication and generate an App Password")
            print("   • Check that EMAIL_SENDER, EMAIL_PASSWORD, and EMAIL_RECIPIENTS are set in .env")
            return False
    
    def send_weekly_summary(self, weekly_data: Dict) -> bool:
        """Send weekly summary email"""
        
        if not self._validate_config():
            return False
        
        # Format weekly data as a report-like structure
        summary_report = {
            "report_metadata": {
                "generated_at": datetime.now().isoformat(),
                "report_type": "Weekly Summary",
                "source_url": "https://journalclub.io/episodes"
            },
            "executive_summary": {
                "total_episodes_analyzed": sum(report.get("episodes", 0) for report in weekly_data.get("daily_reports", [])),
                "key_findings": [
                    f"Analyzed {len(weekly_data.get('daily_reports', []))} daily reports this week",
                    "Identified consistent trends across multiple research domains",
                    "Generated actionable insights for R&D planning"
                ]
            },
            "research_categories": {},
            "actionable_recommendations": [
                "Review daily reports for detailed analysis",
                "Focus on consistent trending technologies",
                "Plan R&D investments based on weekly patterns"
            ],
            "trending_technologies": [],
            "high_impact_opportunities": []
        }
        
        # Create fake file structure for weekly summary
        report_files = {
            "json_file": "weekly_summary.json",  # Would be actual path
            "markdown_file": "weekly_summary.md"
        }
        
        return self.send_research_report(summary_report, report_files, "Weekly")


def setup_email_notifications() -> EmailNotifier:
    """Initialize email notification system"""
    
    print("📧 Setting up Email Notification System...")
    
    # Load configuration
    config = EmailConfig()
    
    if not config.sender_email or not config.recipient_emails:
        print("\n⚙️ Email Configuration Required:")
        print("Add the following to your .env file:")
        print()
        print("# Email Notification Settings")
        print("EMAIL_SENDER=your_email@gmail.com")
        print("EMAIL_PASSWORD=your_app_password")
        print("EMAIL_RECIPIENTS=recipient1@email.com,recipient2@email.com")
        print()
        print("📝 For Gmail:")
        print("   1. Enable 2-factor authentication")
        print("   2. Generate an App Password")
        print("   3. Use the App Password as EMAIL_PASSWORD")
        print()
    
    notifier = EmailNotifier(config)
    
    print("✅ Email notifier initialized!")
    
    return notifier


if __name__ == "__main__":
    # Demo the email system
    print("📧 Research Intelligence Email Notifier")
    print("=" * 50)
    
    notifier = setup_email_notifications()
    
    print("\n🧪 Testing email configuration...")
    
    if notifier.config.sender_email and notifier.config.recipient_emails:
        print("📋 Email Configuration:")
        print(f"   Sender: {notifier.config.sender_email}")
        print(f"   Recipients: {', '.join(notifier.config.recipient_emails)}")
        print(f"   SMTP: {notifier.config.smtp_server}:{notifier.config.smtp_port}")
        
        # Option to send test email
        test_choice = input("\n🚀 Send test email? (y/n): ").lower().strip()
        if test_choice == 'y':
            notifier.send_test_email()
        
    else:
        print("⚠️ Email not configured. Please update your .env file.")
    
    print("\n📧 Email system ready for automated reports!")
