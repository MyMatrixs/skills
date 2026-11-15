# Shot-video prompting

## Prompt before inference

Turn one storyboard row into a compact motion contract. Do not use a generic “make a cinematic video” prompt.

1. **Lock invariants:** named character identity, wardrobe, scene geometry, camera position, lighting/time, and any prop that must remain in the frame.
2. **State the visible beat:** describe the single most important observable change from first frame to last frame.
3. **Specify direction and timing:** identify origin, destination, path, screen direction, and when the beat completes. For example, “right hand begins on thigh, rises continuously toward the terminal, and reaches it only in the final frames.”
4. **Limit secondary motion:** list only supportive motion that helps the beat, such as breathing, eye tracking, distant traffic, or one drone. Too many equal-priority actions reduce control.
5. **State camera behavior literally:** locked, slow dolly-in, descending crane, pan, or handheld. If no move is wanted, write “camera remains locked” and keep the keyframes aligned.
6. **Handle observed failures:** when the workflow has a separate negative-prompt field, put a few shot-specific failure modes there. In the scene prose, state the intended physical result positively and omit a generic quality-word list.

For a story-critical interaction with a prop, make the actor's agency explicit: name the acting hand or body part, its contact with the object, the directional motion, and the resulting object state. Prefer “with his right hand, he presses the two pages together and closes the budget sheet on the table” over “he closes the budget sheet.” The latter can leave the contact unspecified and let a video model animate the object independently.

For this user's current production, make the final model-facing prompt concise, concrete **scene prose**. English describes everything except exact quoted Mandarin speech and exact visible text. A prompt includes the setting, count and placement of visible people, one primary action, a playable expression for each relevant person, camera behavior, and critical object orientation. Keep analysis and alternate takes in the packet. For a silent shot, describe the quiet ambience and state that no one speaks; route final ambience separately. Validate the language boundary and exact dialogue against the approved packet before submission.

### Describe the scene rather than issue commands

Write in the order a viewer experiences the shot: frame and space, visible people and objects, action and expression, spoken line at the moment it is said, listener's response, then a short sound or continuity sentence if needed. A speaking turn should appear once, inside that person's action, rather than as a repeated instruction after the scene. Describe silence as behavior: “Yang nods after Liu Mei finishes and says nothing.” For multiple speakers, let their actions and exact lines follow one another in chronological order. Use a continuous take when the people share a coherent location and the first frame supports it.

Use declarative wording for a necessary constraint: “Speech is clear and synchronized; there is no music or subtitle.” A visible pair can be “the two people remain in frame,” and an object can “stay on the table.” Do not append a stock list of bans on extra people, identity changes, cuts, text, or props to every shot. Include a specific exclusion only when an observed failure makes it relevant, and express the desired visible state positively whenever possible. The review translation must express the same scene and exact lines in natural Chinese.

Example, based on a two-person transaction shot:

> A steady medium two-shot at the old hall table, with a pen, key and agreement on the tabletop. Liu Mei, in a blue quilted jacket, sits on the right with one hand on the agreement; gray-haired Yang, in a charcoal coat, sits on the left. She raises her eyes from the page and, friendly but serious, says: 「能住，不等于像城里的商品房一样能办过户。它是自建房，这点不能瞒你。」 Yang nods after she finishes and says nothing. Speech is clear and synchronized; there is no music or subtitle. Their faces remain clearly visible.

The paired Chinese review text describes that same action once: “堂屋桌边的双人中景，笔、钥匙和协议在桌上……刘梅从纸面抬眼，和气而认真地提醒：「……」；杨听完轻点头，没有说话。”

Store a Chinese review translation of that **same** English prompt, with the English prompt hash or revision ID. If the English version changes, update or mark the translation stale. This translation supports the review UI; it must never become the submitted prompt. Keep exact quoted dialogue and controlled visible wording identical across both views.

