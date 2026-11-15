# Picture-sound routes

## Purpose and routing

The delivery target is an audiovisual work. Choose a route per storyboard shot or scene after its visual contract is known. A project may use different routes in different places; do not make one experimental native-A/V result the universal project default.

| Route | Use when | Main limitation |
|---|---|---|
| `native_audio_video` | This user's default for visible character dialogue and intended monologue: MiniMax jointly samples the performance and spoken Mandarin | Wording, recurring voice identity, and continuity must be reviewed; a valid audio stream is not proof of an acceptable take |
| `separate_sound` | Background ambience, music, foreground effects, loudness control, or a deliberately non-speaking shot | It must not silently replace required native character dialogue with TTS or manually timed voice |
| `hybrid` | Retain approved MiniMax dialogue while augmenting it with post-produced ambience, effects, music, or mastering | Native audio is usually a mixed track, so prompt for minimal room tone and make every added layer explicit |

Native A/V means that the selected model jointly samples picture and audio. An audio-driven visual model, text-to-speech track, or ordinary MP4 mux is not native A/V. Read `native-audio-video.md` when selecting that route.

## Dialogue and monologue default

For this user's productions, select `native_audio_video` for every character line, visible speaker turn, or intended monologue unless the user explicitly authorizes another route. The input packet and prompt must identify the exact spoken Mandarin text, speaker, language, delivery, temporal order, whether the mouth is visible, and the required lip-sync review. Do not put `no intelligible dialogue` in a shot prompt that the storyboard identifies as spoken.

Use `hybrid` when the native MiniMax voice remains the dialogue source and post-production only augments its background. Do not use `separate_sound` as an automatic fallback after a native dialogue failure; mark the candidate `revise`, preserve the failure evidence, and obtain user direction before replacing speech.

## Route contract

Before creating route-specific material, add or update a machine-readable manifest linked to the storyboard shot. It must record:

- shot/scene IDs, the visual candidate or approved visual inputs, and the selected route;
- dialogue text, speaker, language, intended timing, intelligibility and lip-sync requirements;
- `voice_source: minimax_native` for required dialogue or monologue, the expected native output filename(s), and whether post-production may only augment rather than replace it;
- ambience, foreground effects, music, silence, and prohibited audio/text;
- whether native sound is `retained`, `replaced`, `augmented`, or `excluded`;
- the target duration, synchronization/edit decision, current status, and reviewer-facing output paths.

The route is a candidate until picture and sound pass review. Approval never transfers from a visual-only run to its later audiovisual result.

## Material locations

Use these locations for new projects:

```text
06_shot_videos/<SHOT_ID>/runs/r00N/       # source visual or native-A/V generation
07_audio_assets/<SHOT_ID>/                # separate voices, ambience, effects, music, manifests
08_picture_sound_edit/<SHOT_ID>/r00N/     # route manifest, EDL, synchronized result, review
09_master/versions/v00N/                  # assembled film, delivery manifest, final review
```

Keep every raw native-A/V output in the generating shot run, including a companion `-audio` output when the encoder produces one. Before calling a dialogue shot retrieved or verified, inspect the selected local candidate with `ffprobe` (or an equivalent stream inspection) and record its audio codec, sample rate, channel count, duration, checksum, and source filename. Keep independently authored ambience, effects, and music in `07_audio_assets/`; do not bury them inside a rendered MP4. `08_picture_sound_edit/` contains the explicit decision that joins those source assets. Preserve all raw material and never overwrite an earlier candidate.

## Review and master convergence

Review route results for both modalities: picture continuity, exact spoken text, speaker assignment, intelligibility, lip sync where visible, ambience continuity, effect timing, clipping, loudness, prohibited embedded captions/text, and exact duration. For a required native-dialogue shot, absence of an audio stream, an unintended speaker, unusable Mandarin, or a mouth/performance mismatch is `revise`, not an invitation to substitute TTS. For long takes, check joins together with the continuous sound bed.

Only approved picture-sound results enter the master. The master timeline may combine all three routes, but it cites each shot's approved audiovisual result and records any final color, subtitle, loudness, or export transformation. Do not claim the film's audio is complete merely because individual shot MP4s contain audio streams.
