#!/usr/bin/env python3
"""
Setup script to create .env file and test the system
"""

import os
import subprocess
import sys

def create_env_file():
    """Create .env file with Google API key"""
    env_content = "GOOGLE_API_KEY=AIzaSyCTOcxGdHaZRk16IGq4Rp4RHjUSjgNWJ1w\n"
    
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ Created .env file with Google API key")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False

def test_environment():
    """Test if environment variables are loaded correctly"""
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv("GOOGLE_API_KEY")
        if api_key:
            print(f"✅ GOOGLE_API_KEY loaded: {api_key[:10]}...")
            return True
        else:
            print("❌ GOOGLE_API_KEY not found")
            return False
    except Exception as e:
        print(f"❌ Failed to load environment: {e}")
        return False

def test_imports():
    """Test if real system imports work"""
    try:
        from main import run_sequential_crew
        from enhanced_rag_pipeline import EnhancedRAGPipeline
        print("✅ Real system imports successful")
        return True
    except Exception as e:
        print(f"❌ Real system import failed: {e}")
        return False

def main():
    print("🚀 Setting up CareerAIpilot environment...")
    
    # Step 1: Create .env file
    if not create_env_file():
        return False
    
    # Step 2: Test environment loading
    if not test_environment():
        return False
    
    # Step 3: Test imports
    if not test_imports():
        return False
    
    print("\n🎉 Environment setup complete!")
    print("📝 Next steps:")
    print("1. Run: python mock_api.py")
    print("2. Open: http://127.0.0.1:8001/")
    print("3. Test the Career Discovery feature")
    print("4. Check terminal for LiteLLM logs (Gemini API usage)")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
