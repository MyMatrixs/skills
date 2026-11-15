# Storyboard Production

## Inputs

Use only the approved script version. Preserve each shot's source scene ID, any script lines it covers, and the character and location IDs it will require.

## Required outputs

Create `03_storyboard/versions/vNNN/` containing:

- `storyboard.md`: the primary human-review deliverable, with one explicitly headed shot section in timeline order.
- `shots.json`: the machine-readable equivalent.
- `continuity_review.md`: screen direction, 180-degree axis, eyelines, prop state, costume, lighting, and spatial-continuity checks.
- `storyboard_review.md`: shot-duration total, pacing, coverage, transitions, and unresolved production risks.

Create an `.xlsx` workbook only when the user explicitly requests a spreadsheet or needs spreadsheet-native collaboration. Do not make it the default merely because the storyboard has tabular fields. Existing workbook artifacts are historical evidence; preserve them rather than deleting or overwriting them.

Each Markdown shot section must include these information groups:

| Group | Required columns |
|---|---|
| Identification | Shot ID, timeline start/end, script scene ID, location, time, characters, narrative purpose |
| Direction | Shot size, viewpoint, camera movement, composition, image description, performance/psychology, intended viewer information/emotion |
| Sound and continuity | Dialogue, narration, sound/ambience, entry transition, exit transition, continuity note |
| Generation readiness | Duration, first-frame description, last-frame description, motion description, character IDs, location ID, light/color/style, generation status, approval status |

Use concise labels or a small field table beneath each `## <SHOT_ID>` heading. Keep the dialogue, start state, end state, motion, composition, and continuity note readable without horizontal scrolling. The Markdown and `shots.json` must agree on shot IDs, timing, and approval state; `shots.json` remains the automation source of truth.

## Quality gate

The storyboard must accurately cover the approved script and make the viewer's information and emotion legible. Establish space before dependent close-ups; cut only for new information, an emotional change, or motivated action; preserve screen direction and continuity; and provide a concrete first frame, last frame, and dynamic instruction for every future video shot.
