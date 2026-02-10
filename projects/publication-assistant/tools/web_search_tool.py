"""Web Search Tool for finding similar projects and best practices."""
import os
import requests
from typing import Dict, Any
from langchain.tools import BaseTool
from pydantic import BaseModel, Field


class WebSearchToolInput(BaseModel):
    """Input schema for web search tool."""
    query: str = Field(description="Search query string")
    max_results: int = Field(default=5, description="Maximum number of results to return")


class WebSearchTool(BaseTool):
    """Tool for searching the web for similar projects and best practices."""
    
    name = "web_search_tool"
    description = """Searches the web for information about similar projects, best practices, 
    and relevant resources. Use this to find inspiration and compare with other projects."""
    args_schema = WebSearchToolInput
    
    def _run(self, query: str, max_results: int = 5) -> str:
        """Execute the web search tool."""
        try:
            # Using DuckDuckGo HTML search as a fallback (no API key needed)
            # In production, you might use Google Custom Search API, SerpAPI, etc.
            search_url = "https://html.duckduckgo.com/html/"
            params = {"q": query}
            
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            
            response = requests.get(search_url, params=params, headers=headers, timeout=10)
            
            if response.status_code == 200:
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(response.text, 'html.parser')
                
                results = []
                # Extract search results (DuckDuckGo HTML structure)
                result_divs = soup.find_all('div', class_='result')[:max_results]
                
                for div in result_divs:
                    title_elem = div.find('a', class_='result__a')
                    snippet_elem = div.find('a', class_='result__snippet')
                    
                    if title_elem:
                        title = title_elem.get_text(strip=True)
                        url = title_elem.get('href', '')
                        snippet = snippet_elem.get_text(strip=True) if snippet_elem else "No snippet"
                        results.append(f"Title: {title}\nURL: {url}\nSnippet: {snippet}\n")
                
                if results:
                    return f"Web Search Results for '{query}':\n\n" + "\n---\n".join(results)
                else:
                    return f"Found {len(result_divs)} results for '{query}', but couldn't extract details. Try a different search query."
            else:
                return f"Web search returned status code {response.status_code}. Query: {query}"
                
        except Exception as e:
            return f"Error performing web search: {str(e)}. Query: {query}"
    
    async def _arun(self, query: str, max_results: int = 5) -> str:
        """Async execution."""
        return self._run(query, max_results)
