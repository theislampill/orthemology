# R3 Review F — publication, privacy, and closure (adversarial)

**Posture: assume something private leaked, some burden was inflated onto the owner, and the closure language overstates again.**

| Attack | Result | Disposition |
|---|---|---|
| Private leakage | `validate_repo` bans absolute local paths/private patterns/secrets/.env/archives/session dumps — green; the casebook and longitudinal record remain unpublished and are cited only as non-auditable motivation; screenshots/transcripts absent; R2's provenance quarantine (`docs/provenance/document-history.md`) intact | **CLEAN** |
| Owner-only burden inflation (the R2 defect) | Owner list re-narrowed to: license; identity; empirical execution; external publication; genuinely-inaccessible paid sources (none currently identified after documented search); casebook decision. Source verification performed autonomously this pass | **FIXED** |
| False closure, again | Closure language everywhere uses the §16 qualified formulas; the R2 "CLOSED" claims sit under dated supersession notices; the whole-state-reread rule is now a *machine* floor (N11); this review itself lists residuals rather than absorbing them | **FIXED** |
| Empirical overclaim | Corpus-wide: no study run, no term adopted, no utility number; pilot v2 labeled instrument-ready-not-run with the blind human review explicitly pending | **CLEAN** |
| License/identity fabrication | No LICENSE, no CITATION.cff, no author identity anywhere; CITING.md cites by commit | **CLEAN** |
| "Publication-clean"/"reproducible" overstatement | Withdrawn for R2 by supersession; re-asserted for R3 only in the narrow, machine-verified senses (byte-reproducible PDFs; text/visual QA) with residuals listed | **FIXED** |
| Immutable-history corruption | To verify empirically at sign-off (P13 fresh clone): empty diff vs R2 over `archive/`, decisions 0001–0008, `docs/provenance/document-history.md`, frozen terminology v0, pilot0 v1; R2 closure documents modified ONLY by prepended dated notices (bodies verbatim) | **VERIFIED at sign-off** (see R3-INDEPENDENT-SIGNOFF) |
| Force-push/bypass | None used at any point; branch protection intact; merge only via PR after checks | **CLEAN** |

**Residual owner-only burdens (final, narrow):** license · bibliographic identity · empirical execution (spend, ≥3 raters, freeze decision, blind matching review) · external peer review/preprint/DOI · casebook publication decision. Plus deferred research items with triggers (classical paginations; Evans/Turner phrase pair; Darʾ locus queue) which are **not** owner-only.

**Verdict:** publication/privacy lane clean to the stated threshold; closure accounting now applies the project's own false-closure discipline to itself, mechanically where possible.
