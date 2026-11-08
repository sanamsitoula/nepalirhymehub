import json
import os
import random
import re
import subprocess
import sys
import time
from patchright.sync_api import sync_playwright

ROOT = r"D:\claude_project\nepalirhymehub"
SONG = sys.argv[1] if len(sys.argv) > 1 else "bhailo_e_bhaili"
SONG_DIR = os.path.join(ROOT, SONG)
ACCOUNT = os.environ.get("ACCOUNT", "haripriyasitoula")
EMAIL = ACCOUNT + "@gmail.com"
USER_DATA = os.path.join(r"D:\claude_project\gokulkritan\posting\pr_profiles", ACCOUNT)
REFS = os.path.join(ROOT, "flow_refs")
os.makedirs(REFS, exist_ok=True)
UPLOADED = os.path.join(REFS, f"uploaded_{ACCOUNT}.json")
LEDGER = os.path.join(ROOT, "flow_bh_ledger.jsonl")
LOG = os.path.join(SONG_DIR, "musicvideo.log")
CLIPS_DIR = os.path.join(SONG_DIR, "clips", "flow")
os.makedirs(CLIPS_DIR, exist_ok=True)

MAX = int(sys.argv[2]) if len(sys.argv) > 2 else int(os.environ.get("MAX", "5"))
PAUSE = (int(os.environ.get("PAUSE_MIN", "25")), int(os.environ.get("PAUSE_MAX", "45")))
PRICES = {4: 8, 6: 10, 8: 12, 10: 15}
MODEL = "Omni 1.1 Flash"
SLOW_OK = 1.15
GENERATE_TIMEOUT_S = 900
FAILED_WORDS = ("failed", "couldn't generate", "could not generate", "violat", "try again")
FLAGGED = re.compile(r"unusual activity|captcha|verify (that )?you'?re (a )?human|not a robot", re.I)

HOLDER_MARK = ("(()=>{const s=[...document.querySelectorAll(\"button[aria-label='Start generation']\")].find(b=>b.offsetParent);"
               "let e=s;while(e&&!e.querySelector('[contenteditable=true]'))e=e.parentElement;"
               "document.querySelectorAll('[data-pr-box]').forEach(x=>x.removeAttribute('data-pr-box'));"
               "const b=e&&e.querySelector('[contenteditable=true]');if(b)b.setAttribute('data-pr-box','1');return !!b})()")

class Flagged(RuntimeError):
    pass

def say(msg):
    line = time.strftime("%H:%M:%S ") + msg
    print(line, flush=True)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")

def human(a=0.5, b=1.4):
    time.sleep(random.uniform(a, b))

def pick_duration(seconds):
    return next((o for o in sorted(PRICES) if o * SLOW_OK >= seconds), max(PRICES))

def check_flagged(page):
    # Only check visible elements for actual blocking flags / modals
    text = page.evaluate("(()=>{const el=[...document.querySelectorAll('.cdk-overlay-pane, [role=dialog], .mat-mdc-snack-bar-container, flow-toast')].filter(e=>e.offsetParent!==null); return el.map(e=>e.innerText).join(' ');})()")
    if text and FLAGGED.search(text):
        raise Flagged("Flow shows: " + " ".join(FLAGGED.search(text).group(0).split()))

def visible(locator):
    return [el for el in locator.all() if el.is_visible()]

def overlay_button(page, label=None, pattern=None):
    for b in visible(page.locator(".cdk-overlay-container button, .cdk-overlay-container [role=menuitem]")):
        t = b.inner_text().strip()
        if (label and (t == label or t.split()[-1:] == [label])) or (pattern and re.search(pattern, t)):
            return b
    return None

def escape(page):
    page.keyboard.press("Escape")
    human(0.4, 0.8)

def account_ok(page):
    labels = page.evaluate("[...document.querySelectorAll('[aria-label*=\"@\"],img[alt*=\"@\"]')]"
                           ".map(e=>e.getAttribute('aria-label')||e.alt)")
    return any(EMAIL in (l or "") for l in labels), labels[:2]

def open_ingredients(page):
    escape(page)
    visible(page.locator("button[aria-label='Add ingredients to the prompt box']"))[0].click()
    human(1.0, 1.8)

def upload_reference(page, title):
    path = os.path.join(REFS, title)
    if not os.path.isfile(path):
        ref_char = os.path.join(SONG_DIR, "reference", "character.jpg")
        with open(ref_char, "rb") as src, open(path, "wb") as dst:
            dst.write(src.read())
    open_ingredients(page)
    with page.expect_file_chooser(timeout=15000) as fc:
        page.locator(".cdk-overlay-container").get_by_text("Upload media").last.click()
    fc.value.set_files(path)
    for _ in range(60):
        time.sleep(3)
        text = page.locator(".cdk-overlay-container").inner_text()
        if title in text and "Uploading" not in text:
            escape(page)
            return
    raise RuntimeError(f"{title} did not finish uploading")

