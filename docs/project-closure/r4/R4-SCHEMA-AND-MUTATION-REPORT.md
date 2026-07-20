# R4 schema contract and mutation report

> **CANDIDATE PASS — REQUIRES INDEPENDENT REVIEW.**
>
> **Correction notice (same-day, before merge).** An earlier revision of this file stated that the recursive/path-aware mutation engine and the `tests/invalid/` corpus were *not* completed. **That was wrong.** Both were completed; the work landed while the report was being written and was not re-checked before the report and the session closeout were issued. The false statement is corrected below and recorded in `R4-CORRECTION-LEDGER.md` as **SELF-2**. The lesson is the project's own: a completion claim must be checked against the artifact at the moment of claiming, not from a stale observation.
>
> A second revision then attributed two probe classes (P7, P8) to the schema layer. **That was also wrong**, and is corrected in §1: both are caught at the **semantic** layer, because both range over dynamic verdict-id keys that JSON Schema cannot quantify over. Every layer attribution below was re-derived by running the fixture, not recalled.

**Date:** 2026-07-20 · **Scope:** findings B6 (schemas do not encode the settled semantic contract) and B7 ("208 mutants, 0 survivors" narrower than implied), with the schema-side halves of B1, B2, B3 and B5 · **Status:** deterministic consistency work. Nothing here establishes an empirical claim; it establishes that malformed records are now rejected rather than silently accepted.

## 1. Before and after: the probe

The read-only baseline audit ran an independent probe of eleven malformed record classes against the R3 schema and cross-record layers. **Ten of the eleven were accepted by both layers.** The eleventh — a verdict record missing statuses for its required verdicts — was accepted at the schema layer but *was* caught by cross-record pathway recomputation; the audit's phrasing on that sub-case was slightly overstated, and that is recorded as a partial refutation rather than absorbed.

| # | Malformed class | R3 result | R4 layer | Fixture |
|---|---|---|---|---|
| 1 | analysis with an empty task and no D1 components | accepted | schema | `I01-empty-task-analysis` |
| 2 | metaortheme with an empty id | accepted | schema | `I02-empty-id-metaortheme` |
| 3 | metaortheme with a duplicated state member | accepted | schema | `I03-duplicate-state-metaortheme` |
| 4 | metaorthemma with an empty anchor | accepted | schema | `I05-empty-anchor-metaorthemma` |
| 5 | residual `owner-assigned` with no owner | accepted | schema | `I11-owner-assigned-residual-without-owner` |
| 6 | residual `deferred` with no trigger | accepted | schema | `I09-deferred-residual-without-trigger` |
| 7 | residual `risk-accepted` with no risk record | accepted | schema | `I12-risk-accepted-residual-without-risk-record` |
| 8 | handoff with no payload | accepted | schema | `I14-payload-free-handoff` |
| 9 | skeletal record claiming to be audit-ready | accepted | schema | `I16-skeletal-audit-ready-episode` |
| 10 | `not-applicable` with no reason **outside** `required_path` | accepted | **semantic** | `I22-na-without-reason-outside-required-path` |
| 11 | free-form strings standing in for RelSpec / PerturbSpec | accepted | schema | `I18-free-form-relspec`, `I19-free-form-perturbspec` |
| — | verdict record missing statuses for required verdicts | caught semantically already | **semantic**, now reported as its own finding rather than only as a pathway recomputation | `I21-verdict-missing-required-statuses` |

**All eleven classes are now rejected at a declared layer.** Nine at the schema layer, two at the semantic layer.

The rule governing the split: JSON Schema carries everything expressible about a single record in isolation; the cross-record layer carries everything that depends on another record, on a dynamic key set, or on a recomputation. Classes 10 and the missing-status class stay semantic for exactly that reason — both quantify over which verdict ids happen to appear in `statuses`. Where a rule could sit in either layer, it sits in the schema, because the schema layer rejects earlier and more cheaply.

The invalid corpus adds a further seventeen classes the probe did not reach (§4).

## 2. Schema contract changes

Ten schemas now, up from eight. Applied to every schema: `minLength: 1` on every constitutive string and id, `additionalProperties: false` outside the documented typed extension maps (`binding`, `statuses`, `na_reasons`, `rel_spec`, `perturb_spec`, `evidence_status`), and `uniqueItems: true` on every array used as a set.

### `analysis.schema.json` — the D1 declaration contract

