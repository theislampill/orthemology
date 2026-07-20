# Review A — formal/type audit (fresh Fable recovery review)

Scope: the final review-branch diff against `main`. Surfaced model:
`claude-fable-5`.

- **Candidate-set/partial-profile collapse**: none. `docs/notation-registry.yaml`
  carries `Ĉ_{A,α,t}(m)` and `p̂_{A,α,t}(m)` as distinct glyphs; the manuscript
  states the anti-collapse rule explicitly (§5, "a candidate set is not one
  inferred profile"); the core's implication table keeps `p̂ ∈ Π_A^∂` "never a
  set of complete profiles". Mutation family "candidate/partial-profile
  collapse" is semantic-killed.
- **Claim/episode soundness collapse**: none. Sole current formula is the
  claim-relative Decision 0011 definition; machine-checked
  (`validate_decision_dependencies.py`, hardened this review to cover YAML and
  ASCII paraphrase after finding B2-1 in `semantic-roles.yaml`); CR-10/CR-11
  witness divergence from the superseded whole-episode form; the independence
  probe flips route/closure per claim.
- **Observation/state/profile and token/type/execution collapses**: none
  found; semantic-roles registry keeps the bearers distinct
  (`validate_type_token_semantics.py` green); metaortheme ≠ metaorthemma ≠
  execution ≠ episode preserved in the roles and schemas.
- **Vacuous requirement projections**: impossible for any declared claim
  shape — six `when: always` rules guarantee a non-empty `ReqReason_q`
  before the ReqPath intersection; the omission attack pins that recorded
  projections cannot substitute.
- **Hidden factivity**: none. Pathway adequacy remains result-free
  (CorePath excludes V1/V2b-T); factivity enters only through
  `TOKEN_TRUTH_LINKED_q`, claim-wise, with the entailment `V2b-T_q → V1_q`
  declared and checked.
- **Analysis/task/version equivocation**: none found; Decision 0015 A1.6
  separates model-artifact identity from analysis version; handoff
  `valid_for_version` anti-transport rule checked cross-record.
- **Under-specified transport**: repaired upstream in 0015 A1.3 — transport
  requires an explicit validated alignment map and recorded carry; silent
  transport is an `EVIDENCE_CURRENT` failure.

Blocking findings: **none**. Non-blocking notes: the B2-1 gloss repair and
scanner hardening are recorded in PRE-SUBSTITUTION-REVIEW.md.
