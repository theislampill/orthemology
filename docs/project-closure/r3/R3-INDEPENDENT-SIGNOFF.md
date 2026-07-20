# R3 independent sign-off

**Date:** 2026-07-20 · **Mode:** final read-only pass from a **fresh clone** of `closure/r3-independent-signoff` at `e2e782cfe598bdf21cd2baf441dc1e3cb5a2e942` (167 tracked files; 14 commits over the R2 baseline `27f66dd8…`), performed after all mutations stopped. Sign-off is issued on this pass, not on the implementation run's green CI.

## Fresh-clone verification results

- **All validators, 0 failures:** repo hygiene (its single "failure" was the then-dangling forward link to this very report — resolved by this commit); verdict semantics (57 checks); notation; type/token semantic roles + orthability senses; reason fixtures CR-1…CR-8; hardened schemas + 8 examples; cross-record semantics; negative fixtures (11) + mutation testing (208 mutants, 0 survivors); ReqPath derivation incl. the omission attack; registry-generated surfaces (no drift); Qurʾān locus registry; claim-source completeness; cross-document consistency; terminology matching audit; both packet freeze hashes (v1 `ece0412f…` immutable; v2 `a1edbd2c…`).
- **PDFs:** `build_pdfs.py --check` from the fresh clone — clean rebuild **byte-identical** to all four committed artifacts (also green on Linux CI, so byte identity holds across OSes). Artifact SHA-256: manuscript `d55e0c0cf96965a93ca58b68eaa5d39cf1893fe15a2d25bae74bf9036b2d6f1d` (30 pp); core `06fff799cd60efd819c579ac7749c22d4f63b6da6b718983fa77baad7f2c4c45` (20 pp); school-neutral `ecb0eb6b97af476409d82608c71c1f819a4b9f43293a5d94abd6034720061b8d` (10 pp); Atharī `41139d7bfeb19f39e3c4204b3d3c8d4c507631f2ef8c4df32bd3ba43bc5f3938` (7 pp). Source revision `d3b34ef…`; artifact revision `731c8ba…` (two-stage provenance).
- **Historical immutability vs R2 (`git diff 27f66dd8..HEAD`):** **empty** over `archive/`, decision records 0001–0008 (the decisions diff shows only the two new files 0009/0010), `docs/provenance/document-history.md`, the frozen terminology v0 spec, and the whole pilot0 v1 packet. The three R2 closure documents show **additions-only** (+2/−0 each: the dated supersession notices); FORMAL-AUDIT-R2, COUNTEREXAMPLE-LEDGER-R2, and the R2 reviews are untouched. No force-push, no history rewrite, no protection bypass occurred at any point.
- **Papers reviewed front-to-back** in rendered form (every page of all four PDFs imaged and inspected — `R3-PDF-VISUAL-QA.md`); final sourcing ledgers reviewed; adversarial reviews A–F on file with residuals listed.

## What is established, by kind (the §14 separation)

1. **Proved by deterministic checks:** everything the validator suite tests — fixture representability, registry/schema/prose coherence, negative rejections, mutation-kill, matching properties, freeze hashes, manifest integrity, PDF byte-reproducibility. Nothing more.
2. **Coherent definitions:** the R3 formal layer (three-axis typing; strict soundness as derived predicate; orthability senses; general Π_A; ReqPath contract) — internally consistent under the declared definitions and acknowledged open parameters (`RequiredBy`-in-general; evidence-class exhaustiveness; fusion non-uniqueness; Δ_A idealizations).
3. **Sourced historical/theological claims:** verified to the stated threshold (āyāt primary; classical works work-level; kalām nafsī secondary with schools split; deferred items with triggers); school-internal claims remain school-internal.
4. **Conditional philosophical argument:** the transcendental chain with its labeled premises and priced exits — never a neutral proof.
5. **Empirically untested:** every designed study; every coined term; the instrument's field utility. **Nothing here is empirical validation, and no such claim is made.**
6. **Owner-only:** license; identity; empirical execution (incl. the blind human matching review); external publication; casebook decision. (No inaccessible-paid-source blocker was identified.)

## Sign-off

The R3 program's blocking findings (SEM-1/2/3, SRC-1/2/3, SCH-1, TERM-1, PDF-1, ACC-1, FORM-1/2, INT-1) are all **fixed and re-verified from a fresh clone**, with residuals dispositioned in `R3-CLOSURE-BURDEN-LEDGER.md` (3 deferred-with-trigger research items; 2 risk-accepted open parameters; 6 owner-assigned items). **R3 independent sign-off: ISSUED**, with the lane verdicts of `R3-PROJECT-CLOSURE-REPORT.md` and nothing stronger. Merge may proceed under branch protection; post-merge verification (exact remote commit, main CI, fresh clone of main) is recorded in the durable state and final closeout.
