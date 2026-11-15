# Script Production

## Inputs

Accept a concise idea, an existing outline, reference material, or an existing script. Guide the user to provide or choose: one or more genres, target duration, audience, delivery format, style/tone, reference constraints, and non-negotiable content. Preserve the original input in `01_brief/brief.md` and record a structured counterpart in `01_brief/brief.json`.

## Required outputs

Create `02_script/versions/vNNN/` containing:

- `story_outline.md`: logline, premise, character relationships, story structure, emotional curve, and ending.
- `script.md`: reading script with scene ID, location, time, visual action, characters, dialogue, performance/psychology when it changes visible behavior, and estimated duration.
- `script.json`: the same content structured by scene ID for downstream use.
- `script_review.md`: duration calculation, character and location count, production-complexity notes, continuity risks, and user decisions still required.

At `02_script/`, keep `script_manifest.json` with the approved version. Do not mark a version approved before the user accepts it.

## Quality gate

A script is ready for storyboarding only when it has a clear premise, purposeful scenes, visible actions rather than abstract explanation, character goals and choices, a controlled emotional rhythm, natural and attributable dialogue, an achievable duration, and feasible characters/locations/actions. Every scene must be usable by a storyboard without guessing its setting, time, action, or dramatic purpose.
