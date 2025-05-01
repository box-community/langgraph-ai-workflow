from IPython.display import Image
from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph

from workflow_steps import (
    WorkFlowState,
    step_analyze_author,
    step_analyze_locations,
    step_analyze_props,
    step_analyze_roles,
    step_analyze_script,
    step_check_file,
    step_create_markdown,
    step_locate_file_in_box,
    step_potential_directors,
    step_potential_producers,
    step_read_box_file,
    step_suggest_actors_for_role,
)

from file_utils import save_image


def build_workflow() -> CompiledStateGraph:
    """Builds the workflow for the script analysis process."""

    workflow = StateGraph(WorkFlowState)

    # Add nodes
    workflow.add_node("fetch_file", step_locate_file_in_box)
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
        {
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

    return chain
