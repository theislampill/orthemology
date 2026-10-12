# Review response: witness admission and two wording qualifications

9 October 2026. This is the author's repair record. The independent review's original findings, execution evidence and final disposition are separate reviewer-owned artifacts and are not overwritten here.

## Findings preserved

1. The all-unit-price tree formula `2n+1` lacked an explicit proof-existence qualifier. For an uncovered element no proof exists.
2. The inherited unguarded `dag_value` checks structural labels, references, reachability and price, but does not receive an admitted rule catalogue. A fabricated nullary goal rule can pass that structural traversal.
3. The first `check_case(binary=True)` control compared correct binary compiler minima, but its independently constructed forward witness still used the original n-ary goal rule. That rule is absent from the binary grammar when there are at least two element premises.
4. “The only rule concluding xi” was singular despite multiple possible incidence rules.

The two general reductions and the binary compiler's optimum assertions were not invalidated. The second and third findings exposed a real gap in the claimed witness validation. They are not recast as merely typographical findings.

## Repairs

- `checked_dag` and `checked_tree` first verify membership of every rule in the supplied admitted catalogue, then call the inherited structural/price traversal. Returned ordinary compiler frontiers are fully rechecked. Returned exact-support tables use the predecessor's admission-aware `tree_value` and are fully rechecked as well.
- `cover_witness` now takes the binary flag, obtains rules from the actual requested grammar and constructs the matching binary conjunction nodes and final reference.
- One negative control supplies an invented zero-price goal rule. Another supplies the old n-ary cover witness to the binary rule catalogue. Both pass the narrower inherited structural traversal and are rejected by the new admission wrapper. A matching binary witness is then accepted.
- The report qualifies `2n+1` by proof existence, fixes the plural rule wording and describes the validation gap and repair.

The unmodified pre-repair report, script, check outputs and authored manifest are retained under `before-review/`. The repaired complete census still passes: 689 set systems, 1,510 forward witnesses, both exact-support encodings, six binary cases and six all-unit-price cases, plus the admission controls.

No predecessor was edited. The added wrappers validate membership in an already admitted finite rule list; they do not authenticate evidence or justify the substantive rules. This is written mathematics plus executable bounded checking, not a new kernel theorem.
