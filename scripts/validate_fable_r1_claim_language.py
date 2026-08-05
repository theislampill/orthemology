#!/usr/bin/env python3
"""Fail-closed claim-language and source-relation validator (PR #21 repair).

Deterministic checks over docs/project-closure/ar8r-v11/fable-research/:

Check 1 — unverified candidate packets must not carry unqualified
theorem/proof/verification language. Inside a candidate packet, any line
containing a proof-status token (proved/proven/provably/prove(s)/verified/
verifies/establishes/established) fails unless the same line carries an
admissible local status marker, a negation/withdrawal context, or an
evidence owner. The exemption list is deliberately narrow; "proof-theoretic"
as a school-of-derivation label is exempted, bare "proof" claims are not.

Check 2 — the sourcing surface AR8R-FABLE-R1-SOURCING.md must not assign a
factual identity relation to an unverified row, in EITHER the relationship
cell or the claim-supported cell: no IDENTICAL/EQUIVALENT/INHERITS/
ALREADY_EXISTS tokens, and no bare identical/equivalent/inherit*/
"already exists" outside an assessed/analogue wrapper.

Check 3 — the prior-art correspondence table
(AR8R-FABLE-R1-PRIOR-ART-AND-NOVELTY-CEILING.md) is gated the same way:
every Relation cell must be an assessed/analogue/application framing, never
a factual identity token; and the zero-novelty ceiling headline must be
present verbatim.

Deterministic, offline, no network. Exit 0 iff all checks pass.

Scope note: this is a tripwire against re-promotion of withdrawn claim
levels, not a natural-language prover; adversarial paraphrase can evade any
lexical gate, so human review remains the outer gate (CONTRIBUTING.md).
"""

import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PACKET_DIR = os.path.join(ROOT, "docs", "project-closure", "ar8r-v11", "fable-research")
SOURCING = os.path.join(PACKET_DIR, "AR8R-FABLE-R1-SOURCING.md")
PRIOR_ART = os.path.join(PACKET_DIR, "AR8R-FABLE-R1-PRIOR-ART-AND-NOVELTY-CEILING.md")

NOVELTY_CEILING = (
    "**Zero general mathematical novelty is claimed for anything produced in round 1.**"
)

PROOF_TOKEN = re.compile(
    r"\b(Proved|proved|proven|provably|proves?\b|verified|verifies|"
    r"establishes|established)\b"
)
ADMISSIBLE = re.compile(
    r"DERIVED_BUT_UNVERIFIED|CHECKED_FINITE_INSTANCE_ONLY|LEAN_FORMALIZED_SCOPED_RESULT"
    r"|CONJECTURE|SOURCE_LEVEL_UNVERIFIED|UNREPRODUCED_FROM_COMMITTED_ARTIFACTS"
    r"|Lean receipt|kernel-checked|machine-checked in Lean|Lean development"
    r"|checks/|\bwithdrawn\b|\bnarrowed\b|\boriginally\b"
    r"|round 1 (said|asserted|stated|wrote|claim)"
    r"|independent review|checked by no one|not verified|unverified|Unverified|UNVERIFIED"
    r"|\bun(?:sound|verifiable)|never verif|not (?:a )?verif"
    r"|Verification (?:status|vocabulary)|verification status"
    r"|prove nothing|proves nothing|does not (?:establish|prove|verify)"
    r"|[Nn]one (?:has been|of this|is)|has not been|no source|was not|never been"
    r"|\"proved\"|verified independently|independently during review"
    r"|proof-theoretic|primary-verified|-VERIFIED\b"
)
IDENTITY_TOKEN = re.compile(r"\b(IDENTICAL|EQUIVALENT|INHERITS|ALREADY_EXISTS)\b")
BARE_IDENTITY = re.compile(
    r"\b(identical|equivalent|inherits?|inherited|already exists?)\b", re.I
)
ASSESSED_WRAPPER = re.compile(
    r"AUTHOR_ASSESSED_UNVERIFIED|POSSIBLE_ANALOGUE|SEARCH_LEAD"
    r"|[Aa]ssessed [a-z -]*\(unverified\)|\(assessed[^)]*\)"
    r"|\"identical\"|\"equivalent\"|original stronger wording"
    r"|author-assessed|narrowed from"
)

CANDIDATE_PACKETS = [
    "AR8R-FABLE-R1-TYPED-CORE-CANDIDATES.md",
    "AR8R-FABLE-R1-SEPARATION-INDEX-AND-INTERPRETATION-MAPS.md",
    "AR8R-FABLE-R1-NEGATIVE-RESULTS.md",
    "AR8R-FABLE-R1-OSM-TYPED-EXTRACTION.md",
    "AR8R-FABLE-R1-PRIOR-ART-AND-NOVELTY-CEILING.md",
]
# Receipts, audits, the correction record, and README are verification-event
# records (evidence owners), not candidate packets; their "verified" words
# report performed checks and are deliberately out of this gate's scope.

failures = []


def check_packet(path):
    text = io.open(path, encoding="utf-8").read()
    rel = os.path.relpath(path, ROOT).replace(os.sep, "/")
    for no, line in enumerate(text.splitlines(), 1):
        if PROOF_TOKEN.search(line) and not ADMISSIBLE.search(line):
            failures.append("%s:%d: unqualified proof-status language: %s"
                            % (rel, no, line.strip()[:100]))


def _identity_violation(cell):
    if IDENTITY_TOKEN.search(cell):
        return True
    stripped = ASSESSED_WRAPPER.sub("", cell)
    return bool(BARE_IDENTITY.search(stripped))


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
        for cell_name, cell in (("claim-supported", cells[3]),
                                ("relationship", cells[4])):
            if _identity_violation(cell):
                failures.append(
                    "SOURCING.md:%d: factual identity wording in %s cell of an "
                    "UNVERIFIED row: %s" % (no, cell_name, cell[:80]))


def check_prior_art():
    if not os.path.exists(PRIOR_ART):
        failures.append("missing prior-art packet")
        return
    text = io.open(PRIOR_ART, encoding="utf-8").read()
    if NOVELTY_CEILING not in text:
        failures.append("PRIOR-ART: the zero-novelty ceiling headline is missing")
    in_table = False
    for no, line in enumerate(text.splitlines(), 1):
        if line.startswith("| Round-1 object |"):
            in_table = True
            continue
        if in_table:
            if not line.startswith("|"):
                in_table = False
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) < 3 or set(cells[0]) <= {"-", " "}:
                continue
            if _identity_violation(cells[2]):
                failures.append(
                    "PRIOR-ART:%d: factual identity wording in Relation cell: %s"
                    % (no, cells[2][:80]))


def main():
    for name in CANDIDATE_PACKETS:
        path = os.path.join(PACKET_DIR, name)
        if os.path.exists(path):
            check_packet(path)
        else:
            failures.append("missing candidate packet: %s" % name)
    check_sourcing()
    check_prior_art()
    for f in failures:
        print("[FAIL] %s" % f)
    print("[%s] fable-r1 claim-language and source-relation gates (%d failures)"
          % ("FAIL" if failures else "PASS", len(failures)))
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
