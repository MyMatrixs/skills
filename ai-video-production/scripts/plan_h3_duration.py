#!/usr/bin/env python3
"""Calculate a MiniMax H3 source duration that covers a requested edit duration.

This planner is local-only: it neither connects to ComfyUI nor edits a workflow.
Use live node-schema values whenever they differ from the inspected defaults.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


def aligned_frames(requested_seconds: float, fps: float, minimum: int, step: int, offset: int) -> int:
    if requested_seconds <= 0:
        raise ValueError("requested duration must be positive")
    if fps <= 0 or minimum < 1 or step < 1 or not 0 <= offset < step:
        raise ValueError("invalid frame-grid parameters")
    candidate = max(minimum, math.ceil(requested_seconds * fps))
    return candidate + ((offset - candidate) % step)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--duration-seconds", required=True, type=float, help="approved storyboard/EDL duration")
    parser.add_argument("--fps", type=float, default=24.0)
    parser.add_argument("--minimum-frames", type=int, default=5, help="live H3 schema length minimum")
    parser.add_argument("--frame-step", type=int, default=17, help="live H3 schema length step")
    parser.add_argument("--grid-offset", type=int, default=5, help="H3 alignment remainder, normally 5 for 17k+5")
    parser.add_argument("--trained-min-frames", type=int, default=124)
    parser.add_argument("--trained-max-frames", type=int, default=362)
    parser.add_argument("--output", type=Path, help="write JSON to this path instead of stdout")
    args = parser.parse_args()

    frames = aligned_frames(args.duration_seconds, args.fps, args.minimum_frames, args.frame_step, args.grid_offset)
    source_seconds = frames / args.fps
    experimental = frames < args.trained_min_frames or frames > args.trained_max_frames
    plan = {
        "planner": "plan_h3_duration.py",
        "requested_duration_seconds": args.duration_seconds,
        "fps": args.fps,
        "generation_frames": frames,
        "generation_duration_seconds": round(source_seconds, 6),
        "retained_start_seconds": 0.0,
        "retained_end_seconds": args.duration_seconds,
        "h3_length_schema": {
            "min": args.minimum_frames,
            "step": args.frame_step,
            "grid_offset": args.grid_offset,
        },
        "training_range_frames": [args.trained_min_frames, args.trained_max_frames],
        "status": "requires_short_duration_pilot" if experimental and frames < args.trained_min_frames else (
            "requires_long_duration_pilot" if experimental else "within_declared_training_range"
        ),
        "assembly_requirement": "Trim picture and native generated audio together to the retained window; never cut dialogue mid-utterance.",
    }
    rendered = json.dumps(plan, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
        print(args.output)
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