def reference_title(page):
    done = json.load(open(UPLOADED, encoding="utf-8")) if os.path.isfile(UPLOADED) else {}
    title = SONG + ".jpg"
    if done.get(SONG) != title:
        upload_reference(page, title)
        json.dump({**done, SONG: title}, open(UPLOADED, "w", encoding="utf-8"), indent=2)
    return title

def pick_model(page):
    family = page.locator(".cdk-overlay-container [aria-label='Select model family']")
    if not family.count() or MODEL in family.first.inner_text():
        return
    family.first.click()
    human(1.0, 1.6)
    option = page.locator(".cdk-overlay-container [role=menuitem], .cdk-overlay-container [role=option], "
                          ".cdk-overlay-container button").filter(has_text=MODEL)
    if not option.count():
        say(f"Note: {MODEL} not in dropdown, using current model")
        return
    option.last.click()
    human(1.0, 1.6)

def choose(page, seconds, price):
    trigger = page.locator("button[aria-label='Settings trigger']")
    if not trigger.first.is_visible():
        agent = [b for b in visible(page.locator("button")) if b.inner_text().strip() == "Agent" and not b.get_attribute("aria-label")]
        if agent:
            agent[0].click()
            human(1.2, 2.0)
    if not trigger.first.is_visible():
        raise RuntimeError("Flow settings trigger not showing")
    escape(page)
    for _ in range(3):
        trigger.first.click()
        human(1.0, 1.6)
        if "x1" in page.locator(".cdk-overlay-container").inner_text():
            break
    else:
        raise RuntimeError("could not open Flow's settings")
    for label in ["Video", "Ingredients", "MODEL", "16:9", "720p", f"{seconds}s", "x1"]:
        if label == "MODEL":
            pick_model(page)
            continue
        b = overlay_button(page, label=label)
        if b:
            b.click()
            human(0.4, 0.9)
    escape(page)

def prompt_box(page):
    if not page.evaluate(HOLDER_MARK):
        if page.locator("button[aria-label='Insufficient credits warning']").count():
            raise RuntimeError("Flow account has insufficient credits warning")
        raise RuntimeError("Flow prompt box not found")
    return page.locator("[data-pr-box]")

def add_ingredient(page, title):
    if prompt_box(page).evaluate("b=>{let e=b;for(let i=0;i<8&&e;i++){if(e.querySelector('img'))return true;e=e.parentElement}return false}"):
        return
    open_ingredients(page)
    page.locator(".cdk-overlay-container").get_by_text(title, exact=True).last.click()
    human(1.0, 1.8)
    b = overlay_button(page, pattern=r"Add to prompt")
    if b:
        b.click()
        human(0.8, 1.4)
    escape(page)

def write_prompt(page, text):
    box = prompt_box(page)
    box.click()
    human(0.3, 0.7)
    page.keyboard.press("Control+A")
    page.keyboard.press("Backspace")
    human(0.3, 0.7)
    page.keyboard.insert_text(text)
    human(0.8, 1.6)

def wait_tile(page):
    tile = page.locator("flow-video-tile").first
    seen_unfinished, start = False, time.time()
    while time.time() - start < GENERATE_TIMEOUT_S:
        time.sleep(random.uniform(5, 9))
        check_flagged(page)
        if not tile.count():
            continue
        text = tile.inner_text()
        has_menu = tile.locator("button[aria-label='More options']").count() > 0
        if re.search(r"\d+%", text) or not has_menu:
            seen_unfinished = True
            if any(w in text.lower() for w in FAILED_WORDS):
                raise RuntimeError("Flow could not generate this clip: " + " ".join(text.split())[:160])
        elif seen_unfinished:
            human(2, 3)
            return
        elif (time.time() - start) > 60 and has_menu:
            say("Tile has completed options menu (finished). Proceeding to save.")
            human(2, 3)
            return
    raise RuntimeError("generation timed out")

def save(page, out):
    tile = page.locator("flow-video-tile").first
    tile.scroll_into_view_if_needed()
    tile.hover()
    human(0.8, 1.5)
    tile.locator("button[aria-label='More options']").click()
    human(1.0, 1.6)
    b = overlay_button(page, label="Download")
    if not b:
        raise RuntimeError("Download not in tile menu")
    b.click()
    human(1.0, 1.6)
    q = overlay_button(page, pattern=r"720p") or overlay_button(page, pattern=r"1080p")
    if not q:
        raise RuntimeError("no 720p or 1080p download offered")
    with page.expect_download(timeout=600_000) as dl:
        q.click()
    dl.value.save_as(out + ".part")
    os.replace(out + ".part", out)
    escape(page)
    return os.path.getsize(out)

