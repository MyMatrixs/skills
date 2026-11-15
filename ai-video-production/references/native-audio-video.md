# Native audio-video generation

Use this reference only when choosing a workflow that generates video and sound together in one inference. This differs from (a) audio-driven video, where a prepared track drives lip motion or action, and (b) ordinary muxing, where an existing audio track is attached to video.

## User default for spoken performance

For this user's productions, MiniMax native audio-video is the first route for character dialogue and intended monologue. It is used because the image and speech are sampled together, not because it guarantees a particular line or voice. The candidate must contain the intended spoken performance and pass review before it enters a master.

Post-production may add ambience, effects, music, and mastering. It must not replace required MiniMax dialogue with TTS, a new recorded voice, or manually timed speech unless the user explicitly authorizes that change. Since native outputs are normally mixed rather than stem-separated, request dry dialogue or minimal room tone where later ambience is planned.

## Other cases where it earns its cost

Choose native audio-video for a short, self-contained candidate when the value is the immediate relationship between image and sound:

- an atmosphere, product, music, comedy, horror, or transition test in which ambience and visible action should emerge together;
- a proof-of-concept or pitch clip that needs to be watchable with sound before detailed post-production;
- a small number of low-revision inserts where approximate dialogue, sound effects, or environmental sound are acceptable;
- a deliberately experimental shot whose result is reviewed as a candidate rather than assumed final.

It is particularly useful for quickly testing whether a visual idea has an audible rhythm. For this user, it is also the default route for dialogue-heavy sequences at the per-shot level. Preserve a coherent storyboard shot as one take when the live model and reviewed pilot support its cast, action and duration; use deliberate edit boundaries when those conditions fail.

## Risks that require a pilot or revision

The following are risks with native speech and require a representative pilot plus review:

- exact wording, reliable pronunciation, named UI/brand/legal language, or editable dialogue timing;
- stable recurring character voices across many shots;
- an exact mouth performance, speaker turn-taking, or a later change to one line;
- strict requirements for no subtitles, captions, embedded text, or watermarks;
- full-scene sound design, music editing, loudness control, or a long narrative sequence.

Do not silently route around these risks with separate dialogue for this user. If the native candidate fails wording, pronunciation, voice continuity, speaker turn-taking, mouth performance, or an embedded-text constraint, keep it as a failed candidate, revise the prompt or take, and seek user direction before changing the dialogue route.

## Prepare a native-audio shot

Before inference, make the chosen mode explicit in the input manifest:

- `audio_mode: native_audio_video` and the model/workflow family that genuinely produces both modalities;
- sound intent separated into exact dialogue/monologue text, named speaker, a viewer-visible speaker anchor (screen side, posture, wardrobe/prop and mouth visibility), silent visible listeners, language, delivery, approximate time ranges, minimal native ambience, foreground effects, music, and silence;
- whether speech must be intelligible, whether lip sync is visible, and any prohibited embedded text;
- the visual beat, continuity anchors, camera behavior, duration, and approved/provisional visual inputs as for every other shot.

Write the audio direction as a compact companion to the visual prompt. Put every exact Mandarin turn in both the prompt and manifest. Identify each speaker by a screen anchor visible in the supplied first frame: viewer-relative side, age/appearance, distinctive wardrobe or prop, and an unobstructed mouth. During that speaker's turn, all other visible people keep their mouths closed; a later speaker is not silent throughout. State the turn order and avoid overlap. Project IDs and names alone do not identify faces. If an intended speaker cannot be singled out or seen clearly, revise the framing or visual reference; split only when that cannot be resolved in a coherent take. State language, delivery, lip-sync requirement and audible layers. For dialogue planned for post ambience, ask for no music and minimal room tone rather than asking for silence or `no intelligible dialogue`.

### Model-facing dialogue syntax

Keep the cast ID, character name, and dialogue ownership in the manifest and visual anchor; do **not** place them inside the quoted dialogue or use a bare `speaker: dialogue` pattern. Native A/V models can treat a leading name, ID, or colon as spoken content. After visually identifying each speaker, give a separate ordered instruction for each turn, such as `First the viewer-right man speaks with his visible mouth. Speak only this exact Mandarin line: “……”. He closes his mouth. Next the woman behind him speaks ...` The quoted text contains only intended speech.

Preserve the original Chinese text for Mandarin dialogue. Do not convert it to pinyin, tone digits, or transliteration merely to discourage on-screen captions: that can slow delivery, flatten performance, or change pronunciation. If a candidate burns subtitles, retain the failed take and revise its visual/text constraints separately; only change the dialogue text or route with user direction.

### Prompt layer discipline

Keep the model-facing positive prompt focused. It should contain the visible setting and framing, on-screen cast and distinct speaker anchors, start state, primary action, end state, delivery, and ordered Mandarin turns. Include enough concrete detail to fix speaker assignment, physical blocking and prop orientation; remove detail that does not affect the take. Do not lead with boilerplate such as aspect ratio, frame rate or route name when the workflow already carries those settings.

Keep prohibitions targeted: unapproved people/voices, unintended captions or watermarks, continuity-breaking props, unwanted camera behavior, and identity or wardrobe drift. Natural writing may appear on correctly oriented scene props; exact legal or UI wording that must be readable belongs in a controlled post layer. If the validated workflow has a negative-prompt input, pass those constraints there. If it has no such input, put only the essential exclusions in the actual positive prompt and retain the fuller QC list in the manifest. Never describe a manifest-only negative list as though the model received it.

Verify the live server exposes a compatible native AV model, video VAE, audio VAE, text/audio conditioning, and an encoder that retains the generated audio. A node called `AudioVideoCombine` alone only proves muxing, not native generation. Submit a short representative dialogue pilot before an expensive run and use `ffprobe` on the retrieved MP4. The pilot passes only if it has a real audio stream and an audible, reviewable spoken performance.

## Save and review the result

Keep the normal per-run files under `06_shot_videos/<SHOT_ID>/runs/r00N/`, including the executable API graph and every native output returned by the encoder (including any `-audio` companion). Add to `run.json`:

- audio model/VAE or joint model selectors, audio sampling settings, language and seed;
- each retrieved native output filename, checksum, audio codec, sample rate, channel count, actual duration, and whether that exact output contains an audio stream;
- a truthful statement of what was jointly generated versus added after inference.

Review with both picture and sound:

- watch the chronological contact sheet for cuts, unintended text/subtitles, identity drift, and action continuity;
- listen for intelligibility, speaker separation, pronunciation, timing, ambience-to-dialogue balance, clipping, and sound/visual alignment;
- compare the actual audio against the manifest, including every required or forbidden text element and confirmation that the visually anchored intended speaker, not another visible person, articulates the line;
- mark the candidate `revise` if the selected MP4 lacks audio, generated captions/watermarks, an unintended voice, missing or unintelligible required words, or unreliable speech/lip sync conflicts with the shot contract. Do not add a replacement dialogue track without explicit user authorization.

A native AV MP4 is an approved shot only after review. If its sound is retained for a master, explicitly copy or reference it in the later voice/mix manifest; otherwise preserve it only as part of the shot candidate.
