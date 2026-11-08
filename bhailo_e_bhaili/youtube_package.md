# झिलिमिली भैलो! — YouTube package (2026-11-07)

Song folder: `nepalirhymehub/bhailo_e_bhaili` · music take for the video: **take6** (remastered from take4, music audit
10/10, lyric score 10/10, SEO 10/10). Upload text ready in `social/` (title, description with full lyrics, tags).
Nothing is uploaded or approved by Claude: Sanam approves on the review page (`nepalirhymehub/pipeline_server.bat`,
http://127.0.0.1:8767/) and makes the clips in Flow.

## 1. Evidence used (YouTube autocomplete, gl=NP, 2026-11-07)
| Seed | Live suggestions used |
|---|---|
| bhailo | **bhailo song nepali**, bhailo song dance, bhailo song lyrics, bhailo song tihar, भैलो गीत |
| deusi bhailo | **deusi bhailo songs 2083**, देउसी भैलो गीत |
| tihar song | **tihar song 2083**, tihar song nepali, tihar song dance |
| tihar song for kids | no suggestions → the kids angle goes in the description, not the title |
| bhailini | "bhailini aayo aangan" = an existing hit → never used |

## 2. Title A/B (YouTube Studio "Test & compare" takes up to 3 titles or 3 thumbnails)
Brand kept at the end (Sanam's rule). Search phrase inside the first 55 characters in every option.

| | Title | Chars | Why |
|---|---|---|---|
| **A (default)** | झिलिमिली भैलो! \| Bhailo Song Nepali 2083 \| तिहार बालगीत \| Nepali Rhyme Hub | 74 | hook word + biggest phrase + year |
| B | भैलो आयो, भैलो! \| Bhailo Song Nepali 2083 \| Tihar Song \| Nepali Rhyme Hub | 75 | the shouted line, adds "tihar song" |
| C | झिलिमिली भैलो 🪔 \| Deusi Bhailo Song 2083 \| तिहार बालगीत \| Nepali Rhyme Hub | 77 | catches "deusi bhailo songs 2083" |

Run A vs B vs C as YouTube's built-in test once the video has its first 1,000 impressions; keep the winner (watch-time
share), never judge before 7 days. Shorts keep their own title (below).

## 3. Hook options (hook-generator method: 6 written, scored, strongest chosen)
Used for the first description line, the Shorts caption and the thumbnail word.

| # | Hook | Pattern | Score | Note |
|---|---|---|---|---|
| 1 | **झिलिमिली! झिलिमिली! भैलो आयो, भैलो!** | sound-word chant | 9 | = the song's first second; ear-worm |
| 2 | लक्ष्मी आमा, आउनुहोस्! 🪔 | invitation | 8 | strong devotion, weaker for kids |
| 3 | के बल्यो? दियो! के फुल्यो? सयपत्री! | question game | 8 | best for a Short (kids answer) |
| 4 | भैलो खेल्न जाऔँ साथी! | call to play | 7 | generic |
| 5 | सेलरोटी! गोलो गोलो! 😋 | food reward | 7 | fun, off the Laxmi Puja core |
| 6 | आज औँसीको रात, भैलो आयो! | timing | 6 | tied to one night only |
Chosen: **1** for title and description; **3** for Short 2. Scores are editorial (no channel data yet: the
channel has no published videos).

Storyboard v2 (Sanam, 2026-11-07): Kathmandu Valley at night, Tihar/Deepawali lights, children of many Nepali
communities, heritage sites (Kathmandu, Patan and Bhaktapur Durbar Squares, Nyatapola, Changu Narayan,
Pashupatinath roof, Rani Pokhari, Boudhanath and Swayambhu in the skyline). 40 scenes (scene.txt + scene_b.txt).

## 4. Retention arc on take6 (real section times from `music/take6.audit.json`)
| Time | Section | What the viewer gets (the "new reward") | Scene |
|---|---|---|---|
| 0:00 | Intro | sparkle chant in the first second; dive over the glowing Kathmandu Valley | SCENES 1-2 valley → Maju Dega steps |
| 0:12 | Chorus 1 | hook + "भैलो! भैलो!"; children of 8 communities dance | SCENES 3-4 Basantapur, Patan Krishna Mandir |
| 0:25 | Verse 1 | quiet: red footsteps of Laxmi in a Newar home → puja room | SCENES 5-6 |
| 0:39 | Chorus 2 | "सयपत्री! मखमली!" — the whole city lights up, Nyatapola | SCENES 7-8 |
| 0:53 | Verse 2 | Bhaktapur doors, sel roti, traditional line | SCENES 9-10 |
| 1:06 | Instrumental | dhime + madal in Indra Chowk, Asan flower market | SCENES 11-12 |
| 1:22 | Verse 3 | crow, dog, cow of Tihar (three reveals) | SCENES 13-15 |
| 1:41 | Chorus 3 | "सेलरोटी! गोलो गोलो!" | SCENE 16 Changu Narayan |
| 1:54 | Bridge | whispered question game → 1 bar of silence | SCENES 17-18 Pashupatinath roof, window |
| 2:08 | Final Chorus | biggest: Basantapur full of children, Dharahara, far fireworks | SCENE 19 |
| 2:26 | Outro | "शुभ तिहार!" wave over the glowing valley | SCENE 20 |
Every 8-14 s a new picture reward; no fast cuts (kids channel).

## 5. Shorts (cut from the final export; 9:16 centre crop, the hook at 0:00)
| Short | From–to | Title | Why |
|---|---|---|---|
| 1 | 0:00–0:25 | झिलिमिली! भैलो आयो! 🪔 Bhailo Song 2083 #Tihar | hook + first chorus |
| 2 | 1:54–2:26 | के बल्यो? दियो! 🪔 Tihar question game #Bhailo | game → silence → biggest chorus (rewatch loop) |
| 3 | 1:22–1:41 | काग, कुकुर, गाई 🐦🐕🐄 Tihar का साथी #Tihar | animal reveals |

## 6. Thumbnail A/B (120 px phone-feed test, safe zones: nothing in the bottom-right 20 % where the time sits)
| | Picture | Text | Colours |
|---|---|---|---|
| **A** | Aarya holding a lit diyo by her face, singing, the diyo-lit Nyatapola / Durbar Square glowing behind | **झिलिमिली भैलो!** + saffron badge **तिहार** | night blue + marigold orange |
| B | the same art | **भैलो आयो!** big yellow, nothing else | yellow on night blue |
Files: `out/bhailo_e_bhaili-thumb-A.jpg`, `out/bhailo_e_bhaili-thumb-B.jpg` (rendered by our renderer, so the Nepali
is spelled right; the art comes from Flow's free image model). Test them with YouTube "Test & compare".

## 7. Upload settings
Made for kids: **Yes** (comments, notifications and end-screen links are limited by YouTube for made-for-kids
videos, so no pinned comment) · Category: Music · Video language: Nepali · Title/description language: Nepali ·
Playlist: चाडपर्व: तिहार · Altered/synthetic content: **Yes** (AI music and animation) · License: standard.

## 8. Timing (honest)
Laxmi Puja / Bhailo night = Sun 8 Nov 2026. Bhailo searches peak Nov 7-9 and fall after Bhai Tika (Nov 11). After
Sanam approves the stills, the Flow clips (about 30-40) and the render take hours; a first Short from the hook can go
out earlier. If the full video lands after Tihar, it is still a 2084 Tihar asset (update the year in the title then).

## 9. SEO score (measured, `social/` files)
10/10: phrase from autocomplete in title · phrase in first 55 characters · title ≤ 100 · hook + phrase in first 160
description characters · full lyrics in description · 13 relevant tags < 500 characters · 3 hashtags · no other
song's title · thumbnail brief passes the 120 px rules (editorial) · made-for-kids and language set (editorial).
