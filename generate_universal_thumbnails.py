import os
import sys
import subprocess
import tempfile
from pathlib import Path

BASE_DIR = Path(r"D:\claude_project\nepalirhymehub")
LOGO_PATH = BASE_DIR / "brand" / "logo.png"
FALLBACK_HERO = BASE_DIR / "bhailo_e_bhaili" / "reference" / "character.jpg"
FALLBACK_BANNER = BASE_DIR / "brand" / "banner.png"

WIDTH, HEIGHT = 1280, 720
V_WIDTH, V_HEIGHT = 1080, 1920
FONT = "Nirmala UI"

# Catalog presets for all songs in the Nepali Rhyme Hub universe
SONG_PRESETS = {
    "bhailo_e_bhaili": {
        "title_a": "झिलिमिली\\Nभैलो!",
        "badge_a": "तिहार विशेष",
        "title_b": "भैलो\\Nआयो!",
        "badge_b": "४K बालगीत",
        "accent_a": "&H000850E8",  # Saffron Orange
        "accent_b": "&H00C8102E",  # Crimson
    },
    "hamro_sahar_nepal_yatra": {
        "title_a": "हाम्रो\\Nसहर!",
        "badge_a": "सहर यात्रा",
        "title_b": "नेपाल\\Nघुमौँ!",
        "badge_b": "४K नयाँ गीत",
        "accent_a": "&H0017C3B2",  # Teal Blue
        "accent_b": "&H0000EAFF",  # High-voltage Yellow
    },
    "chhath_parva_aayo": {
        "title_a": "छमछम\\Nछठ!",
        "badge_a": "छठ विशेष",
        "title_b": "सूर्य\\Nपूजा!",
        "badge_b": "मिथिला कला",
        "accent_a": "&H000850E8",
        "accent_b": "&H00C8102E",
    },
    "deusi_bhan_mera_bhai": {
        "title_a": "देउसीरे\\Nभन!",
        "badge_a": "तिहार विशेष",
        "title_b": "आहै भन\\Nसाथी!",
        "badge_b": "देउसी धमाका",
        "accent_a": "&H00C8102E",
        "accent_b": "&H000850E8",
    },
    "maghi_lauro_naach": {
        "title_a": "माघी\\Nआयो!",
        "badge_a": "थारु संस्कृति",
        "title_b": "लौरो\\Nनाँचौँ!",
        "badge_b": "४K बालगीत",
        "accent_a": "&H002A9D8F",
        "accent_b": "&H000850E8",
    },
    "chandi_naach_sakela": {
        "title_a": "साकेला\\Nनाँच!",
        "badge_a": "किराँत विशेष",
        "title_b": "ढोल\\Nबज्यो!",
        "badge_b": "पूर्वी धुन",
        "accent_a": "&H0014234B",
        "accent_b": "&H002A9D8F",
    },
    "pani_paryo_jhamjham": {
        "title_a": "पानी\\Nपर्यो!",
        "badge_a": "मौसम बालगीत",
        "title_b": "छाता\\Nओढौँ!",
        "badge_b": "रमाइलो वर्षा",
        "accent_a": "&H0017C3B2",
        "accent_b": "&H0000EAFF",
    },
    "momo_aayo_plate_ma": {
        "title_a": "मिठो\\Nम:म!",
        "badge_a": "स्वादिलो खाना",
        "title_b": "तातो\\Nतातो!",
        "badge_b": "बालगीत",
        "accent_a": "&H00C8102E",
        "accent_b": "&H000850E8",
    },
    "hamro_gaun_ramailo": {
        "title_a": "हाम्रो\\Nगाउँ!",
        "badge_a": "प्रकृति र गाउँ",
        "title_b": "रमाइलो\\Nनेपाल!",
        "badge_b": "४K बालगीत",
        "accent_a": "&H002A9D8F",
        "accent_b": "&H0000EAFF",
    },
    "tara_baji_lai_lai": {
        "title_a": "ताराबाजी\\Nलै लै!",
        "badge_a": "लोकप्रिय बालगीत",
        "title_b": "मामा\\Nआए!",
        "badge_b": "सधैँको मनपर्ने",
        "accent_a": "&H000850E8",
        "accent_b": "&H00C8102E",
    }
}

