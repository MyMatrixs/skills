#!/usr/bin/env python3
"""Create and update an atomic local ledger for a remote video-generation batch."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path


STATES = {"planned", "submitted", "remote_completed", "retrieval_pending", "retrieved", "verified", "failed"}


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def save_atomic(path: Path, ledger: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(temp, path)


def read_shot_ids(path: Path) -> list[str]:
    data = load(path)
    shots = data.get("shots", []) if isinstance(data, dict) else []
    ids = [shot.get("id") for shot in shots if isinstance(shot, dict) and isinstance(shot.get("id"), str)]
    if not ids:
        raise SystemExit("shots JSON contains no shot ids")
    return ids


def init(args: argparse.Namespace) -> None:
    if args.ledger.exists():
        raise SystemExit(f"refusing to overwrite {args.ledger}")
    ledger = {"schema": 1, "created_at": now(), "shots": {shot_id: {"status": "planned", "events": [{"at": now(), "status": "planned"}]} for shot_id in read_shot_ids(args.shots)}}
    save_atomic(args.ledger, ledger)
    print(args.ledger)


def update(args: argparse.Namespace) -> None:
    ledger = load(args.ledger)
    row = ledger.get("shots", {}).get(args.shot_id)
    if not isinstance(row, dict):
        raise SystemExit(f"unknown shot id: {args.shot_id}")
    if args.status not in STATES:
        raise SystemExit(f"invalid state: {args.status}")
    if args.status == "verified":
        if not args.local_output or not args.sha256:
            raise SystemExit("verified requires --local-output and --sha256")
        file_path = Path(args.local_output)
        if file_path.is_file() and hashlib.sha256(file_path.read_bytes()).hexdigest().lower() != args.sha256.lower():
            raise SystemExit("provided SHA-256 does not match local output")
    fields = {"prompt_id": args.prompt_id, "remote_filename": args.remote_filename, "local_output": args.local_output, "sha256": args.sha256, "reason": args.reason}
    for key, value in fields.items():
        if value is not None:
            row[key] = value
    row["status"] = args.status
    row.setdefault("events", []).append({"at": now(), "status": args.status, **{key: value for key, value in fields.items() if value is not None}})
    save_atomic(args.ledger, ledger)
    print(json.dumps({"shot_id": args.shot_id, "status": args.status}, ensure_ascii=False))


def summary(args: argparse.Namespace) -> None:
    ledger = load(args.ledger)
    counts: dict[str, int] = {}
    for row in ledger.get("shots", {}).values():
        state = row.get("status", "unknown")
        counts[state] = counts.get(state, 0) + 1
    print(json.dumps({"ledger": str(args.ledger), "counts": counts}, ensure_ascii=False, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    actions = parser.add_subparsers(required=True)
    create = actions.add_parser("init")
    create.add_argument("--shots", required=True, type=Path)
    create.add_argument("--ledger", required=True, type=Path)
    create.set_defaults(func=init)
    change = actions.add_parser("update")
    change.add_argument("--ledger", required=True, type=Path)
    change.add_argument("--shot-id", required=True)
    change.add_argument("--status", required=True, choices=sorted(STATES))
    change.add_argument("--prompt-id")
    change.add_argument("--remote-filename")
    change.add_argument("--local-output")
    change.add_argument("--sha256")
    change.add_argument("--reason")
    change.set_defaults(func=update)
    show = actions.add_parser("summary")
    show.add_argument("--ledger", required=True, type=Path)
    show.set_defaults(func=summary)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
