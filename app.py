import logging
import json
import ast
import os
import dotenv
import time
from openai import types
from openai import AsyncOpenAI, AsyncAssistantEventHandler
import chainlit as cl
from tools import tools, split_tool_schemas
from tool_caller import make_request
import asyncio


# Define settings
SETTINGS = {
    "model": "gpt-4o-mini"
}
MAX_ITER = 5

# Get Chainlit logger
logger = cl.logger

# Load environment variables
dotenv.load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")
assistant_id = os.environ.get("ASSISTANT_ID")

# Initialize OpenAI clients
async_openai_client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
sync_openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Get the assistant
assistant = sync_openai_client.beta.assistants.retrieve(
    os.environ.get("OPENAI_ASSISTANT_ID")
)

# Set the UI name
config.ui.name = assistant.name

# Event handler class for managing OpenAI assistant events
class EventHandler(AsyncAssistantEventHandler):
    def __init__(self, assistant_name: str) -> None:
        super().__init__()
        self.current_message: cl.Message = None
        self.current_step: cl.Step = None
        self.current_tool_call = None
        self.assistant_name = assistant_name

    async def on_run_step_created(self, run_step: RunStep) -> None:
        cl.user_session.set("run_step", run_step)

    async def on_text_created(self, text) -> None:
        self.current_message = await cl.Message(author=self.assistant_name, content="").send()

    async def on_text_delta(self, delta, snapshot):
        if delta.value:
            await self.current_message.stream_token(delta.value)

    async def on_text_done(self, text):
        await self.current_message.update()
        if text.annotations:
            print(text.annotations)
            for annotation in text.annotations:
                if annotation.type == "file_path":
                    response = await async_openai_client.files.with_raw_response.content(annotation.file_path.file_id)
                    file_name = annotation.text.split("/")[-1]
                    element = cl.File(content=response.content, name=file_name)
                    await cl.Message(
                        content="",
                        elements=[element]).send()
                    # Hack to fix links
                    if annotation.text in self.current_message.content and element.chainlit_key:
                        self.current_message.content = self.current_message.content.replace(annotation.text, f"/project/file/{element.chainlit_key}?session_id={cl.context.session.id}")
                        await self.current_message.update()

    async def on_tool_call_created(self, tool_call):
        self.current_tool_call = tool_call.id
        self.current_step = cl.Step(name=tool_call.type, type="tool", parent_id=cl.context.current_run.id)
        self.current_step.show_input = "python"
        self.current_step.start = utc_now()
        await self.current_step.send()

    async def on_tool_call_delta(self, delta, snapshot): 
        if snapshot.id != self.current_tool_call:
            self.current_tool_call = snapshot.id
            self.current_step = cl.Step(name=delta.type, type="tool",  parent_id=cl.context.current_run.id)
            self.current_step.start = utc_now()
            if snapshot.type == "code_interpreter":
                 self.current_step.show_input = "python"
            if snapshot.type == "function":
                self.current_step.name = snapshot.function.name
                self.current_step.language = "json"
            await self.current_step.send()
        
        if delta.type == "function":
            pass
        
        if delta.type == "code_interpreter":
            if delta.code_interpreter.outputs:
                for output in delta.code_interpreter.outputs:
                    if output.type == "logs":
                        self.current_step.output += output.logs
                        self.current_step.language = "markdown"
                        self.current_step.end = utc_now()
                        await self.current_step.update()
                    elif output.type == "image":
                        self.current_step.language = "json"
                        self.current_step.output = output.image.model_dump_json()
            else:
                if delta.code_interpreter.input:
                    await self.current_step.stream_token(delta.code_interpreter.input, is_input=True)  

    async def on_event(self, event) -> None:
        if event.event == "error":
            return cl.ErrorMessage(content=str(event.data.message)).send()

    async def on_exception(self, exception: Exception) -> None:
        return cl.ErrorMessage(content=str(exception)).send()

    async def on_tool_call_done(self, tool_call):       
        self.current_step.end = utc_now()
        await self.current_step.update()

    async def on_image_file_done(self, image_file):
        image_id = image_file.file_id
        response = await async_openai_client.files.with_raw_response.content(image_id)
        image_element = cl.Image(
            name=image_id,
            content=response.content,
            display="inline",
            size="large"
        )
        if not self.current_message.elements:
            self.current_message.elements = []
        self.current_message.elements.append(image_element)
        await self.current_message.update()

# On chat start, set up the message history
@cl.on_chat_start
async def start_chat():
    # Create a new thread for the conversation
    thread = await client.beta.threads.create()
    cl.user_session.set("thread_id", thread.id)
    cl.user_session.set("message_history", [])

# If the user clicks stop on the current step, cancel the run
@cl.on_stop
async def stop_chat():
    current_run_step: RunStep = cl.user_session.get("run_step")
    if current_run_step:
        await client.beta.threads.runs.cancel(thread_id=current_run_step.thread_id, run_id=current_run_step.run_id)

