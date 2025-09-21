#!/usr/bin/env python3
"""
CareerAIpilot Startup Script
Starts the complete system with frontend and backend
"""

import os
import sys
import subprocess
import time
import webbrowser
from pathlib import Path

def check_environment():
    """Check if environment is properly set up"""
    print("🔍 Checking environment...")
    
    # Check if .env file exists
    if not Path(".env").exists():
        print("❌ .env file not found!")
        print("Please create a .env file with your API keys:")
        print("GOOGLE_API_KEY=your_google_api_key_here")
        print("OPENAI_API_KEY=your_openai_api_key_here (optional)")
        return False
    
    # Check if frontend file exists
    if not Path("career_ai_frontend.html").exists():
        print("❌ career_ai_frontend.html not found!")
        return False
    
    print("✅ Environment check passed")
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

def start_server():
    """Start the MCP server"""
    print("\n🚀 Starting CareerAIpilot server...")
    
    try:
        # Start the server
        process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", 
            "mcp_server:app", 
            "--host", "127.0.0.1", 
            "--port", "8000",
            "--reload"
        ])
        
        # Wait a moment for server to start
        time.sleep(3)
        
        print("✅ Server started successfully!")
        print("🌐 Frontend: http://127.0.0.1:8000/")
        print("📚 API Docs: http://127.0.0.1:8000/docs")
        print("🔧 MCP Discovery: http://127.0.0.1:8000/discover")
        
        # Try to open browser
        try:
            webbrowser.open("http://127.0.0.1:8000/")
            print("🌍 Opened browser automatically")
        except:
            print("⚠️  Could not open browser automatically")
        
        print("\n" + "="*50)
        print("🎉 CareerAIpilot is running!")
        print("="*50)
        print("Press Ctrl+C to stop the server")
        print("="*50)
        
        # Wait for user to stop
        try:
            process.wait()
        except KeyboardInterrupt:
            print("\n🛑 Shutting down server...")
            process.terminate()
            process.wait()
            print("✅ Server stopped")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        return False

def main():
    """Main startup function"""
    print("🚀 CareerAIpilot Startup")
    print("=" * 40)
    
    # Check environment
    if not check_environment():
        print("\n❌ Environment check failed. Please fix the issues above.")
        return False
    
    # Install dependencies if needed
    try:
        import fastapi
        import uvicorn
        import crewai
        print("✅ Core dependencies already installed")
    except ImportError:
        if not install_dependencies():
            print("\n❌ Failed to install dependencies")
            return False
    
    # Start the server
    return start_server()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
