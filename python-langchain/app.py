from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.tools import Tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
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

def reverse_string(text: str) -> str:
    """
    Reverses a string.

    Args:
        text (str): The string to reverse.

    Returns:
        str: The reversed string.
    """
    return text[::-1]

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
        ),
        Tool(
            name="reverse_string",
            func=reverse_string,
            description="Reverses a string. Input should be a single string."
        )
    ]

    # Create a prompt template with system message for the agent
    system_message = "You are a professional and succinct AI assistant. Provide clear, concise responses and use available tools when necessary to answer user queries accurately."
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_message),
        MessagesPlaceholder(variable_name="messages")
    ])
    
    # Create agent with prompt and tools
    agent_executor = prompt | chat.bind_tools(tools)

    # Test queries list
    test_queries = [
        "What time is it right now?",
        "What is 25 * 4 + 10?",
        "Reverse the string 'Hello World'"
    ]

    # Run example queries
    print("\nRunning example queries:")
    print("─" * 50)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n📝 Query {i}: {query}")
        print("─" * 50)
        
        try:
            # Invoke the agent with the query
            result = agent_executor.invoke({"messages": [{"role": "user", "content": query}]})

            # Check if the result contains tool calls and handle them
            if result.tool_calls:
                for tool_call in result.tool_calls:
                    tool_name = tool_call['name']
                    tool_args = tool_call.get('args', {})
                    
                    if tool_name == 'Calculator':
                        expression = tool_args.get('__arg1', '')
                        tool_output = calculator(expression)
                        print("✅ Agent Output (Calculator):", tool_output)
                    elif tool_name == 'get_current_time':
                        tool_output = get_current_time("")
                        print("✅ Agent Output (Time):", tool_output)
                    elif tool_name == 'reverse_string':
                        text = tool_args.get('__arg1', '')
                        tool_output = reverse_string(text)
                        print("✅ Agent Output (Reverse):", tool_output)
                    else:
                        print("✅ Unhandled Tool Call:", tool_call)
            else:
                # Default response handling
                if hasattr(result, "content"):
                    print("✅ Agent Output:", result.content)
                else:
                    print("✅ Agent Output:", result)
        except Exception as e:
            print(f"❌ Error while executing the agent: {e}")
    
    print("\n" + "─" * 50)
    print("🎉 Agent demo complete!")

    # Test query
    # query = "What is 25 * 4 + 10?"
    # response = chat.invoke(query)

    # Print the response content
    # print("AI Response:", response.content)

    # Debugging: Print the output of the get_current_time tool
    # print("DEBUG: get_current_time output:", get_current_time(""))

if __name__ == "__main__":
    # Load environment variables from a .env file
    load_dotenv()
    main()