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

def main():
    # Load the GITHUB_TOKEN from environment variables
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        print("❌ Error: GITHUB_TOKEN not found in environment variables.")
        print("💡 Please create a .env file with the following content:")
        print("   GITHUB_TOKEN=your_personal_access_token")
        print("🔗 For more information, visit: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token")
        return

    print("✅ GITHUB_TOKEN loaded successfully!")

    # Create a ChatOpenAI instance
    chat = ChatOpenAI(
        model="openai/gpt-4o",
        temperature=0,
        base_url="https://models.github.ai/inference",
        api_key=lambda: github_token  # Wrap the token in a callable
    )

    print("🤖 ChatOpenAI instance created successfully!")

    # Create a tools list
    tools = [
        Tool(
            name="Calculator",
            func=calculator,
            description="Use this tool to evaluate mathematical expressions provided as strings. It supports basic arithmetic operations like addition, subtraction, multiplication, and division. Ensure the input is a valid mathematical expression."
        )
    ]

    # Create an agent
    try:
        agent_executor = create_agent(
            model=chat,  # Corrected parameter name
            tools=tools,
            debug=True
        )

        # Test query with messages
        test_query = [
            {"role": "user", "content": "What is 25 * 4 + 10?"}
        ]
        result = chat.invoke(test_query)  # Use the ChatOpenAI instance directly

        # Print the result
        print("Agent Output:", result.text)
    except Exception as e:
        print("❌ Error while executing the agent:", e)

    # Test query
    query = "What is 25 * 4 + 10?"
    response = chat.invoke(query)

    # Print the response content
    print("AI Response:", response.content)

if __name__ == "__main__":
    # Load environment variables from a .env file
    load_dotenv()
    main()