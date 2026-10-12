# Does the reconstructed repair need a Codex successor entry?

11 October 2026 UTC. Targeted follow-up to the intake comparison. No sealed v2 or source API was edited.

## Decision

**Recommend an additive predecessor/successor entry carrying the repaired code and four regression tests, rather than treating this as extra validation only.** Label it a *reconstructed finite-reference input-boundary hardening candidate*, with a precisely bounded accepted-input contract. It is not a newly recovered R3 implementation, mathematical theorem correction, or proof that v2's recorded 26-test replay failed.

There is **no explicit `Iterable` annotation or documented promise of general generator support** in the four old APIs. Accordingly, calling all four violations of an expressly promised Iterable contract would be unsupported. But the old constructor does accept a valid one-shot row, validate mass one, and return an immutable object whose stored row is empty. This directly defeats the documented promise to freeze the validated mappings. The other three changes prevent silently wrong answers on previously unspecified one-shot input shapes; their classification is defensive hardening/input support extension unless a broader API contract is deliberately adopted.

## What sealed v2 actually contains

The delivered ZIP, SHA-256 `d7fce54a6a199ff297aba58f064a9ce1d3368a9b883311207f468c4f2025cfa5`, was opened read-only and both following members freshly hashed. Under `Orthemology_T20_Consolidated_v2_20261011/public_candidate/`:

1. `replay/finite-contracts/contracts.py`
2. `proof-families/rational-hase-j/rational-kernel-additive-preservation-20261011/payload/received-cross-front-synthesis-20261011/Orthemology_T20_Whole_Corpus_Synthesis_20261010/research/contracts.py`

Both are the old 13,980-byte SHA `3c42622d5bebb3d07da5f231e7a8b22bc4d174f806f80a92ecf7817d21a29c06`. `PUBLIC_PROJECTION.json` identifies the first as an **EXACT** original copy, and the second as a required import-relative/source-bound dependency. `SOURCE_INDEX.md:813` lists its owners as `Pro-26-contracts.py`, `rational-hase-j`, and `code26`.

`REPLAY_SCOPE.json` and `replay_selected.py:18–22` promise the 26 finite-contract tests, normal/optimized execution and finite exhaustive oracle. `SELECTED_REPLAY_VERIFICATION.json` records successful execution at precisely that scope. These do not promise all Python input representations are accepted. No reconstructed successor SHA `852609c327636305d8565549bfb7fbb4aba27076012b4e75861fa97d0460a9c0` appears in the v2 source index, projection or contents manifest.

The separate `affected_nodes` repair appears as an ET-14 correction in `CORRECTION_INDEX.json:295–299`. That belongs to the different authorial **52→55** line. It does not fix any of the old26 APIs below.

## Exact API and documentation assessment

Line references below address v2 `replay/finite-contracts/contracts.py`, which is byte-identical to the archived provisional source.

| Function | Actual signature/type/documentation | Old behavior and bounded conclusion |
|---|---|---|
| `Contract.__post_init__(self)` (30–67) | Dataclass fields `states/actions/outcomes: tuple`; `kernels: Mapping` without a value-type annotation (20–28). No constructor docstring or `Iterable` declaration. `research/REPRODUCE.md:16` says the class “rejects floating-point probabilities and invalid row masses, and freezes its validated mappings.” Source line 60 says validation cannot silently be invalidated. | Lines 53–59 validate a row and line 67 iterates it again to store it. A valid generator of one mass-one transition is accepted, then frozen as empty. This is a genuine accepted-input/stored-invariant defect; supporting the finite iterator once or explicitly rejecting it are possible coherent contracts. The supplied successor takes the former route. |
| `valid_partition(c,blocks,coarse=None)` (89–104) | No annotation or docstring. The implementation uses repeated iteration, `b[0]`, slicing and `len(blocks)`, so a reusable sequence of indexable blocks is an implicit working requirement. Original tests use reusable lists/tuples. | An outer one-shot iterator is consumed while flattening at line 90. It can then bypass all label/kernel checks and return `True` for an invalid merge. Snapshotting broadens reliable finite-iterable support and hardens validation; no explicit prior Iterable promise was found. |
| `as_reaches(c,start,target,policy)` (181–201) | No type annotations. Only docstring: exact finite-chain almost-sure reachability for a fixed stationary policy. Original tests pass target sets (`test_contracts.py:125–138`). | `set(target)` at line 183 consumes a one-shot target; later membership and the second set conversion use exhausted input, returning `False` for the demonstrated reachable target. `frozenset(target)` fixes this unspecified-input boundary; no named Iterator/Iterable guarantee was found. |
| `closure_basis(outputs,actions)` (302–313) | No type annotations or docstring. Matrix rows require sequence operations; original tests pass a tuple of tuple matrices (`test_contracts.py:218–237`). Mathematical D8 specifies a finite family `A1,...,Am`, not its Python container protocol. | Dimension validation at line 306 consumes a generator of allowed matrices, so line 309 performs no updates and returns an undersized basis. Snapshotting makes the finite iterable representation reliable. This is executable hardening of an untyped boundary, not a counterexample to D8. |

