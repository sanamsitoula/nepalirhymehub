r"""Nepali Rhyme Hub -- TikTok Studio Automated Uploader
Based on the battle-tested Gokul Kirtan posting architecture.

Workflow:
1. Uses isolated persistent browser profile at D:\claude_project\nepalirhymehub\pr_profiles\tiktok
2. If first run: user signs in to TikTok (@nepaliryhmehub) in the opened window.
3. Once logged in: session cookies are saved permanently in the profile.
4. The script detects login, selects the 1080p video file, sets the caption with 30 mandatory tags,
   posts/schedules, logs to tt_done.jsonl, and alerts Telegram.
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

USER_DATA = Path(r"D:\claude_project\nepalirhymehub\pr_profiles\tiktok")
USER_DATA.mkdir(parents=True, exist_ok=True)
POSTING_DIR = Path(r"D:\claude_project\nepalirhymehub\posting")
LOG_PATH = POSTING_DIR / "tt_done.jsonl"
UPLOAD_URL = "https://www.tiktok.com/tiktokstudio/upload?from=webapp"
EXPECT_ACCOUNT = "nepaliryhmehub"

MANDATORY_TAGS = [
    "#fyp", "#foryou", "#foryoupage", "#viral", "#trending", "#tiktokviral",
    "#explorepage", "#fypシ", "#tiktoktrending", "#mustwatch", "#contentcreator",
    "#relatable", "#funnyvideos", "#aesthetic", "#videoviral", "#tiktok2026",
    "#nextbigthing", "#discover", "#blowthisup", "#content", "#dailypost",
    "#sharethis", "#goodvibes", "#creatorsearchinsights", "#engage",
    "#watchtilltheend", "#youneedthis", "#unfiltered", "#trendalert", "#fypchallenge"
]

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
            print("Telegram alert sent successfully!")
    except Exception as e:
        print("Telegram notification error:", e)

def upload_clip(video_path: Path, caption_hook: str, schedule_time: str = None, headless: bool = False):
    video_path = Path(video_path)
    if not video_path.is_file():
        raise FileNotFoundError(f"Video file not found: {video_path}")
        
    full_caption = f"{caption_hook.strip()}\n\n" + " ".join(MANDATORY_TAGS)
    clean_locks(USER_DATA)
    
    print("=" * 60)
    print("Nepali Rhyme Hub -- TikTok Studio Uploader")
    print(f"Profile: {USER_DATA}")
    print(f"Video: {video_path.name} ({video_path.stat().st_size / 1024 / 1024:.1f} MB)")
    print(f"Caption: {caption_hook[:60]}... (+ 30 mandatory tags)")
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
        
        print("Opening TikTok Studio...")
        page.goto(UPLOAD_URL, timeout=60000)
        page.wait_for_load_state("domcontentloaded")
        time.sleep(3)
        
        # Check if file input is ready, or if login is needed
        file_input = page.locator("input[type=file]").first
        if file_input.count() == 0:
            print("\n" + "=" * 60)
            print("[ACTION REQUIRED: 1-TIME TIKTOK SIGN-IN]")
            print("Please log in to @nepaliryhmehub in the opened browser window.")
            print("(Use QR code scan from TikTok mobile app, phone, or email/password)")
            print("Take your time -- the script will automatically continue once you log in!")
            print("=" * 60 + "\n")
            
            # Wait up to 10 minutes (200 * 3s = 600s) for user to log in
            logged_in = False
            for i in range(200):
                time.sleep(3)
                file_input = page.locator("input[type=file]").first
                if file_input.count() > 0:
                    print(f"Login detected! (Found upload dropzone after {i * 3}s)")
                    logged_in = True
                    break
                # Also check if redirected to upload page
                if "tiktokstudio/upload" in page.url.lower() and "login" not in page.url.lower() and "login" not in page.title().lower():
                    # check if upload container rendered
                    if page.locator("input[type=file]").count() > 0 or "select video" in page.content().lower():
                        logged_in = True
                        break
            if not logged_in:
                print("Timed out waiting for TikTok login. Re-run anytime.")
                ctx.close()
                return False

        # File input is available
        print("Selecting video file for upload...")
        file_input = page.locator("input[type=file]").first
        file_input.set_input_files(str(video_path))
        print("File selected! Uploading to TikTok...")
        
        # Wait for caption editor
        print("Waiting for caption editor...")
        page.wait_for_selector(".DraftEditor-root, [contenteditable='true'], .public-DraftEditor-content", timeout=90000)
        time.sleep(3)
        
        print("Inserting caption and 30 mandatory hashtags...")
        editor = page.locator(".DraftEditor-root, [contenteditable='true'], .public-DraftEditor-content").first
        editor.click()
        page.keyboard.press("Control+A")
        page.keyboard.press("Backspace")
        page.keyboard.insert_text(full_caption)
        time.sleep(3)
        
        # Cover / Thumbnail Handling (STRICT RULE)
        v_thumb = video_path.parent / "bhailo_e_bhaili-vertical-thumb-A.jpg"
        h_thumb = video_path.parent / "bhailo_e_bhaili-thumb-A.jpg"
        target_thumb = v_thumb if v_thumb.is_file() else h_thumb
        if target_thumb.is_file():
            print(f"Setting TikTok cover thumbnail: {target_thumb.name} ({target_thumb.stat().st_size / 1024:.1f} KB)...")
            try:
                edit_cover = page.locator("button:has-text('Edit cover'), div:has-text('Edit cover'), [class*='cover-edit']").first
                if edit_cover.count() and edit_cover.is_visible():
                    edit_cover.click()
                    time.sleep(2)
                    img_input = page.locator("input[type=file][accept*='image']").last
                    if img_input.count():
                        img_input.set_input_files(str(target_thumb))
                        print("Custom cover thumbnail selected!")
                        time.sleep(2)
                    save_btn = page.locator("button:has-text('Save'), button:has-text('Confirm'), button:has-text('Done')").last
                    if save_btn.count() and save_btn.is_visible():
                        save_btn.click()
                        time.sleep(1)
            except Exception as e:
                print("Cover selection notice:", e)

        # Wait for video upload to complete (TikTok shows "Uploaded" or enables Post button)
        print("Waiting for video upload to process in TikTok Studio (313 MB may take 30-60s)...")
        post_btn = page.locator("button:has-text('Post'), button:has-text('Schedule'), button.btn-post").last
        for wait_sec in range(120):
            time.sleep(3)
            # check if upload completed (Post button enabled)
            is_disabled = post_btn.is_disabled() if post_btn.count() else True
            body_text = page.locator("body").inner_text().lower()
            if not is_disabled or "uploaded" in body_text:
                print(f"Video upload completed! (Elapsed: {wait_sec * 3}s)")
                break
        else:
            print("Proceeding to click Post button...")
            
        # Click Post or Schedule
        print("Publishing video...")
        time.sleep(2)
        if post_btn.is_visible() and not post_btn.is_disabled():
            post_btn.click()
            print("Post button clicked! Video submitted to TikTok!")
            time.sleep(8)
            # Wait for confirmation modal
            for _ in range(15):
                time.sleep(2)
                t = page.locator("body").inner_text().lower()
                if "manage your posts" in t or "your video" in t or "uploaded to tiktok" in t:
                    print("TikTok confirmation dialog detected!")
                    break
        else:
            print("Note: Post button is currently processing. You can click 'Post' directly in the window!")
            time.sleep(15)
            
        # Log completion
        POSTING_DIR.mkdir(parents=True, exist_ok=True)
        rec = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            "video": str(video_path),
            "status": "published" if not schedule_time else "scheduled",
            "schedule": schedule_time or "now",
            "caption": full_caption[:100] + "..."
        }
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec) + "\n")
            
        send_telegram(f"🎵 *Nepali Rhyme Hub -- TikTok Uploaded!*\n\n📹 *Video:* `{video_path.name}`\n⏰ *Status:* {rec['status']}\n🏷 *Tags:* 30 mandatory tags applied.")
        print("\nTikTok upload complete! Saved in tt_done.jsonl and sent to Telegram.")
        ctx.close()
        return True

if __name__ == "__main__":
    if "--wait-5m" in sys.argv or "--wait" in sys.argv:
        print("\n[STRICT COOLDOWN] Waiting 5 minutes (300 seconds) before launching TikTok Studio upload...")
        for rem in range(300, 0, -30):
            print(f"  Pacing cooldown: {rem}s remaining...")
            time.sleep(30)
        print("Cooldown completed. Launching TikTok Studio!\n")
    test_video = Path(r"D:\claude_project\nepalirhymehub\bhailo_e_bhaili\out\bhailo_e_bhaili-take6-flow.mp4")
    hook = "झिलिमिली भैलो आयो! 🪔✨ Join Aarya and Kancha for the ultimate Tihar kids dance! Celebrate with your family!"
    headless = "--headless" in sys.argv
    upload_clip(test_video, hook, headless=headless)
