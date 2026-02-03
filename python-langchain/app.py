from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.tools import Tool
from datetime import datetime
import os

def calculator(expression: str) -> str:
    """
    Evaluates a mathematical expression provided as a string.

    Args:
        expression (str): The mathematical expression to evaluate.

    Returns:
        str: The result of the evaluation as a string.

    Note:
        This function uses eval() for demonstration purposes. Avoid using eval() with untrusted input.
    """
    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error: {e}"

def get_current_time(_: str) -> str:
    """
    Returns the current date and time as a formatted string.

    Args:
        _: A string input parameter (required by the Tool interface, not used).

    Returns:
        str: The current date and time in the format 'YYYY-MM-DD HH:MM:SS'.
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def main():
    # Load the GITHUB_TOKEN from environment variables
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        print("❌ Error: GITHUB_TOKEN not found in environment variables.")
        print("💡 Please create a .env file with the following content:")
        print("   GITHUB_TOKEN=your_personal_access_token")
        print("🔗 For more information, visit: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token")
        return

    # Debugging: Check if environment variables are loaded
    print("DEBUG: GITHUB_TOKEN:", os.getenv("GITHUB_TOKEN"))

    print("✅ GITHUB_TOKEN loaded successfully!")

    # Create a ChatOpenAI instance
    chat = ChatOpenAI(
        model="gpt-4o",
        temperature=0,
        api_key=lambda: os.getenv("GITHUB_TOKEN") or "",  # Provide a default empty string if the environment variable is not set
        base_url="https://models.github.ai/inference"
    )

    ###print("🤖 ChatOpenAI instance created successfully!")

    # Create a tools list
    tools = [
        Tool(
            name="Calculator",
            func=calculator,
            description="Use this tool to evaluate mathematical expressions provided as strings. It supports basic arithmetic operations like addition, subtraction, multiplication, and division. Ensure the input is a valid mathematical expression."
        ),
        Tool(
            name="get_current_time",
            func=get_current_time,
            description="Use this tool to get the current date and time in the format 'YYYY-MM-DD HH:MM:SS'."
        )
    ]

    # Updated agent creation to use bind_tools for better integration
    agent_executor = chat.bind_tools(tools)

    # Updated test query to use the documented invocation structure
    test_query = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What time is it right now?"}
    ]

    # Refactor to ensure tool outputs are included in the agent's response
    try:
        result = agent_executor.invoke(test_query)

        # Check if the result contains tool calls and handle them
        if result.tool_calls:
            for tool_call in result.tool_calls:
                if tool_call['name'] == 'get_current_time':
                    tool_output = get_current_time("")
                    print("Agent Output (with tool):", tool_output)
                else:
                    print("Unhandled Tool Call:", tool_call)
        else:
            # Default response handling
            if hasattr(result, "content"):
                print("Agent Output:", result.content)
            else:
                print("Agent Output:", "Unexpected response format:", result)
    except Exception as e:
        print("❌ Error while executing the agent:", e)

    # Test query
    # query = "What is 25 * 4 + 10?"
    # response = chat.invoke(query)

    # Print the response content
    # print("AI Response:", response.content)

    # Debugging: Print the output of the get_current_time tool
    print("DEBUG: get_current_time output:", get_current_time(""))

if __name__ == "__main__":
    # Load environment variables from a .env file
    load_dotenv()
    main()