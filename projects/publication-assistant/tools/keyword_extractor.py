"""Keyword Extraction Tool for analyzing project content."""
import yake
from typing import List, Dict
from langchain.tools import BaseTool
from pydantic import BaseModel, Field


class KeywordExtractorInput(BaseModel):
    """Input schema for keyword extractor tool."""
    text: str = Field(description="Text content to extract keywords from")
    max_keywords: int = Field(default=10, description="Maximum number of keywords to extract")
    language: str = Field(default="en", description="Language code (e.g., 'en', 'es', 'fr')")


class KeywordExtractorTool(BaseTool):
    """Tool for extracting keywords and key phrases from text."""
    
    name = "keyword_extractor"
    description = """Extracts relevant keywords and key phrases from text content. 
    Use this to identify important terms, topics, and themes in project documentation."""
    args_schema = KeywordExtractorInput
    
    def _run(self, text: str, max_keywords: int = 10, language: str = "en") -> str:
        """Execute the keyword extraction tool."""
        try:
            if not text or len(text.strip()) < 10:
                return "Error: Text is too short for keyword extraction"
            
            # Initialize YAKE keyword extractor
            kw_extractor = yake.KeywordExtractor(
                lan=language,
                n=3,  # n-gram size
                dedupLim=0.7,
                top=max_keywords
            )
            
            keywords = kw_extractor.extract_keywords(text)
            
            if keywords:
                result = "Extracted Keywords:\n"
                for score, keyword in keywords:
                    result += f"  - {keyword} (score: {score:.4f})\n"
                return result
            else:
                return "No keywords extracted from the provided text"
                
        except Exception as e:
            return f"Error extracting keywords: {str(e)}"
    
    async def _arun(self, text: str, max_keywords: int = 10, language: str = "en") -> str:
        """Async execution."""
        return self._run(text, max_keywords, language)
