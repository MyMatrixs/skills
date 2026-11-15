# Observational shot detail

## Use

Read this only when the user wants a shot to feel observed in ordinary life: for example a companion-filmed travel diary, handheld phone vlog, casual documentary, street observation, or an intimate home-video record. It makes an individual shot richer; it does not change the one-shot generation model or replace the storyboard.

Translate the intended capture mode into a short, reviewable addition to the shot packet. Keep it separate from the primary visible beat so the generation and review can tell whether either failed.

## The observation card

For each applicable shot, record only the fields that affect the image:

| Field | What to specify |
|---|---|
| Capture relationship | Who is holding the camera and their relationship to the subject, if it affects framing or performance. Example: a friend walking just behind and to the subject's right. |
| Device signature | The intended device class and bounded imperfections: phone-like auto exposure, a small handheld sway, momentary reframing, or ordinary sensor texture. |
| Visible setting | Time, weather, surfaces, depth cues, and one or two truthful background elements that establish the place. |
| Subject's unperformed state | What the person is naturally doing or attending to before the main beat; do not ask them to pose or stare into the camera unless the story calls for it. |
| Physical response | One small cause-and-effect detail, such as wind moving loose hair, a canvas bag settling against a hip, or the camera holder stepping around a pedestrian. |
| Incidental observation | At most one non-plot event that belongs in the same time and space, such as a brief foreground occlusion or a passer-by crossing the far background. |
| Capture exclusions | The capture grammar that would break the style: for example commercial key lighting, drone coverage, stabilized gimbal glide, artificial rack focus, dramatic slow motion, or excessive bokeh. |

Describe facts the shot can establish. A `friend filming` viewpoint does not justify impossible angle changes, unexplained cutaways, or access to events outside that friend's position.

## Detail budget

Use a hierarchy in the final prompt:

1. **Anchor:** character identity, wardrobe/props, place, time, camera position, and the primary visible beat.
2. **Support:** one physical environmental response that makes the anchor feel present.
3. **Texture:** one incidental observation *or* one bounded camera imperfection.

Add a second texture item only when the shot is simple, long enough to accommodate it, and its entry/exit state is already known. Details may never compete with a story-critical hand action, dialogue mouth movement, pose path, or end composition. If several rich observations are important, allocate them to consecutive shots in the storyboard instead of asking one generation to cover them all.

## Prompt mapping

Write the anchor and support in the positive prompt. Phrase texture as a concrete event with a location and short duration, not as a vague request for realism.

```text
Observed-world detail:
The companion holds a phone at walking height, one step behind the subject's right shoulder.
The subject keeps her attention on the road rather than posing for the lens. A light breeze moves the loose ends of her hair.
Near the middle of the shot, a pedestrian briefly crosses the far left edge of frame; the operator makes one small natural reframing correction.
```

Put only the capture modes that would visibly violate this shot's intended look in the negative prompt.

```text
commercial studio lighting, drone viewpoint, perfectly stabilized gimbal tracking,
intentional posing to camera, dramatic slow motion, shallow-focus beauty shot
```

Do not copy a generic negative list into every shot. For an intentionally polished, locked-off, aerial, performance, or stylized shot, omit or explicitly override the conflicting capture exclusions.

## Review gate

Review the observation card together with the usual first/last-frame and motion requirements. The result passes this addition only if:

- its camera viewpoint remains physically possible for the declared operator;
- the subject's identity, wardrobe, props, and place remain continuous;
- the primary beat stays legible and completes as planned;
- the selected texture appears naturally without becoming a second event;
- the result does not add a prohibited capture grammar or an implausible change in camera/device behavior.

If the texture fails but the primary beat passes, retain the diagnosis as a style revision; do not mislabel the shot as a failed action or rebuild its core motion control without evidence.
