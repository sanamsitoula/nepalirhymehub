# Nepali Rhyme Hub — logo, banner, start and end frames (Flow prompts, v2, 2026-11-07)

## The idea: "Puntu and the Singing Himalaya"
- **Mascot:** Puntu (पुन्टु), the baby red panda of our songs. The red panda is a Nepali animal, so the mark is
  unmistakably Nepali, and no Nepali rhyme channel uses one (Nani & Babu and others use human children).
- **Shape:** a rounded badge whose top edge is a snowy Himalaya ridge; a marigold sunrise behind the peaks; Puntu in
  front playing a small madal; three music notes (marigold, crimson, sky blue) bounce out of the drum.
- **Sound match:** every brand sound starts with Puntu's two madal beats "धिन्-ता!" + a 4-note bansuri call
  (the jingle). Picture and sound always arrive together.
- **Text:** never drawn by Flow. A blank ribbon under the badge; our renderer writes "नेपाली राइम हब" on it.
- **Colours:** Night Blue `#14234B`, Marigold `#F7A21B`, Snow `#FFFFFF`, Sindoor Crimson `#C8102E`, Sky `#4FB3FF`.
- **Character lock (same as the songs):** baby red panda, fluffy rust-red fur, white face markings, a ringed bushy
  tail, big friendly dark eyes, a small green scarf.

## 1. Logo (Flow image, free) — three variations, Sanam picks one
**Base prompt (every variation):**
> Mascot logo for a Nepali children's music channel, centred with lots of empty space around it, on a plain flat
> deep night-blue background. A rounded badge whose top edge is a row of three snowy Himalaya peaks (the middle one
> a fishtail peak), a warm marigold-orange sunrise glowing behind the peaks, a night-blue sky with two tiny stars.
> In front of the mountains sits Puntu, a cute baby red panda: fluffy rust-red fur, white face markings, a ringed
> bushy tail curled around him, big friendly dark eyes, a small green scarf, a big happy open-mouth smile. He plays a
> small Nepali madal drum lying across his lap with both paws, and three music notes (marigold, crimson, sky blue)
> bounce up out of the drum. Under the badge, an empty blank marigold ribbon banner with nothing written on it.
> Glossy soft 3D mascot-logo style, thick clean outlines, simple bold shapes that still read at 98 pixels, high
> contrast, joyful. No text, no letters, no words, no numbers, no watermark, no signature.

| Variation | Added line |
|---|---|
| A — classic badge | "Round badge, the mountains inside a thick marigold ring." |
| B — mountain shield | "Shield-shaped badge, the snowy peaks rise above the badge edge, Puntu waving one paw." |
| C — sticker | "Die-cut sticker style with a thick white outline around the whole badge, Puntu winking." |

## 2. Banner art (Flow image, free) — evergreen, not one festival
> Wide panoramic banner illustration, golden hour turning to dusk over a Nepali hill village and the Kathmandu
> Valley: terraced green fields, Newar pagoda temple roofs and carved brick houses, prayer-free festive strings of
> warm golden lights, small diyo lamps on rooftops, snowy Himalaya peaks glowing pink and gold, the first stars in a
> deep-blue sky. On the left third Puntu the baby red panda (rust-red fur, white face markings, ringed tail, green
> scarf) sits on a hilltop rock playing a madal, music notes floating. The middle band of the picture is calm and
> darker, kept empty for a title. Premium 3D children's animated-film look, night blue and marigold colours.
> No text, no letters, no logo, no people.

## 3. Start frame (Flow video, 4 s, logo as ingredient) — the "धिन्-ता!" sting
Used for 2–3 s at the start of long videos only (Shorts start straight on the hook).
> Use the reference logo. Deep night-blue sky, a soft marigold sunrise glow. 0–1 s: the snowy Himalaya peaks of
> the badge rise up from the bottom. 1–2 s: Puntu the baby red panda pops up in front of them and hits his madal
> twice — on each hit a burst of golden sparkles and one bouncing music note (marigold, then crimson). 2–3 s: the
> badge ring draws itself around him, the blank ribbon unrolls underneath, Puntu smiles at the camera. 3–4 s: hold,
> notes floating, gentle twinkle. Static centred camera, smooth bouncy animation, joyful, child-friendly. No text,
> no letters.
**Sound (from the jingle):** madal "धिन्" + "ता" on the two hits, the 4-note bansuri call on the ring, bell on the hold.

## 4. End frame (Flow video, 8 s, logo as ingredient) — "फेरि भेटौँला!"
Used for the last 6–8 s of every long video (made-for-kids videos have no YouTube end screens, so it is in the picture).
> Use the reference logo. Dusk over a small Nepali hill village and pagoda roofs with twinkling warm lights, snowy
> peaks glowing pink, first stars. Puntu the baby red panda sits on top of the logo badge in the upper centre,
> waves goodbye with one paw, gives a small happy yawn and hugs his madal; music notes drift slowly upward and
> become stars. Gentle slow push-in, calm and warm. The lower third of the frame stays empty and dark for a title.
> No text, no letters.
**Sound:** the jingle's last line "नेपाली राइम हब!" and the closing bansuri motif + bell, then silence.
**Text added by our renderer:** "फेरि भेटौँला!" (Marigold) and "@NepaliRhymeHub" (Cream) in the lower third.

