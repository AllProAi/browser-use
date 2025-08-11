# Research Intelligence Agent for Journal Club

This project uses **browser-use** to automatically analyze research episodes from [Journal Club](https://journalclub.io/episodes) and generate actionable R&D intelligence reports.

## 🎯 What It Does

The Research Intelligence Agent:
- 🌐 **Scrapes** Journal Club episodes in real-time
- 🧠 **Analyzes** research trends using AI
- 📊 **Categorizes** episodes by technology domain
- 💡 **Identifies** emerging technologies and research gaps
- 📋 **Generates** actionable R&D recommendations
- 📁 **Exports** detailed reports in JSON and Markdown formats

## 🚀 Quick Start

### 1. Environment Check
```bash
# Verify your environment is set up
uv run python research_config.py
```

### 2. Simple Demo (Recommended First Run)
```bash
# Run the interactive demo
uv run python simple_research_demo.py
```

### 3. Live Web Scraping
```bash
# Run comprehensive analysis
uv run python live_research_scraper.py
```

## 📁 Project Files

| File | Purpose |
|------|---------|
| `simple_research_demo.py` | Interactive demo - start here! |
| `live_research_scraper.py` | Full web scraping and analysis |
| `research_intelligence_agent.py` | Core agent with data structures |
| `research_config.py` | Configuration and environment check |

## 🔧 Configuration Options

### Quick Configuration Types

```python
from research_config import get_research_config

# Fast analysis (cost-effective)
config = get_research_config("fast")

# Standard analysis (recommended)
config = get_research_config("default") 

# Comprehensive analysis (detailed)
config = get_research_config("comprehensive")
```

### Custom Configuration

```python
from research_config import ResearchConfig

config = ResearchConfig(
    model="gpt-4o-mini",        # LLM model to use
    headless=False,             # Show browser during scraping
    max_episodes_extract=100,   # Maximum episodes to analyze
    analysis_depth="standard",  # basic|standard|comprehensive
    target_categories=[         # Focus on specific categories
        "AI/ML", 
        "Computer Vision",
        "Robotics"
    ]
)
```

## 📊 Research Categories Analyzed

The agent automatically categorizes episodes into:

- **AI/ML**: Neural networks, deep learning, transformers
- **Computer Vision**: Image processing, object detection, YOLO
- **Robotics**: Autonomous systems, control systems, navigation
- **Biotechnology**: CRISPR, genomics, medical AI
- **Energy**: Renewable energy, batteries, smart grids
- **Security**: Cybersecurity, encryption, authentication
- **Manufacturing**: Industrial automation, quality control
- **Software Engineering**: DevOps, microservices, frameworks

## 🎯 Sample Use Cases

### 1. Technology Trend Analysis
```bash
# Get comprehensive trend analysis
uv run python live_research_scraper.py
```

### 2. Specific Topic Research
```bash
# Run demo and select option 2
uv run python simple_research_demo.py
# Then search for: "computer vision", "autonomous vehicles", etc.
```

### 3. Competitive Intelligence
```python
# Focus on specific research areas
from research_config import ResearchConfig

config = ResearchConfig(
    focus_areas=[
        "Commercial applications",
        "Investment opportunities",
        "Competitive intelligence"
    ]
)
```

## 📋 Output Reports

### JSON Report Structure
```json
{
  "report_metadata": {
    "generated_at": "2025-01-08T...",
    "source_url": "https://journalclub.io/episodes",
    "analysis_model": "gpt-4o-mini"
  },
  "executive_summary": {
    "total_episodes_analyzed": 150,
    "key_findings": [...]
  },
  "research_categories": {
    "AI_ML": 45,
    "Computer_Vision": 32,
    "Robotics": 28
  },
  "actionable_recommendations": [
    "Investigate YOLO applications for industrial automation",
    "Develop federated learning capabilities",
    "..."
  ]
}
```

### Markdown Summary
- Executive summary with key metrics
- Research category breakdown
- Trending technologies
- High-impact opportunities  
- Actionable R&D recommendations
- Research gap analysis

## 🔍 Analysis Features

### Automated Categorization
- Uses keyword analysis and AI classification
- Maps episodes to research domains
- Identifies cross-domain opportunities

### Trend Identification
- Analyzes trending vs latest episodes
- Identifies emerging technology patterns
- Tracks research momentum

### Commercial Assessment
- Evaluates commercial potential
- Identifies high-impact opportunities
- Suggests investment priorities

### Gap Analysis
- Identifies underexplored research areas
- Suggests novel research directions
- Maps competitive landscape

## ⚡ Performance Tips

### For Speed
```python
config = ResearchConfig(
    model="gpt-4o-mini",      # Faster, cheaper model
    headless=True,            # No browser UI
    analysis_depth="basic",   # Quick analysis
    max_episodes_extract=50   # Fewer episodes
)
```

### For Depth
```python
config = ResearchConfig(
    model="gpt-4o",              # More capable model
    analysis_depth="comprehensive",  # Deep analysis
    max_episodes_extract=200,    # More episodes
    save_csv_data=True          # Additional data formats
)
```

## 🛠️ Troubleshooting

### Common Issues

**No API Key Found**
```bash
# Add to .env file
OPENAI_API_KEY=your_key_here
```

**Browser Issues**
```bash
# Reinstall Playwright browsers
uv run playwright install chromium --with-deps --force
```

**Scraping Blocked**
```bash
# Try with headless mode disabled
config.headless = False
```

**Analysis Fails**
```bash
# Check your internet connection
# Try with a smaller episode limit
config.max_episodes_extract = 25
```

## 📈 Sample Output

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
   1. Investigate computer vision applications for industrial quality control
   2. Develop federated learning capabilities for privacy-preserving AI
   3. Research autonomous system applications in agriculture and logistics
```

## 🔮 Advanced Usage

### Custom Analysis Pipeline
```python
from live_research_scraper import LiveResearchScraper
from research_config import ResearchConfig

async def custom_analysis():
    config = ResearchConfig.create_comprehensive_config()
    scraper = LiveResearchScraper(
        api_key=config.openai_api_key,
        model=config.model,
        headless=config.headless
    )
    
    # Custom scraping
    content = await scraper.scrape_journal_club_episodes()
    
    # Custom analysis
    analysis = await scraper.analyze_scraped_content(content)
    
    # Custom reporting
    report = await scraper.generate_intelligence_report(analysis)
    
    return report
```

### Integration with Existing R&D Workflows
```python
# Schedule regular analysis
import schedule
import time

def run_weekly_analysis():
    asyncio.run(main())

schedule.every().week.do(run_weekly_analysis)

while True:
    schedule.run_pending()
    time.sleep(3600)  # Check every hour
```

## 🤝 Contributing

Feel free to extend the agent with:
- Additional research sources
- New analysis dimensions
- Custom export formats
- Enhanced categorization logic
- Integration with R&D tools

## 📄 License

This project uses the browser-use library and follows the same MIT license principles.

---

**Happy Research Intelligence Gathering! 🚀📊**
