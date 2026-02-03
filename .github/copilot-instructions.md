# GitHub Copilot Custom Instructions

## 1. Project Overview & Tech Stack
- **Core Language:** Python 3.11+
- **Orchestration:** LangChain (LCEL - LangChain Expression Language)
- **Model Provider:** OpenAI (via `langchain-openai`)
- **Primary Docs:** [LangChain OpenAI Integrations]()https://docs.langchain.com/oss/python/integrations/chat/openai

## 2. Coding Standards
- **Style:** Strictly follow PEP 8. Use 4 spaces for indentation.
- **Typing:** Use Python type hints for all function arguments and return types (e.g., `def run_chain(input: str) -> dict:`).
- **Naming:** `snake_case` for variables/functions and `PascalCase` for classes.
- **Async:** Prefer asynchronous implementations (`async/await`) for LLM calls using `ainvoke`, `astream`, or `abatch`.

## 3. LangChain & OpenAI Best Practices
- **Initialization:** Use the latest integration patterns from `langchain-openai`. Prefer `ChatOpenAI` for chat models.
- **LCEL Syntax:** Always use the Pipe operator (`|`) for composing chains instead of legacy `Chain` classes (like `LLMChain`).
- **Configuration:**
  - Assume `OPENAI_API_KEY` is provided via environment variables. 
  - Do not hardcode API keys. 
  - Use `.env` files for local development.
- **Prompts:** Use `ChatPromptTemplate` and `MessagesPlaceholder` for managing chat history rather than manual string concatenation.

## 4. Error Handling & Performance
- **Resilience:** Implement `with_fallbacks()` or `Retrying` logic for API timeouts and rate limits.
- **Streaming:** Enable streaming by default for user-facing chat interfaces to improve perceived latency.
- **Logging:** Use the standard `logging` library to track chain execution and token usage via `get_openai_callback`.

## 5. Documentation & Testing
- **Docstrings:** Use Google-style docstrings (PEP 257) for all public-facing methods.
- **Testing:** Use `pytest` for unit tests. Mock LLM responses using `unittest.mock` or LangChain's built-in mocking utilities to avoid unnecessary API costs during CI/CD.