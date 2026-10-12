# Independent review: actual typed finite sidecars

11 October 2026 UTC.

## Disposition

PASS within the frozen report's stated scope. No blocking mathematical, source-typing, compiler, or claim-transfer defect was found. This is an ordinary independent technical review; it does not authorize adoption, integration, or programme closure.

Reviewed candidate: `hase-finite-sidecar-realisation-20261011`.
Author freeze SHA-256: `6f28e9f7743241b371e23654efe476ce95e97cd251a0379639eb3d0f45b81c6f`.

The earned result is a finite deterministic table-to-source construction, exact joint branch/next-state observations under literal finite source composition, and a conditional cardinality minimum for a fixed ordinary-data/proof-slot architecture. It is not a realization of the full stochastic D1 contract.

## 1. Actual inherited calculus and compiler

The original owner is `P01AC.Has` in inherited `AllSyntax.lean`, with finite explicit formation, lookup, scope, substitution, and conversion premises. The candidate uses that actual judgement. The construction does not substitute a semantic model or an alternative typing relation.

`FiniteCorrectionTable.lookupPR` is structural recursion over a finite list using inherited zero choice and predecessor. `tablePR` nests two lookups. Its compiler is the inherited `P01AC.BooleanPrimitive.PR.compile`, whose syntax-directed `compile_has` returns original Has derivations and whose `compile_obs` proves raw numeral observations. These are restricted positive compiler results; no general compiler-completeness premise is assumed.

`SourceSidecarController.tableBody_has` substitutes actual State projections into this compiled polynomial. `controller_has` then constructs the nested Sigma reply and abstracts the State argument using original Has rules. `controller_hasE` is the inherited inclusion and `controller_hasJ` is literally HasJ.hasBase of that inclusion. The body-only dependency check confirms that the controller uses neither Joint natInduction nor Joint sigmaElim. The inherited grammar and objects were preserved.

## 2. Operational claim and boundaries

The nested Sigma reply is `(branch, (nextCoarse, (nextTag, evidence)))`. All three numeric outputs are computed from the same supplied source state. The observational theorem covers any raw input having the stated two natural observations, not merely a canonical input numeral pair. `runSource` carries the literal next-state polynomial into the next call; no decoder/re-encoder is inserted between steps.

`runSource_observes` establishes the exact finite list of branch observations and final two retained counts for each externally supplied finite list of deterministic tables. The source typing and the HasJ identities of the returned branch numerals are separately established. The history theorem does not itself construct an adaptive policy, supply randomness, or prove a probability law.

Bounds are appropriately external:

- State and Reply contain N, not Fin. A source typing alone gives no finite rectangle invariant.
- The exact tabulated-value specialization requires `z < Z` and `k < M`.
- `ClosedRectangle` and `runCodes_bounded` supply an explicit next-state closure premise. They do not bound the output branch or justify an arbitrary nonrectangular code set.
- Ragged rows, absent rows/columns, and empty tables follow the explicit fallback. The controller uses fallback 0. This total behavior does not grant an authorized action or a faithful interpretation to an out-of-domain code.
- Empty action sequences preserve the input. An empty table is not an enforced empty enabled-action menu. There is no source policy/deadlock/terminal-cost interface here.

Independent controls check ragged and out-of-range fallback, an empty well-typed controller, a well-typed 1-by-1 table that emits nextCoarse 2, and a second execution that consequently falls back. They also check the vacuous zero-count encoding case and the impossibility of mapping a nonempty Fin n into Fin 0. These controls passed kernel elaboration.

## 3. Proof slot and minimum

The fixed proof type is `Evidence = Id_Raw(I,I)`. Its canonical witness establishes only that displayed trivial identity. It authenticates neither the numeric label nor an external source, episode, right, or warrant.

`encoded_identity_iff` uses actual typed numeric projections and inherited count separation. It proves precisely that canonical joint records admit actual HasJ identity iff both ordinary natural coordinates agree. It retains cross-coarse reuse of an ordinary tag.

For varying proof realizers, `proof_slot_cannot_separate` uses inherited identity-proof uniqueness and source arrow congruence through actual J. The independent `same_data_no_proof_observer` theorem confirms that any two well-typed proof realizers in that fixed slot, with equal coarse value and tag, cannot be separated by an actual typed natural-valued observer. No raw-syntax or derivation-tree equality is claimed.

`finite_fibre_lower_bound` is a genuine pigeonhole consequence of this source-observer restriction. Its assumption explicitly stipulates pairwise source-observable required distinctions. `common_alphabet_exact` combines this lower bound with ordinary projection-based finite labeling. It accepts the fibre counts as inputs. It does not calculate D1's coarsest partition, prove that arbitrary D1 distinctions have such source observers, or minimize over every source representation architecture. The frozen report states these limitations correctly. The independent negative checks did not rely on a substitute model for the positive source construction; inherited faithful soundness/count separation is legitimately used for the numerical nonidentity direction.

