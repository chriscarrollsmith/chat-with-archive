**Under Construction**

1. Prerequisites:

- Install [Python 3.12](https://www.python.org/downloads/) or later.
- Install the `uv` package manager: `pip install uv`.

2. Clone the repository and navigate to the `chat-with-archive` directory:

```
git clone https://github.com/chriscarrollsmith/chat-with-archive.git
cd chat-with-archive
```

3. Install the dependencies:

```
uv venv
uv pip install
```

4. Copy `.env.example` to `.env` and set the required environment variables:

```
cp .env.example .env
```

You will need an [OpenAI API key](https://platform.openai.com/account/api-keys) and a [Twitter Community Archive API key](https://archive.org/services/api/archive.php).

5. Run the app:

```
uv run chainlit run app.py
```

6. Interact with the app through the Chainlit interface at http://localhost:8000.
