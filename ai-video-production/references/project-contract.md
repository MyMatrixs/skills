# Project Contract

## Project root and lifecycle

One production owns one unique project root. Create it with `scripts/init_video_project.py`; never merge two productions or overwrite an existing project to reuse a name. The root contains `project.yaml` for delivery choices and `production_status.json` for the current approved state.

```text
project/
  project.yaml
  production_status.json
  01_brief/
  02_script/versions/
  03_storyboard/versions/
  04_characters/
  05_scenes/
  06_shot_videos/
  07_audio_assets/
  08_picture_sound_edit/
  09_master/
```

`06_shot_videos/` follows the conventions in `shot-video-production.md`. `07_audio_assets/` holds independently created dialogue, ambience, effects, music, and their manifests. `08_picture_sound_edit/` holds per-shot or per-scene route manifests, edit decision lists, intermediate mixes, and audiovisual reviews. `09_master/` holds versioned full-film timelines and delivery exports.

Existing projects that already contain `07_voice/` and `08_audio_mix/` remain valid. Do not rename them automatically. For those projects, treat `07_voice/` as the dialogue subset of `07_audio_assets/` and `08_audio_mix/` as the equivalent of `08_picture_sound_edit/`; record that legacy mapping once in the project's production notes before adding new material.

## Stable identifiers and versions

- Script scenes: `SCN001`, `SCN002`.
- Storyboard shots: `S01-001`, `S01-002`; the prefix identifies the script scene.
- Characters: `C001`, `C002`.
- Scene assets: `LOC001`, `LOC002`; a changed time-of-day or weather state receives a new ID.
- Shot video runs: `S01-001/r001`, `S01-001/r002`; a run never replaces another run.
- Versioned documents live under `versions/v001`, `versions/v002`, and so on. Never overwrite an approved version.

Each stage keeps a manifest at its stage root naming the approved version or asset IDs. Downstream artifacts cite those IDs and paths explicitly.

Picture-sound manifests name the chosen route (`native_audio_video`, `separate_sound`, or `hybrid`), every retained and replaced track, the synchronization/edit decision, and the candidate's review status. The master manifest cites approved audiovisual shot results rather than assuming that a visual shot's embedded audio is final.

## Provenance and approval

Store source links/files, user-provided references, prompt text, model/tool configuration, seed when available, generated raw files, and review results with the asset they produced. Keep source and derived files distinct.

Before a later stage uses an artifact, confirm its relevant approval gate. If the user chooses a candidate or approves a version, update both the stage manifest and `production_status.json`.
