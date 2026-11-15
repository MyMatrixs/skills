#!/usr/bin/env python3
"""Create a safe, version-ready folder for one AI-video production."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
from pathlib import Path


STAGE_DIRECTORIES = (
    "01_brief",
    "02_script/versions",
    "03_storyboard/versions",
    "04_characters",
    "05_scenes",
    "06_shot_videos",
    "07_audio_assets",
    "08_picture_sound_edit",
    "09_master",
)


def project_slug(value: str) -> str:
    cleaned = re.sub(r"[^0-9A-Za-z\u4e00-\u9fff_-]+", "-", value.strip())
    cleaned = re.sub(r"-+", "-", cleaned).strip("-_.")
    return cleaned[:48] or "video-project"


def unique_directory(parent: Path, base_name: str) -> Path:
    candidate = parent / base_name
    index = 2
    while candidate.exists():
        candidate = parent / f"{base_name}-{index:02d}"
        index += 1
    return candidate


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, help="Parent directory for the production.")
    parser.add_argument("--name", required=True, help="Human-readable project title.")
    parser.add_argument("--aspect-ratio", default="16:9")
    parser.add_argument("--fps", type=int, default=24)
    parser.add_argument("--duration-seconds", type=int, default=None)
    args = parser.parse_args()

    if args.fps <= 0:
        parser.error("--fps must be positive")
    if args.duration_seconds is not None and args.duration_seconds <= 0:
        parser.error("--duration-seconds must be positive")

    parent = Path(args.root).expanduser().resolve()
    if not parent.exists() or not parent.is_dir():
        parser.error("--root must be an existing directory")

    now = dt.datetime.now().astimezone()
    project_id = f"{now:%Y%m%d-%H%M%S}-{project_slug(args.name)}"
    project_root = unique_directory(parent, project_id)
    project_root.mkdir()
    for relative_path in STAGE_DIRECTORIES:
        (project_root / relative_path).mkdir(parents=True, exist_ok=False)

    template_path = Path(__file__).resolve().parent.parent / "assets" / "project-template" / "project.yaml"
    duration = "null" if args.duration_seconds is None else str(args.duration_seconds)
    rendered = template_path.read_text(encoding="utf-8")
    rendered = rendered.replace("{{PROJECT_ID}}", project_root.name)
    rendered = rendered.replace("{{PROJECT_TITLE}}", args.name.replace('"', "'"))
    rendered = rendered.replace("{{CREATED_AT}}", now.isoformat(timespec="seconds"))
    rendered = rendered.replace("{{ASPECT_RATIO}}", args.aspect_ratio)
    rendered = rendered.replace("{{FPS}}", str(args.fps))
    rendered = rendered.replace("{{DURATION_SECONDS}}", duration)
    (project_root / "project.yaml").write_text(rendered, encoding="utf-8")

    status = {
        "project_id": project_root.name,
        "current_stage": "01_brief",
        "approved_versions": {"brief": None, "script": None, "storyboard": None},
        "approved_assets": {
            "characters": [],
            "scenes": [],
            "shot_videos": [],
            "audio_assets": [],
            "picture_sound_edits": [],
            "masters": [],
        },
    }
    (project_root / "production_status.json").write_text(
        json.dumps(status, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(project_root)


if __name__ == "__main__":
    main()
