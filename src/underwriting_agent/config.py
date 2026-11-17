"""Model, repository paths, and Deep Agent filesystem backend."""

from __future__ import annotations

import os
from pathlib import Path

from deepagents import FilesystemPermission
from deepagents.backends import CompositeBackend, FilesystemBackend, StateBackend
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()


REPO_ROOT = Path(__file__).resolve().parents[2]
APPLICATIONS_DIR = REPO_ROOT / "data" / "applications"
POLICIES_DIR = REPO_ROOT / "policies"
SKILLS_DIR = REPO_ROOT / "skills"
WORKSPACE_DIR = REPO_ROOT / "data" / "workspace"
DEFAULT_MODEL = "anthropic:claude-haiku-5-5"

VIRTUAL_PREFIXES = {
    "/applications/": APPLICATIONS_DIR,
    "/policies/": POLICIES_DIR,
    "/skills/": SKILLS_DIR,
    "/workspace/": WORKSPACE_DIR,
}

PERMISSIONS = [
    FilesystemPermission(
        operations=["write"],
        paths=["/workspace/**"],
        mode="allow",
    ),
    FilesystemPermission(
        operations=["write"],
        paths=["/applications/**", "/policies/**", "/skills/**"],
        mode="deny",
    ),
]


def get_model():
    model_name = os.environ.get("UNDERWRITING_MODEL", DEFAULT_MODEL)
    model = init_chat_model(model_name)
    return model


def ensure_runtime_dirs() -> None:
    APPLICATIONS_DIR.mkdir(parents=True, exist_ok=True)
    WORKSPACE_DIR.mkdir(parents=True, exist_ok=True)
    (WORKSPACE_DIR / "extracted").mkdir(parents=True, exist_ok=True)


def build_backend() -> CompositeBackend:
    """Route loan files, policies, and skills to disk; keep other paths in state."""
    ensure_runtime_dirs()
    return CompositeBackend(
        default=StateBackend(),
        routes={
            "/applications/": FilesystemBackend(root_dir=APPLICATIONS_DIR, virtual_mode=True),
            "/policies/": FilesystemBackend(root_dir=POLICIES_DIR, virtual_mode=True),
            "/skills/": FilesystemBackend(root_dir=SKILLS_DIR, virtual_mode=True),
            "/workspace/": FilesystemBackend(root_dir=WORKSPACE_DIR, virtual_mode=True),
        },
    )


def resolve_virtual_path(virtual_path: str) -> Path:
    """Map a Deep Agent virtual path onto the repository."""
    path = virtual_path.strip()
    if not path.startswith("/"):
        path = f"/{path}"
    for prefix, root in VIRTUAL_PREFIXES.items():
        if path == prefix.rstrip("/") or path.startswith(prefix):
            relative = path[len(prefix) :].lstrip("/")
            resolved = (root / relative).resolve()
            if root.resolve() not in resolved.parents and resolved != root.resolve():
                raise ValueError(f"Path escapes routed directory: {virtual_path}")
            return resolved
    raise ValueError(
        f"Unsupported path {virtual_path!r}. Use /applications/, /policies/, /skills/, or /workspace/."
    )
