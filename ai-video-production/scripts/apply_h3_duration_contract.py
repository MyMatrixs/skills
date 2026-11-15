#!/usr/bin/env python3
"""Apply a saved MiniMax H3 duration contract to one API-format workflow node.

The original workflow is never changed unless --in-place is explicitly selected.
This tool does not submit the workflow or verify a remote server schema.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def graph_nodes(workflow: dict) -> dict:
    nested = workflow.get("prompt")
    if isinstance(nested, dict):
        return nested
    return workflow


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workflow", required=True, type=Path)
    parser.add_argument("--contract", required=True, type=Path)
    destination = parser.add_mutually_exclusive_group(required=True)
    destination.add_argument("--output", type=Path, help="new duration-specific API workflow")
    destination.add_argument("--in-place", action="store_true", help="replace --workflow only when explicitly intended")
    parser.add_argument("--node-id", help="required only when the graph has multiple H3 ReferenceToVideo nodes")
    args = parser.parse_args()

    workflow = load_json(args.workflow)
    contract = load_json(args.contract)
    frames = contract.get("generation_frames")
    if not isinstance(frames, int) or frames < 1:
        parser.error("--contract must contain a positive integer generation_frames")

    nodes = graph_nodes(workflow)
    matches = [
        str(node_id) for node_id, node in nodes.items()
        if isinstance(node, dict) and node.get("class_type") == "MiniMaxH3ReferenceToVideo"
    ]
    if args.node_id:
        if args.node_id not in matches:
            parser.error(f"--node-id {args.node_id!r} is not a MiniMaxH3ReferenceToVideo node; matches: {matches}")
        selected = args.node_id
    elif len(matches) == 1:
        selected = matches[0]
    elif not matches:
        parser.error("workflow has no MiniMaxH3ReferenceToVideo node")
    else:
        parser.error(f"workflow has multiple H3 nodes {matches}; pass --node-id")

    node = nodes[selected]
    inputs = node.setdefault("inputs", {})
    previous = inputs.get("length")
    inputs["length"] = frames
    node.setdefault("_meta", {})
    node["_meta"]["duration_contract"] = {
        "requested_duration_seconds": contract.get("requested_duration_seconds"),
        "generation_frames": frames,
        "generation_duration_seconds": contract.get("generation_duration_seconds"),
        "status": contract.get("status"),
    }

    output = args.workflow if args.in_place else args.output
    assert output is not None
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(workflow, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "workflow": str(output), "node_id": selected, "previous_length": previous,
        "generation_frames": frames, "contract": str(args.contract),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
