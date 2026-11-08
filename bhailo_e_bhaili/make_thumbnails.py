import os
import subprocess
import tempfile
from pathlib import Path

SONG_DIR = Path(r"D:\claude_project\nepalirhymehub\bhailo_e_bhaili")
OUT_DIR = SONG_DIR / "out"
OUT_DIR.mkdir(parents=True, exist_ok=True)

LOGO = Path(r"D:\claude_project\nepalirhymehub\brand\logo.png")
IMG_A = SONG_DIR / "storyboard" / "intro-sc2-b2.jpg"
IMG_B = SONG_DIR / "storyboard" / "chorus1-sc3-b1.jpg"

WIDTH, HEIGHT = 1280, 720
V_WIDTH, V_HEIGHT = 1080, 1920
FONT = "Nirmala UI"

def generate_thumb_a():
    """Thumbnail A (YouTube 16:9 Landscape - Emotional Lead Close-up):
    Aarya with glowing diyo on temple steps + 'झिलिमिली भैलो!' + saffron badge 'तिहार विशेष'
    """
    out_path = OUT_DIR / "bhailo_e_bhaili-thumb-A.jpg"
    ass_content = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {WIDTH}
PlayResY: {HEIGHT}
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Title,{FONT},115,&H00FFFFFF,&H000000FF,&H000B225E,&H80000000,-1,0,0,0,100,100,0,0,1,10,5,4,50,540,15,1
Style: Badge,{FONT},70,&H00FFFFFF,&H000000FF,&H000850E8,&H00000000,-1,0,0,0,100,100,0,0,3,16,0,1,65,550,85,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.00,0:00:05.00,Title,,0,0,0,,झिलिमिली\\Nभैलो!
Dialogue: 0,0:00:00.00,0:00:05.00,Badge,,0,0,0,,तिहार विशेष
"""
    with tempfile.TemporaryDirectory(prefix="thumb_a_") as td:
        ass_file = Path(td) / "thumb.ass"
        ass_file.write_text(ass_content, encoding="utf-8")
        
        filter_complex = (
            f"[0:v]scale={WIDTH}:{HEIGHT}:force_original_aspect_ratio=increase,crop={WIDTH}:{HEIGHT},setsar=1[bg];"
            f"color=c=0x081028:s={WIDTH}x{HEIGHT}:d=1,format=rgba,geq=r=8:g=16:b=40:a='190*max(0\\,1-X/({WIDTH}*0.62))'[shade];"
            f"[bg][shade]overlay=0:0:shortest=1,format=yuv420p[base];"
            f"[1:v]scale=150:-1,format=rgba[logo];"
            f"[base][logo]overlay=40:35[marked];"
            f"[marked]ass={ass_file.name}:shaping=complex[outv]"
        )
        
        cmd = [
            "ffmpeg", "-y", "-v", "error",
            "-i", str(IMG_A),
            "-i", str(LOGO),
            "-filter_complex", filter_complex,
            "-map", "[outv]",
            "-frames:v", "1",
            "-q:v", "2",
            str(out_path)
        ]
        subprocess.run(cmd, cwd=td, check=True)
        print(f"Rendered Thumb A (16:9): {out_path} ({os.path.getsize(out_path) / 1024:.1f} KB)")

def generate_thumb_b():
    """Thumbnail B (YouTube 16:9 Landscape - High Energy Dance & Action):
    Group dance & Aarav with madal + Big bold yellow 'भैलो आयो!' + badge '४K बालगीत'
    """
    out_path = OUT_DIR / "bhailo_e_bhaili-thumb-B.jpg"
    ass_content = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {WIDTH}
PlayResY: {HEIGHT}
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: TitleYellow,{FONT},140,&H0000EAFF,&H000000FF,&H00101830,&H90000000,-1,0,0,0,105,100,0,0,1,12,6,4,50,520,15,1
Style: BadgeB,{FONT},65,&H00FFFFFF,&H000000FF,&H00C8102E,&H00000000,-1,0,0,0,100,100,0,0,3,15,0,1,65,550,85,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.00,0:00:05.00,TitleYellow,,0,0,0,,भैलो\\Nआयो!
Dialogue: 0,0:00:00.00,0:00:05.00,BadgeB,,0,0,0,,४K बालगीत
"""
    with tempfile.TemporaryDirectory(prefix="thumb_b_") as td:
        ass_file = Path(td) / "thumb.ass"
        ass_file.write_text(ass_content, encoding="utf-8")
        
        filter_complex = (
            f"[0:v]scale={WIDTH}:{HEIGHT}:force_original_aspect_ratio=increase,crop={WIDTH}:{HEIGHT},setsar=1[bg];"
            f"color=c=0x040818:s={WIDTH}x{HEIGHT}:d=1,format=rgba,geq=r=4:g=8:b=24:a='195*max(0\\,1-X/({WIDTH}*0.60))'[shade];"
            f"[bg][shade]overlay=0:0:shortest=1,format=yuv420p[base];"
            f"[1:v]scale=150:-1,format=rgba[logo];"
            f"[base][logo]overlay=40:35[marked];"
            f"[marked]ass={ass_file.name}:shaping=complex[outv]"
        )
        
        cmd = [
            "ffmpeg", "-y", "-v", "error",
            "-i", str(IMG_B),
            "-i", str(LOGO),
            "-filter_complex", filter_complex,
            "-map", "[outv]",
            "-frames:v", "1",
            "-q:v", "2",
            str(out_path)
        ]
        subprocess.run(cmd, cwd=td, check=True)
        print(f"Rendered Thumb B (16:9): {out_path} ({os.path.getsize(out_path) / 1024:.1f} KB)")

