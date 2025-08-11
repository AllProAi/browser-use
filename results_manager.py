"""
Results Manager for Research Intelligence System

Manages organized storage, archiving, and retrieval of research reports.

@file purpose: Automated results organization and management
"""

import os
import json
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass
import zipfile


@dataclass
class ResultsConfig:
    """Configuration for results management"""
    base_results_dir: str = "research_results"
    archive_after_days: int = 30
    max_daily_reports: int = 10
    compress_archives: bool = True
    email_reports: bool = True
    cleanup_temp_files: bool = True


class ResultsManager:
    """Manages research intelligence results storage and organization"""
    
    def __init__(self, config: Optional[ResultsConfig] = None):
        self.config = config or ResultsConfig()
        self.base_dir = Path(self.config.base_results_dir)
        self._setup_directories()
    
    def _setup_directories(self):
        """Create organized directory structure"""
        
        directories = [
            self.base_dir,
            self.base_dir / "daily_reports",
            self.base_dir / "weekly_summaries", 
            self.base_dir / "monthly_archives",
            self.base_dir / "topic_analyses",
            self.base_dir / "trends_tracking",
            self.base_dir / "email_reports",
            self.base_dir / "backup",
            self.base_dir / "temp"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            
        print(f"📁 Results directories created in: {self.base_dir.absolute()}")
    
    def get_daily_report_path(self, date: Optional[datetime] = None) -> Path:
        """Get path for daily report"""
        if date is None:
            date = datetime.now()
        
        date_str = date.strftime("%Y-%m-%d")
        daily_dir = self.base_dir / "daily_reports" / date_str
        daily_dir.mkdir(parents=True, exist_ok=True)
        
        return daily_dir
    
    def save_research_report(self, 
                           report_data: Dict, 
                           report_type: str = "daily",
                           custom_name: Optional[str] = None) -> Dict[str, str]:
        """Save research report with organized naming"""
        
        timestamp = datetime.now()
        date_str = timestamp.strftime("%Y-%m-%d")
        time_str = timestamp.strftime("%H-%M-%S")
        
        # Determine save location
        if report_type == "daily":
            save_dir = self.get_daily_report_path(timestamp)
        elif report_type == "topic":
            save_dir = self.base_dir / "topic_analyses" / date_str
            save_dir.mkdir(parents=True, exist_ok=True)
        else:
            save_dir = self.base_dir / report_type / date_str
            save_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate filenames
        base_name = custom_name or f"research_intelligence_{date_str}_{time_str}"
        
        json_file = save_dir / f"{base_name}.json"
        md_file = save_dir / f"{base_name}_summary.md"
        
        # Save JSON report
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        # Generate and save Markdown summary
        md_content = self._generate_markdown_summary(report_data)
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        # Create metadata file
        metadata = {
            "generated_at": timestamp.isoformat(),
            "report_type": report_type,
            "files": {
                "json": str(json_file.name),
                "markdown": str(md_file.name)
            },
            "total_episodes": report_data.get("executive_summary", {}).get("total_episodes_analyzed", "Unknown"),
            "categories": len(report_data.get("research_categories", {})),
            "recommendations": len(report_data.get("actionable_recommendations", []))
        }
        
        metadata_file = save_dir / f"{base_name}_metadata.json"
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"📊 Report saved to: {save_dir}")
        print(f"   • JSON: {json_file.name}")
        print(f"   • Summary: {md_file.name}")
        print(f"   • Metadata: {metadata_file.name}")
        
        return {
            "directory": str(save_dir),
            "json_file": str(json_file),
            "markdown_file": str(md_file),
            "metadata_file": str(metadata_file),
            "timestamp": timestamp.isoformat()
        }
    
    def _generate_markdown_summary(self, report_data: Dict) -> str:
        """Generate markdown summary from report data"""
        
        md = f"""# Research Intelligence Report

**Generated:** {report_data.get('report_metadata', {}).get('generated_at', 'Unknown')}
**Source:** {report_data.get('report_metadata', {}).get('source_url', 'Journal Club Episodes')}

## Executive Summary

- **Episodes Analyzed:** {report_data.get('executive_summary', {}).get('total_episodes_analyzed', 'Unknown')}
- **Analysis Model:** {report_data.get('report_metadata', {}).get('analysis_model', 'Unknown')}

### Key Findings
"""
        
        for finding in report_data.get('executive_summary', {}).get('key_findings', []):
            md += f"- {finding}\n"
        
        md += "\n## Research Categories\n"
        categories = report_data.get('research_categories', {})
        if categories:
            for category, count in sorted(categories.items(), key=lambda x: x[1] if isinstance(x[1], int) else 0, reverse=True):
                md += f"- **{category.replace('_', ' ')}**: {count}\n"
        
        md += "\n## Trending Technologies\n"
        for topic in report_data.get('trending_technologies', [])[:10]:
            md += f"- {topic}\n"
        
        md += "\n## Actionable Recommendations\n"
        for i, rec in enumerate(report_data.get('actionable_recommendations', []), 1):
            md += f"{i}. {rec}\n"
        
        md += "\n## High-Impact Opportunities\n"
        for opp in report_data.get('high_impact_opportunities', [])[:5]:
            md += f"- {opp}\n"
        
        return md
    
    def create_weekly_summary(self) -> Optional[str]:
        """Create weekly summary from daily reports"""
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        
        weekly_data = {
            "week_ending": end_date.strftime("%Y-%m-%d"),
            "period": f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}",
            "daily_reports": [],
            "trends": {},
            "summary_stats": {}
        }
        
        # Collect daily reports from the week
        current_date = start_date
        while current_date <= end_date:
            daily_dir = self.get_daily_report_path(current_date)
            
            if daily_dir.exists():
                # Find JSON files in daily directory
                json_files = list(daily_dir.glob("*.json"))
                json_files = [f for f in json_files if not f.name.endswith("_metadata.json")]
                
                for json_file in json_files:
                    try:
                        with open(json_file, 'r', encoding='utf-8') as f:
                            daily_data = json.load(f)
                            weekly_data["daily_reports"].append({
                                "date": current_date.strftime("%Y-%m-%d"),
                                "file": str(json_file),
                                "episodes": daily_data.get("executive_summary", {}).get("total_episodes_analyzed", 0),
                                "categories": daily_data.get("research_categories", {})
                            })
                    except Exception as e:
                        print(f"⚠️ Error processing {json_file}: {e}")
            
            current_date += timedelta(days=1)
        
        if not weekly_data["daily_reports"]:
            print("📅 No daily reports found for weekly summary")
            return None
        
        # Save weekly summary
        weekly_dir = self.base_dir / "weekly_summaries"
        weekly_file = weekly_dir / f"weekly_summary_{end_date.strftime('%Y-%m-%d')}.json"
        
        with open(weekly_file, 'w', encoding='utf-8') as f:
            json.dump(weekly_data, f, indent=2, ensure_ascii=False)
        
        print(f"📅 Weekly summary created: {weekly_file}")
        return str(weekly_file)
    
    def archive_old_reports(self) -> List[str]:
        """Archive reports older than specified days"""
        
        cutoff_date = datetime.now() - timedelta(days=self.config.archive_after_days)
        archived_files = []
        
        # Archive daily reports
        daily_reports_dir = self.base_dir / "daily_reports"
        
        if daily_reports_dir.exists():
            for date_dir in daily_reports_dir.iterdir():
                if date_dir.is_dir():
                    try:
                        dir_date = datetime.strptime(date_dir.name, "%Y-%m-%d")
                        
                        if dir_date < cutoff_date:
                            # Create archive
                            archive_name = f"archived_reports_{date_dir.name}.zip"
                            archive_path = self.base_dir / "monthly_archives" / archive_name
                            
                            with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                                for file in date_dir.rglob("*"):
                                    if file.is_file():
                                        zipf.write(file, file.relative_to(date_dir))
                            
                            # Remove original directory
                            shutil.rmtree(date_dir)
                            archived_files.append(str(archive_path))
                            
                    except ValueError:
                        # Skip directories that don't match date format
                        continue
        
        if archived_files:
            print(f"🗄️ Archived {len(archived_files)} old report directories")
        
        return archived_files
    
    def get_latest_report(self, report_type: str = "daily") -> Optional[Dict]:
        """Get the most recent report of specified type"""
        
        if report_type == "daily":
            search_dir = self.base_dir / "daily_reports"
        elif report_type == "weekly":
            search_dir = self.base_dir / "weekly_summaries"
        else:
            search_dir = self.base_dir / report_type
        
        if not search_dir.exists():
            return None
        
        # Find most recent JSON file
        json_files = []
        for file_path in search_dir.rglob("*.json"):
            if not file_path.name.endswith("_metadata.json"):
                json_files.append(file_path)
        
        if not json_files:
            return None
        
        # Sort by modification time
        latest_file = max(json_files, key=lambda f: f.stat().st_mtime)
        
        try:
            with open(latest_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                data["_file_path"] = str(latest_file)
                return data
        except Exception as e:
            print(f"❌ Error reading {latest_file}: {e}")
            return None
    
    def cleanup_temp_files(self):
        """Clean up temporary files"""
        temp_dir = self.base_dir / "temp"
        
        if temp_dir.exists():
            for file_path in temp_dir.iterdir():
                try:
                    if file_path.is_file():
                        file_path.unlink()
                    elif file_path.is_dir():
                        shutil.rmtree(file_path)
                except Exception as e:
                    print(f"⚠️ Error cleaning {file_path}: {e}")
        
        print("🧹 Temporary files cleaned up")
    
    def get_results_summary(self) -> Dict:
        """Get summary of all results"""
        
        summary = {
            "directories": {
                "base": str(self.base_dir),
                "daily_reports": len(list((self.base_dir / "daily_reports").iterdir())) if (self.base_dir / "daily_reports").exists() else 0,
                "weekly_summaries": len(list((self.base_dir / "weekly_summaries").glob("*.json"))) if (self.base_dir / "weekly_summaries").exists() else 0,
                "archives": len(list((self.base_dir / "monthly_archives").glob("*.zip"))) if (self.base_dir / "monthly_archives").exists() else 0
            },
            "latest_report": None,
            "disk_usage": self._get_disk_usage()
        }
        
        # Get latest report info
        latest = self.get_latest_report("daily")
        if latest:
            summary["latest_report"] = {
                "timestamp": latest.get("report_metadata", {}).get("generated_at"),
                "episodes": latest.get("executive_summary", {}).get("total_episodes_analyzed"),
                "file_path": latest.get("_file_path")
            }
        
        return summary
    
    def _get_disk_usage(self) -> Dict:
        """Get disk usage statistics"""
        
        total_size = 0
        file_count = 0
        
        if self.base_dir.exists():
            for file_path in self.base_dir.rglob("*"):
                if file_path.is_file():
                    total_size += file_path.stat().st_size
                    file_count += 1
        
        return {
            "total_size_mb": round(total_size / (1024 * 1024), 2),
            "total_files": file_count
        }


def setup_results_system() -> ResultsManager:
    """Initialize the complete results management system"""
    
    print("🚀 Setting up Research Intelligence Results System...")
    
    config = ResultsConfig(
        base_results_dir="research_results",
        archive_after_days=30,
        email_reports=True,
        cleanup_temp_files=True
    )
    
    manager = ResultsManager(config)
    
    # Create initial structure
    manager._setup_directories()
    
    # Clean up any existing temp files
    manager.cleanup_temp_files()
    
    print("✅ Results system initialized successfully!")
    
    return manager


if __name__ == "__main__":
    # Demo the results system
    print("📊 Research Intelligence Results Manager")
    print("=" * 50)
    
    manager = setup_results_system()
    
    # Show system status
    summary = manager.get_results_summary()
    print(f"\n📁 Results Directory: {summary['directories']['base']}")
    print(f"📅 Daily Reports: {summary['directories']['daily_reports']}")
    print(f"📊 Weekly Summaries: {summary['directories']['weekly_summaries']}")
    print(f"🗄️ Archives: {summary['directories']['archives']}")
    print(f"💾 Total Size: {summary['disk_usage']['total_size_mb']} MB")
    print(f"📄 Total Files: {summary['disk_usage']['total_files']}")
    
    if summary['latest_report']:
        print(f"\n🆕 Latest Report:")
        print(f"   • Timestamp: {summary['latest_report']['timestamp']}")
        print(f"   • Episodes: {summary['latest_report']['episodes']}")
    else:
        print("\n📭 No reports found yet")
    
    print("\n🎯 Ready to save research intelligence reports!")
