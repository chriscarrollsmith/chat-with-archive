import logging
import json
import ast
import os
import dotenv
import time
from datetime import UTC, datetime
from openai import OpenAI, AsyncOpenAI, AsyncAssistantEventHandler
from openai.types.beta.threads.runs import RunStep
import chainlit as cl
from chainlit.config import config
from chainlit.element import Element
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
    assistant_id
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
        self.current_step.start = datetime.now(UTC).isoformat()
        await self.current_step.send()

    async def on_tool_call_delta(self, delta, snapshot): 
        if snapshot.id != self.current_tool_call:
            self.current_tool_call = snapshot.id
            self.current_step = cl.Step(name=delta.type, type="tool",  parent_id=cl.context.current_run.id)
            self.current_step.start = datetime.now(UTC).isoformat()
            if snapshot.type == "code_interpreter":
                 self.current_step.show_input = "python"
            if snapshot.type == "function":
                self.current_step.name = snapshot.function.name
                self.current_step.language = "json"
            await self.current_step.send()
        
        if delta.type == "function":
            if delta.function.output:
                # Update the current step with the function output
                self.current_step.output = json.dumps(delta.function.output, indent=2)
                self.current_step.language = "json"
                self.current_step.end = datetime.now(UTC).isoformat()
                await self.current_step.update()
        
        if delta.type == "code_interpreter":
            if delta.code_interpreter.outputs:
                for output in delta.code_interpreter.outputs:
                    if output.type == "logs":
                        self.current_step.output += output.logs
                        self.current_step.language = "markdown"
                        self.current_step.end = datetime.now(UTC).isoformat()
                        await self.current_step.update()
                    elif output.type == "image":
                        self.current_step.language = "json"
                        self.current_step.output = output.image.model_dump_json()
            else:
                if delta.code_interpreter.input:
                    await self.current_step.stream_token(delta.code_interpreter.input, is_input=True)  

    async def on_event(self, event) -> None:
        if event.event == "error":
            return await cl.ErrorMessage(content=str(event.data.message)).send()

    async def on_exception(self, exception: Exception) -> None:
        return await cl.ErrorMessage(content=str(exception)).send()

    async def on_tool_call_done(self, tool_call):       
        self.current_step.end = datetime.now(UTC).isoformat()
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

# Set starter suggestions
@cl.set_starters
async def set_starters():
    return [
        cl.Starter(
            label="Tweets that mention tpot",
            message="What are the most recent 5 tweets that mention tpot?"
        ),
        cl.Starter(
            label="What is a postrat?",
            message="Search the archive for the term 'postrat' and see if you can figure out what that means."
        )
    ]

# On chat start, set up the message history
@cl.on_chat_start
async def start_chat():
    # Create a new OAI thread for the conversation
    thread = await async_openai_client.beta.threads.create()
    # Store the thread id in the user session
    cl.user_session.set("thread_id", thread.id)

# If the user clicks stop on the current step, cancel the run
@cl.on_stop
async def stop_chat():
    current_run_step: RunStep = cl.user_session.get("run_step")
    if current_run_step:
        await async_openai_client.beta.threads.runs.cancel(thread_id=current_run_step.thread_id, run_id=current_run_step.run_id)

# When the user sends a message, add it to the OAI thread and run the assistant
@cl.on_message
async def main(message: cl.Message):
    # Get the OAI thread id from the user session
    thread_id = cl.user_session.get("thread_id")

    # Process any attachments
    attachments = await process_files(message.elements)

    # Add a Message to the Thread
    oai_message = await async_openai_client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=message.content,
        attachments=attachments,
    )

    # Create and Stream a Run
    async with async_openai_client.beta.threads.runs.stream(
        thread_id=thread_id,
        assistant_id=assistant.id,
        event_handler=EventHandler(assistant_name=assistant.name),
    ) as stream:
        await stream.until_done()


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


async def upload_files(files: list[Element]):
    file_ids = []
    for file in files:
        uploaded_file = await async_openai_client.files.create(
            file=Path(file.path), purpose="assistants"
        )
        file_ids.append(uploaded_file.id)
    return file_ids


async def process_files(files: list[Element]):
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