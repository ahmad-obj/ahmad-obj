from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


W = 1000
BG = (11, 11, 10)
CORAL = (240, 74, 42)
COBALT = (49, 87, 213)
ACID = (231, 240, 74)
OFF = (241, 238, 231)
GRAY = (155, 153, 147)

FONT = Path("/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf")


def _font(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT), size)


def _center_x(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont) -> int:
    box = draw.textbbox((0, 0), text, font=font, stroke_width=0)
    return (W - (box[2] - box[0])) // 2 - box[0]


def render_current() -> Image.Image:
    h = 126
    im = Image.new("RGB", (W, h), BG)
    font = _font(96)
    text = "CURRENT"

    layers = [
        (COBALT, -12, 5),
        (ACID, 9, -5),
        (CORAL, 5, 5),
        (OFF, 0, 0),
    ]
    base = Image.new("L", (W, h), 0)
    bd = ImageDraw.Draw(base)
    x = _center_x(bd, text, font)
    y = 11
    bd.text((x, y), text, font=font, fill=255)

    for idx, (color, dx, dy) in enumerate(layers):
        mask = Image.new("L", (W, h), 0)
        mask.paste(base, (dx, dy))
        if idx == 0:
            ImageDraw.Draw(mask).rectangle((0, 0, W, 26), fill=0)
        elif idx == 1:
            ImageDraw.Draw(mask).rectangle((0, 93, W, h), fill=0)
        color_layer = Image.new("RGB", (W, h), color)
        im.paste(color_layer, (0, 0), mask)

    d = ImageDraw.Draw(im)
    d.rectangle((48, 20, 56, 106), fill=CORAL)
    d.rectangle((944, 20, 952, 106), fill=COBALT)
    return im


def render_academic() -> Image.Image:
    h = 144
    im = Image.new("RGB", (W, h), BG)
    d = ImageDraw.Draw(im)
    font = _font(82)
    text = "ACADEMIC"
    x = _center_x(d, text, font) + 24
    y = 28

    for depth in range(16, 0, -1):
        dx = -depth * 3
        dy = depth * 2
        if depth > 11:
            color = COBALT
        elif depth > 5:
            color = CORAL
        else:
            color = GRAY
        d.text((x + dx, y + dy), text, font=font, fill=color)

    d.text((x, y), text, font=font, fill=OFF)
    d.line((60, 118, 302, 118), fill=CORAL, width=2)
    d.line((698, 25, 940, 25), fill=COBALT, width=2)
    return im


def render_interests() -> Image.Image:
    h = 140
    im = Image.new("RGB", (W, h), BG)
    d = ImageDraw.Draw(im)
    font = _font(84)
    text = "INTERESTS"
    x = _center_x(d, text, font)
    y = 25

    offsets = [
        (-18, 10), (-14, 6), (-10, 3), (-6, 0), (-2, -2),
        (2, -3), (6, -2), (10, 1), (14, 5), (18, 10),
    ]
    for i, (dx, dy) in enumerate(offsets):
        if i in (1, 8):
            color = COBALT
        elif i in (3, 6):
            color = CORAL
        else:
            color = GRAY
        d.text(
            (x + dx, y + dy),
            text,
            font=font,
            fill=BG,
            stroke_width=1,
            stroke_fill=color,
        )

    d.text((x, y), text, font=font, fill=OFF)
    return im


def save_all(output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    images = {
        "current.png": render_current(),
        "academic.png": render_academic(),
        "interests.png": render_interests(),
    }
    for name, image in images.items():
        image.save(output_dir / name, format="PNG", optimize=True, compress_level=9)


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[2]
    save_all(root / "assets" / "typography")
