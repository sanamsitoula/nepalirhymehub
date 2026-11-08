# Nepali Rhyme Hub — Launch Plan (draft, 2026-11-07)

## Status (2026-11-07, after Sanam's answers)
2nd round (Sanam): every song opens with a child saying "साथीहरू, आज हामी …"; festival songs follow Hindu tradition in detail, vegetarian only; two Tihar specials added (Bhailo, Deusi). Tihar 2083 = Nov 7-11 (Laxmi Puja Nov 8, Govardhan Nov 9/10, Bhai Tika Nov 11).
Answers: song mix (originals + 1 classic) · brand KEPT at the end of titles · added as a subu-os channel · make videos only (no posting plan yet).

| Song | lyrics.txt | lyric_score | scenes | seo.md | music | stills | clips | video |
|---|---|---|---|---|---|---|---|---|
| pani_paryo_jhamjham | ✅ | 10/10 | 12 + 10 | ✅ | — | — | — | — |
| ka_kha_ga_gha | ✅ | 10/10 | 12 + 10 | ✅ | — | — | — | — |
| tali_bajau_nachau | ✅ | 10/10 | 12 + 10 | ✅ | — | — | — | — |
| school_janchhu_ma | ✅ | 10/10 | 12 + 10 | ✅ | — | — | — | — |
| ek_dui_tin_ganti | ✅ | 10/10 | 12 + 10 | ✅ | — | — | — | — |
| bhailo_e_bhaili (Tihar, Laxmi Puja night) | ✅ | 10/10 | 12 + 10 | ✅ 10/10 | Flow Music running | — | — | — |
| deusi_bhan_mera_bhai (Tihar, Govardhan night) | ✅ | 10/10 | 12 + 10 | ✅ 10/10 | next | — | — | — |
| tara_baji_lai_lai | waiting for Sanam's traditional words (folder README) | | | | | | | |

- **subu-os:**
  - channel `nepali-rhyme-hub` added to `config/musicvideo.toml`, Flow only;
  - the songs are in `[batch] skip`, so nothing runs unattended;
  - project added to `config/projects.toml` (per-project kill switch);
  - the scorer label now reads "Devanagari (Hindi/Nepali)", and Nepali unsafe words were added;
  - setup item S83 added to USER_SETUP.md.
- **Titles:** with the brand kept they run 72–82 characters (60 is the guideline), but the search phrase sits within the first 47. Listed in `seo_titles.json` (`approved: false`).
- **Next, in order:**
  1. Sanam reads the Nepali lyrics.
  2. Logo goes to `brand/logo.png`.
  3. `python -m subu.musicvideo music pani_paryo_jhamjham --takes 2`: the Nepali pronunciation test in Flow Music.
  4. Audit the takes, then Sanam picks one.
  5. `reference` → stills → pipeline.html approval → Flow clips → render.
  6. Letters and numbers (songs 2 and 5) are added as renderer overlays. The renderer does not do this yet and needs a small addition.

## 1. What is in the folder today
- Rules: `CLAUDE.md`, `CHILD_FRIENDLY_NEPALI_RHYME_CREATOR.md` (9 roles, 10-point QA), `channel_settings_seo.md`, `brand/channel_info.json`.
- Research: `files (15)/` (competitors, SEO playbook, metadata template) and `NepaliRhymeHub_project_starter/` (strategy, 15-topic bank, 30-day plan, keyword bank, brand, checklist).
- Empty: `calendar/`, `posting/`, `_archive/`, `templates/rhyme_template/*`. **No songs, no logo, no characters yet.**
- Gaps found:
  - The "reference videos" were never read. They are now filled in `files (15)/reference_videos.csv`.
  - The SEO had no autocomplete evidence. That is now done (section 3).
  - The two title rules contradict each other: CLAUDE.md puts the brand in the title, the SEO playbook says no brand.

## 2. Gokul Kirtan format to copy (verified in `gokulkritan/balvenkateswara`)
- **Song folder:** `lyrics.txt` (Core Direction, Flow Music prompt, negative prompt, ARRANGEMENT MAP, clean lyric sheet), `scene.txt` (master style, character lock, at least 20 scenes), `scene_b.txt`, `musicvideo.json`, and the folders `music/ reference/ storyboard/ plan/ clips/ out/ social/ review/`.
- **Pipeline:** `subu-os` `python -m subu.musicvideo` (music, reference, prepare, clips, render) already supports several `[[channel]]` blocks. Only Gokul is configured today.
- **Gates:**
  - `lyric_score` must give 10/10 before Flow Music. It checks Devanagari, so Nepali passes. One check is labelled "Hindi", which is only a cosmetic issue.
  - `music_audit` scores every take.
  - Clips need approval on the `pipeline.html` review page first.
  - No clip is ever used twice.
  - Approved songs are locked.
  - Only free generators.

## 3. SEO evidence (YouTube autocomplete, gl=NP, 2026-11-07)
| Seed | Live suggestions (what people actually type) |
|---|---|
| nepali rhymes | for babies, **for nursery class**, **for class ukg**, **for lkg class**, collection, ka kha ga, tara baji lai lai |
| nepali balgeet | collection, **dance video**, **tali bajao**, pani muni macha, meow meow biralo, tara baji lai lai |
| ka kha ga | **ka kha ga gha nepali song**, ka kha ga gha gana, abcd |
| pani paryo | asina jharyo, **jhamma jhamma**, nepali song |
| kukhuri kaa | nani & babu, sound, dj song |
| school janchu | school janchu la, **school janchhu ma nepali song** |
| nepali cartoon song | for baby, dance, new |
| Devanagari-only (नेपाली बालगीत), "for kids", "counting", "animal", "dashain/tihar for kids" | **no suggestions** |

