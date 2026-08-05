#!/usr/bin/env python3
"""Fail-closed claim-language and source-relation validator (PR #21 repair).

Two deterministic checks over docs/project-closure/ar8r-v11/fable-research/:

Check 1 — unverified candidate packets must not carry unqualified
theorem/proof/verification language. A packet is "unverified-candidate" when
its text contains DERIVED_BUT_UNVERIFIED. Inside such a packet, any line
containing a bare proof-status token (Proved/proved/proven/verified/
establishes) fails unless the same line also carries an admissible local
status marker, a negation/withdrawal context, or an evidence owner:

    admissible on-line contexts:
      DERIVED_BUT_UNVERIFIED, CHECKED_FINITE_INSTANCE_ONLY,
      LEAN_FORMALIZED_SCOPED_RESULT, CONJECTURE, SOURCE_LEVEL_UNVERIFIED,
      UNREPRODUCED_FROM_COMMITTED_ARTIFACTS,
      "Lean" (a receipt-backed kernel check is an admissible owner),
      checks/ (a committed checker is an admissible owner),
      un-/not-/never-/no- negations, "withdrawn", "narrowed",
      quoted withdrawal context ("originally", "round 1 said/asserted/
      stated/wrote/claim"), "independent review", "checked by no one",
      "not verified", "unverified", "Verification" (vocabulary lines).

Check 2 — the sourcing surface AR8R-FABLE-R1-SOURCING.md must not assign a
factual identity relation to an unverified row. Any table row whose
verification cell is UNVERIFIED fails if its relationship cell asserts
IDENTICAL/EQUIVALENT/INHERITS/ALREADY_EXISTS outside an
AUTHOR_ASSESSED/POSSIBLE_ANALOGUE/SEARCH_LEAD wrapper ("assessed identical
(unverified)" is admissible; bare "identical" is not).

Deterministic, offline, no network. Exit 0 iff both checks pass.
"""

import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PACKET_DIR = os.path.join(ROOT, "docs", "project-closure", "ar8r-v11", "fable-research")
SOURCING = os.path.join(PACKET_DIR, "AR8R-FABLE-R1-SOURCING.md")

PROOF_TOKEN = re.compile(r"\b(Proved|proved|proven|verified|verifies|establishes)\b")
ADMISSIBLE = re.compile(
    r"DERIVED_BUT_UNVERIFIED|CHECKED_FINITE_INSTANCE_ONLY|LEAN_FORMALIZED_SCOPED_RESULT"
    r"|CONJECTURE|SOURCE_LEVEL_UNVERIFIED|UNREPRODUCED_FROM_COMMITTED_ARTIFACTS"
    r"|\bLean\b|checks/|\bwithdrawn\b|\bnarrowed\b|\boriginally\b"
    r"|round 1 (said|asserted|stated|wrote|claim)"
    r"|independent review|checked by no one|not verified|unverified|Unverified|UNVERIFIED"
    r"|\bun(?:sound|verifiable)|never verif|not (?:a )?verif|no (?:committed|checker)"
    r"|Verification|prove nothing|proves nothing|does not (?:establish|prove|verify)"
    r"|[Nn]one (?:has been|of this|is)|has not been|no source|was not|never been"
    r"|\"proved\"|verified independently|independently during review"
    r"|must not|forbidden|primary-verified|-VERIFIED\b"
)
FACTUAL_RELATION = re.compile(r"\b(IDENTICAL|EQUIVALENT|INHERITS|ALREADY_EXISTS)\b|"
                              r"(?<![Aa]ssessed )(?<!\")\b[Ii]dentical\b(?! \(unverified\))|"
                              r"(?<![Aa]ssessed )\b[Ee]quivalent\b(?! in both directions \(unverified\))")

failures = []


def check_packet(path):
    text = io.open(path, encoding="utf-8").read()
    if "DERIVED_BUT_UNVERIFIED" not in text:
        return
    rel = os.path.relpath(path, ROOT).replace(os.sep, "/")
    for no, line in enumerate(text.splitlines(), 1):
        if PROOF_TOKEN.search(line) and not ADMISSIBLE.search(line):
            failures.append("%s:%d: unqualified proof-status language: %s"
                            % (rel, no, line.strip()[:100]))


def check_sourcing():
    if not os.path.exists(SOURCING):
        failures.append("missing sourcing surface: AR8R-FABLE-R1-SOURCING.md")
        return
    text = io.open(SOURCING, encoding="utf-8").read()
    for no, line in enumerate(text.splitlines(), 1):
        if not line.startswith("|") or line.count("|") < 6:
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 6 or "UNVERIFIED" not in cells[5]:
            continue
        relation = cells[4]
        if re.search(r"\b(IDENTICAL|EQUIVALENT|INHERITS|ALREADY_EXISTS)\b", relation):
            failures.append("SOURCING.md:%d: factual relation on UNVERIFIED row: %s"
                            % (no, relation[:80]))
            continue
        stripped = re.sub(r"AUTHOR_ASSESSED_UNVERIFIED|POSSIBLE_ANALOGUE|SEARCH_LEAD", "", relation)
        stripped = re.sub(r"assessed [a-z ]*\((?:unverified[^)]*)\)", "", stripped, flags=re.I)
        stripped = re.sub(r"\(assessed[^)]*\)", "", stripped)
        if re.search(r"\b(identical|equivalent|inherits)\b", stripped, flags=re.I):
            failures.append("SOURCING.md:%d: bare identity wording on UNVERIFIED row: %s"
                            % (no, relation[:80]))


CANDIDATE_PACKETS = [
    "AR8R-FABLE-R1-TYPED-CORE-CANDIDATES.md",
    "AR8R-FABLE-R1-SEPARATION-INDEX-AND-INTERPRETATION-MAPS.md",
    "AR8R-FABLE-R1-NEGATIVE-RESULTS.md",
    "AR8R-FABLE-R1-OSM-TYPED-EXTRACTION.md",
    "AR8R-FABLE-R1-PRIOR-ART-AND-NOVELTY-CEILING.md",
    "AR8R-FABLE-R1-TYPED-CORE-CANDIDATES.md",
]
# Receipts, audits, the correction record, and README are verification-event
# records (evidence owners), not candidate packets; their "verified" words
# report performed checks and are deliberately out of this gate's scope.


def main():
    for name in sorted(set(CANDIDATE_PACKETS)):
        path = os.path.join(PACKET_DIR, name)
        if os.path.exists(path):
            check_packet(path)
        else:
            failures.append("missing candidate packet: %s" % name)
    check_sourcing()
    for f in failures:
        print("[FAIL] %s" % f)
    print("[%s] fable-r1 claim-language and source-relation gates (%d failures)"
          % ("FAIL" if failures else "PASS", len(failures)))
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
