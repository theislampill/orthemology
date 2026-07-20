# R3 closure burden ledger

**Date:** 2026-07-20. Every burden of the R3 corrective program, one honest disposition each, using the project's residual taxonomy. Supersedes the R2 ledger's dispositions (that ledger is preserved under its supersession notice). Findings source: `R2-INDEPENDENT-READONLY-AUDIT.md`; corrections: `R3-CORRECTION-LEDGER.md`.

| # | Burden | Disposition | Evidence / trigger |
|---|---|---|---|
| 1 | False-closure accounting corrected without rewriting history | **validated-resolved** | dated supersession notices; R2 bodies verbatim (empty-diff check in the sign-off report) |
| 2 | Type/token collapse repaired with the concrete/sound distinction preserved | **validated-resolved** | Decision 0009; companion three-axis rewrite; CONCRETE-AND-SOUND-REASON.md; role validator; CR-1…CR-8 (CI) |
| 3 | Orthability equivocation repaired | **validated-resolved** | Decision 0010; L→O bridge; ARGUMENT-MAP; sense guard (CI); objections G1/G2 |
| 4 | Π_A generalized; five profile states separated | **validated-resolved** | Definition 10 R3; CE-R1…CE-R4 |
| 5 | ReqPath machine-derivable with trace; omission attack caught | **validated-resolved** | governance table + derive_reqpath (CI); RP-1…RP-5 |
| 6 | `RequiredBy` universal calculus | **risk-accepted (open parameter, stated)** | core §4.1; manuscript §15.1; R3-FORMAL-AUDIT §2 |
| 7 | Evidence-class exhaustiveness; fusion non-uniqueness; Δ_A idealizations | **risk-accepted (stated)** | R3-FORMAL-AUDIT §5; CE-R8 |
| 8 | Qurʾānic loci verified; 20:11–12 corrected everywhere | **validated-resolved** | quran-loci.yaml + CI validator; all 29 āyāt primary-verified |
| 9 | Hadith + classical works verified at work level | **validated-resolved** | R3 companion sourcing ledger; no phantom source |
| 10 | Classical page-level (edition) verification (6 loci) | **deferred** | trigger: library/edition access before any external submission; non-load-bearing (paginations are citation conveniences) |
| 11 | Kalām nafsī comparative paragraph sourced, schools split | **validated-resolved** (secondary threshold stated) | Atharī §7; tradition-internal anchors both schools |
| 12 | Hagiographic courtroom narrative | **validated-resolved** (downgraded to doctrinal-usage; not load-bearing) | Atharī §3.2 + source-critical note |
| 13 | Academic bibliography re-verification; mismatches | **validated-resolved** | 26 rows re-graded; 6 bib fixes (SEP archive-pinning etc.); 0 unverified |
| 14 | Evans/Turner "concrete/ideal reason" phrase-pair verification | **deferred** | trigger: full-text access (library); prose softened; non-load-bearing |
| 15 | Darʾ primary-locus queue for Taymiyyan attributions | **deferred** | trigger: continued research; all attributions labeled secondary reconstruction meanwhile |
| 16 | Schemas hardened; negative + mutation testing | **validated-resolved** | 11 negative fixtures; 208 mutants, 0 survivors (CI) |
| 17 | Cross-record semantics incl. Definition-13 closure floor | **validated-resolved** | validator (CI); N11; whole-state-reread example |
| 18 | Terminology instrument matched (v2); v1 preserved | **validated-resolved** | matching audit 0 failures (CI); v1+v2 freeze hashes (CI) |
| 19 | Blind human matching review of v2 | **owner-assigned** | requires human reviewers; part of execution gate |
| 20 | Empirical execution of any designed study | **owner-assigned** | spend + ≥3 raters + freeze decision; NOT RUN and not claimed run |
| 21 | PDFs byte-reproducible, structural, visually QA'd | **validated-resolved** | double-build + CI clean-rebuild byte-equality (cross-OS, green); R3-PDF-VISUAL-QA |
| 22 | daee-epistemics bounded imports + rejections recorded | **validated-resolved** | mapping note; CR-7; N11; generated surfaces |
| 23 | CI expanded, offline-deterministic, pinned | **validated-resolved** | 18 steps; pinned deps; green at 9ff3a90 and at the artifact commit |
| 24 | Adversarial reviews A–F + 15 amendment questions | **validated-resolved** | reviews/ + R3-FORMAL-AUDIT §4; residuals listed, not absorbed |
| 25 | Legal license | **owner-assigned** | owner-only legal act |
| 26 | Author/citation identity; numbered release | **owner-assigned** | owner-only identity facts |
| 27 | External peer review / preprint / DOI | **owner-assigned** | owner-identity acts |
| 28 | Casebook publication decision | **owner-assigned** | rights/privacy call; corpus does not depend on it |
| 29 | Final read-only sign-off from fresh clone; PR; merge; post-merge verification | **validated-resolved at merge** | R3-INDEPENDENT-SIGNOFF.md; closure report records the merge facts |

**Counts:** 18 validated-resolved (+1 at merge = 19) · 3 deferred (#10, #14, #15 — ordinary research with triggers, not owner-only) · 5 owner-assigned (#19, #20, #25, #26, #27, #28 → six items, of which #19/#20 are the execution gate) · 2 risk-accepted (#6, #7). Nothing is unresolved-without-a-plan; no ordinary research burden sits on the owner list.
