# Known AutoDL ComfyUI profile

Use this only when operating the inspected AutoDL 云绘/ComfyUI environment. It is an observed baseline, not a substitute for the per-run inventory check. Do not store or request credentials in this file. Before changing the known AutoDL.Art Pro instance's power state, follow [AutoDL.Art instance lifecycle](autodl-art-instance-lifecycle.md).

## Verified workflow pattern

The server exposed ComfyUI 0.37 on an RTX 5090 with the WanVideoWrapper nodes. A successful higher-quality short I2V candidate used:

- `Wan/Wan2_2-I2V-A14B-HIGH_fp8_e4m3fn_scaled_KJ.safetensors` and `Wan/Wan2_2-I2V-A14B-LOW_fp8_e4m3fn_scaled_KJ.safetensors`;
- `Lightx2v/lightx2v_I2V_14B_480p_cfg_step_distill_rank64_bf16.safetensors`;
- `Wan2_1_VAE_bf16.safetensors` and `umt5-xxl-enc-bf16.safetensors`;
- `WanVideoImageToVideoEncode`, two `WanVideoSampler` stages, `WanVideoDecode`, and `VHS_VideoCombine`.

The working short-run baseline was 832×480, 24 fps, 81 frames for 3.375 seconds, six sampling steps split at step three, CFG 2, shift 8, `dpm++_sde`, SageAttention, and block swap 20. Treat these as a tested starting point; retain the user’s requested resolution, duration, and quality requirements rather than silently applying them everywhere.

An additional high-quality long-sub-shot test succeeded with the same 14B HIGH/LOW pair and block swap 20, but without the six-step LightX distillation LoRA: 960×544, 24 fps, 121 frames (5.04 seconds), 16 steps split 8/8, CFG 5, shift 8, `dpm++_sde`, and `video/h264-mp4` at CRF 16. The requested 960×540 failed before sampling with `apply_rope freqs shape is not broadcastable to input`; use dimensions aligned to the model’s required latent grid (960×544 worked) and perform one validation before queueing a whole sequence. This is a quality-oriented sub-shot profile, not evidence that 30+ seconds can be generated as one continuous inference.

## Operational safeguards

- Treat launch locations as live-discovered, not fixed. First check ComfyUI HTTP health and the running process. If service recovery is needed, locate the image-supplied launcher (for example an installed `start-comfyui.sh`) and verify its working directory before starting it. A previously observed `/root/LaunchTool311` layout is not guaranteed; an observed alternative image used `/root/zealman-app/start-comfyui.sh`. Do not substitute a generic `main.py` launch when an image-supplied supervisor is available.
- Query the active server's `object_info`, system stats, and selected model lists before using names from this profile. Bundled example workflows may contain stale paths.
- Use a unique remote filename for every input image and API workflow. Uploading same-named inputs into one ComfyUI input directory silently overwrites prior assets.
- Keep the API-form workflow, prompt ID, actual output filename, seed, and encoder result in the local run directory.
- On this server, `video/nvenc_h264-mp4` failed because the installed FFmpeg lacked `h264_nvenc`. `video/h264-mp4` successfully produced H.264 output. Verify the encoder with the first output rather than assuming GPU encoding is available.
- The 5B TI2V path was suitable only for a fast proxy and produced weak small-object and hand motion in this project. Use it for validation, not as an assumed final-quality workflow.
- The 14B dual-model path improves fidelity but does not itself guarantee direction. Start/end keyframes or motion references remain necessary for narrative-critical movement.
- During the 960×544/121-frame/16-step run, a 32GB RTX 5090 used roughly 14–16GB VRAM, reached around 575W, and remained stable around 57–72°C. Monitor these values plus disk and queue health during a real batch; do not store server credentials in a project or skill.
