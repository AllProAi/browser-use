"""
Simple Research Demo - Journal Club Episodes Analysis

A streamlined example showing how to use browser-use for research intelligence gathering.

@file purpose: Simple demo of research intelligence automation
"""

import asyncio
from browser_use import Agent
from browser_use.browser import Browser
from browser_use.llm import ChatOpenAI


async def analyze_journal_club():
    """Simple function to analyze Journal Club episodes"""
    
    task = """
    Go to https://journalclub.io/episodes and analyze the research topics.
    
    Please:
    1. Navigate to the Journal Club episodes page
    2. Identify the main research categories (AI/ML, Computer Vision, Robotics, etc.)
    3. List 10 most interesting episode titles related to cutting-edge technology
    4. Identify 3 emerging technology trends based on episode titles
    5. Suggest 3 R&D areas that would be most valuable to investigate further
    
    Focus on episodes that could provide actionable insights for technology R&D.
    
    Provide a summary in this format:
    
    ## Research Categories Found
    [List categories]
    
    ## Top 10 Interesting Episodes
    [List episodes with brief explanation of why they're interesting]
    
    ## Emerging Technology Trends
    [List 3 trends]
    
    ## R&D Recommendations
    [List 3 specific recommendations]
    """
    
    # Initialize the agent
    agent = Agent(
        task=task,
        llm=ChatOpenAI(model="gpt-4o-mini"),  # Using mini model for cost efficiency
        browser=Browser(
            headless=False,  # Set to True for headless operation
            window_width=1280,
            window_height=720
        )
    )
    
    print("🚀 Starting Journal Club research analysis...")
    print("🌐 Navigating to https://journalclub.io/episodes")
    print("📊 This will take a few minutes to analyze the content...")
    
    # Run the analysis
    history = await agent.run()
    
    print("\n" + "="*60)
    print("✅ ANALYSIS COMPLETE!")
    print("="*60)
    
    # Extract and display the result
    if history and len(history) > 0:
        final_result = history[-1]
        if hasattr(final_result, 'result') and final_result.result:
            content = final_result.result.extracted_content or str(final_result.result)
            print(content)
        else:
            print("Analysis completed successfully!")
    
    return history


async def focused_topic_search(topic: str):
    """Search for specific topic in Journal Club episodes"""
    
    task = f"""
    Go to https://journalclub.io/episodes and search for episodes related to "{topic}".
    
    Please:
    1. Navigate to the Journal Club episodes page
    2. Look for all episodes related to {topic}
    3. Analyze the research focus of each related episode
    4. Identify key research opportunities in this area
    5. Suggest specific next steps for R&D investigation
    
    Provide results in this format:
    
    ## Episodes Related to {topic}
    [List all relevant episodes with brief description]
    
    ## Research Opportunities
    [Identify specific research opportunities]
    
    ## R&D Next Steps
    [Suggest concrete actions to take]
    """
    
    agent = Agent(
        task=task,
        llm=ChatOpenAI(model="gpt-4o-mini"),
        browser=Browser(headless=False)
    )
    
    print(f"🔍 Searching for {topic}-related research...")
    
    history = await agent.run()
    
    print(f"\n" + "="*60)
    print(f"✅ {topic.upper()} RESEARCH ANALYSIS COMPLETE!")
    print("="*60)
    
    if history and len(history) > 0:
        final_result = history[-1]
        if hasattr(final_result, 'result') and final_result.result:
            content = final_result.result.extracted_content or str(final_result.result)
            print(content)
    
    return history


async def main():
    """Main function with interactive menu"""
    
    print("🧠 Journal Club Research Intelligence Tool")
    print("=" * 50)
    print("1. Full research analysis (recommended)")
    print("2. Search for specific topic")
    print("3. Exit")
    
    while True:
        try:
            choice = input("\nSelect an option (1-3): ").strip()
            
            if choice == "1":
                print("\n🚀 Starting comprehensive research analysis...")
                await analyze_journal_club()
                break
                
            elif choice == "2":
                topic = input("Enter the research topic to search for: ").strip()
                if topic:
                    print(f"\n🔍 Searching for '{topic}' research...")
                    await focused_topic_search(topic)
                else:
                    print("Please enter a valid topic.")
                    continue
                break
                
            elif choice == "3":
                print("👋 Goodbye!")
                return
                
            else:
                print("Please enter 1, 2, or 3.")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            return
        except Exception as e:
            print(f"❌ Error: {e}")
            return


if __name__ == "__main__":
    print("🔬 Simple Research Intelligence Demo")
    print("📚 Analyzing Journal Club episodes for R&D insights")
    print("\n⚠️  Make sure you have:")
    print("   • Added OPENAI_API_KEY to your .env file")
    print("   • Internet connection")
    print("   • Chrome/Chromium browser available")
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        print("Please check your .env file and internet connection")
