"""Nepali Rhyme Hub -- 90-Day Posting Timeline & Multi-Platform Calendar Generator
Based directly on the battle-tested Gokul Kirtan subu.publishing calendar architecture.

Rule: 4-slot daily cadence (Nepal Time +05:45):
- 07:15: Hook A Short (Chorus Dance, 15-30s) -> YouTube Shorts, TikTok, Facebook Reels, Instagram Reels
- 12:45: Hook B Short (Story / Curiosity Hook, 15-45s) -> YouTube Shorts, TikTok, Facebook Reels, Instagram Reels
- 15:15: Story Teaser (Teaser Video / Carousel) -> Facebook Story, Instagram Story
- 18:45: Master Full Video (Long 3-5m Broadcast Video) -> YouTube Long & Facebook Watch
- 21:15: Hook C Extended Reel (~1-2m TikTok/FB cut) -> TikTok, Facebook, YouTube Shorts, Instagram Reels
"""

import csv
from datetime import date, timedelta
from pathlib import Path

START_DATE = date(2026, 11, 8)  # Today (Laxmi Puja / Bhailo 2083)
TOTAL_DAYS = 90
CALENDAR_DIR = Path(r"D:\claude_project\nepalirhymehub\calendar")

SONGS = [
    ("bhailo_e_bhaili", "झिलिमिली भैलो! | Bhailo Song Nepali 2083 | तिहार बालगीत", "Tihar Special / Bhailo Song"),
    ("madal_bajyo_thamtham", "मादल बज्यो ठमठम | Madal Bajyo Thamtham | नेपाली बालगीत", "Nepali Folk Instrument / Dance"),
    ("hamra_sahayogi_saathi", "हाम्रा सहयोगी साथी | Community Helpers Song | नेपाली बालगीत", "Social Pillars / Helpers"),
    ("hamro_gaun_ramailo", "हाम्रो गाउँ रमाइलो | Hamro Gaun Ramailo | सुन्दर नेपाल", "Village Life / Nature"),
    ("changa_udyo_firiri", "चङ्गा उड्यो फिरिरी | Changa Udyo Firiri | दशैँ रमाइलो", "Dashain / Kite Flying"),
    ("pingma_machchi_machchi", "पिङमा मच्ची मच्ची | Pingma Machchi Machchi | रोटेपिङ", "Traditional Swing / Festival"),
    ("hatti_aayo_jhum_jhum", "हात्ती आयो झुम झुम | Hatti Aayo Jhum Jhum | जनावर गीत", "Wildlife / Elephant Fun"),
    ("bandar_mama", "बाँदर मामाको उफ्री उफ्री | Bandar Mama Song | चञ्चल बाँदर", "Playful Monkey / Animal Rhyme"),
    ("bakhri_ko_chhamchham", "बाख्रीको छमछम | Bakhri Ko Chhamchham | नेपाली बालगीत", "Farm Animals / Joyful Kid"),
    ("bhale_basyo_kukhuri_kaa", "भाले बास्यो कुखुरी काँ | Bhale Basyo Kukhuri Kaa | बिहानी गीत", "Morning Routine / Wake Up"),
    ("gai_ko_bachho", "गाईको बाच्छो उफ्री उफ्री | Gai Ko Bachho | नेपाली बालगीत", "Cow & Calf / Empathy"),
    ("momo_aayo_plate_ma", "मःमः आयो प्लेटमा | Momo Aayo Plate Ma | नेपाली खाना", "Nepali Food / Momo Fun"),
    ("syau_kera_mitho_mitho", "स्याउ केरा मीठो मीठो | Fruits Song Nepali | स्वस्थ फलफूल", "Healthy Eating / Fruits"),
    ("aama_baba_pyaro_ghar", "आमा बाबा प्यारो घर | Family Love Song | मेरो परिवार", "Family Values / Love"),
    ("daant_majhaun_chamcham", "दाँत माझौँ चमचम | Toothbrushing Habit Song | सरसफाइ", "Daily Hygiene / Good Habits"),
    ("sabun_pani_chhamchham", "साबुन पानी छमछम | Handwashing Song | सफा हात", "Cleanliness / Health"),
    ("himal_hamro_aglo", "हिमाल हाम्रो अग्लो | Himal Hamro Aglo | सुन्दर सगरमाथा", "National Pride / Himalayas"),
    ("saat_rang_ko_indreni", "सात रङ्गको इन्द्रेणी | Rainbow Colors Song | इन्द्रेणी", "Colors / Nature Magic"),
    ("chhath_parva_aayo", "छठ पर्व आयो | Chhath Parva Song | सूर्य पूजा", "Madhesh Culture / Chhath"),
    ("chandi_naach_sakela", "चाँदी नाच साकेला | Sakela Sili Song | किराँत राई", "Rai & Kirat Heritage"),
    ("maghi_lauro_naach", "माघी लौरो नाच | Maghi Song | थारू संस्कृति", "Tharu Culture / Maghi")
]

TAGS = "#fyp #foryou #foryoupage #viral #trending #tiktokviral #explorepage #fypシ #tiktoktrending #mustwatch #contentcreator #relatable #funnyvideos #aesthetic #videoviral #tiktok2026 #nextbigthing #discover #blowthisup #content #dailypost #sharethis #goodvibes #creatorsearchinsights #engage #watchtilltheend #youneedthis #unfiltered #trendalert #fypchallenge"

