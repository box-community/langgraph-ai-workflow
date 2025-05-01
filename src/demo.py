import logging

import dotenv
from box_ai_agents_toolkit import get_ccg_client

from workflow_design import build_workflow
from workflow_classes import (
    BoxFileLocation,
    WorkFlowState,
)
from console_utils import (
    print_markdown,
)
from file_utils import save_markdown

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

    chain = build_workflow()

    state = WorkFlowState(
        box_script_file=BoxFileLocation(
            file_name="MINORITY REPORT - by Jon Cohen",
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
