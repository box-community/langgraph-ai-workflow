from typing import List, Union

from box_ai_agents_toolkit import (
    File,
    Folder,
    SearchForContentContentTypes,
    box_file_ai_ask,
    box_file_ai_extract,
    box_file_text_extract,
    box_folder_list_content,
    box_locate_folder_by_name,
    box_search,
    get_ccg_client,
)
from langchain.tools.base import StructuredTool
from langchain_core.tools import BaseTool
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.graph import CompiledGraph
from langgraph.prebuilt import create_react_agent
from pydantic import BaseModel


StructuredResponseSchema = Union[dict, type[BaseModel]]


def init_tools():
    """Initialize the tools for the agent."""
    tools: List[BaseTool] = []
    tools.append(
        StructuredTool.from_function(
            box_who_am_i,
            parse_docstring=True,
        )
    )
    tools.append(
        StructuredTool.from_function(
            box_search_tool,
            parse_docstring=True,
        )
    )
    tools.append(
        StructuredTool.from_function(
            box_read_tool,
            parse_docstring=True,
        )
    )
    tools.append(
        StructuredTool.from_function(
            box_ask_ai_tool,
            parse_docstring=True,
        )
    )
    tools.append(
        StructuredTool.from_function(
            box_search_folder_by_name,
            parse_docstring=True,
        )
    )
    tools.append(
        StructuredTool.from_function(
            box_ai_extract_data,
            parse_docstring=True,
        )
    )
    tools.append(
        StructuredTool.from_function(
            box_list_folder_content_by_folder_id,
            parse_docstring=True,
        )
    )

    return tools


def get_box_agent(
    has_memory: bool = False,
    response_format: StructuredResponseSchema
    | tuple[str, StructuredResponseSchema]
    | None = None,
) -> CompiledGraph:
    # Initialize language model
    model = init_chat_model("gpt-4o", model_provider="openai")

    # Create the Box agent
    if has_memory:
        memory = MemorySaver()
    else:
        memory = None
    tools = init_tools()
    return create_react_agent(
        model, tools, checkpointer=memory, response_format=response_format
    )


def box_who_am_i() -> dict:
    """who am I, Retrieves the current user's information in box. Checks the connection to Box

    Returns:
        str: A string containing the current user's information.
    """
    client = get_ccg_client()
    return client.users.get_user_me().to_dict()


def box_search_tool(
    query: str,
    file_extensions: List[str] | None = None,
    where_to_look_for_query: List[str] | None = None,
    ancestor_folder_ids: List[str] | None = None,
) -> List[dict]:
    """Searches for files in Box using the specified query and filters.

    Args:
        query (str): The search query.
        file_extensions (List[str] | None): A list of file extensions to filter results (e.g., ['.pdf']).
        where_to_look_for_query (List[str] | None): Specifies where to search for the query. Possible values:
            NAME
            DESCRIPTION
            FILE_CONTENT
            COMMENTS
            TAG
        ancestor_folder_ids (List[str] | None): A list of ancestor folder IDs to limit the search scope.

    Returns:
        dict: A list of a dictionary of ["id", "name", "type", "size", "description"].
    """
    client = get_ccg_client()
    # Convert the where to look for query to content types
    content_types: List[SearchForContentContentTypes] = []
    if where_to_look_for_query:
        for content_type in where_to_look_for_query:
            content_types.append(SearchForContentContentTypes[content_type])

    # Search for files with the query
    search_results = box_search(
        client, query, file_extensions, content_types, ancestor_folder_ids
    )

    # Return the dictionary of each file in the search results
    return [file.to_dict() for file in search_results]


def box_read_tool(file_id: str) -> str:
    """Reads the text content of a file in Box.

    Args:
        file_id (str): The ID of the file to read.

    Returns:
        str: The text content of the file.
    """
    client = get_ccg_client()
    response = box_file_text_extract(client, file_id)
    return response


def box_ask_ai_tool(file_id: str, prompt: str) -> dict:
    """Asks Box AI about a file in Box.

    Args:
        file_id (str): The ID of the file to analyze.
        prompt (str): The prompt or question to ask the AI.

    Returns:
        dict: The AI-generated response based on the file's content.
    """
    client = get_ccg_client()
    response = box_file_ai_ask(client, file_id, prompt=prompt)

    return response


def box_search_folder_by_name(folder_name: str) -> List[dict]:
    """Locates a folder in Box by its name.

    Args:
        folder_name (str): The name of the folder to locate.

    Returns:
        List[dict]: A list of a dict with ["id", "name", "type"] string containing the folder's ID and name.
    """
    client = get_ccg_client()
    search_results = box_locate_folder_by_name(client, folder_name)

    return [folder.to_dict() for folder in search_results]


def box_ai_extract_data(file_id: str, fields: str) -> dict:
    """Extracts data from a file in Box using AI.

    Args:
        file_id (str): The ID of the file to analyze.
        fields (str): The fields to extract from the file.

    Returns:
        dict: The extracted data as a dict.
    """
    client = get_ccg_client()
    response = box_file_ai_extract(client, file_id, fields)

    return response


def box_list_folder_content_by_folder_id(
    folder_id: str, is_recursive: bool
) -> List[dict]:
    """Lists the content of a folder in Box by its ID.

    Args:
        folder_id (str): The ID of the folder to list the content of.
        is_recursive (bool): Whether to list the content recursively.

    Returns:
        List[dict]: A list with the content of the folder in a dict, including the "id", "name", "type", and "description".
    """
    client = get_ccg_client()

    response: List[Union[File, Folder]] = box_folder_list_content(
        client, folder_id, is_recursive
    )

    return [item.to_dict() for item in response]
