#!/usr/bin/env python3
"""Paint a transparent gold title PNG. No HTML/CSS text banner."""
from pathlib import Path
import io
import sys
import urllib.request

ROOT = Path(".")
OUT = ROOT / "title-banner.png"

# If a real brush PNG is already committed and valid, keep it.
if OUT.exists():
    raw = OUT.read_bytes()
    if raw[:8] == b"\x89PNG\r\n\x1a\n" and len(raw) >= 8000:
        print("keep existing title-banner.png", len(raw))
        sys.exit(0)

try:
    from PIL import Image, ImageDraw, ImageFont, ImageFilter
except ImportError:
    sys.exit("Pillow missing — pip install pillow")

FONT_URLS = {
    "script": "https://github.com/google/fonts/raw/main/ofl/greatvibes/GreatVibes-Regular.ttf",
    "caps": "https://github.com/google/fonts/raw/main/ofl/cinzel/Cinzel%5Bwght%5D.ttf",
}

def load_font(url, size):
    req = urllib.request.Request(url, headers={"User-Agent": "nioh3-builder"})
    data = urllib.request.urlopen(req, timeout=30).read()
    return ImageFont.truetype(io.BytesIO(data), size=size)

W, H = 880, 360
img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

script = load_font(FONT_URLS["script"], 168)
caps = load_font(FONT_URLS["caps"], 42)

line1 = "Nioh 3"
line2 = "EQUIPMENT BUILDER"

def centered(text, font):
    box = draw.textbbox((0, 0), text, font=font)
    tw, th = box[2] - box[0], box[3] - box[1]
    return (W - tw) / 2 - box[0], th, box

x1, h1, b1 = centered(line1, script)
y1 = 28
x2, h2, b2 = centered(line2, caps)
y2 = y1 + h1 + 18

# soft gold glow, then the letters
for ox, oy, col, a in (
    (0, 2, (40, 18, 8), 90),
    (0, 0, (196, 160, 80), 255),
):
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.text((x1 + ox, y1 + oy), line1, font=script, fill=(*col, a))
    sd.text((x2 + ox, y2 + oy), line2, font=caps, fill=(*col, a))
    if a < 255:
        shadow = shadow.filter(ImageFilter.GaussianBlur(3))
    img = Image.alpha_composite(img, shadow)

# trim empty margin but keep some padding
bbox = img.getbbox()
if bbox:
    l, t, r, b = bbox
    pad = 16
    l = max(0, l - pad)
    t = max(0, t - pad)
    r = min(W, r + pad)
    b = min(H, b + pad)
    img = img.crop((l, t, r, b))

img.save(OUT, "PNG", optimize=True)
raw = OUT.read_bytes()
if raw[:8] != b"\x89PNG\r\n\x1a\n" or len(raw) < 8000:
    sys.exit(f"wrote invalid banner ({len(raw)} bytes)")
print("wrote", OUT, len(raw), img.size)
