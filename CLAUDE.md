# Nepali Rhyme Hub (नेपाली राइम हब) — Project Guidelines & Production Rules

This document establishes the mandatory production standards for all children's Nepali rhymes, educational songs, 2.5D/3D animation videos, lyrics, audio mastering, and publishing assets in `D:\claude_project\nepalirhymehub`.

---

## 1. Channel Identity & Core Mission

- **Channel Name**: Nepali Rhyme Hub (नेपाली राइम हब)
- **Handle**: [@NepaliRhymeHub](https://www.youtube.com/@NepaliRhymeHub)
- **Channel ID**: `UCuZRsCjjzvlLPdL5AsgWE7w`
- **Official Contact Email**: `info.bhrikuty@gmail.com`
- **Language**: Nepali (`ne` / नेपाली भाषा in Devanagari script)
- **Target Audience**: Toddlers and young children (ages 1–8), parents, Nepali diaspora families looking to connect their children to Nepali language and culture.
- **Reference Standard**: Modeled after the production architecture and quality bar of [`D:\claude_project\gokulkritan`](file:///D:/claude_project/gokulkritan).

---

## 2. Child-Friendly Nepali Rhyme Creation Mandate

Every Nepali rhyme must inspire children to sing, dance, learn, and appreciate their language, nature, family values, and traditions.

### The 6 Core Objectives for Every Song:
1. **Learn Nepali Language & Vocabulary**: Introduce clear, rhythmic Nepali words, nouns, verbs, and pronunciation (e.g., जनावरका नाम, रङहरू, फलफूल, नातागोता, गन्ती, कखग).
2. **Celebrate Nepali Culture & Nature**: Feature Nepal's rich flora, fauna, and geography (Lali Gurans, Danphe, green hills, mustard fields, traditional homes, prayer flags, festivals like Dashain/Tihar).
3. **Impart Moral & Life Habits**: Teach kindness to animals, brushing teeth, washing hands, respecting elders (आदर/सत्कार), sharing, teamwork, and love for learning.
4. **Emotional Safety & Positive Framing**: Never use fear, punishment, or frightening creatures. All lessons are framed through encouragement, joy, and gentle guidance.
5. **Interactive Call-and-Response**: Energetic child-friendly interactions (clapping, jumping, mimicking animal sounds, simple hand gestures).
6. **Catchy 10–15s Opening Hook**: Every rhyme must deliver its most infectious melodic hook right in the first 10–15 seconds to hook toddlers instantly.

---

## 3. Musical Composition & Audio Engineering Standards

1. **Acoustic Nepali Folk & Child Pop Instrumentation**:
   - **Lead Rhythm**: Madal (मादल) with bouncy Keherwa, Jhyaure, or Khyali beats.
   - **Melody & Accent**: Bansuri (नेपाली बाँसुरी), Sarangi (सारङ्गी), acoustic nylon/steel guitars, Damphu/Tungna accents.
   - **Kids Pop Layer**: Playful bells, glockenspiel/xylophone, warm bass, and soft rhythmic handclaps.
2. **Tempo & Key**:
   - Tempo: **100–125 BPM** (steady, marchable, danceable for toddlers).
   - Keys: Open, bright major keys (C Major, D Major, G Major, A Major).
3. **Vocal Architecture**:
   - Warm, expressive, smiling lead vocalist (female/male child educator voice).
   - Enthusiastic children's choir ("नानी-बाबु समूह") answering in call-and-response.
   - Singable lyric pace: **4.0–5.5 characters per second**.
4. **Dynamic Subtraction Arrangement**:
   - *Verse 1*: Light acoustic layer (bansuri + guitar + claps; madal rests).
   - *Bridge*: Softest moment (sarangi/flute + vocal; 1 full bar of silence before final drop).
   - *Final Chorus*: Fullest celebratory burst (+0.5 dB lift with all instruments, claps, and children singing).
5. **Mastering Specs**:
   - Target Loudness: **-14 LUFS (±1.0 LUFS)**.
   - True Peak: **≤ -1.0 dBTP**.
   - Loudness Range (LRA): **4–10 LU**.

---

## 4. Visual & Video Production Rules

- **Handcrafted 2.5D/3D Animation Aesthetic**: High-end children's illustration style (Ghibli + modern 3D Pixar warmth), rich vibrant colors, cute expressive characters.
- **Widescreen 16:9 Aspect Ratio**: Rendered at 1080p (1920x1080), 24 or 30 fps.
- **Minimum 20 Unique Scenes per Rhyme**: 50% natural landscapes (rivers, meadows, hills, forests) / 50% village, school, home, and courtyard settings.
- **Zero Duplicate Clip Reuse**: Never repeat the exact same clip in the video. Every planned shot has a unique visual beat and camera motion.
- **Clean Visual Frame**: No text or titles burned directly into AI video generation pixels. All typography and channel branding are applied via renderer overlays.

---

## 5. Song / Rhyme Folder Structure

Each rhyme is completely self-contained in its own slug folder:

```text
nepalirhymehub/
├── brand/                    # Brand assets, logo, fonts, channel_info.json
├── posting/                  # Social & YouTube posting automation & sidecars
├── calendar/                 # Editorial calendar & curriculum plan
├── <rhyme_slug>/             # E.g. kukhuri_kaa, ma_ta_saano_chhu, dasain_tihar
│   ├── lyrics.txt            # Master Nepali lyrics with arrangement map
│   ├── scene.txt             # Visual scene breakdown (minimum 20 scenes)
│   ├── scene_b.txt           # Alternate pass scenes for long version
│   ├── musicvideo.json       # Metadata, chosen take, approval status
│   ├── music/                # take1.wav, take1.long.wav, stems, audit.json
│   ├── reference/            # character.jpg (character reference lock)
│   ├── storyboard/           # s01.jpg ... s20.jpg (approved stills)
│   ├── clips/                # flow/, gemini/, seedance/ (individual clips)
│   ├── out/                  # <slug>-master.mp4, <slug>-logo.mp4, thumbnails
│   ├── social/               # TikTok, Instagram, Facebook sidecars
│   └── review/               # Automated QA reports, checks.json, events.jsonl
```

---

## 6. Social Media & TikTok Mandatory Posting Rules

When generating social media sidecars (`.description`, `.txt`, TikTok/Instagram posts) for Nepali Rhyme Hub:
1. Include an engaging Nepali & English hook before the hashtag block.
2. Append the **mandatory 30 TikTok hashtags** to every TikTok post:
   ```text
   #fyp #foryou #foryoupage #viral #trending #tiktokviral #explorepage #fypシ #tiktoktrending #mustwatch #contentcreator #relatable #funnyvideos #aesthetic #videoviral #tiktok2026 #nextbigthing #discover #blowthisup #content #dailypost #sharethis #goodvibes #creatorsearchinsights #engage #watchtilltheend #youneedthis #unfiltered #trendalert #fypchallenge
   ```
3. Add relevant Nepali niche tags: `#nepalirhymes #nepalisong #nepalikids #nepalirhymehub #balgeet`.

---

## 7. YouTube Publishing & SEO Standard

- **Category**: Film & Animation or Music (Audience: **Yes, it's Made for Kids**).
- **Title Formula**: `Nepali Hook | Nepali Keywords / Rhyme Name | नेपाली बालगीत | Nepali Rhyme Hub` (under 60 characters for desktop/mobile display).
- **Video Language & Audio**: Nepali (`ne`).
