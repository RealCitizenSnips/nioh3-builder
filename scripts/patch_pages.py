#!/usr/bin/env python3
"""Decode shipped HTML + banner. Do not rewrite CSS."""
from pathlib import Path
import base64, gzip, re

root = Path(".")

def decode_text(p: Path) -> bytes:
    raw = re.sub(r"\s+", "", p.read_text())
    raw += "=" * ((4 - len(raw) % 4) % 4)
    return base64.b64decode(raw)

parts = sorted(root.glob("index.gz.b64.*"))
blob = root / "index.html.gz.b64"
if parts:
    data = base64.b64decode(re.sub(r"\s+", "", "".join(p.read_text() for p in parts)))
    (root / "index.html").write_bytes(gzip.decompress(data))
    print("gunzipped parts", (root/"index.html").stat().st_size)
elif blob.exists():
    (root / "index.html").write_bytes(gzip.decompress(decode_text(blob)))
    print("gunzipped blob", (root/"index.html").stat().st_size)

b64p = root / "title-banner.b64"
if b64p.exists():
    data = decode_text(b64p)
    if data[:2] == b"\xff\xd8" and len(data) > 20000:
        (root / "title-banner.jpg").write_bytes(data)
        print("wrote banner", len(data))

print("index size", (root/"index.html").stat().st_size)
