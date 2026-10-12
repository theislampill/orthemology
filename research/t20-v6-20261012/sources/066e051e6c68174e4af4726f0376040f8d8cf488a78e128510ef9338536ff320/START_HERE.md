# Criterion revision and transport reviewed V3

This packet answers question 4 with one fully specified source-bound governing-criterion repair. The result is warranted retained-standard repair in a typed research model. It includes exact sources, proofs, executable models, tests and compact replay evidence. It is an independently reviewed Seventh-tranche lane result, not a declaration that the entire programme or tranche is complete.

## Main result

A deliberately constructed governing rule accepts source copies after stripping trailing LF bytes. Under the retained exact-byte recovery standard it is defective: source-plus-LF is accepted even though it differs from the source. The corrected rule accepts exactly the source bytes. The installation transition actually replaces the recipient's installed rule, advances its separate rule version/history, and changes its acceptance decisions. It preserves source, draft bytes, draft revision and unrelated state.

The replacement has an explicit interpretation in a two-constructor rule language. The model does not trust arbitrary uploaded code merely because its label says C1. Each recipient needs a current install-specific grant. A copied proof can preserve the source-grounded adequacy argument without conveying another recipient's permission. Installing the rule and repairing an existing bad draft require distinct operation scopes.

The case retains the target, standard, inference resources and authority conditions. It does not instantiate full-basis radical correction. Necessary-source N2, essential truthful attestation T0, Wisdom and metaphysical unity are not used; no R5 defeat or canonical Candidate E adoption follows.

## Canonical source

Repository theislampill/orthemology, commit 19de267cd41d2a5eeeb3eaf0b91562f706e2a916, path docs/project-closure/ar8r-v11/programs/proper-function-and-candidate-e.md. The exact 3,013 bytes have SHA256 e4ae2e2751535e625f245a1bb2f2e4f2f4c447a55c859e1b1c94dbbf48adf359 and Git blob c032efd2236060906b2d2dfc15b52f336aeeac87, matching the historical record. Five substantive historical packet files also match the recovered Sixth copies.

The earlier extra-newline source-file recovery event is author-observed history. The independent review checked the source and relevant digests, not that earlier physical write. The C0-to-C1 checker experiment is deliberate; it is not attributed as historical governance of the initial write.

## Read in this order

1. CRITERION_INSTALLATION_ARGUMENT.md
2. TRANSPORT_ARGUMENT.md
3. CANDIDATE_E_COLD_ASSESSMENT.md
4. SUPPORT_AND_DEPENDENCY_LEDGER.md and PRIMARY_SOURCE_REVIEW.md
5. CRITERION_INSTALLATION_SPEC.md and SPECIFICATION.md
6. REVIEW_SUMMARY.md, proofs, models and evidence records

## Independently verified

- All 44 Python tests pass.
- The original guarded-draft model checks 393,216 shared Python/Lean fixture projections with zero differences; 480 apply and 392,736 reject.
- Explicit rule installation checks 4,096 shared Python/Lean fixture projections with zero differences; 8 install and 4,088 reject. Four accepted cases correct normalized rules; four reinstall already exact rules at a new version.
- Actual installed decisions accept exact source, reject source-plus-LF after correction and reject another distinct wrong candidate.
- Full typed Lean proofs establish the transport conditions, criterion adequacy, contextual guards and preservation obligations. Some generic list lemmas use standard Lean logical axioms; no custom axiom or sorry is used.
- Independent review passed the exact 33-file V3 snapshot and rechecked every bound input unchanged after execution.

The large CSVs are omitted because the included generators reproduce them exactly. Their hashes and the output hashes remain in the evidence JSON records. Full original replay of actual source bytes takes several minutes.

## What remains outside the result

The implementation is not a real-recipient deployment, arbitrary-code updater, verified compiler, hostile-input parser or all-input Python-to-Lean refinement. Source, actor, grant, clock and revocation records require independent actual-world warrant. Non-bypassable execution and fault-tolerant live authorization are external mechanism obligations. Safe rejection alone does not guarantee eventual restoration. The separate composition of rule installation, payload repair and a dynamic fault mechanism is not claimed by this packet.

Candidate E remains DEFERRED_INSUFFICIENT_AUDIT in the canonical owner. No GitHub mutation or owner adoption occurred.

## Reproduce

Use Python 3.12 and Lean 4.19.0, commit 6caaee842e94. No mathlib is required. From this folder:

- python verify_bundle.py
- python -m unittest discover -s tests -v
- lean CriterionTransport.lean
- lean -o TypedCriterionGuard.olean TypedCriterionGuard.lean
- LEAN_PATH=. lean -o CriterionInstallation.olean CriterionInstallation.lean
- python bounded_audit.py
- python shared_fixture_check.py generate
- LEAN_PATH=. lean --run ReplayCriterionFixtures.lean
- python shared_fixture_check.py compare --label green
- python rule_install_audit.py generate
- LEAN_PATH=. lean --run ReplayRuleInstallation.lean
- python rule_install_audit.py compare
