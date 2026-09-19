#!/usr/bin/env python3
"""Decode shipped HTML + banner chunks. Do not rewrite CSS."""
from pathlib import Path
import base64, gzip, re

root = Path(".")

def join_b64(prefix: str) -> bytes | None:
    parts = sorted(root.glob(prefix + ".*"))
    blob = root / prefix
    raw = ""
    if parts:
        raw = "".join(p.read_text() for p in parts)
    elif blob.exists():
        raw = blob.read_text()
    else:
        return None
    raw = re.sub(r"\s+", "", raw)
    raw += "=" * ((4 - len(raw) % 4) % 4)
    return base64.b64decode(raw)

html = join_b64("index.gz.b64")
if html is None:
    html = join_b64("index.html.gz.b64")
if html:
    if html[:2] == b"\x1f\x8b":
        html = gzip.decompress(html)
    (root / "index.html").write_bytes(html)
    print("wrote index", len(html))

ban = join_b64("title-banner.b64")
if ban and ban[:2] == b"\xff\xd8" and len(ban) > 20000:
    (root / "title-banner.jpg").write_bytes(ban)
    print("wrote banner", len(ban))

print("index size", (root/"index.html").stat().st_size if (root/"index.html").exists() else 0)
