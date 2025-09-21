# main.py
from crewai import Crew, Process
from langchain_core.messages import HumanMessage

# Import the agent and task classes from your other files
from agents import CareerAgents
from tasks import CareerTasks
# Note: Interview functionality is now implemented as a simple function to avoid LangGraph recursion issues

def run_sequential_crew(user_interests: str):
    """
    Assembles and runs the sequential part of the workflow using CrewAI.
    """
    print("--- Starting Career Discovery and Resume Tailoring Crew ---")
    
    # 1. Instantiate agents and tasks
    agents = CareerAgents()
    tasks = CareerTasks()

    # Create agent instances
    career_discovery_agent = agents.career_discovery_agent()
    resume_tailoring_agent = agents.resume_tailoring_agent()
    
    # Create task instances
    # Note: These tasks are designed to use the MCP client.
    # The 'discover_careers_task' will use the agent's WebSearchMCPTool.
    # Both tasks will call the MCP resource accessor to get the user's CV.
    discover_task = tasks.discover_careers_task(
        agent=career_discovery_agent, 
        user_interests=user_interests
    )
    
    tailor_task = tasks.tailor_resume_task(
        agent=resume_tailoring_agent
    )

    # 2. Assemble the Crew
    # The Crew brings together agents and tasks to execute the workflow.
    crew = Crew(
        agents=[career_discovery_agent, resume_tailoring_agent],
        tasks=[discover_task, tailor_task],
        process=Process.sequential,  # Defines a sequential execution process [4]
        verbose=True
    )

    # 3. Kick off the Crew
    # The kickoff() method starts the execution.
    # The output of discover_task is automatically passed as context to tailor_task.
    result = crew.kickoff()
    
    print("\n--- Sequential Crew Finished ---")
    print("Final Report and Tailored Resume:")
    print(result)
    
    return result

def run_interview_graph():
    """
    Runs the interactive mock interview using a simple function approach.
    """
    print("\n--- Starting Interactive Interview Preparation ---")
    print("Mock interview initiated. Type 'quit' to end the session.")
    
    # Simple interview questions
    questions = [
        "Hello! I'm conducting a mock interview for a Principal AI Architect position. Let's start with: Can you tell me about yourself and your experience with AI systems?",
        "Thank you for that response. Now, can you tell me about a challenging technical problem you solved recently?",
        "Interesting! Final question: How do you stay updated with the latest developments in AI and machine learning?"
    ]
    
    # Interactive loop for the conversational agent
    for i, question in enumerate(questions):
        print(f"\n--- Interview Round {i + 1} ---")
        print("\nAI Coach:", question)
        
        # Get user input
        user_input = input("\nYou: ")
        if user_input.lower() == 'quit':
            print("Interview ended by user.")
            break
        
        print(f"Thank you for your response: '{user_input}'")
    
    print("\n--- Mock interview finished. ---")

if __name__ == "__main__":
    # Define user's high-level interests to start the process
    interests = "I am interested in roles related to artificial intelligence, specifically in building agentic systems and working with large language models."
    
    # --- Part 1: Run the sequential CrewAI process ---
    run_sequential_crew(user_interests=interests)
    
    # --- Part 2: Run the stateful LangGraph process ---
    run_interview_graph()