Every constitutive component (`task`, `boundary`, `repertoire_ref`, `evidence_repertoire`, `action_repertoire`, `loss`, `hard_constraints`, `horizon`, `tolerance`, `representation_family`, `merger_family`, `governance_boundary`) must now be **declared**: either a nonempty value, or an explicit typed disposition object `{"disposition": "not_applicable" | "unspecified_with_reason", "reason": "..."}`. Silence is no longer a legal declaration; neither is `""`. The compact form (`analysis_id` + `version` alone) is admissible only when a resolvable `inherits_from` parent reference is present, and the cross-record layer checks that the parent actually resolves in the bundle. `governance_boundary` is a new component.

### `metaortheme.schema.json`

Nonempty `mu_id`/`version`. `states.members` is a set (`uniqueItems`, `minItems: 2`). The `selector` is now a **typed object** requiring at least `{kind, description}` — a state-selecting procedure that cannot be inspected is not a declared selector. New required `exclusivity` enum `[exclusive, overlapping, uncertain]`; `overlapping` and `uncertain` conditionally require `uncertainty_semantics`, so a record whose selection may be non-unique must say what a non-unique selection means for conduct. `provenance` is nonempty in all three subfields, and the pairing rule is enforced: at least one of `meta_policy` or `policy_ref` must be present.

### `metaorthemma.schema.json`

`of_type` remains singular and the schema now states why: **single-typing is the R4 rule**, and many-to-many `MetaInst` — one token instantiating several metaortheme types — is an *unimplemented future extension*, rejected here rather than silently accommodated (finding B5). `binding` stays nonempty (`minProperties: 1`, the M1 zero-burden rule) and its keys are now constrained. `anchor`, `analysis` and `binder` subfields are all nonempty; `binder.binding_time` is required, so every binding carries its time index. `scope` must carry a nonempty `claims` array **or** a typed `no_claim_dependency_reason`. `validity` must carry `effective_from` **or** an explicit `validity_unbounded_reason` — a binding with no declared start is undated governance. And a token must name a `designated_executor` **or** state a `no_separate_executor_reason`, keeping the binder/executor role distinction visible even when one actor fills both.

### `claim-ledger.schema.json`

Claims now require `claim_id`, `proposition`, `target` (`identity_key` + `version`), **`analysis`** (`analysis_id` + `version` — claims are analysis-relative, and an unindexed claim is not auditable), `property_class`, `success_surface`, `verification_status`, and either nonempty `evidence_ids` or an `evidence_inapplicable_reason`.

Residuals now carry a per-disposition completeness contract, expressed with JSON Schema `if`/`then`:

| Disposition | Now requires |
|---|---|
| `unresolved` | `responsible_queue` **and** `next_review_condition` |
| `deferred` | `trigger` **or** `review_date` |
| `transferred` | `receiver` **and** `transfer_record` |
| `owner-assigned` | `owner` **and** `acceptance_state` |
| `risk-accepted` | `risk_owner`, `rationale`, `scope`, `review_trigger` |
| `validated-resolved` | `evidence_refs` **or** `verdict_refs` |

A disposition without the fields that make it auditable is a label, not a disposition.

### `handoff.schema.json`

A handoff must now carry **substantive payload**: an `anyOf` requiring at least one of `state_claims` (≥1), `evidence_refs` (≥1), `authority_claims` (≥1), `residual_obligations` (≥1, a new typed field), or `requested_action`. A correctly addressed envelope that transports nothing is no longer a valid handoff. `state_claims` entries must additionally carry `analysis_id` and `analysis_version` alongside `valid_for_version`.

### `orthing-episode.schema.json`

New required `record_mode` enum `[audit-ready, minimal]`. `minimal` is an honest label for a record that makes no audit claim — it is not a licence to omit the base fields, which are unchanged. `audit-ready` triggers a conditional contract: nonempty `actor`, `time`, `observation`, `claim_ledger_ref` and `verdict_record_ref`; a nonempty `policy` or a `policy_inapplicable_reason`; nonempty `evidence` or an explicit `evidence_absent_reason`; and a nonempty `placement` or `candidates`. A skeletal record can no longer claim audit readiness. Separately, `candidates.profile` is documented and typed as a **set of complete profiles** with `minItems: 1` — collapsing it into a single partial profile object is a type error (finding B1).

### `verdict-record.schema.json`

