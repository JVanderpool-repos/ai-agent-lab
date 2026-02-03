from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

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

    # Test query
    query = "What is 25 * 4 + 10?"
    response = chat.invoke(query)

    # Print the response content
    print("AI Response:", response.content)

if __name__ == "__main__":
    # Load environment variables from a .env file
    load_dotenv()
    main()