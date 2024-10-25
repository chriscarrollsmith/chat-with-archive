# Chat with the Twitter Community Archive via a tool-calling OpenAI Assistant

1. Prerequisites:

- Install [Python 3.12](https://www.python.org/downloads/) or later.
- Install the [`uv` package manager](https://github.com/astral-sh/uv).

Note: you can use Python to install `uv`... or the other way around! See the `uv` documentation linked above for details.

2. Clone the repository and navigate to the `chat-with-archive` directory:

```
git clone https://github.com/chriscarrollsmith/chat-with-archive.git
cd chat-with-archive
```

3. Install the dependencies:

```
uv venv
uv pip install -r pyproject.toml
```

4. Copy `.env.example` to `.env` and set the required environment variables:

```
cp .env.example .env
```

You will need an [OpenAI API key](https://platform.openai.com/account/api-keys) and a [Twitter Community Archive API key](https://archive.org/services/api/archive.php).

5. Create the assistant:

```
uv run create_assistant.py
```

Unless you want to modify the tools or system prompt, you'll only need to do this once. The assistant ID will be automatically written to the `.env` file when the assistant is created. If you do run this script again, it will update the existing assistant (using the ID from the `.env` file) rather than creating a new one.

6. Run the Chainlit application:

```
uv run chainlit run app.py
```

7. Interact with the app through the Chainlit interface at http://localhost:8000.
