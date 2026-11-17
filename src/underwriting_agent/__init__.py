"""Underwriting Deep Agent package."""

from underwriting_agent.graph import agent


def main() -> None:
    print(
        "Underwriting Deep Agent. Start LangGraph Studio with:\n"
        "  uv run langgraph dev\n"
        "Then underwrite a folder under /applications/."
    )


__all__ = ["agent", "main"]
