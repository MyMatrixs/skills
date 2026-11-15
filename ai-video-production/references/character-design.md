# Character Design

## Inputs

Use the approved script and storyboard. Derive role, gender, age, appearance, body type, hair, wardrobe, required expressions/actions, closest planned shot size, visual style, and period/location constraints. Do not invent sensitive identity details without a user or story basis.

## Candidate and approval workflow

Generate three candidates—`A`, `B`, and `C`—for every character. They should be deliberate variations around the same role brief, not unrelated designs. After selection, generate the selected identity's definitive turnaround: front, side, and back. For principal characters, add a face reference and expression sheet when the storyboard needs close-ups or notable acting.

## Required outputs

```text
04_characters/
  character_bible.xlsx
  C001_name/
    brief.md
    character_spec.json
    candidates/A/{concept.png,prompt.txt,generation.json}
    candidates/B/
    candidates/C/
    approved/{turnaround_front.png,turnaround_side.png,turnaround_back.png,face_reference.png,expression_sheet.png,selection.md}
```

`character_bible.xlsx` records the role and selection status for every character. Save prompts, raw assets, tool settings, and seed when available with each candidate. Only approved turnarounds and references may be used downstream.

## Quality gate

The approved character matches the story's identity and world, remains recognisable across all views, has reproducible clothing and distinguishing features, and can support the closest planned framing. A simple concept image is not a production-ready character reference.
