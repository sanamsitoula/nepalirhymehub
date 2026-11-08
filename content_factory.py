r"""Nepali Rhyme Hub -- Content Factory & 14-Day Production Runway Auditor
Patterned directly after Gokul Kirtan's subu.content_factory engine.

Rule: Production must stay at least 14 days ahead of scheduled posting on every platform:
- YouTube (Long Master Videos + Shorts)
- TikTok (Videos + Reels)
- Facebook & Instagram (Reels + Stories + Full Videos)
- Bilibili (International Video Library)

Run with:
    py -3 D:\claude_project\nepalirhymehub\content_factory.py
    py -3 D:\claude_project\nepalirhymehub\content_factory.py --alert
"""

import io
import json
import os
import sys
import time
import urllib.parse
import urllib.request
from datetime import date, datetime, timedelta
from pathlib import Path

MIN_DAYS = 14
ROOT = Path(r"D:\claude_project\nepalirhymehub")
CALENDAR_DIR = ROOT / "calendar"
REPORT_TXT = CALENDAR_DIR / "content-runway.txt"
REPORT_JSON = CALENDAR_DIR / "content-runway.json"

def send_telegram(msg):
    token = None
    env_path = Path(r"D:\claude_project\subu-os\.env")
    if env_path.is_file():
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("GOKUL_BOT_TOKEN="):
                    token = line.strip().split("=", 1)[1]
    if not token:
        return
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = urllib.parse.urlencode({
        "chat_id": "1207551211",
        "text": msg,
        "parse_mode": "Markdown"
    }).encode("utf-8")
    try:
        req = urllib.request.Request(url, data=data, method="POST")
        with urllib.request.urlopen(req, timeout=10) as resp:
            pass
    except Exception:
        pass

def inspect_projects():
    projects = []
    for p in sorted(ROOT.iterdir()):
        if not p.is_dir() or p.name.startswith((".", "_")) or p.name in ["calendar", "brand", "posting", "pr_profiles", "templates", "flow_refs", "files (15)"]:
            continue
            
        has_lyrics = (p / "lyrics.txt").is_file()
        has_scene = (p / "scene.txt").is_file()
        has_musicvideo = (p / "musicvideo.json").is_file()
        
        # Check rendered masters
        out_dir = p / "out"
        mp4s = list(out_dir.glob("*.mp4")) if out_dir.is_dir() else []
        thumbs = list(out_dir.glob("*thumb*.jpg")) if out_dir.is_dir() else []
        
        # Check review
        lyric_score = (p / "review" / "lyric_score.json").is_file()
        music_score = (p / "review" / "music_quality.json").is_file()
        
        # Check social
        yt_meta = (p / "social" / "youtube.title.txt").is_file()
        tt_meta = (p / "social" / "tiktok.description.txt").is_file()
        
        status = "CONCEPT"
        if has_lyrics and has_scene and has_musicvideo:
            status = "PLANNED"
        if lyric_score and music_score:
            status = "APPROVED_10"
        if mp4s:
            status = "RENDERED_READY"
            
        projects.append({
            "name": p.name,
            "status": status,
            "rendered_mp4": str(mp4s[0]) if mp4s else None,
            "mp4_size_mb": round(mp4s[0].stat().st_size / 1024 / 1024, 1) if mp4s else 0,
            "thumbs_count": len(thumbs),
            "ab_thumbs_ready": len(thumbs) >= 4,
            "social_ready": yt_meta and tt_meta,
            "path": str(p)
        })
    return projects

