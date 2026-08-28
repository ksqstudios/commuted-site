#!/usr/bin/env python3
"""
make_og.py, generate a 1200x630 Open Graph image for commuted.app.

Reuses the exported apple-touch-icon.png as the brand mark, so the icon in
the preview matches exactly what shows as the favicon, the iOS home screen
icon and the masthead on the site itself.

Usage
-----
Place this script in the site repo root, next to apple-touch-icon.png, then:

    python3 make_og.py

Or point it somewhere else:

    python3 make_og.py --icon path/to/apple-touch-icon.png --out .

Output
------
og-image.png, 1200x630.

Fonts
-----
Fraunces for the wordmark, Inter for the headline, IBM Plex Mono for the
URL. Same roles as the site's stylesheet. The script looks for them in the
usual system font directories and in ./fonts/. Without them it falls back to
stand ins and prints a warning: the layout will be right but the letterforms
will not be Commuted's, so do not ship that version.

Requirements
------------
    pip install Pillow
"""

import argparse
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------------------
# Canvas and palette, taken from the site's stylesheet
# ---------------------------------------------------------------------------

W, H = 1200, 630
PAD = 84

CREAM = (0xF8, 0xF5, 0xF0)
INK = (0x2A, 0x26, 0x22)
INK_SOFT = (0x6B, 0x65, 0x5D)

ASPHALT = (0x0E, 0x16, 0x20)
SLATE = (0x1E, 0x30, 0x40)
STEEL = (0x33, 0x54, 0x6B)
CHANNEL = (0x3E, 0x82, 0x9B)
SIGNAL = (0x5F, 0xBF, 0xCF)

GRADIENT_STOPS = [
    (0.00, ASPHALT),
    (0.25, SLATE),
    (0.50, STEEL),
    (0.75, CHANNEL),
    (1.00, SIGNAL),
]

WORDMARK = "Commuted"
HEADLINE = ["Your commute costs hours", "before it costs dollars."]
FIGURE = "4 h 54 min"
FIGURE_CAPTION = "this week"
URL = "commuted.app"

# ---------------------------------------------------------------------------
# Fonts
# ---------------------------------------------------------------------------

FONT_ROOTS = [
    Path("./fonts"),
    Path.home() / "Library/Fonts",
    Path("/Library/Fonts"),
    Path("/System/Library/Fonts"),
    Path("/System/Library/Fonts/Supplemental"),
    Path("/usr/share/fonts"),
    Path("/usr/local/share/fonts"),
]

FALLBACKS = [
    Path("/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"),
    Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
    Path("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"),
]


def find_font(patterns):
    for root in FONT_ROOTS:
        if not root.exists():
            continue
        for pattern in patterns:
            for match in sorted(root.rglob(pattern)):
                return match
    return None


def load(patterns, size, fallback_index):
    path = find_font(patterns)
    if path is None:
        fallback = FALLBACKS[fallback_index]
        if fallback.exists():
            return ImageFont.truetype(str(fallback), size), False
        return ImageFont.load_default(), False
    return ImageFont.truetype(str(path), size), True


# ---------------------------------------------------------------------------
# Drawing
# ---------------------------------------------------------------------------

def gradient_band(width, height):
    """The 135 degree arc, flattened to a horizontal band."""
    band = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(band)
    for x in range(width):
        t = x / max(width - 1, 1)
        for i in range(len(GRADIENT_STOPS) - 1):
            p1, c1 = GRADIENT_STOPS[i]
            p2, c2 = GRADIENT_STOPS[i + 1]
            if p1 <= t <= p2:
                local = (t - p1) / (p2 - p1)
                color = tuple(
                    int(c1[j] + (c2[j] - c1[j]) * local) for j in range(3)
                )
                draw.line([(x, 0), (x, height)], fill=color)
                break
    return band


def rounded(img, radius):
    mask = Image.new("L", img.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        [0, 0, img.size[0] - 1, img.size[1] - 1], radius=radius, fill=255
    )
    out = Image.new("RGBA", img.size, (0, 0, 0, 0))
    out.paste(img, (0, 0), mask=mask)
    return out


def build(icon_path):
    canvas = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(canvas)

    fraunces, ok_f = load(["Fraunces*.ttf", "Fraunces*.otf"], 40, 0)
    inter_head, ok_i = load(["Inter*.ttf", "Inter*.otf"], 62, 1)
    mono, ok_m = load(["IBMPlexMono*.ttf", "IBM*Plex*Mono*.ttf"], 22, 2)
    fraunces_big, _ = load(["Fraunces*.ttf", "Fraunces*.otf"], 76, 0)
    inter_small, _ = load(["Inter*.ttf", "Inter*.otf"], 22, 1)

    if not (ok_f and ok_i and ok_m):
        print("WARNING: one or more of Fraunces, Inter, IBM Plex Mono was not")
        print("         found. Falling back to stand in faces. The layout will")
        print("         be right but do not ship this version.")

    # Masthead ------------------------------------------------------------
    y = PAD
    if icon_path and Path(icon_path).exists():
        icon = Image.open(icon_path).convert("RGBA").resize((72, 72), Image.LANCZOS)
        canvas.paste(rounded(icon, 17), (PAD, y), rounded(icon, 17))
        text_x = PAD + 72 + 20
    else:
        print("NOTE: no apple-touch-icon.png found, drawing without the mark.")
        text_x = PAD

    draw.text((text_x, y + 18), WORDMARK, font=fraunces, fill=INK)

    # Headline ------------------------------------------------------------
    y = 214
    for line in HEADLINE:
        draw.text((PAD, y), line, font=inter_head, fill=INK)
        y += 78

    # The figure, as a small gradient card in the lower right --------------
    # Placed below the headline rather than beside it: at this size the
    # headline runs most of the canvas width and a card alongside it collides.
    card_w, card_h = 340, 152
    card_x, card_y = W - PAD - card_w, H - PAD - card_h - 14

    card = rounded(gradient_band(card_w, card_h), 20)
    canvas.paste(card, (card_x, card_y), card)

    cdraw = ImageDraw.Draw(canvas)

    # Shrink the figure until it fits the card with margin to spare.
    size = 76
    while size > 30:
        candidate, _ = load(["Fraunces*.ttf", "Fraunces*.otf"], size, 0)
        if cdraw.textlength(FIGURE, font=candidate) <= card_w - 56:
            fraunces_big = candidate
            break
        size -= 2

    cdraw.text((card_x + 28, card_y + 30), FIGURE, font=fraunces_big, fill=CREAM)
    cdraw.text((card_x + 30, card_y + 30 + size + 14), FIGURE_CAPTION,
               font=inter_small, fill=(230, 238, 242))

    # URL ------------------------------------------------------------------
    draw.text((PAD, H - PAD - 40), URL, font=mono, fill=INK_SOFT)

    # Gradient rule along the bottom edge, the brand signature -------------
    band = gradient_band(W, 12)
    canvas.paste(band, (0, H - 12))

    return canvas


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--icon", default="apple-touch-icon.png")
    parser.add_argument("--out", default=".")
    args = parser.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "og-image.png"

    build(args.icon).save(out_path, optimize=True)
    print(f"wrote {out_path} ({W}x{H})")


if __name__ == "__main__":
    main()
