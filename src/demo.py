import logging

import dotenv
from box_ai_agents_toolkit import get_ccg_client
from IPython.display import Image
from langgraph.graph import END, START, StateGraph

from box_agent import (
    BoxFileLocation,
    WorkFlowState,
    step_analyze_author,
    step_analyze_locations,
    step_analyze_props,
    step_analyze_roles,
    step_analyze_script,
    step_check_file,
    step_dummy,
    step_fetch_file,
    step_read_box_file,
    step_suggest_actors_for_role,
)
from console_utils.console_app import (
    print_markdown,
)
from utils import save_image

dotenv.load_dotenv()

# Disable all logging below CRITICAL
logging.disable(logging.CRITICAL)


def main() -> None:
    """Main function to run the demo."""

    # Initialize Box client
    client = get_ccg_client()

    # Get user info for status message
    user_info = client.users.get_user_me()
    print(f"Connected as: {user_info.name}")

    # box_agent = get_box_agent(has_memory=False, response_format=BoxFileLocation)

    # Build workflow
    workflow = StateGraph(WorkFlowState)

    # Add nodes
    workflow.add_node("fetch_file", step_fetch_file)
    workflow.add_node("read_box_file", step_read_box_file)
    workflow.add_node("analyze_script", step_analyze_script)
    # workflow.add_node("analyze_author", step_analyze_author)

    workflow.add_node("analyze_locations", step_analyze_locations)
    workflow.add_node("analyze_roles", step_analyze_roles)
    workflow.add_node("analyze_props", step_analyze_props)
    # workflow.add_node("aggregator", step_dummy)
    workflow.add_node("suggest_actors_for_role", step_suggest_actors_for_role)

    workflow.add_node("analyze_author", step_analyze_author)

    workflow.add_node("dummy", step_dummy)

    # Add edges to connect nodes
    workflow.add_edge(START, "fetch_file")

    workflow.add_conditional_edges(
        "fetch_file",
        step_check_file,
        {  # Name returned by route_joke : Name of next node to visit
            "Found": "read_box_file",
            "Not Found": END,
        },
    )
    workflow.add_edge("read_box_file", "analyze_script")
    # workflow.add_edge("analyze_script", "analyze_author")

    workflow.add_edge("analyze_script", "analyze_locations")
    workflow.add_edge("analyze_script", "analyze_props")
    workflow.add_edge("analyze_script", "analyze_roles")
    workflow.add_edge("analyze_roles", "suggest_actors_for_role")
    workflow.add_edge("suggest_actors_for_role", "analyze_author")
    workflow.add_edge("analyze_locations", "analyze_author")
    workflow.add_edge("analyze_props", "analyze_author")
    workflow.add_edge("analyze_author", "dummy")
    workflow.add_edge("dummy", END)

    # Compile
    chain = workflow.compile()

    # Show workflow
    save_image(Image(chain.get_graph().draw_mermaid_png()), "img/demo.png")

    state = WorkFlowState(
        box_script_file=BoxFileLocation(
            file_name="I, Robot",
            parent_folder_name="Scripts",
        )
    )
    # Invoke
    state = chain.invoke(state)
    print("State after invoking the chain:")
    state.pop("script_file_read")
    print(state)
    # print author details
    print_markdown("## Author Details")
    print(state["author"])


if __name__ == "__main__":
    main()
