#!/usr/bin/env python3
"""Audit local shot recovery and a master file without altering the production."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


def probe(path: Path) -> dict:
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=codec_type,codec_name,width,height,avg_frame_rate,sample_rate,channels", "-of", "json", str(path)], capture_output=True, text=True, check=True)
    return json.loads(result.stdout)


def local_candidates(run_dir: Path) -> list[Path]:
    """Support both classic output/ runs and raw retrieved native-A/V runs."""
    candidates = list(run_dir.glob("output/*.mp4")) + list(run_dir.glob("raw/*.mp4"))
    record = run_dir / "run.json"
    if record.exists():
        try:
            output = json.loads(record.read_text(encoding="utf-8")).get("local_output")
            if isinstance(output, str) and Path(output).is_file():
                candidates.append(Path(output))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError):
            pass
    return list(dict.fromkeys(candidates))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True, type=Path)
    parser.add_argument("--shots", required=True, type=Path)
    parser.add_argument("--master", required=True, type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    storyboard = json.loads(args.shots.read_text(encoding="utf-8"))
    shots = storyboard.get("shots", [])
    missing = []
    recovered = {}
    for shot in shots:
        output_dir = args.project / "06_shot_videos" / shot["id"] / "runs"
        candidates = []
        if output_dir.exists():
            for run in output_dir.iterdir():
                if run.is_dir():
                    candidates.extend(local_candidates(run))
        if not candidates:
            missing.append(shot["id"])
        else:
            recovered[shot["id"]] = [str(path) for path in candidates]
    master_probe = probe(args.master) if args.master.exists() else None
    has_audio = bool(master_probe and any(stream.get("codec_type") == "audio" for stream in master_probe.get("streams", [])))
    report = {"master": str(args.master), "master_exists": args.master.exists(), "master_probe": master_probe, "master_has_audio": has_audio, "recovered_local_shots": recovered, "missing_local_shots": missing, "valid": args.master.exists() and has_audio and not missing}
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.report:
        args.report.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    raise SystemExit(0 if report["valid"] else 1)


if __name__ == "__main__":
    main()
