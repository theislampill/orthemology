# R4 PR #3 — Fresh Fable Review of the Pre-Substitution Range (Phase B)

Range reviewed: `25d035a..00cf05d6` — the prior review session's Phases A–D:

- `d8517d8` review: Phase A read-only reproduction (report-only);
- `1223110` state: convergent source-tree-digest contract (Phase B);
- `d7b9687` formal: strict-soundness definition, CR-9..CR-15, governed
  ReqReason_q, machine-checked supersession (Phase C);
- `00cf05d` schema+semantics: reference-model completion (Phase D).

Every commit was reviewed, not merely the final files. Session surfaced model
at this phase boundary: `claude-fable-5`; no substitution observed.

## B1. Generated-state contract — VERIFIED (design, not just tests)

- **No `HEAD` hash in the tracked equality contract.** The derived block
  contains no commit hash; `docs/project-state-inputs.yaml` states the
  non-convergence rationale explicitly. The only commit values in the derived
  block are the PDF sidecars' `source_commit` fields, which are read from
  tracked sidecar files (stable tree content), never from `HEAD`.
- **Machine-readable source-input policy**: `docs/project-state-inputs.yaml`
  with per-exclusion reasons.
- **State output excluded from its own digest**: `docs/current-state.yaml`,
  the manifest, `artifacts/`, `docs/generated/`, `docs/project-closure/` are
  excluded; each exclusion names the check that covers it instead (manifest
  covers closure reports; artifacts covered by `build_pdfs.py --check`;
  generated surfaces by `generate_from_registry.py --check`).
- **Convergence across a commit boundary**: `validate_state_convergence.py`
  proves regenerate→commit→`--check` passes on the containing commit,
  idempotence, source-tamper failure, and excluded-path immunity, in a
  throwaway git repository. Reproduced green at `00cf05d6`, the PR head, and
  the quarantine head.
- **Exact burden IDs and state markers**: `validate_current_state.py` uses
  HTML-comment state markers with exact string equality (decision range,
  example count, burden-ID set equality with no extras/omissions/duplicates,
  verbatim claim-status wording per lane, freeze-hash cross-check against the
  packet files). No fuzzy "exact" claims found.
- Minor, non-blocking: the README decision-range marker is a min–max display
  contract and would not catch a gap strictly inside the ID sequence; the
  exact `decision_ids` list in the state file carries the precise set.

## B2. Strict soundness — ONE FINDING, REPAIRED

Verified:

- sole current definition is
  `StrictlySoundReasoning_q(e) := ReasoningPathAdequate_q(e) ∧ TOKEN_TRUTH_LINKED_q(e)`
  (Decision 0011), machine-registered in `docs/decision-status.yaml`;
- Decision 0009 preserved verbatim with a dated partial-supersession notice
  naming 0011; supersession machine-checked (`validate_decision_dependencies.py`
  checks the notice, history preservation, and the current definer);
- CR-9..CR-15 + CR-OMIT-1 exist and are structurally asserted (shared-upstream
  symmetry without truth, route/closure divergence from the superseded
  formula, mixed episode with one sound and one unsound claim, correct-by-luck,
  rare miss, unresolved claim, omission attack);
- strict soundness is claim-relative; an independence probe flips
  ROUTE_ADMISSIBLE/CLOSURE_TRUTHFUL per non-routing/non-closure claim and
  requires no state change;
- factivity enforced claim-wise (TOKEN_TRUTH_LINKED pass ⇒ RESULT_CORRECT
  pass, checked per claim).

**Finding B2-1 (repaired).** `docs/semantic-roles.yaml` — a current normative
surface by `docs/decision-status.yaml`'s own note — still glossed
`strict_reason_soundness` with the superseded whole-episode formula
(`… = PathwayAdequate(e) AND TOKEN_TRUTH_LINKED_q(e)`). It evaded the
machine check twice over: check 5 scanned only `.md` files, and the gloss
paraphrased the formula (ASCII `AND` for `∧`, `=` for `:=`).

Repairs:

1. gloss updated to the Decision 0011 claim-relative formula with an explicit
   supersession pointer (`docs/semantic-roles.yaml`);
2. `validate_decision_dependencies.py` check 5 hardened: scans `.md` and
   `.yaml`/`.yml`, matches an ASCII-normalized form (`∧`→`AND`, `:=`→`=`,
   whitespace collapsed), with a single principled exemption for
   `docs/decision-status.yaml` (the supersession registry records the
   superseded formula by design).

Negative control executed: restoring the old gloss under the hardened scanner
fails with exactly `['docs/semantic-roles.yaml']`; restoring the repair
returns 0 failures. `validate_type_token_semantics.py` remains green.

## B3. Governance-derived ReqReason_q — VERIFIED

- `ReqReason_q(e)` is recomputed by `validate_claim_reasoning_paths.py` from
  `docs/claim-reason-requirements.yaml` and the claim's declared shape,
  independently of any recorded projection; a recorded projection is used
  only as an attack surface (CR-OMIT-1) and the derived projection decides;
- derivation inputs: claim type, evidence kind, token dependencies,
  robustness obligation, currency exemption; always intersected with the
  governance-derived `ReqPath(e)`;
- a per-verdict inclusion/exclusion trace is required to cover every CorePath
  verdict;
- the omission-attack fixture demonstrates that trusting the recorded
  projection would manufacture a better state;
- the table honestly states it is a bounded governed instance
  ("RequiredReasonBy is, in general, a GOVERNANCE-SUPPLIED PARAMETERIZED
  INTERFACE… not a closed universal calculus"), same posture as
  `docs/governance-requirements.yaml`.

## B4. Cross-record semantic contract — VERIFIED

`validate_cross_record_semantics.py` implements, and invalid fixtures
I29–I44 witness: analysis-inheritance self-edge/cycle/unresolved chain
(I29–I31) with effective-analysis completeness; episode-local token ownership
with global token_id uniqueness and same-token redeclaration rules (I32);
standalone-token ownership or explicit external scope (I33); token claim
scope (I34); metaortheme/edition reference resolution (I35); precedence
self-edge/cycle (I36/I37); token membership in the governing configuration
(I38); explicit external/unresolved reference modes for audit-ready records
(I39/I40); timezone-aware ordering — naive timestamps rejected wherever
ordering matters, comparisons only on aware UTC instants (I41/I42);
effective-before-expiry validity ordering (I43); ReqReason omission (I44).
Token/ledger comparisons are ownership-scoped; no all-token-to-all-ledger
comparison exists. Spot-review of the exact semantics (timestamp
normalization, token-identity rule) confirmed the implementation matches the
declared rules, not merely the fixtures.

## B5. Negative and mutation coverage — VERIFIED (bounded)

At `00cf05d6` and at the PR head, `validate_recursive_mutations.py` reports:
**1,813 generated mutants over 23 path-aware operator families — 1,546
schema-killed, 248 semantic-killed, 19 survivors, every survivor declared
equivalent in `mutation-spec.json` with a stated reason** (residual
evidence/verdict-ref redundancy on validated-resolved dispositions;
legitimately-empty lists whose detection would require truth external to the
record — the whole-state-reread limit stated in prose). Families cover nested
empties, duplicate IDs, broken references, version mismatches,
conditional-field removal, cycles, verdict-status omissions,
summary/status contradictions, candidate/partial-profile and
claim/episode-path collapses, ghost references, and precedence cycles.
This is a bounded result over the shipped families and fixtures, not a
completeness claim.

## Disposition

The pre-substitution range is **kept**: reviewed and confirmed with one
repaired finding (B2-1) and one hardening (the supersession scanner). No
other change to the range's work was needed.
