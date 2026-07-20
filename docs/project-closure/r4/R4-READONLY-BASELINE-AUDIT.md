# R4 read-only baseline audit

**Date:** 2026-07-20 · **Executor:** Claude Fable 5 under the R4 owner authorization (consolidated prompt v2; Part II latent-state amendment controlling where more specific) · **Mode:** read-only — no repository file was modified before this report was complete.

## 0. Starting verification

- **Live remote verified** (not taken from the closeout or the ZIP): `gh api repos/theislampill/orthemology/branches/main` → `63d15ecf4aa50672265100b7d5620af764421862`, `protected: true`; latest `main` CI run **success** (29743263628, the R3 merge). This matches the R4 prompt's expected commit and the supplied archive's ZIP comment, so the audited export and the live remote agree.
- Working tree: fresh clone of that commit; branch `closure/r4-semantic-contract-source-integrity`. **168 tracked files.**
- Inventory: 8 schemas · 8 JSON examples (+1 Markdown worked case) · 10 decision records (0001–0010) · 4 draft PDFs + 4 sidecars · 19 validator/build scripts · fixtures: verdict F1–F7, reason CR-1…CR-8, ReqPath RP-1…RP-5, negative N1–N11, mutation spec.
- **Every existing validator re-run from the fresh clone: 0 failures** (repo hygiene; verdict semantics 57 checks; notation; type/token; reason fixtures; schemas; cross-record semantics; negative+mutation; ReqPath derivation; generated-surface drift; Qurʾān loci; claim sources; cross-document; terminology matching). Both terminology freeze hashes PASS (v1 `ece0412f…`, v2 `a1edbd2c…`). `build_pdfs.py --check`: **0 failures** — clean rebuild byte-identical to all four committed artifacts.
- **The independent audit's positive findings are confirmed**: R3's checks are genuine, and the PDF pipeline is genuinely reproducible and structurally rendered. The blocking findings below are coverage and consistency gaps, not fabricated test output.

## 1. Reproduced blocking findings

| # | Audit finding | Status | Evidence |
|---|---|---|---|
| B1 | `p̂` typed both as one partial profile and as a set of complete profiles | **CONFIRMED** | `theory/orthemic-core-formalization.md:159` — "`p̂ ∈ Π_A^∂` … the profile actually placed (**or a bounded set of profiles if unresolved**)", against manuscript Definition 10's `Ĉ ⊆ Π_A` vs `p̂ ∈ Π_A^∂` and its explicit "a candidate set is not one vague partial profile". Direct type contradiction. (Two archive copies carry the same gloss and stay historical.) |
| B2 | Strict soundness claim-level in name, episode-level in its pathway conjunct | **CONFIRMED** | `StrictlySoundReasoning_q(e) := PathwayAdequate(e) ∧ TOKEN_TRUTH_LINKED_q(e)` in Decision 0009, `CONCRETE-AND-SOUND-REASON.md` §5, companion §2.1: `PathwayAdequate` conjoins over the whole `ReqPath` including `ROUTE_ADMISSIBLE` and `CLOSURE_TRUTHFUL`, so a downstream routing or closure failure would flip a soundly reached claim to "not strictly sound". |
| B3 | Objectivity/indexing overstated | **CONFIRMED** | `R3-FORMAL-AUDIT.md:33` and `CONCRETE-AND-SOUND-REASON.md:82` both say pathway adequacy is "objective given `A`" while `EX_ANTE_JUSTIFIED` ∈ CorePath is explicitly indexed to actor, decision time, and information state. |
| B4 | Evaluator symmetry + corroboration asserted to give non-circularity | **CONFIRMED** | `R3-FORMAL-AUDIT.md:27` Q9: "Non-circularity comes from evaluator symmetry + corroboration". Too strong: shared upstream dependence survives both. |
| B5 | Metaorthemma zero-burden ontology and typing cardinality not normalized | **CONFIRMED** | Zero-burden is stated as "no metaorthemma exists" (CR-8, core) but elsewhere as an unrecorded-token reading; `CONCRETE-AND-SOUND-REASON.md` §6 permits one token instantiating several metaortheme types while `metaorthemma.schema.json` has singular `of_type` and the R3 formal audit calls plural typing a future extension. |
| B6 | Schemas do not encode the settled semantic contract | **CONFIRMED, quantified** | Independent probe (11 malformed classes): **10 accepted by both the schema and cross-record layers** — analysis with empty task and no D1 components; metaortheme with empty ids/duplicate states/no policy relation; metaorthemma with empty anchors/binder and no validity semantics; residuals `owner-assigned`/`deferred`/`risk-accepted` with no owner/trigger/risk record; handoff with no payload; skeletal "audit-ready" episode with empty actor/time/policy/placement; `not-applicable` without reason **outside** `required_path`; free-form strings standing in for RelSpec/PerturbSpec. **Partial refutation:** the "verdict record missing statuses for required verdicts" class is accepted at the *schema* layer but **is** caught by the cross-record validator (pathway recomputation returns MALFORMED) — the audit's phrasing overstates that one case. |
| B7 | "208 mutants, 0 survivors" narrower than implied | **CONFIRMED** | `tests/schema-mutations/mutation-spec.json` declares exactly three operators, all top-level: `drop-required`, `bad-enum`, `extra-field`. No nested/path-aware, reference, cardinality, or cross-record operators exist. |
| B8 | Concrete/ideal-reason attribution mislocated | **CONFIRMED** (correction sourced in Phase 5) | Companion and `CONCRETE-AND-SOUND-REASON.md` attribute the phrase pair to Evans 2010 + Turner 2022; R3 itself recorded the phrase pair as unverified in those works. Correct chain per the supplied compilation and the audit: Doko & Turner 2023 for the application, Evans 1998 as the reported phrase source. |
| B9 | Atharī front matter contradicts the R3 sourcing closeout | **CONFIRMED** | `orthability-divine-attributes-and-speech-athari.md:3` still says classical loci are `[via compilation]` and "the printed editions were not independently opened", while `R3-SOURCING-AUDIT.md` reports work-level verification, verbatim confirmation of the Majmūʿ vol-12 formula, and no phantom sources. Both cannot govern. |
| B10 | Public state drifted | **CONFIRMED, itemized** | `VERSION` says "R2 … autonomous closure revision"; all four primary document headers say R2; README says "0001–0003 … and 0004–0008" (0009/0010 exist) and "seven machine-readable examples" (eight exist); `OPEN-DECISIONS.md` still lists classical-edition verification as owner-only (R3 withdrew that); `STATUS.md` retains blanket compilation-mediated wording; `R3-CLOSURE-BURDEN-LEDGER.md` says "5 owner-assigned" then enumerates six items. |

