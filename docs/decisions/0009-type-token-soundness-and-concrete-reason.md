# Decision 0009 — Type/token normalization, soundness bearers, and concrete reason

**Date:** 2026-07-20 · **Authority:** R3 owner authorization (consolidated prompt v2; Part II amendment controlling) · **Status:** adopted · **Does not reopen:** D1, M1, O2, D3 (0004), D4 (0005), O3 (0006), Π_A (0007), C′ (0008).

## Problem

The R2 school-neutral companion used "concrete ortheme" for a diagnosis/parse, "concrete metaortheme" for a locally operative standard, and said a higher-order faculty "outputs concrete metaorthemes." Under the settled ontology those phrasings are ambiguous and sometimes false: an ortheme is a repeatable operational state-type; a diagnosis is a placement `p̂` (or placement claim); a metaortheme is a repeatable governing type; the case-bound governing token is a metaorthemma; the act of applying it is an execution. At the same time, the underlying philosophical distinction — concretely instantiated reason vs sound reason — is genuine (supported by the supplied Taymiyyan scholarship) and must be **preserved by relocation**, not deleted.

## Decision

### 1. One normative ontology (restated, unchanged)

orthemma = concrete situated occurrence/token · ortheme = repeatable operational state-type, never the actor's local judgment token · objective profile = `O*(m; A)` · placement / inferred profile = `p̂_{A,α,t}(m)` · placement claim = the proposition that a case instantiates a type/profile · metaortheme = repeatable governing configuration/type · meta-policy = repeatable conduct rule paired with it · metaorthemma = case-bound configuration token where material binding exists · execution = the event/trace applying it · orthing episode = the complete auditable run.

### 2. Three independent axes replace the two-noun-class picture

**Concrete and sound are not contraries.** Every status claim must declare: (I) the **object level** (type / represented standard / case-bound token / execution event / resulting placement); (II) the **mode of instantiation** (normative specification vs concrete instantiation); (III) the **normative/epistemic status**, applied to its proper bearer; plus the separate **result status**. The bearer table:

| Object | Preferred status language | Avoid unless explicitly defined |
|---|---|---|
| Orthemma `m` | identified/misidentified; current/stale; observed/unobserved | "sound orthemma" |
| Ortheme `o` | well-individuated; analysis-relevant; over/under-segmented | "concrete ortheme" for a judgment token |
| True profile `O*(m; A)` | objective under declared `A`; obtaining profile | reification as a separately subsisting Platonic object |
| Inferred profile `p̂` | correct/incorrect; sound only per the declared definition | calling it the ortheme itself |
| Placement claim | true/false; supported/unsupported; current/stale | "pure ortheme" |
| Metaortheme `μ` | adequate/inadequate; fitting/misfitting; current/obsolete (as type/version) | "concrete metaortheme" for a token |
| Meta-policy `π_μ` | adequate/inadequate; safe/unsafe | collapsing into `μ` |
| Metaorthemma `μ̄_{e,j}` | properly bound/mis-bound; current/stale; adequate/defective | identifying it with the execution event |
| Execution trace | faithful/deviant; complete/incomplete | calling it the metaorthemma |
| Episode `e` | pathway-adequate/defective/undetermined; ex-ante justified/unjustified | making pathway adequacy factive |
| Result | correct/incorrect; truth-linked/lucky | inferring pathway adequacy from correctness |
| Faculty / fiṭrah condition | healthy/impaired; properly functioning/corrupted | equating fiṭrah with a faculty or a metaortheme without a declared analysis |

### 3. Derived soundness predicates (no new registry verdict)

- `PlacementCorrect(p̂, m, A)` iff `p̂` agrees with `O*(m; A)` at the governed level and tolerance.
- `ReasoningPathAdequate(e)` = the reasoning-relevant pathway requirements pass (non-factive, per O2).
- `ExAnteReasonable(e)` = `EX_ANTE_JUSTIFIED` passes.
- **`StrictlySoundReasoning_q(e) := PathwayAdequate(e) ∧ TOKEN_TRUTH_LINKED_q(e)`** — factive at the claim level; episode-level aggregation is claim-wise conjunction over the episode's asserted claims and must be stated explicitly wherever used; an episode may contain some strictly sound and some not-strictly-sound placements.
  > **SUPERSESSION NOTICE (2026-07-20, R4 independent review).** This formula — and only this formula — is superseded by **Decision 0011**. Conjoining the whole-episode `PathwayAdequate(e)` makes a claim-level predicate fail on unrelated downstream route or closure defects and cannot represent a mixed episode. The sole current normative definition is `StrictlySoundReasoning_q(e) := ReasoningPathAdequate_q(e) ∧ TOKEN_TRUTH_LINKED_q(e)`, with `ReasoningPathAdequate_q(e)` computed over the governance-derived claim-relative projection `ReqReason_q(e) ⊆ ReqPath(e)` (docs/claim-reason-requirements.yaml; `scripts/validate_claim_reasoning_paths.py`; supersession machine-checked via `docs/decision-status.yaml`). Every other clause of this decision, including `ReasoningPathAdequate` as introduced here and all of §§1–2 and 4–5, stands unchanged.
