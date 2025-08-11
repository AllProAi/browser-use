"""
Research Intelligence Configuration

Configuration settings and utilities for research intelligence agents.

@file purpose: Configuration management for research intelligence tools
"""

import os
from dataclasses import dataclass
from typing import List, Dict, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@dataclass
class ResearchConfig:
    """Configuration for research intelligence agents"""
    
    # API Configuration
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    model: str = "gpt-4o-mini"
    
    # Browser Configuration
    headless: bool = False
    window_width: int = 1280
    window_height: int = 720
    
    # Scraping Configuration
    max_episodes_extract: int = 100
    analysis_depth: str = "standard"  # basic, standard, comprehensive
    
    # Output Configuration
    save_detailed_json: bool = True
    save_markdown_summary: bool = True
    save_csv_data: bool = False
    
    # Research Categories
    target_categories: List[str] = None
    
    # Analysis Focus
    focus_areas: List[str] = None
    
    def __post_init__(self):
        # Load from environment variables
        self.openai_api_key = os.getenv('OPENAI_API_KEY', self.openai_api_key)
        self.anthropic_api_key = os.getenv('ANTHROPIC_API_KEY', self.anthropic_api_key)
        
        # Set default categories if not provided
        if self.target_categories is None:
            self.target_categories = [
                "AI/ML",
                "Computer Vision", 
                "Robotics",
                "Biotechnology",
                "Energy",
                "Security",
                "Manufacturing",
                "Software Engineering"
            ]
        
        # Set default focus areas
        if self.focus_areas is None:
            self.focus_areas = [
                "Commercial applications",
                "Breakthrough technologies", 
                "Research gaps",
                "Investment opportunities",
                "Competitive intelligence"
            ]
    
    def validate(self) -> bool:
        """Validate configuration"""
        if not self.openai_api_key and not self.anthropic_api_key:
            print("❌ Error: No API keys found. Please add OPENAI_API_KEY or ANTHROPIC_API_KEY to .env")
            return False
        return True

    @classmethod
    def create_default(cls) -> 'ResearchConfig':
        """Create default configuration"""
        return cls()
    
    @classmethod
    def create_fast_config(cls) -> 'ResearchConfig':
        """Create configuration optimized for speed"""
        return cls(
            model="gpt-4o-mini",
            headless=True,
            analysis_depth="basic",
            max_episodes_extract=50
        )
    
    @classmethod
    def create_comprehensive_config(cls) -> 'ResearchConfig':
        """Create configuration for comprehensive analysis"""
        return cls(
            model="gpt-4o",
            headless=False,
            analysis_depth="comprehensive", 
            max_episodes_extract=200,
            save_csv_data=True
        )


# Research Intelligence Templates
ANALYSIS_TEMPLATES = {
    "basic": """
    Analyze the research episodes and provide:
    1. Top 5 research categories
    2. 10 most interesting episodes
    3. 3 emerging trends
    4. 3 R&D recommendations
    """,
    
    "standard": """
    Provide comprehensive research analysis including:
    1. Detailed category breakdown with episode counts
    2. Trending vs latest episodes analysis
    3. Emerging technology identification
    4. Commercial opportunity assessment
    5. Research gap analysis
    6. Actionable R&D recommendations
    7. Competitive intelligence insights
    """,
    
    "comprehensive": """
    Conduct thorough research intelligence analysis covering:
    1. Complete episode categorization and classification
    2. Technology trend analysis with timeline projection
    3. Innovation level assessment (breakthrough vs incremental)
    4. Commercial potential scoring
    5. Market opportunity analysis
    6. Research gap identification with priority scoring
    7. Detailed R&D roadmap recommendations
    8. Competitive landscape analysis
    9. Investment opportunity prioritization
    10. Partnership and collaboration opportunities
    """
}


# Keywords for research categorization
RESEARCH_KEYWORDS = {
    "AI_ML": [
        "neural", "learning", "artificial intelligence", "machine learning", 
        "deep learning", "transformer", "llm", "gpt", "bert", "ai", "ml"
    ],
    "Computer_Vision": [
        "vision", "image", "video", "detection", "recognition", "segmentation",
        "yolo", "cnn", "opencv", "visual", "camera", "facial", "object detection"
    ],
    "Robotics": [
        "robot", "robotic", "autonomous", "automation", "control", "actuator",
        "sensor", "navigation", "manipulation", "humanoid", "drone"
    ],
    "Biotechnology": [
        "bio", "genetic", "genome", "dna", "rna", "crispr", "gene", "protein",
        "medical", "pharmaceutical", "biotech", "molecular", "cellular"
    ],
    "Energy": [
        "energy", "battery", "solar", "renewable", "power", "fuel", "electric",
        "grid", "storage", "efficiency", "sustainable", "carbon"
    ],
    "Security": [
        "security", "cyber", "encryption", "cryptography", "attack", "vulnerability",
        "authentication", "privacy", "blockchain", "quantum cryptography"
    ],
    "Manufacturing": [
        "manufacturing", "industrial", "factory", "production", "quality",
        "automation", "iot", "industry 4.0", "smart factory", "assembly"
    ],
    "Software_Engineering": [
        "software", "programming", "development", "code", "framework", "api",
        "microservices", "cloud", "devops", "testing", "debugging"
    ]
}


def get_research_config(config_type: str = "default") -> ResearchConfig:
    """Get research configuration by type"""
    
    if config_type == "fast":
        return ResearchConfig.create_fast_config()
    elif config_type == "comprehensive":
        return ResearchConfig.create_comprehensive_config()
    else:
        return ResearchConfig.create_default()


def check_environment_setup() -> bool:
    """Check if environment is properly set up"""
    
    print("🔍 Checking environment setup...")
    
    # Check API keys
    openai_key = os.getenv('OPENAI_API_KEY')
    anthropic_key = os.getenv('ANTHROPIC_API_KEY')
    
    if not openai_key and not anthropic_key:
        print("❌ No API keys found")
        print("   Please add OPENAI_API_KEY or ANTHROPIC_API_KEY to your .env file")
        return False
    
    if openai_key:
        print("✅ OpenAI API key found")
    if anthropic_key:
        print("✅ Anthropic API key found")
    
    # Check browser-use installation
    try:
        import browser_use
        print("✅ browser-use package available")
    except ImportError:
        print("❌ browser-use package not found")
        print("   Run: uv sync --dev --all-extras")
        return False
    
    # Check playwright
    try:
        import playwright
        print("✅ Playwright available")
    except ImportError:
        print("❌ Playwright not found")
        print("   Run: uv run playwright install chromium --with-deps")
        return False
    
    print("🎉 Environment setup looks good!")
    return True


if __name__ == "__main__":
    print("🔧 Research Intelligence Configuration")
    print("=" * 50)
    
    if check_environment_setup():
        print("\n✅ Ready to run research intelligence agents!")
        
        # Show sample configurations
        print("\n📋 Available Configurations:")
        print("   • default: Balanced analysis with standard settings")
        print("   • fast: Quick analysis optimized for speed")
        print("   • comprehensive: Deep analysis with all features")
        
        config = get_research_config("default")
        print(f"\n🔧 Default Configuration:")
        print(f"   • Model: {config.model}")
        print(f"   • Headless: {config.headless}")
        print(f"   • Max Episodes: {config.max_episodes_extract}")
        print(f"   • Analysis Depth: {config.analysis_depth}")
        
    else:
        print("\n❌ Please fix environment issues before running agents")
