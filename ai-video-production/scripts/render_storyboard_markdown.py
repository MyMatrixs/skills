"""Render a human-reviewable Markdown storyboard from the canonical shots.json."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


FIELDS = (
    ("时长", "duration_seconds"),
    ("时间线", None),
    ("剧本场景", "script_scene_id"),
    ("地点／时间", None),
    ("人物", "character_ids"),
    ("叙事目的", "narrative_purpose"),
    ("景别／机位", None),
    ("构图", "composition"),
    ("画面与表演", None),
    ("台词", "dialogue"),
    ("声音", "sound_ambience"),
    ("转场", None),
    ("连续性", "continuity_note"),
    ("首帧", "first_frame"),
    ("末帧", "last_frame"),
    ("动作", "motion_description"),
    ("光线／风格", "light_color_style"),
    ("状态", None),
)


def value(shot: dict, label: str, key: str | None) -> str:
    if key is not None:
        item = shot.get(key, "")
        return "、".join(item) if isinstance(item, list) else str(item)
    derived = {
        "时间线": f"{shot.get('start_seconds', '')}s – {shot.get('end_seconds', '')}s",
        "地点／时间": f"{shot.get('location_id', '')}／{shot.get('time', '')}",
        "景别／机位": "；".join(
            part for part in (shot.get("shot_size", ""), shot.get("viewpoint", ""), shot.get("camera_movement", "")) if part
        ),
        "画面与表演": "；".join(
            part for part in (shot.get("image_description", ""), shot.get("performance", ""), shot.get("viewer_information", "")) if part
        ),
        "转场": f"入：{shot.get('entry_transition', '')}；出：{shot.get('exit_transition', '')}",
        "状态": f"生成：{shot.get('generation_status', '')}；审批：{shot.get('approval_status', '')}",
    }
    return derived[label]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--shots", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    document = json.loads(args.shots.read_text(encoding="utf-8"))
    lines = [
        "# 分镜", "", f"- 版本：{document.get('version', '')}",
        f"- 状态：{document.get('status', '')}", f"- 帧率：{document.get('fps', '')} fps",
        f"- 总时长：{document.get('total_duration_seconds', '')} 秒", "",
    ]
    for index, shot in enumerate(document.get("shots", []), start=1):
        lines.extend((f"## {index:02d}｜{shot.get('id', '')}", ""))
        for label, key in FIELDS:
            lines.append(f"- **{label}：** {value(shot, label, key)}")
        lines.append("")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
