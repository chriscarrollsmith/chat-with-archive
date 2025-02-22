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

## Troubleshooting

Complex queries against the public archive database may fail due to the 3 second timeout imposed by Supabase on the anon role.

If you encounter query failures due to timeout, you can mirror the database on your own Supabase instance and change the timeout by running `psql -h 127.0.0.1 -p 54322 -U postgres -d postgres -c "ALTER ROLE anon SET statement_timeout = '15s';"`. (Note that you will need `psql` installed to run this query. This query will not work if run inside the Supabase Studio.)

You will then edit the `.env` file to use your new Supabase URL (probably `http://localhost:54321`) and anon key (probably `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6ImFub24iLCJleHAiOjE5ODM4MTI5OTZ9.CRXP1A7WOeoJeXxjNni43kdQwgnWNReilDMblYTn_I0`). This will point the agent to your local database instance so it can run longer queries.