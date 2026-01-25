"""Example usage of the Publication Assistant system."""
import os
from dotenv import load_dotenv
from orchestrator import MultiAgentOrchestrator

# Load environment variables
load_dotenv()


def example_usage():
    """Example of how to use the Publication Assistant."""
    
    # Initialize the orchestrator
    orchestrator = MultiAgentOrchestrator()
    
    # Example: Analyze a GitHub repository
    repo_url = "https://github.com/langchain-ai/langchain"
    project_description = "A framework for developing applications powered by language models"
    
    print(f"Analyzing repository: {repo_url}")
    print(f"Description: {project_description}\n")
    
    # Run the analysis
    result = orchestrator.analyze_repository(repo_url, project_description)
    
    # Display results
    if result["status"] == "success":
        print("\n" + "="*60)
        print("ANALYSIS RESULTS")
        print("="*60)
        print(result["report"])
    else:
        print(f"Error: {result.get('error', 'Unknown error')}")


if __name__ == "__main__":
    example_usage()
