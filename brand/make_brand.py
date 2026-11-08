"""Nepali Rhyme Hub brand kit generator (2026-11-07). One source of truth for every brand picture.

    python brand/make_brand.py            -> brand/logo.png, profile.png, watermark.png, banner.png, entry.png, exit.png

Graphics are drawn with Pillow; every Nepali word is set by libass (ffmpeg, complex shaping) because Pillow on this
PC has no Devanagari shaping (no libraqm). Colours and sizes come from BRAND_GUIDE.md.
"""
from __future__ import annotations

import math
import random
import subprocess
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = Path(__file__).resolve().parent
NIGHT, NIGHT_DEEP = (20, 35, 75), (8, 14, 38)
MARIGOLD, GOLD, CREAM = (247, 162, 27), (255, 209, 102), (255, 244, 224)
CRIMSON, FLAME = (200, 16, 46), (255, 120, 20)
DEVANAGARI_FONT, LATIN_FONT = "Nirmala UI", "Segoe UI"


# ---------- text (libass) ----------

def _ass_colour(rgb: tuple[int, int, int]) -> str:
    r, g, b = rgb
    return f"&H00{b:02X}{g:02X}{r:02X}"


def text_layer(width: int, height: int, items: list[dict]) -> Image.Image:
    """RGBA picture with each item {text, size, colour, x, y, align (ass numpad, default 5), font, outline, bold}."""
    def script(mask: bool) -> str:
        head = ["[Script Info]", "ScriptType: v4.00+", f"PlayResX: {width}", f"PlayResY: {height}", "WrapStyle: 2", "",
                "[V4+ Styles]",
                "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, "
                "Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, "
                "Alignment, MarginL, MarginR, MarginV, Encoding"]
        events = ["", "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
        for i, it in enumerate(items):
            fill = (255, 255, 255) if mask else it["colour"]
            line = (255, 255, 255) if mask else it.get("line", NIGHT_DEEP)
            head.append(f"Style: S{i},{it.get('font', DEVANAGARI_FONT)},{it['size']},{_ass_colour(fill)},&H000000FF,"
                        f"{_ass_colour(line)},&H00000000,{-1 if it.get('bold', True) else 0},0,0,0,100,100,"
                        f"{it.get('spacing', 0)},0,1,{it.get('outline', 0)},0,{it.get('align', 5)},0,0,0,1")
            events.append(f"Dialogue: 0,0:00:00.00,0:00:05.00,S{i},,0,0,0,,{{\\pos({it['x']},{it['y']})}}{it['text']}")
        return "\n".join(head + events) + "\n"

    planes = []
    with tempfile.TemporaryDirectory(prefix="nrh-brand-") as work:
        for mask in (False, True):
            (Path(work) / "t.ass").write_text(script(mask), encoding="utf-8")
            subprocess.run(["ffmpeg", "-v", "error", "-nostdin", "-y", "-f", "lavfi", "-i",
                            f"color=c=black:s={width}x{height}", "-vf", "ass=t.ass:shaping=complex",
                            "-frames:v", "1", "out.png"], cwd=work, check=True)
            planes.append(np.asarray(Image.open(Path(work) / "out.png").convert("RGB"), dtype=np.float32))
    colour, mask = planes
    alpha = mask.max(axis=2, keepdims=True)
    rgb = np.clip(colour * 255.0 / np.maximum(alpha, 1.0), 0, 255)          # undo the blend onto black
    return Image.fromarray(np.concatenate([rgb, alpha], axis=2).astype(np.uint8), "RGBA")


# ---------- the emblem ----------

def _note(d: ImageDraw.ImageDraw, x: float, y: float, s: float, colour) -> None:
    d.ellipse([x - s * 0.55, y - s * 0.38, x + s * 0.55, y + s * 0.38], fill=colour)
    d.rectangle([x + s * 0.42, y - s * 2.2, x + s * 0.58, y], fill=colour)
    d.polygon([(x + s * 0.58, y - s * 2.2), (x + s * 1.35, y - s * 1.6), (x + s * 0.58, y - s * 1.5)], fill=colour)


def emblem(size: int, background: bool = True) -> Image.Image:
    """Round badge: night-blue disc, marigold ring, a golden diyo with its flame and two music notes."""
    big = size * 4
    im = Image.new("RGBA", (big, big), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    c = big / 2
    if background:
        d.ellipse([0, 0, big - 1, big - 1], fill=MARIGOLD + (255,))
        d.ellipse([big * 0.055, big * 0.055, big * 0.945, big * 0.945], fill=NIGHT + (255,))
        d.ellipse([big * 0.085, big * 0.085, big * 0.915, big * 0.915], outline=GOLD + (255,), width=int(big * 0.008))
    glow = Image.new("RGBA", (big, big), (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse([c - big * 0.24, c - big * 0.30, c + big * 0.24, c + big * 0.18], fill=FLAME + (150,))
    im.alpha_composite(glow.filter(ImageFilter.GaussianBlur(big * 0.06)))
    d = ImageDraw.Draw(im)
    # flame: a teardrop of two layers
    for scale, colour in ((1.0, FLAME), (0.62, GOLD), (0.30, CREAM)):
        w, top, base = big * 0.085 * scale, c - big * 0.29 * scale - big * 0.02, c + big * 0.02
        pts = [(c + w * math.sin(t) * (1 - (1 - math.cos(t)) * 0.15), base - (top - base) * -0.5 * (1 - math.cos(t)) - 0)
               for t in np.linspace(0, 2 * math.pi, 60)]
        pts = [(c + w * math.sin(t), base - (base - top) * (0.5 - 0.5 * math.cos(t)) ** 1.6) for t in np.linspace(0, 2 * math.pi, 80)]
        d.polygon(pts, fill=colour + (255,))
    # diyo bowl
    d.chord([c - big * 0.22, c - big * 0.04, c + big * 0.22, c + big * 0.24], 0, 180, fill=MARIGOLD + (255,))
    d.chord([c - big * 0.22, c - big * 0.04, c + big * 0.22, c + big * 0.24], 0, 180, outline=GOLD + (255,), width=int(big * 0.012))
    d.ellipse([c - big * 0.22, c + big * 0.065, c + big * 0.22, c + big * 0.115], fill=CRIMSON + (255,))
    d.rectangle([c - big * 0.07, c + big * 0.20, c + big * 0.07, c + big * 0.25], fill=GOLD + (255,))
    d.ellipse([c - big * 0.13, c + big * 0.235, c + big * 0.13, c + big * 0.28], fill=MARIGOLD + (255,))
    _note(d, c - big * 0.30, c - big * 0.02, big * 0.055, CREAM + (255,))
    _note(d, c + big * 0.25, c - big * 0.14, big * 0.045, GOLD + (255,))
    for sx, sy, r in ((-0.18, -0.30, 0.012), (0.20, -0.30, 0.009), (-0.30, -0.22, 0.008), (0.31, 0.02, 0.010)):
        d.ellipse([c + big * (sx - r), c + big * (sy - r), c + big * (sx + r), c + big * (sy + r)], fill=GOLD + (255,))
    return im.resize((size, size), Image.LANCZOS)


# ---------- Kathmandu night skyline ----------

def _pagoda(d, x, base, w, tiers, colour):
    y = base
    d.rectangle([x - w * 0.22, y - w * 0.35, x + w * 0.22, y], fill=colour)
    y -= w * 0.35
    for i in range(tiers):
        tw = w * (1 - i * 0.22)
        d.polygon([(x - tw / 2, y), (x + tw / 2, y), (x + tw * 0.28, y - w * 0.16), (x - tw * 0.28, y - w * 0.16)], fill=colour)
        y -= w * 0.16
        d.rectangle([x - tw * 0.2, y - w * 0.10, x + tw * 0.2, y], fill=colour)
        y -= w * 0.10
    d.polygon([(x - w * 0.04, y), (x + w * 0.04, y), (x, y - w * 0.18)], fill=colour)
    return y


def _stupa(d, x, base, w, colour):
    d.chord([x - w / 2, base - w * 0.55, x + w / 2, base + w * 0.45], 180, 360, fill=colour)
    d.rectangle([x - w * 0.12, base - w * 0.62, x + w * 0.12, base - w * 0.48], fill=colour)
    d.polygon([(x - w * 0.10, base - w * 0.62), (x + w * 0.10, base - w * 0.62), (x, base - w * 1.05)], fill=colour)


def skyline(width: int, height: int, base: int, scale: float, seed: int = 7) -> Image.Image:
    """Transparent strip: Himalaya, hills, pagodas and a stupa in silhouette, with diyo lights and light strings."""
    rnd = random.Random(seed)
    im = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    peaks = [(0, base - 210 * scale)]
    for x in range(0, width + 200, int(160 * scale)):
        peaks.append((x, base - (200 + rnd.randint(0, 150)) * scale))
    d.polygon(peaks + [(width, base), (0, base)], fill=(70, 96, 150, 255))
    for x, y in peaks[1:]:
        d.polygon([(x - 40 * scale, y + 34 * scale), (x, y), (x + 40 * scale, y + 34 * scale)], fill=(232, 240, 255, 255))
    hills = [(0, base - 90 * scale)] + [(x, base - (70 + rnd.randint(0, 50)) * scale) for x in range(0, width + 300, int(260 * scale))]
    d.polygon(hills + [(width, base), (0, base)], fill=(30, 45, 90, 255))
    city = (12, 20, 48, 255)
    tops = []
    x = 40 * scale
    while x < width:
        kind = rnd.random()
        if kind < 0.42:
            top = _pagoda(d, x, base, (110 + rnd.randint(0, 70)) * scale, rnd.choice((2, 3, 3, 5)), city)
            tops.append((x, top))
            x += 170 * scale
        elif kind < 0.5:
            _stupa(d, x, base, 150 * scale, city)
            tops.append((x, base - 160 * scale))
            x += 190 * scale
        else:
            h = (50 + rnd.randint(0, 70)) * scale
            w = (70 + rnd.randint(0, 60)) * scale
            d.rectangle([x - w / 2, base - h, x + w / 2, base], fill=city)
            for wx in range(int(x - w / 2 + 12 * scale), int(x + w / 2 - 8 * scale), int(22 * scale)):
                if rnd.random() < 0.6:
                    d.rectangle([wx, base - h + 14 * scale, wx + 9 * scale, base - h + 26 * scale], fill=GOLD + (255,))
            tops.append((x, base - h))
            x += w + 30 * scale
    glow = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    g = ImageDraw.Draw(glow)
    for (x1, y1), (x2, y2) in zip(tops, tops[1:]):                     # light strings between the roofs
        for i in range(1, 12):
            t = i / 12
            px, py = x1 + (x2 - x1) * t, y1 + (y2 - y1) * t + math.sin(math.pi * t) * 28 * scale
            r = 3.2 * scale
            g.ellipse([px - r * 3, py - r * 3, px + r * 3, py + r * 3], fill=GOLD + (90,))
            d.ellipse([px - r, py - r, px + r, py + r], fill=(GOLD if i % 2 else MARIGOLD) + (255,))
    for _ in range(int(width / 9)):                                     # diyo lamps along the ground
        px, r = rnd.uniform(0, width), 2.6 * scale
        py = base - rnd.uniform(2, 8) * scale
        g.ellipse([px - r * 4, py - r * 4, px + r * 4, py + r * 4], fill=FLAME + (80,))
        d.ellipse([px - r, py - r, px + r, py + r], fill=GOLD + (255,))
    out = glow.filter(ImageFilter.GaussianBlur(6 * scale))
    out.alpha_composite(im)
    return out


def night_sky(width: int, height: int, seed: int = 3) -> Image.Image:
    rnd = random.Random(seed)
    y = np.linspace(0, 1, height)[:, None, None]
    top, bottom = np.array(NIGHT_DEEP, np.float32), np.array((44, 62, 120), np.float32)
    sky = Image.fromarray(np.broadcast_to(top + (bottom - top) * y, (height, width, 3)).astype(np.uint8), "RGB").convert("RGBA")
    d = ImageDraw.Draw(sky)
    for _ in range(int(width * height / 9000)):
        x, yy, r = rnd.uniform(0, width), rnd.uniform(0, height * 0.75), rnd.choice((1, 1, 1.5, 2))
        d.ellipse([x - r, yy - r, x + r, yy + r], fill=(255, 255, 255, rnd.randint(120, 255)))
    return sky


# ---------- the assets ----------

def wordmark(width: int, height: int, cx: int, cy: int, scale: float, tagline: bool = True) -> Image.Image:
    items = [dict(text="नेपाली राइम हब", size=int(150 * scale), colour=MARIGOLD, x=cx, y=int(cy - 70 * scale),
                  outline=int(6 * scale), align=4),
             dict(text="NEPALI RHYME HUB", size=int(58 * scale), colour=CREAM, x=cx + int(6 * scale),
                  y=int(cy + 45 * scale), font=LATIN_FONT, spacing=int(10 * scale), outline=int(3 * scale), align=4)]
    if tagline:
        items.append(dict(text="गाऔँ · नाचौँ · सिकौँ!", size=int(66 * scale), colour=GOLD, x=cx + int(4 * scale),
                          y=int(cy + 125 * scale), outline=int(4 * scale), align=4))
    return text_layer(width, height, items)


def make_banner() -> None:
    w, h = 2560, 1440                                   # safe area for every device: centre 1546 x 423 (y 508-931)
    im = night_sky(w, h)
    ground = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    gd = ImageDraw.Draw(ground)
    gd.rectangle([0, 990, w, h], fill=NIGHT_DEEP + (255,))
    rnd = random.Random(5)
    for _ in range(420):                                 # lamp reflections on the ground (seen on TV only)
        x, y = rnd.uniform(0, w), rnd.uniform(1000, h)
        r = 1.5 + (y - 990) / 160
        gd.ellipse([x - r, y - r * 0.6, x + r, y + r * 0.6], fill=GOLD + (rnd.randint(60, 200),))
    im.alpha_composite(ground)
    im.alpha_composite(skyline(w, h, base=990, scale=1.15))
    band = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(band).rounded_rectangle([600, 530, 1960, 860], radius=60, fill=NIGHT_DEEP + (150,))
    im.alpha_composite(band.filter(ImageFilter.GaussianBlur(18)))
    badge = emblem(300)
    im.alpha_composite(badge, (640, 545))
    im.alpha_composite(wordmark(w, h, 990, 690, 1.0))
    im.convert("RGB").save(HERE / "banner.png", optimize=True)


def make_cards() -> None:
    w, h = 1920, 1080
    entry = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    pill = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(pill).rounded_rectangle([36, 32, 640, 186], radius=77, fill=NIGHT_DEEP + (200,))
    entry.alpha_composite(pill)
    entry.alpha_composite(emblem(140), (44, 39))
    entry.alpha_composite(text_layer(w, h, [
        dict(text="नेपाली राइम हब", size=62, colour=MARIGOLD, x=200, y=88, outline=3, align=4),
        dict(text="NEPALI RHYME HUB", size=26, colour=CREAM, x=203, y=140, font=LATIN_FONT, spacing=5, outline=2, align=4)]))
    entry.save(HERE / "entry.png", optimize=True)

    card = Image.new("RGBA", (w, h), NIGHT_DEEP + (215,))
    card.alpha_composite(skyline(w, h, base=h, scale=0.8, seed=11))
    card.alpha_composite(emblem(300), (w // 2 - 150, 120))
    card.alpha_composite(text_layer(w, h, [
        dict(text="फेरि भेटौँला!", size=130, colour=MARIGOLD, x=w // 2, y=560, outline=6),
        dict(text="अर्को गीतमा सँगै गाऔँ, नाचौँ, सिकौँ!", size=58, colour=CREAM, x=w // 2, y=670, outline=3),
        dict(text="NEPALI RHYME HUB  ·  @NepaliRhymeHub", size=40, colour=GOLD, x=w // 2, y=750, font=LATIN_FONT,
             spacing=4, outline=2)]))
    card.save(HERE / "exit.png", optimize=True)


def main() -> None:
    emblem(512).save(HERE / "logo.png", optimize=True)          # renderer watermark (bottom-right of every video)
    profile = Image.new("RGBA", (800, 800), NIGHT + (255,))
    profile.alpha_composite(emblem(800))
    profile.convert("RGB").save(HERE / "profile.png", optimize=True)
    emblem(150).save(HERE / "watermark.png", optimize=True)
    make_banner()
    make_cards()
    for name in ("logo.png", "profile.png", "watermark.png", "banner.png", "entry.png", "exit.png"):
        print(name, Image.open(HERE / name).size, f"{(HERE / name).stat().st_size // 1024} KB")


def retired() -> None:
    """v1 (diyo) kit, superseded on 2026-11-08 by the Puntu logo: running it would overwrite logo.png, banner.png and
    bring back an entry card, which Sanam does not want. Its text_layer() is still used by brand_clips.py."""
    raise SystemExit("make_brand.py is retired: use brand_clips.py (banner, exit clip) and brand/logo.png (Puntu).")


if __name__ == "__main__":
    retired()
    main()
