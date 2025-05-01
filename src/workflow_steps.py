from box_agent_tools import get_box_agent
from workflow_classes import (
    WorkFlowState,
    BoxFileLocation,
    ScriptData,
    Locations,
    Roles,
    Props,
    Characters,
    Author,
    Producers,
    Directors,
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
    box_agent = get_box_agent(
        has_memory=False,
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
    state["script_file_read"] = response["messages"][-1].content
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
    state["locations"] = response["structured_response"]
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
    state["characters"] = response["structured_response"]
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
    state["props"] = response["structured_response"]

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

    state["characters"] = response["structured_response"]
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
    state["author"] = response["structured_response"]
    return {"author": response["structured_response"]}


def step_potential_producers(state: WorkFlowState) -> WorkFlowState:
    """Suggest potential producers for the script."""
    box_agent = get_box_agent(
        has_memory=False,
        response_format=Producers,
    )
    # Use the agent to fetch the file
    response = box_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": f"Suggest potential producers for the script {state['script_data']}, considering the type of work they are known for",
                }
            ]
        }
    )
    state["producers"] = response["structured_response"]
    # return {"producers": response["structured_response"]}
    return response["structured_response"]


def step_potential_directors(state: WorkFlowState) -> WorkFlowState:
    """Suggest potential directors for the script."""
    box_agent = get_box_agent(
        has_memory=False,
        response_format=Directors,
    )
    # Use the agent to fetch the file
    response = box_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": f"Suggest potential directors for the script {state['script_data']}, considering the type of work they are known for",
                }
            ]
        }
    )
    state["directors"] = response["structured_response"]
    # return {"directors": response["structured_response"]}
    return response["structured_response"]


def step_create_markdown(state: WorkFlowState) -> WorkFlowState:
    """Create markdown for the script."""
    box_agent = get_box_agent(
        has_memory=False,
    )
    # Use the agent to fetch the file
    response = box_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": f"Create a markdown report for the script with the following sections:"
                    f"About the script: (using {state['script_data']})"
                    f"Locations: {state['locations']}"
                    f"Characters: {state['characters']}"
                    f"Props: {state['props']}"
                    f"Author: {state['author']}"
                    f"Suggested Producers: {state['producers']}"
                    f"Suggested Directors: {state['directors']}"
                    f"do not add any other information",
                }
            ]
        }
    )
    state["markdown"] = response["messages"][-1].content
    return state
