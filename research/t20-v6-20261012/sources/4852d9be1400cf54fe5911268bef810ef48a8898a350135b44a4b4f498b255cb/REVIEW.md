# Independent qualification: reconstructed finite-contract iterator repair

11 October 2026 UTC. Bounded code review and fresh Python replay. All execution is isolated under this review directory; original intake, historical receipts, catalogue and v2 were not edited.

## Recommendation

**Accept the received repair as an additive current finite-reference successor, with the four accepted iterable boundaries and ordering caveat below. Preserve the exact old26 historical replay target and rational-hase-j source-bound dependency.** Give any promoted successor its own replay target and new bindings. Do not silently replace an `EXACT` historical copy or repin an old receipt. No broader API overhaul is required for this recommendation.

This is one genuine constructor invariant repair plus three useful defensive input-boundary hardenings/extensions. It is not a newly recovered R3, an 88-test successor, a theorem correction, a production adoption, or evidence that the historical 26-test PASS was false. The separate authorial 52-to-55 line is unaffected.

## Identity and exact scope

- Old source: SHA-256 `3c42622d5bebb3d07da5f231e7a8b22bc4d174f806f80a92ecf7817d21a29c06`.
- Received repaired source: SHA-256 `852609c327636305d8565549bfb7fbb4aba27076012b4e75861fa97d0460a9c0`.
- Fresh unified diff equals the supplied patch byte-for-byte. The only changed definitions are `Contract.__post_init__`, `valid_partition`, `as_reaches`, and `closure_basis`; public signatures are unchanged. See `EXACT_DIFF.patch`.
- The original `research/REPRODUCE.md:16` explicitly promises exact integer/Fraction arithmetic, rejection of invalid row masses, and freezing of validated mappings. Neither that document nor the inspected signatures/docstrings declares a general `Iterable` API. The unused `Sequence` import is not such a declaration either.

The clearest actual defect is the constructor: old code accepts a generator row of mass one, validates it, then freezes an empty row on its second traversal. The returned immutable contract has mass zero. The repair freezes precisely the rationalized triples validated in the same traversal and retains the existing rejection rules.

## Four qualified input boundaries

1. **Transition rows:** each kernel mapping value may be a finite iterable of valid `(outcome, successor, exact_probability)` triples. State/action/outcome membership, nonnegative exact probabilities, unit row mass, enabled-pair coverage and nonnegative exact costs still apply. The repair does not broaden the enabled-action-menu interface: those menus still need reusable sized containers.
2. **Partition validator:** `valid_partition` snapshots the finite outer iterable and each finite block iterable before using them. Invalid label merges no longer pass because their iterator was exhausted. Coverage, disjointness, nonempty blocks, labels, menus, costs and joint branch/next-block signatures remain the same checks.
3. **Fixed-policy reachability target:** `as_reaches` snapshots a finite iterable of hashable state identifiers as a frozenset. This retains set-membership semantics, including duplicate-insensitivity, through validation, graph construction and backward closure. It remains a finite-chain fixed-stationary-policy check.
4. **Linear action family:** `closure_basis` snapshots a finite family of finite matrices and finite row iterables. Actions still need the appropriate square dimension and exact integer/Fraction entries when used. **The output row family is not repaired:** `row_reduce` still expects sequence operations. Do not advertise generator support for all matrix inputs.

These scopes assume ordinary finite, stable input values. They are not promises about infinite iterables, shared exhausted iterator aliases, concurrent mutation, or arbitrary effectful container methods.

## Concrete old/new outcomes and residual restrictions

The independently replayed four supplied witnesses change as intended:

| Witness | Old | Repaired |
|---|---|---|
| Stored mass after accepting unit-row iterator | 0 | 1 |
| Validator accepts iterator block merging unequal labels | True | False |
| Reachable target supplied as iterator | False | True |
| Closure rank with iterator containing the shear action | 1 | 2 |

Half-mass, negative, float, bool and unknown-successor generator rows are rejected by both versions. The inherited immutable-mapping tests still pass.

**`quotient` and `sidecar` still require reusable, indexable partition containers and blocks.** Their calls to the improved validator consume one-shot input, but neither caller keeps that snapshot. Fresh repaired-code probes show:

