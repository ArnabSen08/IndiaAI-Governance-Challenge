"""
Research Agent - Handles information gathering and analysis.
"""

import asyncio
from typing import Dict, Any, List
from .base_agent import BaseAgent

class ResearchAgent(BaseAgent):
    """Specialized agent for research and information gathering tasks."""
    
    def __init__(self, config, logger):
        super().__init__("ResearchAgent", config, logger)
        self.research_cache = {}
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process research request and gather relevant information."""
        
        if not self.validate_input(input_data):
            return {"error": "Invalid input data", "success": False}
        
        try:
            query = input_data.get("query", input_data.get("task", ""))
            research_type = input_data.get("research_type", "general")
            
            self.logger.info(f"ResearchAgent: Processing research query: {query[:100]}...")
            
            # Check cache first
            cache_key = f"{research_type}:{hash(query)}"
            if cache_key in self.research_cache:
                self.logger.info("ResearchAgent: Using cached result")
                return self.research_cache[cache_key]
            
            # Perform research based on type
            if research_type == "factual":
                result = await self._factual_research(query)
            elif research_type == "analytical":
                result = await self._analytical_research(query)
            elif research_type == "comparative":
                result = await self._comparative_research(query)
            else:
                result = await self._general_research(query)
            
            # Cache the result
            self.research_cache[cache_key] = result
            
            return result
            
        except Exception as e:
            self.logger.error(f"ResearchAgent: Error processing research: {str(e)}")
            return {
                "error": str(e),
                "success": False,
                "agent": self.name
            }
    
    async def _general_research(self, query: str) -> Dict[str, Any]:
        """Perform general research on the given query."""
        
        messages = [
            {
                "role": "system",
                "content": """You are a research specialist. Provide comprehensive, accurate information on the given topic.
                
                Structure your response as:
                1. Key findings (3-5 main points)
                2. Supporting details
                3. Relevant context
                4. Confidence level (high/medium/low)
                
                Be factual, cite reasoning, and acknowledge limitations."""
            },
            {
                "role": "user",
                "content": f"Research topic: {query}"
            }
        ]
        
        try:
            response = await self._make_llm_request(messages, max_tokens=800)
            filtered_response = self.filter_output(response)
            
            return {
                "success": True,
                "research_type": "general",
                "query": query,
                "findings": filtered_response,
                "confidence": self._assess_confidence(filtered_response),
                "agent": self.name
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "agent": self.name
            }
    
    async def _factual_research(self, query: str) -> Dict[str, Any]:
        """Perform factual research focusing on verifiable information."""
        
        messages = [
            {
                "role": "system",
                "content": """You are a fact-checking specialist. Provide only verifiable, factual information.
                
                Focus on:
                - Specific facts and figures
                - Dates, names, and locations
                - Quantifiable data
                - Well-established information
                
                Clearly indicate when information cannot be verified or is uncertain."""
            },
            {
                "role": "user",
                "content": f"Factual research request: {query}"
            }
        ]
        
        try:
            response = await self._make_llm_request(messages, max_tokens=600)
            filtered_response = self.filter_output(response)
            
            return {
                "success": True,
                "research_type": "factual",
                "query": query,
                "facts": filtered_response,
                "verification_notes": "Based on training data - verify current information independently",
                "agent": self.name
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "agent": self.name
            }
    
    async def _analytical_research(self, query: str) -> Dict[str, Any]:
        """Perform analytical research with deeper insights."""
        
        messages = [
            {
                "role": "system",
                "content": """You are an analytical research specialist. Provide deep analysis and insights.
                
                Include:
                - Multiple perspectives
                - Cause and effect relationships
                - Trends and patterns
                - Implications and consequences
                - Critical evaluation
                
                Structure your analysis clearly and support conclusions with reasoning."""
            },
            {
                "role": "user",
                "content": f"Analytical research request: {query}"
            }
        ]
        
        try:
            response = await self._make_llm_request(messages, max_tokens=1000)
            filtered_response = self.filter_output(response)
            
            return {
                "success": True,
                "research_type": "analytical",
                "query": query,
                "analysis": filtered_response,
                "methodology": "Multi-perspective analytical approach",
                "agent": self.name
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "agent": self.name
            }
    
    async def _comparative_research(self, query: str) -> Dict[str, Any]:
        """Perform comparative research analyzing multiple options or perspectives."""
        
        messages = [
            {
                "role": "system",
                "content": """You are a comparative research specialist. Analyze and compare different options, approaches, or perspectives.
                
                Provide:
                - Clear comparison criteria
                - Pros and cons for each option
                - Objective evaluation
                - Recommendations based on different use cases
                - Summary comparison table if applicable
                
                Maintain objectivity and acknowledge trade-offs."""
            },
            {
                "role": "user",
                "content": f"Comparative research request: {query}"
            }
        ]
        
        try:
            response = await self._make_llm_request(messages, max_tokens=900)
            filtered_response = self.filter_output(response)
            
            return {
                "success": True,
                "research_type": "comparative",
                "query": query,
                "comparison": filtered_response,
                "evaluation_criteria": "Multi-factor comparative analysis",
                "agent": self.name
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "agent": self.name
            }
    
    def _assess_confidence(self, response: str) -> str:
        """Assess confidence level based on response content."""
        
        # Simple heuristic-based confidence assessment
        uncertainty_indicators = [
            "might", "could", "possibly", "perhaps", "uncertain",
            "unclear", "depends", "varies", "approximately"
        ]
        
        confidence_indicators = [
            "definitely", "certainly", "established", "proven",
            "confirmed", "verified", "documented"
        ]
        
        response_lower = response.lower()
        
        uncertainty_count = sum(1 for indicator in uncertainty_indicators if indicator in response_lower)
        confidence_count = sum(1 for indicator in confidence_indicators if indicator in response_lower)
        
        if confidence_count > uncertainty_count:
            return "high"
        elif uncertainty_count > confidence_count * 2:
            return "low"
        else:
            return "medium"
    
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate research-specific input data."""
        
        if not super().validate_input(input_data):
            return False
        
        # Check for query or task
        query = input_data.get("query", input_data.get("task", ""))
        if not query or len(query.strip()) < 3:
            self.logger.error(f"{self.name}: Query too short or missing")
            return False
        
        # Validate research type if provided
        valid_types = ["general", "factual", "analytical", "comparative"]
        research_type = input_data.get("research_type", "general")
        if research_type not in valid_types:
            self.logger.error(f"{self.name}: Invalid research type: {research_type}")
            return False
        
        return True
    
    def clear_cache(self):
        """Clear the research cache."""
        self.research_cache.clear()
        self.logger.info("ResearchAgent: Cache cleared")
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        return {
            "cache_size": len(self.research_cache),
            "cache_keys": list(self.research_cache.keys())[:5]  # Show first 5 keys
        }