def generate():
    CALENDAR_DIR.mkdir(parents=True, exist_ok=True)
    csv_rows = []
    headers = ["day", "date", "weekday", "time", "ist", "kind", "song", "clip", "what", "status", "platforms", "title", "hashtags", "note"]
    csv_rows.append(headers)
    
    md_lines = [
        "# Nepali Rhyme Hub: 90-Day Multi-Platform Posting Calendar",
        "",
        "Built strictly following the **Gokul Kirtan** multi-platform scheduling architecture.",
        "Times are in **Asia/Kathmandu (+05:45)** (IST is 15 minutes earlier).",
        "",
        "## Schedule Summary",
        "| Metric | Details |",
        "|---|---|",
        f"| **Window** | {START_DATE.isoformat()} to {(START_DATE + timedelta(days=TOTAL_DAYS-1)).isoformat()} (90 Days) |",
        f"| **Active Universe** | {len(SONGS)} Original Cultural Hit Rhymes |",
        "| **Daily Slots** | 07:15 (Short), 12:45 (Short), 15:15 (Story/Teaser), 18:45 (Master Video), 21:15 (Extended Short) |",
        "| **Platforms** | YouTube, TikTok, Facebook, Instagram, Bilibili |",
        "| **Mandatory TikTok Tags** | All 30 viral tags enforced on every short form post |",
        "",
        "## Day-by-Day Master Schedule",
        "",
        "| Day | Date | Time | Slot | Song | Platforms | Title | Note |",
        "|---:|---|---|---|---|---|---|---|"
    ]
    
    current_day = 1
    for i in range(TOTAL_DAYS):
        dt = START_DATE + timedelta(days=i)
        wday = dt.strftime("%a")
        dt_str = dt.isoformat()
        
        # Pick song
        song_tuple = SONGS[i % len(SONGS)]
        song_id, title, note = song_tuple
        
        # Slot 1: 07:15 Hook A Short
        csv_rows.append([current_day, dt_str, wday, "07:15", "07:00", "short", song_id, "a", "Hook A (Chorus Dance, 15-30s)", "ready" if song_id == "bhailo_e_bhaili" else "planned", "youtube, tiktok, facebook, instagram", f"{title} #Shorts", TAGS, note])
        md_lines.append(f"| {current_day} | {dt_str} {wday} | 07:15 | Hook A (Chorus) | `{song_id}` | YT Shorts, TikTok, FB Reels, IG Reels | {title} #Shorts | Morning Dance Hook |")
        
        # Slot 2: 12:45 Hook B Short
        csv_rows.append([current_day, dt_str, wday, "12:45", "12:30", "short", song_id, "b", "Hook B (Curiosity / Story, 15-45s)", "ready" if song_id == "bhailo_e_bhaili" else "planned", "youtube, tiktok, facebook, instagram", f"{title} #Shorts", TAGS, note])
        md_lines.append(f"| {current_day} | {dt_str} {wday} | 12:45 | Hook B (Story) | `{song_id}` | YT Shorts, TikTok, FB Reels, IG Reels | {title} #Shorts | Afternoon Story Hook |")
        
        # Slot 3: 15:15 Story Teaser
        csv_rows.append([current_day, dt_str, wday, "15:15", "15:00", "story", song_id, "s", "Story / Teaser Carousel", "ready" if song_id == "bhailo_e_bhaili" else "planned", "facebook story, instagram story", f"नयाँ बालगीत · {title}", "", "Teaser 3.5h before full video"])
        md_lines.append(f"| {current_day} | {dt_str} {wday} | 15:15 | Story Teaser | `{song_id}` | FB Story, IG Story | नयाँ बालगीत: {title} | Teaser 3.5h before full release |")
        
        # Slot 4: 18:45 Master Full Video
        status = "ready (rendered 1080p)" if song_id == "bhailo_e_bhaili" else "pipeline approved"
        csv_rows.append([current_day, dt_str, wday, "18:45", "18:30", "long", song_id, "", "Full Master Video (1080p)", status, "youtube, facebook, bilibili", title, TAGS, note])
        md_lines.append(f"| {current_day} | {dt_str} {wday} | 18:45 | **Full Master Video** | `{song_id}` | **YouTube Main, Facebook Watch, Bilibili** | **{title}** | **Prime Evening Broadcast** |")
        
        # Slot 5: 21:15 Hook C Extended Short
        csv_rows.append([current_day, dt_str, wday, "21:15", "21:00", "short", song_id, "c", "Hook C (Extended 1-2m Cut)", "ready" if song_id == "bhailo_e_bhaili" else "planned", "youtube, tiktok, facebook, instagram", f"{title} #Shorts", TAGS, note])
        md_lines.append(f"| {current_day} | {dt_str} {wday} | 21:15 | Hook C (Extended) | `{song_id}` | TikTok, FB Reels, IG Reels, YT Shorts | {title} #Shorts | Prime Night Viral Hook |")
        
        current_day += 1

    # Write CSV
    csv_path = CALENDAR_DIR / "calendar.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(csv_rows)
        
    # Write MD
    md_path = CALENDAR_DIR / "calendar.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))
        
    print(f"Generated 90-day calendar: {csv_path} and {md_path}")

if __name__ == "__main__":
    generate()
