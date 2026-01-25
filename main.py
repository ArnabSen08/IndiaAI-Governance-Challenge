"""Main entry point for the Publication Assistant multi-agent system."""
import os
import sys
from dotenv import load_dotenv
from orchestrator import MultiAgentOrchestrator

# Load environment variables
load_dotenv()


def main():
    """Main function to run the publication assistant."""
    print("=" * 60)
    print("Publication Assistant for AI Projects")
    print("Multi-Agent System")
    print("=" * 60)
    print()
    
    # Check for required API key
    if not os.getenv("OPENAI_API_KEY"):
        print("ERROR: OPENAI_API_KEY not found in environment variables.")
        print("Please create a .env file with your API key.")
        print("See .env_example for reference.")
        sys.exit(1)
    
    # Initialize orchestrator
    print("Initializing multi-agent system...")
    orchestrator = MultiAgentOrchestrator()
    print("✓ System initialized\n")
    
    # Get repository URL from user
    print("Enter GitHub repository URL to analyze:")
    repo_url = input("> ").strip()
    
    if not repo_url:
        print("No URL provided. Exiting.")
        sys.exit(1)
    
    # Optional project description
    print("\nEnter project description (optional, press Enter to skip):")
    description = input("> ").strip()
    
    if not description:
        description = None
    
    # Analyze repository
    print("\n" + "=" * 60)
    print("Starting analysis...")
    print("=" * 60 + "\n")
    
    result = orchestrator.analyze_repository(repo_url, description)
    
    # Display results
    print("\n" + "=" * 60)
    print("ANALYSIS COMPLETE")
    print("=" * 60 + "\n")
    
    if result["status"] == "success":
        print(result["report"])
        
        # Save report to file
        output_file = "analysis_report.md"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(result["report"])
        print(f"\n✓ Report saved to {output_file}")
    else:
        print(f"ERROR: {result.get('error', 'Unknown error')}")
        if result.get("errors"):
            print("\nErrors encountered:")
            for error in result["errors"]:
                print(f"  - {error}")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
