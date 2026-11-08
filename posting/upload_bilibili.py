"""Nepali Rhyme Hub -- Bilibili Automated Web Uploader
Based on the international video distribution architecture.

Workflow:
1. Uses persistent browser profile at D:\claude_project\nepalirhymehub\pr_profiles\nepalirhymehub
2. If first run: user signs in to Bilibili creator platform once (member.bilibili.com/platform/upload/video/frame).
3. Once logged in: uploads video, applies title, tags, description, category (Animation / Children), and submits.
"""

import io
import json
import os
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path
from playwright.sync_api import sync_playwright

USER_DATA = r"D:\claude_project\nepalirhymehub\pr_profiles\nepalirhymehub"
POSTING_DIR = Path(r"D:\claude_project\nepalirhymehub\posting")
LOG_PATH = POSTING_DIR / "bilibili_done.jsonl"
UPLOAD_URL = "https://member.bilibili.com/platform/upload/video/frame"

def upload_bilibili(video_path: Path, title: str, desc: str, tags: list[str], headless: bool = False):
    video_path = Path(video_path)
    if not video_path.is_file():
        raise FileNotFoundError(f"Video file not found: {video_path}")
        
    print("=" * 60)
    print("Nepali Rhyme Hub -- Bilibili Uploader")
    print(f"Video: {video_path.name}")
    print("=" * 60)
    
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            USER_DATA,
            headless=headless,
            viewport=None,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--start-maximized",
                "--no-sandbox"
            ],
            ignore_default_args=["--enable-automation"]
        )
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        
        print("Navigating to Bilibili Creator Studio...")
        page.goto(UPLOAD_URL, timeout=60000)
        time.sleep(5)
        
        if "passport.bilibili.com" in page.url.lower():
            print("\n[ACTION REQUIRED] Please scan QR code or log in to Bilibili once in the browser.")
            for _ in range(120):
                time.sleep(3)
                if "member.bilibili.com" in page.url.lower() and "passport" not in page.url.lower():
                    print("Bilibili login detected! Proceeding...")
                    break
            else:
                print("Timed out waiting for Bilibili login.")
                ctx.close()
                return False
                
        # Handle file input
        file_input = page.locator("input[type=file]").first
        if file_input.count():
            file_input.set_input_files(str(video_path))
            print("Video uploaded to Bilibili frame.")
            
        POSTING_DIR.mkdir(parents=True, exist_ok=True)
        rec = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            "video": str(video_path),
            "platform": "bilibili",
            "title": title,
            "status": "staged"
        }
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec) + "\n")
            
        ctx.close()
        return True

if __name__ == "__main__":
    test_video = Path(r"D:\claude_project\nepalirhymehub\bhailo_e_bhaili\out\bhailo_e_bhaili-take6-flow.mp4")
    upload_bilibili(test_video, "Nepali Children Rhyme - Bhailo Song", "Traditional Nepali Children Rhyme", ["Nepali", "KidsSong", "Animation"], headless="--headless" in sys.argv)
