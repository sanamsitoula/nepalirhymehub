"""Write the channel name onto the Flow brand clips and the banner (Sanam, 2026-11-08). AI never draws our text.

    python -I brand/brand_clips.py entry    brand/flow/entry.mp4  -> brand/entry_named.mp4  (name pops onto the ribbon)
    python -I brand/brand_clips.py exit     brand/flow/exit.mp4   -> brand/exit_named.mp4   (name plate covers the
                                            badge Flow drew under Puntu, following the camera push-in)
    python -I brand/brand_clips.py banner   brand/flow/banner_art.jpg + logo -> brand/banner.png (2560 x 1440)
    python -I brand/brand_clips.py all
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, str(Path(__file__).resolve().parent))
from make_brand import CREAM, GOLD, LATIN_FONT, MARIGOLD, NIGHT, NIGHT_DEEP, text_layer  # noqa: E402

HERE = Path(__file__).resolve().parent
FLOW = HERE / "flow"
NAME_NE, NAME_EN, TAGLINE = "नेपाली राइम हब", "NEPALI RHYME HUB", "गाऔँ · नाचौँ · सिकौँ!"
FPS = 24

# Where Flow's drawn badge sits in exit.mp4 (frame -> x0, y0, x1, y1), measured by hand on a pixel grid.
EXIT_BADGE = {0: (560, 222, 732, 320), 24: (550, 285, 740, 385), 48: (540, 335, 755, 445),
              72: (525, 390, 780, 525), 96: (505, 425, 800, 595), 120: (495, 475, 820, 645),
              144: (490, 490, 830, 675), 168: (485, 495, 840, 690), 191: (485, 495, 835, 700)}
PLATE_PAD = 0.07                                         # cover a little more than the badge on every side
POP_FRAMES = 8                                           # the plate lands with a small bounce

ENTRY_RIBBON_CENTRE = (640, 574)                         # the flat front of the ribbon once it has unrolled
ENTRY_TEXT_START_S = 3.2


def _encode(frames_dir: Path, audio_from: Path, dest: Path) -> None:
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", str(FPS), "-i", str(frames_dir / "f%03d.png"),
                    "-i", str(audio_from), "-map", "0:v", "-map", "1:a?", "-c:v", "libx264", "-crf", "17",
                    "-preset", "slow", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", str(dest)],
                   check=True)


def _frames(video: Path, work: Path) -> list[Path]:
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(video), str(work / "f%03d.png")], check=True)
    return sorted(work.glob("f*.png"))


def _interp(table: dict[int, tuple], n: int) -> tuple[float, ...]:
    keys = sorted(table)
    if n <= keys[0]:
        return table[keys[0]]
    for a, b in zip(keys, keys[1:]):
        if n <= b:
            t = (n - a) / (b - a)
            return tuple(pa + (pb - pa) * t for pa, pb in zip(table[a], table[b]))
    return table[keys[-1]]


def name_plate(width: int = 900, height: int = 520) -> Image.Image:
    """Night Blue badge with a Marigold ring and the channel name: our replacement for Flow's misspelled badge."""
    plate = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    d = ImageDraw.Draw(plate)
    d.rounded_rectangle([8, 8, width - 8, height - 8], radius=height // 2 - 8, fill=MARIGOLD + (255,))
    d.rounded_rectangle([34, 34, width - 34, height - 34], radius=height // 2 - 34, fill=NIGHT + (255,))
    rng = np.random.default_rng(4)
    for _ in range(26):                                   # a few small stars inside the badge
        x, y = rng.uniform(110, width - 110), rng.uniform(60, height - 60)
        if 160 < y < height - 120:
            continue
        r = rng.uniform(2, 4.5)
        d.ellipse([x - r, y - r, x + r, y + r], fill=GOLD + (220,))
    plate.alpha_composite(text_layer(width, height, [
        dict(text=NAME_NE, size=150, colour=MARIGOLD, x=width // 2, y=height // 2 - 40, outline=6),
        dict(text=NAME_EN, size=54, colour=CREAM, x=width // 2, y=height // 2 + 95, font=LATIN_FONT, spacing=9,
             outline=3)]))
    return plate


def make_exit() -> Path:
    plate = name_plate()
    dest = HERE / "exit_named.mp4"
    with tempfile.TemporaryDirectory(prefix="nrh-exit-") as tmp:
        work = Path(tmp)
        for n, path in enumerate(_frames(FLOW / "exit.mp4", work)):
            x0, y0, x1, y1 = _interp(EXIT_BADGE, n)
            w, h = (x1 - x0) * (1 + 2 * PLATE_PAD), (y1 - y0) * (1 + 2 * PLATE_PAD)
            w = max(w, h * plate.width / plate.height)    # keep the plate's shape; never narrower than the badge
            h = w * plate.height / plate.width
            if n < POP_FRAMES:                            # lands slightly big and settles: always covers the badge
                grow = 1 + 0.12 * (1 - n / POP_FRAMES)
                w, h = w * grow, h * grow
            cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
            frame = Image.open(path).convert("RGBA")
            shadow = Image.new("RGBA", frame.size, (0, 0, 0, 0))
            ImageDraw.Draw(shadow).rounded_rectangle(
                [cx - w / 2, cy - h / 2 + 6, cx + w / 2, cy + h / 2 + 10], radius=h / 2, fill=(0, 0, 0, 120))
            frame.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(8)))
            sized = plate.resize((round(w), round(h)), Image.LANCZOS)
            frame.alpha_composite(sized, (round(cx - w / 2), round(cy - h / 2)))
            frame.convert("RGB").save(path)
        _encode(work, FLOW / "exit.mp4", dest)
    return dest


def _entry_ass() -> str:
    cx, cy = ENTRY_RIBBON_CENTRE
    start = f"0:00:{ENTRY_TEXT_START_S:05.2f}"
    head = ("[Script Info]\nScriptType: v4.00+\nPlayResX: 1280\nPlayResY: 720\nWrapStyle: 2\n\n[V4+ Styles]\n"
            "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, "
            "Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, "
            "MarginL, MarginR, MarginV, Encoding\n"
            "Style: NE,Nirmala UI,70,&H004B2314,&H000000FF,&H00E0F4FF,&H00000000,-1,0,0,0,100,100,0,0,1,2,0,5,0,0,0,1\n"
            "Style: EN,Segoe UI,24,&H002E10C8,&H000000FF,&H00E0F4FF,&H00000000,-1,0,0,0,100,100,6,0,1,1,0,5,0,0,0,1\n\n"
            "[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")
    pop = r"\fscx40\fscy40\t(0,180,\fscx112\fscy112)\t(180,300,\fscx100\fscy100)"
    return head + (f"Dialogue: 0,{start},0:00:09.00,NE,,0,0,0,,{{\\pos({cx},{cy - 14})\\fad(120,0){pop}}}{NAME_NE}\n"
                   f"Dialogue: 0,{start},0:00:09.00,EN,,0,0,0,,{{\\pos({cx},{cy + 34})\\fad(250,0)}}{NAME_EN}\n")


def make_entry() -> Path:
    dest = HERE / "entry_named.mp4"
    with tempfile.TemporaryDirectory(prefix="nrh-entry-") as tmp:
        (Path(tmp) / "t.ass").write_text(_entry_ass(), encoding="utf-8")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(FLOW / "entry.mp4"), "-vf",
                        "ass=t.ass:shaping=complex", "-c:v", "libx264", "-crf", "17", "-preset", "slow",
                        "-pix_fmt", "yuv420p", "-c:a", "copy", str(dest.resolve())], cwd=tmp, check=True)
    return dest


