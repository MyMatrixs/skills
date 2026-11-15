#!/usr/bin/env python3
"""Create non-destructive shot packet manifests and an exact EDL from an approved storyboard."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_json(path: Path) -> object:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def legacy_evidence(input_dir: Path) -> dict:
    """Extract only existing evidence from an older API packet; never invent it."""
    keyframes = sorted(input_dir.glob("*keyframe*.*"))
    api_path = input_dir / "api_prompt.json"
    prompt = None
    if api_path.exists():
        try:
            graph = load_json(api_path)
            nodes = graph.get("prompt", graph) if isinstance(graph, dict) else {}
            if isinstance(nodes, dict):
                for node in nodes.values():
                    if not isinstance(node, dict):
                        continue
                    inputs = node.get("inputs", {})
                    if node.get("class_type") == "WanVideoTextEncode" and isinstance(inputs.get("positive_prompt"), str):
                        prompt = inputs["positive_prompt"]
                        break
                if prompt is None:
                    for node in nodes.values():
                        inputs = node.get("inputs", {}) if isinstance(node, dict) else {}
                        text = inputs.get("text")
                        if isinstance(text, str) and len(text.strip()) >= 40:
                            prompt = text
                            break
        except (OSError, UnicodeDecodeError, json.JSONDecodeError):
            pass
    return {
        "first_keyframe": str(keyframes[0]) if keyframes else None,
        "approved_positive_prompt": prompt,
        "source_api_graph": str(api_path) if api_path.exists() else None,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True, type=Path)
    parser.add_argument("--shots", required=True, type=Path)
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--hydrate-legacy", action="store_true", help="add evidence from older API packets without replacing existing fields")
    args = parser.parse_args()

    project = args.project.resolve()
    storyboard = load_json(args.shots.resolve())
    if not isinstance(storyboard, dict) or not isinstance(storyboard.get("shots"), list):
        parser.error("--shots must be a JSON object containing a shots array")
    project_config = project / "project.yaml"
    if not project_config.exists():
        parser.error("--project must contain project.yaml")

    # The template keeps fps visible and dependency-free; reject ambiguity instead of guessing.
    fps_line = next((line for line in project_config.read_text(encoding="utf-8").splitlines() if line.strip().startswith("fps:")), None)
    if fps_line is None:
        parser.error("project.yaml is missing delivery.fps")
    fps = int(fps_line.split(":", 1)[1].strip())
    edl = {"fps": fps, "shots": [], "total_duration_seconds": 0}

    for index, shot in enumerate(storyboard["shots"], start=1):
        if not isinstance(shot, dict) or not isinstance(shot.get("id"), str):
            parser.error(f"shot {index} is missing a string id")
        duration = shot.get("duration_seconds")
        if not isinstance(duration, (int, float)) or duration <= 0:
            parser.error(f"shot {shot['id']} has an invalid duration_seconds")
        shot_id = shot["id"]
        frames = int(round(duration * fps)) + 1
        packet = {
            "shot_id": shot_id,
            "storyboard_source": str(args.shots.resolve()),
            "target_duration_seconds": duration,
            "target_fps": fps,
            "model_frame_count": frames,
            "route": "controlled_post",
            "visual_status": "planned",
            "audio_status": "planned",
            "remote": {"prompt_id": None, "output_filename": None, "retrieved": False, "sha256": None},
        }
        packet_path = project / "06_shot_videos" / shot_id / "input" / "input_manifest.json"
        packet_path.parent.mkdir(parents=True, exist_ok=True)
        if packet_path.exists() and args.hydrate_legacy:
            existing = load_json(packet_path)
            if not isinstance(existing, dict):
                parser.error(f"{packet_path} must contain a JSON object")
            evidence = legacy_evidence(packet_path.parent)
            existing.setdefault("legacy_evidence", {})
            if isinstance(existing["legacy_evidence"], dict):
                for key, value in evidence.items():
                    if value is not None:
                        existing["legacy_evidence"].setdefault(key, value)
            existing.setdefault("target_duration_seconds", duration)
            existing.setdefault("target_fps", fps)
            existing.setdefault("model_frame_count", frames)
            packet_path.write_text(json.dumps(existing, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        elif packet_path.exists() and not args.overwrite:
            raise SystemExit(f"Refusing to overwrite {packet_path}; pass --overwrite to replace it")
        else:
            if args.hydrate_legacy:
                packet["legacy_evidence"] = legacy_evidence(packet_path.parent)
            packet_path.write_text(json.dumps(packet, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        edl["shots"].append({"index": index, "shot_id": shot_id, "duration_seconds": duration, "frames": int(round(duration * fps))})
        edl["total_duration_seconds"] += duration

    edl_path = project / "08_picture_sound_edit" / "edl.json"
    edl_path.parent.mkdir(parents=True, exist_ok=True)
    if edl_path.exists() and args.hydrate_legacy:
        return
    if edl_path.exists() and not args.overwrite:
        raise SystemExit(f"Refusing to overwrite {edl_path}; pass --overwrite to replace it")
    edl_path.write_text(json.dumps(edl, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(edl_path)


if __name__ == "__main__":
    main()