What this shows:
1. Roman Nepali phrases are what people search. The Devanagari-only and English "for kids" phrases get no suggestions, the same pattern as Gokul. Titles are therefore **mixed**: Devanagari hook + Roman search phrase.
2. Teachers and parents search by **class** (nursery, LKG, UKG). Nobody else targets this, so it is the low-competition opening.
3. "School Janchu La" has 28.1M views and 36K likes in 16 months. It is daily life plus kids performing: daily-routine topics win.
4. Two of the 7 references use the "X आऊ आऊ" repeated-call hook. A repeated call word is the dominant hook form.

**Title formula proposed** (≤60 chars, keyword in the first 55):
`<Devanagari hook> | <Roman phrase> Nepali Rhymes | <class/occasion>`
For example: `पानी पर्‍यो झमझम! | Pani Paryo Jhamma Jhamma | Nursery Class`.

## 4. Hook arc + "constant dopamine" (retention map for every song)
Toddlers watch with a parent. Their retention comes from **new reward every few seconds, not fast cuts**. Strobe cuts and overstimulation are banned by our own brand rules and by YouTube's kids-quality guidance.

| Time | Beat | Why |
|---|---|---|
| 0:00–0:03 | Sound word + character face close-up (e.g. "झम! झम!" + rain on Aarya's nose). No logo intro. | The thumbnail promise is paid at once |
| 0:03–0:12 | Chorus hook, sung twice, with one easy hand action | Hook by 0:15 (rule) |
| every 8–12 s | **New reveal**: next animal, number, colour or letter appears (a "what comes next?" payoff) | Curiosity loop, the core retention engine |
| ~0:40 | Action call: "सबैले ताली!" / "उफ्री!" | Physical participation |
| ~1:10 | **Guess game**: sound plays, 2-beat pause, kids shout the answer | Interactive peak; parents comment |
| verse 2 | Same structure, new world (nature ⇄ village alternate) | Novelty without a new learning load |
| bridge | Softest moment, then 1 bar of silence | Contrast resets attention |
| final chorus | Biggest burst; every character from the song returns | Payoff + rewatch |
| last 15 s | Outro tease of the next song's character, then end screen | Session time / next video |

Every chorus answer evolves, as in Gokul. Every shot is its own clip. Scenes alternate 50% nature, 50% village/home/school.

## 5. Recurring cast (from the creator framework, to lock on reference sheets)
- **Aarav (आरभ)**: 4-year-old boy, dhaka topi.
- **Aarya (आर्या)**: 4-year-old girl, two ribboned braids, gunyo cholo.
- **Puntu (पुन्टु)**: baby red panda mascot. This is original and Nepal-specific, so it does not copy Nani & Babu.
- Look: soft 3D chibi (same `look` line as Gokul so clips match), 16:9, logo drawn by the renderer.

## 6. First 5 songs (proposed, evidence-led, each with its own sound)
| # | Slug | Hook (no "कौन…?") | Search phrase | Lesson | Sound identity |
|---|---|---|---|---|---|
| 1 | `pani_paryo_jhamjham` | "झम! झम! पानी पर्‍यो" sound-word chant | pani paryo jhamma jhamma | weather, rain words, puddle play safely | 108 BPM G maj, madal + glockenspiel, female teacher lead |
| 2 | `ka_kha_ga_gha` | letter chant + object reveal per letter | ka kha ga gha nepali song | व्यञ्जन क–ञ with objects | 116 BPM D maj, xylophone + claps, child choir lead |
| 3 | `tali_bajau_nachau` | "ताली! ताली!" action call | nepali balgeet tali bajao / dance video | body parts + movement | 124 BPM A maj, Jhyaure 6/8 madal, male lead |
| 4 | `school_janchhu_ma` | morning bell + "तयार? हो!" | school janchhu ma nepali song | morning routine, bag, greeting teacher | 112 BPM C maj, guitar + sarangi, boy lead |
| 5 | `ek_dui_tin_ganti` | counting game, 1 to 10 hills/birds | nepali rhymes for nursery class | numbers १–१० | 104 BPM F maj, bansuri + damphu, girl lead |

Each one is original lyrics and an original melody. If traditional classics are allowed (question 1), `tara_baji_lai_lai` and `kukhuri_kaa` join as new arrangements.

## 7. Execution steps once answered
1. Set up the channel (folders, logo, `seo_titles.json`, add a `[[channel]]` to subu-os if approved).
2. Character reference sheets (Flow's free image model), then review.
3. Per song: Researcher → Lyricist (`lyrics.txt`) → `lyric_score` 10/10 → `mc-workflow` ARR-SPEC → Flow Music takes → `music_audit` + `mc-ai-tell-audit` → Sanam picks a take.
4. `scene.txt` + `scene_b.txt` (20+ scenes, the retention map above) → stills → `pipeline.html` approval → free clips → render 16:9 + long version.
5. SEO package per song: title, first 160 chars of the description, lyrics in Devanagari + Roman, tags, thumbnail brief (120px test), Shorts cut from the chorus, TikTok/IG/FB sidecars (30 TikTok tags; at most 5 tags on IG).
6. Calendar in `calendar/`. Nothing is posted until it is approved and the account check passes.

## 8. Risks
- **Flow Music may sing Nepali with Hindi pronunciation.** Test with song 1 before writing all five.
- **I am not a native Nepali reviewer.** Every lyric sheet needs Sanam's (or a fluent speaker's) read on pipeline.html.
- **Made-for-kids rules:** no comments and no notification bell on YouTube, so retention and search do the growth work.

## Open questions
See the conversation: traditional vs original, brand in title, subu-os channel, posting cadence/accounts.