def make_banner() -> Path:
    """2560 x 1440 from the Flow banner art. Logo + name sit inside the 1546 x 423 safe area (seen on every device)."""
    w, h = 2560, 1440
    art = Image.open(FLOW / "banner_art.jpg").convert("RGB").resize((w, h), Image.LANCZOS).convert("RGBA")
    band = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(band).rounded_rectangle([600, 520, 2110, 920], radius=80, fill=NIGHT_DEEP + (165,))
    art.alpha_composite(band.filter(ImageFilter.GaussianBlur(22)))
    logo = Image.open(FLOW / "logo_A_transparent.png").convert("RGBA")
    size = 390
    logo = logo.resize((round(logo.width * size / logo.height), size), Image.LANCZOS)
    art.alpha_composite(logo, (650, 525))
    tx = 650 + logo.width + 50
    art.alpha_composite(text_layer(w, h, [
        dict(text=NAME_NE, size=170, colour=MARIGOLD, x=tx, y=640, outline=7, align=4),
        dict(text=NAME_EN, size=64, colour=CREAM, x=tx + 8, y=770, font=LATIN_FONT, spacing=11, outline=3, align=4),
        dict(text=TAGLINE, size=74, colour=GOLD, x=tx + 4, y=860, outline=4, align=4)]))
    dest = HERE / "banner.png"
    art.convert("RGB").save(dest, optimize=True)
    return dest


if __name__ == "__main__":
    jobs = {"entry": make_entry, "exit": make_exit, "banner": make_banner}
    for name in (jobs if sys.argv[1] == "all" else [sys.argv[1]]):
        print(f"{name}: {jobs[name]()}", flush=True)
