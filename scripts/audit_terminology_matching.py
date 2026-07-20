#!/usr/bin/env python3
"""Deterministic matching audit for the pilot0-v2 terminology packet (R3 §8.2).

Checks, offline:
  ITEMS (terminology/pilot0-v2/items/ITEMS.json):
  - every rendering = framing + identical stem: stems byte-identical per item;
  - framing token counts: B/C/Cprime within ±2 of each other; A within ±4 of B;
  - Cprime framing == sham_map(C framing) for eligible items;
  - ineligible non-control items have C == Cprime (label-independent control);
  - negative controls: all four framings byte-identical (empty allowed);
  - no leakage phrases ("the distinction(s) to apply", "the vocabulary to
    apply") in any framing or stem;
  - every B_alternates entry is a single formulation (one sentence) and stays
    within the same token budget;
  - construct coverage: >=1 item per required family; >=2 negative controls;
  - eligibility flags present on every item.
  PRIMERS (terminology/pilot0-v2/primers/):
  - four primers exist; word counts pairwise within 15%;
  - primer-armCprime == sham_map(primer-armC) modulo the arm title line;
  - Arm A primer contains none of the taught construct markers (no coined
    terms, no 'identity and version' evidence rule, no result/process split
    teaching phrases).
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V2 = os.path.join(ROOT, "terminology", "pilot0-v2")
FAILS = []

LEAK = re.compile(r"the distinctions? to apply|the vocabulary to apply", re.I)
REQUIRED_FAMILIES = {
    "occurrence-version-identity", "plural-profile-candidates", "pathway-vs-result",
    "false-closure", "governing-rule-revision", "metaorthemma-binding",
    "multi-actor-separation", "negative-control",
}


def check(name, ok, detail=""):
    print("[%s] %s%s" % ("PASS" if ok else "FAIL", name, (" — " + detail) if detail and not ok else ""))
    if not ok:
        FAILS.append(name)


def wc(s):
    return len(s.split())


def apply_sham(text, sham):
    for a in sorted(sham, key=len, reverse=True):
        b = sham[a]
        text = text.replace(a, b)
        text = text.replace(a.capitalize(), b.capitalize())
    return text


def main():
    data = json.load(open(os.path.join(V2, "items", "ITEMS.json"), encoding="utf-8"))
    sham = data["sham_map"]
    items = data["items"]

    fams = {}
    n_nc = 0
    for it in items:
        iid = it["id"]
        fams.setdefault(it["family"], 0)
        fams[it["family"]] += 1
        f = it["framing"]
        check("%s eligibility flag present" % iid, "eligible_for_c_vs_cprime" in it)

        for text in list(f.values()) + [it["stem"], it["scenario_common"]]:
            if LEAK.search(text):
                check("%s leakage phrase" % iid, False, LEAK.search(text).group(0))

        if it.get("negative_control"):
            n_nc += 1
            check("%s negative control byte-identical across arms" % iid,
                  len(set(f.values())) == 1)
            check("%s negative control ineligible for C-vs-Cprime" % iid,
                  it["eligible_for_c_vs_cprime"] is False)
            continue

        b, c, cp, a = wc(f["B"]), wc(f["C"]), wc(f["Cprime"]), wc(f["A"])
        check("%s framing counts B/C/Cprime within ±2 (B=%d C=%d C'=%d)" % (iid, b, c, cp),
              max(b, c, cp) - min(b, c, cp) <= 2)
        check("%s framing count A within ±4 of B (A=%d B=%d)" % (iid, a, b), abs(a - b) <= 4)
        check("%s stems identical across arms (single stem field)" % iid, bool(it["stem"]))

        if it["eligible_for_c_vs_cprime"]:
            check("%s Cprime == sham(C)" % iid, apply_sham(f["C"], sham) == f["Cprime"],
                  "sham(C)=%r Cprime=%r" % (apply_sham(f["C"], sham), f["Cprime"]))
            check("%s C actually uses a coined term" % iid,
                  f["C"] != f["Cprime"], "no active coinage but marked eligible")
        else:
            check("%s label-independent: C == Cprime" % iid, f["C"] == f["Cprime"])

        for j, alt in enumerate(it.get("B_alternates", [])):
            check("%s B_alternate %d single formulation" % (iid, j),
                  alt.count(".") <= 1 and " or " not in alt and "," not in alt)
            check("%s B_alternate %d token budget" % (iid, j), abs(wc(alt) - b) <= 2,
                  "alt=%d B=%d" % (wc(alt), b))

    check("all required construct families covered", REQUIRED_FAMILIES <= set(fams),
          str(sorted(REQUIRED_FAMILIES - set(fams))))
    check(">=2 negative controls", n_nc >= 2, str(n_nc))

    # primers
    pdir = os.path.join(V2, "primers")
    primers = {}
    for arm in ("armA", "armB", "armC", "armCprime"):
        path = os.path.join(pdir, "primer-%s.md" % arm)
        check("primer %s exists" % arm, os.path.exists(path))
        if os.path.exists(path):
            primers[arm] = open(path, encoding="utf-8").read()
    if len(primers) == 4:
        counts = {k: wc(v) for k, v in primers.items()}
        mx, mn = max(counts.values()), min(counts.values())
        check("primer word counts within 15%% (%s)" % counts, (mx - mn) / mx <= 0.15)
        gen = apply_sham(primers["armC"], sham).replace(
            "Arm C (coined vocabulary)", "Arm C′ (sham vocabulary)")
        check("primer-armCprime == sham(primer-armC)", gen == primers["armCprime"])
        a_text = primers["armA"].lower()
        for marker in ["orthemma", "ortheme", "orthing", "identity and version",
                       "right answer through a bad process", "bound configuration",
                       "false completion", "per-side"]:
            check("armA primer free of construct marker %r" % marker, marker not in a_text)

    print("TOTAL: %d failures" % len(FAILS))
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
