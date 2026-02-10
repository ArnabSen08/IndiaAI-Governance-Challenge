"""
Unit tests for ValidationAgent class.
"""

import pytest
import asyncio
import logging
from unittest.mock import Mock, AsyncMock, patch
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent.parent / "src"))

from src.agents.validation_agent import ValidationAgent
from src.core.config import Config

class TestValidationAgent:
    """Test cases for ValidationAgent."""
    
    @pytest.fixture
    def config(self):
        """Create test configuration."""
        return Config(
            openai_api_key="test_key",
            enable_output_filtering=True,
            max_input_length=1000
        )
    
    @pytest.fixture
    def logger(self):
        """Create test logger."""
        return logging.getLogger("test")
    
    @pytest.fixture
    def agent(self, config, logger):
        """Create validation agent instance."""
        return ValidationAgent(config, logger)
    
    def test_agent_initialization(self, agent):
        """Test validation agent initialization."""
        assert agent.name == "ValidationAgent"
        assert "validations_performed" in agent.quality_metrics
        assert len(agent.safety_patterns) > 0
    
    def test_validate_input_valid(self, agent):
        """Test input validation with valid data."""
        valid_input = {"content": "test content", "validation_type": "safety"}
        assert agent.validate_input(valid_input) is True
    
    def test_validate_input_missing_content(self, agent):
        """Test input validation with missing content."""
        invalid_input = {"validation_type": "safety"}
        assert agent.validate_input(invalid_input) is False
    
    def test_validate_input_invalid_type(self, agent):
        """Test input validation with invalid validation type."""
        invalid_input = {"content": "test", "validation_type": "invalid"}
        assert agent.validate_input(invalid_input) is False
    
    @pytest.mark.asyncio
    async def test_safety_validation_clean_content(self, agent):
        """Test safety validation with clean content."""
        with patch.object(agent, '_llm_safety_check') as mock_safety:
            mock_safety.return_value = {"issues": []}
            
            input_data = {"content": "This is clean content", "validation_type": "safety"}
            result = await agent.process(input_data)
            
            assert result["success"] is True
            assert result["validation_passed"] is True
            assert len(result["safety_issues"]) == 0
    
    @pytest.mark.asyncio
    async def test_safety_validation_with_issues(self, agent):
        """Test safety validation with safety issues."""
        with patch.object(agent, '_llm_safety_check') as mock_safety:
            mock_safety.return_value = {
                "issues": [{
                    "type": "test_issue",
                    "severity": "high",
                    "description": "Test safety issue"
                }]
            }
            
            input_data = {"content": "Content with api_key", "validation_type": "safety"}
            result = await agent.process(input_data)
            
            assert result["success"] is True
            assert result["validation_passed"] is False
            assert len(result["safety_issues"]) > 0
    
    @pytest.mark.asyncio
    async def test_quality_validation(self, agent):
        """Test quality validation."""
        with patch.object(agent, '_llm_quality_check') as mock_quality:
            mock_quality.return_value = {"issues": []}
            
            input_data = {"content": "High quality content with proper structure.", "validation_type": "quality"}
            result = await agent.process(input_data)
            
            assert result["success"] is True
            assert "quality_score" in result
            assert "readability_score" in result
    
    @pytest.mark.asyncio
    async def test_technical_validation(self, agent):
        """Test technical validation."""
        with patch.object(agent, '_llm_technical_check') as mock_technical:
            mock_technical.return_value = {"issues": []}
            
            code_content = """
            ```python
            def hello_world():
                print("Hello, World!")
            ```
            """
            
            input_data = {"content": code_content, "validation_type": "technical"}
            result = await agent.process(input_data)
            
            assert result["success"] is True
            assert "technical_score" in result
            assert result["code_blocks_found"] == 1
    
    @pytest.mark.asyncio
    async def test_comprehensive_validation(self, agent):
        """Test comprehensive validation."""
        with patch.object(agent, '_llm_safety_check') as mock_safety, \
             patch.object(agent, '_llm_quality_check') as mock_quality:
            
            mock_safety.return_value = {"issues": []}
            mock_quality.return_value = {"issues": []}
            
            input_data = {"content": "Test content for comprehensive validation"}
            result = await agent.process(input_data)
            
            assert result["success"] is True
            assert result["validation_type"] == "comprehensive"
            assert "safety_score" in result
            assert "quality_score" in result
            assert "overall_score" in result
    
    def test_check_basic_quality_short_content(self, agent):
        """Test basic quality check with short content."""
        issues = agent._check_basic_quality("short", False)
        
        # Should detect content too short
        assert any(issue["type"] == "length" for issue in issues)
    
    def test_check_basic_quality_repetitive_content(self, agent):
        """Test basic quality check with repetitive content."""
        repetitive_content = "test " * 50  # Very repetitive
        issues = agent._check_basic_quality(repetitive_content, False)
        
        # Should detect repetition
        assert any(issue["type"] == "repetition" for issue in issues)
    
    def test_validate_code_block_balanced(self, agent):
        """Test code block validation with balanced brackets."""
        code = "def func(): return {'key': 'value'}"
        issues = agent._validate_code_block(code, 0)
        
        assert len(issues) == 0
    
    def test_validate_code_block_unbalanced(self, agent):
        """Test code block validation with unbalanced brackets."""
        code = "def func(): return {'key': 'value'"  # Missing closing brace
        issues = agent._validate_code_block(code, 0)
        
        assert len(issues) > 0
        assert any(issue["type"] == "syntax" for issue in issues)
    
    def test_calculate_readability_score(self, agent):
        """Test readability score calculation."""
        # Good readability - moderate sentence length
        good_content = "This is a sentence. This is another sentence with moderate length."
        good_score = agent._calculate_readability_score(good_content)
        
        # Poor readability - very long sentences
        poor_content = "This is an extremely long sentence that goes on and on without any breaks and contains way too many words for good readability and should be broken up into smaller more manageable pieces."
        poor_score = agent._calculate_readability_score(poor_content)
        
        assert good_score > poor_score
    
    def test_generate_recommendations_no_issues(self, agent):
        """Test recommendation generation with no issues."""
        recommendations = agent._generate_recommendations([])
        
        assert len(recommendations) == 1
        assert "meets validation standards" in recommendations[0]
    
    def test_generate_recommendations_with_issues(self, agent):
        """Test recommendation generation with various issues."""
        issues = [
            {"type": "safety", "severity": "high"},
            {"type": "quality", "severity": "medium"},
            {"type": "syntax", "severity": "high"}
        ]
        
        recommendations = agent._generate_recommendations(issues)
        
        assert len(recommendations) > 1
        assert any("safety" in rec for rec in recommendations)
        assert any("quality" in rec for rec in recommendations)
        assert any("syntax" in rec for rec in recommendations)
    
    def test_get_validation_metrics(self, agent):
        """Test getting validation metrics."""
        # Simulate some validations
        agent.quality_metrics["validations_performed"] = 10
        agent.quality_metrics["validations_passed"] = 8
        agent.quality_metrics["safety_issues_detected"] = 3
        agent.quality_metrics["quality_issues_detected"] = 5
        
        metrics = agent.get_validation_metrics()
        
        assert metrics["validations_performed"] == 10
        assert metrics["pass_rate"] == 80.0
        assert metrics["avg_safety_issues"] == 0.3
        assert metrics["avg_quality_issues"] == 0.5
    
    def test_safety_patterns_initialization(self, agent):
        """Test that safety patterns are properly initialized."""
        patterns = agent.safety_patterns
        
        assert "personal_info" in patterns
        assert "harmful_instructions" in patterns
        assert "inappropriate_content" in patterns
        
        # Check that patterns are actually regex patterns
        for category, pattern_list in patterns.items():
            assert isinstance(pattern_list, list)
            assert len(pattern_list) > 0

if __name__ == "__main__":
    pytest.main([__file__])