from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
import math
import shutil
import subprocess

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "assets" / "motion"
OUT.mkdir(parents=True, exist_ok=True)

BG = (11, 11, 10)
FG = (241, 238, 231)
MUTED = (112, 110, 105)
DIM = (55, 54, 51)
ACC = (240, 74, 42)
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
BOLD = "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf"
FPS = 24


def _encode(frames: list[Image.Image], output: Path) -> None:
    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg is None:
        raise RuntimeError("ffmpeg is required")
    with TemporaryDirectory(prefix="readme-motion-") as td:
        td = Path(td)
        for i, frame in enumerate(frames):
            frame.save(td / f"f{i:04d}.png", optimize=True)
        palette = td / "palette.png"
        subprocess.run([
            ffmpeg, "-v", "error", "-y", "-framerate", str(FPS),
            "-i", str(td / "f%04d.png"),
            "-vf", "palettegen=max_colors=32:stats_mode=diff", str(palette)
        ], check=True)
        subprocess.run([
            ffmpeg, "-v", "error", "-y", "-framerate", str(FPS),
            "-i", str(td / "f%04d.png"), "-i", str(palette),
            "-lavfi", "paletteuse=dither=none:diff_mode=rectangle",
            "-loop", "0", "-map_metadata", "-1", str(output)
        ], check=True)


def ascii_interference() -> None:
    w, h = 1000, 110
    frames: list[Image.Image] = []
    font = ImageFont.truetype(MONO, 13)
    chars = " .:-=+*/\\\\|#@"
    cols, rows = 104, 7
    x0, y0 = 20, 11
    cw, rh = 9.2, 14
    total = 120

    for fi in range(total):
        t = fi / (total - 1)
        phase = 2 * math.pi * t
        im = Image.new("RGB", (w, h), BG)
        d = ImageDraw.Draw(im)

        for r in range(rows):
            for c in range(cols):
                a = math.sin(c * 0.245 + r * 0.72 + phase)
                b = math.sin(c * 0.109 - r * 1.08 - phase * 2)
                q = (a + b + 2.0) / 4.0
                idx = min(len(chars) - 1, int(q * len(chars)))
                ch = chars[idx]

                seam = (c * 0.75 + r * 6.2 + t * cols) % cols
                dist = min(seam, cols - seam)
                if dist < 1.5 and q > 0.42:
                    color = ACC
                elif q > 0.72:
                    color = MUTED
                else:
                    color = DIM
                d.text((x0 + c * cw, y0 + r * rh), ch, font=font, fill=color)

        aperture_x = int(500 + 320 * math.sin(phase * 0.5))
        d.rectangle((aperture_x - 36, 0, aperture_x + 36, h), fill=BG)
        d.line((aperture_x + 42, 18, aperture_x + 42, 92), fill=ACC, width=2)
        frames.append(im)

    _encode(frames, OUT / "ascii-interference.gif")


def selected_work() -> None:
    w, h = 1000, 126
    total = 96
    font = ImageFont.truetype(BOLD, 84)
    label = "SELECTED WORK"

    mask = Image.new("L", (w, h), 0)
    md = ImageDraw.Draw(mask)
    box = md.textbbox((0, 0), label, font=font)
    tw = box[2] - box[0]
    tx = (w - tw) // 2
    ty = 13 - box[1]
    md.text((tx, ty), label, font=font, fill=255)

    frames: list[Image.Image] = []
    bands = 7
    slice_h = h // bands + 1
    phases = [-1.0, 0.7, -0.35, 0.0, 0.55, -0.8, 0.25]

    for fi in range(total):
        t = fi / total
        p = 2 * math.pi * t
        envelope = (1 - math.cos(p)) / 2
        im = Image.new("RGB", (w, h), BG)

        for i in range(bands):
            y0 = i * (h // bands)
            y1 = min(h, y0 + slice_h)
            amp = 42 + (i % 3) * 14
            offset = int(amp * envelope * math.sin(p + phases[i]))
            crop = mask.crop((0, y0, w, y1))
            dest = Image.new("L", (w, y1 - y0), 0)
            dest.paste(crop, (offset, 0))
            color_layer = Image.new(
                "RGB", (w, y1 - y0),
                ACC if i == 3 and envelope > 0.38 else FG
            )
            im.paste(color_layer, (0, y0), dest)

        d = ImageDraw.Draw(im)
        register = int(56 * envelope * math.sin(p * 2))
        d.line((56 + register, 112, 214 + register, 112), fill=ACC, width=2)
        d.line((786 - register, 112, 944 - register, 112), fill=DIM, width=1)
        frames.append(im)

    _encode(frames, OUT / "selected-work.gif")


if __name__ == "__main__":
    ascii_interference()
    selected_work()
