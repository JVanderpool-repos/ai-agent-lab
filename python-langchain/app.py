from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.tools import Tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, BaseMessage
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

def weather_tool(date: str) -> str:
    """
    Returns weather information for a given date.

    Args:
        date (str): The date in the format 'YYYY-MM-DD'.

    Returns:
        str: Weather information as a string. Returns "Sunny, 72°F" for today's date,
             and "Rainy, 55°F" for all other dates.

    Raises:
        ValueError: If the date format is invalid.
    """
    try:
        # Validate date format
        provided_date = datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m-%d")
        today_date = datetime.now().strftime("%Y-%m-%d")

        # Check if the provided date matches today's date
        if provided_date == today_date:
            return "Sunny, 72°F"
        else:
            return "Rainy, 55°F"
    except ValueError as e:
        return f"Error: Invalid date format. Expected 'YYYY-MM-DD', got '{date}'. Details: {e}"
    except Exception as e:
        return f"Error: An unexpected error occurred while processing the date. Details: {e}"

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
        model="gpt-4o",
        temperature=0,
        api_key=lambda: os.getenv("GITHUB_TOKEN") or "",  # Provide a default empty string if the environment variable is not set
        base_url="https://models.github.ai/inference"
    )

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
        ),
        Tool(
            name="get_weather",
            func=weather_tool,
            description="Retrieves weather information for a specified date. This tool accepts a date parameter formatted as 'YYYY-MM-DD' (e.g., '2026-02-04'). It returns 'Sunny, 72°F' if the date matches today's date, and 'Rainy, 55°F' for all other dates. Use this tool to get weather predictions or historical weather data for any date."
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
        "Reverse the string 'Hello World'",
        f"What is the weather for today? ({datetime.now().strftime('%Y-%m-%d')})",
        "What's the weather like today?"
    ]

    # Run example queries
    print("\nRunning example queries:")
    print("─" * 50)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n📝 Query {i}: {query}")
        print("─" * 50)
        
        try:
            # Initialize messages with the user query
            messages: list[BaseMessage] = [HumanMessage(content=query)]
            
            # Agentic loop: continue until we get a final response (no more tool calls)
            max_iterations = 10
            iteration = 0
            
            while iteration < max_iterations:
                iteration += 1
                
                # Invoke the agent
                result = agent_executor.invoke({"messages": messages})
                
                # Check if the result contains tool calls
                if result.tool_calls:
                    # Add the assistant message to the conversation
                    messages.append(result)
                    
                    # Process each tool call
                    for tool_call in result.tool_calls:
                        tool_name = tool_call['name']
                        tool_args = tool_call.get('args', {})
                        tool_call_id = tool_call.get('id', '')
                        tool_output = ""
                        
                        if tool_name == 'Calculator':
                            expression = tool_args.get('__arg1', '')
                            tool_output = calculator(expression)
                            print(f"  🔧 Tool: {tool_name} → {tool_output}")
                        elif tool_name == 'get_current_time':
                            tool_output = get_current_time("")
                            print(f"  🔧 Tool: {tool_name} → {tool_output}")
                        elif tool_name == 'reverse_string':
                            text = tool_args.get('__arg1', '')
                            tool_output = reverse_string(text)
                            print(f"  🔧 Tool: {tool_name} → {tool_output}")
                        elif tool_name == 'get_weather':
                            date = tool_args.get('__arg1', '')
                            tool_output = weather_tool(date)
                            print(f"  🔧 Tool: {tool_name} → {tool_output}")
                        else:
                            tool_output = f"Unhandled tool: {tool_name}"
                            print(f"  ⚠️ {tool_output}")
                        
                        # Add the tool result to messages as a ToolMessage with tool_call_id
                        messages.append(ToolMessage(content=tool_output, tool_call_id=tool_call_id))
                else:
                    # No tool calls - this is the final response
                    if hasattr(result, "content"):
                        print("✅ Final Answer:", result.content)
                    else:
                        print("✅ Final Answer:", result)
                    break
            
            if iteration >= max_iterations:
                print("⚠️ Max iterations reached. Agent may not have completed.")
                
        except Exception as e:
            print(f"❌ Error while executing the agent: {e}")
    
    print("\n" + "─" * 50)
    print("🎉 Agent demo complete!")

if __name__ == "__main__":
    # Load environment variables from a .env file
    load_dotenv()
    main()