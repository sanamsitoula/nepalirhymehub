# Nepali Rhyme Hub — Brand Guide (v1, 2026-11-07)

Every asset (videos, Shorts, thumbnails, banner, social posts) follows this page. The pictures are generated from
one script, `brand/make_brand.py`, so they stay identical: change the script, run it again, never edit a PNG by hand.

## 1. Promise and voice
- **Promise:** गाऔँ · नाचौँ · सिकौँ! — original Nepali songs where children sing, dance and learn their language,
  festivals and heritage. Happy, safe, vegetarian, respectful of Hindu tradition and of every Nepali community.
- **Voice:** warm, playful, simple Nepali; every video opens with a child saying "साथीहरू, आज हामी …".

## 2. Colours
| Name | Hex | Use |
|---|---|---|
| Night Blue | `#14234B` | backgrounds, emblem disc, text outline |
| Deep Night | `#080E26` | darkest background, cards |
| Marigold | `#F7A21B` | the brand colour: emblem ring, Nepali title |
| Diyo Gold | `#FFD166` | highlights, tagline, light strings |
| Cream | `#FFF4E0` | English text, small text on dark |
| Sindoor Crimson | `#C8102E` | accent only (diyo oil, badges) |
| Flame Orange | `#FF7814` | flame and glow only |
Two dominant colours per picture: **Night Blue + Marigold**.

## 3. Type
- Nepali: **Nirmala UI Bold** (Windows), set with libass complex shaping. AI image models never draw text.
- English: **Segoe UI Bold**, uppercase with wide spacing for the name (NEPALI RHYME HUB).
- Never more than 3-5 words of text on a thumbnail.

## 4. Logo system (Puntu, since 2026-11-08)
| File | Size | Where |
|---|---|---|
| `logo.png` | 512 × 512, transparent | **bottom-right corner of every song video** (renderer, 170 px high, 36 px margin) |
| `flow/profile_A.png` | 800 × 800 | YouTube / TikTok / Facebook / Instagram profile picture (live on YouTube) |
| `watermark_A.png` | 150 × 150 | YouTube Studio watermark, entire video (live) |
| `banner.png` | 2560 × 1440 | YouTube banner (live); made by `brand_clips.py banner` |
The mark: Puntu the baby red panda playing a madal in front of the Himalaya in a marigold ring, "नेपाली राइम हब"
on the ribbon (text set by our renderer, never by AI). Never stretch, recolour or rotate it. The v1 diyo kit is in
`_archive/2026-11-08-diyo-and-entry/`; `make_brand.py` is retired.

## 5. Opening and closing (Sanam, 2026-11-08)
- **No entry / intro.** Every video starts straight on the song's hook at 0:00. (`entry.mp4`/`entry.png` are archived;
  the renderer adds an entry only if such a file is put back in `brand/`, so keep it out.)
- **Logo bottom-right on every song,** for the whole song part (`logo.png`). Shorts carry the same logo.
- **Exit:** `exit.mp4` (8 s Puntu goodbye with the name plate and the jingle ending) plays after the song.

## 6. Thumbnails
1280 × 720. The lead character's face 30–50 % of the frame, warm diyo light, Night Blue + Marigold, the Nepali hook
word big in Marigold with a Night Blue outline (rendered by `subu.publishing.thumbnail`), a small saffron occasion
badge (e.g. तिहार). Nothing in the bottom-right 20 % (the video length covers it). Pass the 120 px phone test.
Two versions per video for YouTube "Test & compare".

## 7. Characters (same in every song)
Aarya (girl lead, red ribbons, gunyo cholo), Aarav (dhaka topi, mustard kurta), Puntu (baby red panda, green scarf),
and friends from many Nepali communities. Character lock text: each song's `scene.txt`.

## 8. Don'ts
No fear, no fighting, no meat, no firecrackers in children's hands, no cremation scenes, no copied songs, titles,
characters or thumbnails of other channels, no text drawn by AI image models.
