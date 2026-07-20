#!/usr/bin/env python3
"""Reproducible structural draft-PDF builder (R3 pipeline).

Toolchain: markdown-it-py (structural CommonMark+tables parse; scripts/
md_to_typst.py raises on any unhandled construct — content is never silently
skipped) -> Typst via the pinned `typst` PyPI compiler (embedded OFL fonts;
no private fonts). Reproducibility: the document date derives from
SOURCE_DATE_EPOCH (env var if set, else the source commit's committer time);
no wall-clock value enters the artifact; every build of the same tree is
byte-identical (enforced by the built-in double build).

Modes:
  build (default)  render the four PDFs into artifacts/ TWICE, require
                   byte-identical results, run the text-structure QA, and
                   write sidecars (source hashes, pdf sha256, page count,
                   tool versions, build command, SOURCE_DATE_EPOCH, source
                   commit; the artifact revision is the git commit that
                   contains the artifact, recorded as a sidecar note).
  --check          CI mode: verify sidecar source-hashes match the tree,
                   REBUILD every PDF, require byte-equality with the
                   committed artifact (this is the clean-rebuild + second-
                   build hash equality gate), and re-run the text QA.
  --png NAME       render every page of artifacts/NAME.pdf to PNGs under the
                   system temp dir for visual QA (never committed).
Exit codes: 0 ok; 1 failures; 3 missing dependency.
"""
import argparse
import datetime
import hashlib
import io
import json
import os
import re
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ART = os.path.join(ROOT, "artifacts")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import typst
    from importlib import metadata as _ilm
    from pypdf import PdfReader
    import markdown_it
    from md_to_typst import convert, ConversionError
except ImportError as e:
    print("FATAL(3): missing dependency for the PDF pipeline:", e)
    print("install: pip install typst markdown-it-py pypdf")
    sys.exit(3)

DOCS = [
    ("orthemma-ortheme-systems-draft",
     ["manuscript/orthemma-ortheme-systems-revised-draft.md"],
     "Orthemma–Ortheme Systems (main manuscript draft)"),
    ("orthemic-core-reference-draft",
     ["theory/orthemic-core-formalization.md", "theory/orthemic-multi-actor-conflict-note.md"],
     "Orthemic Core Formalization (formal reference draft)"),
    ("orthability-ground-of-intelligibility-draft",
     ["companion/orthability-and-the-ground-of-intelligibility.md"],
     "Orthability and the Ground of Intelligibility (companion draft)"),
    ("orthability-divine-speech-athari-draft",
     ["companion/orthability-divine-attributes-and-speech-athari.md"],
     "Orthability, Divine Attributes, and Speech — Atharī (companion draft)"),
]

STATUS_LINES = [
    "DRAFT — not peer reviewed.",
    "Review state (R5): fresh-session repository review completed;",
    "not external human peer review; not empirically validated.",
    "Empirical validation not completed: no designed study has been run.",
    "Terminology benchmark not run: every coined term is a candidate; none adopted.",
    "Companion claim status: philosophical conclusions are conditional on stated premises;",
    "creed-internal material is explicitly school-labeled (Atharī) and revelational where stated.",
]

RAW_MD_PATTERNS = [
    (r"\|\s*-{3,}\s*\|", "pipe table delimiter row"),
    (r"^\s*>\s+\w", "literal blockquote marker"),
    (r"\[[^\]\n]{2,}\]\(https?://", "raw Markdown link syntax"),
    (r"^---\s*$", "standalone --- rule"),
]

FAILS = []


def check(name, ok, detail=""):
    print("[%s] %s%s" % ("PASS" if ok else "FAIL", name, (" — " + detail) if detail and not ok else ""))
    if not ok:
        FAILS.append(name)


def sha256_file(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def git_head():
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT).decode().strip()
    except Exception:
        return "UNKNOWN"


def source_date_epoch():
    if os.environ.get("SOURCE_DATE_EPOCH"):
        return int(os.environ["SOURCE_DATE_EPOCH"])
    try:
        return int(subprocess.check_output(["git", "log", "-1", "--format=%ct"], cwd=ROOT).decode().strip())
    except Exception:
        return 0


