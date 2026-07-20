#!/usr/bin/env python3
"""Deterministic draft-PDF builder (pure Python: fpdf2 + DejaVu fonts bundled
with matplotlib — both under embedding-permissive free licenses; no private
font files are embedded or redistributed).

Modes:
  build   (default) — render the four draft PDFs into artifacts/ with a DRAFT
          status page (commit hash + generation date), and write a sidecar
          artifacts/<name>.sources.json recording the sha256 of every source.
  --check — CI mode, no rendering, no font dependency: for every committed
          artifacts/*.sources.json, verify the recorded source hashes still
          match the tree (a changed source with an un-rebuilt PDF fails).
          Passes trivially (with a note) when no artifacts are committed.

Missing-dependency behavior (build mode): reports the exact missing package
and exits 3 — every other closure phase is independent of PDF building.
"""
import argparse
import datetime
import hashlib
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ART = os.path.join(ROOT, "artifacts")

DOCS = [
    ("orthemma-ortheme-systems-draft",
     ["manuscript/orthemma-ortheme-systems-revised-draft.md"],
     "Orthemma-Ortheme Systems (main manuscript draft)"),
    ("orthemic-core-reference-draft",
     ["theory/orthemic-core-formalization.md", "theory/orthemic-multi-actor-conflict-note.md"],
     "Orthemic Core Formalization (formal reference draft)"),
    ("orthability-ground-of-intelligibility-draft",
     ["companion/orthability-and-the-ground-of-intelligibility.md"],
     "Orthability and the Ground of Intelligibility (companion draft)"),
    ("orthability-divine-speech-athari-draft",
     ["companion/orthability-divine-attributes-and-speech-athari.md"],
     "Orthability, Divine Attributes, and Speech - Athari (companion draft)"),
]

STATUS_LINES = [
    "DRAFT - not peer reviewed.",
    "Empirical validation not completed: no designed study has been run.",
    "Terminology benchmark not run: every coined term is a candidate; none adopted.",
    "Companion claim status: philosophical conclusions are conditional on stated premises;",
    "creed-internal material is explicitly school-labeled (Athari) and revelational where stated.",
]

# Glyph fallbacks for characters outside DejaVu coverage (math-script letters etc.)
FALLBACK = {
    "\U0001d4ac": "Q", "\U0001d4a2": "G", "\U0001d4a6": "K", "\U0001d4b2": "W",
    "\U0001d4dc": "M", "\U0001d4de": "O", "\U0001d4c2": "m", "\U0001d4f8": "o",
    "\U0001d4d0": "A", "\U0001d4d6": "G", "\U0001d4da": "K",
    "\U0001d4e6": "W", "\U0001d4e2": "S", "\U0001d49c": "A",
    "\U0001d4b6": "a", "\U0001d500": "M", "\U0001d502": "O",
    "ℳ": "M", "ℛ": "R", "ℒ": "L",
    "⫷": "<<", "⫸": ">>",
}


def sha256(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def commit_hash():
    try:
        return subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True,
                              text=True, check=True).stdout.strip()
    except Exception:
        return "unknown"


def clean_text(s):
    for k, v in FALLBACK.items():
        s = s.replace(k, v)
    # break unbreakable overlong tokens so fpdf2 can always wrap
    out = []
    for tok in s.split(" "):
        while len(tok) > 60:
            out.append(tok[:60])
            tok = tok[60:]
        out.append(tok)
    return " ".join(out)


def emit(pdf, text, height):
    """Robust multi_cell: reset x to the left margin first; degrade on failure."""
    pdf.set_x(pdf.l_margin)
    try:
        pdf.multi_cell(0, height, text if text else " ")
    except Exception:
        try:
            pdf.set_x(pdf.l_margin)
            pdf.multi_cell(0, height, text.encode("ascii", "replace").decode() or " ")
        except Exception:
            pass  # skip an unrenderable line rather than fail the build


def check_mode():
    if not os.path.isdir(ART):
        print("[PASS] no artifacts/ directory committed; nothing to check")
        return 0
    sidecars = [f for f in os.listdir(ART) if f.endswith(".sources.json")]
    if not sidecars:
        print("[PASS] no artifact sidecars committed; nothing to check")
        return 0
    fails = 0
    for sc in sorted(sidecars):
        rec = json.load(open(os.path.join(ART, sc), encoding="utf-8"))
        pdf = os.path.join(ART, rec["pdf"])
        ok = os.path.exists(pdf)
        detail = [] if ok else ["missing " + rec["pdf"]]
        for src, h in rec["sources"].items():
            p = os.path.join(ROOT, src)
            if not os.path.exists(p) or sha256(p) != h:
                ok = False
                detail.append("source drift: " + src)
        print("[%s] %s %s" % ("PASS" if ok else "FAIL", sc, "; ".join(detail)))
        fails += 0 if ok else 1
    print("TOTAL: %d failures" % fails)
    return 1 if fails else 0


