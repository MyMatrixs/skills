# Shot visual-consistency gate

Apply this gate to still first-keyframe generation and to the keyframes used for an I2V or native audio-video submission.

## Batch reference review

Generate a maximum of four new still-keyframe candidates per batch. Immediately before each batch—including a final batch of fewer than four—visually inspect only the approved assets that the batch will actually use:

- the reference sheets for every named, visible character in those shots;
- the matching scene state plate(s), plus its blocking map when screen direction, seating, table axis, entry point, or camera reversal matters;
- adjacent approved/candidate shots when they establish a required reverse angle, prop state, wardrobe state, or weather transition.

Record the inspected asset IDs/paths and the continuity facts that affect the batch in each shot packet or run record. Do not rely on an implicit visual memory, and do not review unrelated assets merely to satisfy the gate. If a batch needs more than four candidates, split it and repeat this review before the next group.

## Spatial and physical plausibility

Before submission, translate the reviewed assets into concrete screen constraints: visible cast count, identity anchors, viewer-relative placement, facing and eyeline, camera side of the 180-degree axis, depth ordering, and each story-critical prop's holder/resting point.

- A reverse shot must visibly face the opposite side of the same space. Do not reuse the preceding shot's distinctive background, furniture cluster, door/window relationship, or orientation unless the camera plan calls for it.
- Preserve the approved set geometry and blocking. Do not add unplanned characters, merge characters, duplicate them, or substitute an ambiguous look-alike for a named role.
- Require normal clearance between bodies, furniture, architecture, and props. Hands must have plausible anatomy and contact; no hand, limb, paper, chair, or person may intersect or pass through another object.
- Check the candidate at normal framing before accepting it. Revise a candidate that breaks placement, depth, background continuity, physical contact, or camera direction even if its facial identity is good.

## World-state realism

Prompts and review must reflect the visible conditions of the scene rather than treating people and props as weatherproof set dressing. Specify only conditions supported by the shot:

- In rain or just after rain, exposed outdoor surfaces should be wet; paper, clothing, hair, footwear, and objects show moisture only to the degree their exposure and elapsed time justify. For example, exposed paper can have damp edges, slight curl, spotting, or be protected under a hand or folder; covered material need not be wet.
- Wind, cold, dirt, handling, and time of day should have consistent, observable effects where they matter to the beat.
- Do not add dramatic damage, weather, or grime that the approved scene/time state does not support.

## Diegetic text

Do not impose a blanket ban on generated text. Include text when it has a clear in-world source and makes the frame more believable or communicates an approved story fact: for example, a naturally printed notice, a believable phone interface, a properly placed document heading, or an approved environmental sign.

Text must have a scene-appropriate physical surface, scale, perspective, language, contrast, and lighting. It must not appear as detached overlay copy, arbitrary gibberish, or an unexplained graphic. When exact wording, legally material content, names, numbers, or a precise UI label is required, use an approved verbatim text specification and a controllable compositing/tracked-text layer if the generation model cannot render it accurately. Keep any visible legal text fictionalized unless the project explicitly authorizes the source wording.

## Screen and document point of view

For every phone, monitor, letter, form, or other information-bearing prop, specify who can physically see its information in the shot. The visible surface must agree with that viewing relationship:

- When a character is reading or operating a hand-held phone, its screen faces that character. From an external over-the-shoulder or frontal view, the camera normally sees the phone back or edge, not the screen. Use a separate motivated insert or the character's POV only when the audience must read the display.
- A phone lying flat may face upward when the actor is looking down at it; camera visibility alone does not make it an information insert. Do not show readable UI to the audience unless the shot purpose calls for it.
- A character reading a held document sees its printed front. A camera on the opposite side therefore sees the blank or non-informative back. Show text only when the camera is deliberately on the document's printed side or in a motivated insert/POV. A document held at an oblique angle must still make its readable side physically reachable by its reader.
- Before accepting a candidate, verify that any visible writing is on the intended front side, not rendered through the reverse; blank backs and closed covers do not need invented writing. If a shot needs both the reader's reaction and legible content, split it into a reader-facing reaction shot plus a document insert, or use a clear over-the-shoulder composition.

## Candidate record

For each retained candidate, record the reviewed references, environmental assumptions, text treatment (none, generated diegetic, or post-composited), and any unresolved continuity risk. A generated still remains a candidate until user approval.