def find_best_images(project_dir: Path):
    """Finds the best candidate images for Thumbnail A and B"""
    sb_dir = project_dir / "storyboard"
    ref_dir = project_dir / "reference"
    
    candidates = []
    if sb_dir.is_dir():
        candidates.extend(sorted(sb_dir.glob("*.jpg")))
        candidates.extend(sorted(sb_dir.glob("*.png")))
    if ref_dir.is_dir():
        candidates.extend(sorted(ref_dir.glob("*.jpg")))
        candidates.extend(sorted(ref_dir.glob("*.png")))
        
    if len(candidates) >= 2:
        return candidates[0], candidates[-1]
    elif len(candidates) == 1:
        return candidates[0], candidates[0]
    elif FALLBACK_HERO.is_file():
        return FALLBACK_HERO, FALLBACK_BANNER if FALLBACK_BANNER.is_file() else FALLBACK_HERO
    else:
        raise FileNotFoundError(f"No suitable background images found for {project_dir.name}")

def generate_project_thumbnails(project_name: str):
    project_dir = BASE_DIR / project_name
    if not project_dir.is_dir():
        print(f"Error: Project directory not found: {project_dir}")
        return False
        
    out_dir = project_dir / "out"
    out_dir.mkdir(parents=True, exist_ok=True)
    
    preset = SONG_PRESETS.get(project_name, {
        "title_a": f"{project_name.replace('_', ' ').title()}\\Nगीत!",
        "badge_a": "नयाँ बालगीत",
        "title_b": "नाचौँ\\Nसाथी!",
        "badge_b": "४K बालगीत",
        "accent_a": "&H000850E8",
        "accent_b": "&H00C8102E",
    })
    
    img_a, img_b = find_best_images(project_dir)
    print(f"\nProcessing project: {project_name}")
    print(f"  Image A: {img_a.name}")
    print(f"  Image B: {img_b.name}")
    
    # --- 1. Landscape Thumbnail A (16:9 - 1280x720) ---
    out_thumb_a = out_dir / f"{project_name}-thumb-A.jpg"
    ass_a = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {WIDTH}
