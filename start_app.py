#!/usr/bin/env python3
"""
CareerAIpilot Startup Script
Starts the MCP server with frontend integration
"""

import subprocess
import sys
import time
import webbrowser
import os
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import fastapi
        import uvicorn
        import crewai
        print("✅ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def check_env_file():
    """Check if .env file exists and has required keys"""
    env_file = Path(".env")
    if not env_file.exists():
        print("❌ .env file not found")
        print("Please create a .env file with your API keys:")
        print("GOOGLE_API_KEY=your_google_api_key_here")
        print("OPENAI_API_KEY=your_openai_api_key_here")
        return False
    
    with open(env_file, 'r') as f:
        content = f.read()
        if 'GOOGLE_API_KEY=' not in content or 'GOOGLE_API_KEY=your_' in content:
            print("⚠️  GOOGLE_API_KEY not properly configured in .env file")
            return False
    
    print("✅ Environment file configured")
    return True

def start_server():
    """Start the MCP server"""
    print("🚀 Starting CareerAIpilot MCP Server...")
    print("📍 Server will be available at: http://localhost:8000")
    print("📖 API documentation: http://localhost:8000/docs")
    print("🌐 Frontend interface: http://localhost:8000")
    print("\nPress Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        # Start the server
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "mcp_server:app", 
            "--host", "127.0.0.1", 
            "--port", "8000",
            "--reload"
        ])
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

def main():
    """Main startup function"""
    print("🎯 CareerAIpilot - AI-Powered Career Assistant")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        return
    
    # Check environment
    if not check_env_file():
        return
    
    # Wait a moment then open browser
    print("\n🌐 Opening browser in 3 seconds...")
    time.sleep(3)
    
    try:
        webbrowser.open("http://localhost:8000")
    except Exception as e:
        print(f"⚠️  Could not open browser automatically: {e}")
        print("Please manually open: http://localhost:8000")
    
    # Start the server
    start_server()

if __name__ == "__main__":
    main()
