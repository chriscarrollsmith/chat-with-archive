import logging
import os
import dotenv
from openai import AsyncOpenAI
from tools import tools, split_tool_schemas
import asyncio

async def main():
    # Configure logging to output to the console
    logging.basicConfig(level=logging.INFO)
    
    # Load environment variables
    dotenv.load_dotenv()
    api_key = os.environ.get("OPENAI_API_KEY")

    # Initialize OpenAI client and instrument it
    client = AsyncOpenAI(api_key=api_key)

    # Define maximum
    MAX_ITER = 5

    # Split tool schemas into endpoint schemas and request schemas
    endpoint_schemas, request_schemas = split_tool_schemas(tools)

    # Set system prompt
    system_prompt = """Users will ask you questions about activity on Twitter, as represented in data voluntarily uploaded to the Twitter Community Archive. You have no access to Twitter itself and cannot answer questions about Twitter activity outside of what is in the archive. Always format your responses in markdown. Be proactive about soliciting from the user any parameters needed to answer their questions, but don't refuse a query just because it's a bit vague. For instance, if the user asks about their own activity but neglects to provide any identifying information, you should ask for their username. Fulfill the user's request if at all possible even if it's vague, but invite them to be more specific in their next message when you present the results. Since the Twitter Community Archive API is a PostgREST API, you must use PostgREST operators for filtering. If possible, you should retrieve any information requested by the user using a single API call. You may use nested resource embedding or include logical operator keys in your request parameters to construct complex user queries. Always use the `limit` parameter to paginate results! Requesting more than 50 results at a time is abusive of the Twitter Community Archive API. Please do not abuse our tools! When constructing nested queries, you should pay close attention to foreign key relationships and endpoint names specified in the schema. For example, if the user wants bios for their followers, you cannot use `follower_account_id` from `get_followers`, because that variable has no foreign key relationships. Instead, you should use `account_id` from `get_following_accounts`, because that variable has a foreign key relationship to `account.account_id`, which in turn has a relationship to `user_profiles.account_id`. The nested "select" parameter would look like this: `account(account_id,profile(bio))`."""

    # Create the assistant
    assistant = await client.beta.assistants.create(
      name="Twitter Community Archive Assistant",
      instructions=system_prompt,
      tools=request_schemas,
      model="gpt-4o-mini",
    )

    logger = logging.getLogger(__name__)
    logger.info(f"Created assistant: {assistant}")

# Run the main function
asyncio.run(main())
