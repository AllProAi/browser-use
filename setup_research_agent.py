"""
Setup Script for Research Intelligence Agent

This script helps users set up and test the research intelligence system.

@file purpose: Setup and validation for research intelligence tools
"""

import os
import sys
from pathlib import Path


def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 11):
        print("❌ Python 3.11+ is required")
        print(f"   Current version: {version.major}.{version.minor}")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True


def check_env_file():
    """Check if .env file exists and has required keys"""
    env_path = Path(".env")
    
    if not env_path.exists():
        print("❌ .env file not found")
        print("   Creating .env template...")
        
        env_template = """# Research Intelligence Agent Configuration

# OpenAI API Key (recommended)
OPENAI_API_KEY=your_openai_api_key_here

# Alternative: Anthropic API Key
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Optional: Browser-use settings
BROWSER_USE_LOGGING_LEVEL=info
BROWSER_USE_DEBUG=false
"""
        
        with open(".env", "w") as f:
            f.write(env_template)
        
        print("✅ .env template created")
        print("   Please edit .env and add your API keys")
        return False
    
    # Check if API keys are configured
    with open(".env", "r") as f:
        content = f.read()
    
    has_openai = "OPENAI_API_KEY=" in content and "your_openai_api_key_here" not in content
    has_anthropic = "ANTHROPIC_API_KEY=" in content and "your_anthropic_api_key_here" not in content
    
    if not has_openai and not has_anthropic:
        print("⚠️  .env file exists but no API keys configured")
        print("   Please add your OPENAI_API_KEY or ANTHROPIC_API_KEY to .env")
        return False
    
    if has_openai:
        print("✅ OpenAI API key configured")
    if has_anthropic:
        print("✅ Anthropic API key configured")
    
    return True


def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import browser_use
        print("✅ browser-use installed")
    except ImportError:
        print("❌ browser-use not installed")
        print("   Run: uv sync --dev --all-extras")
        return False
    
    try:
        import playwright
        print("✅ playwright installed")
    except ImportError:
        print("❌ playwright not installed")
        print("   Run: uv run playwright install chromium --with-deps")
        return False
    
    try:
        from dotenv import load_dotenv
        print("✅ python-dotenv available")
    except ImportError:
        print("❌ python-dotenv not installed")
        return False
    
    return True


def test_browser_installation():
    """Test if Chromium browser is properly installed"""
    try:
        from playwright.sync_api import sync_playwright
        
        with sync_playwright() as p:
            # Try to launch browser
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto("https://www.google.com")
            title = page.title()
            browser.close()
            
            if "Google" in title:
                print("✅ Browser installation working")
                return True
            else:
                print("⚠️  Browser launched but may have issues")
                return False
                
    except Exception as e:
        print(f"❌ Browser test failed: {str(e)}")
        print("   Try running: uv run playwright install chromium --with-deps --force")
        return False


def create_sample_script():
    """Create a simple test script for users"""
    sample_code = '''"""
Test Script for Research Intelligence Agent
Run this after setup to verify everything works.
"""

import asyncio
from browser_use import Agent
from browser_use.browser import Browser
from browser_use.llm import ChatOpenAI


async def test_basic_functionality():
    """Test basic browser-use functionality"""
    
    task = """
    Go to https://example.com and tell me what you see.
    Just describe the main content of the page.
    """
    
    agent = Agent(
        task=task,
        llm=ChatOpenAI(model="gpt-4o-mini"),
        browser=Browser(headless=True, window_width=800, window_height=600)
    )
    
    print("Testing basic browser automation...")
    
    try:
        history = await agent.run()
        print("Basic test successful!")
        
        if history and len(history) > 0:
            final_result = history[-1]
            if hasattr(final_result, 'result') and final_result.result:
                print("Result preview:", str(final_result.result)[:200], "...")
        
        return True
        
    except Exception as e:
        print(f"Basic test failed: {e}")
        return False


async def main():
    """Run the test"""
    print("🧪 Testing Research Intelligence Agent Setup")
    print("=" * 50)
    
    success = await test_basic_functionality()
    
    if success:
        print("\\n🎉 Setup test successful!")
        print("You can now run the research intelligence agents:")
        print("  • python simple_research_demo.py")
        print("  • python live_research_scraper.py")
    else:
        print("\\n❌ Setup test failed")
        print("Please check your configuration and try again")


if __name__ == "__main__":
    asyncio.run(main())
'''
    
    with open("test_setup.py", "w", encoding="utf-8") as f:
        f.write(sample_code)
    
    print("✅ Test script created: test_setup.py")


def main():
    """Main setup function"""
    print("🚀 Research Intelligence Agent Setup")
    print("=" * 50)
    
    print("\n1. Checking Python version...")
    if not check_python_version():
        return False
    
    print("\n2. Checking environment configuration...")
    env_ok = check_env_file()
    
    print("\n3. Checking dependencies...")
    if not check_dependencies():
        return False
    
    print("\n4. Testing browser installation...")
    if not test_browser_installation():
        return False
    
    print("\n5. Creating test script...")
    create_sample_script()
    
    if env_ok:
        print("\n🎉 Setup complete!")
        print("\n📋 Next steps:")
        print("   1. Run test: uv run python test_setup.py")
        print("   2. Try demo: uv run python simple_research_demo.py")
        print("   3. Full analysis: uv run python live_research_scraper.py")
        
        print("\n📚 Available scripts:")
        print("   • simple_research_demo.py - Interactive demo")
        print("   • live_research_scraper.py - Full web scraping")
        print("   • research_config.py - Configuration check")
        print("   • test_setup.py - Basic functionality test")
        
        return True
    else:
        print("\n⚠️  Setup partially complete")
        print("   Please configure your API keys in .env file")
        print("   Then run this setup script again")
        return False


if __name__ == "__main__":
    success = main()
    
    if not success:
        print("\n❌ Setup incomplete")
        sys.exit(1)
    else:
        print("\n✅ Ready to analyze research intelligence!")
