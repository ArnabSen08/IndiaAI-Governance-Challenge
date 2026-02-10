"""GitHub API Tool for fetching repository information."""
import os
import re
from typing import Dict, Any, Optional
from github import Github
from langchain.tools import BaseTool
from pydantic import BaseModel, Field


class GitHubToolInput(BaseModel):
    """Input schema for GitHub tool."""
    repo_url: str = Field(description="GitHub repository URL (e.g., https://github.com/user/repo)")
    action: str = Field(
        default="readme",
        description="Action to perform: 'readme', 'structure', 'files', or 'info'"
    )


class GitHubTool(BaseTool):
    """Tool for interacting with GitHub repositories."""
    
    name = "github_tool"
    description = """Fetches information from GitHub repositories including README content, 
    file structure, and repository metadata. Use this to analyze project documentation and code organization."""
    args_schema = GitHubToolInput
    
    def __init__(self):
        super().__init__()
        token = os.getenv("GITHUB_TOKEN")
        self.github = Github(token) if token else None
    
    def _run(self, repo_url: str, action: str = "readme") -> str:
        """Execute the GitHub tool."""
        try:
            # Extract owner and repo from URL
            match = re.search(r"github\.com/([^/]+)/([^/]+)", repo_url)
            if not match:
                return f"Error: Invalid GitHub URL format: {repo_url}"
            
            owner, repo_name = match.groups()
            repo_name = repo_name.rstrip('.git')
            
            if not self.github:
                return f"GitHub token not configured. Using public API for {owner}/{repo_name}"
            
            repo = self.github.get_repo(f"{owner}/{repo_name}")
            
            if action == "readme":
                try:
                    readme = repo.get_readme()
                    return f"README Content:\n{readme.decoded_content.decode('utf-8')}"
                except Exception as e:
                    return f"README not found or error: {str(e)}"
            
            elif action == "structure":
                contents = repo.get_contents("")
                structure = []
                for content in contents[:20]:  # Limit to first 20 items
                    structure.append(f"{content.type}: {content.name}")
                return f"Repository Structure:\n" + "\n".join(structure)
            
            elif action == "files":
                files = []
                for content in repo.get_contents(""):
                    if content.type == "file" and content.name.endswith(('.py', '.md', '.txt', '.json')):
                        files.append(content.name)
                return f"Key Files:\n" + "\n".join(files[:15])
            
            elif action == "info":
                return f"""Repository Info:
Name: {repo.name}
Description: {repo.description or 'No description'}
Language: {repo.language or 'Not specified'}
Stars: {repo.stargazers_count}
Forks: {repo.forks_count}
Topics: {', '.join(repo.get_topics()[:10])}
Created: {repo.created_at}
Updated: {repo.updated_at}"""
            
            else:
                return f"Unknown action: {action}. Use 'readme', 'structure', 'files', or 'info'"
                
        except Exception as e:
            return f"Error accessing GitHub repository: {str(e)}"
    
    async def _arun(self, repo_url: str, action: str = "readme") -> str:
        """Async execution."""
        return self._run(repo_url, action)
