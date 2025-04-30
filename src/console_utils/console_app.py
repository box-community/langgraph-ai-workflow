import time

from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt

console = Console()


def print_markdown(text: str) -> None:
    """
    Print the given text as markdown in the console.

    Args:
        text (str): The text to print as markdown.
    """
    md = Markdown(text)
    console.print(md)


def prompt_user(prompt: str) -> str:
    """
    Prompt the user for input and return the response.

    Args:
        prompt (str): The prompt to display to the user.

    Returns:
        str: The user's input.
    """
    return Prompt.ask(prompt)


def print_ai_message(ai_message: AIMessage):
    """
    Print the AI message in the console.

    Args:
        ai_message (AIMessage): The AI message to print.
    """
    print_markdown("**AI:**")

    # check if there are tool calls
    if hasattr(ai_message, "tool_calls") and ai_message.tool_calls:
        for call in ai_message.tool_calls:
            type_writer_effect_machine(
                f"  Using tool: {call['name']}", is_dim=True, delay=0.02
            )
            type_writer_effect_machine(
                f"  Arguments: {call['args']}", is_dim=True, delay=0.01
            )

    # if it has content
    if hasattr(ai_message, "content") and ai_message.content:
        # Print the AI message content
        print_markdown(f"{ai_message.content}")
        # type_writer_effect_machine(f"{ai_message.content}", is_dim=False, delay=0.01)

    if hasattr(ai_message, "structured_response") and ai_message.content:
        # Print the AI message content
        print(f"{ai_message.structured_response}")
        # type_writer_effect_machine(f"{ai_message.content}", is_dim=False, delay=0.01)


def print_tool_message(tool_message: ToolMessage):
    """
    Print the Tool message in the console.

    Args:
        tool_message (ToolMessage): The Tool message to print.
    """
    print_markdown("**Tool:**")

    type_writer_effect_machine(
        f" Tool name: {tool_message.name}", is_dim=True, delay=0.02
    )
    type_writer_effect_machine(
        f" Status: {tool_message.status}", is_dim=True, delay=0.01
    )
    console.print("Content:", style="dim")
    console.print(f"{tool_message.content}", style="dim")


def print_human_message(human_message: HumanMessage):
    """
    Print the Human message in the console.

    Args:
        human_message (HumanMessage): The Human message to print.
    """
    print_markdown("**Human:**")

    console.print(f" Content: {human_message.content}", style="dim")


def type_writer_effect_machine(message: str, is_dim: bool, delay: float = 0.01):
    """
    Simulate a typewriter effect for the given message.

    Args:
        message (str): The message to display.
        delay (float): The delay between each character.
    """
    for char in message:
        console.print(char, end="", style="dim" if is_dim else None, markup=True)
        time.sleep(delay)
    print()  # Move to the next line after the message is printed


def print_messages(messages: list[HumanMessage | AIMessage | ToolMessage]):
    """
    Print a list of messages in the console.

    Args:
        messages (list): The list of messages to print.
    """
    for message in messages:
        if isinstance(message, HumanMessage):
            print_human_message(message)
        elif isinstance(message, AIMessage):
            print_ai_message(message)
        elif isinstance(message, ToolMessage):
            print_tool_message(message)
