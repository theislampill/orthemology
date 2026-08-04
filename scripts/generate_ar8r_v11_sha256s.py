#!/usr/bin/env python3
"""Regenerate the complete AR8R V11 packet SHA256SUMS deterministically."""

from __future__ import annotations

import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / "docs" / "project-closure" / "ar8r-v11"
OUTPUT = PACKET / "SHA256SUMS"

paths = sorted(
    path for path in PACKET.rglob("*")
    if path.is_file() and path != OUTPUT
)
lines = [
    f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.relative_to(PACKET).as_posix()}"
    for path in paths
]
OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
print(f"wrote {len(lines)} entries to {OUTPUT.relative_to(ROOT)}")
