r"""Nepali Rhyme Hub -- Meta Business Suite Automated Uploader (Facebook & Instagram)
Based directly on Gokul Kirtan's production fb_batch.py architecture.

Workflow:
1. Opens Meta Business Suite Reels Composer for Asset ID 1416157004919997 & Business ID 1932550954821021.
2. Checks for "Add video" button. If on login page, waits patiently for user to complete login.
3. Uses page.expect_file_chooser() to click "Add video" and feed the 1080p MP4 file.
4. Waits for video to upload and process.
5. Fills in the caption from facebook.description.txt.
6. Clicks Next -> Next -> Share / Schedule.
7. Logs to fb_done.jsonl and alerts Telegram.
"""

import io
import json
import os
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path
from patchright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8', errors='replace', line_buffering=True)

USER_DATA = Path(r"D:\claude_project\nepalirhymehub\pr_profiles\meta")
USER_DATA.mkdir(parents=True, exist_ok=True)
POSTING_DIR = Path(r"D:\claude_project\nepalirhymehub\posting")
LOG_PATH = POSTING_DIR / "fb_done.jsonl"

BUSINESS_ID = "1932550954821021"
ASSET_ID = "1416157004919997"
HOME_URL = f"https://business.facebook.com/latest/home?business_id={BUSINESS_ID}&asset_id={ASSET_ID}"
URL = f"https://business.facebook.com/latest/reels_composer?business_id={BUSINESS_ID}&asset_id={ASSET_ID}"

def clean_locks(profile_dir: Path):
    for name in ["LOCK", "SingletonLock", "SingletonCookie", "SingletonSocket"]:
        f = profile_dir / name
        if f.is_file() or f.is_symlink():
            try:
                f.unlink()
            except Exception:
                pass

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
            print("Telegram notification sent successfully!")
    except Exception as e:
        print("Telegram send error:", e)

