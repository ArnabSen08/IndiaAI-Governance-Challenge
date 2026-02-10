"""
Unit tests for Config class.
"""

import pytest
import os
import tempfile
from pathlib import Path
import sys

# Add src to path
sys.path.append(str(Path(__file__).parent.parent.parent / "src"))

from src.core.config import Config
from pydantic import ValidationError

class TestConfig:
    """Test cases for Config class."""
    
    def test_config_initialization_with_defaults(self):
        """Test config initialization with default values."""
        config = Config(openai_api_key="test_key")
        
        assert config.openai_api_key == "test_key"
        assert config.openai_model == "gpt-4"
        assert config.max_retries == 3
        assert config.timeout_seconds == 30
        assert config.log_level == "INFO"
    
    def test_config_initialization_with_custom_values(self):
        """Test config initialization with custom values."""
        config = Config(
            openai_api_key="custom_key",
            max_retries=5,
            timeout_seconds=60,
            log_level="DEBUG"
        )
        
        assert config.openai_api_key == "custom_key"
        assert config.max_retries == 5
        assert config.timeout_seconds == 60
        assert config.log_level == "DEBUG"
    
    def test_config_validation_invalid_api_key(self):
        """Test config validation with invalid API key."""
        with pytest.raises(ValidationError):
            Config(openai_api_key="")
        
        with pytest.raises(ValidationError):
            Config(openai_api_key="your_openai_api_key_here")
    
    def test_config_validation_invalid_log_level(self):
        """Test config validation with invalid log level."""
        with pytest.raises(ValidationError):
            Config(openai_api_key="test_key", log_level="INVALID")
    
    def test_config_validation_invalid_ranges(self):
        """Test config validation with values outside valid ranges."""
        with pytest.raises(ValidationError):
            Config(openai_api_key="test_key", max_retries=0)
        
        with pytest.raises(ValidationError):
            Config(openai_api_key="test_key", timeout_seconds=1)
        
        with pytest.raises(ValidationError):
            Config(openai_api_key="test_key", max_iterations=0)
    
    def test_get_allowed_file_types(self):
        """Test getting allowed file types."""
        config = Config(
            openai_api_key="test_key",
            allowed_file_types="txt,md,json,py"
        )
        
        file_types = config.get_allowed_file_types()
        assert file_types == ["txt", "md", "json", "py"]
    
    def test_get_allowed_file_types_with_spaces(self):
        """Test getting allowed file types with spaces."""
        config = Config(
            openai_api_key="test_key",
            allowed_file_types="txt, md , json,  py  "
        )
        
        file_types = config.get_allowed_file_types()
        assert file_types == ["txt", "md", "json", "py"]
    
    def test_ensure_log_directory(self):
        """Test ensuring log directory exists."""
        with tempfile.TemporaryDirectory() as temp_dir:
            log_file = Path(temp_dir) / "logs" / "test.log"
            config = Config(
                openai_api_key="test_key",
                log_file=str(log_file)
            )
            
            # Directory shouldn't exist initially
            assert not log_file.parent.exists()
            
            # Ensure directory
            config.ensure_log_directory()
            
            # Directory should now exist
            assert log_file.parent.exists()
    
    def test_to_dict(self):
        """Test converting config to dictionary."""
        config = Config(
            openai_api_key="test_key",
            max_retries=5,
            debug_mode=True
        )
        
        config_dict = config.to_dict()
        
        assert isinstance(config_dict, dict)
        assert config_dict["openai_api_key"] == "test_key"
        assert config_dict["max_retries"] == 5
        assert config_dict["debug_mode"] is True
    
    def test_environment_variable_override(self):
        """Test that environment variables override defaults."""
        # Set environment variables
        os.environ["OPENAI_API_KEY"] = "env_key"
        os.environ["MAX_RETRIES"] = "7"
        os.environ["DEBUG_MODE"] = "true"
        
        try:
            config = Config()
            
            assert config.openai_api_key == "env_key"
            assert config.max_retries == 7
            assert config.debug_mode is True
            
        finally:
            # Clean up environment variables
            os.environ.pop("OPENAI_API_KEY", None)
            os.environ.pop("MAX_RETRIES", None)
            os.environ.pop("DEBUG_MODE", None)
    
    def test_boolean_environment_variables(self):
        """Test boolean environment variable parsing."""
        test_cases = [
            ("true", True),
            ("True", True),
            ("TRUE", True),
            ("false", False),
            ("False", False),
            ("FALSE", False),
            ("anything_else", False)
        ]
        
        for env_value, expected in test_cases:
            os.environ["DEBUG_MODE"] = env_value
            
            try:
                config = Config(openai_api_key="test_key")
                assert config.debug_mode == expected
            finally:
                os.environ.pop("DEBUG_MODE", None)

if __name__ == "__main__":
    pytest.main([__file__])