import logging
import json
import ast
import os
import dotenv
from openai import types
from openai import AsyncOpenAI
import chainlit as cl
from tools import tools, split_tool_schemas
from tool_caller import make_request


# Get Chainlit logger
logger = cl.logger

# Load environment variables
dotenv.load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")

# Initialize OpenAI client and instrument it
client = AsyncOpenAI(api_key=api_key)
cl.instrument_openai()

# Define maximum
MAX_ITER = 5

# Split tool schemas into endpoint schemas and request schemas
endpoint_schemas, request_schemas = split_tool_schemas(tools)

# Set system prompt
system_prompt = """
Users will ask you questions about activity on Twitter, as represented
in data voluntarily uploaded to the Twitter Community Archive. You
have no access to Twitter itself and cannot answer questions about
Twitter activity outside of what is in the archive. Always format your
responses in markdown. Be proactive about soliciting from the user any
necessary parameters that might be necessary to answer their
questions. For instance, if the user asks about their own activity but
negelects to provide any identifying information, you should ask for
their username.

Since the Twitter Community Archive API is a PostgREST API, you must
use PostgREST operators for filtering. If possible, you should
retrieve any information requested by the user using a single API call.
You may use nested resource embedding or include logical operator keys
in your request parameters to construct complex user queries.

When constructing nested queries, you should pay close attention to
foreign key relationships and endpoint names specified in the schema.
For example, if the user wants bios for their followers, you cannot use
`follower_account_id` from `get_followers`, because that variable has
no foreign key relationships. Instead, you should use `account_id` from
`get_following_accounts`, because that variable has a foreign key
relationship to `account.account_id`, which in turn has a relationship
to `user_profiles.account_id`. The nested "select" parameter would look
like this: `account(account_id,profile(bio))`.
"""


# On chat start, set up the message history
@cl.on_chat_start
def start_chat():
    cl.user_session.set(
        "message_history",
        [{"role": "system", "content": system_prompt}],
    )


@cl.step(type="tool")
async def call_tool(tool_call, endpoint, message_history):
    function_name = tool_call.function.name
    arguments = tool_call.function.arguments
    logger.info(f"Calling tool {function_name} with arguments {arguments}")

    current_step = cl.context.current_step
    current_step.name = function_name
    current_step.input = arguments

    function_response = make_request(
        arguments, endpoint
    )

    current_step.output = function_response
    current_step.language = "json"

    message_history.append(
        {
            "role": "function",
            "name": function_name,
            "content": function_response,
            "tool_call_id": tool_call.id,
        }
    )


async def call_llm(message_history) -> cl.Message:
    settings = {
        "model": "gpt-4o-mini",
        "tools": tools,
        "tool_choice": "auto",
    }

    response = await client.chat.completions.create(
        messages=message_history, **settings
    )

    message: cl.Message = response.choices[0].message
    logger.info(f"Finish reason: {response.finish_reason}")

    if response.finish_reason == "tool_calls":
        logger.info(f"Tool calls: {message.tool_calls}")
        for tool_call in message.tool_calls or []:
            endpoint_name = tool_call.function.name
            endpoint = next((item for item in endpoint_schemas if item["name"] == endpoint_name), None)
            if not endpoint:
                logger.warning(f"Endpoint {endpoint_name} not found")
            else:
                await call_tool(tool_call, endpoint, message_history)

    if message.content:
        cl.context.current_step.output = message.content

    elif message.tool_calls:
        completion = message.tool_calls

        cl.context.current_step.language = "json"
        cl.context.current_step.output = completion

    return message


@cl.on_message
async def run_conversation(message: cl.Message):
    message_history = cl.user_session.get("message_history")
    message_history.append({"name": "user", "role": "user", "content": message.content})

    cur_iter = 0

    while cur_iter < MAX_ITER:
        message = await call_llm(message_history)
        if not message.tool_calls:
            await cl.Message(content=message.content, author="Answer").send()
            break

        cur_iter += 1