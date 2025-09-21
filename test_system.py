#!/usr/bin/env python3
"""
Comprehensive Test Suite for CareerAIpilot
Tests all components: RAG pipelines, agents, MCP server, and main workflow
"""

import os
import sys
import time
import subprocess
import requests
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_environment():
    """Test environment setup and API keys"""
    print("🔍 Testing Environment Setup...")
    
    required_vars = ['GOOGLE_API_KEY']
    optional_vars = ['OPENAI_API_KEY']
    
    for var in required_vars:
        if not os.getenv(var) or os.getenv(var) == f"your_{var.lower()}_here":
            print(f"❌ {var} not properly configured")
            return False
        else:
            print(f"✅ {var} configured")
    
    for var in optional_vars:
        if os.getenv(var) and os.getenv(var) != f"your_{var.lower()}_here":
            print(f"✅ {var} configured")
        else:
            print(f"⚠️  {var} not configured (optional)")
    
    return True

def test_dependencies():
    """Test if all required packages are installed"""
    print("\n📦 Testing Dependencies...")
    
    required_packages = [
        'crewai', 'langchain', 'langgraph', 'chromadb', 
        'fastapi', 'uvicorn', 'sentence_transformers'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package}")
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    return True

def test_rag_pipeline():
    """Test basic RAG pipeline"""
    print("\n🔍 Testing Basic RAG Pipeline...")
    
    try:
        from rag_pipeline import CVRAGPipeline
        
        # Test with sample CV
        cv_path = "test_sample_cv.txt"
        if not os.path.exists(cv_path):
            print(f"❌ Sample CV file not found: {cv_path}")
            return False
        
        pipeline = CVRAGPipeline()
        success = pipeline.build_cv_index(cv_path)
        
        if success:
            print("✅ CV index built successfully")
            
            # Test querying
            results = pipeline.query_cv_index("What programming languages does John know?", top_k=3)
            if results:
                print(f"✅ Query successful, found {len(results)} results")
                return True
            else:
                print("❌ Query failed")
                return False
        else:
            print("❌ Failed to build CV index")
            return False
            
    except Exception as e:
        print(f"❌ RAG pipeline test failed: {str(e)}")
        return False

def test_enhanced_rag_pipeline():
    """Test enhanced RAG pipeline"""
    print("\n🚀 Testing Enhanced RAG Pipeline...")
    
    try:
        from enhanced_rag_pipeline import CVCreatorAgent, InterviewPrepGeneratorAgent
        
        # Test CV Creator Agent
        cv_agent = CVCreatorAgent()
        success = cv_agent.build_cv_index("test_sample_cv.txt")
        
        if success:
            print("✅ CV Creator Agent working")
            
            # Test querying
            results = cv_agent.query_cv_index("What is John's experience?", top_k=2)
            if results:
                print(f"✅ CV query successful, found {len(results)} results")
            else:
                print("❌ CV query failed")
                return False
        else:
            print("❌ CV Creator Agent failed")
            return False
        
        # Test Interview Prep Generator Agent
        interview_agent = InterviewPrepGeneratorAgent()
        success = interview_agent.build_interview_knowledge_base("test_interview_knowledge.txt")
        
        if success:
            print("✅ Interview Prep Generator Agent working")
            
            # Test question generation
            job_desc = "Senior AI Engineer position"
            cv_content = open("test_sample_cv.txt").read()
            questions = interview_agent.generate_interview_questions(job_desc, cv_content, ['technical', 'behavioral'])
            
            if questions:
                print(f"✅ Generated {sum(len(q) for q in questions.values())} interview questions")
                return True
            else:
                print("❌ Question generation failed")
                return False
        else:
            print("❌ Interview Prep Generator Agent failed")
            return False
            
    except Exception as e:
        print(f"❌ Enhanced RAG pipeline test failed: {str(e)}")
        return False

def test_agents():
    """Test AI agents"""
    print("\n🤖 Testing AI Agents...")
    
    try:
        from agents import CareerAgents
        
        agents = CareerAgents()
        
        # Test agent creation
        career_agent = agents.career_discovery_agent()
        resume_agent = agents.resume_tailoring_agent()
        interview_agent = agents.interview_prep_agent()
        
        if all([career_agent, resume_agent, interview_agent]):
            print("✅ All agents created successfully")
            return True
        else:
            print("❌ Some agents failed to create")
            return False
            
    except Exception as e:
        print(f"❌ Agents test failed: {str(e)}")
        return False

def test_mcp_server():
    """Test MCP server"""
    print("\n🌐 Testing MCP Server...")
    
    server_process = None
    
    try:
        # Start MCP server in background
        print("Starting MCP server...")
        server_process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", 
            "mcp_server:app", 
            "--host", "127.0.0.1", 
            "--port", "8000"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for server to start
        time.sleep(5)
        
        # Test server endpoints
        base_url = "http://127.0.0.1:8000"
        
        # Test discovery endpoint
        response = requests.get(f"{base_url}/", timeout=10)
        if response.status_code == 200:
            print("✅ MCP server discovery endpoint working")
        else:
            print(f"❌ Discovery endpoint failed: {response.status_code}")
            return False
        
        # Test token endpoint
        response = requests.post(f"{base_url}/token", timeout=10)
        if response.status_code == 200:
            print("✅ MCP server token endpoint working")
        else:
            print(f"❌ Token endpoint failed: {response.status_code}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ MCP server test failed: {str(e)}")
        return False
        
    finally:
        if server_process:
            server_process.terminate()
            server_process.wait()

def test_tasks():
    """Test CrewAI tasks"""
    print("\n📋 Testing CrewAI Tasks...")
    
    try:
        from tasks import CareerTasks
        
        tasks = CareerTasks()
        
        # Test task creation (without actually running them)
        # We'll just check if they can be instantiated
        print("✅ Tasks module imported successfully")
        return True
        
    except Exception as e:
        print(f"❌ Tasks test failed: {str(e)}")
        return False

def test_interview_graph():
    """Test LangGraph interview system"""
    print("\n🔄 Testing Interview Graph...")
    
    try:
        from interview_graph import interview_graph, InterviewState
        from langchain_core.messages import HumanMessage
        
        # Test graph compilation
        if interview_graph:
            print("✅ Interview graph compiled successfully")
            
            # Test a simple invocation (without full interview)
            initial_state = {"messages": [HumanMessage(content="Hello, I'm ready for an interview.")]}
            
            # This would normally run the full interview, but we'll just test compilation
            print("✅ Interview graph ready for use")
            return True
        else:
            print("❌ Interview graph compilation failed")
            return False
            
    except Exception as e:
        print(f"❌ Interview graph test failed: {str(e)}")
        return False

def run_comprehensive_test():
    """Run all tests"""
    print("🧪 CareerAIpilot Comprehensive Test Suite")
    print("=" * 50)
    
    tests = [
        ("Environment Setup", test_environment),
        ("Dependencies", test_dependencies),
        ("Basic RAG Pipeline", test_rag_pipeline),
        ("Enhanced RAG Pipeline", test_enhanced_rag_pipeline),
        ("AI Agents", test_agents),
        ("CrewAI Tasks", test_tasks),
        ("Interview Graph", test_interview_graph),
        ("MCP Server", test_mcp_server),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} test crashed: {str(e)}")
            results[test_name] = False
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    passed = 0
    total = len(tests)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<25} {status}")
        if result:
            passed += 1
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is ready for deployment.")
        return True
    else:
        print("⚠️  Some tests failed. Please fix issues before deployment.")
        return False

if __name__ == "__main__":
    success = run_comprehensive_test()
    sys.exit(0 if success else 1)