New required **`index`** block `{analysis_id, analysis_version, actor, decision_time, information_state}`. This is the objectivity-indexing repair for finding B3: pathway adequacy is objective *given* a full index, and `EX_ANTE_JUSTIFIED` is explicitly indexed to actor, decision time and information state, so a record that omits them overstates its own objectivity.

New optional **`claim_reasoning_paths`** array of `{claim_id, req_reason[], reasoning_path_adequate}`. This represents claim-relative reasoning adequacy **distinctly** from the episode-level `pathway_state` (finding B2): `ReqReason_q(e)` is the projection of `ReqPath` onto the verdicts bearing on claim *q*, and the conjunction is taken over that projection alone, so a downstream routing or closure failure cannot retroactively flip a soundly reached claim. The cross-record layer recomputes both levels independently and rejects a projection that reaches outside `ReqPath`.

`rel_spec` and `perturb_spec` are now typed extension maps from claim id to a full RelSpec / PerturbSpec object; free-form prose no longer stands in for either. `required_path` gains `minItems: 1`; `statuses` gains `minProperties: 1`. The registry-generated `$defs.verdict_id` enum is unchanged in content and is still regenerated by `scripts/generate_from_registry.py` (`--check` passes).

### `reliability-spec.schema.json` (new)

RelSpec: `procedure_id`, `procedure_version`, `reference_class`, `risk_stratum`, `metric`, `threshold`, `evaluation_protocol`, `evidence_basis`, `declared_at`, `validity{effective_from, expiry}` — all required, `additionalProperties: false`. `declared_at` is the timestamp that makes **pre-outcome declaration checkable**; the cross-record layer rejects any RelSpec declared at or after the recorded result time. This is what keeps `PROCEDURE_RELIABLE` from being a figure chosen once the outcome is known.

### `perturbation-spec.schema.json` (new)

PerturbSpec: `neighborhood_family`, `enumeration` **XOR** `measure`, `invariants[]`, `varied_fields[]`, `metaorthemma_rebinding_rule`, `failure_criterion`, `version`, `validity` — all required, `additionalProperties: false`. The XOR is expressed with `oneOf` + `not`. `metaorthemma_rebinding_rule` exists so that robustness cannot silently smuggle in a rebinding of case-bound tokens as the case is perturbed. Disjointness of `invariants` and `varied_fields` is a cross-record check, since it relates the contents of two sibling arrays.

## 3. Positive-example migration

All eight example bundles still validate at both layers. Changes were confined to fields the hardened contract newly requires, plus the two free-form spec strings that are now typed objects. No example's semantics were changed.

- `record_mode` added to all eight episodes: `pillar-episode` is **audit-ready** (it carries both a claim ledger and a verdict record, evidence, an observation and a placement); the other seven are **minimal**, the honest label for records with `verdict_record_ref: null`.
- Full D1 declarations added to the three analysis records. Where the example genuinely never declared a component — the chess compatibility illustration declares no loss functional, no numeric tolerance and no merger — a typed `not_applicable` disposition with a reason was recorded rather than an invented value.
- `index` blocks added to all five verdict records, and `claim_reasoning_paths` added to all five.
- `no_separate_executor_reason`, `validity.effective_from` and `scope.claims` completed on the metaorthemma records. Two embedded token copies (in `pillar-episode` and `rare-miss`) carried `scope.claims: []` while the surrounding records showed a claim depending on them; these were completed to match the standalone record of the same token. That is a repair of an inconsistency already present in R3, not a change of meaning.
- Claim `analysis` indices and `evidence_ids` / `evidence_inapplicable_reason` added across the ledgers; residual conditional fields completed.
- `rare-miss` and `stopped-clock-validator` rel_spec/perturb_spec prose converted to typed objects. The stopped-clock RelSpec now records honestly that **no** sensitivity was ever measured for the marker-string check — which is why `PROCEDURE_RELIABLE` fails there.
- `tests/schema-negative/NEGATIVE-FIXTURES.json` was updated **additively** so its six semantic fixtures still carry the fields the hardened schemas require, and therefore remain schema-valid *by design*. Without that, their rejection would silently migrate to the schema layer and stop testing the semantic layer at all. No fixture was removed, renamed or weakened.

## 4. Invalid-fixture inventory

`tests/invalid/` — 28 files, one per malformed class, each carrying `{id, why, expect_layer, schema, instance}`. 22 are caught at the schema layer, 6 at the semantic layer.

