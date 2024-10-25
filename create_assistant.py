import logging
import os
import dotenv
from openai import AsyncOpenAI
from tools import tools, split_tool_schemas
import asyncio

# Set system prompt
SYSTEM_PROMPT = """
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

def update_env_file(assistant_id, logger):
    """
    Update the .env file with a new assistant ID.

    If the .env file already contains an ASSISTANT_ID, it will be removed.
    The new assistant ID will be appended to the .env file. If the .env file
    does not exist, it will be created.
    """
    if os.path.exists('.env'):
        with open('.env', 'r') as env_file:
            lines = env_file.readlines()

        # Remove any existing ASSISTANT_ID line
        lines = [line for line in lines if not line.startswith("ASSISTANT_ID=")]

        # Write back the modified lines
        with open('.env', 'w') as env_file:
            env_file.writelines(lines)

    # Write the new assistant ID to the .env file
    with open('.env', 'a') as env_file:
        env_file.write(f"ASSISTANT_ID={assistant_id}\n")
    logger.info(f"Assistant ID written to .env: {assistant_id}")

async def create_or_update_assistant(client, assistant_id, request_schemas, logger):
    """
    Create or update the assistant based on the presence of an assistant_id.
    """
    try:
        if assistant_id:
            # Update the existing assistant
            assistant = await client.beta.assistants.update(
                assistant_id,
                name="Twitter Community Archive Assistant",
                instructions=SYSTEM_PROMPT,
                tools=request_schemas,
                model="gpt-4o-mini",
            )
            logger.info(f"Updated assistant with ID: {assistant_id}")
        else:
            # Create a new assistant
            assistant = await client.beta.assistants.create(
                name="Twitter Community Archive Assistant",
                instructions=SYSTEM_PROMPT,
                tools=request_schemas,
                model="gpt-4o-mini",
            )
            logger.info(f"Created new assistant: {assistant}")

            # Update the .env file with the new assistant ID
            update_env_file(assistant.id, logger)

    except Exception as e:
        action = "update" if assistant_id else "create"
        logger.error(f"Failed to {action} assistant: {e}")

async def main():
    # Configure logging to output to the console
    logging.basicConfig(level=logging.INFO)
    
    # Load environment variables
    dotenv.load_dotenv()
    api_key = os.environ.get("OPENAI_API_KEY")
    assistant_id = os.environ.get("ASSISTANT_ID")

    # Initialize OpenAI client and instrument it
    client = AsyncOpenAI(api_key=api_key)

    # Define maximum
    MAX_ITER = 5

    # Split tool schemas into endpoint schemas and request schemas
    endpoint_schemas, request_schemas = split_tool_schemas(tools)

    logger = logging.getLogger(__name__)

    # Use the refactored function to create or update the assistant
    await create_or_update_assistant(client, assistant_id, request_schemas, logger)

# Run the main function
asyncio.run(main())
