# R3 terminology readiness

**Status: matched instrument-ready v2, NOT RUN; no experiment of any kind has been executed; no term is adopted.**

- **v1 preserved:** `terminology/pilot0/` untouched; freeze hash `ece0412f16d301dcf25b0e6f8956045a45518eceb3d8da1cd63c7478753762c1` still verifies. v1 is superseded for inferential use (unmatched arms — see `terminology/TERMINOLOGY-MATCHING-AUDIT-R3.md`).
- **v2 packet:** `terminology/pilot0-v2/` — 4 exposure-matched primers (C′ machine-generated from C via the sham map), 9 matched items (6 C/C′-eligible, 1 label-independent control, 2 byte-identical negative controls), complete execution spec (`EXECUTION-SPEC.md`: exact executor prompts, output JSON schema, 5 repetitions, declared sampling parameters, model pinning, deterministic item-order seeds, B-variant rotation, ≥3 blinded raters with masking and Latin-square assignment, comprehension checks, majority adjudication, deviation ledger, estimands E1–E4 with eligibility flags, frozen three-outcome decision rule). Packet freeze hash recorded in `terminology/pilot0-v2/FREEZE-HASH.txt` (`freeze_pilot0.py --packet pilot0-v2 --check` in CI).
- **Deterministic matching audit:** 0 failures in CI (`audit_terminology_matching.py`).
- **Outstanding before execution (owner-gated):** blind human matching review; model spend; ≥3 raters; human-subjects responsibility. Nothing here reports or implies any utility result.