## 2. Latent-state amendment baseline (Part II)

No latent-state, aliasing, or representation-geometry material exists in the corpus: grep finds no `latent`, `aliasing`, `orthogonaliz*`, `hidden state`, or `posterior` in current normative documents, and no related-work note. The amendment's integration is therefore wholly additive — the risk to guard is conflation on introduction (latent state ≡ ortheme; representation geometry as ontology; endpoint fit as mechanism proof), not repair of existing text. The three cited papers are absent from `references/orthemology.bib`. Bibliographic verification is in progress in Phase 5.

## 3. Bounded `daee-epistemics` recheck baseline

The R3 mapping note's five claimed controls (canonical atomized source → generated runtime with freshness checks; evaluator/practitioner symmetry; inference-boundary legend; whole-state reread after a burden lands; bounded release/closure contract) were re-inspected against the current public repository and still hold as described. The two additional engineering applications the R4 prompt authorizes — a single generated project-state source, and transition-triggered whole-state reread extended to source-status changes — are not yet implemented here; R3 implemented only the closure-floor slice.

## 4. Severity-ranked mutation plan

| ID | Severity | Repair | Phase |
|---|---|---|---|
| B10 | BLOCKING | generated current-state contract; VERSION/README/STATUS/OPEN-DECISIONS/CHANGELOG synchronized and drift-checked | P1 |
| B1 | BLOCKING | `p̂`/`Ĉ` typing normalized corpus-wide + profile-typing validator + negative tests | P2 |
| B2 | BLOCKING | `ReqReason_q(e)` projection; `ReasoningPathAdequate_q`; claim-relative strict soundness; 6 fixtures | P2 |
| B3 | BLOCKING | full-index objectivity language; indices required in the verdict schema | P2 |
| B4 | BLOCKING | circularity language corrected; shared-upstream corroboration fixture | P2 |
| B5 | BLOCKING | zero-burden existence rule + single-typing rule, stated once and schema-enforced | P2/P3 |
| B6 | BLOCKING | full reference-model semantic contract across all schemas + new RelSpec/PerturbSpec schemas + expanded cross-record semantics | P3 |
| B7 | BLOCKING | 20 recursive/path-aware operators; invalid-fixture corpus; honest per-family reporting | P4 |
| B8 | BLOCKING | attribution chain corrected in the source-status registry and prose | P5 |
| B9 | BLOCKING | per-claim source-status synchronization; blanket front-matter claim replaced | P5 |
| — | ADDITIVE | latent-state note, decision, LS-1…LS-7 fixtures, anti-conflation tests, related-work subsection | P6 |

**Not reopened (verified intact at baseline):** D1, M1, O2, D3, D4, O3, orthability-L/O/R, the reason/revelation boundary, the created/uncreated distinctions, the PDF pipeline, terminology v2 status, and the R3 daee imports. R1/R2/R3 history will be preserved byte-for-byte except for dated supersession notices.
