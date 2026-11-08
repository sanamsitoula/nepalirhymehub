"""Nepali Rhyme Hub brand assets made in Google Flow / Flow Music (Sanam, 2026-11-07).

    python -I brand/flow_brand.py art     logos A, B, C + banner art (Flow free image model, 0 credits)
    python -I brand/flow_brand.py music   the sonic logo / jingle (Flow Music, free)
    python -I brand/flow_brand.py video   entry (4 s) and exit (8 s) clips with the chosen logo (Flow credits, ~20);
                                          only after Sanam writes A, B or C into brand/flow/chosen_logo.txt
Prompts and the concept: brand/LOGO_PROMPTS.md

Everything lands in brand/flow/. Uses the subu-os music-video browser profile, lock and kill switch, like every
pipeline stage. `make_brand.py compose` then puts the Nepali name on top (AI never draws text).
"""
from __future__ import annotations

import os
import sys
from dataclasses import replace
from pathlib import Path

REPO = Path(r"D:\claude_project\subu-os")
sys.path.insert(0, str(REPO))
from subu.musicvideo import browser, flowclips, flowmusic, pipeline, stages  # noqa: E402

OUT = Path(__file__).resolve().parent / "flow"
CHANNEL_ID = "nepali-rhyme-hub"

PUNTU = ("Puntu, a cute baby red panda: fluffy rust-red fur, white face markings, a ringed bushy tail, big friendly "
         "dark eyes, a small green scarf")
LOGO_BASE = ("Mascot logo for a Nepali children's music channel, centred with lots of empty space around it, on a plain "
             "flat deep night-blue background. A rounded badge whose top edge is a row of three snowy Himalaya peaks (the "
             "middle one a fishtail peak), a warm marigold-orange sunrise glowing behind the peaks, a night-blue sky with "
             "two tiny stars. In front of the mountains sits " + PUNTU + ", with a big happy open-mouth smile. He plays a "
             "small Nepali madal drum lying across his lap with both paws, and three music notes (marigold, crimson, sky "
             "blue) bounce up out of the drum. Under the badge, an empty blank marigold ribbon banner with nothing written "
             "on it. Glossy soft 3D mascot-logo style, thick clean outlines, simple bold shapes that still read at 98 "
             "pixels, high contrast, joyful. No text, no letters, no words, no numbers, no watermark, no signature. ")
LOGOS = {"A": LOGO_BASE + "Round badge, the mountains inside a thick marigold ring.",
         "B": LOGO_BASE + "Shield-shaped badge, the snowy peaks rise above the badge edge, Puntu waving one paw.",
         "C": LOGO_BASE + "Die-cut sticker style with a thick white outline around the whole badge, Puntu winking."}
BANNER = ("Wide panoramic banner illustration, golden hour turning to dusk over a Nepali hill village and the Kathmandu "
          "Valley: terraced green fields, Newar pagoda temple roofs and carved brick houses, festive strings of warm "
          "golden lights, small diyo lamps on rooftops, snowy Himalaya peaks glowing pink and gold, the first stars in a "
          "deep-blue sky. On the left third " + PUNTU + " sits on a hilltop rock playing a madal, music notes floating. "
          "The middle band of the picture is calm and darker, kept empty for a title. Premium 3D children's "
          "animated-film look, night blue and marigold colours. No text, no letters, no logo, no people.")
ENTRY = ("Use the reference logo. Deep night-blue sky, a soft marigold sunrise glow. First second: the snowy Himalaya "
         "peaks of the badge rise up from the bottom. Then Puntu the baby red panda pops up in front of them and hits "
         "his madal twice, each hit a burst of golden sparkles and one bouncing music note (marigold, then crimson). "
         "Then the badge ring draws itself around him, the blank ribbon unrolls underneath and Puntu smiles at the "
         "camera; hold with notes floating and a gentle twinkle. Static centred camera, smooth bouncy animation, "
         "joyful, child-friendly. No text, no letters.")
EXIT = ("Use the reference logo. Dusk over a small Nepali hill village and pagoda roofs with twinkling warm lights, "
        "snowy peaks glowing pink, first stars. Puntu the baby red panda sits on top of the logo badge in the upper "
        "centre, waves goodbye with one paw, gives a small happy yawn and hugs his madal; music notes drift slowly "
        "upward and become stars. Gentle slow push-in, calm and warm. The lower third of the frame stays empty and "
        "dark for a title. No text, no letters.")
JINGLE = """Please make a short 30-second channel jingle (a sonic logo) for "Nepali Rhyme Hub", a Nepali children's \
music channel, whose mascot is Puntu the baby red panda who plays the madal. Bright, joyful Nepali folk-pop, 110 BPM, D major: two deep madal hits "dhin-ta!" right at the start, a small temple bell (ghanti), a \
sparkling 4-note bansuri signature motif that opens and closes it, xylophone sparkles, a happy children's choir singing \
in Nepali with clear Nepali pronunciation. It starts at once with the madal hit, the bell and the bansuri motif; the \
children sing the lines below; it ends on the bansuri motif and one bell. Unique and simple, not like any existing \
song or jingle. No English words, sing only these Nepali lines:

[Intro]
नेपाली राइम हब!

[Chorus 1]
गाऔँ, नाचौँ, सिकौँ!
नेपाली राइम हब!

[Outro]
नेपाली राइम हब!
"""