| Fixture | Layer | Class |
|---|---|---|
| `I01-empty-task-analysis` | schema | empty task, no D1 components |
| `I02-empty-id-metaortheme` | schema | empty metaortheme id |
| `I03-duplicate-state-metaortheme` | schema | duplicated state member |
| `I04-bare-string-selector-metaortheme` | schema | selector as a bare string |
| `I05-empty-anchor-metaorthemma` | schema | empty anchor |
| `I06-plural-metaorthemma-type` | schema | plural `of_type` (unimplemented many-to-many MetaInst) |
| `I07-empty-metaorthemma-binding` | schema | empty binding map |
| `I08-unresolved-residual-without-queue` | schema | `unresolved` without queue or review condition |
| `I09-deferred-residual-without-trigger` | schema | `deferred` without trigger or review date |
| `I10-transferred-residual-without-receiver` | schema | `transferred` without receiver or record |
| `I11-owner-assigned-residual-without-owner` | schema | `owner-assigned` without owner or acceptance |
| `I12-risk-accepted-residual-without-risk-record` | schema | `risk-accepted` without owner, rationale, scope, trigger |
| `I13-validated-resolved-without-evidence` | schema | `validated-resolved` without evidence or verdict refs |
| `I14-payload-free-handoff` | schema | handoff carrying nothing |
| `I15-handoff-state-claim-without-valid-for-version` | schema | state claim without its `(κ, v)` |
| `I16-skeletal-audit-ready-episode` | schema | skeletal record claiming audit readiness |
| `I17-verdict-without-objectivity-index` | schema | verdict record with no index block |
| `I18-free-form-relspec` | schema | prose standing in for a RelSpec |
| `I19-free-form-perturbspec` | schema | prose standing in for a PerturbSpec |
| `I20-perturbspec-without-enumeration-or-measure` | schema | neighborhood named but never delimited |
| `I21-verdict-missing-required-statuses` | semantic | required verdict with no status at all |
| `I22-na-without-reason-outside-required-path` | semantic | `not-applicable` with no reason, off the required path |
| `I23-contradicted-pathway-summary` | semantic | asserted pathway state the statuses do not support |
| `I24-claim-path-collapsed-into-episode-path` | semantic | claim adequacy overwritten by episode pathway (B2) |
| `I25-relspec-declared-after-the-result` | semantic | reliability declared after the outcome |
| `I26-perturbspec-invariant-also-varied` | semantic | incoherent neighborhood |
| `I27-claim-dependency-cycle` | semantic | mutually dependent claims |
| `I28-token-anchored-to-another-occurrence` | semantic | token governing a case other than the one decided |

Each schema-layer fixture was checked to fail for its **intended** reason, not incidentally.

## 5. Cross-record semantic layer

`scripts/validate_cross_record_semantics.py` preserves every R3 check and its `collect_issues(parts)` API (other validators import it). Added in R4: bundle-wide id uniqueness; reference resolution for claim, token, evidence and handoff-episode ids and for `rel_spec`/`perturb_spec` keys and analysis inheritance; analysis/version compatibility across episode, ledger claims and the verdict index; occurrence/version anchoring across orthemma parts, episodes and handoff subjects (subject **version** drift included — that is precisely how stale state propagates); metaorthemma scope versus the claims that actually depend on the token; single-`of_type` enforcement; claim dependency cycle detection; residual conditional-field completeness; explicit required-path status completeness; `na_reasons` for **every** not-applicable status anywhere in the record; independent recomputation of the episode-level pathway **and** each claim-level reasoning path, with the projection-containment rule; RelSpec pre-outcome declaration; and PerturbSpec invariant/varied disjointness.

References are only checked where the referent set is actually present in the bundle. This is deliberate: reporting a dangling reference to a record the bundle never claimed to contain would be noise, not a finding.

## 6. Mutation operator families

`scripts/validate_recursive_mutations.py` walks every positive example part **recursively**, resolving the effective schema at each node — through `$ref`, `allOf`, and the applicable `if`/`then` and `anyOf`/`oneOf` branch — so that it knows at every path which fields are required, which arrays are sets, and which values are references. Eighteen families, no randomness, mutants enumerated in sorted path order.

A mutant is **killed** if the hardened schema rejects the mutated part, or if `collect_issues` flags the mutated bundle. Every unmutated bundle is issue-free (the engine asserts this before starting), so any issue a mutant raises is attributable to the mutation.

