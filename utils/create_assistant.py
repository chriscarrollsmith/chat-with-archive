import os
import logging
import asyncio
from dotenv import load_dotenv
from openai import AsyncOpenAI
from openai.types.beta.assistant_create_params import AssistantCreateParams
from openai.types.beta.assistant import Assistant
from utils.tools import SYSTEM_PROMPT, REQUEST_SCHEMAS


def update_env_file(var_name: str, var_value: str, logger: logging.Logger):
    """
    Update the .env file with a new environment variable.

    If the .env file already contains the specified variable, it will be updated.
    The new value will be appended to the .env file if it doesn't exist.
    If the .env file does not exist, it will be created.

    Args:
        var_name: The name of the environment variable to update
        var_value: The value to set for the environment variable
        logger: Logger instance for output
    """
    lines = []
    # Read existing contents if file exists
    if os.path.exists('.env'):
        with open('.env', 'r') as env_file:
            lines = env_file.readlines()

        # Remove any existing line with this variable
        lines = [line for line in lines if not line.startswith(f"{var_name}=")]
    else:
        # Log when we're creating a new .env file
        logger.info("Creating new .env file")

    # Write back all lines including the new variable
    with open('.env', 'w') as env_file:
        env_file.writelines(lines)
        env_file.write(f"{var_name}={var_value}\n")
    
    logger.debug(f"Environment variable {var_name} written to .env: {var_value}")


async def create_or_update_assistant(
        client: AsyncOpenAI,
        assistant_id: str,
        request: AssistantCreateParams,
        logger: logging.Logger
) -> str:
    """
    Create or update the assistant based on the presence of an assistant_id.
    """
    try:
        if assistant_id:
            # Update the existing assistant
            assistant: Assistant = await client.beta.assistants.update(
                assistant_id,
                **request
            )
            logger.info(f"Updated assistant with ID: {assistant_id}")
        else:
            # Create a new assistant
            assistant: Assistant = await client.beta.assistants.create(**request)
            logger.info(f"Created new assistant: {assistant.id}")

            # Update the .env file with the new assistant ID
            update_env_file("ASSISTANT_ID", assistant.id, logger)
    
        return assistant.id

    except Exception as e:
        action = "update" if assistant_id else "create"
        logger.error(f"Failed to {action} assistant: {e}")


request: AssistantCreateParams = AssistantCreateParams(
    instructions=SYSTEM_PROMPT,
    name="Community Archive Assistant",
    model="gpt-4o",
    tools=REQUEST_SCHEMAS,
)


# Run the assistant creation in an asyncio event loop
if __name__ == "__main__":
    import sys

    # Configure logger to stream to console
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    logger: logging.Logger = logging.getLogger(__name__)
    
    load_dotenv()
    assistant_id = os.getenv("ASSISTANT_ID")

    # Initialize the OpenAI client
    openai: AsyncOpenAI = AsyncOpenAI()

    # Run the main function in an asyncio event loop
    asyncio.run(
        create_or_update_assistant(openai, assistant_id, request, logger)
    )
