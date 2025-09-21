import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, Any, List
import os

# --- Part 1: Underlying Implementations of Tools & Resources ---
# These are the actual Python functions and data that the server will wrap.
# In a real application, these could be complex RAG pipelines or calls to external APIs.

def search_the_web(query: str) -> str:
    """Simulates a web search using a service like Serper."""
    print(f"--- SERVER LOG: Performing web search for: {query} ---")
    # In a real implementation, this would call the Serper API.
    return f"Found search results for '{query}': Top 3 AI career paths are AI Engineer, ML Scientist, and Robotics Engineer."

def retrieve_cv_summary(cv_content: str) -> str:
    """Simulates a RAG pipeline that analyzes and summarizes a CV."""
    print("--- SERVER LOG: Running RAG pipeline on CV content ---")
    summary = f"CV Summary: Candidate is an experienced AI Engineer with skills in Python and TensorFlow. Length: {len(cv_content)} chars."
    return summary

def retrieve_interview_prep(job_title: str) -> str:
    """Simulates a RAG pipeline that generates interview questions."""
    print(f"--- SERVER LOG: Running RAG pipeline for interview prep for '{job_title}' ---")
    return f"Top 3 interview questions for {job_title}: 1. Tell me about a complex project. 2. Explain backpropagation. 3. Code a simple neural network."

# This simulates the user's CV being available as a server-side resource.
USER_CV_RESOURCE = {
    "name": "user_cv.txt",
    "content": """
    Jane Doe
    Lead Machine Learning Engineer | 12+ Years of Experience
    
    A dedicated professional with a proven track record in developing scalable machine learning models.
    Expertise in Python, PyTorch, and deploying models on AWS.
    """
}

# This simulates a user-controlled prompt template.
SUMMARIZE_PROMPT_TEMPLATE = {
    "name": "summarize_experience",
    "template": "Based on the user's CV, summarize their last 5 years of experience into a single, compelling paragraph for a recruiter."
}