For Mandarin speech, normalize any numeric notation into natural Chinese numerals before the line is approved and copied into the prompt. Keep the value and unit unchanged: `127万` is spoken and written in the dialogue as `一百二十七万`; the number on a payment record or legal end card may still appear as `127万`. Apply this to narration and read-aloud lines as well as character exchanges. A preflight check should reject Arabic digits inside quoted spoken lines while leaving scene text and metadata alone.

## Make every scene description drawable

Write the positive scene description as observable screen information, not a summary of story intent. A reviewer should be able to draw the supplied first frame and the intended end frame from it without guessing. State only details that matter to the shot, but make each stated detail concrete:

- **People and geometry:** how many visible people there are; viewer-relative side, seat or standing position, facing direction, and relevant eyeline or distance relationship. Avoid vague references such as “the others” when placement matters.
- **Identity anchors:** the clothing, hairstyle, or distinctive allowed object that separates recurring characters when that distinction is needed for the beat or speaker assignment.
- **Room and props:** the table/chair/door or other spatial anchor that fixes the layout; each story-critical prop's exact holder or resting place, orientation, and whether it must remain still.
- **Temporal states:** the visible start state, one primary physical action, and visible end state. Describe contact and agency for any interaction, not merely the intended outcome.
- **Camera and light:** framing, camera behavior, and the lighting/time-of-day anchor only when they must hold across the edit.

Prefer image-space language such as “viewer-right lower chair,” “on the near edge of the walnut table,” and “left aisle toward the door” over inferred names or off-screen assumptions. Do not add decorative scene detail, a second plot beat, or facts a viewer cannot see. Before submission, remove any phrase whose first-frame placement, motion, or final state cannot be checked in a contact sheet.

## Direct the people, not just the props

For every story-relevant person visible in a shot, write one concise, playable cue: their expression, gaze or posture at the actual first frame; what they notice; a small visible reaction; and where that reaction settles by the end. A listener should react naturally without mouthing another person's line. For each spoken turn, describe the intended pace, volume, pause or emphasis and the attitude behind it, tied to that speaker's screen anchor and the exact Mandarin line. A label such as “angry” or “happy” alone gives too little control; a list of repeated smiles and gestures gives too much competing motion.

Read the emotional baseline from the scene's point in the story. Distinguish what the characters believed then from what they know later. In a transaction that was friendly when it happened, allow warmth and ordinary informality even if a later dispute makes the same words consequential. Retain a real warning or moment of doubt as a brief change within that baseline when the script requires it. Check the previous and next shot so faces, tone and reaction timing can join cleanly.

If the selected first frame already shows an action or expression, continue from it rather than restarting that action. If the new performance depends on a first-frame face, prop or position the reference cannot support, revise the visual reference or mark the input for review; prompt wording alone cannot erase a contradictory first frame. Keep the performance cues subordinate to the shot's primary physical beat.

For an internal or off-screen line, decide whether its sound source is genuinely invisible in this scene. Do not describe a visible character with moving lips as silent inner speech. Test the exact line as a short native-A/V pilot and listen; if it is too quiet, missing, or assigned to moving lips, try a story-consistent visible reading or spoken exchange as a versioned candidate. Preserve the rejected take and record why the change still expresses the approved story fact. Do not declare success from an audio stream or volume reading alone.

Use an English positive/negative pair for the verified Wan workflows unless the selected model documents a different prompt language. For this user's MiniMax native-dialogue shots, put every approved turn for the chosen shot in the manifest and prompt, with exact Mandarin, order, delivery, visible-mouth/lip-sync, no music and minimal room tone. A character ID is not a speaker anchor: describe each speaker's screen side, apparent age, clothing or prop, and unobstructed face. During each turn, the other people are silent with mouths closed. Keep the exchange within one continuous shot when its location, cast, action and timing are coherent; do not add dialogue from adjacent storyboard shots.

## Observational detail for a single shot

When a shot needs an observed, lived-in quality rather than a neutral coverage image, use [observational-shot-detail.md](observational-shot-detail.md). Add grounded detail in a hierarchy; do not turn a single-shot prompt into a condensed multi-scene treatment.

