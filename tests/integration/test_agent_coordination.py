"""
Integration tests for agent coordination and communication.
"""

import pytest
import asyncio
import logging
from unittest.mock import Mock, AsyncMock, patch
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent.parent / "src"))

from src.agents.coordinator_agent import CoordinatorAgent
from src.agents.research_agent import ResearchAgent
from src.agents.content_agent import ContentAgent
from src.agents.validation_agent import ValidationAgent
from src.core.config import Config

class TestAgentCoordination:
    """Test cases for agent coordination and communication."""
    
    @pytest.fixture
    def config(self):
        """Create test configuration."""
        return Config(
            openai_api_key="test_key",
            max_retries=2,
            timeout_seconds=10
        )
    
    @pytest.fixture
    def logger(self):
        """Create test logger."""
        return logging.getLogger("test")
    
    @pytest.fixture
    def coordinator(self, config, logger):
        """Create coordinator agent instance."""
        return CoordinatorAgent(config, logger)
    
    def test_coordinator_initialization(self, coordinator):
        """Test coordinator initialization with all agents."""
        assert coordinator.name == "CoordinatorAgent"
        assert "ResearchAgent" in coordinator.agents
        assert "ContentAgent" in coordinator.agents
        assert "ValidationAgent" in coordinator.agents
        
        # Check that agents are properly initialized
        assert isinstance(coordinator.agents["ResearchAgent"], ResearchAgent)
        assert isinstance(coordinator.agents["ContentAgent"], ContentAgent)
        assert isinstance(coordinator.agents["ValidationAgent"], ValidationAgent)
    
    @pytest.mark.asyncio
    async def test_workflow_execution_with_mocked_agents(self, coordinator):
        """Test workflow execution with mocked agent responses."""
        
        # Mock agent responses
        with patch.object(coordinator.research_agent, 'process') as mock_research, \
             patch.object(coordinator.content_agent, 'process') as mock_content, \
             patch.object(coordinator.validation_agent, 'process') as mock_validation:
            
            mock_research.return_value = {
                "success": True,
                "findings": "Research findings about the topic"
            }
            
            mock_content.return_value = {
                "success": True,
                "content": "Generated content based on research"
            }
            
            mock_validation.return_value = {
                "success": True,
                "validation_passed": True,
                "safety_score": 95,
                "quality_score": 90
            }
            
            # Test workflow execution
            input_data = {
                "task": "Explain machine learning basics",
                "context": {"user_level": "beginner"}
            }
            
            result = await coordinator.process(input_data)
            
            assert result["success"] is True
            assert "workflow_results" in result["result"]
            assert "final_output" in result["result"]
    
    @pytest.mark.asyncio
    async def test_agent_failure_handling(self, coordinator):
        """Test handling of agent failures in workflow."""
        
        with patch.object(coordinator.research_agent, 'process') as mock_research:
            mock_research.return_value = {
                "success": False,
                "error": "Research agent failed"
            }
            
            input_data = {"task": "Test task"}
            result = await coordinator.process(input_data)
            
            # Coordinator should still succeed even if individual agents fail
            assert result["success"] is True
            assert "workflow_results" in result["result"]
    
    @pytest.mark.asyncio
    async def test_research_to_content_flow(self, coordinator):
        """Test data flow from research agent to content agent."""
        
        with patch.object(coordinator.research_agent, 'process') as mock_research, \
             patch.object(coordinator.content_agent, 'process') as mock_content:
            
            research_findings = "Detailed research about AI"
            mock_research.return_value = {
                "success": True,
                "findings": research_findings
            }
            
            mock_content.return_value = {
                "success": True,
                "content": "Content based on research"
            }
            
            input_data = {"task": "Write about AI"}
            result = await coordinator.process(input_data)
            
            # Verify research agent was called
            mock_research.assert_called_once()
            
            # Verify content agent was called
            mock_content.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_content_to_validation_flow(self, coordinator):
        """Test data flow from content agent to validation agent."""
        
        with patch.object(coordinator.content_agent, 'process') as mock_content, \
             patch.object(coordinator.validation_agent, 'process') as mock_validation:
            
            generated_content = "Generated content for validation"
            mock_content.return_value = {
                "success": True,
                "content": generated_content
            }
            
            mock_validation.return_value = {
                "success": True,
                "validation_passed": True,
                "issues": []
            }
            
            input_data = {"task": "Generate and validate content"}
            result = await coordinator.process(input_data)
            
            # Verify both agents were called
            mock_content.assert_called_once()
            mock_validation.assert_called_once()
    
    def test_get_all_agent_metrics(self, coordinator):
        """Test getting metrics from all agents."""
        metrics = coordinator.get_all_agent_metrics()
        
        assert "coordinator" in metrics
        assert "researchagent" in metrics
        assert "contentagent" in metrics
        assert "validationagent" in metrics
        
        # Check that each metric set has expected fields
        for agent_metrics in metrics.values():
            assert "requests" in agent_metrics
            assert "successes" in agent_metrics
            assert "failures" in agent_metrics
    
    @pytest.mark.asyncio
    async def test_health_check_all_agents(self, coordinator):
        """Test health check for all agents."""
        
        with patch.object(coordinator, 'health_check') as mock_coord_health, \
             patch.object(coordinator.research_agent, 'health_check') as mock_research_health, \
             patch.object(coordinator.content_agent, 'health_check') as mock_content_health, \
             patch.object(coordinator.validation_agent, 'health_check') as mock_validation_health:
            
            # Mock all health checks as successful
            mock_coord_health.return_value = {"healthy": True, "agent": "CoordinatorAgent"}
            mock_research_health.return_value = {"healthy": True, "agent": "ResearchAgent"}
            mock_content_health.return_value = {"healthy": True, "agent": "ContentAgent"}
            mock_validation_health.return_value = {"healthy": True, "agent": "ValidationAgent"}
            
            result = await coordinator.health_check_all_agents()
            
            assert result["system_healthy"] is True
            assert "individual_results" in result
            assert len(result["individual_results"]) == 4
    
    @pytest.mark.asyncio
    async def test_health_check_with_failures(self, coordinator):
        """Test health check when some agents fail."""
        
        with patch.object(coordinator, 'health_check') as mock_coord_health, \
             patch.object(coordinator.research_agent, 'health_check') as mock_research_health:
            
            # Mock coordinator as healthy, research agent as unhealthy
            mock_coord_health.return_value = {"healthy": True, "agent": "CoordinatorAgent"}
            mock_research_health.return_value = {"healthy": False, "agent": "ResearchAgent", "error": "Test error"}
            
            result = await coordinator.health_check_all_agents()
            
            assert result["system_healthy"] is False
            assert result["individual_results"]["coordinator"]["healthy"] is True
            assert result["individual_results"]["researchagent"]["healthy"] is False
    
    def test_workflow_history_tracking(self, coordinator):
        """Test that workflow history is properly tracked."""
        
        # Initially empty
        history = coordinator.get_workflow_history()
        assert len(history) == 0
        
        # Add some mock workflow history
        coordinator.workflow_history.append({
            "task": "Test task 1",
            "result": {"success": True},
            "timestamp": 123456789
        })
        
        coordinator.workflow_history.append({
            "task": "Test task 2", 
            "result": {"success": False},
            "timestamp": 123456790
        })
        
        history = coordinator.get_workflow_history()
        assert len(history) == 2
        assert history[0]["task"] == "Test task 1"
        assert history[1]["task"] == "Test task 2"
    
    def test_workflow_history_limit(self, coordinator):
        """Test that workflow history is limited to last 10 entries."""
        
        # Add 15 workflow entries
        for i in range(15):
            coordinator.workflow_history.append({
                "task": f"Test task {i}",
                "result": {"success": True},
                "timestamp": 123456789 + i
            })
        
        history = coordinator.get_workflow_history()
        
        # Should only return last 10
        assert len(history) == 10
        assert history[0]["task"] == "Test task 5"  # First of the last 10
        assert history[-1]["task"] == "Test task 14"  # Last entry

if __name__ == "__main__":
    pytest.main([__file__])