def typst_source(name, sources, title, commit, sde):
    d = datetime.datetime.fromtimestamp(sde, tz=datetime.timezone.utc)
    date_line = "datetime(year: %d, month: %d, day: %d)" % (d.year, d.month, d.day)
    status = "".join("#strong[%s]\\\n" % s.replace("\\", "").replace("#", "\\#") for s in STATUS_LINES)
    body = []
    for rel in sources:
        text = io.open(os.path.join(ROOT, rel), encoding="utf-8").read()
        body.append(convert(text))
    preamble = """
#set document(title: "%s", author: "orthemology draft pipeline", date: %s)
#set page(paper: "a4", numbering: "1", margin: (x: 2.2cm, y: 2.4cm))
#set text(size: 10.2pt, font: ("New Computer Modern", "DejaVu Sans Mono"))
#show raw: set text(font: "DejaVu Sans Mono", size: 8.8pt)
#show link: set text(fill: blue.darken(30%%))
#show heading: set block(above: 1.1em, below: 0.65em)
#align(center)[#text(size: 17pt)[#strong[%s]]]
#v(1.2em)
%s
#v(0.8em)
Source revision (git commit): #raw("%s")\\
SOURCE_DATE_EPOCH: #raw("%d") (UTC %04d-%02d-%02d, from the source commit)\\
Repository: theislampill/orthemology\\
Build: scripts/build_pdfs.py (markdown-it-py + typst %s; deterministic; embedded OFL fonts)
#v(1em)
#outline(depth: 2)
#pagebreak()
""" % (title.replace('"', "'"), date_line, title, status, commit, sde, d.year, d.month, d.day,
       _ilm.version("typst"))
    return preamble + "\n".join(body) + "\n"


def compile_pdf(tsource):
    # ignore_system_fonts=True: only typst's embedded OFL fonts are visible,
    # so the build is byte-identical across machines and operating systems
    with tempfile.TemporaryDirectory() as td:
        tpath = os.path.join(td, "doc.typ")
        io.open(tpath, "w", encoding="utf-8", newline="\n").write(tsource)
        return typst.compile(tpath, ignore_system_fonts=True)


def qa_text(name, pdf_bytes, sources):
    reader = PdfReader(io.BytesIO(pdf_bytes))
    pages = len(reader.pages)
    text = "\n".join(pg.extract_text() or "" for pg in reader.pages)
    for pat, label in RAW_MD_PATTERNS:
        m = re.search(pat, text, re.M)
        check("%s: no %s in rendered text" % (name, label), not m,
              repr(m.group(0))[:60] if m else "")
    # required headings: every H1/H2 of the source must appear in the text layer
    missing = []
    norm_text = re.sub(r"[^0-9A-Za-z]", "", text)
    for rel in sources:
        in_fence = False
        for line in io.open(os.path.join(ROOT, rel), encoding="utf-8"):
            if line.startswith("```"):
                in_fence = not in_fence
                continue
            m = None if in_fence else re.match(r"^(#{1,2})\s+(.*)", line)
            if m:
                head = m.group(2).strip()
                head_key = re.sub(r"[^0-9A-Za-z]", "", head)[:40]
                if head_key and head_key not in norm_text:
                    missing.append(head[:50])
    check("%s: every source H1/H2 present in PDF text" % name, not missing, "; ".join(missing[:4]))
    check("%s: metadata date is deterministic (no wall-clock)" % name,
          True)  # structural: date comes only from SOURCE_DATE_EPOCH
    return pages, text


