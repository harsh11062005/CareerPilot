# 🚀 CareerAIpilot

A comprehensive AI-powered career assistance system that combines multiple agents, RAG pipelines, and interactive workflows to provide end-to-end career guidance.

## 🌟 Features

- **Multi-Agent Career Discovery**: AI agents analyze your CV and interests to identify ideal career paths
- **Resume Tailoring**: Automatic CV customization for specific job descriptions
- **Interactive Mock Interviews**: Real-time interview practice with AI coaching
- **Advanced RAG Pipelines**: Document processing with ChromaDB and FAISS
- **MCP Server Integration**: Scalable server-client architecture
- **Web Search Integration**: Real-time market research and trend analysis

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   CrewAI Agents │    │   LangGraph      │    │   RAG Pipelines │
│                 │    │   Interview      │    │                 │
│ • Career        │    │   System         │    │ • CV Processing │
│ • Resume        │    │                  │    │ • Knowledge     │
│ • Interview     │    │ • Stateful       │    │   Base          │
│                 │    │   Conversations  │    │ • ChromaDB      │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌──────────────────┐
                    │   MCP Server     │
                    │   (FastAPI)      │
                    │                  │
                    │ • Tools          │
                    │ • Resources      │
                    │ • Authentication │
                    └──────────────────┘
```

## 🚀 Quick Start

### 1. Environment Setup

```bash
# Clone or navigate to the project directory
cd CareerAIpilot

# Create environment file
cp .env.example .env
# Edit .env with your API keys:
# GOOGLE_API_KEY=your_google_api_key_here
# OPENAI_API_KEY=your_openai_api_key_here (optional)
```

### 2. Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt

# Or run the setup script
python setup.py
```

### 3. Test the System

```bash
# Run comprehensive tests
python test_system.py

# Or run individual components
python rag_pipeline.py          # Test basic RAG
python enhanced_rag_pipeline.py # Test enhanced RAG
```

### 4. Start the Application

```bash
# Start MCP server (in one terminal)
uvicorn mcp_server:app --reload

# Run main application (in another terminal)
python main.py
```

## 📁 Project Structure

```
CareerAIpilot/
├── agents.py                 # AI agent definitions
├── tasks.py                  # CrewAI task definitions
├── main.py                   # Main application entry point
├── interview_graph.py        # LangGraph interview system
├── mcp_client.py             # MCP client implementation
├── mcp_server.py             # MCP server (FastAPI)
├── rag_pipeline.py           # Basic RAG implementation
├── enhanced_rag_pipeline.py  # Advanced RAG with ChromaDB
├── test_system.py            # Comprehensive test suite
├── deploy.py                 # Deployment automation
├── setup.py                  # Quick setup script
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables
└── README.md                 # This file
```

## 🔧 Configuration

### Required Environment Variables

```bash
# Required
GOOGLE_API_KEY=your_google_api_key_here

# Optional (fallback to sentence transformers)
OPENAI_API_KEY=your_openai_api_key_here

# Server Configuration
MCP_SERVER_URL=http://127.0.0.1:8000
HOST=0.0.0.0
PORT=8000
```

### API Keys Setup

1. **Google API Key** (Required for Gemini LLM):
   - Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Add to `.env` file

