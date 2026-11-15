# Production chain and remote-session handoff

Use this reference when an AI-video project proceeds beyond planning into remote generation, audio, or final delivery. The purpose is to keep every creative decision reproducible while making billed GPU sessions short, intentional, and productive.

## End-to-end chain

1. **Project and creative brief**
   - Input: premise, one or more genres, intended duration, audience, format, visual direction, and constraints.
   - Output: initialized project, approved brief, success criteria, and a production plan.

2. **Script**
   - Input: approved brief and research or source material when applicable.
   - Output: scene-based script with premise, dramatic progression, character motivations, dialogue/action, timing estimate, and an explicit ending. Do not move forward with only a theme or outline.

3. **Storyboard / shot script**
   - Input: approved script.
   - Output: a reviewable shot table. Each shot records its scene and time, framing, viewpoint/camera movement, visual content, character action and dialogue, essential inner state, transition, target duration, and referenced character/scene assets. It must both faithfully cover the script and deliberately control audience attention and pacing.

4. **Character visual design**
   - Input: character requirements from the script and storyboard.
   - Output: three labeled candidate concepts per character for review, then an approved multi-view character sheet (front, side, back) with gender presentation, apparent age, facial features, build, hair, wardrobe, palette, and distinguishing details. Preserve the selected source and prompts for shot continuity.

5. **Scene plate design**
   - Input: approved story, shot requirements, and approved character sheets.
   - Output: approved empty scene plates with mood, time, lighting, composition, prop continuity, and deliberate clear space for each character/action. Do not bake a character into a reusable plate unless the shot specifically requires it.

6. **Shot packet and route decision**
   - Input: one approved storyboard row plus its character/scene references.
   - Output: one shot packet containing the shot ID, approved input images, first/end frame or motion reference when needed, positive and negative video prompt, dialogue/timing, camera constraint, target resolution/fps/duration, acceptance tests, and output directory. Select and record exactly one initial picture-sound route:
     - **Native audio-video:** for this user's character dialogue and intended monologue, this is the required first route. Include exact Mandarin text, speaker, delivery, visible-mouth requirement, and minimal-ambience direction in the prompt and packet.
     - **Controlled picture plus separate sound:** use for non-speaking shots or independently authored ambience, effects, music, and mastering. Do not use it to silently replace required character dialogue.
     - **Hybrid:** retain selected native MiniMax dialogue and augment it with controlled background sound during the mix; never replace that dialogue without explicit user authorization.

7. **Shot generation and review**
   - Input: approved shot packet and a validated workflow.
   - Output: raw candidate video(s), workflow/API JSON, model and node selectors, seed where available, prompts, source filenames, actual output filename, and a review against the storyboard. Start with a small pilot when the workflow or assets are unverified; promote only approved candidates.

8. **Audio creation and audiovisual assembly**
   - Input: approved visual candidate and its selected route.
   - Output: retained native dialogue/monologue candidates, sound-effect/ambience/music layers as required, a timed mix, and an audiovisual candidate. Document whether native sound was retained, augmented, or omitted; replacement of required spoken performance needs explicit user authorization. Verify duration, exact spoken text, lip/dialogue timing, audio presence on the selected source MP4, sync, loudness intent, and edit points.

9. **Master assembly and export**
   - Input: approved audiovisual shots and transitions.
   - Output: versioned master timeline, final render, delivery encode, export settings, and technical/media validation. Retain source shots and manifests; a final MP4 never replaces its production evidence.

Do not pass a provisional asset across an approval gate as though it were final. If an upstream decision changes, retain the prior version and regenerate only affected downstream work.

## When remote GPU work starts

Stages 1–6 should normally be completed locally while the server is off. Opening the remote instance is justified only when the user has asked to test its capabilities or to generate actual visual/audio assets and at least one runnable shot packet is ready.

Before power-on, prepare the local input files, final workflow selection, unique remote input/output names, prompts, queue order, local destination paths, and review criteria. This makes the session useful as soon as ComfyUI is ready rather than consuming billed time in preparation.

## Remote execution sequence

1. Read [AutoDL.Art instance lifecycle](autodl-art-instance-lifecycle.md), then check the platform state.
2. If it is shut down and remote work is now authorized, start it and wait for `running`:

   ```powershell
   python scripts/autodl_art_instance.py status
   python scripts/autodl_art_instance.py power-on --wait
   ```

3. Treat `running` only as platform readiness. Confirm SSH/ComfyUI health, free disk, GPU visibility, no inherited queue, and the live model/node selectors before submitting work.
4. Run a small pilot for a new workflow or new input set. For a dialogue batch, use a representative Mandarin line and inspect the retrieved MP4 audio stream before queueing more shots. Review direction, motion, identity consistency, camera, duration, exact spoken text, lip sync, audio behavior, and encoder result against the shot packet.
5. Once the pilot is accepted, submit the approved queue in a controlled sequence. Use the available GPU deliberately, but do not run incompatible heavy workflows concurrently simply to maximize utilization.
6. During generation, monitor GPU utilization/VRAM/temperature/power, disk capacity, ComfyUI queue/history, error logs, and the actual output files. For native dialogue, retrieve all returned artifacts (including companion audio-bearing outputs), inspect their streams, and stop to correct the first missing-audio or recovery failure before spending the rest of the queue.
7. Copy each accepted result and all reproducibility metadata to its local project run directory. Confirm the local media file opens and passes validation before removing remote-only copies or ending the session.
8. Complete the selected audio route and master assembly. If remote compute is still needed for an approved next batch, keep the session active; otherwise inspect that no execution, queue, upload, or download remains.
9. Close the session promptly:

   ```powershell
   python scripts/autodl_art_instance.py power-off
   python scripts/autodl_art_instance.py status
   ```

   Successful completion means the final status is `shutdown`. Do not send `power-off` while a ComfyUI job, queued job, upload/download, or required output verification remains.

## Proven lifecycle boundary

The known configured AutoDL.Art instance has been verified through the platform sequence `shutdown → running → shutdown` using the helper. This proves the platform power API and local configuration path; it does not prove that ComfyUI, a particular model, or a selected workflow is healthy on a future run. Re-check those conditions live each time.