PlayResY: {HEIGHT}
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Title,{FONT},115,&H00FFFFFF,&H000000FF,&H000B225E,&H80000000,-1,0,0,0,100,100,0,0,1,10,5,4,50,540,15,1
Style: Badge,{FONT},70,&H00FFFFFF,&H000000FF,{preset['accent_a']},&H00000000,-1,0,0,0,100,100,0,0,3,16,0,1,65,550,85,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.00,0:00:05.00,Title,,0,0,0,,{preset['title_a']}
Dialogue: 0,0:00:00.00,0:00:05.00,Badge,,0,0,0,,{preset['badge_a']}
"""
    with tempfile.TemporaryDirectory(prefix="th_a_") as td:
        ass_path = Path(td) / "thumb.ass"
        ass_path.write_text(ass_a, encoding="utf-8")
        
        filter_complex = (
            f"[0:v]scale={WIDTH}:{HEIGHT}:force_original_aspect_ratio=increase,crop={WIDTH}:{HEIGHT},setsar=1[bg];"
            f"color=c=0x081028:s={WIDTH}x{HEIGHT}:d=1,format=rgba,geq=r=8:g=16:b=40:a='190*max(0\\,1-X/({WIDTH}*0.62))'[shade];"
            f"[bg][shade]overlay=0:0:shortest=1,format=yuv420p[base];"
            f"[1:v]scale=150:-1,format=rgba[logo];"
            f"[base][logo]overlay=40:35[marked];"
            f"[marked]ass={ass_path.name}:shaping=complex[outv]"
        )
        cmd = ["ffmpeg", "-y", "-v", "error", "-i", str(img_a), "-i", str(LOGO_PATH), "-filter_complex", filter_complex, "-map", "[outv]", "-frames:v", "1", "-q:v", "2", str(out_thumb_a)]
        subprocess.run(cmd, cwd=td, check=True)
        print(f"  -> Generated Landscape Thumb A: {out_thumb_a.name} ({out_thumb_a.stat().st_size / 1024:.1f} KB)")

    # --- 2. Landscape Thumbnail B (16:9 - 1280x720) ---
    out_thumb_b = out_dir / f"{project_name}-thumb-B.jpg"
    ass_b = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {WIDTH}
PlayResY: {HEIGHT}
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: TitleB,{FONT},140,&H0000EAFF,&H000000FF,&H00101830,&H90000000,-1,0,0,0,105,100,0,0,1,12,6,4,50,520,15,1
Style: BadgeB,{FONT},65,&H00FFFFFF,&H000000FF,{preset['accent_b']},&H00000000,-1,0,0,0,100,100,0,0,3,15,0,1,65,550,85,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.00,0:00:05.00,TitleB,,0,0,0,,{preset['title_b']}
Dialogue: 0,0:00:00.00,0:00:05.00,BadgeB,,0,0,0,,{preset['badge_b']}
"""
    with tempfile.TemporaryDirectory(prefix="th_b_") as td:
        ass_path = Path(td) / "thumb.ass"
        ass_path.write_text(ass_b, encoding="utf-8")
        
        filter_complex = (
            f"[0:v]scale={WIDTH}:{HEIGHT}:force_original_aspect_ratio=increase,crop={WIDTH}:{HEIGHT},setsar=1[bg];"
            f"color=c=0x040818:s={WIDTH}x{HEIGHT}:d=1,format=rgba,geq=r=4:g=8:b=24:a='195*max(0\\,1-X/({WIDTH}*0.60))'[shade];"
            f"[bg][shade]overlay=0:0:shortest=1,format=yuv420p[base];"
            f"[1:v]scale=150:-1,format=rgba[logo];"
            f"[base][logo]overlay=40:35[marked];"
            f"[marked]ass={ass_path.name}:shaping=complex[outv]"
        )
        cmd = ["ffmpeg", "-y", "-v", "error", "-i", str(img_b), "-i", str(LOGO_PATH), "-filter_complex", filter_complex, "-map", "[outv]", "-frames:v", "1", "-q:v", "2", str(out_thumb_b)]
        subprocess.run(cmd, cwd=td, check=True)
        print(f"  -> Generated Landscape Thumb B: {out_thumb_b.name} ({out_thumb_b.stat().st_size / 1024:.1f} KB)")

    # --- 3. Vertical Cover A (9:16 - 1080x1920) ---
    out_v_thumb_a = out_dir / f"{project_name}-vertical-thumb-A.jpg"
    v_ass_a = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {V_WIDTH}