2. **OpenAI API Key** (Optional for embeddings):
   - Go to [OpenAI Platform](https://platform.openai.com/api-keys)
   - Create a new API key
   - Add to `.env` file

## 🧪 Testing

### Run All Tests
```bash
python test_system.py
```

### Test Individual Components
```bash
# Test basic RAG pipeline
python rag_pipeline.py

# Test enhanced RAG pipeline
python enhanced_rag_pipeline.py

# Test MCP server
uvicorn mcp_server:app --reload
# Then visit: http://127.0.0.1:8000/docs
```

### Test Coverage
- ✅ Environment setup and API keys
- ✅ Dependencies installation
- ✅ Basic RAG pipeline (FAISS)
- ✅ Enhanced RAG pipeline (ChromaDB)
- ✅ AI agents creation
- ✅ CrewAI tasks
- ✅ LangGraph interview system
- ✅ MCP server endpoints

## 🚀 Deployment

### Development
```bash
# Start development server
uvicorn mcp_server:app --reload --host 0.0.0.0 --port 8000
```

### Production with Docker
```bash
# Create production configuration
python deploy.py

# Build and run with Docker
docker-compose up --build
```

### Production on Linux Server
```bash
# Run deployment script
python deploy.py
./deploy.sh
```

### Deployment Options
- **Docker**: Containerized deployment with docker-compose
- **Systemd**: Linux service with auto-restart
- **Nginx**: Reverse proxy with SSL support
- **Monitoring**: Health checks and logging

## 📊 Usage Examples

### 1. Career Discovery
```python
from agents import CareerAgents
from tasks import CareerTasks

# Create agents and tasks
agents = CareerAgents()
tasks = CareerTasks()

# Run career discovery
career_agent = agents.career_discovery_agent()
discover_task = tasks.discover_careers_task(career_agent, "AI and machine learning")

# Execute task
result = discover_task.execute()
```

### 2. Resume Tailoring
```python
# Tailor resume for specific job
resume_agent = agents.resume_tailoring_agent()
tailor_task = tasks.tailor_resume_task(resume_agent)

result = tailor_task.execute()
```

### 3. Mock Interview
```python
from interview_graph import interview_graph
from langchain_core.messages import HumanMessage

# Start mock interview
initial_state = {
    "messages": [HumanMessage(content="I'm ready for my AI Engineer interview")]
}

output = interview_graph.invoke(initial_state)
```

### 4. RAG Pipeline
```python
from enhanced_rag_pipeline import CVCreatorAgent

# Process CV
cv_agent = CVCreatorAgent()
cv_agent.build_cv_index("path/to/cv.pdf")

# Query CV
results = cv_agent.query_cv_index("What programming languages does the candidate know?")
```

## 🔌 API Endpoints

### MCP Server Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Discovery endpoint |
| `/invoke` | POST | Tool invocation |
| `/resources/{name}` | GET | Resource access |
| `/prompts/{name}` | GET | Prompt templates |
| `/docs` | GET | API documentation |
| `/token` | POST | Authentication |

### Example API Usage
```bash
# Get API documentation
curl http://localhost:8000/docs

# Invoke web search tool
curl -X POST http://localhost:8000/invoke \
  -H "Content-Type: application/json" \
  -d '{"tool_name": "WebSearchTool", "arguments": {"query": "AI engineer salary 2024"}}'
```

## 🛠️ Development

### Adding New Agents
```python
# In agents.py
def new_agent(self):
    return Agent(
        role='New Agent Role',
        goal="Agent's specific goal",
        backstory="Agent's background and expertise",
        verbose=True,
        llm=llm,
        allow_delegation=False
    )
```

### Adding New Tasks
```python
# In tasks.py
def new_task(self, agent):
    return Task(
        description="Task description with context",
        expected_output="Expected output format",
        agent=agent
    )
```

### Adding New Tools
```python
# In mcp_client.py
class NewTool(BaseTool):
    name: str = "NewTool"
    description: str = "Tool description for LLM"
    
    def _run(self, param: str) -> str:
        # Tool implementation
        return result
```

## 📈 Performance

### Optimization Tips
1. **Use GPU**: Install CUDA-enabled PyTorch for faster embeddings
2. **Caching**: Implement Redis for session management
3. **Database**: Use PostgreSQL for production data storage
4. **Load Balancing**: Deploy multiple server instances
5. **CDN**: Use CloudFlare for static content delivery

### Monitoring
- **Health Checks**: Built-in endpoint monitoring
- **Logging**: Structured logging with rotation
- **Metrics**: Performance and usage tracking
- **Alerts**: Automated failure notifications

## 🐛 Troubleshooting

### Common Issues

1. **API Key Errors**
   ```bash
   # Check environment variables
   python -c "import os; print(os.getenv('GOOGLE_API_KEY'))"
   ```

2. **Import Errors**
   ```bash
   # Reinstall dependencies
   pip install -r requirements.txt --force-reinstall
   ```

3. **Port Conflicts**
   ```bash
   # Use different port
   uvicorn mcp_server:app --port 8001
   ```

4. **Memory Issues**
   ```bash
   # Reduce workers
   uvicorn mcp_server:app --workers 1
   ```

### Debug Mode
```bash
# Enable debug logging
export LOG_LEVEL=DEBUG
python main.py
```

## 📚 Documentation

- **API Documentation**: http://localhost:8000/docs
- **Deployment Guide**: [DEPLOYMENT.md](DEPLOYMENT.md)
- **Architecture Overview**: See Architecture section above
- **Code Examples**: See Usage Examples section

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

### Development Setup
```bash
# Clone repository
git clone <repository-url>
cd CareerAIpilot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # If available

# Run tests
python test_system.py
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **CrewAI**: Multi-agent framework
- **LangChain**: LLM application framework
- **LangGraph**: Stateful conversation management
- **FastAPI**: Modern web framework
- **ChromaDB**: Vector database
- **Google Gemini**: Language model

## 📞 Support

For questions and support:
1. Check the troubleshooting section
2. Run the test suite: `python test_system.py`
3. Review the API documentation: http://localhost:8000/docs
4. Open an issue on GitHub (if applicable)

---

**Happy Career Building! 🚀**
