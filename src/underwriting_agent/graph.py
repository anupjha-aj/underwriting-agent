"""LangGraph Deep Agent entrypoint for Studio (`langgraph.json`)."""

from __future__ import annotations

from deepagents import create_deep_agent
from dotenv import load_dotenv

from underwriting_agent.config import PERMISSIONS, build_backend, get_model
from underwriting_agent.models import CreditDecision
from underwriting_agent.prompts import SUPERVISOR_PROMPT
from underwriting_agent.subagents import build_subagents
from underwriting_agent.tools import ALL_TOOLS

load_dotenv()

agent = create_deep_agent(
    model=get_model(),
    tools=ALL_TOOLS,
    system_prompt=SUPERVISOR_PROMPT,
    subagents=build_subagents(),
    skills=["/skills/"],
    permissions=PERMISSIONS,
    backend=build_backend(),
    name="underwriting-agent",
)
