# Shot-input QC

Use this gate for every paid video-generation input. Its goal is a compact, physically credible instruction that gives the video model one dominant thing to do and makes spoken Mandarin easy to hear and associate with the correct face.

## Review boundary

Use this review directly. When the user or task explicitly calls for an independent reviewer, give that reviewer the approved storyboard row, cited character and scene assets, first/end keyframes where applicable, adjacent-shot continuity facts, intended duration, selected model/route, and exact approved dialogue. A reviewer must not infer missing story facts, invent characters, operate remote infrastructure, submit jobs, or decide creative approval.

Save the following review object as `06_shot_videos/<SHOT_ID>/input/input_qc.json`:

```json
{
  "shot_id": "S01-001",
  "source_facts": ["approved storyboard: ...", "character asset: ..."],
  "on_screen_cast": [{
    "id": "A",
    "role": "speaker",
    "visible": true,
    "screen_anchor": "viewer-right, seated closest to camera, navy utility jacket, black thermos in foreground",
    "mouth_visibility": "unobstructed from line start to end"
  }],
  "permitted_background_people": "none",
  "visual_contract": {
    "camera_and_setting": "...",
    "start_state": "...",
    "single_primary_beat": "...",
    "physical_logic": "...",
    "allowed_secondary_motion": ["..."],
    "continuity_anchors": ["..."]
  },
  "performance_contract": {
    "scene_emotional_baseline": "what the people believe at this point in the timeline",
    "visible_people": [{
      "id": "A",
      "first_frame_expression_posture": "...",
      "reaction_trigger": "what changes during this shot",
      "end_expression_posture": "..."
    }],
    "adjacent_shot_emotional_continuity": "..."
  },
  "native_dialogue": [{
    "turn": 1,
    "speaker_id": "A",
    "speaker_visual_anchor": "the viewer-right man in the navy utility jacket beside the black thermos",
    "silent_listener_ids_during_turn": ["B"],
    "exact_mandarin": "...",
    "delivery": "...",
    "visible_mouth": true,
    "audio_direction": "dry Mandarin speech; no music; minimal room tone"
  }],
  "negative_constraints": ["no extra people", "no unintended subtitles or watermark"],
  "prompt_distractions_removed": ["..."],
  "status": "ready",
  "risks_or_revision": []
}
```

`source_facts` must point to supplied assets or storyboard facts. Empty dialogue uses `native_dialogue: null`; multiple approved speakers use an ordered array of turns. Do not create dialogue to make a shot feel fuller.

## Prompt drafting rules

The reviewer checks a compact motion contract rather than a scene synopsis. It must:

1. Name the exact people visible in frame and their count. For each person, record a **screen anchor** a video model can see: viewer-relative position, pose, distinctive wardrobe/prop, and whether their mouth is unobstructed. Internal IDs such as `A` or `C003` are project bookkeeping only; never use an ID by itself to identify a speaker in the model prompt. Default to no background people. Add an extra only when the storyboard explicitly needs one, identify its placement and behavior, and keep it non-speaking unless named.
2. Describe a coherent camera position, setting, subject placement, start state, one primary action, and end state. The action must respect the supplied set geometry and props: a visible screen faces the camera if its content must be seen; a seated person cannot simultaneously cross the room; a hand reaches only an object within reach.
3. Keep secondary motion subordinate. One small support action is normally enough. Remove unrelated acting, crowd behavior, decorative props, camera moves, UI copy, stylistic adjective stacks, and sound cues that do not help the single beat.
   For each story-relevant person in frame, preserve a distinct, playable expression or posture and one small reaction to the event or speaker. Ground the ensemble's mood in what these people know at this point in the timeline; a later conflict must not automatically make an earlier friendly exchange tense. Check that the cue can begin from the selected first frame and join the next shot.
4. For spoken shots, put every approved Mandarin turn verbatim in the manifest and MiniMax prompt, in order. Anchor each speaker to a distinct visible person using screen side, appearance, clothing or prop, and mouth visibility. During each turn, the other visible people keep their mouths closed; do not say they are silent throughout if they speak later. Specify language, delivery, lip sync, no music and minimal room tone. One continuous same-location exchange is eligible for one inference when the cast and timing remain legible; an unproven multi-speaker take needs an isolated pilot and review.
   Make `delivery` specific to that turn: conversational pace, pause, emphasis, volume and attitude where they affect meaning. Give silent listeners a small visible response without assigning them speech.
5. Put exact UI words, prices, notifications and legal conclusions that must be perfectly readable in a separate tracked-post requirement. Natural writing on correctly oriented props may remain in the generated scene.
6. State only targeted negatives. Reject unapproved people or voices, unintended captions/watermarks, overlapping or wrongly assigned speech, camera drift when the camera must stay locked, and identity/wardrobe changes.

### Positive/negative separation

Return the positive prompt and `negative_constraints` as distinct review fields. The model-facing prompt should describe visible subjects, framing, approved prop/start state, action, delivery and ordered spoken turns without restating workflow settings. Confirm whether the chosen workflow actually has a negative-prompt input: if it does, pass targeted negatives there; if it does not, include only essential exclusions in the model-facing positive text. Keep the full negative list for QC and record which constraints the model actually received.

If a required speaker cannot be uniquely located or becomes obscured during their turn, or the input demands incompatible locations, actions or exact readable UI in one frame, return `status: "revise"` with the smallest concrete correction. Revise blocking or prompt first when that can resolve the issue; propose a split when the spatial/timing conflict remains or a pilot demonstrates failure. Speaker count alone is not a reason to split.

## Required QC verdict

Set `ready` only if every answer is yes:

- Is every on-screen person named by an approved asset or storyboard role, with an explicit count?
- Does the visual description have one legible primary beat and physically plausible blocking?
- Are the shot's emotional baseline, each story-relevant person's visible reaction, and every spoken turn's delivery specific to this point in the story and compatible with the first frame and adjacent shots?
- Are camera, cast, setting, prop orientation, and entry/exit state unambiguous?
- Does the prompt exclude nonessential people, speech, readable UI, and unrelated motion?
- If there is dialogue, does each turn identify its approved speaker by a distinct viewer-visible anchor rather than an internal ID, keep that mouth unobstructed, and keep the other visible mouths closed during the turn?
- Are all approved Mandarin turns exact, ordered and feasible within the retained duration, with dry/minimal native ambience?
- Does the prompt omit details that do not affect this shot's visible or audible result?

Any "no" yields `revise` and identifies a concise correction or evidence-based sub-shot split. A coherent but unproven speaker/duration combination may receive `ready_for_isolated_pilot` when the user has authorized that test; this permits only the named pilot, not a batch. The producing agent preserves the review and accepts input only after resolving the risks and setting QC to `ready`.

## Batch continuity when one shot is unresolved

An unresolved creative choice or failed candidate must be ledgered and isolated to its shot. It does not automatically block later independent, already-approved shots. Continue those later submissions in the approved order when their own input QC, continuity dependency, and recovery checks pass; mark the unresolved shot as `decision_pending` in the batch plan or an equivalent durable note. At assembly, stop promotion of the master until every required EDL slot has either a retained candidate or an authorized substitute. Do not silently fill a missing shot with a different take.
