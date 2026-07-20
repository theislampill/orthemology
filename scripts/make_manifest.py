#!/usr/bin/env python3
"""Regenerate docs/provenance/RELEASE-MANIFEST.sha256 over all git-tracked files
(the manifest itself excluded). Deterministic: sorted paths, LF lines."""
import hashlib
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(ROOT, "docs", "provenance", "RELEASE-MANIFEST.sha256")


def main():
    out = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=True)
    paths = sorted(p for p in out.stdout.splitlines()
                   if p and p != "docs/provenance/RELEASE-MANIFEST.sha256")
    lines = []
    for p in paths:
        fp = os.path.join(ROOT, p)
        h = hashlib.sha256(open(fp, "rb").read()).hexdigest()
        lines.append("%s  %s" % (h, p))
    with open(MANIFEST, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")
    print("wrote %d entries" % len(lines))


if __name__ == "__main__":
    main()
