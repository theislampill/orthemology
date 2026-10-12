# Verified formal frontier checkpoint — 2026-09-30

## Result

Eight new mathematical modules (1,218 source lines), plus the verification module, build successfully. The final checkpoint audits 38 required declarations and verifies that their transitive axiom footprints are subsets of `propext`, `Classical.choice`, and `Quot.sound`. No `sorry`, custom foundational axiom, or native-decision proof is used.

Passing receipt: `receipts/verify-20260930T134917Z.log`
Machine-readable axiom footprints: the same path followed by `.axioms.json`

## Established

1. Conservative maximum-fibre continuation rank transport, matched source runs, nonblocking run existence, and positive/negative relational fixtures
2. Exact PER potential `2(m−|D|)+c`, strict growth, and `2m−1` stabilization
3. Actual universal-input Mealy semantics and distinguishing-word correspondence
4. All-positive-cardinality sharpness, including the one-state case
5. Equality of guarded `R ∩ refine(R)` and unguarded top iterations, so the same bounds apply literally to both
6. Exact finite block-path counts and the rational geometric bound `(1−2^−L)^j`, with `L=2m−1`
7. The complementary minimum-fibre bad-visit budget theorem under pairwise bad reflection, with bounded bad-visit count and an unbounded-time eventual-good cutoff

## Lock and commands

- Repository mathematical source basis: `03e2604dfcef278b01c60d19b05370fcec4194b6`
- Lean 4.19.0, compiler commit `6caaee842e94`, official Linux release
- Mathlib `c44e0c8ee63ca166450922a373c7409c5d26b00b`
- All ten dependency identities and clean tracked trees are checked against `SOURCE_V5_MANIFEST.json`
- Existing prepared environment: `./verify.sh`
- Fresh Linux directory: `./bootstrap.sh`

The archive contains sources, configuration, a bootstrap script, hashes, and passing receipts. It does not contain the large compiler/dependency binaries or caches. Fresh network bootstrap has not been re-downloaded a second time; the script's component acquisition/build operations were executed successfully in the research environment, and its shell syntax was checked.

## Remaining boundaries

This does not mechanize the full infinite-stream measure/atomic-mass theorem or arithmetical hierarchy. It does not prove that a physical system supplies the modeled observations, complete dynamics, source meaning, permissions, or safety labels. The two rank theorems have different label/coverage hypotheses and must not be interchanged. The minimum budget bounds bad-visit count, not the time of the last bad visit. Historical originality and external refereeing remain open.

Additional semantic readbacks confirmed the stated rank and finite-counting meanings. They were code reviews rather than independent compiler executions. The complete declaration statements and transitive footprints are in the passing receipt; source meanings and limits are mapped in `AUDIT_MAP.md`.