def generate_vertical_thumb_a():
    """Vertical Cover A (9:16 - 1080x1920 for TikTok, Reels, Shorts):
    Centered Aarya with glowing diyo + top text in vertical safe area
    """
    out_path = OUT_DIR / "bhailo_e_bhaili-vertical-thumb-A.jpg"
    ass_content = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {V_WIDTH}
PlayResY: {V_HEIGHT}
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: VTitle,{FONT},130,&H00FFFFFF,&H000000FF,&H000B225E,&H80000000,-1,0,0,0,100,100,0,0,1,12,6,8,0,0,320,1
Style: VBadge,{FONT},70,&H00FFFFFF,&H000000FF,&H000850E8,&H00000000,-1,0,0,0,100,100,0,0,3,16,0,8,0,0,480,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.00,0:00:05.00,VTitle,,0,0,0,,झिलिमिली भैलो! 🪔
Dialogue: 0,0:00:00.00,0:00:05.00,VBadge,,0,0,0,,तिहार विशेष २०२६
"""
    with tempfile.TemporaryDirectory(prefix="v_thumb_a_") as td:
        ass_file = Path(td) / "thumb.ass"
        ass_file.write_text(ass_content, encoding="utf-8")
        
        # Scale to fill 1080x1920, add gentle top & bottom vignette for text & safe zone
        filter_complex = (
            f"[0:v]scale={V_WIDTH}:{V_HEIGHT}:force_original_aspect_ratio=increase,crop={V_WIDTH}:{V_HEIGHT},setsar=1[bg];"
            f"color=c=0x081028:s={V_WIDTH}x{V_HEIGHT}:d=1,format=rgba,geq=r=8:g=16:b=40:a='160*if(lt(Y\\,{V_HEIGHT}*0.35)\\,1-Y/({V_HEIGHT}*0.35)\\,0)'[topshade];"
            f"[bg][topshade]overlay=0:0:shortest=1,format=yuv420p[base];"
            f"[1:v]scale=220:-1,format=rgba[logo];"
            f"[base][logo]overlay=60:60[marked];"
            f"[marked]ass={ass_file.name}:shaping=complex[outv]"
        )
        
        cmd = [
            "ffmpeg", "-y", "-v", "error",
            "-i", str(IMG_A),
            "-i", str(LOGO),
            "-filter_complex", filter_complex,
            "-map", "[outv]",
            "-frames:v", "1",
            "-q:v", "2",
            str(out_path)
        ]
        subprocess.run(cmd, cwd=td, check=True)
        print(f"Rendered Vertical Thumb A (9:16): {out_path} ({os.path.getsize(out_path) / 1024:.1f} KB)")

def generate_vertical_thumb_b():
    """Vertical Cover B (9:16 - 1080x1920 for TikTok, Reels, Shorts):
    Action dance + bold yellow title
    """
    out_path = OUT_DIR / "bhailo_e_bhaili-vertical-thumb-B.jpg"
    ass_content = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {V_WIDTH}
PlayResY: {V_HEIGHT}
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: VTitleB,{FONT},150,&H0000EAFF,&H000000FF,&H00101830,&H90000000,-1,0,0,0,105,100,0,0,1,14,6,8,0,0,320,1
Style: VBadgeB,{FONT},70,&H00FFFFFF,&H000000FF,&H00C8102E,&H00000000,-1,0,0,0,100,100,0,0,3,16,0,8,0,0,500,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.00,0:00:05.00,VTitleB,,0,0,0,,भैलो आयो! ✨
Dialogue: 0,0:00:00.00,0:00:05.00,VBadgeB,,0,0,0,,४K नेपाली बालगीत
"""
    with tempfile.TemporaryDirectory(prefix="v_thumb_b_") as td:
        ass_file = Path(td) / "thumb.ass"
        ass_file.write_text(ass_content, encoding="utf-8")
        
        filter_complex = (
            f"[0:v]scale={V_WIDTH}:{V_HEIGHT}:force_original_aspect_ratio=increase,crop={V_WIDTH}:{V_HEIGHT},setsar=1[bg];"
            f"color=c=0x040818:s={V_WIDTH}x{V_HEIGHT}:d=1,format=rgba,geq=r=4:g=8:b=24:a='170*if(lt(Y\\,{V_HEIGHT}*0.35)\\,1-Y/({V_HEIGHT}*0.35)\\,0)'[topshade];"
            f"[bg][topshade]overlay=0:0:shortest=1,format=yuv420p[base];"
            f"[1:v]scale=220:-1,format=rgba[logo];"
            f"[base][logo]overlay=60:60[marked];"
            f"[marked]ass={ass_file.name}:shaping=complex[outv]"
        )
        
        cmd = [
            "ffmpeg", "-y", "-v", "error",
            "-i", str(IMG_B),
            "-i", str(LOGO),
            "-filter_complex", filter_complex,
            "-map", "[outv]",
            "-frames:v", "1",
            "-q:v", "2",
            str(out_path)
        ]
        subprocess.run(cmd, cwd=td, check=True)
        print(f"Rendered Vertical Thumb B (9:16): {out_path} ({os.path.getsize(out_path) / 1024:.1f} KB)")

if __name__ == "__main__":
    print("=" * 60)
    print("Nepali Rhyme Hub — Rendering High-CTR A/B Thumbnails")
    print("=" * 60)
    generate_thumb_a()
    generate_thumb_b()
    generate_vertical_thumb_a()
    generate_vertical_thumb_b()
    print("All 4 A/B Thumbnails (Landscape & Vertical) successfully rendered!")
