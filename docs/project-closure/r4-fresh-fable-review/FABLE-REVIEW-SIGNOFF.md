# R4 PR #3 — Fresh Fable Recovery Review: Sign-Off

Date: 2026-07-20.

## What this sign-off is, in honest wording

This is a **fresh-session Fable review of a prior mixed-provenance
candidate**. The same fresh session performed bounded repairs and then
verified the stopped final tree from a clean clone. It is **independent of
the prior implementing and post-substitution candidate runs**; it is **not an
external human peer review**. It attests only to the current session's
surfaced identity and to evidence it directly reproduced.

Surfaced model identity at every phase boundary of this review:
`claude-fable-5`. No substitution was observed in this session. The
historical provenance disagreement is preserved unadjudicated as two
attributed observations (internal harness claim `claude-fable-5`;
owner-observed UI substitution `claude-opus-4.8`) and was neither resolved
nor overwritten anywhere.

## What was reviewed

- Phase A: live topology, substitution boundary, four-state exact-check
  reproduction, ZIP↔quarantine byte equivalence, audit finding matrix
  (`READONLY-REPRODUCTION.md`).
- Phase B: pre-substitution range `25d035a..00cf05d6`
  (`PRE-SUBSTITUTION-REVIEW.md`) — one repaired finding (B2-1) + scanner
  hardening.
- Phase C: post-substitution range `00cf05d6..de19ccf4` hunk by hunk
  (`POST-SUBSTITUTION-HUNK-REVIEW.md`) — all hunks kept (two with repair /
  revision); ATH-3 downgrade retained; no upgrade from memory.
- Phase D: quarantine-only work selectively ported, never merged wholesale
  (`QUARANTINE-PORT-REVIEW.md`) — interruption record byte-identical
  additive port; internal-reference validator ported with two hardenings;
  tracked-cache guard; PDFs rebuilt from verified sources; 68 pages
  rendered and inspected; state/manifest regenerated in order.
- Phase E: full acceptance + 10 adversarial probes
  (`ACCEPTANCE-AND-PROBES.md`) — one gap (P7) repaired and pinned (I45).
- Phase F: six adversarial passes (`reviews/REVIEW-A…F`) — no blocking
  findings.

## Verification of the final tree

Final review-branch commit at sign-off verification: `f5ad055843d1c43634318c5aed220f47ba6331aa`.

- Full 26-step workflow suite: **0 failures** on the working tree at that
  commit (Python 3.11.9, pinned `pyyaml jsonschema typst==0.15.0
  markdown-it-py==4.0.0 pypdf>=6,<7`).
- **Protected CI green** at that commit: Actions run 29762735763, conclusion
  `success`.
- **Fresh clone** of that exact commit into a new directory, new venv with
  the pinned dependency line: full suite **26/26 steps, 0 failures**;
  `build_pdfs.py --check` performed the clean double rebuild with **byte
  equality** against the committed artifacts; `git status --porcelain`
  empty after all checks.
- Complete diff against `main` inspected across Phases B–F (157 files);
  R1/R2/R3 archives, frozen terminology packets (`pilot0`, `pilot0-v2`),
  and the adopted decision bodies 0001–0008/0010 are **byte-unchanged**
  against `main`.
- This sign-off document (and the state/manifest regeneration that carries
  it) is the only change after `f5ad055`; the full suite was rerun against
  the exact final commit containing this document, its CI awaited, and the
  clean-clone check repeated at that final commit before PR #3 was updated
  (results recorded in the PR body and closeout).

## Artifacts at sign-off

| PDF | Pages | SHA-256 |
|---|---|---|
| orthemma-ortheme-systems-draft.pdf | 31 | `3f2f328a52130834336f45e6b9baee5ead78b86d44c6cb086c53b340d0527bbb` |
| orthemic-core-reference-draft.pdf | 20 | `2629d5ea45941a733c10d4581d284d1f0cd4c059c850e53dfb87fead94563772` |
| orthability-ground-of-intelligibility-draft.pdf | 10 | `a4a12dd5c36209699b93786e23d23d750d626811a6f39077f567f2c61bc945ec` |
| orthability-divine-speech-athari-draft.pdf | 7 | `c78c9dcc0b0e5e53eba2a36788a1ff6b94cc6e8116539591b9611f1a8bce07e5` |

## Bounded lane statements

- Formal specification: internally consistent under all shipped machine
  checks; bounded, not a universal calculus (RequiredBy/RequiredReasonBy
  remain governance-supplied interfaces).
- Manuscript: complete draft, revision-labeled, not peer reviewed.
- School-neutral companion: complete draft with stated conditional exits.
- Atharī companion: complete school-labeled draft; evidence-access statuses
  per registry row; adopted doctrine unchanged.
- Terminology: instrument-ready, NOT RUN, no term adopted.
- **Empirical validation: not performed and not claimed.**
- Legal/publication: owner-only burdens open (license, citation identity,
  external publication).

No required check was red and no blocking review item remained when this
sign-off was issued.
