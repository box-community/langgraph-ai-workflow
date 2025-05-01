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
    step_create_markdown,
    step_fetch_file,
    step_potential_directors,
    step_potential_producers,
    step_read_box_file,
    step_suggest_actors_for_role,
)
from console_utils import (
    print_markdown,
)
from file_utils import save_image, save_markdown

dotenv.load_dotenv()

# Disable all logging below CRITICAL
logging.disable(logging.CRITICAL)


def main() -> None:
    """Main function to run the demo."""

    # Initialize Box client
    client = get_ccg_client()

    # Check connection
    user_info = client.users.get_user_me()
    print(f"Connected as: {user_info.name}")

    # Build workflow
    workflow = StateGraph(WorkFlowState)

    # Add nodes
    workflow.add_node("fetch_file", step_fetch_file)
    workflow.add_node("read_box_file", step_read_box_file)
    workflow.add_node("analyze_script", step_analyze_script)

    workflow.add_node("analyze_locations", step_analyze_locations)
    workflow.add_node("analyze_roles", step_analyze_roles)
    workflow.add_node("analyze_props", step_analyze_props)
    workflow.add_node("suggest_actors_for_role", step_suggest_actors_for_role)

    workflow.add_node("analyze_author", step_analyze_author)

    workflow.add_node("potential_producers", step_potential_producers)
    workflow.add_node("potential_directors", step_potential_directors)

    workflow.add_node("create_markdown", step_create_markdown)

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

    workflow.add_edge("analyze_script", "analyze_locations")
    workflow.add_edge("analyze_script", "analyze_props")
    workflow.add_edge("analyze_script", "analyze_roles")
    workflow.add_edge("analyze_roles", "suggest_actors_for_role")

    workflow.add_edge(
        ["suggest_actors_for_role", "analyze_locations", "analyze_props"],
        "analyze_author",
    )

    workflow.add_edge("analyze_author", "potential_producers")
    workflow.add_edge("analyze_author", "potential_directors")

    workflow.add_edge(["potential_producers", "potential_directors"], "create_markdown")
    workflow.add_edge("create_markdown", END)

    chain = workflow.compile()

    save_image(Image(chain.get_graph().draw_mermaid_png()), "output/workflow.png")

    state = WorkFlowState(
        box_script_file=BoxFileLocation(
            file_name="Limitless",
            parent_folder_name="Scripts",
        )
    )
    # Invoke
    state = chain.invoke(state)

    # print final document in markdown
    print_markdown("## Final Document")
    print_markdown(
        state["markdown"],
    )
    save_markdown(
        state["markdown"],
        "output/" + state["box_script_file"].file_name.replace(" ", "_") + ".md",
    )
    save_markdown(
        state["markdown"],
        "output/script_analysis.md",
    )


if __name__ == "__main__":
    main()