## 4. Direct D1–D3 comparison

The inspected synthesis source archive has the supplied SHA-256 `38ed92bbec0877b5dc55ea049689cf25945d9d9d5fd253cb4bbfc9e9f88cf753`. Its D1 contract separately requires labels, enabled action menus, immediate costs, and a joint outcome/next-block probability kernel. The reference Python implementation uses exact rational probabilities; the written finite-kernel theorem is not restricted to an implemented rational sampler.

The candidate realizes deterministic natural-valued tables and their exact source computations. Numeric label, cost, or menu-indicator tables can be read, but their intended interpretation, authorized-action enforcement, finite-outcome range, and class-preservation premises are not automatic. Applying this layer to an already justified deterministic quotient is a bounded application of the construction. Calling it an implementation of arbitrary real stochastic kernels, D1's refinement algorithm, or stochastic D3 history laws would exceed the evidence.

An externally chosen branch or table supplies a particular realization; it does not prove the selection law. No sampler, authentic randomness interface, arbitrary-real probability representation, Bellman-value preservation, or almost-sure reachability proof is supplied by this packet. Nor does a tag establish source authenticity or actual human warrant. These are explicit boundaries in frozen `RESULT.md`, not unresolved defects in its narrower theorem statements.

## 5. Independent replay and dependency evidence

Six frozen additive modules and two independent reviewer modules were compiled into a fresh reviewer output directory with installed Lean 4.19.0, commit `6caaee842e94`, and `--trust=0`. Every final command exited 0 with no warning, error, or sorryAx. No candidate output directory was available for imports. No retained dependency was rebuilt, and neither candidate nor inherited files were written.

Before and after replay, the reviewer verified all ten author-frozen files, 244 inherited source-file pins drawn from existing binding manifests, and all 2,835 inherited imported-object pins. The final environment audit records 2,841 imported objects; every inherited object in it was already pinned before replay. Fresh additive/reviewer objects are separately identified by source and object hashes in `REPLAY.json`. These observed object hashes and retained source bindings are not a claim of freshly rebuilding all predecessor sources.

The independent audit checks allowed axioms for 19 main candidate/reviewer declarations and then checks the actual compiler, proof-uniqueness, and J paths. Only standard propext, Classical.choice and Quot.sound are allowed. Positive source construction/computation excludes the named semantic fundamental-theorem shortcuts. Controller-only body traversal separately excludes the completion constructors. Negative count-separation and typed-natural extraction results retain their disclosed inherited semantic dependencies.

Audit calibration is preserved transparently. An initial reviewer audit tried to exclude completion constructors from the proof-slot theorem's whole value-dependency graph. Inherited structural transformations over arbitrary HasJ proofs include cases for all source constructors, so that exclusion was stronger than the claim. It was restricted to the actual original-Has controller wrappers while retaining semantic-shortcut exclusions and the source-J checks for the proof-slot result. The second full fresh additive replay passed. The initial diagnostic logs remain labeled as an initial attempt. Likewise, old author diagnostic failures are not accepted proof evidence.

After the mathematical freeze, the author supplied metadata-only verification updates. `AUTHOR_METADATA_BINDING.json` binds SOURCE_BOUNDARY.json at `e94ae8b2b9f2d292219d1a81d198c7297368ff7efe215e476856cbe79c33a6f4` and the author replay receipt at `7d09f6ae380a68d39e07d4e88c71b9b063836f7a8f3ca1b245dfe4713528bdd4`. The reviewer inspected verify.py, verified every declared author pin and the author log digest, and checked that its 2,835 first-resolved inherited objects and LEAN_PATH exactly match the independent baseline. The wrapper itself was not rerun by the reviewer; the independent replay above supplies the compilation evidence. None of the ten mathematically frozen files changed.

## 6. Evidence and stopping boundary

- `REPLAY.json`: exact frozen identity, toolchain, eight final compilations, source/object hashes, and before/after preservation checks
- `REVIEW_RECEIPT.json`: review scope and artifact identities
- `candidate/`: copied author-frozen source and report
- `IndependentBoundaries.lean` and its log: independent edge cases and proof-only observer exclusion
- `IndependentAudit.lean` and its log: independent axiom, value-dependency, and imported-environment checks
- `INHERITED_SOURCES_BEFORE.json`, `INHERITED_OBJECTS_BEFORE.json`, and `ACTUAL_IMPORTED_OBJECTS.json`: dependency evidence
- `TRANSFER_INPUTS.json`: inspected synthesis/comparison inputs
- `AUTHOR_METADATA_BINDING.json` and `author-metadata/`: verified late author verification metadata

No protected source edit, full dependency rebuild, rule adoption, integration, stochastic extension, philosophical-warrant revision, or programme closure was performed or authorized by this review.
