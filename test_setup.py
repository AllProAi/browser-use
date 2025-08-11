"""
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
        print("\n🎉 Setup test successful!")
        print("You can now run the research intelligence agents:")
        print("  • python simple_research_demo.py")
        print("  • python live_research_scraper.py")
    else:
        print("\n❌ Setup test failed")
        print("Please check your configuration and try again")


if __name__ == "__main__":
    asyncio.run(main())
