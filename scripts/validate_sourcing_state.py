#!/usr/bin/env python3
"""Sourcing-state validator (Decision 0019, R6).

Validates the CLASSIFICATION and NAVIGATION of sourcing surfaces — which
ledger is current, which is an overlay, which is bannered history — never
source truth. Deterministic, offline.

Checks:
  1. the index classifies every sourcing surface it names, with a known
     classification, and every named path exists;
  2. every historical-baseline surface carries its additive HISTORICAL
     BASELINE banner (bodies preserved below it);
  3. exactly one current-view surface exists and it links the index;
  4. current navigation surfaces (STATUS, README, CONTRIBUTING, companion
     README, papers) do not present an R2 ledger as the current destination:
     any mention of the R2 ledger paths outside the index/overlays must sit
     on a line that also signals the historical/current split;
  5. the current view does not restate R2-only status vocabulary as a
     current status of record (the vocabulary may be MENTIONED as
     historical);
  6. the current view's registry claims agree with the registry (ATH-3's
     stated status matches references/source-status.yaml);
  7. overlays declare their base and the base exists.
"""
import io
import os
import re
import sys

try:
    import yaml
except ImportError as e:
    print("FATAL: requires pyyaml:", e)
    sys.exit(2)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAILS = []

R2_LEDGERS = ["docs/sourcing/SOURCING-LEDGER.md",
              "companion/sourcing/COMPANION-SOURCING-LEDGER.md"]
NAV_SURFACES = ["STATUS.md", "README.md", "CONTRIBUTING.md", "companion/README.md",
                "manuscript/orthemma-ortheme-systems-revised-draft.md",
                "companion/orthability-and-the-ground-of-intelligibility.md",
                "companion/orthability-divine-attributes-and-speech-athari.md"]
HIST_MARKERS = ("HISTORICAL", "historical baseline", "bannered", "Decision 0019",
                "CURRENT-SOURCING-LEDGER", "banners-marked", "history")


def check(name, ok, detail=""):
    print("[%s] %s%s" % ("PASS" if ok else "FAIL", name, (" — " + detail) if detail and not ok else ""))
    if not ok:
        FAILS.append(name)


def read(rel):
    p = os.path.join(ROOT, rel)
    return io.open(p, encoding="utf-8").read() if os.path.exists(p) else ""


def main():
    idx = yaml.safe_load(read("docs/sourcing/SOURCING-STATUS-INDEX.yaml"))
    vocab = set(idx["classifications"])
    surfaces = idx["surfaces"]

    for s in surfaces:
        check("index path %s exists" % s["path"],
              os.path.exists(os.path.join(ROOT, s["path"])))
        check("index classification for %s is known" % s["path"],
              s["classification"] in vocab, s.get("classification"))

    by_class = {}
    for s in surfaces:
        by_class.setdefault(s["classification"], []).append(s)

    for s in by_class.get("historical-baseline", []):
        if s["path"].endswith(".md"):
            check("historical surface %s carries its banner" % s["path"],
                  "HISTORICAL BASELINE" in read(s["path"]))

    views = by_class.get("current-view", [])
    check("exactly one current-view surface", len(views) == 1, str([v["path"] for v in views]))
    view = read(views[0]["path"]) if views else ""
    check("current view links the machine index", "SOURCING-STATUS-INDEX.yaml" in view)

    # 4. navigation hygiene
    for rel in NAV_SURFACES:
        text = read(rel)
        for ln_no, ln in enumerate(text.splitlines(), 1):
            for r2 in R2_LEDGERS:
                base = os.path.basename(r2)
                if base in ln and "R3-" + base not in ln:
                    check("%s line %d mentions %s only with a historical/current signal"
                          % (rel, ln_no, base),
                          any(m.lower() in ln.lower() for m in HIST_MARKERS),
                          ln.strip()[:100])

    # 5. R2-only vocabulary not presented as current status in the view
    for tok in ("RECORD-CONFIRMED", "WEB-VERIFIED"):
        for ln in view.splitlines():
            if tok in ln:
                check("current view mentions %r only as historical vocabulary" % tok,
                      "not current" in ln.lower() or "historical" in ln.lower(),
                      ln.strip()[:100])

    # 6. registry agreement (the one status the view states)
    reg = yaml.safe_load(read("references/source-status.yaml"))
    ath3 = next(r["status"] for r in reg["claims"] if r["id"] == "ATH-3")
    m = re.search(r"ATH-3 = `([A-Z_]+)`", view)
    check("current view's ATH-3 status matches the registry",
          m is not None and m.group(1) == ath3,
          "view=%s registry=%s" % (m.group(1) if m else None, ath3))

    # 7. overlays declare an existing base
    for s in by_class.get("overlay", []):
        check("overlay %s declares an existing base" % s["path"],
              bool(s.get("base")) and os.path.exists(os.path.join(ROOT, s["base"])))

    print("TOTAL: %d failures" % len(FAILS))
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