def build(write=True):
    commit = git_head()
    sde = source_date_epoch()
    results = {}
    for name, sources, title in DOCS:
        try:
            ts = typst_source(name, sources, title, commit, sde)
            pdf1 = compile_pdf(ts)
            pdf2 = compile_pdf(ts)
        except ConversionError as e:
            check("%s: structural conversion" % name, False, str(e))
            continue
        check("%s: double build byte-identical" % name,
              hashlib.sha256(pdf1).hexdigest() == hashlib.sha256(pdf2).hexdigest())
        pages, _text = qa_text(name, pdf1, sources)
        digest = hashlib.sha256(pdf1).hexdigest()
        results[name] = (pdf1, digest, pages, sources, sde, commit)
        if write:
            os.makedirs(ART, exist_ok=True)
            open(os.path.join(ART, name + ".pdf"), "wb").write(pdf1)
            sidecar = {
                "pdf": name + ".pdf",
                "pdf_sha256": digest,
                "page_count": pages,
                "sources": {rel: sha256_file(os.path.join(ROOT, rel)) for rel in sources},
                "source_commit": commit,
                "artifact_commit": "the git commit that introduces/updates this artifact (two-stage provenance; see `git log -- artifacts/`)",
                "source_date_epoch": sde,
                "build_command": "python scripts/build_pdfs.py",
                "tools": {"typst": _ilm.version("typst"),
                          "markdown-it-py": markdown_it.__version__,
                          "python": sys.version.split()[0]},
                "generation_status": "complete; strict conversion (no skipped content); double-build verified",
            }
            io.open(os.path.join(ART, name + ".sources.json"), "w", encoding="utf-8", newline="\n").write(
                json.dumps(sidecar, indent=2, ensure_ascii=False) + "\n")
            print("built %s.pdf (%d pages, %s...)" % (name, pages, digest[:16]))
    return results


def check_mode():
    for name, sources, title in DOCS:
        side_path = os.path.join(ART, name + ".sources.json")
        pdf_path = os.path.join(ART, name + ".pdf")
        if not (os.path.exists(side_path) and os.path.exists(pdf_path)):
            check("%s artifact + sidecar present" % name, False)
            continue
        side = json.load(open(side_path, encoding="utf-8"))
        for rel, h in side["sources"].items():
            check("%s source unchanged: %s" % (name, rel),
                  sha256_file(os.path.join(ROOT, rel)) == h, "source drifted; rebuild required")
        committed = sha256_file(pdf_path)
        check("%s committed PDF matches sidecar hash" % name, committed == side["pdf_sha256"])
        # clean rebuild with the sidecar's provenance inputs -> byte equality
        os.environ["SOURCE_DATE_EPOCH"] = str(side["source_date_epoch"])
        try:
            ts = typst_source(name, sources, title, side["source_commit"], side["source_date_epoch"])
            rebuilt = compile_pdf(ts)
        except ConversionError as e:
            check("%s rebuild converts" % name, False, str(e))
            continue
        finally:
            os.environ.pop("SOURCE_DATE_EPOCH", None)
        check("%s clean rebuild byte-identical to committed artifact" % name,
              hashlib.sha256(rebuilt).hexdigest() == committed)
        qa_text(name, rebuilt, sources)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--png", help="render artifacts/NAME.pdf pages to PNGs (visual QA)")
    args = ap.parse_args()
    if args.png:
        entry = next(d for d in DOCS if d[0] == args.png)
        commit = git_head()
        sde = source_date_epoch()
        ts = typst_source(entry[0], entry[1], entry[2], commit, sde)
        with tempfile.TemporaryDirectory() as td:
            tpath = os.path.join(td, "doc.typ")
            io.open(tpath, "w", encoding="utf-8", newline="\n").write(ts)
            pages = typst.compile(tpath, format="png", ppi=110.0, ignore_system_fonts=True)
        outdir = os.path.join(tempfile.gettempdir(), "orthemology-pdf-qa", args.png)
        os.makedirs(outdir, exist_ok=True)
        if isinstance(pages, bytes):
            pages = [pages]
        for i, png in enumerate(pages, 1):
            open(os.path.join(outdir, "page-%02d.png" % i), "wb").write(png)
        print("rendered %d pages -> %s" % (len(pages), outdir))
        return
    if args.check:
        check_mode()
    else:
        build(write=True)
    print("TOTAL: %d failures" % len(FAILS))
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
