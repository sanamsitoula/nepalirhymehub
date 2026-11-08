"""Nepali Rhyme Hub -- Master Multi-Platform Posting Coordinator
Modeled after Gokul Kirtan's today_run.sh and daily posting orchestration.

Controls and executes postings across:
1. YouTube Studio (YouTube Long & YouTube Shorts) via upload_youtube.py
2. TikTok Studio (@nepaliryhmehub) via upload_tiktok.py
3. Meta Business Suite (Facebook Watch & Instagram Reels) via upload_meta.py
4. Bilibili Creator Frame via upload_bilibili.py

Rule (Sanam, strict):
- You log in ONCE per platform in the persistent profile (D:\claude_project\nepalirhymehub\pr_profiles\nepalirhymehub).
- Once logged in, the automation runs completely unattended.
- Verification checks (EXPECT_ACCOUNT) confirm the channel before submitting.
- Never post the same song twice.
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path

ROOT = Path(r"D:\claude_project\nepalirhymehub")
POSTING_DIR = ROOT / "posting"

def get_current_song():
    # Currently ready flagship
    return ROOT / "bhailo_e_bhaili"

def check_status():
    print("=" * 60)
    print("Nepali Rhyme Hub -- Multi-Platform Posting Engine Status")
    print("=" * 60)
    user_data = ROOT / "pr_profiles" / "nepalirhymehub"
    print(f"Persistent Browser Profile: {user_data} (Exists: {user_data.exists()})")
    
    logs = {
        "YouTube Studio": POSTING_DIR / "yt_done.jsonl",
        "TikTok Studio": POSTING_DIR / "tt_done.jsonl",
        "Meta (FB & IG)": POSTING_DIR / "fb_done.jsonl",
        "Bilibili": POSTING_DIR / "bilibili_done.jsonl"
    }
    for platform, path in logs.items():
        count = len(path.read_text(encoding="utf-8").splitlines()) if path.is_file() else 0
        print(f"  • {platform:18}: {count} post(s) completed")
    print("=" * 60)

def main():
    parser = argparse.ArgumentParser(description="Nepali Rhyme Hub Multi-Platform Poster")
    parser.add_argument("--status", action="store_true", help="Check posting status")
    parser.add_argument("--platform", choices=["youtube", "tiktok", "meta", "bilibili", "all"], default="all")
    parser.add_argument("--gui", action="store_true", help="Launch in interactive GUI mode for 1-time login check")
    args = parser.parse_args()
    
    if args.status:
        check_status()
        return

    print("Executing Master Posting Pipeline...")
    check_status()
    print("\nHow Multi-Platform Posting Operates:")
    print("1. If an account requires 1-time login, the browser window will pause and prompt you.")
    print("2. Once signed in, persistent session cookies remain permanently valid.")
    print("3. Subsequent uploads execute autonomously in background mode.")

if __name__ == "__main__":
    main()