The `Sequence` import at line 10 is unused and cannot create a declared sequence contract. Conversely, the absence of an `Iterable` annotation cannot establish that generators were expressly forbidden. The honest classification is **under-specified boundary**, with the constructor's documented frozen-valid-state invariant giving the clearest correctness obligation.

The original implementation documentation is from the full archive's `prior_work/previous_synthesis/Orthemology_T20_Whole_Corpus_Synthesis_20261010/research/REPRODUCE.md`, SHA `a632439d83142e606c2bdd1532cece996b25aef7181d19f8c45dcf78b5860f7c`. The theorem/source interface is `documents/CROSS_FRONT_SYNTHESIS.md`, SHA `8aad39f6fb030620059edd4e0639f58078537a10181836b64089f6d82dbe10f4`, especially 26–52, 391–412 and 454–460. `INPUT_CONTRACT_SEARCH.json` records the bounded text search; no claim of inspecting every historical document for an API promise is made.

## Integration consequence

- Preserve the two exact old v2 copies and their historical replay/hash bindings. In particular, do not overwrite the source-bound rational-hase-j dependency with a changed file.
- Add the separately received repaired code, four new tests, exact patch, predecessor/successor hashes and reconstruction attribution to the next additive intake/handoff. Explicitly state finite iterables accepted at these four boundaries, and that `quotient`/`sidecar` still require reusable partitions. This record is needed because actual implementation bytes changed; calling it only an extra test suite loses the correction.
- If a new working edition promotes the successor as the default finite diagnostic, give it a separate replay target and new evidence/status bindings. Carry the old26 target as historical reproduction. Existing v2's 26-test PASS remains true; do not silently change its scope to 30 tests.
- Treat adoption as a scoped review decision. This evidence supports carrying a hardened successor candidate; it does not by itself mandate replacing a faithfully preserved historical component or invalidate v2's scientific claims.

## Additional compatibility evidence

The intake had already observed 30/30 tests passing in normal/optimized Python and all four regressions failing against exact old code in both modes. This follow-up additionally read v2's complete 4,421-byte `exhaustive_oracle.py` (SHA `423cee2356215f9e7e8372fb1adc183d9099243f256011bcacc78af694e139f2`) and ran an unchanged copy against the repaired code in a disposable intake directory. Both modes pass: 1,728 contracts, 8,640 candidate partitions, 252 value-bound instances and 4,752 conditioning instances. Evidence: `SUCCESSOR_ORACLE_RUNS.json` and corresponding `fresh-local-evidence/repaired-v2-oracle-*` logs. No code, tests, or API was patched during this comparison.


## Portable edition note

Original intake file/path names in the report identify its source custody. The public current assessment is in this directory and the source hashes remain exact. Private transfer identities, bulk archives and unfiltered logs are not republished. Public summary evidence is CUSTODY_UPDATE.json and CONTRACT_REPAIR_STATUS.json; actual successor code/tests are under replay/finite-contracts-reconstructed. Exact changed code is retained separately.
