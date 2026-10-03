#!/usr/bin/env python3
"""
make_site_images.py

Builds the commuted.app screenshot images from the v1.1 raw captures. The
site adds its own rounded corners, and the stylesheet crops the iPhone tiles
to a shared aspect ratio, so these are plain resized captures, not the App
Store composites.

Usage, from the commuted.app repo root:
    python3 make_site_images.py "<path to>/screenshots/raw"

where raw/ holds the iphone/ and ipad/ folders the App Store script uses.

Writes:
    images/01.png to 04.png        iPhone, 900 px wide
    images/ipad-01.png, ipad-02.png iPad landscape, 1400 px wide

Widths are sized for Retina at the largest each tile is drawn: an iPhone
tile reaches about 420 CSS px in the two-column layout, an iPad image about
860 px when stacked on a narrow screen.
"""

import sys
from pathlib import Path
from PIL import Image

JOBS = [
    # (subfolder, source, destination, width)
    ("iphone", "01-home.png", "01.png", 900),
    ("iphone", "02-running.png", "02.png", 900),
    ("iphone", "03-history.png", "03.png", 900),
    ("iphone", "05-rate.png", "04.png", 900),
    ("ipad", "02-running.png", "ipad-01.png", 1400),
    ("ipad", "03-history.png", "ipad-02.png", 1400),
]


def main():
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    raw = Path(sys.argv[1]).expanduser()
    out = Path("images")
    out.mkdir(exist_ok=True)
    for folder, src, dst, width in JOBS:
        path = raw / folder / src
        if not path.exists():
            print(f"  MISSING {path}, skipping")
            continue
        im = Image.open(path).convert("RGB")
        height = round(im.height * width / im.width)
        im.resize((width, height), Image.LANCZOS).save(out / dst, optimize=True)
        print(f"  wrote {out / dst} ({width} x {height}) from {folder}/{src}")
    print(f"\nImages are in {out.resolve()}")


if __name__ == "__main__":
    main()
