import os
from dotenv import load_dotenv
from crewai import Agent
from crewai.llm import LLM
# Import the MCP tool instead of any local tool implementations
from mcp_client import web_search_mcp_tool

# Load environment variables from .env file
load_dotenv()

# Get API key from environment
api_key = os.getenv("GOOGLE_API_KEY")

# Initialize the Gemini language model using CrewAI's LLM class
if api_key:
    llm = LLM(
        model="gemini/gemini-1.5-flash",
        api_key=api_key
    )
else:
    print("⚠️  Warning: GOOGLE_API_KEY not found in environment variables.")
    print("Please add your Google API key to the .env file:")
    print("GOOGLE_API_KEY=your_api_key_here")
    llm = None

class CareerAgents():
    """
    A class to define the AI agents for the career assistance crew.
    Each agent is configured with a specific role, goal, and backstory
    to ensure it performs its tasks effectively.
    """
    def career_discovery_agent(self):
        """
        Defines the Career Discovery Agent.
        This agent is responsible for researching and identifying suitable career paths.
        """
        return Agent(
            role='Senior Career Strategist',
            goal="Analyze a user's CV and interests to identify and report on 5 ideal career paths, including skills and market trends.",
            backstory=(
                "As a seasoned professional with decades of experience in labor market analysis and career coaching, "
                "you excel at identifying emerging job trends and aligning them with individual skills and aspirations "
                "to create actionable career roadmaps."
            ),
            verbose=True,
            llm=llm,
            allow_delegation=False
        )

    def resume_tailoring_agent(self):
        """
        Defines the Resume Tailoring Agent.
        This agent specializes in rewriting resumes to match specific job descriptions.
        """
        return Agent(
            role='Professional Resume Writer',
            goal="Rewrite a user's CV to perfectly align with a target job description, highlighting relevant skills and experience.",
            backstory=(
                "You are an expert resume crafter with a background in HR and recruiting. "
                "You have extensive experience creating compelling, targeted resumes that capture the attention "
                "of hiring managers and successfully pass through Applicant Tracking Systems (ATS)."
            ),
            verbose=True,
            llm=llm,
            allow_delegation=False
        )

    def interview_prep_agent(self):
        """
        Defines the Interview Preparation Agent.
        This agent conducts mock interviews and provides feedback.
        """
        return Agent(
            role='Expert Interview Coach',
            goal="Conduct a simulated, conversational interview with the user for a specific job role, asking relevant questions and providing constructive feedback.",
            backstory=(
                "As a veteran interview coach who has prepared hundreds of candidates for roles at top companies, "
                "you are skilled at simulating real interview scenarios, asking behavioral and technical questions, "
                "and providing feedback to build a user's confidence and performance."
            ),
            verbose=True,
            llm=llm,
            allow_delegation=False
        )
