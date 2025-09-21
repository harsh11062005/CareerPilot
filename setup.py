#!/usr/bin/env python3
"""
CareerAIpilot Quick Setup Script
Handles initial setup, testing, and deployment preparation
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required. Current version:", sys.version)
        return False
    print(f"✅ Python {sys.version.split()[0]} detected")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("\n📦 Installing dependencies...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def setup_environment():
    """Setup environment variables"""
    print("\n🔧 Setting up environment...")
    
    env_file = Path(".env")
    if not env_file.exists():
        print("❌ .env file not found. Please create it with your API keys.")
        print("Required variables:")
        print("  GOOGLE_API_KEY=your_google_api_key_here")
        print("  OPENAI_API_KEY=your_openai_api_key_here (optional)")
        return False
    
    print("✅ .env file found")
    return True

def run_tests():
    """Run system tests"""
    print("\n🧪 Running system tests...")
    
    try:
        result = subprocess.run([sys.executable, "test_system.py"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ All tests passed!")
            return True
        else:
            print("❌ Some tests failed:")
            print(result.stdout)
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Failed to run tests: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 CareerAIpilot Quick Setup")
    print("=" * 40)
    
    steps = [
        ("Python Version Check", check_python_version),
        ("Install Dependencies", install_dependencies),
        ("Environment Setup", setup_environment),
        ("Run Tests", run_tests),
    ]
    
    for step_name, step_func in steps:
        print(f"\n{step_name}...")
        if not step_func():
            print(f"\n❌ Setup failed at: {step_name}")
            print("\n📋 Manual setup required:")
            print("1. Ensure Python 3.8+ is installed")
            print("2. Create .env file with API keys")
            print("3. Install dependencies: pip install -r requirements.txt")
            print("4. Run tests: python test_system.py")
            return False
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Start MCP server: uvicorn mcp_server:app --reload")
    print("2. Run main application: python main.py")
    print("3. For deployment: python deploy.py")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