Describe the setting as the camera can actually see it: its time of day, spatial texture, useful background activity, and a specific camera-holder relationship when it matters. Then add only details that reinforce the primary beat:

- **subject state:** the subject's ordinary posture, attention, or unfinished action at the first frame;
- **one environmental response:** a small physical reaction such as hair responding to wind, a bag shifting as the subject walks, or a passing vehicle changing the sound/visual field;
- **at most one incidental event:** a passer-by briefly occluding the edge of frame, a glance toward a landmark, or a natural pause before continuing;
- **capture signature:** a deliberately bounded device or operator behavior, such as a companion's slightly uneven handheld framing or a brief autofocus/exposure adjustment.

Every added detail must either make the primary action more legible, preserve continuity, or establish the requested capture style. Keep it subordinate to the visible beat. Do not invent a separate plot event, a second competing action, or decorative detail that cannot remain coherent between the shot's first and last frame.

## Descriptive scene pattern

```text
A [locked / moving] [shot size] in [scene, time and useful spatial anchor].
[Character identity and screen position] is [actual first-frame state], with
[critical prop and its orientation] nearby. [Character] [physical action and
observable expression], then says: 「exact approved Mandarin line」.
[Listener's visible response and silence]. [Prop or body reaches the visible
end state]. Speech is clear and synchronized; there is no music or subtitle.
```

## Negative prompt template

```text
[direction failure], [unwanted camera behavior], [identity/wardrobe failure],
[anatomy or object failure], [unwanted people], unintended subtitles, watermark,
unexplained cut, blur
```

## Directional control rules

- If a vehicle, limb, gaze, or camera direction is story-critical, provide aligned start and end keyframes or a motion/pose reference. The final keyframe must visibly embody the intended direction.
- For traffic, name the vehicle orientation and destination in image space: “front grille/headlights face the near foreground; vehicles advance toward the bottom edge.” Do not rely only on “drive forward.”
- For a hand action, show the initial hand pose and target pose. Add the exact contact/hover condition and forbid the reverse path.
- When the end state is reached too early and holds, shorten the clip, move the end pose later, or split the action. Do not claim a frozen end pose is continuous acting.
- If a result appears reversed, inspect a chronological contact sheet and frame timestamps before blaming playback. Do not reverse the delivered MP4 if that would break the intended first frame; revise the motion constraints instead.

## UI, dialogue, and sound

Video models are not reliable for readable, exact interface text. For a required route name, button, chart, or terminal UI, create a clean UI plate or tracked post-production layer and record it as a separate required asset. Do not mark the visual beat complete when a required UI remains a blank screen. A generated keyframe can establish the physical terminal and broad card/icon layout, but exact labels, route names, and selections must be added as a designed tracked layer in post-production.

The same check applies to visible writing on paper. When the beat is writing, inspect chronological frames for ink appearing and remaining on the front of the page. If the hand moves but the page stays blank, revise the take or use a controlled, perspective-matched text treatment; record any unresolved preview limitation. Do not add text to a reverse-facing sheet merely to make the image look fuller.

Plan dialogue and ambience in the manifest. Once wording, speaker, timing, and language are approved, generate the required MiniMax voice and lip sync jointly with the picture; do not create a silent dialogue candidate unless the user explicitly asks for one. A non-speaking visual candidate must be labelled silent or post-ambience-only.

For two-person dialogue, describe each visible speaker and turn in the scene's flow: “The viewer-right man in the navy jacket beside the black thermos looks up and asks: 「怎么涨？」 The viewer-left man in the grey suit listens, then replies: 「我也不知道。」 He looks down at the table as the first man falls silent.” Verify both mouths can be seen from the first frame and that the words fit the duration. Revise framing or reference if a speaker is ambiguous; split only when the shot cannot hold the exchange or a pilot fails. Do not ask the model to infer a speaker from `C003`, an off-screen name, or audio alone.
