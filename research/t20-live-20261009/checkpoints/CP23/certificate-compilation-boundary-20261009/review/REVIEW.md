# Independent review: finite grounded-rule compilation

9 October 2026. Revision-bound mathematical and implementation review. No blocking defect found in the inspected revision.

## Findings

- **Tree theorem:** Removing an ancestor with the same scoped judgement as a descendant preserves the declared substitution interface, only removes evidence requirements, and only removes nonnegative occurrence charges. Finite node count supplies termination even at zero price. The resulting height bound is `n`, independently of numerical cost discreteness. Finiteness of the bounded-height grammar then gives the global Pareto frontier and attainment. Childwise dominance is preserved by both support union and additive tree cost, so the synchronous recurrence computes the normalized height-`h` family and reaches a fixed point by round `n`.
- **Exact-support qualification:** Unrestricted loop removal can shrink support. Restricting removal to matching judgement and matching subtree support preserves exact support. Nested support sets have at most `m + 1` constant-support blocks along a branch, each containing at most `n` judgements after reduction. The stated `n(m + 1)` attainment bound is valid.
- **DAG theorem:** The earliest representative of an original premise precedes the selected parent in the original premise-first topological order. Redirecting premise references to these representatives therefore preserves acyclicity and the ordered premise judgements. Root restriction leaves a subset of original rule occurrences, so support and nonnegative once-per-node cost cannot increase. Enumeration of one rule or absence per judgement covers every resulting reduced graph; rejecting only root-reachable missing premises or cycles is correct.
- **Sharing obstruction:** The four-judgement example has minimum tree cost `9` and minimum DAG cost `5`. A standalone cost-`4` proof of `a` strictly dominates its cost-`5` proof through `p`, although the latter shares `p` with `b` in the best completed DAG. Consequently the intermediate pair-only pruning is genuinely unsound for that shared-node objective. This does not challenge normalization of a completed terminal DAG catalogue.
- **Boundaries:** Nonnegative rational/real weights do not invalidate either finite-dominator argument. Exact effective arithmetic is an additional computational requirement. The negative self-loop, infinite nullary-rule family, and nonadditive size-charge examples correctly separate distinct failure modes. Finite printed schemata do not establish finite fully scoped grounding. The theorem does not supply the missing finite interface or proof-normalization result for HasE, and it does not certify philosophical or epistemic application premises.

Two wording suggestions from this review were incorporated: “at most n” in the summary and “cannot be strictly dominated” in the finite-frontier proof. No mathematical claim needed withdrawal.

## Implementation and fresh replay

`compiler.py` follows the declared algorithms: the tree step uses the preceding round only; immutable witnesses preserve ordered and repeated premise positions; DAG enumeration is whole-graph and root-specific; `prune_dag` implements earliest representatives. Tree traversal charges copied/shared Python objects once per syntactic occurrence, while DAG traversal charges each reachable indexed node once. Generated witnesses use input rule records.

Fresh full replay passed all **12 tests**, with **2,517 grammars**, **10,520 traversed compiled witnesses**, and **250 seeded root-reachable DAG/tree-unfolding cases**. The small-grammar comparison is against a separately written, unpruned height-four **tree** pair oracle; it is not an independently exhaustive DAG-frontier oracle. The reviewer harness runs the whole submitted suite without replacing the author's `CHECK_RESULTS.json`:

    python3 certificate-compilation-boundary-20261009/review/replay.py

An additional reviewer implementation, importing no submitted compiler code, exhaustively checked the earliest-representative construction on **41,488** root-reachable DAG models with 1–3 nodes, two judgement labels, two evidence tokens, ordered arity 0–2, and prices 0 or 1. This includes 10,240 cases with actual redirected references. Reproduce with:

    python3 certificate-compilation-boundary-20261009/review/sanity.py

Results are in `REPLAY_RESULTS.json`, `replay.log`, and `SANITY_RESULTS.json`. These finite checks support implementation review; they are not a kernel proof of the general theorems. The traversal functions are structural checks, not external rule-registry admission checks, evidence authentication, or semantic soundness proofs. The package documents that distinction.

## Exact inspected revisions

SHA-256 values, relative to the package except where stated:

- `RESULT.md`: `3d8d11d73055b62913cf36138cc0b3b273d032f8f927a885ee2af11bd8eaf459`
- `compiler.py`: `5da2762fe31720e898165751bf53636f66a5267719e0b3687587628c48ac4714`
- `verify.py`: `ba6b947c758b0541ce4dc489c116c87cc6000ebc221ff23f8b5f3efd5de94f70`
- `READ_FIRST.md`: `769e6052c53dadef27260445f546eb7a9a1be26677fb819302718ee55229e19d`
- `SOURCES.json`: `750a30b2cc811c5fd37f5532ba8902bc69712792a0c32501eef4818969c0ac50`
- Inherited `warranted-discrimination-research-20261009/RESULT.md`: `71551ae962a17ec72709b6d36cfb58ed99237a2ef776339709a43b8d3b436d28` (catalogue, persistence, frontier, and test-model interface inspected).
- Inherited `warranted-discrimination-kernel-20261009/RESULT.md`: `a8c3ea0ad398c412a8a15f532ebad7ff6caed0254e6fcb953cb25471aa708026` (report and exclusions inspected).

The two inherited report hashes agree with their values at review start. This review does not re-certify the inherited Lean development, independently re-review the historical HasE/System R arguments, or establish field-wide originality. Its positive verdict is limited to the bound compiler mathematics, implementation, controls, and stated scope. No submitted report, algorithm, test suite, or inherited input was edited by this reviewer.