- `valid_partition(c, iter(valid_blocks))` returns True.
- `quotient(c, iter(valid_blocks))` raises `TypeError: object of type 'tuple_iterator' has no len()`.
- `sidecar(c, coarse, iter(valid_blocks))` raises `ValueError: max() iterable argument is empty`.
- A reusable outer tuple containing an iterator block still fails in `quotient` with a non-subscriptable iterator error.
- Generator output rows in `closure_basis`, and generator enabled-action menus in `Contract`, likewise remain unsupported.

The normal workflow using `coarsest_refinement` returns tuple-of-tuple blocks and avoids these restrictions. Calling `valid_partition` on an iterator does not make that consumed iterator reusable. Sidecar's global minimum continues to depend on passing the coarsest admissible refinement; with a finer valid partition it encodes that chosen partition.

## Reusable-container semantics: one observable caveat

For stable tuple/list inputs, the modified formulas and decision procedures are unchanged. Fresh differential checks agree on 3,456 three-state contract/container variants, 17,280 partition decisions, 5,112 valid quotient/sidecar comparisons, 25,920 fixed-policy reachability comparisons and 810 linear-closure comparisons. These are finite diagnostic comparisons, not new theorem or unit-test counts.

**It would nevertheless be false to claim complete Python-observable equivalence.** Old `Contract` freezes kernels by iterating the input mapping; repaired `Contract` inserts rows while iterating the enabled-pair **set**. Consequently kernel mapping key iteration order may change and can depend on hash randomization. The per-key rows, within-row transition order and mapping values are preserved. A fixed-seed probe records input/old key order `((0, 'a'), (2, 'a'), (1, 'a'))` versus repaired order `((1, 'a'), (2, 'a'), (0, 'a'))` with equal mappings.

No ordering promise was found in the inspected documentation, and this does not alter the finite contract's mathematical law. It matters to callers serializing `kernels.items()` or relying on insertion order. Such consumers need an explicit canonical order, or a separately authorized order-preserving successor. This review does not modify the received repair. Eager snapshots can also change consumption timing and malformed-input exception precedence, including action consumption before an empty-output closure returns; these are outside the claimed mathematical value equivalence.

## Exact downstream caller and historical pins

The retained rational caller imports the old reference by a fixed relative path (`test_transport.py:73–79`), constructs its actual D1 quotient, checks the joint counting law, and compares projected concrete histories with seeded quotient histories. The original `SOURCE_BOUNDARY.json` pins that dependency to the old SHA. The caller, `rational_kernel.py`, and `FIXTURE.json` were copied unchanged into two isolated layouts with that same import-relative path; only the dependency differs.

- Exact old dependency: **162/162 checks, including 125 finite rows, pass**, normal and optimized Python.
- Disclosed repaired dependency substitution: **the same 162/162 checks pass** in both modes.
- All four stdout files are byte-identical, SHA `e072620588390aac946369f61a1f569872d163fe19f91791792b80328f81ca8b`.
- The original dependency-pin comparison accepts old bytes and raises the expected `RuntimeError: Retained input changed: …/research/contracts.py` on repaired bytes. **This was the single dependency preflight comparison from the original verifier, not execution of its full 3,097-pin/Lean verifier.** No historical receipt, pin, freeze, or source boundary was changed to manufacture a pass.

Thus the exact exercised rational Python caller is compatible at its reported law/fixture scope; its historical source identity is not interchangeable. A new edition may select the repaired finite diagnostic independently while retaining the old rational source-bound dependency. Promoting a changed rational dependency would need an explicitly new binding and replay record. Nothing here recertifies Lean source/object imports or extends the source theorem.

## Fresh evidence and reproduction

`run_review.py` is the complete local qualification driver; run from the workspace with `PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 python3 -B t20-depth-reassessment-20261011/contract_repair_review/run_review.py`.

- Old inherited suite: 26/26 pass, normal and optimized.
- Four added regressions on old code: 4/4 expected failures in both modes.
- Repaired suite: 30/30 pass, normal and optimized.
- Unchanged retained oracle on repaired code, both modes: 1,728 contracts, 8,640 candidate partitions, 252 value-bound instances, 4,752 conditioning instances pass.
- Exact downstream caller and differential controls: scopes above.

`RESULTS.json` records commands, exit codes, hashes, concrete errors, and counts; individual stdout/stderr files preserve the runs. `INPUT_BINDINGS.json` binds inspected executable sources, documentation, original boundary, and historical receipt; the driver verifies every bound source unchanged afterward. No external publication, repository adoption, v2 mutation, full-corpus rereading, theorem reproof, or full Lean replay was performed.