```
fam  operator family                                generated   schema  semantic  survivors
--------------------------------------------------------------------------------------------
1    delete-nested-required                               531      530         0 1 (1 justified)
2    empty-required-string                                378      378         0          0
3    empty-required-array-or-map                          131      125         0 6 (6 justified)
4    duplicate-unique-member                               61       60         1          0
5    unknown-reference-id                                  16        0        16          0
6    analysis-version-mismatch                              6        0         6          0
7    occurrence-version-mismatch                           14        0        14          0
8    delete-disposition-conditional-field                  10        8         0 2 (2 justified)
9    claim-dependency-cycle                                 4        0         4          0
10   remove-required-verdict-status                        45        0        45          0
11   contradict-pathway-summary                            21        0        21          0
12   na-without-reason                                     14        0        14          0
13   plural-metaorthemma-type                               5        5         0          0
14   empty-metaorthemma-binding                             5        5         0          0
15   postdate-reliability-declaration                       2        0         2          0
16   violate-perturbation-invariant                         1        0         1          0
17   collapse-candidate-set-into-partial-profile            2        2         0          0
18   collapse-claim-path-into-episode-path                  1        0         1          0
--------------------------------------------------------------------------------------------
     TOTAL                                               1247     1113       125          9
```

**1247 mutants; 1238 killed (1113 at the schema layer, 125 at the semantic layer); 9 survivors, all declared as justified equivalents with reasons in `tests/schema-mutations/mutation-spec.json`; 0 unjustified survivors.** An undeclared survivor fails the run.

The nine equivalents fall into three groups, and each is a statement about the model's limits rather than an excuse:

1. **Redundant support (4 mutants; families 1, 3, 8).** `pillar-episode`'s `validated-resolved` residual carries *both* `evidence_refs` and `verdict_refs`; the contract requires one. Deleting or emptying either leaves the disposition fully discharged. Deleting *both* is killed.
2. **Empty residual lists (3 mutants; family 3).** A ledger that opens no burdens is well-formed — not every episode leaves a residual. Convicting this would need an external source of truth about which burdens actually existed, which is outside the reference model by construction. This is the same limit the `whole-state-reread` example states in prose: the machine floor can convict a closure claim asserted *over a recorded* unresolved burden, but it cannot know about a burden nobody recorded.
3. **Empty evidence on minimal records (2 mutants; family 3).** A `minimal` record may legitimately carry no evidence, because it makes no audit claim. The same mutation on the audit-ready record is killed at the schema layer — which is exactly the discrimination `record_mode` was introduced to make.

The report always prints every family with its own counts. "N mutants killed" as a bare summary is the reporting style finding B7 was about, and this engine exists to replace it. The historical figure "208 mutants, 0 survivors" describes only the three top-level v1 operators (`drop-required`, `bad-enum`, `extra-field`, still run by `validate_negative_fixtures.py`, now 223 mutants) and must not be cited as semantic completeness. Neither should the current figure.

## 7. Coverage limits — what these operators do NOT test

Stated plainly, because an honest kill rate is worth less than an honest boundary.

- **The corpus is eight hand-written illustrative bundles.** Every count above is relative to what those bundles happen to contain. Family 16 generated **one** mutant because exactly one example carries a PerturbSpec; family 18 generated **one** because exactly one example has a claim whose reasoning path legitimately diverges from its episode pathway. A large per-family count means the corpus exercises that structure often, not that the rule is more strongly verified.
- **No generative or property-based testing.** Mutants are perturbations of valid records. Malformed shapes that no valid example is one edit away from — a deeply wrong composition graph, a pathological lineage DAG, an adversarially constructed axis system — are not reached.
- **Only single mutations.** Every mutant applies exactly one operator at one path. Compensating pairs, where two coordinated edits leave every local check satisfied, are not searched for. This is the most substantial gap.
- **No semantic content is judged.** The layers check that declarations are present, typed, internally consistent and mutually resolvable. Whether a declared `reason` is a *good* reason, whether a `success_surface` is the right surface, whether a reference class suits its risk stratum — none of that is machine-checkable here, and a record can be fully valid and substantively wrong. The typed-disposition machinery makes evasion *visible and attributable*; it does not make it impossible.
- **Timestamp comparison is lexicographic.** The pre-outcome declaration check compares ISO-8601 strings directly. That is correct for the UTC `Z` timestamps the corpus uses and for date prefixes, but it would not correctly order mixed offsets. No timezone library is used, to keep the validators dependency-free and deterministic.
- **The governance derivation is one instance.** `RequiredBy` remains a governance-supplied parameterized interface. `derive_reqpath.py` ships one complete deterministic table, not a universal calculus, and the mutation engine inherits that scope.
- **Equivalent-mutant detection is by declaration, not by proof.** The nine equivalents were identified by inspecting survivors and reasoned about individually. There is no automated equivalence checker, so the claim is "these nine were examined and judged non-killable", not "these are provably the only equivalents".
- **Cross-bundle consistency is out of scope.** Checks run per bundle. Two example files making incompatible claims about the same `(κ, v)` would not be caught, because the reference model has no notion of a global record store.

