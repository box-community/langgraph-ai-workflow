from typing import TypedDict, Union

from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.graph import CompiledGraph
from langgraph.prebuilt import create_react_agent
from pydantic import BaseModel, Field

from box.box_agent_tools import init_tools

StructuredResponseSchema = Union[dict, type[BaseModel]]


class BoxFileLocation(BaseModel):
    """Model for Box file location."""

    file_name: str = Field(None, description="Name of the file.")
    file_id: str = Field(None, description="Box file id.")
    parent_folder_name: str = Field(None, description="Name of the parent folder.")


class ScriptData(BaseModel):
    """Model for script data."""

    title: str = Field(None, description="Title of the script.")
    author: str = Field(None, description="Author of the script.")
    genre: str = Field(None, description="Genre of the script.")
    date: str = Field(None, description="Date of the script.")
    plot_summary: str = Field(None, description="Plot summary of the script.")


class Location(BaseModel):
    name: str = Field(None, description="Name of the location.")
    description: str = Field(None, description="Description of the location.")


class Locations(BaseModel):
    locations: list[Location] = Field(
        None, description="List of locations in the script."
    )


class SuggestedActor(BaseModel):
    name: str = Field(None, description="Name of the actor.")
    description: str = Field(None, description="Description of the actor.")


class Role(BaseModel):
    role: str = Field(None, description="Name of the movie role.")
    description: str = Field(None, description="Description of the role.")


class Roles(BaseModel):
    roles: list[Role] = Field(None, description="List of roles in the script.")


class Character(BaseModel):
    name: str = Field(None, description="Name of the character.")
    description: str = Field(None, description="Description of the character.")
    # role: str = Field(None, description="Role of the character.")
    suggested_actors: list[SuggestedActor] = Field(
        None, description="List of suggested actors for the character."
    )


class Characters(BaseModel):
    characters: list[Character] = Field(
        None, description="List of characters in the script."
    )


class Prop(BaseModel):
    name: str = Field(None, description="Name of the prop.")
    description: str = Field(None, description="Description of the prop.")


class Props(BaseModel):
    props: list[Prop] = Field(None, description="List of props in the script.")


class AuthorAccomplishment(BaseModel):
    name: str = Field(None, description="Name of the accomplishment.")
    description: str = Field(None, description="Description of the accomplishment.")


class AuthorOtherMovieScript(BaseModel):
    name: str = Field(None, description="Name of the other movie script.")
    description: str = Field(None, description="Description of the other movie script.")


class AuthorWorkedWith(BaseModel):
    name: str = Field(
        None, description="Name of the company or organizations worked with."
    )
    description: str = Field(
        None, description="Description of the company or organizations worked with."
    )


class Author(BaseModel):
    accomplishments: list[AuthorAccomplishment] = Field(
        None, description="List of accomplishments of the author."
    )
    other_movie_scripts: list[AuthorOtherMovieScript] = Field(
        None, description="List of other movie scripts by the author."
    )
    worked_with: list[AuthorWorkedWith] = Field(
        None, description="List of companies or organizations worked with the author."
    )


# Graph state
class WorkFlowState(TypedDict):
    box_script_file: BoxFileLocation
    script_file_read: str
    script_data: ScriptData
    locations: Locations
    roles: Roles
    characters: Characters
    props: Props
    author: Author


def get_box_agent(
    has_memory: bool = False,
    response_format: StructuredResponseSchema
    | tuple[str, StructuredResponseSchema]
    | None = None,
) -> CompiledGraph:
    # Initialize language model
    model = init_chat_model("gpt-4o", model_provider="openai")
    # model_structured = model.with_structured_output(BoxFileLocation)

    # Create the Box agent
    if has_memory:
        memory = MemorySaver()
    else:
        memory = None
    tools = init_tools()
    return create_react_agent(
        model, tools, checkpointer=memory, response_format=response_format
    )


def step_dummy(state: WorkFlowState) -> WorkFlowState:
    """Dummy step to demonstrate the workflow."""
    # This is a placeholder for any processing you want to do
    # For now, it just returns the state unchanged
    return state


def step_fetch_file(state: WorkFlowState) -> WorkFlowState:
    """Fetch a file from Box."""
    box_agent = get_box_agent(
        has_memory=False,
        response_format=BoxFileLocation,
    )
    # Use the agent to fetch the file
    response = box_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": f"locate the file {state['box_script_file'].file_name} under my {state['box_script_file'].parent_folder_name} folder",
                }
            ]
        }
    )

    state["box_script_file"] = response["structured_response"]
    return state


