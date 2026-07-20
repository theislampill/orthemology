#!/usr/bin/env python3
"""Generate the Arm C' (sham) primer and verify sham consistency (pilot0-v2).

The C' primer is C with the 1:1 sham lexical map applied (longest-first so
'metaorthemma' maps before 'orthemma'). Deterministic; also used by the
matching audit to verify that C' artifacts are exactly map(C).
"""
import os
import sys

SHAM = [
    ("Metaorthemma", "Metatarvemma"), ("metaorthemma", "metatarvemma"),
    ("Metaortheme", "Metatarveme"), ("metaortheme", "metatarveme"),
    ("Orthemma", "Tarvemma"), ("orthemma", "tarvemma"),
    ("Ortheme", "Tarveme"), ("ortheme", "tarveme"),
    ("Orthing", "Tarving"), ("orthing", "tarving"),
]


def sham(text):
    for a, b in SHAM:
        text = text.replace(a, b)
    return text


def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pdir = os.path.join(root, "terminology", "pilot0-v2", "primers")
    src = open(os.path.join(pdir, "primer-armC.md"), encoding="utf-8").read()
    out = sham(src).replace("Arm C (coined vocabulary)", "Arm C′ (sham vocabulary)")
    with open(os.path.join(pdir, "primer-armCprime.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write(out)
    print("wrote primer-armCprime.md (%d chars)" % len(out))


if __name__ == "__main__":
    main()
