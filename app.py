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
parameters needed to answer their questions, but don't refuse a query
just because it's a bit vague. For instance, if the user asks about
their own activity but neglects to provide any identifying
information, you should ask for their username. Fulfill the user's
request if at all possible even if it's vague, but invite them to be
more specific in their next message when you present the results.

Since the Twitter Community Archive API is a PostgREST API, you must
use PostgREST operators for filtering. If possible, you should
retrieve any information requested by the user using a single API call.
You may use nested resource embedding or include logical operator keys
in your request parameters to construct complex user queries. Always
use the `limit` parameter to paginate results! Requesting more than 50
results at a time is abusive of the Twitter Community Archive API.
Please do not abuse our tools!

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
    settings = {
        "model": "gpt-4o-mini",
        "tools": request_schemas,
        "tool_choice": "auto",
    }

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


@cl.on_message
async def run_conversation(message: cl.Message):
    message_history = cl.user_session.get("message_history")

    # Add the user's message to the message history
    message_history.append({"role": "user", "content": message.content})

    cur_iter = 0

    while cur_iter < MAX_ITER:
        message = await call_llm(message_history)
        if not message.tool_calls:
            await cl.Message(content=message.content, author="Answer").send()
            break

        cur_iter += 1
