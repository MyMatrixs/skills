# Custom MiniMax H3 duration planning

Use this reference when the user specifies a source or final shot duration that does not match MiniMax H3's previously used 124-frame profile.

## Separate the two durations

Every duration-controlled H3 shot has two explicit values:

- `requested_duration_seconds`: the approved storyboard/EDL duration; this is the final editorial authority.
- `generation_frames` and `generation_duration_seconds`: the H3 source requested from the model after its live frame-grid alignment.

Do not overwrite the requested duration with the source duration. If a generated source is longer, retain the declared window from picture and its native audio together. If it is shorter, do not silently hold frames, stretch audio, or change the EDL: split the shot, generate a longer source, or obtain explicit approval for a named edit treatment.

## H3 grid and safety gate

Before a run, query the live `MiniMaxH3ReferenceToVideo` schema. On the inspected ComfyUI 0.37 server it declared 24 fps, `length.min = 5`, `length.step = 17`; implementation aligns frames upward to the `17k+5` grid. The node labels approximately 124–362 frames as its trained range.

For a requested duration `d`, calculate the smallest valid source frame count that covers it:

```text
n = max(live_minimum_frames, ceil(d × fps))
generation_frames = smallest m >= n where m mod live_step = grid_offset
generation_duration_seconds = generation_frames / fps
```

For the inspected H3 node, `grid_offset = 5` and `live_step = 17`. At 24 fps, a 3-second request becomes 73 frames (3.042 seconds); a 4-second request becomes 107 frames (4.458 seconds); a 5-second request becomes 124 frames (5.167 seconds).

`generation_frames < 124` or `> 362` is an **experimental duration**. Create one representative candidate only, using the same resolution, reference input, exact dialogue, and output encoder as the planned shot. Require a real audio stream, complete spoken line inside the retained window, intelligibility, lip sync, and visual continuity before allowing another short-duration H3 job. Do not batch experimental lengths after merely validating the workflow schema.

## Duration contract artifact

Run `scripts/plan_h3_duration.py` and save its JSON output as `06_shot_videos/<SHOT_ID>/input/duration_contract.json`. Add its path and the same fields to the input manifest:

```json
{
  "duration_contract": {
    "requested_duration_seconds": 3.0,
    "fps": 24,
    "generation_frames": 73,
    "generation_duration_seconds": 3.041667,
    "retained_start_seconds": 0.0,
    "retained_end_seconds": 3.0,
    "h3_length_schema": {"min": 5, "step": 17, "grid_offset": 5},
    "training_range_frames": [124, 362],
    "status": "requires_short_duration_pilot"
  }
}
```

For a native-dialogue shot, ensure every approved turn finishes before `retained_end_seconds`; the retained window must never cut a word, breath needed for intelligibility, or visible mouth movement. Trim video and native generated audio together during assembly. A request for a custom duration never authorizes separate TTS, audio time-stretching, or a voice replacement.

To apply an approved contract to an API-form workflow without overwriting the original, run:

```text
python scripts/apply_h3_duration_contract.py --workflow <input-api.json> --contract <duration-contract.json> --output <duration-specific-api.json>
```

The helper only changes the `length` input of exactly one `MiniMaxH3ReferenceToVideo` node. It refuses an ambiguous graph; pass `--node-id` only after inspecting the graph. Validate the resulting workflow against a fresh live `object_info` capture before any remote submission.

## Other routes

LTX 2.5 exposes shorter frame ranges in the observed environment and can be considered for non-speaking inserts after a pilot. It is not an automatic substitute for the user's MiniMax-native character dialogue policy: use it for dialogue only if the user explicitly changes that policy and a candidate passes subtitle, wording, and lip-sync review.