@cl.on_message
async def run_conversation(message: cl.Message):
    thread_id = cl.user_session.get("thread_id")
    message_history = cl.user_session.get("message_history")

    # Add the user's message to the message history
    message_history.append({"role": "user", "content": message.content})

    # Create a message in the thread
    await client.beta.threads.messages.create(
        thread_id=thread_id, role="user", content=message.content
    )

    cur_iter = 0

    while cur_iter < MAX_ITER:
        try:
            # Check if there's an active run before creating a new one
            active_runs = await client.beta.threads.runs.list(thread_id=thread_id)
            if any(run.status in ["queued", "in_progress"] for run in active_runs.data):
                logger.info("Waiting for active run to complete.")
                await asyncio.sleep(1)
                continue

            # Create a run for the assistant to process the thread
            run = await client.beta.threads.runs.create(
                thread_id=thread_id,
                assistant_id=assistant_id,
            )

            # Wait for the run to complete
            run = await wait_on_run(run, thread_id)

            # Retrieve messages from the thread
            messages = await client.beta.threads.messages.list(thread_id=thread_id, order="asc")
            for msg in messages.data:
                if msg.role == "assistant":
                    # Check if the message has already been sent
                    if not any(m['content'] == msg.content[0].text.value for m in message_history):
                        await cl.Message(content=msg.content[0].text.value, author="Answer").send()
                        message_history.append({"role": "assistant", "content": msg.content[0].text.value})
                        return  # Exit the loop after sending a valid response

        except openai.BadRequestError as e:
            # Handle the case where there is already an active run
            if "already has an active run" in str(e):
                logger.info("Active run detected, waiting for it to complete.")
                await asyncio.sleep(1)  # Wait before retrying
            else:
                raise  # Re-raise the exception if it's not the expected error

        cur_iter += 1
        await asyncio.sleep(1)  # Add a delay to reduce request frequency


async def wait_on_run(run, thread_id):
    while run.status in ["queued", "in_progress"]:
        # Retrieve the latest status of the run
        run = await client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id,
        )
        logger.info(f"Run status: {run.status}")  # Log the status for debugging
        await asyncio.sleep(0.5)  # Use asyncio.sleep for non-blocking delay
    return run



# TODO: Finish implementing this template: https://github.com/Chainlit/cookbook/blob/main/openai-data-analyst/app.py
# TODO: Finish reading the docs: https://docs.chainlit.io/concepts/chat-lifecycle
@cl.step(type="tool")
async def call_tool(tool_call, endpoint: dict, message_history: list) -> None:
    function_name: str = tool_call.function.name
    arguments: str = tool_call.function.arguments
    logger.info(f"Calling tool {function_name} with arguments {arguments}")

    current_step = cl.context.current_step
    current_step.name = function_name
    current_step.input = arguments

    function_response = make_request(
        endpoint, arguments
    )

    serialized_response = json.dumps(function_response)
    if len(serialized_response) > 4000:
        prefix = "Looks like the response was very long. Are you being a naughty chatbot and making requests without the `limit` parameter? Here's the first 4000 characters of the response:\n\n"
        serialized_response = serialized_response[:4000] + "..."

    current_step.output = serialized_response
    current_step.language = "json"

    return {
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": serialized_response,
    }


async def call_llm(message_history) -> cl.Message:
    response = await client.chat.completions.create(
        messages=message_history, **settings
    )

    message: cl.Message = response.choices[0].message
    message_history.append(message)

    tool_calls = message.tool_calls or []
    for tool_call in tool_calls:
        endpoint_name: str = tool_call.function.name
        endpoint: dict | None = next((item for item in endpoint_schemas if item["name"] == endpoint_name), None)

        if not endpoint:
            logger.warning(f"Endpoint {endpoint_name} not found")
        else:
            tool_message = await call_tool(tool_call, endpoint, message_history)
            message_history.append(tool_message)

    if message.content:
        cl.context.current_step.output = message.content

    return message


async def upload_files(files: List[Element]):
    file_ids = []
    for file in files:
        uploaded_file = await async_openai_client.files.create(
            file=Path(file.path), purpose="assistants"
        )
        file_ids.append(uploaded_file.id)
    return file_ids


async def process_files(files: List[Element]):
    # Upload files if any and get file_ids
    file_ids = []
    if len(files) > 0:
        file_ids = await upload_files(files)

    return [
        {
            "file_id": file_id,
            "tools": [{"type": "code_interpreter"}, {"type": "file_search"}] if file.mime in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document", "text/markdown", "application/pdf", "text/plain"] else [{"type": "code_interpreter"}],
        }
        for file_id, file in zip(file_ids, files)
    ]