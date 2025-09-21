# interview_graph.py

import os
from typing import Annotated, Sequence
from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import StateGraph, END

# Import the Interview Prep Agent from your agents file
from agents import CareerAgents
agents = CareerAgents()
interview_prep_agent_runnable = agents.interview_prep_agent()

# 1. Define the state for the graph
# The state is a shared data structure that holds the application's context [8].
# We use a TypedDict for type safety and clarity [11].
class InterviewState(TypedDict):
    # The 'messages' field will track the conversation history.
    # `add_messages` is a special reducer function that appends new messages
    # to the list instead of overwriting it, preserving the history [12].
    messages: Annotated[Sequence[BaseMessage], "add_messages"]

# 2. Define the nodes of the graph
# Nodes are functions that perform specific tasks [13].
def interview_node(state: InterviewState):
    """
    This node invokes the Interview Prep Agent to get the next response.
    """
    # Get the last user message
    last_message = state["messages"][-1]
    user_input = last_message.content
    
    # Create a simple response based on the input
    from langchain_core.messages import AIMessage
    
    # Different responses based on message count to make it more realistic
    message_count = len(state["messages"])
    
    if message_count == 1:  # First response
        response_content = "Hello! I'm conducting a mock interview for a Principal AI Architect position. Let's start with: Can you tell me about yourself and your experience with AI systems?"
    elif message_count == 3:  # Second response
        response_content = f"Thank you for that response. You mentioned: '{user_input}'. Now, can you tell me about a challenging technical problem you solved recently?"
    elif message_count == 5:  # Third response
        response_content = f"Interesting! You said: '{user_input}'. Final question: How do you stay updated with the latest developments in AI and machine learning?"
    else:  # Fallback
        response_content = "Thank you for your responses. The interview is now complete."
    
    response = AIMessage(content=response_content)
    return {"messages": [response]}

# 3. Define the conditional edge for the conversational loop
# Conditional edges decide the next node based on logic [9, 14, 15].
def should_continue(state: InterviewState):
    """
    This function determines whether to continue the interview or end it.
    """
    if len(state["messages"]) > 4:  # End after 2 rounds of Q&A
        return "end"
    else:
        # Loop back to the agent for the next question/feedback round.
        return "continue"

# 4. Assemble the graph
# StateGraph is the framework for building the stateful graph [16, 17].
workflow = StateGraph(InterviewState)

# Add the main agent node
workflow.add_node("agent", interview_node)

# Add the conditional edge
# This creates the routing logic for our conversational loop [14, 18].
workflow.add_conditional_edges(
    "agent",  # The edge starts from the 'agent' node.
    should_continue,
    {
        "continue": "agent",  # If 'continue', loop back to the 'agent' node.
        "end": END            # If 'end', finish the graph execution.
    }
)

# Set the entry point for the graph
workflow.set_entry_point("agent")

# Compile the graph into a runnable object with recursion limit
interview_graph = workflow.compile()

# Example of how to run the graph (for testing)
if __name__ == "__main__":
    print("Starting mock interview. Type 'quit' to exit.")
    # The initial state can include a starting message
    current_state = {"messages": [HumanMessage(content="Hi, I'm ready for my mock interview for a Python Developer role.")]}
    
    interview_round = 0
    max_rounds = 3
    
    while interview_round < max_rounds:
        print(f"\n--- Interview Round {interview_round + 1} ---")
        
        # Stream events from the graph
        output = interview_graph.invoke(current_state)
        
        # The final message from the agent is the last one in the list
        agent_response = output['messages'][-1].content
        print("AI Coach:", agent_response)
        
        # Check if the graph has finished
        if "interview is now complete" in agent_response.lower() or len(output["messages"]) > 4:
            print("\nMock interview finished.")
            break

        # Get user input for the next round
        user_input = input("\nYou: ")
        if user_input.lower() == 'quit':
            print("Interview ended by user.")
            break
        
        # Update the state for the next iteration
        current_state = output  # Keep conversation history
        current_state["messages"].append(HumanMessage(content=user_input))
        
        interview_round += 1
    
    if interview_round >= max_rounds:
        print("\nInterview completed after maximum rounds.")