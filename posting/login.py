r"""Nepali Rhyme Hub -- One-Time Profile Sign-In Utility
Copied directly from Gokul Kirtan's flow_pr_login.py architecture.

Opens the Patchright real Chrome profile for a platform so Sanam can sign in BY HAND, once.
Nothing is typed or clicked by a script: the window stays open until you sign in and close it.
All cookies, sessions, and 2FA approvals are permanently saved in the platform's profile.

Usage:
    py -3 D:\claude_project\nepalirhymehub\posting\login.py youtube
    py -3 D:\claude_project\nepalirhymehub\posting\login.py tiktok
    py -3 D:\claude_project\nepalirhymehub\posting\login.py meta
"""

import os
import sys
from pathlib import Path
from patchright.sync_api import sync_playwright

ROOT = Path(r"D:\claude_project\nepalirhymehub")
PROFILES_DIR = ROOT / "pr_profiles"

URLS = {
    "youtube": "https://studio.youtube.com/channel/UCuZRsCjjzvlLPdL5AsgWE7w",
    "tiktok": "https://www.tiktok.com/tiktokstudio/upload?from=webapp",
    "meta": "https://business.facebook.com/latest/home?business_id=1932550954821021&asset_id=1416157004919997"
}

def main():
    platform = (sys.argv[1] if len(sys.argv) > 1 else "youtube").lower()
    if platform not in URLS:
        print(f"Unknown platform '{platform}'. Choose from: youtube, tiktok, meta")
        return 1

    user_data = PROFILES_DIR / platform
    user_data.mkdir(parents=True, exist_ok=True)

    # Clean locks
    for lock in ["LOCK", "SingletonLock", "SingletonCookie", "SingletonSocket"]:
        f = user_data / lock
        if f.exists():
            try:
                f.unlink()
            except Exception:
                pass

    target_url = URLS[platform]
    print("=" * 60)
    print(f"Nepali Rhyme Hub -- 1-Time Hand Sign-In: {platform.upper()}")
    print(f"Profile Directory: {user_data}")
    print(f"Target URL: {target_url}")
    print("=" * 60)
    print(f"\nOpening real Google Chrome via Patchright on profile '{platform}'...")
    print("👉 Please log in by hand, complete 2FA or verification, then close the browser window.")
    print("The script will keep the window open for as long as you need.\n")

    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            str(user_data),
            channel="chrome",
            headless=False,
            no_viewport=True,
            args=["--start-maximized"]
        )
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        page.goto(target_url)
        
        try:
            while ctx.pages:
                ctx.pages[0].wait_for_timeout(2000)
        except Exception:
            pass

    print(f"\nProfile '{platform}' saved successfully! Future uploads will run fully autonomous.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
