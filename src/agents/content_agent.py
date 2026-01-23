"""
Content Agent - Manages content generation and refinement.
"""

import asyncio
from typing import Dict, Any, List
from .base_agent import BaseAgent

class ContentAgent(BaseAgent):
    """Specialized agent for content generation and refinement tasks."""
    
    def __init__(self, config, logger):
        super().__init__("ContentAgent", config, logger)
        self.content_templates = {
            "explanation": "Provide a clear, structured explanation",
            "summary": "Create a concise summary",
            "analysis": "Perform detailed analysis",
            "creative": "Generate creative content",
            "technical": "Provide technical documentation"
        }
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process content generation request."""
        
        if not self.validate_input(input_data):
            return {"error": "Invalid input data", "success": False}
        
        try:
            content_request = input_data.get("content_request", input_data.get("task", ""))
            content_type = input_data.get("content_type", "explanation")
            style = input_data.get("style", "professional")
            length = input_data.get("length", "medium")
            
            self.logger.info(f"ContentAgent: Generating {content_type} content: {content_request[:100]}...")
            
            # Generate content based on type
            if content_type == "summary":
                result = await self._generate_summary(content_request, style, length)
            elif content_type == "analysis":
                result = await self._generate_analysis(content_request, style, length)
            elif content_type == "creative":
                result = await self._generate_creative(content_request, style, length)
            elif content_type == "technical":
                result = await self._generate_technical(content_request, style, length)
            else:
                result = await self._generate_explanation(content_request, style, length)
            
            return result
            
        except Exception as e:
            self.logger.error(f"ContentAgent: Error generating content: {str(e)}")
            return {
                "error": str(e),
                "success": False,
                "agent": self.name
            }
    
    async def _generate_explanation(self, request: str, style: str, length: str) -> Dict[str, Any]:
        """Generate explanatory content."""
        
        length_guidance = self._get_length_guidance(length)
        style_guidance = self._get_style_guidance(style)
        
        messages = [
            {
                "role": "system",
                "content": f"""You are a content specialist focused on clear explanations.
                
                Style: {style_guidance}
                Length: {length_guidance}
                
                Structure your explanation with:
                1. Clear introduction
                2. Main concepts with examples
                3. Step-by-step breakdown if applicable
                4. Conclusion or summary
                
                Make it accessible and engaging while maintaining accuracy."""
            },
            {
                "role": "user",
                "content": f"Please explain: {request}"
            }
        ]
        
        try:
            response = await self._make_llm_request(messages, max_tokens=self._get_max_tokens(length))
            filtered_response = self.filter_output(response)
            
            return {
                "success": True,
                "content_type": "explanation",
                "content": filtered_response,
                "style": style,
                "length": length,
                "word_count": len(filtered_response.split()),
                "agent": self.name
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "agent": self.name
            }
    
    async def _generate_summary(self, request: str, style: str, length: str) -> Dict[str, Any]:
        """Generate summary content."""
        
        length_guidance = self._get_length_guidance(length)
        style_guidance = self._get_style_guidance(style)
        
        messages = [
            {
                "role": "system",
                "content": f"""You are a content specialist focused on creating concise summaries.
                
                Style: {style_guidance}
                Length: {length_guidance}
                
                Create a summary that:
                1. Captures key points
                2. Maintains essential information
                3. Uses clear, direct language
                4. Follows logical structure
                
                Prioritize clarity and completeness within the length constraints."""
            },
            {
                "role": "user",
                "content": f"Please summarize: {request}"
            }
        ]
        
        try:
            response = await self._make_llm_request(messages, max_tokens=self._get_max_tokens(length))
            filtered_response = self.filter_output(response)
            
            return {
                "success": True,
                "content_type": "summary",
                "content": filtered_response,
                "style": style,
                "length": length,
                "word_count": len(filtered_response.split()),
                "agent": self.name
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "agent": self.name
            }
    
    async def _generate_analysis(self, request: str, style: str, length: str) -> Dict[str, Any]:
        """Generate analytical content."""
        
        length_guidance = self._get_length_guidance(length)
        style_guidance = self._get_style_guidance(style)
        
        messages = [
            {
                "role": "system",
                "content": f"""You are a content specialist focused on analytical writing.
                
                Style: {style_guidance}
                Length: {length_guidance}
                
                Provide analysis that includes:
                1. Context and background
                2. Key factors and variables
                3. Relationships and patterns
                4. Implications and conclusions
                5. Supporting evidence and reasoning
                
                Maintain objectivity and critical thinking throughout."""
            },
            {
                "role": "user",
                "content": f"Please analyze: {request}"
            }
        ]
        
        try:
            response = await self._make_llm_request(messages, max_tokens=self._get_max_tokens(length))
            filtered_response = self.filter_output(response)
            
            return {
                "success": True,
                "content_type": "analysis",
                "content": filtered_response,
                "style": style,
                "length": length,
                "word_count": len(filtered_response.split()),
                "agent": self.name
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "agent": self.name
            }
    
    async def _generate_creative(self, request: str, style: str, length: str) -> Dict[str, Any]:
        """Generate creative content."""
        
        length_guidance = self._get_length_guidance(length)
        
        messages = [
            {
                "role": "system",
                "content": f"""You are a creative content specialist.
                
                Length: {length_guidance}
                
                Create engaging, original content that:
                1. Captures attention and interest
                2. Uses vivid language and imagery
                3. Maintains coherent narrative or structure
                4. Balances creativity with clarity
                
                Be imaginative while staying relevant to the request."""
            },
            {
                "role": "user",
                "content": f"Creative content request: {request}"
            }
        ]
        
        try:
            response = await self._make_llm_request(messages, max_tokens=self._get_max_tokens(length))
            filtered_response = self.filter_output(response)
            
            return {
                "success": True,
                "content_type": "creative",
                "content": filtered_response,
                "style": style,
                "length": length,
                "word_count": len(filtered_response.split()),
                "agent": self.name
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "agent": self.name
            }
    
    async def _generate_technical(self, request: str, style: str, length: str) -> Dict[str, Any]:
        """Generate technical documentation content."""
        
        length_guidance = self._get_length_guidance(length)
        
        messages = [
            {
                "role": "system",
                "content": f"""You are a technical documentation specialist.
                
                Length: {length_guidance}
                
                Create technical content that:
                1. Uses precise, accurate terminology
                2. Includes step-by-step instructions when applicable
                3. Provides examples and code snippets if relevant
                4. Follows standard documentation practices
                5. Considers different skill levels
                
                Prioritize accuracy, completeness, and usability."""
            },
            {
                "role": "user",
                "content": f"Technical documentation request: {request}"
            }
        ]
        
        try:
            response = await self._make_llm_request(messages, max_tokens=self._get_max_tokens(length))
            filtered_response = self.filter_output(response)
            
            return {
                "success": True,
                "content_type": "technical",
                "content": filtered_response,
                "style": style,
                "length": length,
                "word_count": len(filtered_response.split()),
                "agent": self.name
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "agent": self.name
            }
    
    def _get_length_guidance(self, length: str) -> str:
        """Get length guidance for content generation."""
        
        guidance = {
            "short": "Keep it concise (100-200 words). Focus on essential information only.",
            "medium": "Provide moderate detail (200-500 words). Balance completeness with brevity.",
            "long": "Provide comprehensive coverage (500-800 words). Include detailed explanations and examples.",
            "extended": "Create thorough, in-depth content (800+ words). Cover all relevant aspects comprehensively."
        }
        
        return guidance.get(length, guidance["medium"])
    
    def _get_style_guidance(self, style: str) -> str:
        """Get style guidance for content generation."""
        
        guidance = {
            "professional": "Use formal, business-appropriate language. Maintain professional tone throughout.",
            "casual": "Use conversational, friendly language. Be approachable and relatable.",
            "academic": "Use scholarly language with proper citations and formal structure.",
            "technical": "Use precise technical terminology. Focus on accuracy and clarity.",
            "creative": "Use engaging, expressive language. Be imaginative and compelling."
        }
        
        return guidance.get(style, guidance["professional"])
    
    def _get_max_tokens(self, length: str) -> int:
        """Get maximum tokens based on length requirement."""
        
        token_limits = {
            "short": 300,
            "medium": 600,
            "long": 1000,
            "extended": 1500
        }
        
        return token_limits.get(length, 600)
    
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate content-specific input data."""
        
        if not super().validate_input(input_data):
            return False
        
        # Check for content request
        request = input_data.get("content_request", input_data.get("task", ""))
        if not request or len(request.strip()) < 5:
            self.logger.error(f"{self.name}: Content request too short or missing")
            return False
        
        # Validate content type
        valid_types = ["explanation", "summary", "analysis", "creative", "technical"]
        content_type = input_data.get("content_type", "explanation")
        if content_type not in valid_types:
            self.logger.error(f"{self.name}: Invalid content type: {content_type}")
            return False
        
        # Validate style
        valid_styles = ["professional", "casual", "academic", "technical", "creative"]
        style = input_data.get("style", "professional")
        if style not in valid_styles:
            self.logger.error(f"{self.name}: Invalid style: {style}")
            return False
        
        # Validate length
        valid_lengths = ["short", "medium", "long", "extended"]
        length = input_data.get("length", "medium")
        if length not in valid_lengths:
            self.logger.error(f"{self.name}: Invalid length: {length}")
            return False
        
        return True
    
    async def refine_content(self, content: str, refinement_instructions: str) -> Dict[str, Any]:
        """Refine existing content based on instructions."""
        
        messages = [
            {
                "role": "system",
                "content": """You are a content refinement specialist. Improve the given content based on the specific instructions provided.
                
                Maintain the core message while enhancing:
                - Clarity and readability
                - Structure and flow
                - Accuracy and completeness
                - Style and tone consistency
                
                Preserve the original intent and key information."""
            },
            {
                "role": "user",
                "content": f"Original content:\n{content}\n\nRefinement instructions:\n{refinement_instructions}"
            }
        ]
        
        try:
            response = await self._make_llm_request(messages, max_tokens=800)
            filtered_response = self.filter_output(response)
            
            return {
                "success": True,
                "original_content": content,
                "refined_content": filtered_response,
                "refinement_instructions": refinement_instructions,
                "agent": self.name
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "agent": self.name
            }