PlayResY: {V_HEIGHT}
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: VTitle,{FONT},130,&H00FFFFFF,&H000000FF,&H000B225E,&H80000000,-1,0,0,0,100,100,0,0,1,12,6,8,0,0,320,1
Style: VBadge,{FONT},70,&H00FFFFFF,&H000000FF,{preset['accent_a']},&H00000000,-1,0,0,0,100,100,0,0,3,16,0,8,0,0,480,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.00,0:00:05.00,VTitle,,0,0,0,,{preset['title_a'].replace('\\N', ' ')}
Dialogue: 0,0:00:00.00,0:00:05.00,VBadge,,0,0,0,,{preset['badge_a']}
"""
    with tempfile.TemporaryDirectory(prefix="v_th_a_") as td:
        ass_path = Path(td) / "thumb.ass"
        ass_path.write_text(v_ass_a, encoding="utf-8")
        
        filter_complex = (
            f"[0:v]scale={V_WIDTH}:{V_HEIGHT}:force_original_aspect_ratio=increase,crop={V_WIDTH}:{V_HEIGHT},setsar=1[bg];"
            f"color=c=0x081028:s={V_WIDTH}x{V_HEIGHT}:d=1,format=rgba,geq=r=8:g=16:b=40:a='160*if(lt(Y\\,{V_HEIGHT}*0.35)\\,1-Y/({V_HEIGHT}*0.35)\\,0)'[topshade];"
            f"[bg][topshade]overlay=0:0:shortest=1,format=yuv420p[base];"
            f"[1:v]scale=220:-1,format=rgba[logo];"
            f"[base][logo]overlay=60:60[marked];"
            f"[marked]ass={ass_path.name}:shaping=complex[outv]"
        )
        cmd = ["ffmpeg", "-y", "-v", "error", "-i", str(img_a), "-i", str(LOGO_PATH), "-filter_complex", filter_complex, "-map", "[outv]", "-frames:v", "1", "-q:v", "2", str(out_v_thumb_a)]
        subprocess.run(cmd, cwd=td, check=True)
        print(f"  -> Generated Vertical Cover A: {out_v_thumb_a.name} ({out_v_thumb_a.stat().st_size / 1024:.1f} KB)")

    # --- 4. Vertical Cover B (9:16 - 1080x1920) ---
    out_v_thumb_b = out_dir / f"{project_name}-vertical-thumb-B.jpg"
    v_ass_b = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {V_WIDTH}
PlayResY: {V_HEIGHT}
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: VTitleB,{FONT},150,&H0000EAFF,&H000000FF,&H00101830,&H90000000,-1,0,0,0,105,100,0,0,1,14,6,8,0,0,320,1
Style: VBadgeB,{FONT},70,&H00FFFFFF,&H000000FF,{preset['accent_b']},&H00000000,-1,0,0,0,100,100,0,0,3,16,0,8,0,0,500,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.00,0:00:05.00,VTitleB,,0,0,0,,{preset['title_b'].replace('\\N', ' ')}
Dialogue: 0,0:00:00.00,0:00:05.00,VBadgeB,,0,0,0,,{preset['badge_b']}
"""
    with tempfile.TemporaryDirectory(prefix="v_th_b_") as td:
        ass_path = Path(td) / "thumb.ass"
        ass_path.write_text(v_ass_b, encoding="utf-8")
        
        filter_complex = (
            f"[0:v]scale={V_WIDTH}:{V_HEIGHT}:force_original_aspect_ratio=increase,crop={V_WIDTH}:{V_HEIGHT},setsar=1[bg];"
            f"color=c=0x040818:s={V_WIDTH}x{V_HEIGHT}:d=1,format=rgba,geq=r=4:g=8:b=24:a='170*if(lt(Y\\,{V_HEIGHT}*0.35)\\,1-Y/({V_HEIGHT}*0.35)\\,0)'[topshade];"
            f"[bg][topshade]overlay=0:0:shortest=1,format=yuv420p[base];"
            f"[1:v]scale=220:-1,format=rgba[logo];"
            f"[base][logo]overlay=60:60[marked];"
            f"[marked]ass={ass_path.name}:shaping=complex[outv]"
        )
        cmd = ["ffmpeg", "-y", "-v", "error", "-i", str(img_b), "-i", str(LOGO_PATH), "-filter_complex", filter_complex, "-map", "[outv]", "-frames:v", "1", "-q:v", "2", str(out_v_thumb_b)]
        subprocess.run(cmd, cwd=td, check=True)
        print(f"  -> Generated Vertical Cover B: {out_v_thumb_b.name} ({out_v_thumb_b.stat().st_size / 1024:.1f} KB)")
        
    return True

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding='utf-8', errors='replace', line_buffering=True)
    print("=" * 60)
    print("Nepali Rhyme Hub -- Universal High-Attraction Thumbnail Generator")
    print("Enforcing: 16:9 A/B Testing + 9:16 Vertical Covers + 120px Phone Test")
    print("=" * 60)
    
    target_projects = sys.argv[1:]
    if not target_projects or "--all" in target_projects:
        target_projects = ["bhailo_e_bhaili", "hamro_sahar_nepal_yatra", "chhath_parva_aayo", "deusi_bhan_mera_bhai"]
        
    for p in target_projects:
        if p.startswith("--"):
            continue
        generate_project_thumbnails(p)
        
    print("\n[SUCCESS] Universal Thumbnails batch execution complete!")
