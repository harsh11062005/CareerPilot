from crewai import Task
from textwrap import dedent
# Import the resource access function
from mcp_client import get_user_cv_from_server

class CareerTasks():
    def discover_careers_task(self, agent, user_interests):
        # The task logic now controls when to get the resource [7].
        # It fetches the CV from the MCP server before defining the task description.
        user_cv_content = get_user_cv_from_server()

        return Task(
            description=dedent(f"""
                Analyze the user's CV and their stated interests to identify potential career paths.
                Your final report should be a comprehensive analysis of 5 promising career roles.

                Use your WebSearchTool to find current market demand and salary expectations for the roles you identify.

                User Interests: {user_interests}
                User CV Content:
                ---
                {user_cv_content}
                ---
            """),
            expected_output="A detailed, well-structured report in markdown format containing the analysis of 5 career paths.",
            agent=agent
        )

    def tailor_resume_task(self, agent):
        # This task also needs the CV, so it fetches it from the server.
        user_cv_content = get_user_cv_from_server()

        return Task(
            description=dedent(f"""
                Using the career path report from the previous task, select the top recommended
                career path and tailor the user's CV for that role.

                User CV Content to be tailored:
                ---
                {user_cv_content}
                ---
            """),
            expected_output="A professionally tailored resume in markdown format, customized for the top career path.",
            agent=agent
        )