def step_check_file(state: WorkFlowState) -> WorkFlowState:
    """Check if the file exists in Box."""

    if state["box_script_file"].file_id:
        return "Found"
    else:
        return "Not Found"


def step_read_box_file(state: WorkFlowState) -> WorkFlowState:
    """Read the file from Box."""
    # This is a placeholder for any processing you want to do
    # For now, it just returns the state unchanged
    box_agent = get_box_agent(
        has_memory=False,
        # response_format={"content": str},
    )
    # Use the agent to fetch the file
    response = box_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": f"Read the box file id {state['box_script_file'].file_id} and respond with the actual text content of the movie scrip",
                }
            ]
        }
    )
    # print_messages(response["messages"])
    state["script_file_read"] = response["messages"][-1].content
    # state["script_file_read"] = response["structured_response"]
    return state


def step_analyze_script(state: WorkFlowState) -> WorkFlowState:
    """Analyze the script."""
    box_agent = get_box_agent(
        has_memory=False,
        response_format=ScriptData,
    )
    # Use the agent to fetch the file
    response = box_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": f"Analyze the script {state['script_file_read']}",
                }
            ]
        }
    )
    # print_messages(response["messages"])
    # state["script_file_read"] = response["messages"][-1].content
    state["script_data"] = response["structured_response"]
    return state


def step_analyze_locations(state: WorkFlowState) -> WorkFlowState:
    """Analyze the locations in the script."""
    box_agent = get_box_agent(
        has_memory=False,
        response_format=Locations,
    )
    # Use the agent to fetch the file
    response = box_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": f"Analyze the locations in the script {state['script_file_read']}",
                }
            ]
        }
    )
    # print_messages(response["messages"])
    # state["script_file_read"] = response["messages"][-1].content
    state["locations"] = response["structured_response"]
    # return state
    return response["structured_response"]


def step_analyze_roles(state: WorkFlowState) -> WorkFlowState:
    """Analyze the characters in the script."""
    box_agent = get_box_agent(
        has_memory=False,
        response_format=Roles,
    )
    # Use the agent to fetch the file
    response = box_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": f"Analyze the characters in the script {state['script_file_read']}, ignoring the suggested actors",
                }
            ]
        }
    )
    # print_messages(response["messages"])
    # state["script_file_read"] = response["messages"][-1].content
    state["characters"] = response["structured_response"]
    # return state
    return response["structured_response"]


def step_analyze_props(state: WorkFlowState) -> WorkFlowState:
    """Analyze the props in the script."""
    box_agent = get_box_agent(
        has_memory=False,
        response_format=Props,
    )
    # Use the agent to fetch the file
    response = box_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": f"Analyze the props in the script {state['script_file_read']}",
                }
            ]
        }
    )
    # print_messages(response["messages"])
    # state["script_file_read"] = response["messages"][-1].content
    state["props"] = response["structured_response"]
    # return state

    return response["structured_response"]


def step_aggregate_analysis(state: WorkFlowState) -> WorkFlowState:
    """Aggregate the analysis results."""
    print("Aggregating analysis results...")
    print(state)
    return state


def step_suggest_actors_for_role(state: WorkFlowState) -> WorkFlowState:
    """Suggest actors for each character in the script."""
    box_agent = get_box_agent(
        has_memory=False,
        response_format=Characters,
    )
    # Use the agent to fetch the file
    response = box_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": f"Suggest 3 modern day actors for each character in the script, excluding the original actor if any {state['roles']}",
                }
            ]
        }
    )
    # print_messages(response["messages"])
    # state["script_file_read"] = response["messages"][-1].content

    state["characters"] = response["structured_response"]
    # return state
    return response["structured_response"]


def step_analyze_author(state: WorkFlowState) -> WorkFlowState:
    """Analyze the author of the script."""
    box_agent = get_box_agent(
        has_memory=False,
        response_format=Author,
    )
    # Use the agent to fetch the file
    response = box_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": f"Analyze the author of the script {state['script_data']}, including their accomplishments, other movie scripts, and companies or organizations they have worked with",
                }
            ]
        }
    )
    # print_messages(response["messages"])
    # state["script_file_read"] = response["messages"][-1].content
    state["author"] = response["structured_response"]
    # return state
    return {"author": response["structured_response"]}
