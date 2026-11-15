# Native-A/V batch resilience

Read this before a billed native audio-video batch, especially MiniMax H3 Ref2VA.

## Packet and duration contract

Every selected shot packet must identify the approved first keyframe or an explicit text-only choice, the approved visual prompt, native-audio direction, FPS, model generation frame count, retained edit duration, and route. For this user's dialogue or monologue shots, it must also include every exact Mandarin turn in order, each speaker's visible anchor, language, delivery, mouth/lip-sync requirement, `voice_source: minimax_native`, and a minimal-ambience instruction for later sound design. A model's generated source duration is not permission to change the storyboard: record the requested duration and the retained window as a duration contract. Read [custom-duration-planning.md](custom-duration-planning.md) when the H3 source duration differs from the requested duration.

For MiniMax H3, verify the live node's dimensions, length increments, reference-media slots, and model selectors. The inspected ComfyUI node accepts a `length` minimum of 5 frames with a 17-frame step, internally aligns output to `17k+5` frames at 24 fps, and labels its trained range as roughly 124–362 frames. The 124-frame (about 5.17-second) profile is the shortest validated profile, not a node-enforced minimum. A source shorter than 124 frames or longer than 362 frames is experimental and needs a one-shot pilot before any batch; use `scripts/plan_h3_duration.py` to calculate and save the source plan. Any higher pixel count, duration, or changed model variant requires a new pilot on the active GPU.

Reference uploads must use a unique remote filename. Record the exact relative path returned or required by the live media-loader node; some upload endpoints return only a basename although the H3 reference node requires its input subdirectory as part of the path. Submit one representative image-reference dialogue pilot, including multiple speakers when that is the intended production pattern, and confirm the reference is actually read, the selected local output has an audio stream, all required turns fit, and the speaker assignment is reviewable before queuing similar shots.

## Ledger and recovery

Initialize `08_picture_sound_edit/batch_ledger.json` before submitting a batch. Each row carries one of these states:

`planned → submitted → remote_completed → retrieval_pending → retrieved → verified`

`failed` may be entered from a nonterminal state, with a reason. Keep the original prompt ID and remote filename when retrying; a new generation is a linked retry, never a replacement for the original attempt.

Update the ledger before starting another remote job when a job has completed or failed. Record every output returned for the job, not only the first MP4: companion native-audio files need their own remote filename, local path, checksum, and stream inspection. A local background process may improve throughput, but its stdout is not sufficient recovery evidence. For native-dialogue batches, stop adding jobs after the first candidate that lacks its expected audio stream or fails output recovery; diagnose/recover it before incurring another batch of billed runs. Before power-off, every retained row must be `verified`, including the local checksum and a recorded audio stream on the exact candidate selected for the master. If the server was manually shut down, treat it as a normal lifecycle terminal state: inspect the ledger and local media first, and do not issue another shutdown call merely to satisfy a checklist.

### Overlapping the serial handoff with local review

When the next approved packet is independent of the previous generated result, avoid leaving the GPU idle for local download and review. At remote completion of shot *n*:

1. save its prompt ID, output name, and `remote_completed` / `retrieval_pending` ledger state;
2. submit the already approved shot *n + 1* immediately, after confirming the ComfyUI queue is otherwise empty;
3. while *n + 1* runs, retrieve and checksum *n*, inspect streams and the contact sheet, and write the acceptance or failure result to the ledger;
4. when *n + 1* completes, repeat the handoff to *n + 2* before reviewing *n + 1*.

Use this only when later packets use their own approved first keyframes and do not inherit timing, picture, props, or continuity from the unreviewed take. Maintain a one-job remote queue; this is generation/review overlap, not parallel model inference. If a review rejects *n*, keep it `failed` or `decision_pending`, repeat input QC for any paid revision, and continue only unrelated approved shots. Do not enqueue a revision ahead of an already-running shot or treat a speculative take as a continuity source.

## Native-dialogue and post-ambience masters

For this user's spoken-performance projects, create a native-dialogue review master and, when needed, a post-ambience master:

- **native-dialogue master**: the retained H3 picture plus its sampled dialogue performance, useful for evaluating wording, speaker, and audiovisual rhythm;
- **post-ambience master**: the identical visual EDL and retained native dialogue, plus approved ambience, effects, music, and mastering. It is not a replacement-voice master.

Both masters must have the exact approved EDL duration, video and audio streams, a contact sheet, and a delivery audit. For the native-dialogue master, record codec, sample rate, channel count, basic loudness measurement, and source filename for every retained spoken shot. Human listening remains required before accepting generated speech or relying on its ambience continuity.

For a preview, measure each spoken source's peak or loudness before concatenation. Large shot-to-shot level differences can be corrected with bounded, documented per-shot gain while keeping the native words and raw tracks unchanged. Record the gain and master version; check that boosting a quiet take does not merely amplify noise or clipping. If a line itself is weak or incoherent, treat that as a generation failure and make a versioned retry. Compare any internal-voice take with visible-mouth motion: an unintended moving mouth is a performance mismatch even if the container has audio.

An EDL may deliberately add approved time cards or a result card. In that case record storyboard duration, added/removed edit seconds, and expected versus actual master duration rather than calling the extension an unnoticed mismatch. Keep a clean preview plus a numbered review copy and matching index when the user needs to cite problem segments.
