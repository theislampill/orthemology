# Terminology matching audit (R3)

**Date:** 2026-07-20 · **Verdict on v1:** NOT matched as its protocol claimed; superseded. **Verdict on v2:** matched under the deterministic audit below; **instrument-ready, NOT RUN**.

## v1 findings (from the R3 read-only audit, quantified)

Per-arm framing word counts in `terminology/pilot0/items/ITEMS.json`: B exceeded A by **+14…+35 words** on every substantive item (P0-ID-1 +21, P0-PL-1 +24, P0-PW-1 +18, P0-FC-1 +24, P0-RR-1 +14, P0-MB-1 +26, P0-MA-1 +35); Arm B repeatedly opened with "The distinction to apply:" and supplied much of the target answer; P0-FC-1's C and C′ renderings were identical while the item was counted as a C/C′ item; the metaorthemma B rendering supplied three ordinary-language synonyms at once; negative controls differed across arms (A bare; B/C/C′ with parentheticals). **v1 remains frozen, immutable superseded history** (hash `ece0412f16d301dcf25b0e6f8956045a45518eceb3d8da1cd63c7478753762c1`; `freeze_pilot0.py --check` still verifies it); it may be used as a smoke-test prototype only and never for inference.

## v2 architecture

All construct teaching moved into **exposure-matched primers** (A: filler with zero construct content; B: ordinary vocabulary; C: coined; C′ machine-generated from C by the 1:1 sham map orth→tarv, `scripts/gen_sham_primer.py`). Item renderings = common scenario + **one length-matched framing sentence** + an **identical question stem**; B/C/C′ framings differ only by the lexical mapping; A's framing is neutral, never an impoverished question. The false-closure item is a declared **label-independent control** (`eligible_for_c_vs_cprime: false`); negative controls are **byte-identical** across all four arms; the metaorthemma item's B arm rotates three single-formulation variants across runs, one per run.

## Deterministic audit results (`scripts/audit_terminology_matching.py`, in CI)

- Framing counts B/C/C′ within ±2 tokens on every substantive item; A within ±4 of B — PASS (v1's +14…+35 deltas eliminated).
- C′ framing == sham(C) exactly for every eligible item; C ≠ C′ (an active coinage) on every eligible item — PASS.
- Label-independent items have C == C′ and are excluded by flag — PASS.
- Negative controls byte-identical across arms — PASS.
- No leakage phrases ("the distinction(s) to apply", "the vocabulary to apply") anywhere — PASS.
- B alternates: single formulation each, within the token budget — PASS.
- Primer word counts pairwise within 15%; primer-C′ == sham(primer-C) modulo title; Arm A primer contains **none** of the construct markers — PASS.
- All eight construct families covered; ≥2 negative controls — PASS.
- **TOTAL: 0 failures.**

## Blind matching review (specified, not yet performed — requires humans)

Before any run, ≥2 reviewers receive the four primers and all item renderings with arm labels stripped and construct nouns masked, and judge per item whether any arm teaches or reveals more than another; a majority "yes" on any item returns the packet to revision and re-freeze. This review needs human reviewers and is therefore part of the owner-gated execution step — recorded in `EXECUTION-SPEC.md` and the readiness report, not claimed done.

## Status line

**Pilot 0 v2: matched instrument-ready under the deterministic audit; blind human matching review pending at execution time; NOT RUN; no term adopted.**