- **No primitive `SOUND_REASON` verdict is added to the registry** (D3 unchanged); any summary label is derived from existing semantic IDs.

### 4. Concrete reason: mandatory disambiguation

"Concrete reason" is a modern interpretive lens (Evans; applied by Turner to Ibn Taymiyyah), not classical terminology. Every use in current normative prose must declare its sense: (A) historically/socially embodied rationality `ConcreteRationality(C, t)` — a composite of accepted premises, inferential repertoire, semantic conventions, evidential authorities, defaults, incentives, and exclusions, not one ortheme; or (B) one concrete reasoning episode `ReasonEpisode(e)`. Sliding between A and B unannounced is forbidden. "Ideal reason" is a normative specification or regulative model, never a reified abstract entity. `ʿaql ṣarīḥ` (Taymiyyan reconstruction) is clear/unadulterated reason — a normative distinction *within* concrete reason. "Sound reason" without a declared bearer is forbidden; its dimensions are: faculty condition; premise/source soundness; governing-standard adequacy; token adequacy; execution fidelity; inferential validity; result correctness; truth linkage.

### 5. Higher-order cognition

A higher-order faculty outputs higher-order placements/judgments about governing types, configuration tokens, executions, and episode adequacy — or candidate proposals for new repeatable metaorthemes. Only a proposal, after type admission, becomes a metaortheme. A one-off cognitive token never becomes a repeatable type by being called "concrete."

### 6. Anti-reification (mental universals / external particulars)

Orthemes and metaorthemes are formal repeatable types; their usefulness requires no independently existing universal outside all minds. Objectivity resides in the truth of `Inst_A(m, o)` and `O*(m; A)`. "Pure/objective ortheme" is replaced by: true profile under `A`; objective instantiation fact; obtaining orthemic profile. "Objectively fitting metaortheme" is expressed through the adequacy predicate `AdequateMetaType(μ_rep; A)` (or fittingness of the type under `A`), not by positing a second subsisting object. In the theological companion, eternally known possibilities are grounded in Allah's Knowledge, never reified as an eternal abstract realm.

### 7. Fiṭrah and tawātur (mapping discipline)

Fiṭrah: an original normative disposition — representable as (i) an actor condition (orthemic state under a declared cognitive analysis), (ii) governing norms for impairment assessment (metaorthemic), (iii) case-bound assessment bindings (metaorthemmata), (iv) the audit itself as an orthing episode subject to evaluator symmetry. Never `fiṭrah = a metaortheme` or `= the orthing faculty` without a declared analysis and argument. Tawātur: never "majority agreement"; a tawātur-like metaortheme states independence/origin-continuity/competence/scope/corroboration/anti-collusion conditions; the metaorthemma binds this claim, source set, origin map, independence assessment, reference class, indicants, edition, evaluator, warrant, time; false popularization (shared upstream dependency bound as independent) is a V3c-family binding failure with possibly faithful execution.

### 8. Enforcement

`scripts/validate_type_token_semantics.py` + `docs/semantic-roles.yaml` enforce §§2–4 as **semantic-role checks with an explicit allowlist** (historical quotation; explicitly analyzed rejected terminology; "concrete orthemic placement"; "concrete reasoning episode"; "concrete representation of a metaortheme"; defined "sound placement"; dimension-declared "sound reason"; source-labeled Turner/Evans "concrete reason"), not a blind phrase ban. Conceptual fixtures CR-1…CR-8 (`tests/reason-fixtures.json`, checked by `scripts/validate_reason_fixtures.py`) keep the four-cell matrix and the binding/execution separations representable.

## Consequences

The school-neutral companion §§2–3 are rewritten (three-axis model; §2.1 strict soundness; §2.2 concrete reason/ʿaql ṣarīḥ; higher-order outputs retyped; design-argument wording de-reified); `companion/CONCRETE-AND-SOUND-REASON.md` carries the full development. Source status: the Taymiyyan material is used as **secondary reconstruction** with a primary-locus verification queue in the companion sourcing ledger; no direct attribution to Ibn Taymiyyah is presented as primary-verified in this pass.
