"""Text Processing Tool for analyzing text quality and structure."""
import textstat
from typing import Dict
from langchain.tools import BaseTool
from pydantic import BaseModel, Field


class TextProcessorInput(BaseModel):
    """Input schema for text processor tool."""
    text: str = Field(description="Text content to analyze")
    analysis_type: str = Field(
        default="all",
        description="Type of analysis: 'readability', 'statistics', 'structure', or 'all'"
    )


class TextProcessorTool(BaseTool):
    """Tool for analyzing text quality, readability, and structure."""
    
    name = "text_processor"
    description = """Analyzes text quality, readability scores, and structural elements. 
    Use this to evaluate documentation clarity and identify areas for improvement."""
    args_schema = TextProcessorInput
    
    def _run(self, text: str, analysis_type: str = "all") -> str:
        """Execute the text processing tool."""
        try:
            if not text or len(text.strip()) < 10:
                return "Error: Text is too short for analysis"
            
            results = []
            
            if analysis_type in ["readability", "all"]:
                flesch_score = textstat.flesch_reading_ease(text)
                flesch_kincaid = textstat.flesch_kincaid_grade(text)
                smog_index = textstat.smog_index(text)
                
                results.append(f"""Readability Metrics:
  - Flesch Reading Ease: {flesch_score:.2f} ({self._interpret_flesch(flesch_score)})
  - Flesch-Kincaid Grade Level: {flesch_kincaid:.2f}
  - SMOG Index: {smog_index:.2f}""")
            
            if analysis_type in ["statistics", "all"]:
                char_count = len(text)
                word_count = textstat.lexicon_count(text)
                sentence_count = textstat.sentence_count(text)
                syllable_count = textstat.syllable_count(text)
                
                results.append(f"""Text Statistics:
  - Characters: {char_count:,}
  - Words: {word_count:,}
  - Sentences: {sentence_count:,}
  - Syllables: {syllable_count:,}
  - Avg words per sentence: {word_count/sentence_count if sentence_count > 0 else 0:.2f}""")
            
            if analysis_type in ["structure", "all"]:
                # Check for common README sections
                sections = []
                text_lower = text.lower()
                common_sections = [
                    "installation", "usage", "features", "requirements",
                    "contributing", "license", "examples", "documentation",
                    "getting started", "quick start", "overview", "description"
                ]
                
                for section in common_sections:
                    if section in text_lower:
                        sections.append(section)
                
                results.append(f"""Structure Analysis:
  - Common sections found: {', '.join(sections) if sections else 'None detected'}
  - Has headings: {'Yes' if '#' in text else 'No'}
  - Has code blocks: {'Yes' if '```' in text else 'No'}
  - Has links: {'Yes' if 'http' in text_lower or '[' in text else 'No'}""")
            
            return "\n\n".join(results) if results else "No analysis performed"
            
        except Exception as e:
            return f"Error processing text: {str(e)}"
    
    def _interpret_flesch(self, score: float) -> str:
        """Interpret Flesch Reading Ease score."""
        if score >= 90:
            return "Very Easy"
        elif score >= 80:
            return "Easy"
        elif score >= 70:
            return "Fairly Easy"
        elif score >= 60:
            return "Standard"
        elif score >= 50:
            return "Fairly Difficult"
        elif score >= 30:
            return "Difficult"
        else:
            return "Very Difficult"
    
    async def _arun(self, text: str, analysis_type: str = "all") -> str:
        """Async execution."""
        return self._run(text, analysis_type)
