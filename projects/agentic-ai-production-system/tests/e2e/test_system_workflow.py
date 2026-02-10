"""
End-to-end tests for complete system workflows.
"""

import pytest
import asyncio
import logging
import tempfile
import os
from pathlib import Path
import sys

# Add src to path
sys.path.append(str(Path(__file__).parent.parent.parent / "src"))

from src.agents.coordinator_agent import CoordinatorAgent
from src.core.config import Config
from src.core.health import HealthChecker
from src.utils.logger import setup_logger

class TestSystemWorkflow:
    """End-to-end test cases for complete system workflows."""
    
    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for test files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            yield temp_dir
    
    @pytest.fixture
    def config(self, temp_dir):
        """Create test configuration with temporary log directory."""
        return Config(
            openai_api_key="test_key_for_e2e",
            log_file=os.path.join(temp_dir, "test.log"),
            max_retries=1,
            timeout_seconds=5,
            enable_file_logging=True
        )
    
    @pytest.fixture
    def logger(self, config):
        """Create test logger."""
        return setup_logger("e2e_test", config.log_level, config.log_file)
    
    @pytest.fixture
    def coordinator(self, config, logger):
        """Create coordinator for end-to-end testing."""
        return CoordinatorAgent(config, logger)
    
    @pytest.fixture
    def health_checker(self, config):
        """Create health checker for testing."""
        return HealthChecker(config)
    
    def test_system_initialization(self, coordinator, health_checker):
        """Test complete system initialization."""
        
        # Test coordinator initialization
        assert coordinator is not None
        assert coordinator.name == "CoordinatorAgent"
        assert len(coordinator.agents) == 3
        
        # Test health checker initialization
        assert health_checker is not None
        assert health_checker.config is not None
    
    def test_configuration_loading(self, config, temp_dir):
        """Test configuration loading and validation."""
        
        assert config.openai_api_key == "test_key_for_e2e"
        assert config.max_retries == 1
        assert config.timeout_seconds == 5
        
        # Test log directory creation
        config.ensure_log_directory()
        log_path = Path(config.log_file)
        assert log_path.parent.exists()
    
    def test_logging_system(self, logger, config):
        """Test logging system functionality."""
        
        # Test logging
        logger.info("Test info message")
        logger.warning("Test warning message")
        logger.error("Test error message")
        
        # Check log file exists and has content
        log_path = Path(config.log_file)
        if config.enable_file_logging:
            assert log_path.exists()
            
            # Read log content
            log_content = log_path.read_text()
            assert "Test info message" in log_content
            assert "Test warning message" in log_content
            assert "Test error message" in log_content
    
    @pytest.mark.asyncio
    async def test_complete_workflow_simulation(self, coordinator):
        """Test complete workflow with simulated responses."""
        
        # This test simulates a complete workflow without actual API calls
        input_data = {
            "task": "Explain the benefits of renewable energy",
            "context": {
                "audience": "general public",
                "length": "medium"
            }
        }
        
        # Mock the LLM requests to avoid actual API calls
        async def mock_llm_request(messages, **kwargs):
            if "workflow" in str(messages).lower():
                return '{"steps": [{"agent": "ResearchAgent", "action": "research", "priority": 1}]}'
            elif "research" in str(messages).lower():
                return "Renewable energy sources like solar and wind are sustainable and environmentally friendly."
            elif "content" in str(messages).lower():
                return "Renewable energy offers numerous benefits including environmental protection and energy independence."
            else:
                return "Validation passed - content is safe and high quality."
        
        # Patch all agents' LLM request methods
        coordinator._make_llm_request = mock_llm_request
        coordinator.research_agent._make_llm_request = mock_llm_request
        coordinator.content_agent._make_llm_request = mock_llm_request
        coordinator.validation_agent._make_llm_request = mock_llm_request
        
        # Execute workflow
        result = await coordinator.process(input_data)
        
        # Verify results
        assert result["success"] is True
        assert "result" in result
        assert "workflow_plan" in result
        
        # Check workflow history
        history = coordinator.get_workflow_history()
        assert len(history) == 1
        assert history[0]["task"] == input_data["task"]
    
    def test_health_check_system(self, health_checker):
        """Test system health checking."""
        
        # Note: This will fail with real API key validation, but tests the structure
        health_status = health_checker.check_system_health()
        
        assert "healthy" in health_status
        assert "checks" in health_status
        assert "timestamp" in health_status
        
        # Check individual health checks
        checks = health_status["checks"]
        assert "api" in checks
        assert "resources" in checks
        assert "filesystem" in checks
        assert "configuration" in checks
        
        # Each check should have status and message
        for check_name, check_result in checks.items():
            assert "status" in check_result
            assert "message" in check_result
    
    def test_system_metrics(self, health_checker):
        """Test system metrics collection."""
        
        metrics = health_checker.get_system_metrics()
        
        if "error" not in metrics:
            assert "memory" in metrics
            assert "disk" in metrics
            assert "cpu" in metrics
            assert "timestamp" in metrics
            
            # Check memory metrics
            memory = metrics["memory"]
            assert "total_gb" in memory
            assert "available_gb" in memory
            assert "percent_used" in memory
            
            # Check disk metrics
            disk = metrics["disk"]
            assert "total_gb" in disk
            assert "free_gb" in disk
            assert "percent_used" in disk
            
            # Check CPU metrics
            cpu = metrics["cpu"]
            assert "percent" in cpu
            assert "count" in cpu
    
    def test_agent_metrics_collection(self, coordinator):
        """Test metrics collection from all agents."""
        
        metrics = coordinator.get_all_agent_metrics()
        
        # Should have metrics for all agents
        expected_agents = ["coordinator", "researchagent", "contentagent", "validationagent"]
        for agent in expected_agents:
            assert agent in metrics
            
            agent_metrics = metrics[agent]
            assert "requests" in agent_metrics
            assert "successes" in agent_metrics
            assert "failures" in agent_metrics
            assert "success_rate" in agent_metrics
            assert "average_time" in agent_metrics
    
    @pytest.mark.asyncio
    async def test_error_handling_and_recovery(self, coordinator):
        """Test system error handling and recovery."""
        
        # Test with invalid input
        invalid_input = {"invalid": "data"}
        result = await coordinator.process(invalid_input)
        
        # System should handle gracefully
        assert "error" in result or result.get("success") is False
        
        # Test with empty input
        empty_input = {}
        result = await coordinator.process(empty_input)
        
        # System should handle gracefully
        assert "error" in result or result.get("success") is False
        
        # Test with very long input (if validation is enabled)
        long_input = {"task": "x" * 20000}  # Very long task
        result = await coordinator.process(long_input)
        
        # Should either process or reject gracefully
        assert isinstance(result, dict)
    
    def test_configuration_validation(self):
        """Test configuration validation with various inputs."""
        
        # Test valid configuration
        valid_config = Config(
            openai_api_key="valid_key",
            max_retries=3,
            timeout_seconds=30
        )
        assert valid_config.openai_api_key == "valid_key"
        
        # Test configuration with environment variables
        os.environ["OPENAI_API_KEY"] = "env_test_key"
        os.environ["MAX_RETRIES"] = "5"
        
        try:
            env_config = Config()
            assert env_config.openai_api_key == "env_test_key"
            assert env_config.max_retries == 5
        finally:
            # Clean up
            os.environ.pop("OPENAI_API_KEY", None)
            os.environ.pop("MAX_RETRIES", None)
    
    def test_file_system_operations(self, config, temp_dir):
        """Test file system operations and permissions."""
        
        # Test log directory creation
        config.ensure_log_directory()
        log_dir = Path(config.log_file).parent
        assert log_dir.exists()
        
        # Test file writing permissions
        test_file = log_dir / "test_write.txt"
        test_file.write_text("test content")
        assert test_file.exists()
        
        # Test file reading
        content = test_file.read_text()
        assert content == "test content"
        
        # Clean up
        test_file.unlink()
    
    @pytest.mark.asyncio
    async def test_concurrent_requests(self, coordinator):
        """Test handling of concurrent requests."""
        
        # Mock LLM request for testing
        async def mock_llm_request(messages, **kwargs):
            await asyncio.sleep(0.1)  # Simulate processing time
            return "Mock response"
        
        coordinator._make_llm_request = mock_llm_request
        coordinator.research_agent._make_llm_request = mock_llm_request
        coordinator.content_agent._make_llm_request = mock_llm_request
        coordinator.validation_agent._make_llm_request = mock_llm_request
        
        # Create multiple concurrent requests
        tasks = []
        for i in range(3):
            input_data = {"task": f"Test task {i}"}
            task = coordinator.process(input_data)
            tasks.append(task)
        
        # Execute concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # All should complete successfully
        assert len(results) == 3
        for result in results:
            assert not isinstance(result, Exception)
            assert isinstance(result, dict)

if __name__ == "__main__":
    pytest.main([__file__])