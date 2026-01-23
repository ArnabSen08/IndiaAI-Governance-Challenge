#!/usr/bin/env python3
"""
Deployment verification script.
Checks that all components are ready for production deployment.
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

def check_dependencies():
    """Check that all required dependencies are installed."""
    
    print("🔍 Checking Dependencies...")
    
    required_packages = [
        ('streamlit', 'streamlit'), 
        ('openai', 'openai'), 
        ('pydantic', 'pydantic'), 
        ('python-dotenv', 'dotenv'),
        ('tenacity', 'tenacity'), 
        ('loguru', 'loguru'), 
        ('psutil', 'psutil'), 
        ('pandas', 'pandas'), 
        ('numpy', 'numpy'),
        ('matplotlib', 'matplotlib'), 
        ('seaborn', 'seaborn'), 
        ('plotly', 'plotly'), 
        ('pytest', 'pytest')
    ]
    
    missing_packages = []
    
    for package_name, import_name in required_packages:
        try:
            __import__(import_name)
            print(f"   ✅ {package_name}")
        except ImportError:
            print(f"   ❌ {package_name} - MISSING")
            missing_packages.append(package_name)
    
    if missing_packages:
        print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    print("   ✅ All dependencies installed")
    return True

def check_core_imports():
    """Check that core system components can be imported."""
    
    print("\n🔍 Checking Core Imports...")
    
    try:
        from src.core.config import Config
        print("   ✅ Config")
        
        from src.utils.logger import setup_logger
        print("   ✅ Logger")
        
        from src.core.health import HealthChecker
        print("   ✅ Health Checker")
        
        from src.agents.base_agent import BaseAgent
        print("   ✅ Base Agent")
        
        from src.agents.coordinator_agent import CoordinatorAgent
        print("   ✅ Coordinator Agent")
        
        from src.agents.research_agent import ResearchAgent
        print("   ✅ Research Agent")
        
        from src.agents.content_agent import ContentAgent
        print("   ✅ Content Agent")
        
        from src.agents.validation_agent import ValidationAgent
        print("   ✅ Validation Agent")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Import failed: {e}")
        return False

def check_configuration():
    """Check configuration system."""
    
    print("\n🔍 Checking Configuration...")
    
    try:
        from src.core.config import Config
        
        # Test with minimal config
        config = Config(openai_api_key="test_key")
        print("   ✅ Configuration initialization")
        
        # Test environment file
        env_example = Path(".env.example")
        if env_example.exists():
            print("   ✅ .env.example exists")
        else:
            print("   ❌ .env.example missing")
            return False
        
        # Test log directory creation
        config.ensure_log_directory()
        log_dir = Path(config.log_file).parent
        if log_dir.exists():
            print("   ✅ Log directory creation")
        else:
            print("   ❌ Log directory creation failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"   ❌ Configuration check failed: {e}")
        return False

def check_agents():
    """Check agent initialization."""
    
    print("\n🔍 Checking Agent System...")
    
    try:
        from src.agents.coordinator_agent import CoordinatorAgent
        from src.core.config import Config
        from src.utils.logger import setup_logger
        
        config = Config(openai_api_key="test_key")
        logger = setup_logger("test", "INFO")
        
        coordinator = CoordinatorAgent(config, logger)
        print("   ✅ Coordinator initialization")
        
        # Check all agents are available
        expected_agents = ["ResearchAgent", "ContentAgent", "ValidationAgent"]
        for agent_name in expected_agents:
            if agent_name in coordinator.agents:
                print(f"   ✅ {agent_name} available")
            else:
                print(f"   ❌ {agent_name} missing")
                return False
        
        return True
        
    except Exception as e:
        print(f"   ❌ Agent check failed: {e}")
        return False

def check_tests():
    """Check test system."""
    
    print("\n🔍 Checking Test System...")
    
    try:
        # Check test directories
        test_dirs = ["tests", "tests/unit", "tests/integration", "tests/e2e"]
        for test_dir in test_dirs:
            if Path(test_dir).exists():
                print(f"   ✅ {test_dir} directory")
            else:
                print(f"   ❌ {test_dir} directory missing")
                return False
        
        # Check key test files
        key_tests = [
            "tests/unit/test_config.py",
            "tests/unit/test_base_agent.py",
            "tests/integration/test_agent_coordination.py"
        ]
        
        for test_file in key_tests:
            if Path(test_file).exists():
                print(f"   ✅ {Path(test_file).name}")
            else:
                print(f"   ❌ {test_file} missing")
                return False
        
        return True
        
    except Exception as e:
        print(f"   ❌ Test check failed: {e}")
        return False

def check_documentation():
    """Check documentation completeness."""
    
    print("\n🔍 Checking Documentation...")
    
    required_docs = [
        "README.md",
        "docs/api.md", 
        "docs/deployment.md",
        "docs/troubleshooting.md"
    ]
    
    for doc_file in required_docs:
        if Path(doc_file).exists():
            print(f"   ✅ {doc_file}")
        else:
            print(f"   ❌ {doc_file} missing")
            return False
    
    return True

def check_project_structure():
    """Check project structure."""
    
    print("\n🔍 Checking Project Structure...")
    
    required_structure = [
        "src/",
        "src/agents/",
        "src/core/",
        "src/utils/",
        "src/web/",
        "tests/",
        "docs/",
        "app.py",
        "requirements.txt",
        ".env.example"
    ]
    
    for item in required_structure:
        if Path(item).exists():
            print(f"   ✅ {item}")
        else:
            print(f"   ❌ {item} missing")
            return False
    
    return True

def main():
    """Main verification function."""
    
    print("🚀 Production Deployment Verification")
    print("=" * 60)
    
    checks = [
        ("Dependencies", check_dependencies),
        ("Core Imports", check_core_imports),
        ("Configuration", check_configuration),
        ("Agent System", check_agents),
        ("Test System", check_tests),
        ("Documentation", check_documentation),
        ("Project Structure", check_project_structure)
    ]
    
    results = []
    
    for check_name, check_func in checks:
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print(f"   💥 {check_name} check crashed: {e}")
            results.append((check_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 VERIFICATION RESULTS")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for check_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{check_name:<20} {status}")
        if result:
            passed += 1
    
    print("=" * 60)
    
    success_rate = (passed / total) * 100
    print(f"Success Rate: {success_rate:.1f}% ({passed}/{total})")
    
    if success_rate == 100:
        print("\n🎉 SYSTEM READY FOR DEPLOYMENT!")
        print("\nDeployment Instructions:")
        print("1. Set your OpenAI API key in .env file:")
        print("   cp .env.example .env")
        print("   # Edit .env and set OPENAI_API_KEY=your_actual_key")
        print("\n2. Start the application:")
        print("   streamlit run app.py")
        print("\n3. Open http://localhost:8501 in your browser")
        print("\n4. Run tests to verify functionality:")
        print("   python -m pytest tests/ -v")
        
    elif success_rate >= 80:
        print("\n⚠️  MOSTLY READY - Minor issues to resolve")
        print("Review failed checks above and fix before deployment")
        
    else:
        print("\n❌ NOT READY FOR DEPLOYMENT")
        print("Multiple critical issues need to be resolved")
    
    return success_rate == 100

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️  Verification interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n💥 Verification failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)