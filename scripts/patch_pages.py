#!/usr/bin/env python3
"""Decode the banner JPEG only. Do not rewrite CSS or HTML."""
from pathlib import Path
import base64, re
root = Path(".")
jpg = root / "title-banner.jpg"
b64p = root / "title-banner.b64"
if b64p.exists():
    raw = re.sub(r"\s+", "", b64p.read_text())
    raw += "=" * ((4 - len(raw) % 4) % 4)
    try:
        data = base64.b64decode(raw)
        if data[:2] == b"\xff\xd8" and len(data) > 20000:
            jpg.write_bytes(data)
            print("wrote banner", len(data))
        else:
            print("banner b64 not a large jpeg", len(data) if data else 0)
    except Exception as e:
        print("banner decode failed", e)
else:
    print("no title-banner.b64")
print("index size", (root/"index.html").stat().st_size)
