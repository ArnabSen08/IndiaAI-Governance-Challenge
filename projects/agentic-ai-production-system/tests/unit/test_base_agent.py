"""
Unit tests for BaseAgent class.
"""

import pytest
import asyncio
import logging
from unittest.mock import Mock, AsyncMock, patch
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent.parent / "src"))

from src.agents.base_agent import BaseAgent
from src.core.config import Config

class TestableAgent(BaseAgent):
    """Testable implementation of BaseAgent for testing."""
    
    async def process(self, input_data):
        return {"success": True, "result": "test_result"}

class TestBaseAgent:
    """Test cases for BaseAgent."""
    
    @pytest.fixture
    def config(self):
        """Create test configuration."""
        return Config(
            openai_api_key="test_key",
            max_retries=2,
            timeout_seconds=10,
            max_input_length=1000
        )
    
    @pytest.fixture
    def logger(self):
        """Create test logger."""
        return logging.getLogger("test")
    
    @pytest.fixture
    def agent(self, config, logger):
        """Create test agent instance."""
        return TestableAgent("TestAgent", config, logger)
    
    def test_agent_initialization(self, agent, config):
        """Test agent initialization."""
        assert agent.name == "TestAgent"
        assert agent.config == config
        assert agent.metrics["requests"] == 0
        assert agent.metrics["successes"] == 0
        assert agent.metrics["failures"] == 0
    
    def test_validate_input_valid(self, agent):
        """Test input validation with valid data."""
        valid_input = {"text": "test input", "other": "data"}
        assert agent.validate_input(valid_input) is True
    
    def test_validate_input_invalid_type(self, agent):
        """Test input validation with invalid type."""
        invalid_input = "not a dictionary"
        assert agent.validate_input(invalid_input) is False
    
    def test_validate_input_too_long(self, agent):
        """Test input validation with text too long."""
        long_text = "x" * 2000  # Exceeds max_input_length
        invalid_input = {"text": long_text}
        assert agent.validate_input(invalid_input) is False
    
    def test_filter_output_disabled(self, agent):
        """Test output filtering when disabled."""
        agent.config.enable_output_filtering = False
        output = "test output with api_key"
        result = agent.filter_output(output)
        assert result == output
    
    def test_filter_output_enabled(self, agent):
        """Test output filtering when enabled."""
        agent.config.enable_output_filtering = True
        output = "test output with api_key"
        result = agent.filter_output(output)
        assert "[FILTERED]" in result
        assert "api_key" not in result
    
    def test_get_metrics_initial(self, agent):
        """Test getting initial metrics."""
        metrics = agent.get_metrics()
        assert metrics["name"] == "TestAgent"
        assert metrics["requests"] == 0
        assert metrics["success_rate"] == 0
        assert metrics["average_time"] == 0
    
    def test_get_metrics_with_data(self, agent):
        """Test getting metrics with some data."""
        agent.metrics["requests"] = 10
        agent.metrics["successes"] = 8
        agent.metrics["failures"] = 2
        agent.metrics["total_time"] = 50.0
        
        metrics = agent.get_metrics()
        assert metrics["requests"] == 10
        assert metrics["success_rate"] == 80.0
        assert metrics["average_time"] == 5.0
    
    @pytest.mark.asyncio
    async def test_make_llm_request_success(self, agent):
        """Test successful LLM request."""
        with patch.object(agent.client.chat.completions, 'create') as mock_create:
            # Mock response
            mock_response = Mock()
            mock_response.choices = [Mock()]
            mock_response.choices[0].message.content = "test response"
            mock_create.return_value = mock_response
            
            messages = [{"role": "user", "content": "test"}]
            result = await agent._make_llm_request(messages)
            
            assert result == "test response"
            assert agent.metrics["requests"] == 1
            assert agent.metrics["successes"] == 1
            assert agent.metrics["failures"] == 0
    
    @pytest.mark.asyncio
    async def test_make_llm_request_failure(self, agent):
        """Test failed LLM request."""
        with patch.object(agent.client.chat.completions, 'create') as mock_create:
            mock_create.side_effect = Exception("API Error")
            
            messages = [{"role": "user", "content": "test"}]
            
            with pytest.raises(Exception):
                await agent._make_llm_request(messages)
            
            assert agent.metrics["failures"] > 0
    
    @pytest.mark.asyncio
    async def test_health_check_success(self, agent):
        """Test successful health check."""
        with patch.object(agent, '_make_llm_request') as mock_request:
            mock_request.return_value = "OK"
            
            result = await agent.health_check()
            
            assert result["agent"] == "TestAgent"
            assert result["healthy"] is True
            assert "test_response" in result
    
    @pytest.mark.asyncio
    async def test_health_check_failure(self, agent):
        """Test failed health check."""
        with patch.object(agent, '_make_llm_request') as mock_request:
            mock_request.side_effect = Exception("Health check failed")
            
            result = await agent.health_check()
            
            assert result["agent"] == "TestAgent"
            assert result["healthy"] is False
            assert "error" in result
    
    @pytest.mark.asyncio
    async def test_process_implementation(self, agent):
        """Test that process method is implemented."""
        input_data = {"test": "data"}
        result = await agent.process(input_data)
        
        assert result["success"] is True
        assert result["result"] == "test_result"

if __name__ == "__main__":
    pytest.main([__file__])