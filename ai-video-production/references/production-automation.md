# Production automation gates

Use these helpers for multi-shot productions. They create or validate evidence; they do not approve creative work or start remote compute.

## Before remote generation

After `shots.json` is approved, prepare shot packets and an EDL:

```text
python scripts/prepare_shot_batch.py --project <project-root> --shots <approved-shots.json>
```

The resulting `08_picture_sound_edit/edl.json` is the duration authority for the master. A generated segment may be longer than the retained edit window; do not silently change the storyboard duration to match it.

For a custom MiniMax H3 source duration, calculate the aligned source frame count before editing the API workflow. Save the output beside the shot input as `duration_contract.json` and copy its `generation_frames` value to the H3 node's `length` input:

```text
python scripts/plan_h3_duration.py --duration-seconds 3 --output <project-root>/06_shot_videos/S01-001/input/duration_contract.json
python scripts/apply_h3_duration_contract.py --workflow <input-api.json> --contract <duration-contract.json> --output <duration-specific-api.json>
```

This creates an approximately 3.04-second H3 source (73 frames at 24 fps) while retaining the storyboard's exact 3-second EDL duration. It does not submit a job or alter a workflow. Read [custom-duration-planning.md](custom-duration-planning.md) before using a source outside H3's trained duration range.

For a legacy project whose prompts/keyframes were saved only in its old API graphs, preserve that evidence in the new packet before generating:

```text
python scripts/prepare_shot_batch.py --project <project-root> --shots <approved-shots.json> --hydrate-legacy
```

## Before a billed remote batch

Initialize a durable ledger. Update it at each remote submission, completion, retrieval, verification, or failure; do not rely on a terminal log for recovery.

```text
python scripts/batch_ledger.py init --shots <approved-shots.json> --ledger <project-root>/08_picture_sound_edit/batch_ledger.json
python scripts/batch_ledger.py update --ledger <ledger.json> --shot-id S01-001 --status submitted --prompt-id <remote-prompt-id>
python scripts/batch_ledger.py update --ledger <ledger.json> --shot-id S01-001 --status verified --local-output <local.mp4> --sha256 <sha256>
python scripts/batch_ledger.py summary --ledger <ledger.json>
```

If a session ends unexpectedly, recover `remote_completed` or `retrieval_pending` rows before submitting retries. A verified row requires both its local path and checksum.

## Before the first API submission

Capture the live server schema, then validate the API prompt:

```text
curl http://127.0.0.1:6006/object_info > object_info.json
python scripts/validate_comfy_api_workflow.py --workflow api_prompt.json --object-info object_info.json
```

This validates an API graph only. Review any UI-to-API conversion separately, especially where a UI graph stores fallback values for linked widgets.

## Before master delivery

```text
python scripts/audit_video_delivery.py --project <project-root> --shots <approved-shots.json> --master <master.mp4>
```

The audit checks classic `output/` candidates plus retrieved `raw/` candidates named by a run record, that the master has video and audio, and that its duration and FPS match the delivery target when declared. Review the generated JSON report and the master contact sheet before calling the delivery final.
