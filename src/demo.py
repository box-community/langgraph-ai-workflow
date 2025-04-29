import logging
import uuid

import dotenv
from box_ai_agents_toolkit import get_ccg_client
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from pydantic import BaseModel, Field

from box.box_agent_tools import (
    init_tools,
)
from console_utils.console_app import (
    print_markdown,
)

dotenv.load_dotenv()

# Disable all logging below CRITICAL
logging.disable(logging.CRITICAL)


class BoxFileLocation(BaseModel):
    """Model for Box file location."""

    file_name: str = Field(None, description="Name of the file.")
    file_id: str = Field(None, description="Box file id.")


def main() -> None:
    """Main function to run the demo."""

    # Initialize Box client
    client = get_ccg_client()

    # Get user info for status message
    user_info = client.users.get_user_me()
    print(f"Connected as: {user_info.name}")

    # Initialize language model
    model = init_chat_model("gpt-4o-mini", model_provider="openai")
    # model_structured = model.with_structured_output(BoxFileLocation)

    # Create the Box agent
    memory = MemorySaver()
    tools = init_tools()
    box_agent = create_react_agent(
        model, tools, checkpointer=memory, response_format=BoxFileLocation
    )

    chat_id = uuid.uuid4()
    chat_config = {"configurable": {"thread_id": str(chat_id)}}

    conversation = box_agent.invoke(
        {
            "messages": [
                HumanMessage(
                    content="locate the file Aliens - by James Cameron under my Scripts folder"
                )
            ]
        },
        chat_config,
    )

    print_markdown("---")
    # print(conversation["structured_response"])
    script_location: BoxFileLocation = conversation["structured_response"]
    print(script_location.model_dump())
    print_markdown("---")


if __name__ == "__main__":
    main()
