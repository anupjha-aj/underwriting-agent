"""Load product rules from YAML so thresholds are data, not prompt text."""

from __future__ import annotations

import json
from pathlib import Path

import yaml
from langchain.tools import tool

from underwriting_agent.config import POLICIES_DIR


def _products_index_path() -> Path:
    return POLICIES_DIR / "products.yaml"


def load_products_index() -> dict:
    path = _products_index_path()
    if not path.is_file():
        raise FileNotFoundError(f"Missing product registry at {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError("products.yaml must be a mapping")
    return data


def load_policy_dict(product_id: str) -> dict:
    index = load_products_index()
    products = index.get("products") or {}
    entry = products.get(product_id)
    if entry is None:
        known = ", ".join(sorted(products)) or "(none)"
        raise KeyError(f"Unknown product_id {product_id!r}. Known: {known}")
    policy_file = POLICIES_DIR / entry["policy_file"]
    if not policy_file.is_file():
        raise FileNotFoundError(f"Missing policy file {policy_file}")
    policy = yaml.safe_load(policy_file.read_text(encoding="utf-8")) or {}
    if not isinstance(policy, dict):
        raise ValueError(f"{policy_file.name} must be a mapping")
    policy.setdefault("product_id", product_id)
    policy["policy_file"] = f"/policies/{entry['policy_file']}"
    narrative = entry.get("narrative_file")
    if narrative:
        policy["narrative_file"] = f"/policies/{narrative}"
    return policy


@tool
def list_products() -> str:
    """List product_ids in the policy registry and the default product."""
    try:
        index = load_products_index()
    except (OSError, ValueError) as exc:
        return f"Error: {exc}"
    return json.dumps(index, indent=2)


@tool
def load_product_policy(product_id: str) -> str:
    """Load structured credit policy and product rules for a product_id.

    Returns JSON with limits, required document sets, and paths to narrative policy files.
    """
    try:
        policy = load_policy_dict(product_id)
    except (OSError, KeyError, ValueError) as exc:
        return f"Error: {exc}"
    return json.dumps(policy, indent=2)