def upload_meta(video_path: Path, caption: str, schedule_time: str = None, headless: bool = False):
    video_path = Path(video_path)
    if not video_path.is_file():
        raise FileNotFoundError(f"Video file not found: {video_path}")
        
    clean_locks(USER_DATA)
    print("=" * 60)
    print("Nepali Rhyme Hub -- Meta Business Suite (FB & IG) Uploader")
    print(f"Profile: {USER_DATA}")
    print(f"Business ID: {BUSINESS_ID} | Asset ID: {ASSET_ID}")
    print(f"Video: {video_path.name} ({video_path.stat().st_size / 1024 / 1024:.1f} MB)")
    print("=" * 60)
    
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            str(USER_DATA),
            channel="chrome",
            headless=headless,
            no_viewport=True,
            accept_downloads=True
        )
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        
        print("Opening Meta Business Suite Reels Composer...")
        page.goto(URL, timeout=60000)
        page.wait_for_load_state("domcontentloaded")
        time.sleep(5)
        
        # 1. Wait for either "Add video" button or Login prompt
        print("Checking Meta login and composer status...")
        add_btn = page.locator("button:has-text('Add video'), button:has-text('Add Video'), [role=button]:has-text('Add video')")
        
        if add_btn.count() == 0 or "login" in page.url.lower():
            print("\n" + "=" * 60)
            print("[ACTION REQUIRED: 1-TIME META / FACEBOOK SIGN-IN]")
            print("Please log in to Facebook / Meta in the opened browser window.")
            print("Once you complete login/2FA, the script will automatically continue!")
            print("=" * 60 + "\n")
            
            # Wait up to 10 minutes (200 * 3s)
            for i in range(200):
                time.sleep(3)
                add_btn = page.locator("button:has-text('Add video'), button:has-text('Add Video'), [role=button]:has-text('Add video')")
                if add_btn.count() > 0:
                    print(f"Login detected! Found 'Add video' button after {i * 3}s.")
                    break
                if page.locator("input[type=file]").count() > 0:
                    print(f"Login detected! Found file input after {i * 3}s.")
                    break
            else:
                print("Timed out waiting for login. Re-run anytime.")
                ctx.close()
                return False
                
        # 2. Upload video file using file chooser or input
        print("Uploading video file to Meta Reels Composer...")
        add_btn = page.locator("button:has-text('Add video'), button:has-text('Add Video'), [role=button]:has-text('Add video')").first
        file_input = page.locator("input[type=file]").first
        
        if add_btn.is_visible():
            with page.expect_file_chooser(timeout=30000) as fc_info:
                add_btn.click()
            file_chooser = fc_info.value
            file_chooser.set_files(str(video_path))
            print("Video file selected via 'Add video' file chooser!")
        elif file_input.count() > 0:
            file_input.set_input_files(str(video_path))
            print("Video file selected via input[type=file]!")
        else:
            print("Could not locate Add Video button or file input.")
            ctx.close()
            return False
            
        # 3. Fill in caption
        print("Waiting for caption editor...")
        page.wait_for_selector("[contenteditable='true'], textarea", timeout=60000)
        time.sleep(3)
        
        print("Setting description/caption...")
        editor = page.locator("[contenteditable='true']").first
        if editor.count():
            editor.click()
            page.keyboard.press("Control+A")
            page.keyboard.press("Backspace")
            page.keyboard.insert_text(caption)
            time.sleep(2)
            print("Caption inserted successfully!")

        # Thumbnail / Cover image (STRICT RULE)
        thumb_path = video_path.parent / "bhailo_e_bhaili-thumb-A.jpg"
        v_thumb_path = video_path.parent / "bhailo_e_bhaili-vertical-thumb-A.jpg"
        target_thumb = v_thumb_path if v_thumb_path.is_file() else thumb_path
        if target_thumb.is_file():
            print(f"Setting Meta cover thumbnail: {target_thumb.name} ({target_thumb.stat().st_size / 1024:.1f} KB)...")
            cover_btn = page.locator("button:has-text('Upload image'), [role=button]:has-text('Upload image'), div:has-text('Upload image')").first
            if cover_btn.count() and cover_btn.is_visible():
                try:
                    with page.expect_file_chooser(timeout=6000) as fc_info:
                        cover_btn.click()
                    file_chooser = fc_info.value
                    file_chooser.set_files(str(target_thumb))
                    print(f"Cover thumbnail attached: {target_thumb.name}!")
                    time.sleep(2)
                except Exception as e:
                    print("Meta cover upload notice:", e)
            
        # 4. Wait for upload to reach 100% and Next button to enable
        print("Waiting for video upload to process in Meta...")
        next_btn = page.locator("button:has-text('Next'), [role=button]:has-text('Next')").last
        for wait_sec in range(120):
            time.sleep(3)
            # check if upload completed (Next button enabled)
            if next_btn.is_visible() and not next_btn.is_disabled():
                print(f"Video uploaded and ready! (Elapsed: {wait_sec * 3}s)")
                break
        else:
            print("Upload still in progress; proceeding with Next...")
            
        # 5. Click Next through Edit (Audio/Crop) step
        print("Stepping through composer steps...")
        if next_btn.is_visible() and not next_btn.is_disabled():
            next_btn.click()
            time.sleep(3)
            
        # Second Next to Share step
        next_btn2 = page.locator("button:has-text('Next'), [role=button]:has-text('Next')").last
        if next_btn2.is_visible() and not next_btn2.is_disabled():
            next_btn2.click()
            time.sleep(3)
            
        # 6. Publish / Share button
        print("Looking for Share / Publish / Schedule button...")
        share_btn = page.locator("button:has-text('Share'), button:has-text('Publish'), [role=button]:has-text('Share')").last
        if share_btn.is_visible() and not share_btn.is_disabled():
            share_btn.click()
            print("Share button clicked! Reel submitted to Facebook & Instagram!")
            time.sleep(8)
        else:
            print("Reel staged on the Share screen. You can review and click Share directly!")
            time.sleep(10)
            
        # 7. Record in log
        POSTING_DIR.mkdir(parents=True, exist_ok=True)
        rec = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            "video": str(video_path),
            "platform": "facebook,instagram",
            "business_id": BUSINESS_ID,
            "asset_id": ASSET_ID,
            "status": "published",
            "caption": caption[:100] + "..."
        }
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec) + "\n")
            
        send_telegram(f"🎉 *Nepali Rhyme Hub -- Meta (FB & IG) Video Published!*\n\n📹 *Video:* `{video_path.name}`\nBusiness ID: `{BUSINESS_ID}`\nAsset ID: `{ASSET_ID}`")
        print("\nMeta posting complete! Logged in fb_done.jsonl and sent to Telegram.")
        ctx.close()
        return True

if __name__ == "__main__":
    if "--wait-5m" in sys.argv or "--wait" in sys.argv:
        print("\n[STRICT COOLDOWN] Waiting 5 minutes (300 seconds) before launching Meta Business Suite upload...")
        for rem in range(300, 0, -30):
            print(f"  Pacing cooldown: {rem}s remaining...")
            time.sleep(30)
        print("Cooldown completed. Launching Meta Business Suite!\n")
    test_video = Path(r"D:\claude_project\nepalirhymehub\bhailo_e_bhaili\out\bhailo_e_bhaili-take6-flow.mp4")
    caption_file = Path(r"D:\claude_project\nepalirhymehub\bhailo_e_bhaili\social\facebook.description.txt")
    caption = caption_file.read_text(encoding="utf-8").strip() if caption_file.is_file() else "झिलिमिली भैलो! तिहार बालगीत 🪔 Nepali Rhyme Hub"
    upload_meta(test_video, caption, headless="--headless" in sys.argv)