def make_clip(page, clip, rec):
    clip_id = clip["id"]
    out = os.path.join(CLIPS_DIR, clip_id + ".mp4")
    if os.path.isfile(out):
        rec["status"] = "skipped"
        return rec
    seconds = pick_duration(clip["seconds"])
    price = PRICES[seconds]
    before_tiles = page.locator("flow-video-tile").count()
    if before_tiles > 0:
        page.locator("flow-video-tile").first.scroll_into_view_if_needed()
    escape(page)
    title = reference_title(page)
    choose(page, seconds, price)
    add_ingredient(page, title)
    write_prompt(page, clip["prompt"])
    
    # Ensure dialogs or blockers are not in front
    escape(page)
        
    start_btn = visible(page.locator("button[aria-label='Start generation']"))
    if not start_btn:
        raise RuntimeError("Start generation button not found")
    start_btn[0].click()
    rec.update(paid=True, credits=price)
    with open(LEDGER, "a", encoding="utf-8") as f:
        f.write(json.dumps({"t": time.strftime("%Y-%m-%dT%H:%M:%S"), "song": SONG,
                            "clip": clip_id, "credits": price, "via": "patchright"}) + "\n")
    say(f"Clip {clip_id}: generation clicked ({seconds}s, ~{price} credits)... waiting for tile")
    
    # Verify tile started
    for _i in range(15):
        time.sleep(2)
        if page.locator("flow-video-tile").count() > before_tiles:
            break
        sb = visible(page.locator("button[aria-label='Start generation']"))
        if sb and not sb[0].is_disabled() and _i == 7:
            say("Re-clicking start generation button...")
            sb[0].click()
    else:
        say("Note: tile count did not increase immediately, checking first tile...")
        
    say(f"Clip {clip_id}: tile active, waiting for completion...")
    wait_tile(page)
    rec.update(bytes=save(page, out), status="saved", seconds=seconds)
    say(f"Clip {clip_id}: saved successfully ({rec['bytes'] / 1024 / 1024:.2f} MB)")
    return rec

def main():
    mv_path = os.path.join(SONG_DIR, "musicvideo.json")
    mv = json.load(open(mv_path, encoding="utf-8"))
    url = os.environ.get("PROJECT_URL") or mv.get("flow", {}).get(f"project_url_{ACCOUNT}") or mv.get("flow", {}).get("project_url", "https://flow.google.com/project/a8aa2c07-c3ad-4da3-9b7e-5712903c758e")
    plan_path = os.path.join(SONG_DIR, "plan", "take6.shots.json")
    plan = json.load(open(plan_path, encoding="utf-8"))
    clips = plan.get("clips", [])
    
    # Missing clips
    missing = [c for c in clips if not os.path.isfile(os.path.join(CLIPS_DIR, c["id"] + ".mp4"))]
    say(f"Target Song: {SONG} | Missing clips: {len(missing)} of {len(clips)} | Max this run: {MAX}")
    if not missing:
        say("All clips already generated!")
        return 0

    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(USER_DATA, channel="chrome", headless=True,
                                                   accept_downloads=True)
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        say(f"Loading project: {url}")
        page.goto(url, timeout=45000)
        page.wait_for_load_state("domcontentloaded")
        time.sleep(random.uniform(5, 8))
        good, labels = account_ok(page)
        say(f"Account check: {good} (labels: {labels})")
        if not good:
            say(f"ERROR: Expected {EMAIL}, got {labels}")
            ctx.close()
            return 1

        made = 0
        for clip in missing:
            if made >= MAX:
                break
            rec = dict(song=SONG, clip=clip["id"], paid=False, account=ACCOUNT)
            try:
                make_clip(page, clip, rec)
            except Flagged as e:
                say(f"Rate-limit cooldown notice: {e}. Pausing 75s...")
                time.sleep(75)
                try:
                    page.reload()
                    page.wait_for_load_state("domcontentloaded")
                    time.sleep(6)
                    check_flagged(page)
                    say("Notice cleared! Retrying clip...")
                    make_clip(page, clip, rec)
                except Exception as e2:
                    say(f"Failed after cooldown on {clip['id']}: {e2}. Stopping run to be safe.")
                    break
            except Exception as e:
                say(f"Error on {clip['id']}: {e}")
                rec["status"] = f"ERROR: {e}"
                err_str = str(e).lower()
                if "insufficient credits" in err_str or "unusual activity" in err_str:
                    say("Stopping: account quota / rate limit hit.")
                    break
            if rec.get("status") == "saved":
                made += 1
                if made < MAX:
                    pause = random.uniform(*PAUSE)
                    say(f"Sleeping {pause:.1f}s before next clip...")
                    time.sleep(pause)
        say(f"Run completed: {made} clips made.")
        ctx.close()
    return 0

if __name__ == "__main__":
    sys.exit(main())
