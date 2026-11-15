# AutoDL.Art Pro instance lifecycle

Use this reference only for the already-inspected AutoDL.Art Pro instance configured in the sibling `.env`. It is a practical operating procedure, not permission to start a remote server for planning or discussion.

## Credential boundary

- `.env` holds the developer token locally and is ignored by Git. `.env.example` is the safe shareable template.
- Never print, paste, upload, commit, or transfer `.env`; do not put the token in a project, ComfyUI workflow, run manifest, shell history, or remote server.
- The helper redacts credentials. If it reports an authorization failure or a login-expired message, obtain a fresh Developer Token from the AutoDL console, replace only `AUTODL_ART_TOKEN` in the local `.env`, and retry `status`. Do not paste the replacement token into chat or a terminal command.

## Local commands

Run these from the skill directory, or pass the absolute script path. The helper uses only Python's standard library.

```powershell
python scripts/autodl_art_instance.py status
python scripts/autodl_art_instance.py power-on --wait
python scripts/autodl_art_instance.py snapshot
python scripts/autodl_art_instance.py power-off
```

`status` is read-only. `snapshot` intentionally returns only safe connection and hardware metadata; it never prints server passwords or web tokens. `power-on` requests GPU-mode boot and `--wait` waits for the platform state to become `running`; it does not prove ComfyUI itself is ready. After it reports running, verify SSH/ComfyUI health and the actual workflow selectors before submitting a job.

### Capacity retry policy

For a user-authorized generation session, retry `power-on` only when the sanitized platform response explicitly reports unavailable capacity/resources. Retry at 3-minute intervals from the first such failure, with a hard 30-minute maximum window. Stop on the first success. If capacity is still unavailable at the deadline, stop and report the outcome; do not keep a background retry loop alive. Authentication, token, configuration, billing, network, and other API errors are not capacity failures and must be reported without this retry loop. A user cancellation or changed request ends the loop immediately.

Use `--dry-run` with `power-on` or `power-off` to inspect the request without changing instance state. The target instance ID can be changed locally only by editing `.env`.

## Required operating sequence

1. **Prepare while off.** Finish the script, storyboard, selected visual inputs, workflow JSON, prompts, target run directories, and acceptance checks locally. Decide the pilot and the full queue before requesting GPU power.
2. **Start only for live remote work.** Power on only when conducting a user-authorized capability test or producing actual assets. Run `power-on --wait`, then confirm the service is healthy, disk space is sufficient, model selectors exist, and no previous queue is active.
3. **Use the session fully but safely.** Run a minimal pilot if the workflow is unverified. Once accepted, submit the approved jobs in a controlled sequence. Monitor `nvidia-smi` (utilization, VRAM, temperature and power), free disk, ComfyUI queue/history, and output files. Do not overlap incompatible heavy models just to chase higher utilization.
4. **Preserve the work.** For every accepted result, copy it to the local project run directory, retain the workflow/prompt/seed/actual filename and media validation result, and confirm the local file opens before cleanup or shutdown.
5. **Close promptly.** Confirm ComfyUI has no executing or queued jobs, no upload/download is active, required outputs and metadata are local, and no recovery test is pending. Then run `power-off`. If any condition fails, resolve it first; never power off merely because the first candidate was produced.

## Monitor closure and shutdown attribution

Use a single heartbeat only while it has an allowed remote action: monitor an active job, execute the bounded capacity-retry policy, recover a known output, or move to the next approved packet. Update that heartbeat when the current shot changes rather than creating another one.

Delete the heartbeat immediately after its terminal notification when the batch is complete, the retry window expires, the user stops monitoring, work is redirected, a non-recoverable error requires user direction, or the batch is deliberately put on hold for a user decision. A safe hold with the instance off is terminal for that monitor; it is not a reason to keep polling quietly.

Immediately before an intentional shutdown, write the last known platform status, queue state, output-retrieval state, and an `agent_initiated` reason to the ledger or monitor record. This distinguishes it from a platform-side interruption. If a later status check returns `shutdown` with no such local record, call it an **unexpected platform-state loss**, not a service crash: preserve the last probe and sanitized API response, inspect whether the active output exists after recovery, and report that the root cause is unproven unless AutoDL exposes a specific event/reason.

The user's standing preference is: remote exploration and actual creation are valid reasons to start this server; all other steps remain local, and an idle instance is shut down after remote work is safely retained.

## Troubleshooting limits

- `running` is a platform state, not a ComfyUI readiness guarantee. Wait for the service health check before treating a run as available.
- If a command reports an API failure, capture only the sanitized error text and request a fresh token or user direction. Never retry with a token pasted into a command line.
- Do not use the AutoDL.Art lifecycle helper for an arbitrary AutoDL host. Confirm that its configured instance is the intended known environment before an action that changes power state.
