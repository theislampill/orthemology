# Imported compiler transport into the open-term full-PER test

10 October 2026. The source-to-mirror gap in the preceding isolated test is now closed by kernel-checked imported-source theorems. **The literal `HasE [] c3 (W q)` remains OPEN.** No new full-HasE interpretation or completeness theorem is claimed.

## What changed

The previous reviewed package proved standardness and typed endpoint equality for a faithful formula mirror, with its source correspondence independently inspected. This additive package imports the unchanged original definitions and proves the correspondence in Lean.

`ImportedCompilerTransport.lean` establishes:

- `map_abstract`: the actual imported whole-subterm K-priority abstraction commutes with the translation to the reviewed polynomial mirror.
- `interp_abstraction_beta`: the actual source abstraction has the required behavior at arbitrary **open-term** valuations, not just embedded closed source environments.
- `source_plus_sound`: every constructor of the original eight-generator `PolyConvPlus`, including the atom/application bridge, preserves the new raw conversion relation at arbitrary open-term valuations.
- `original_q_poly_exact`: the imported `redundantExpr.closed` translates exactly to the reviewed q polynomial. This proof invokes the original `redundant_closed_exact` theorem, rather than treating its printed statement as an assumption.
- `original_p_eval_exact` and `original_q_eval_exact`: the actual original endpoints translate to I and the reviewed q under every original evaluation environment. The difference between the source's zero-filled default environment and the mirror's I-filled default environment is explicitly discharged by closed-evaluation independence.
- `original_endpoints_related`: the actual imported endpoints are related by the reviewed open-term full-PER `N → N` relation.

The transport is not obtained by collapsing the original carrier. `embed_injective` proves injectivity, and `embed_conversion_iff` proves preservation **and reflection** of raw conversion between embedded source terms. The retraction sends fresh semantic variables to the source's inert zero marker and is a homomorphism for the combinatory equations. `original_raw_endpoints_still_distinct` then retains the inherited raw nonconversion of the original endpoints. Typed PER equality and raw conversion remain different relations.

## Exact inputs and fresh build

The read-only GitHub acquisition used repository `theislampill/orthemology`, immutable commit `7efc6217c090b92d65f2c4cb8b011c18eb96bf7c`.

`UArrowAndCompilerControls.lean` has an exact local import closure of 83 project modules. Every module was retrieved at that commit from its source-store path. `ACQUISITION.json` binds module name, import list, SHA-256 and Git blob SHA-1. `PINNED_SOURCE_INDEX.json` and its acquisition receipt preserve the source-index evidence linking those paths and digests to the retained repository snapshot.

All 83 unchanged project modules were compiled successfully. The local Mathlib dependency is the existing pinned revision `c44e0c8ee63ca166450922a373c7409c5d26b00b`. Two absent object modules, `Mathlib.Algebra.MvPolynomial.Polynomial` and `Mathlib.Algebra.MvPolynomial.Funext`, were compiled from that pinned local source into the new package's output area. Existing package objects were used read-only. No upstream source, existing package object or protected project file was edited.

The preceding three isolated proof files are byte-identical copies of the independently reviewed versions. The earlier reviewed directory and manifest remain unchanged. Source comments recording older unavailable-runtime statuses are retained verbatim as historical source bytes; the present build receipt establishes only this new replay's actual scope.

The new transport theorem dependencies are ordinary Lean `propext`, `Classical.choice` and `Quot.sound`; `source_plus_sound` is axiom-free. No new axioms, admitted proofs, unsafe implementations or oracle evaluation are used. This is a source-and-kernel transport result, not simply another formula comparison.

## Precise conclusion

The imported original compiler can now be used directly in the previous new-to-project separator-class exclusion. In the finite open-term applicative reduct, with the **full** conversion-saturated PER Church interpretation and ordinary extensional arrow relation, the actual original endpoints are related at `N → N`.

For a whole HasE model that extends this reduct and uses the specified represented identity convention, these endpoints cannot be separated by making that identity empty. This remains conditional on that model extension. The present source imports do **not** turn the inherited F/G soundness theorem into soundness for this different full-PER interpretation. The inherited F/G interpretation has its own heterogeneous-link/uniformity clauses.

Still not established:

- a fundamental theorem for all actual HasE rules in the newly tested interpretation;
- orbit-PER admissibility in every syntax-generated Henkin universe;
- a derivation or nonderivability proof of the literal original HasE target;
- raw conversion of q to I, uniqueness/computable extraction of the standard count, or semantic completeness.

The retrieved source closure enables a subsequent rule-level test without re-fetching or guessing the actual formation premises. It does not close the programme.

## Reproduction

Run `python build_sources.py` to verify and compile the exact source closure against the already-pinned local Mathlib package. `BUILD_OUT` selects a separate fresh output directory. Then compile the four files in `proofs/` in order: `OpenTermStandardness`, `FrozenCompilerMirror`, `PERInterface`, `ImportedCompilerTransport`, with that output directory and the recorded package library paths on `LEAN_PATH`.

`replay.sh` performs the full fresh-output replay and preserves the receipts. `validation/INDEPENDENT_REVIEW.md` records the completed separate review. See the final manifest for exact delivered file hashes and the separate review's precise scope.
