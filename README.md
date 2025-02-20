# Chat with the X / Twitter Community Archive

This is a local web application for using the OpenAI Assistants API to chat with the X / Twitter Community Archive.

You will need an [OpenAI API key](https://platform.openai.com/account/api-keys) and a [Twitter Community Archive API key](https://archive.org/services/api/archive.php).

## Quickstart Setup

### 1. Clone repo

```shell
git clone https://github.com/chriscarrollsmith/chat-with-archive.git
cd chat-with-archive
```

### 2. Install dependencies

```shell
uv sync
```

### 3. Run the FastAPI server

```shell
uv run uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 4. Navigate to [http://localhost:8000](http://localhost:8000).

### 5. Set your OpenAI API key and create an assistant in the GUI

If your OPENAI_API_KEY or ASSISTANT_ID are not set, you will be redirected to the setup page where you can set them. (The values will be saved in a .env file in the root of the project.) Once set, you will be redirected to the home page and can begin a chat session.

