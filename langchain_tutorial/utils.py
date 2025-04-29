import dotenv
from IPython.display import Image
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()


def get_llm() -> ChatOpenAI:
    """Initialize the LLM with the specified model."""
    # Initialize the LLM with the specified model
    # Note: The model name "gpt-4o-mini" is a placeholder and should be replaced with the actual model name you want to use.
    # For example, you might use "gpt-3.5-turbo" or "gpt-4" depending on your requirements and availability.
    # Ensure that you have access to the specified model in your OpenAI account.
    return ChatOpenAI(model="gpt-4o-mini")


def save_image(image: Image, filename):
    """Save the image to a file."""
    with open(filename, "wb") as f:
        f.write(image.data)
