"""
Base agent class with common functionality for all agents.
Includes retry logic, error handling, and monitoring.
"""

import time
import asyncio
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from openai import OpenAI
import logging

class BaseAgent(ABC):
    """Base class for all agents with common functionality."""
    
    def __init__(self, name: str, config, logger: logging.Logger):
        self.name = name
        self.config = config
        self.logger = logger
        self.client = OpenAI(api_key=config.openai_api_key)
        self.metrics = {
            "requests": 0,
            "successes": 0,
            "failures": 0,
            "total_time": 0.0
        }
    
    @abstractmethod
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process input and return result. Must be implemented by subclasses."""
        pass
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type(Exception)
    )
    async def _make_llm_request(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Make LLM request with retry logic and error handling."""
        
        start_time = time.time()
        self.metrics["requests"] += 1
        
        try:
            self.logger.info(f"{self.name}: Making LLM request")
            
            response = self.client.chat.completions.create(
                model=self.config.openai_model,
                messages=messages,
                timeout=self.config.timeout_seconds,
                **kwargs
            )
            
            result = response.choices[0].message.content
            
            # Update metrics
            self.metrics["successes"] += 1
            self.metrics["total_time"] += time.time() - start_time
            
            self.logger.info(f"{self.name}: LLM request successful")
            return result
            
        except Exception as e:
            self.metrics["failures"] += 1
            self.logger.error(f"{self.name}: LLM request failed: {str(e)}")
            raise
    
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate input data. Override in subclasses for specific validation."""
        
        if not isinstance(input_data, dict):
            self.logger.error(f"{self.name}: Input must be a dictionary")
            return False
        
        # Check input length if text is provided
        if "text" in input_data:
            text = input_data["text"]
            if len(text) > self.config.max_input_length:
                self.logger.error(f"{self.name}: Input text too long ({len(text)} > {self.config.max_input_length})")
                return False
        
        return True
    
    def filter_output(self, output: str) -> str:
        """Filter output for safety. Override in subclasses for specific filtering."""
        
        if not self.config.enable_output_filtering:
            return output
        
        # Basic content filtering
        filtered_output = output
        
        # Remove potential sensitive patterns (basic implementation)
        sensitive_patterns = [
            "api_key",
            "password",
            "secret",
            "token"
        ]
        
        for pattern in sensitive_patterns:
            if pattern.lower() in filtered_output.lower():
                self.logger.warning(f"{self.name}: Potential sensitive content detected and filtered")
                filtered_output = filtered_output.replace(pattern, "[FILTERED]")
        
        return filtered_output
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get agent performance metrics."""
        
        success_rate = (self.metrics["successes"] / self.metrics["requests"]) * 100 if self.metrics["requests"] > 0 else 0
        avg_time = self.metrics["total_time"] / self.metrics["requests"] if self.metrics["requests"] > 0 else 0
        
        return {
            "name": self.name,
            "requests": self.metrics["requests"],
            "successes": self.metrics["successes"],
            "failures": self.metrics["failures"],
            "success_rate": round(success_rate, 2),
            "average_time": round(avg_time, 2)
        }
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform agent health check."""
        
        try:
            # Simple test request
            test_messages = [
                {"role": "user", "content": "Hello, this is a health check. Please respond with 'OK'."}
            ]
            
            response = await self._make_llm_request(test_messages, max_tokens=10)
            
            return {
                "agent": self.name,
                "healthy": True,
                "response_time": time.time(),
                "test_response": response[:50]  # First 50 chars
            }
            
        except Exception as e:
            return {
                "agent": self.name,
                "healthy": False,
                "error": str(e),
                "response_time": time.time()
            }