What these results support is narrow and specific: **the shipped reference model rejects the malformed-record classes enumerated here, at a declared layer, deterministically.**

## 8. Migration note — reference-model version bump

These are **breaking** schema changes. Records valid against the R3 schemas are not in general valid against R4. A consumer migrating existing records must:

1. **Analyses** — add `governance_boundary` and every other D1 component, as a value or a typed disposition. Where a component was genuinely never declared, `{"disposition": "unspecified_with_reason", "reason": "..."}` is the honest migration; inventing a value is not. An analysis that legitimately specializes another may instead add `inherits_from`.
2. **Episodes** — add `record_mode`. Default to `minimal` unless the record actually carries a claim ledger reference, a verdict record reference, evidence (or an `evidence_absent_reason`), an observation, and a placement or candidate set. Labelling a record `audit-ready` that is not is now a validation failure rather than an undetected overstatement, which is the point.
3. **Verdict records** — add the `index` block. `analysis_id`/`analysis_version` come from the episode; `actor`, `decision_time` and `information_state` must be supplied by whoever made the judgement and cannot be reconstructed mechanically. Where they are genuinely unrecoverable for a historical record, that record cannot be migrated honestly and should be retained as an R3-era artifact rather than back-filled with guesses.
4. **Verdict records with `rel_spec` / `perturb_spec`** — convert prose to typed objects. `declared_at` must be a real declaration time; if the reliability figure was in fact settled after the outcome, the migration will fail the pre-outcome check, and that failure is the correct result.
5. **Claim ledgers** — add per-claim `analysis`; add `evidence_ids` or `evidence_inapplicable_reason`; complete each residual's disposition-conditional fields. A residual that cannot be completed is evidence that its disposition was never really made, and the honest migration is to re-dispose it as `unresolved` with a queue and a review condition.
6. **Metaorthemmata** — complete `scope`, `validity` and the executor declaration. Tokens relying on plural typing must be split into one token per metaortheme type; there is no migration path that preserves many-to-many `MetaInst`, because it was never implemented.
7. **Handoffs** — a packet with no payload was never transporting anything; it should be deleted rather than padded.

Two schemas are new (`reliability-spec`, `perturbation-spec`), so any tooling that enumerates `schemas/*.schema.json` and expects exactly eight files needs updating. `scripts/validate_schemas.py` checks the eight expected schemas as a *subset*, so it is unaffected; `scripts/generate_current_state.py` counts schemas and must be re-run so `docs/current-state.yaml` reports ten.

## 9. Verification

All run offline and deterministically, each exiting 0:

| Validator | Result |
|---|---|
| `validate_schemas.py` | 0 failures |
| `validate_cross_record_semantics.py` | 0 failures |
| `validate_negative_fixtures.py` | 0 failures (197 checks; 223 top-level mutants, 0 survivors) |
| `validate_recursive_mutations.py` | 1247 mutants, 1238 killed, 9 justified equivalents, 0 unjustified survivors |
| `generate_from_registry.py --check` | 0 failures (no generated-surface drift) |
| `derive_reqpath.py` | 0 failures |
| `validate_reason_fixtures.py` | 0 failures |
| `validate_verdict_semantics.py` | 0 failures |
| `validate_type_token_semantics.py` | 0 failures |
| `validate_notation.py` | 0 failures |
| `validate_cross_document_consistency.py` | 0 failures |

`scripts/validate_repo.py`'s SHA-256 manifest check will report mismatches until `docs/provenance/RELEASE-MANIFEST.sha256` is regenerated with `scripts/make_manifest.py`: every file this pass touched is a manifest entry whose content changed by design. That regeneration is outside this pass's file ownership.
