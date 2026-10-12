# Exact source map and remaining trust boundary

This is a new mathematical source-AST model in Lean 4.19.0. It does not redefine or adopt the supplied Python source. Its positive theorem is a real induction over independently evaluated constructors, not an alias for target checking.

## Source owners and representation

The Python owner is the unchanged reconstructed attempt-0001 `source/reference.py` (the canonical reference.py has identical bytes). `SourceProof` represents a dictionary already validated to have exactly the fields of one of the seven rule constructors. TypeCode represents the corresponding validated tagged sequence: `v/n`, `bottom`, `arr/A/B`, `all/A`. Term represents `i/k/s/zero/one` or `app/f/x`. Boolean, negative, foreign or malformed indices have no TypeCode representation; raw rejection of these is not silently claimed mechanised.

`SourceRepresentation.proofTree` is an explicit generic native-tree encoding. It retains all rule and field strings, field-name key nodes, arrays and integer leaves. `proofTree_shape` proves that its generic tree resource counts equal the source model's direct counts. Python lists and tuples are identified only as tagged-tree values. Dictionary order and aliasing do not become semantic proof coordinates.

## Equation correspondence

- reference.py `_wf_type`: `sourceScoped`; `sourceScoped_eq` proves equality to the inherited finite target scope checker
- reference.py `shift_type` at the nonnegative shifts used by substitution: `sourceShift`
- reference.py `instantiate_type`: `sourceSubstitute`, using the exact less/equal/greater binder-index cases; `sourceInstantiate_eq` proves equality to inherited `instantiateType` for all encoded type trees
- reference.py `_head_step`: `sourceHeadStep`, independently following I/K/S/left-spine cases; `sourceHeadStep_eq` proves equality to the erased inherited certified successor
- reference.py `raw_go`: `sourceCheckCore`, independently returning plain term/type pairs across seven rule constructors, including all_i depth increment, exact app domain equality, all_e substitution and explicit trace start/transition checks
- reference.py successful `go` work charges: `sourceRun`/`finish`; every child output charge and parent output term/type charge are accumulated, intermediate size/depth/integer guards stay active
- proof_export.py `_cert`: `encode`; reduce expands to exactly trace.length-1 nested Cert.step constructors, separately from source trace validation
- inherited FiniteBridge.lean `check` and `checked_sound`: unchanged target checker and semantic theorem

Neither `sourceCheckCore` nor `sourceRun` calls `encode`, `check`, or `certifiedHeadStep`. The source computation has no target-acceptance premise. The proofs use the independently established substitution/head-step lemmas and induction on the actual seven source constructors.

## What is proved

`source_checker_constructor_erasure_square`: if resource-aware sourceCheck returns `(t,A)`, the inherited checker accepts encode(p), and its returned object's term is t and type is A.

`source_checker_sound`: every such successful result is accepted by the interpreted type under every semantic environment, using the inherited checked_sound theorem.

`sourceCheck_input_guards`: a successful model call has initial depth<=100, exact encoded native-tree shape bounds, at most 20,000 proof visits and proof-call height<=100. The last two guards are redundant under the encoded full transport-tree bounds, rather than omitted as assumptions.

The axiom footprint is propext and Quot.sound; no sorryAx, user axiom, classical choice or native_decide occurs in the new main proofs.

## Why this is not circular and why refusal is asymmetric

A malformed trace can erase to an accepted Cert, since exporter erasure keeps only its length. The source still checks its actual content. `erased_checker_acceptance_is_not_source_acceptance` is a kernel-checked countertheorem to replacing the source checker with target acceptance. Empty, wrong-start and invalid-transition traces, bad application, nonpolymorphic elimination, ill-scoped variables and depth-limit failure are separate kernel-checked refusal controls.

## Exact remaining boundary

The formal input is SourceProof, not bytes or arbitrary Python objects. No theorem states that CPython executing reference.py always corresponds to this model. The source-to-model correspondence is a branch-by-branch source analysis plus separately executed cross-language tests. Strict UTF-8/JSON parsing, duplicate/extra fields, native hostile/mutable objects, byte-size/serialization limits, host stack/memory exceptions and the exporter’s 512-constructor / 16-row / 1 MiB refusal guards remain outside this constructor theorem. They must not be erased from a later whole-pipeline theorem.

The resource-aware model checks the declared root transport shape, initial depth, all intermediate output shape and aggregate 2,000,000-node work. It models logical resource refusal, not physical allocation scheduling or construction-time memory usage. The original substitution implementation’s before-allocation guards remain necessary even where final accepted-output conditions coincide mathematically.

The original P03 U03/U04 reformulations and historical obligation labels are not automatically closed or modified. Q1f's original source required two real source repairs before its own target qualified; those changes are recorded independently.


## Partial exporter gate and its non-totality witness

The acceptance-only constructor theorem is now explicitly named `source_checker_constructor_erasure_square`. It proves target behavior for mathematical constructor erasure, without asserting that the textual exporter returns.

`SourceExportBoundary` separately models `_cert`'s actual 512-unit work guard. `partial_constructor_export_square` requires this partial constructor export to return and gives target acceptance, equal output term/type and a 512-node target bound. The explicitly named `source_checker_export_square` lists both source acceptance and that partial export success as premises. It still does not assert text-level name/module/byte/host success.

The source-accepted balanced identity at depth 8 has 7,916 native input nodes and 1,022 certificate-construction units. Python's exporter refuses it at the declared 512-unit gate. This is intended partiality, not an exporter bug. The same source model acceptance and separate export refusal are kernel-checked in `checker_acceptance_not_total_export`. The independent actual-Python witness is retained at `private-locator:e1fb971a0fd4a8d28a90` and its standalone reproducer.

`SourceBranchControls` adds explicit trace singleton acceptance, empty/wrong-start/normal-form/incorrect-successor refusal, child/scoping refusal branches across all seven rules, four capture-index controls, and a universal theorem that resource checking cannot turn semantic-model refusal into acceptance. These controls do not claim to cover every malformed raw Python object.
