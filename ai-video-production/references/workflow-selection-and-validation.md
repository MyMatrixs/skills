# Workflow selection and validation

Choose a workflow from the shot's **control requirement**, not from a generic quality ranking. Confirm that the active ComfyUI instance exposes the required nodes and compatible model selectors before building a workflow.

## Route the shot

| Storyboard risk or requirement | Preferred workflow family | Required evidence before full run |
|---|---|---|
| Restrained atmospheric motion; no critical end composition | Dual-model I2V | approved first keyframe and a short pilot showing stable environment motion |
| Specific final composition, reveal, transition, or irreversible action | Start/end-frame VACE or equivalent first-last-frame workflow | aligned start and end images; the end visibly contains the intended story state |
| Named character with visible hand/body action or contact | Animate/pose-controlled workflow | identity reference plus pose video/images covering the action path and contact pose |
| Narratively important camera trajectory | Camera-conditioned I2V | named camera path/control asset; do not rely only on wording such as “slow descent” |
| Shot exceeds a prior proven duration but is within the live model's accepted range | One complete-shot pilot before choosing continuation | source/retained duration contract, resource check, and reviewed full-length candidate |
| Complete-shot pilot fails or the live model cannot produce the required duration | Latent/video continuation with overlap | a tested continuation window, overlap, and entry/exit edit plan |
| A candidate already passes story and motion review but needs smoother playback | Frame interpolation | review pass before interpolation; interpolation is never a repair for wrong action, direction, or identity |

Use the smallest sufficient control. A more elaborate workflow is not automatically better if the required evidence cannot be supplied.

## Validate before the full queue

For every newly adapted family, submit one inexpensive validation before expensive production runs. The validation should use the same essential control inputs and aspect ratio, but a shorter duration/resolution when that does not remove the relevant risk.

The pilot must answer the question that justified the workflow:

- VACE: did it actually reach the supplied final state without tail-end snapback?
- pose control: does the body, hand, contact point, and action direction remain valid?
- camera control: does the camera follow the requested path without unwanted drift or reversal?
- continuation: are identity, lighting, motion, and geometry coherent across the overlap?

Save the pilot's API graph, inputs, output, contact sheet, resource reading, and `pass`/`revise` result. If an explicit node/model/encoder mismatch occurs, correct that mismatch once and retry once. Do not queue a full batch until the pilot passes or the user explicitly accepts the risk.

## Long-shot assembly

For a physically continuous shot, attempt one full-length inference when a live capability check and bounded pilot support it. If continuation is needed, use latent/video overlap and retain an edit decision list containing each segment's in/out range, overlap duration, and continuity anchors.

If continuation is unavailable or fails review, split the storyboard shot into intentional sub-shots with visible edit points. Do not present a hard-cut chain as a single uninterrupted camera move. Render the assembled master to the exact storyboard duration and inspect a chronological contact sheet plus all join points.

## Live AutoDL observations

The inspected AutoDL environment exposed these useful, but still per-run verified, routes:

- `WanVideoVACEStartToEndFrame`: accepts start/end images, control images, masks, and frame indices;
- `WanAnimate2ToVideo` and `WanVideoUniAnimatePoseInput`: support pose-video/reference-driven character actions;
- `WanCameraImageToVideo` and ReCamMaster nodes: support camera conditions rather than text-only camera instructions;
- `WanVideoAddOneToAllExtendEmbeds`: supports continuation using prior latents, window size, and overlap;
- `RIFE VFI` and `GIMMVFI_interpolate`: provide post-review frame interpolation.

These node names prove availability only. Validate a compatible graph and selected model set before treating any route as ready.

## Resource gate and run monitoring

Before each batch, record free disk, GPU free VRAM, active ComfyUI process, HTTP health, queue state, exact model selectors, and output encoder. During active work, monitor GPU utilization, temperature, power, VRAM, disk, process health, and queue progress at a useful cadence.

Keep a single-GPU inference queue serial unless the chosen workflows and memory measurements prove safe concurrency. High utilization alone is not a quality target. Stop adding jobs on OOM, service loss, unsafe disk headroom, or repeated workflow errors; preserve completed assets and diagnostics.

On the observed RTX 5090 environment, 960×540 caused a RoPE shape error while 960×544 worked. Treat exact latent-grid dimensions as a verified setting, not a cosmetic rounding choice. Re-verify it whenever the model or workflow family changes.
