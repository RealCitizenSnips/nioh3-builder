#!/usr/bin/env python3
"""Unpack the full builder. Do not restyle."""
from pathlib import Path
import gzip, base64, re

root = Path(".")
parts = sorted(root.glob("index.gz.b64.*"))
if not parts:
    raise SystemExit("missing packed builder")
raw = "".join(p.read_text() for p in parts)
raw = re.sub(r"\\s+", "", raw)
raw += "=" * ((4 - len(raw) % 4) % 4)
data = gzip.decompress(base64.b64decode(raw))
(root / "index.html").write_bytes(data)
print("unpacked", len(data))
