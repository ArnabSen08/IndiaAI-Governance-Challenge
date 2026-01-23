#!/usr/bin/env python3
"""
Simple system test script to verify the multi-agent system works.
This script tests the system without requiring actual API calls.
"""

import asyncio
import sys
import os
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from src.agents.coordinator_agent import CoordinatorAgent
from src.core.config import Config
from src.core.health import HealthChecker
from src.utils.logger import setup_logger

async def mock_llm_request(messages, **kwargs):
    """Mock LLM request for testing without API calls."""
    
    # Simulate different responses based on message content
    content = str(messages).lower()
    
    if "workflow" in content or "plan" in content:
        return '''
        Based on the task, I recommend the following workflow:
        1. Research the topic to gather relevant information
        2. Generate comprehensive content based on findings
        3. Validate the content for quality and safety
        '''
    elif "research" in content:
        return "Research findings: This is a comprehensive analysis of the requested topic with relevant information and insights."
    elif "content" in content or "generate" in content:
        return "Generated content: This is well-structured, informative content that addresses the user's request effectively."
    elif "validat" in content:
        return "Validation complete: Content meets all quality and safety standards."
    else:
        return "Mock response for testing purposes."

async def test_system_components():
    """Test individual system components."""
    
    print("🧪 Testing System Components")
    print("=" * 50)
    
    # Test configuration
    print("1. Testing Configuration...")
    try:
        config = Config(openai_api_key="test_key_for_system_test")
        print("   ✅ Configuration loaded successfully")
        print(f"   - Model: {config.openai_model}")
        print(f"   - Max Retries: {config.max_retries}")
        print(f"   - Timeout: {config.timeout_seconds}s")
    except Exception as e:
        print(f"   ❌ Configuration failed: {e}")
        return False
    
    # Test logging
    print("\n2. Testing Logging...")
    try:
        logger = setup_logger("system_test", config.log_level)
        logger.info("Test log message")
        print("   ✅ Logging system working")
    except Exception as e:
        print(f"   ❌ Logging failed: {e}")
        return False
    
    # Test health checker
    print("\n3. Testing Health Checker...")
    try:
        health_checker = HealthChecker(config)
        # Note: This will show API connectivity failure, which is expected
        health_status = health_checker.check_system_health()
        print("   ✅ Health checker working")
        print(f"   - System healthy: {health_status['healthy']}")
        print(f"   - Checks performed: {len(health_status['checks'])}")
    except Exception as e:
        print(f"   ❌ Health checker failed: {e}")
        return False
    
    # Test coordinator initialization
    print("\n4. Testing Coordinator Agent...")
    try:
        coordinator = CoordinatorAgent(config, logger)
        print("   ✅ Coordinator initialized successfully")
        print(f"   - Available agents: {list(coordinator.agents.keys())}")
    except Exception as e:
        print(f"   ❌ Coordinator initialization failed: {e}")
        return False
    
    return True, coordinator, config, logger

async def test_workflow_execution(coordinator):
    """Test complete workflow execution."""
    
    print("\n🔄 Testing Workflow Execution")
    print("=" * 50)
    
    # Mock the LLM requests to avoid API calls
    coordinator._make_llm_request = mock_llm_request
    coordinator.research_agent._make_llm_request = mock_llm_request
    coordinator.content_agent._make_llm_request = mock_llm_request
    coordinator.validation_agent._make_llm_request = mock_llm_request
    
    # Test cases
    test_cases = [
        {
            "name": "Simple Explanation Request",
            "input": {
                "task": "Explain how photosynthesis works",
                "context": {"audience": "students"}
            }
        },
        {
            "name": "Technical Documentation",
            "input": {
                "task": "Create API documentation for user authentication",
                "context": {"type": "technical", "format": "markdown"}
            }
        },
        {
            "name": "Research Query",
            "input": {
                "task": "Research the benefits of renewable energy",
                "context": {"depth": "comprehensive"}
            }
        }
    ]
    
    results = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. {test_case['name']}")
        try:
            result = await coordinator.process(test_case["input"])
            
            if result.get("success"):
                print("   ✅ Workflow completed successfully")
                print(f"   - Workflow steps: {len(result.get('workflow_plan', {}).get('steps', []))}")
                print(f"   - Final output length: {len(str(result.get('result', {}).get('final_output', '')))}")
                results.append(True)
            else:
                print(f"   ❌ Workflow failed: {result.get('error', 'Unknown error')}")
                results.append(False)
                
        except Exception as e:
            print(f"   ❌ Workflow execution error: {e}")
            results.append(False)
    
    success_rate = sum(results) / len(results) * 100
    print(f"\n📊 Workflow Success Rate: {success_rate:.1f}% ({sum(results)}/{len(results)})")
    
    return success_rate > 50  # At least 50% success rate

def test_metrics_and_monitoring(coordinator):
    """Test metrics collection and monitoring."""
    
    print("\n📊 Testing Metrics and Monitoring")
    print("=" * 50)
    
    try:
        # Test agent metrics
        print("1. Agent Metrics...")
        metrics = coordinator.get_all_agent_metrics()
        print(f"   ✅ Collected metrics from {len(metrics)} agents")
        
        for agent_name, agent_metrics in metrics.items():
            print(f"   - {agent_name}: {agent_metrics['requests']} requests, {agent_metrics['success_rate']}% success")
        
        # Test workflow history
        print("\n2. Workflow History...")
        history = coordinator.get_workflow_history()
        print(f"   ✅ Workflow history: {len(history)} entries")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Metrics collection failed: {e}")
        return False

async def main():
    """Main test function."""
    
    print("🚀 Multi-Agent AI System - System Test")
    print("=" * 60)
    print("This test verifies system functionality without API calls")
    print("=" * 60)
    
    # Test system components
    component_test = await test_system_components()
    if not component_test[0]:
        print("\n❌ Component tests failed. Exiting.")
        return False
    
    coordinator = component_test[1]
    
    # Test workflow execution
    workflow_success = await test_workflow_execution(coordinator)
    
    # Test metrics and monitoring
    metrics_success = test_metrics_and_monitoring(coordinator)
    
    # Overall results
    print("\n" + "=" * 60)
    print("📋 SYSTEM TEST RESULTS")
    print("=" * 60)
    
    tests = [
        ("Component Initialization", component_test[0]),
        ("Workflow Execution", workflow_success),
        ("Metrics & Monitoring", metrics_success)
    ]
    
    all_passed = True
    for test_name, passed in tests:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name:<25} {status}")
        if not passed:
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("🎉 ALL TESTS PASSED - System is ready for deployment!")
        print("\nNext steps:")
        print("1. Set your OpenAI API key in .env file")
        print("2. Run: streamlit run app.py")
        print("3. Open http://localhost:8501 in your browser")
    else:
        print("⚠️  Some tests failed - please review the issues above")
    
    return all_passed

if __name__ == "__main__":
    try:
        success = asyncio.run(main())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️  Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n💥 Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)