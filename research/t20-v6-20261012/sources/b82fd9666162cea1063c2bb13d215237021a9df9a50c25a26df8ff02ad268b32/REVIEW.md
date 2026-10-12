# Independent semantic review

## Verdict

PASS for the bounded constructive reference-extractor contract at the exact source hashes in `reviewed-source-hashes.json`. No blocking semantic or implementation finding remains. This verdict is not integration, adoption, practical scalability, domain-semantic soundness, or research closure.

The review was performed independently in `review_semantic/fresh/`. Only source files and scripts were copied there; the final replay began with zero local `.olean` files. All eleven frozen modules and all four new modules were rebuilt in dependency order. The submitter's `.olean` files were never in the review `LEAN_PATH`. Existing pinned Mathlib/Lean libraries were used, not rebuilt from source.

## Verified semantic contract

- `tuples` preserves ordered premise positions and occurrence multiplicity. Its zero-arity case is a singleton even over an empty input list. `shapes` and `trees` give executable lists of actual inductive finite trees, and `mem_trees` proves exact coverage of height-bounded syntax. Neither an equality decision on trees nor deduplication is used.
- `validDecidable` checks recursive child validity, each child's required judgement, and the original guard on the exact ordered vector of child supports. `accept_iff` additionally binds exact root judgement, exact support equality, and recomputed rational cost. The verifier does not certify minimality by itself.
- Costs remain occurrence-additive: repeated children are counted once per premise position even when their supports or runtime subvalues coincide. Support union is idempotent; price summation is not. The returned repeated-premise tree `4(0(),0())` costs `7/6`, not `2/3`.
- `extractRound` obtains the numeric table value, returns immediately for `none`, and otherwise enumerates finite trees and selects the first exact-cost accepted tree. It does not obtain a tree by evaluating the numeric theorem's existential proof. `extract_sound`, `extract_complete`, and `extract_cost_eq` justify every bounded output, including absent keys.
- `extract_global_cost_eq` is exact projection to the inherited fixed-bound numeric compiler. Under nonnegative rule prices, `extract_global` proves validity, the exact key, and least cost among all valid finite trees at that key; `extract_none_iff` proves global unreachability equivalence. The inherited bound is `card J * (card grammarSupport + 1)`. Bounded extraction and numeric projection do not need nonnegativity; unrestricted least-price correctness does.
- Guards need not be monotone. Correctness preserves each exact support vector rather than using support-inclusion pruning. Ambient evidence need not be finite.
- First-match ties are deterministic relative to the supplied ordered list and requested height. They do not minimize node count or give canonical/stable tree identities. The final same-order control returns one versus four nodes at heights one and four while both prices are zero.

## Executability and assumptions

Runtime use requires executable grammar fields, supplied finite enumeration instances for judgements and rules, decidable equality for judgements/evidence, executable decisions for every guard, and a complete explicit `RuleList`. Its completeness proof is erased. Duplicate rule labels are allowed. No additional decision procedure for tree equality or finite ambient evidence is required.

Accepted sources contain no `sorry`, introduced `axiom`, unsafe code, `native_decide`, `implemented_by`, or `extern` declaration. Final replay output contains no `sorryAx`. Axiom reports include ordinary inherited `propext`, `Classical.choice`, and `Quot.sound`, including reports for definitions whose types contain erased proof dependencies; these reports must not be misrepresented as an absence of classical proof infrastructure.

As an additional computational check, Lean emitted C for `Enumeration.lean` and `Witness.lean`. Inspection of `extractRound` shows the numeric compiler/read call followed by an absent-value branch or `search`; `search` calls executable tree enumeration and `List.find?`. The emitted code contains no scanned classical-choice or noncomputable catalogue/proof-oracle identifiers. This is supporting code inspection, not a separate formal compiler-correctness proof, and the emitted C was not separately compiled and run as a native binary.

## Fresh evidence

Final `run-review.sh` completed successfully:

- Eleven frozen and four new modules rebuilt with Lean 4.19.0 and warnings as errors.
- 23 actual-tree checks passed twice, once through `#eval` and once through `--run`.
- 17 inherited numeric controls also passed, for 63 `PASS` lines in the final replay log.
- All three supplied semantic mutations were rejected at their intended proof obligations: omit recursive validity, delete the nullary Cartesian tuple, and replace exact support equality with subset inclusion.
- Twelve independent adverse checks passed: empty rule type at bounded and global calls; seed-first/unary-first ties; duplicate-list multiplicity (14 versus 3 trees at height three); a genuinely non-monotone guard accepting empty support but rejecting its strict extension; rejection of the corresponding actual invalid tree; and negative prices reaching -4 at height five while the fixed grammar-bound result is 0.
- Two independent verifier mutations were rejected at the exact `accept_iff` obligation: accept an overstated cost via `cost <= claimed`, and ignore the requested root judgement via a tautological equality. Negative-control error-recovery `sorryAx` occurs only in rejected mutation logs.

All eleven frozen sources were independently compared with both their bound digests and the original predecessor bytes. Pinned environment-file hashes and the Mathlib revision in `BINDING.json` were checked. Current accepted sources and the replay copies matched the final review snapshot after execution.

## Resource and claim boundaries

This is exhaustive bounded reconstruction after numeric compilation, not an efficient witness-reconstruction algorithm. Enumeration is eager before `find?` scans the list. The raw list-length recurrence is `N(0)=0`, `N(h+1)=sum_{r in rules} N(h)^arity(r)`, counting duplicate rules and treating the nullary power as one. This explains rapid growth without asserting a measured runtime or formal complexity bound. The numeric table and tree-extraction resource costs are distinct. No global-height enumeration of the large ordered/repeated grammar was attempted; those runtime controls intentionally use height two. Global correctness is supplied by the general checked theorem and tractable global controls.

The review proves no source authenticity, admission soundness, external semantic warrant, Python-prototype correspondence, deployment, or integration. It does not certify the whole existing Mathlib/toolchain implementation, practical memory limits, or performance. No predecessor or accepted source was edited by this reviewer; all reviewer writes stayed under `review_semantic/`.

## Exact new-source binding

- `Enumeration.lean`: `c5df2d89314f78e45c7d4a2906ce081d38c58524f1d577dcb1fee049bd39313b`
- `Witness.lean`: `d5d7fe1449f82f4cf62504b543cdd1068a9fcde9e70603644c15f2945af43ca0`
- `WitnessControls.lean`: `07728cc7c4cda2c59c0db57d794ed358a1369a9533fe3f5ffd783e027d99f9b5`
- `Main.lean`: `a16e74aa2e8701d9159fd5e7b635fbc7e2880ae2c37ca9028be65500bbdfad70`

All dependency, mutation, specification, result, and harness hashes are in `reviewed-source-hashes.json`. The review receipt binds that snapshot and the decisive logs.

## Commands and artifacts

From the package directory:

1. `./review_semantic/run-review.sh`
2. `./review_semantic/check-independent-mutations.sh`
3. `R="$PWD/review_semantic/fresh"; "$R/run-lean.sh" -c "$R/Enumeration.c" "$R/Enumeration.lean"; "$R/run-lean.sh" -c "$R/Witness.c" "$R/Witness.lean"`
4. `python3 review_semantic/verify-binding.py`

The driver records the zero-olean starting condition and exact external dependency path in `logs/environment.log`. Its underlying compile commands are in the copied `fresh/replay.sh` and `fresh/run-lean.sh`; all paths are reviewer-local except the pinned Mathlib/toolchain installation. Final evidence is in `logs/final-replay.log`, `logs/submitter-mutations.log`, `fresh/mutations/*.log`, `logs/adverse.log`, `logs/independent-mutations.log`, the two named independent mutation logs, and `logs/c-emission.log` / `logs/c-scan.log`.

Earlier snapshots and logs are retained as superseded development evidence. An initial reviewer invocation used a relative path after the launcher changed directories and failed to locate the file; it was corrected to an absolute path. A first predecessor-comparison helper similarly used an unresolved relative parent and was corrected before the successful comparison. Neither failure is counted as evidence for a passing semantic check.