def _setup():
    cfg = pipeline.load_config(REPO)
    channel = cfg.channels[CHANNEL_ID]
    check = pipeline.guard(REPO, channel)
    check()
    pipeline.require_machine(channel, REPO)
    return cfg, channel, check


def art() -> None:
    cfg, channel, check = _setup()
    free = replace(cfg, flow=replace(cfg.flow, reference_max_credits=0))         # a priced image stops it
    hold, switch = stages._session(REPO, channel, "nepalirhymehub-brand-art")
    try:
        with hold, browser.open_context(stages._profile(REPO, channel), cfg.browser) as context:
            page, url = flowclips.open_project(context, free.flow, cfg.browser, "", "Brand - Nepali Rhyme Hub",
                                               guard=lambda home: flowclips.require_account(home, free.flow))
            flowclips.require_account(page, free.flow)
            (OUT).mkdir(parents=True, exist_ok=True)
            (OUT / "project_url.txt").write_text(url + "\n", encoding="utf-8")
            chosen = OUT / "chosen_logo.txt"               # once Sanam has picked, the other logos are not drawn
            keys = [chosen.read_text(encoding="utf-8").strip().upper()] if chosen.is_file() else list(LOGOS)
            jobs = [(f"logo_{key}", LOGOS[key]) for key in keys] + [("banner_art", BANNER)]
            for name, prompt in jobs:
                if (OUT / f"{name}.jpg").is_file():
                    print(f"{name}: already there", flush=True)
                    continue
                check()
                title = flowclips.make_reference(page, free.flow, prompt, OUT / f"{name}.jpg", check)
                (OUT / f"{name}.title.txt").write_text(title + "\n", encoding="utf-8")
                print(f"{name}: '{title}' saved", flush=True)
    finally:
        switch.unregister(os.getpid())


def music() -> None:
    cfg, channel, check = _setup()
    hold, switch = stages._session(REPO, channel, "nepalirhymehub-brand-music")
    try:
        with hold, browser.open_context(stages._profile(REPO, channel), cfg.browser) as context:
            page = flowmusic.open_session(context, cfg.flowmusic, "")
            title = flowmusic.make_take(page, cfg.flowmusic, cfg.browser, JINGLE, check)
            OUT.mkdir(parents=True, exist_ok=True)
            flowmusic.download_song(page, title, cfg.flowmusic.download_format, OUT / "jingle.wav")
            flowmusic.download_stems(page, title, OUT / "jingle.stems")
            (OUT / "jingle.session.txt").write_text(page.url + "\n" + title + "\n", encoding="utf-8")
            print(f"jingle '{title}' saved to brand/flow/jingle.wav", flush=True)
    finally:
        switch.unregister(os.getpid())


def video() -> None:
    cfg, channel, check = _setup()
    url = (OUT / "project_url.txt").read_text(encoding="utf-8").strip()
    chosen = OUT / "chosen_logo.txt"                      # Sanam picks A, B or C first: the clips cost credits
    if not chosen.is_file():
        print("video: waiting for Sanam to pick a logo (brand/flow/chosen_logo.txt = A, B or C); nothing generated")
        return
    key = chosen.read_text(encoding="utf-8").strip().upper()
    logo_title = (OUT / f"logo_{key}.title.txt").read_text(encoding="utf-8").strip()
    hold, switch = stages._session(REPO, channel, "nepalirhymehub-brand-video")
    try:
        with hold, browser.open_context(stages._profile(REPO, channel), cfg.browser) as context:
            page, _ = flowclips.open_project(context, cfg.flow, cfg.browser, url, "Brand - Nepali Rhyme Hub",
                                             guard=lambda home: flowclips.require_account(home, cfg.flow))
            flowclips.require_account(page, cfg.flow)
            for name, prompt, seconds in (("entry", ENTRY, 4), ("exit", EXIT, 8)):
                target = OUT / f"{name}.mp4"
                if target.is_file():
                    print(f"{name}: already there", flush=True)
                    continue
                check()
                tile = flowclips.generate_clip(page, cfg.flow, cfg.browser, prompt, seconds, logo_title, check)
                flowclips.fetch(flowclips.video_url(page, tile), target, page=page)
                print(f"{name}: saved brand/flow/{name}.mp4", flush=True)
    finally:
        switch.unregister(os.getpid())


def recover() -> None:
    """Save entry/exit clips that Flow made but that were not downloaded: the newest video tile is the exit clip,
    the one before it the entry clip (video() makes them in that order). Nothing is generated."""
    cfg, channel, check = _setup()
    url = (OUT / "project_url.txt").read_text(encoding="utf-8").strip()
    hold, switch = stages._session(REPO, channel, "nepalirhymehub-brand-recover")
    try:
        with hold, browser.open_context(stages._profile(REPO, channel), cfg.browser) as context:
            page, _ = flowclips.open_project(context, cfg.flow, cfg.browser, url, "Brand - Nepali Rhyme Hub")
            names = iter(("exit", "entry"))
            for _tile, address in flowclips.each_tile(page, check):
                name = next(names, None)
                if name is None:
                    break
                flowclips.fetch(address, OUT / f"{name}.mp4", page=page)
                print(f"{name}: recovered to brand/flow/{name}.mp4", flush=True)
    finally:
        switch.unregister(os.getpid())


if __name__ == "__main__":
    {"art": art, "music": music, "video": video, "recover": recover}[sys.argv[1]]()