## 5. Jingle (Flow Music) — see `flow_brand.py` JINGLE
Madal "धिन्-ता!" → 4-note bansuri call → children: "नेपाली राइम हब! गाऔँ, नाचौँ, सिकौँ!" → bansuri call + bell.
110 BPM, D major, about 30 s; we cut the start sting (≈2.5 s) and the end tag (≈6 s) from it.

## 6. Approval order
1. Flow draws logo A, B, C and the banner art (free) → Sanam picks one logo.
2. Only then the start and end frames are generated in Flow video (credits, ~20) with the chosen logo.
3. Composed with the jingle and our Nepali text → review → uploaded to Studio and used in every video.

## 7. Detailed prompts v3 (2026-11-08) — based on the approved logo A and banner art
Use these in Flow (free image model), Gemini or ChatGPT. Text is always added afterwards by `brand_clips.py`.

### 7.1 Logo (square, 1:1)
> A premium mascot logo for "Nepali Rhyme Hub", a Nepali children's music channel. Square 1:1 canvas, plain flat
> deep night-blue background (#14234B), the emblem centred with 12% empty margin on every side.
> EMBLEM: a perfect round badge with a thick glossy marigold-orange ring (#F7A21B) and a thin cream inner line.
> Inside the badge: a night-blue sky with two tiny gold stars; three snowy Himalaya peaks across the upper half, the
> middle one the fishtail shape of Machhapuchhre, crisp white snow with soft blue shadows; a warm marigold sunrise
> glowing behind the peaks; a gentle green hill at the bottom.
> CHARACTER (in front of the mountains, overlapping the lower ring): Puntu, a cute baby red panda — fluffy
> rust-red fur, white face markings and white-tipped ears, big round friendly dark-brown eyes with a white sparkle,
> small black nose, a wide happy open-mouth smile, a ringed bushy rust-and-cream tail curled to one side, a small
> knitted green scarf. He sits and plays a small traditional Nepali madal drum (wooden barrel body, leather heads,
> thin straps) lying across his lap, both paws on the drum heads.
> Three music notes bounce up out of the drum: one marigold, one sindoor crimson (#C8102E), one sky blue (#4FB3FF).
> RIBBON: a wide blank cream-and-marigold ribbon banner curving under the badge, both ends folded back, completely
> empty — nothing written on it.
> STYLE: glossy soft 3D mascot-logo style, Pixar-like warmth, thick clean dark outlines, simple bold shapes that
> still read at 98 pixels, strong contrast, even soft studio light, joyful and child-friendly.
> NEGATIVE: no text, no letters, no words, no numbers, no fake writing on the ribbon, no watermark, no signature,
> no extra animals, no people, no flags, no busy background, no gradients outside the badge, not blurry.

### 7.2 Banner (wide 16:9, for YouTube 2560 x 1440)
> Wide panoramic 16:9 banner illustration, blue hour just after sunset over a Nepali hill village and the
> Kathmandu Valley. LEFT THIRD: Puntu, a cute baby red panda (fluffy rust-red fur, white face markings, big
> friendly dark eyes, ringed bushy tail, small green knitted scarf) sits on a mossy hilltop rock among tiny
> wildflowers, playing a small Nepali madal drum on his lap, smiling; a soft trail of glowing golden music notes
> rises from the drum. CENTRE BAND (from 35% to 65% of the height, from 20% to 80% of the width): calm, darker,
> low-detail sky and distant valley haze, kept empty for the channel name and logo. RIGHT THIRD: Newar pagoda
> temple roofs with tiered brick-red eaves, carved wooden windows and brick houses on terraced green-gold rice
> fields, warm strings of small golden lights and diyo lamps on rooftops. BACKGROUND: the snowy Annapurna and
> Machhapuchhre peaks glowing pink and gold in the last light, a deep night-blue sky with the first stars, distant
> twinkling valley city lights.
> COLOURS: night blue and marigold dominant, warm gold lights, soft pink snow. LIGHT: gentle rim light on Puntu, warm
> glow from the village. STYLE: premium 3D children's animated-film look, soft depth of field, clean and uncluttered.
> NEGATIVE: no text, no letters, no logo, no watermark, no people, no fireworks, no flags, no meat or food stalls,
> no busy detail in the centre band, not dark or gloomy.

**After generating:** logo → `brand/flow/logo_X.jpg`; banner → `brand/flow/banner_art.jpg`, then
`python -I brand/brand_clips.py banner` adds the logo, "नेपाली राइम हब", "NEPALI RHYME HUB" and the tagline inside the
1546 × 423 safe area.
