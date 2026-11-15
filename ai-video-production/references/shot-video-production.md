# Shot-video generation

## Gate, scope, and shot plan

Generate only after the storyboard row and cited character/scene assets are approved, unless the user has explicitly named provisional assets for the run. A scene plate alone is not a character shot: create a shot-specific first keyframe that places the selected character in the storyboard blocking zone.

## Delegated generation-input quality gate

Before creating or changing the generation input for each storyboard shot or sub-shot, perform the structured check in [delegated-shot-input-qc.md](delegated-shot-input-qc.md). An independent child agent can draft or check the input when the user or task explicitly calls for one; provide only the approved storyboard row, cited character/scene assets, adjacent-shot continuity facts, and route/model constraints. The reviewer checks cast count, physical plausibility, dialogue clarity, and prompt distraction. The reviewer does not submit jobs, edit remote workflows, generate assets, or approve the shot.

The producing agent checks that facts cite the approved packet rather than invented visual details, resolves any `revise` outcome, and records the result in `06_shot_videos/<SHOT_ID>/input/`. A paid submission needs QC status `ready`; an explicitly bounded, user-directed capability test may use `ready_for_isolated_pilot` and must remain a candidate until reviewed. The structured check remains required whether or not another agent participates.

First determine whether the requested result is a **complete storyboard shot**, a **sub-shot**, or a **motion proxy**. For a continuous location, cast and action, prepare the complete shot as the first generation plan. An older short-run result does not establish a hard duration limit: check the live node's length range and resources, calculate the source/retained duration contract, and run one representative pilot when the duration or speaker count is unproven. If the live model cannot support the length or the pilot fails review, plan contiguous sub-shots with entry/exit states and edit points. Never label a short proxy as the full shot.

## Intended long takes

A 20- to 40-second storyboard shot may be an intended continuous long take. Test one complete generation when live model capabilities and a bounded pilot make that credible. If segmentation is necessary, retain one **master camera plan** across the generation segments rather than independently reframing each part.

For a segmented long take, record a plan that names:

- master duration, framing, lens/viewpoint, lighting, and the camera state at the beginning and end;
- one camera rule for the entire take: locked camera, or one purposeful continuous move with its start/end times and direction;
- each retained segment's target duration, visual action, entry/exit state, reference frame or video range, and a stable edit window;
- the intended sound route and whether a continuous post-produced sound bed is required.

Do not restart a push, pull, pan, or other camera motion in every short segment. For a locked master camera, every segment must request a locked camera. For a single continuous move, only the scheduled portion may move; later segments inherit the arrival state rather than beginning another move. Place joins during low visual change, such as a held pose, completed turn, blink, foreground occlusion, or terminal pulse. Generate overlap only to select a stable bridge; document the retained in/out range and any crossfade in the edit decision list.

For dialogue-heavy shots in this user's productions, first assess one MiniMax native audio-video take with the approved turns in order. Identify each speaker by visible position, age/appearance and clothing, keep the other mouths closed during that turn, and check that the total speech fits the retained duration. A failed or unsupported take may be divided at natural pauses or location changes; each resulting inference still uses native MiniMax speech. Since each inference can reset voice, room tone and camera behavior, review every join and add only continuity ambience in post.

Before remote execution, record the reachable ComfyUI URL, version, GPU/free VRAM, relevant nodes, exact selectable model names, and output encoder choices. Treat example workflows as starting points only. Do not enqueue a job merely to inspect an installation.

For a rented remote GPU, monitor every active batch rather than treating successful submission as completion. At a useful cadence, record GPU utilization, temperature, power, VRAM, host disk free space, the ComfyUI process, and queue state. If the service exits, disk headroom becomes unsafe, or a job reports an error/OOM, stop adding work, preserve completed outputs and diagnostics, and report the specific condition. Use the GPU continuously when the user requests it, but do not run competing single-GPU model jobs in parallel merely to inflate utilization; an orderly queue avoids OOM and corrupted output.

## Required per-shot input package

Create `06_shot_videos/<SHOT_ID>/input/` before inference. Preserve the actual asset files or stable relative links and an `input_manifest.json` (or a versioned sibling) that records:

