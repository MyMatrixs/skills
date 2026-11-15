# AutoDL ComfyUI native audio-video routes

This reference records two observed native audio-video routes on the known AutoDL 云绘 ComfyUI server. Both jointly produce video and audio before MP4 export. They are starting points, not a server inventory: verify the live `object_info` selectors, node inputs, service health, queue, VRAM, disk, and encoder before every run.

Use this reference together with `native-audio-video.md`. Keep a run's prompt, API graph, selected models, seed, resource observations, raw output, audio-stream metadata, contact sheet, and audiovisual review under the normal shot run directory.

## Route choice

| Route | Choose it when | Do not assume |
|---|---|---|
| LTX 2.5 text-to-audio-and-video | Fast, text-only atmosphere or concept tests; no reference assets are needed | Exact spoken wording, no embedded subtitles, or stable recurring character voices |
| MiniMax H3 Ref2VA | This user's required first route for short, reference-controlled character dialogue or monologue, and for native AV candidates that benefit from reference images/video | That a bundled workflow's model path is current, that empty references will preserve identity, that spoken wording/voice identity will be exact, or that 32 GB VRAM permits a longer/higher-resolution run |

For this user, MiniMax H3 is the first route for spoken character performance. It does not guarantee exact words, pronunciation, or recurring voice identity: test one representative dialogue shot, retain every audio-capable output, and review it before a billed batch. A final multitrack mix may add ambience, effects, music, and mastering, but must not silently replace accepted MiniMax dialogue.

## LTX 2.5 — validated text-only route

The validated local model set was:

- transformer: `Ltx/ltx-2.5-22b-distilled-transformer-comfy-int8-convrot.safetensors`;
- video VAE: `ltx-2.5-video-vae-conv-bf16.safetensors`;
- audio VAE: `ltx-2.5-audio-vae-bf16.safetensors`;
- text encoder: `gemma4-12b-with-proj-ltx-2.5-comfy-int8-convrot.safetensors`.

### Minimal graph shape

1. Encode one prompt containing the visual action and a separate, time-ordered description of dialogue, ambience, foreground sound, music, and silence.
2. Create `EmptyLTXVLatentVideo` and `LTXVEmptyLatentAudio` with matched frame count and FPS, then join them with `LTXVConcatAVLatent`.
3. Use `LTXVDualCFGGuider` with explicit video and audio CFG, sample the joint latent, then split it.
4. Decode video with the video VAE and audio with `LTXVAudioVAEDecode`; use an audio-capable encoder such as `VHS_VideoCombine` to retain the generated audio stream.

The observed 8-second candidate used 193 frames at 24 fps, a requested 0.6 MP setting, `euler_ancestral`, video/audio CFG 1, seed 1, and produced 1056×608 H.264 video with 48 kHz stereo AAC. It was a valid native AV output, but it burned in unwanted Chinese subtitles despite a negative instruction. Treat generated text/subtitles as a review failure, not something prompt wording reliably prevents.

### Template caveats

The bundled `video_ltx2_5_t2v_bult_In_Audio_API.json` was useful as a graph source but had stale selectors. The validated model requires the `Ltx/` prefix. An unconnected `SaveVideo` output node caused validation failure and must be removed or connected. Its unavailable latent-upscaler branch was bypassed for the validated first-stage output; do not enable unused nodes merely because they appear in the template.

The live installation also exposed `LTXVImgToVideo` and `LTXVReferenceAudio`, but their compatibility with a particular graph is unproven until a short pilot succeeds. Do not represent them as validated just because the nodes appear.

## MiniMax H3 Ref2VA — validated short pilot

The live server exposed a native AV reference-to-video graph using:

- transformer: `minimax/minimax_h3_ref2va_pruned_int8_convrot.safetensors`;
- video VAE: `minimax_h3_video_vae_fp16.safetensors`;
- audio VAE: `minimax_h3_audio_vae_fp32.safetensors`;
- text encoder: `qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors`;
- generation node: `MiniMaxH3ReferenceToVideo`.

The node can receive a prompt plus reference-media slots. The observed API template exposed nine image slots and three video slots. Leaving those arrays empty is allowed for a text-only comparison, but it does not provide the identity and composition control that justifies the Ref2VA route.

### Validated pilot profile

The pilot used the corrected model selector above, no references, a 0.9 MP 16:9 target, requested 5 seconds, 24 fps, `res_multistep`, `simple` scheduler, 20 steps, and seed `2026100401`. It completed as a native-audio MP4 at 1280×736, 5.167 seconds, H.264 plus 32 kHz stereo AAC. The visual review found a stable single character, continuous camera push-in, and no burned-in dialogue subtitles; human listening was still required before judging pronunciation or lip sync. Do not generalize this non-dialogue pilot to a dialogue batch: submit and inspect a representative Mandarin line with the intended first-frame reference.

A later S01-003 image-reference pilot completed one continuous **two-speaker** Mandarin exchange at 0.3 MP, 16:9, 345 frames/24 fps (14.375 seconds), 20 steps and `res_multistep`. Its 736×416 MP4 contained H.264 video and 32 kHz stereo AAC native audio; the three people and gate stayed visually stable, and the user considered the quality high. This shows that speaker count and a previous 5-second sample alone do not require splitting a coherent shot. The 32 GB GPU ran close to full VRAM, and automated recognition did not conclusively verify every spoken word; retain per-shot listening and lip-sync review, and re-check resources before changing resolution or duration.

### Resource boundary and template caveat

On the 32 GB RTX 5090, that 5-second 0.9 MP pilot reached approximately 31.6 GB of VRAM. Keep this route serial, do not enqueue a competing model, and treat any duration or resolution increase as a new pilot. Stop adding jobs on OOM or service loss; preserve the graph and diagnostics rather than repeatedly retrying.

The bundled `minimax_built_in_audio_builder_api.json` used a stale model name without the `minimax/` prefix. Replace it only after confirming the current selector. Its `VHS_VideoCombine` output must receive both the decoded video frames and audio stream; retrieve every returned output, including a possible `-audio` companion, then inspect the exact selected MP4 with `ffprobe`. An MP4 with an attached audio track is evidence of successful export but not sufficient evidence of dialogue quality.

## Shared acceptance checklist

- Confirm the API graph contains a joint AV sampling path and an audio decoder, not merely `AudioVideoCombine` with a pre-existing track.
- Record actual resolution, duration, video codec, audio sample rate/channel count, seed, and selected model/VAE/text-encoder names.
- Inspect a chronological contact sheet for cuts, bad action, embedded captions, watermarks, or identity drift.
- Listen for exact required wording, intelligibility, language, speaker assignment, lip sync, ambience balance, clipping, and the required silence/music conditions.
- Keep every output as a candidate until both visual and audio review pass. A one-sample comparison does not establish a model ranking.
