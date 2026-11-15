#!/usr/bin/env python3
"""Validate a ComfyUI API prompt against a captured /object_info response."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def is_link(value: object) -> bool:
    return isinstance(value, list) and len(value) == 2 and isinstance(value[0], str) and isinstance(value[1], int)


def is_dynamic_selector(class_type: object, input_name: str) -> bool:
    """Return true for selectors populated after an object-info capture."""
    return class_type == "LoadImage" and input_name == "image"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workflow", required=True, type=Path)
    parser.add_argument("--object-info", required=True, type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    workflow = json.loads(args.workflow.read_text(encoding="utf-8-sig"))
    prompt = workflow.get("prompt", workflow)
    schema = json.loads(args.object_info.read_text(encoding="utf-8-sig"))
    if not isinstance(prompt, dict) or not isinstance(schema, dict):
        parser.error("workflow and object-info must be JSON objects")

    errors: list[dict[str, str]] = []
    for node_id, node in prompt.items():
        if not isinstance(node, dict):
            errors.append({"node": str(node_id), "error": "node is not an object"})
            continue
        class_type = node.get("class_type")
        inputs = node.get("inputs", {})
        node_schema = schema.get(class_type)
        if not isinstance(node_schema, dict):
            errors.append({"node": str(node_id), "error": f"unknown class_type {class_type!r}"})
            continue
        required = node_schema.get("input", {}).get("required", {})
        for name, definition in required.items():
            if name not in inputs:
                errors.append({"node": str(node_id), "error": f"missing required input {name}"})
                continue
            value = inputs[name]
            if is_link(value) or not isinstance(definition, list) or not definition:
                continue
            choices = definition[0]
            if isinstance(choices, list) and not is_dynamic_selector(class_type, name) and value not in choices:
                errors.append({"node": str(node_id), "error": f"{name} value {value!r} is not an allowed selector"})
    report = {"workflow": str(args.workflow), "valid": not errors, "errors": errors}
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.report:
        args.report.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    raise SystemExit(0 if not errors else 1)


if __name__ == "__main__":
    main()
