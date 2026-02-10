"""
Health checking and system monitoring for the Multi-Agent AI System.
"""

import os
import time
import psutil
from typing import Dict, List, Any
from pathlib import Path
import requests
from openai import OpenAI

class HealthChecker:
    """System health monitoring and validation."""
    
    def __init__(self, config):
        self.config = config
        self.client = OpenAI(api_key=config.openai_api_key) if config.openai_api_key else None
    
    def check_system_health(self) -> Dict[str, Any]:
        """Comprehensive system health check."""
        
        health_status = {
            "healthy": True,
            "timestamp": time.time(),
            "checks": {},
            "issues": []
        }
        
        # Check API connectivity
        api_check = self._check_api_connectivity()
        health_status["checks"]["api"] = api_check
        if not api_check["status"]:
            health_status["healthy"] = False
            health_status["issues"].append("API connectivity failed")
        
        # Check system resources
        resource_check = self._check_system_resources()
        health_status["checks"]["resources"] = resource_check
        if not resource_check["status"]:
            health_status["healthy"] = False
            health_status["issues"].append("System resources low")
        
        # Check file system
        fs_check = self._check_file_system()
        health_status["checks"]["filesystem"] = fs_check
        if not fs_check["status"]:
            health_status["healthy"] = False
            health_status["issues"].append("File system issues")
        
        # Check configuration
        config_check = self._check_configuration()
        health_status["checks"]["configuration"] = config_check
        if not config_check["status"]:
            health_status["healthy"] = False
            health_status["issues"].append("Configuration issues")
        
        return health_status
    
    def _check_api_connectivity(self) -> Dict[str, Any]:
        """Check OpenAI API connectivity."""
        
        if not self.client:
            return {
                "status": False,
                "message": "OpenAI client not initialized",
                "details": {"error": "Missing API key"}
            }
        
        try:
            # Simple API test
            response = self.client.models.list()
            return {
                "status": True,
                "message": "API connectivity OK",
                "details": {"models_available": len(list(response))}
            }
        except Exception as e:
            return {
                "status": False,
                "message": "API connectivity failed",
                "details": {"error": str(e)}
            }
    
    def _check_system_resources(self) -> Dict[str, Any]:
        """Check system resource availability."""
        
        try:
            # Check memory usage
            memory = psutil.virtual_memory()
            memory_available = memory.available / (1024**3)  # GB
            
            # Check disk space
            disk = psutil.disk_usage('/')
            disk_free = disk.free / (1024**3)  # GB
            
            # Check CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # Determine if resources are sufficient
            sufficient_memory = memory_available > 1.0  # At least 1GB
            sufficient_disk = disk_free > 1.0  # At least 1GB
            reasonable_cpu = cpu_percent < 90  # Less than 90% CPU
            
            status = sufficient_memory and sufficient_disk and reasonable_cpu
            
            return {
                "status": status,
                "message": "Resources OK" if status else "Resources low",
                "details": {
                    "memory_available_gb": round(memory_available, 2),
                    "disk_free_gb": round(disk_free, 2),
                    "cpu_percent": cpu_percent,
                    "sufficient_memory": sufficient_memory,
                    "sufficient_disk": sufficient_disk,
                    "reasonable_cpu": reasonable_cpu
                }
            }
        except Exception as e:
            return {
                "status": False,
                "message": "Resource check failed",
                "details": {"error": str(e)}
            }
    
    def _check_file_system(self) -> Dict[str, Any]:
        """Check file system permissions and directories."""
        
        try:
            # Ensure log directory exists and is writable
            self.config.ensure_log_directory()
            log_dir = Path(self.config.log_file).parent
            
            # Test write permissions
            test_file = log_dir / "health_check.tmp"
            test_file.write_text("test")
            test_file.unlink()
            
            return {
                "status": True,
                "message": "File system OK",
                "details": {
                    "log_directory": str(log_dir),
                    "writable": True
                }
            }
        except Exception as e:
            return {
                "status": False,
                "message": "File system check failed",
                "details": {"error": str(e)}
            }
    
    def _check_configuration(self) -> Dict[str, Any]:
        """Validate system configuration."""
        
        issues = []
        
        # Check required configuration
        if not self.config.openai_api_key:
            issues.append("Missing OpenAI API key")
        
        if self.config.max_retries < 1:
            issues.append("Invalid max_retries value")
        
        if self.config.timeout_seconds < 5:
            issues.append("Timeout too low")
        
        # Check file type configuration
        try:
            file_types = self.config.get_allowed_file_types()
            if not file_types:
                issues.append("No allowed file types configured")
        except Exception:
            issues.append("Invalid file types configuration")
        
        status = len(issues) == 0
        
        return {
            "status": status,
            "message": "Configuration OK" if status else "Configuration issues",
            "details": {
                "issues": issues,
                "config_valid": status
            }
        }
    
    def get_system_metrics(self) -> Dict[str, Any]:
        """Get current system metrics."""
        
        try:
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            return {
                "timestamp": time.time(),
                "memory": {
                    "total_gb": round(memory.total / (1024**3), 2),
                    "available_gb": round(memory.available / (1024**3), 2),
                    "percent_used": memory.percent
                },
                "disk": {
                    "total_gb": round(disk.total / (1024**3), 2),
                    "free_gb": round(disk.free / (1024**3), 2),
                    "percent_used": round((disk.used / disk.total) * 100, 2)
                },
                "cpu": {
                    "percent": psutil.cpu_percent(interval=1),
                    "count": psutil.cpu_count()
                }
            }
        except Exception as e:
            return {
                "error": str(e),
                "timestamp": time.time()
            }