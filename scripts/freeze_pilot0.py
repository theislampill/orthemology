#!/usr/bin/env python3
"""Recompute (or verify with --check) a pilot packet freeze hash.

Hash = sha256 over sorted (relpath NUL content NUL) of every file under the
packet directory except FREEZE-HASH.txt itself. Default packet:
terminology/pilot0 (the immutable v1). Pass --packet pilot0-v2 for the R3
matched packet (with --check, both recorded hashes can be verified in one CI
step by running the script twice)."""
import hashlib
import os
import sys

PACKET = "pilot0"
if "--packet" in sys.argv:
    PACKET = sys.argv[sys.argv.index("--packet") + 1]
ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "terminology", PACKET)
HASH_FILE = os.path.join(ROOT, "FREEZE-HASH.txt")


def compute():
    h = hashlib.sha256()
    files = []
    for dp, _, fns in os.walk(ROOT):
        for fn in fns:
            if fn == "FREEZE-HASH.txt":
                continue
            files.append(os.path.join(dp, fn))
    for p in sorted(files):
        rel = os.path.relpath(p, ROOT).replace("\\", "/")
        h.update(rel.encode())
        h.update(b"\0")
        h.update(open(p, "rb").read())
        h.update(b"\0")
    return h.hexdigest()


def main():
    digest = compute()
    if "--check" in sys.argv:
        recorded = ""
        if os.path.exists(HASH_FILE):
            for line in open(HASH_FILE, encoding="utf-8"):
                line = line.strip()
                if len(line) == 64 and all(c in "0123456789abcdef" for c in line):
                    recorded = line
        ok = digest == recorded
        print("[%s] %s packet hash %s recorded hash" % ("PASS" if ok else "FAIL", PACKET,
                                                        "matches" if ok else "does NOT match"))
        sys.exit(0 if ok else 1)
    print(digest)


if __name__ == "__main__":
    main()