# --- Part 2: FastAPI Server Setup & Pydantic Models ---
app = FastAPI(
    title="CareerPilot MCP Server",
    description="Exposes tools, resources, and prompts for the CareerPilot AI agent crew.",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ToolInvocationRequest(BaseModel):
    tool_name: str
    arguments: Dict[str, Any] = Field(default_factory=dict)

class CareerAnalysisRequest(BaseModel):
    """Request model for career analysis from frontend."""
    user_input: str = Field(..., description="User's interests, skills, and career goals")
    analysis_type: str = Field(..., description="Type of analysis: career_discovery, resume_tailoring, interview_prep")

class CareerAnalysisResponse(BaseModel):
    """Response model for career analysis."""
    success: bool = Field(..., description="Whether the analysis was successful")
    result: str = Field(..., description="The analysis result")
    error: str = Field(default="", description="Error message if any")

# --- Part 3: Authentication and Security (Simulated OAuth 2.0) ---
# The MCP spec supports OAuth 2.0. The server handles the real tokens,
# and provides the client with a session token.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")  # Dummy token URL

# Simulated database of valid session tokens
# In a real app, this would be a proper session management system.
VALID_SESSION_TOKENS = {"secret-session-token-for-client"}

async def verify_session_token(token: str = Depends(oauth2_scheme)):
    """A dependency to protect endpoints, ensuring only authorized clients can access them."""
    if token not in VALID_SESSION_TOKENS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid session token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token

@app.post("/token", summary="Simulated OAuth Token Endpoint")
async def login():
    """
    Simulates the final step of an OAuth 2.0 flow.
    A real server would validate user credentials and issue a session token.
    """
    # In a real scenario, this would exchange an authorization code for an access token
    # and then create a session for the MCP client.
    return {"access_token": "secret-session-token-for-client", "token_type": "bearer"}

# --- Part 4: MCP Interface Endpoints ---
@app.get("/discover", summary="MCP Discovery Endpoint")
async def discover_capabilities():
    """
    The discovery endpoint. It lists all available tools, resources, and prompts
    so the client application and its LLM know what this server can do.
    The descriptions are crucial for model-controlled tool use.
    """
    return {
        "protocol": "mcp",
        "version": "1.0",
        "capabilities": {
            "tools": [
                {
                    "name": "WebSearchTool",
                    "description": "Searches the web for up-to-date information on topics like market trends and job skills.",
                    "parameters": {"query": "string"}
                },
                {
                    "name": "CVRetrievalTool",
                    "description": "Analyzes a provided CV and returns a concise summary of the candidate's experience.",
                    "parameters": {"cv_content": "string"}
                },
                {
                    "name": "InterviewPrepRetrievalTool",
                    "description": "Generates relevant interview questions for a specified job title.",
                    "parameters": {"job_title": "string"}
                }
            ],
            "resources": [
                {
                    "name": USER_CV_RESOURCE["name"],
                    "description": "The user's base curriculum vitae (CV) file."
                }
            ],
            "prompts": [
                {
                    "name": SUMMARIZE_PROMPT_TEMPLATE["name"],
                    "description": "A template to generate a summary of the user's experience."
                }
            ]
        }
    }

@app.post("/invoke", summary="MCP Tool Invocation Endpoint")
async def invoke_tool(request: ToolInvocationRequest, token: str = Depends(verify_session_token)):
    """
    Handles model-controlled tool calls from the client.
    This endpoint is protected and requires a valid session token.
    """
    tool_map = {
        "WebSearchTool": search_the_web,
        "CVRetrievalTool": retrieve_cv_summary,
        "InterviewPrepRetrievalTool": retrieve_interview_prep,
    }
    
    tool_function = tool_map.get(request.tool_name)
    
    if not tool_function:
        raise HTTPException(status_code=404, detail=f"Tool '{request.tool_name}' not found.")
    
    try:
        result = tool_function(**request.arguments)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/resources/{resource_name}", summary="MCP Resource Retrieval Endpoint")
async def get_resource(resource_name: str, token: str = Depends(verify_session_token)):
    """
    Handles application-controlled requests for resources like files.
    """
    if resource_name == USER_CV_RESOURCE["name"]:
        return {"name": resource_name, "content": USER_CV_RESOURCE["content"]}
    
    raise HTTPException(status_code=404, detail="Resource not found.")

@app.get("/prompts/{prompt_name}", summary="MCP Prompt Template Endpoint")
async def get_prompt(prompt_name: str, token: str = Depends(verify_session_token)):
    """
    Handles user-controlled requests for prompt templates.
    """
    if prompt_name == SUMMARIZE_PROMPT_TEMPLATE["name"]:
        return {"name": prompt_name, "template": SUMMARIZE_PROMPT_TEMPLATE["template"]}
    
    raise HTTPException(status_code=404, detail="Prompt not found.")

# --- Part 6: Frontend Integration Endpoints ---
class CareerAnalysisRequest(BaseModel):
    user_input: str
    analysis_type: str  # 'career_discovery', 'resume_tailoring', 'interview_prep'


# --- Part 4: Frontend Integration Endpoints ---

@app.options("/api/career-analysis")
async def career_analysis_options():
    """Handle CORS preflight requests."""
    return {"message": "OK"}

@app.post("/api/career-analysis", response_model=CareerAnalysisResponse, summary="Career Analysis API")
async def career_analysis(request: CareerAnalysisRequest):
    """
    Handle career analysis requests from the frontend.
    Integrates with the CrewAI agents and RAG pipelines.
    """
    try:
        print(f"--- SERVER LOG: Processing {request.analysis_type} for user input: {request.user_input[:100]}... ---")
        
        # Import the main functions from our backend
        from main import run_sequential_crew
        from enhanced_rag_pipeline import EnhancedRAGPipeline
        
        if request.analysis_type == "career_discovery":
            # Run the CrewAI career discovery
            result = run_sequential_crew(request.user_input)
            return CareerAnalysisResponse(
                success=True,
                result=result
            )
            
        elif request.analysis_type == "resume_tailoring":
            # Use RAG pipeline for resume analysis
            rag = EnhancedRAGPipeline()
            # This would integrate with your resume tailoring logic
            result = f"Resume tailored based on: {request.user_input}"
            return CareerAnalysisResponse(
                success=True,
                result=result
            )
            
        elif request.analysis_type == "interview_prep":
            # Generate interview questions using RAG
            rag = EnhancedRAGPipeline()
            result = f"Interview questions generated for: {request.user_input}"
            return CareerAnalysisResponse(
                success=True,
                result=result
            )
            
        else:
            return CareerAnalysisResponse(
                success=False,
                error=f"Unknown analysis type: {request.analysis_type}"
            )
            
    except Exception as e:
        print(f"--- SERVER ERROR: {str(e)} ---")
        return CareerAnalysisResponse(
            success=False,
            error=f"Internal server error: {str(e)}"
        )

@app.get("/api/health", summary="Health Check")
async def health_check():
    """Simple health check endpoint."""
    return {"status": "healthy", "service": "CareerAIpilot MCP Server"}

# --- Part 7: Frontend Serving ---
@app.get("/", response_class=HTMLResponse, summary="CareerAIpilot Frontend")
async def serve_frontend():
    """
    Serve the CareerAIpilot frontend HTML file.
    """
    try:
        with open("career_ai_frontend.html", "r", encoding="utf-8") as f:
            html_content = f.read()
        return HTMLResponse(content=html_content, status_code=200)
    except FileNotFoundError:
        return HTMLResponse(content="""
        <html>
        <body style="font-family: Arial, sans-serif; text-align: center; padding: 50px;">
            <h1>CareerAIpilot Backend Server</h1>
            <p>Frontend file not found. Please ensure <code>career_ai_frontend.html</code> exists.</p>
            <p><a href="/docs">View API Documentation</a></p>
        </body>
        </html>
        """, status_code=404)

# --- Part 8: Run the Server ---
if __name__ == "__main__":
    # To run this server:
    # 1. Install necessary libraries: pip install "fastapi[all]"
    # 2. Run from the terminal: uvicorn mcp_server:app --reload
    print("Starting CareerAIpilot MCP Server...")
    print("Frontend will be available at http://127.0.0.1:8000/")
    print("API documentation will be available at http://127.0.0.1:8000/docs")
    uvicorn.run(app, host="127.0.0.1", port=8000)