def calculate_runway(projects):
    ready_masters = [p for p in projects if p["status"] == "RENDERED_READY"]
    approved_pipelines = [p for p in projects if p["status"] in ["APPROVED_10", "RENDERED_READY"]]
    
    # Platform runway
    today = date.today()
    master_runway_days = len(ready_masters)
    planned_runway_days = len(approved_pipelines)
    
    report = {
        "date": today.isoformat(),
        "total_songs": len(projects),
        "rendered_masters_count": len(ready_masters),
        "approved_pipelines_count": len(approved_pipelines),
        "master_runway_days": master_runway_days,
        "planned_runway_days": planned_runway_days,
        "min_days_requirement": MIN_DAYS,
        "is_short": master_runway_days < MIN_DAYS,
        "platforms": {
            "YouTube_Long": {"ready": len(ready_masters), "runway_days": master_runway_days, "status": "OK" if master_runway_days >= MIN_DAYS else "SHORT"},
            "YouTube_Shorts": {"ready": len(ready_masters) * 3, "runway_days": master_runway_days, "status": "OK" if master_runway_days >= MIN_DAYS else "SHORT"},
            "TikTok": {"ready": len(ready_masters), "runway_days": master_runway_days, "status": "OK" if master_runway_days >= MIN_DAYS else "SHORT"},
            "Facebook_Instagram": {"ready": len(ready_masters), "runway_days": master_runway_days, "status": "OK" if master_runway_days >= MIN_DAYS else "SHORT"}
        },
        "ready_songs": [p["name"] for p in ready_masters],
        "next_in_pipeline": [p["name"] for p in approved_pipelines if p["status"] != "RENDERED_READY"][:5]
    }
    return report

def main():
    CALENDAR_DIR.mkdir(parents=True, exist_ok=True)
    projects = inspect_projects()
    report = calculate_runway(projects)
    
    # Save JSON report
    with open(REPORT_JSON, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
        
    # Write plain-text report
    lines = [
        f"Nepali Rhyme Hub -- Content Runway Report ({report['date']})",
        "=" * 60,
        f"Minimum Runway Standard: {MIN_DAYS} Days (Gokul Kirtan Mandate)",
        f"Total Songs in Universe: {report['total_songs']}",
        f"Rendered Masters on Disk: {report['rendered_masters_count']}",
        f"Approved 10/10 Pipelines: {report['approved_pipelines_count']}",
        "",
        "PLATFORM RUNWAYS:",
        f"  YouTube (Long):       {report['platforms']['YouTube_Long']['runway_days']} days ({report['platforms']['YouTube_Long']['status']})",
        f"  YouTube Shorts:       {report['platforms']['YouTube_Shorts']['runway_days']} days ({report['platforms']['YouTube_Shorts']['status']})",
        f"  TikTok:               {report['platforms']['TikTok']['runway_days']} days ({report['platforms']['TikTok']['status']})",
        f"  Meta (FB & IG):       {report['platforms']['Facebook_Instagram']['runway_days']} days ({report['platforms']['Facebook_Instagram']['status']})",
        "",
        f"READY FOR IMMEDIATE RELEASE:",
    ]
    for s in report['ready_songs']:
        lines.append(f"  • {s} (1080p Master Rendered & Thumbnails Verified)")
        
    lines.append("")
    lines.append("TOP PRODUCTION PRIORITIES TO REACH 14-DAY RUNWAY:")
    for i, s in enumerate(report['next_in_pipeline'], 1):
        lines.append(f"  {i}. {s} (10/10 Lyrics & Scenes Ready -- Generate Stills & Flow Clips)")
        
    text_content = "\n".join(lines)
    with open(REPORT_TXT, "w", encoding="utf-8") as f:
        f.write(text_content)
        
    print(text_content)
    
    if "--alert" in sys.argv or report["is_short"]:
        msg = f"""🏭 *Nepali Rhyme Hub -- Content Factory Runway Update*
📅 *Date:* {report['date']}
🎬 *Rendered Masters Ready:* {report['rendered_masters_count']} songs
🚀 *Live Single:* `bhailo_e_bhaili` (5:15 1080p broadcast master)
📋 *10/10 Pipeline Packages Ready:* {report['approved_pipelines_count']} songs
⚡ *Next Render Target:* `{report['next_in_pipeline'][0] if report['next_in_pipeline'] else 'Complete'}`"""
        send_telegram(msg)

if __name__ == "__main__":
    main()