- storyboard shot ID, script scene, any planned sub-shot range, and whether it is proxy/sub-shot/complete;
- selected character IDs, scene ID, and approved or explicitly authorized provisional asset paths;
- first keyframe, optional end keyframe, visual references, aspect ratio, output resolution, frames, FPS, and intended duration;
- camera size, viewpoint, movement, blocking, lighting, continuity anchors, required props/UI, forbidden elements, and expected entry/exit state;
- dialogue, exact speaker/language/delivery, audio timing, and lip-sync requirement; for required character dialogue or monologue, mark `voice_source: minimax_native` rather than `deferred`;
- workflow family and why it provides enough control.
- `input_qc.json`: source citations, generation-input draft, cast/on-screen count, per-turn dialogue check, clutter check, risks, and `ready`, `ready_for_isolated_pilot`, or `revise` status. Preserve it alongside the actual submitted prompt; if the draft changes, record the resolved version rather than overwriting the review.

Use an end keyframe or pose/motion reference whenever the direction or final composition matters. The start and end frames must preserve camera, lighting, cast, wardrobe, and fixed scenery; change only the planned motion or story state. A text instruction such as “move forward” is not reliable directional control by itself. If a model visibly ignores a large end-frame change or returns to the starting composition near the tail, treat the result as a revision, not as a compliant transition; split at a stable visual beat, revise the keyframes, or use a shorter retained portion with an intentional edit.

## Select the workflow family

Choose the smallest workflow that provides the required control:

- **I2V draft:** one approved first keyframe plus restrained motion. Use for low-risk environmental movement or exploratory timing.
- **Dual-model I2V:** high/low-noise pair for higher-fidelity short candidates. It is a strong default when the active server exposes a verified pair.
- **Start/end-frame I2V or FLF2V:** use when the ending image, movement direction, reveal, or transition is essential. Confirm that the active workflow accepts an end frame; do not infer that any I2V model supports it.
- **Pose/reference-controlled animation:** use for exact named-character action, especially visible hands, contact points, or body direction. Supply identity and pose/motion references rather than hoping an empty plate preserves the character.
- **Post-process:** interpolate, upscale, denoise, or combine only after a motion candidate passes review. It cannot correct wrong blocking, reversed motion, unreadable UI, or identity drift.

Use a low-cost validation for a newly adapted workflow. If the validation fails because of a missing node, model, or encoder, correct that explicit mismatch once and retry once. Do not download models, alter server configuration, or keep retrying without user direction.

## Run record and review

Each submission lives in `06_shot_videos/<SHOT_ID>/runs/r00N/`:

```text
r00N/
  api_prompt.json         # executable API graph, never only a UI graph
  run.json                # server, selectors, seed, timing, queue/job IDs, status
  raw/                    # untouched retrieved video/frames/logs
  contact_sheet.jpg       # chronological visual review aid
  review.md               # compliance check against the storyboard
  approved/               # populated only after user approval
```

Save the API workflow before submission. Copy the actual output and metadata from the server into `raw/`. Record model/LoRA/VAE/text-encoder selectors, seed, sampler, steps, CFG, scheduler, frame count, FPS, resolution, codec, and memory/offload controls.

Review the candidate against the storyboard row, not only against the prompt:

- duration and whether it is honestly labelled proxy, sub-shot, or complete;
- shot size, viewpoint, camera move, entry/exit states, and transitions;
- character identity, scene/prop/UI presence, intended action direction, and physical contact;
- stable anatomy/architecture, lighting, palette, no unwanted people, no unintended captions/watermark; natural writing belongs on the correct visible prop surface;
- audio/dialogue/ambience status, explicitly marked pending if not produced.

Create a chronological contact sheet before accepting a candidate. It is mandatory for checking reversed motion, frozen vehicles/hands, tail-end snapback, and whether a controlled end frame was actually reached. When assembling a complete long storyboard shot from sub-shots, preserve a sub-shot edit decision list that names the retained in/out ranges and crossfades; render the final duration exactly and re-review the joined master for visible discontinuities.

Record `pass`, `revise`, or `reject` in `review.md`. A locally reviewed `pass` remains a candidate until user approval; only then copy it to `approved/` and add it to the project status.