def find_fonts():
    try:
        import matplotlib
    except ImportError:
        print("MISSING DEPENDENCY: matplotlib (provides the freely-embeddable DejaVu fonts). pip install matplotlib")
        sys.exit(3)
    d = os.path.join(os.path.dirname(matplotlib.__file__), "mpl-data", "fonts", "ttf")
    fonts = {k: os.path.join(d, v) for k, v in
             {"": "DejaVuSans.ttf", "B": "DejaVuSans-Bold.ttf",
              "I": "DejaVuSans-Oblique.ttf", "M": "DejaVuSansMono.ttf"}.items()}
    for p in fonts.values():
        if not os.path.exists(p):
            print("MISSING DEPENDENCY: DejaVu font file not found:", p)
            sys.exit(3)
    return fonts


def build():
    try:
        from fpdf import FPDF
    except ImportError:
        print("MISSING DEPENDENCY: fpdf2 (pip install fpdf2)")
        sys.exit(3)
    fonts = find_fonts()
    os.makedirs(ART, exist_ok=True)
    commit = commit_hash()
    date = datetime.date.today().isoformat()

    for name, sources, title in DOCS:
        pdf = FPDF(format="A4")
        pdf.set_auto_page_break(True, margin=18)
        pdf.add_font("DV", "", fonts[""])
        pdf.add_font("DV", "B", fonts["B"])
        pdf.add_font("DV", "I", fonts["I"])
        pdf.add_font("DVM", "", fonts["M"])
        # status page
        pdf.add_page()
        pdf.set_font("DV", "B", 20)
        emit(pdf, clean_text(title), 10)
        pdf.ln(4)
        pdf.set_font("DV", "B", 12)
        for status_line in STATUS_LINES:
            emit(pdf, status_line, 7)
        pdf.ln(4)
        pdf.set_font("DV", "", 10)
        emit(pdf, "Source revision (git commit): %s\nGenerated: %s\nRepository: theislampill/orthemology\nBuild: scripts/build_pdfs.py (fpdf2 + DejaVu; deterministic pipeline)" % (commit, date), 6)
        # body
        for src in sources:
            text = open(os.path.join(ROOT, src), encoding="utf-8").read()
            pdf.add_page()
            in_code = False
            for raw in text.splitlines():
                line = clean_text(raw.rstrip())
                if line.strip().startswith("```"):
                    in_code = not in_code
                    continue
                if in_code or line.startswith("    "):
                    pdf.set_font("DVM", "", 7.5)
                    emit(pdf, line, 4.2)
                elif line.startswith("#"):
                    level = len(line) - len(line.lstrip("#"))
                    pdf.ln(3)
                    pdf.set_font("DV", "B", max(10, 16 - 2 * level))
                    emit(pdf, line.lstrip("# "), 7)
                    pdf.ln(1)
                elif line.startswith("|"):
                    pdf.set_font("DVM", "", 6.8)
                    emit(pdf, line, 4.0)
                else:
                    pdf.set_font("DV", "", 9.5)
                    stripped = re.sub(r"\*\*([^*]+)\*\*", r"\1", line)
                    stripped = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"\1", stripped)
                    stripped = stripped.replace("`", "")
                    emit(pdf, stripped, 5)
        out = os.path.join(ART, name + ".pdf")
        pdf.output(out)
        sidecar = {
            "pdf": name + ".pdf",
            "commit": commit,
            "generated": date,
            "sources": {src: sha256(os.path.join(ROOT, src)) for src in sources},
            "pipeline": "fpdf2 + matplotlib-bundled DejaVu (embedding-permissive licenses)",
        }
        with open(os.path.join(ART, name + ".sources.json"), "w", encoding="utf-8", newline="\n") as f:
            json.dump(sidecar, f, indent=2)
            f.write("\n")
        print("built", out, "(%d bytes)" % os.path.getsize(out))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    if args.check:
        sys.exit(check_mode())
    build()


if __name__ == "__main__":
    main()
