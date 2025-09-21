# tools/mcp_client.py

from crewai.tools import BaseTool

# --- 1. Simulate the MCP Client Library ---
# In a real-world scenario, this might be an imported library like `langgraph_mcp_adapter`.
# It handles the connection and communication with the MCP server.

class MCPClient:
    """
    A simulated client to connect to and interact with an MCP server.
    This class abstracts away the network communication details.
    """
    def __init__(self, server_url: str):
        self.server_url = server_url
        print(f"MCP Client initialized for server at: {self.server_url}")
        # A real implementation would establish a persistent connection,
        # possibly using Server-Sent Events (SSE) for remote servers [6].

    def invoke_tool(self, tool_name: str, **kwargs) -> str:
        """
        Simulates making a request to the MCP server to invoke a tool.
        This is a "model-controlled" action [7].
        """
        print(f"--> MCP CLIENT: Invoking tool '{tool_name}' on server with args: {kwargs}")
        # In a real implementation, this would make an API call (e.g., HTTP POST)
        # to the server's endpoint, sending the tool name and arguments.
        # The server would then execute the tool and return the result.
        
        # We'll return a mock response for demonstration.
        if tool_name == "WebSearchTool":
            query = kwargs.get('query', 'no query provided')
            return f"[Mock Result from MCP Server]: Successfully searched the web for '{query}' and found relevant articles on AI careers."
        
        return f"[Mock Result from MCP Server]: Result for tool '{tool_name}'."

    def get_resource(self, resource_name: str) -> str:
        """
        Simulates requesting a resource from the MCP server.
        This is an "application-controlled" action [7].
        """
        print(f"--> MCP CLIENT: Requesting resource '{resource_name}' from server.")
        # This would make an API call (e.g., HTTP GET) to the server's
        # resource endpoint. The server would return the resource's content.

        if resource_name == "user_cv.txt":
            return """
            --- MOCK CV FROM MCP SERVER ---
            John Doe
            Senior AI Engineer | 10+ Years of Experience

            Summary:
            A highly motivated AI Engineer with extensive experience in developing and deploying
            machine learning models. Proficient in Python, TensorFlow, and cloud platforms.
            Seeking to leverage my skills to build innovative AI-driven solutions.
            
            Experience:
            - Lead AI Engineer, TechCorp (2018-Present)
            - Machine Learning Developer, Innovate Inc. (2014-2018)
            --------------------------------
            """
        return f"Content of resource '{resource_name}' from MCP server."

# --- 2. Define Client-Side Tools and Resource Accessors ---
# These are the functions that the CrewAI agents and tasks will be given.
# They use the MCPClient to communicate with the server.

# The URL for the MCP server developed by Person 3
MCP_SERVER_URL = "http://mcp-server.local:8080"
mcp_client = MCPClient(server_url=MCP_SERVER_URL)

# For CrewAI, it's best practice to define tools as classes inheriting from BaseTool.
class WebSearchMCPTool(BaseTool):
    name: str = "WebSearchTool"
    description: str = "A tool to search the internet for up-to-date information on topics like market trends and required job skills."

    def _run(self, query: str) -> str:
        """
        Invokes the WebSearchTool on the remote MCP server.
        The agent's LLM uses the `description` to decide when to call this tool [8].
        """
        return mcp_client.invoke_tool(self.name, query=query)

# Instantiate the tool for the agents
web_search_mcp_tool = WebSearchMCPTool()

# This function accesses a resource. It's "application-controlled," meaning our
# task logic will call it directly when the CV is needed [7].
def get_user_cv_from_server() -> str:
    """
    Retrieves the user's CV content from the central MCP resource server.
    """
    return mcp_client.get_resource("user_cv.txt")