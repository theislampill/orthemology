# Concrete and Sound Reason: Bearers, Axes, and the Taymiyyan Comparison

**Status: companion research note (R3, 2026-07-20). Not peer reviewed; no empirical validation; school-neutral in its assertions** (the Taymiyyan material is reported as historical/comparative scholarship, not asserted as creed here). Normative typing: Decision 0009. Formal anchors: D1 (`Inst_A`, `O*(m; A)`), M1 (metaorthemma), O2 (non-factive pathway adequacy), D3 registry (no new verdicts added).

## 1. Source-status caveat (read first)

Two supplied research inputs inform this note: a *compilation* of modern scholarship on Ibn Taymiyyah's epistemology (including work by Jamie B. Turner and Carl Sharif El-Tobgui), and El-Tobgui's study of the *Darʾ Taʿāruḍ al-ʿaql wa-l-naql*. Both are **secondary scholarship**; the compilation is additionally not one authorial source and must not be cited as though it were the original publication of each included work. Every doctrine this note connects to Ibn Taymiyyah is therefore labeled **secondary reconstruction**; candidate primary loci (*Darʾ* passages; *Majmūʿ al-Fatāwā*) are carried as a **verification queue** in [`sourcing/COMPANION-SOURCING-LEDGER.md`](sourcing/COMPANION-SOURCING-LEDGER.md) and are not presented as primary-verified. "Concrete reason" vs "ideal reason" is a modern contrast the compilation associates with C. Stephen Evans (*Natural Signs and Knowledge of God*, OUP 2010 — book verified; the exact phrase pair **not** confirmed in accessible text this pass) and reports Turner applying to Ibn Taymiyyah (the verified identity is Turner, "Ibn Taymiyya on theistic signs and knowledge of God," *Religious Studies* 58(3) 2022, 583–597, doi:10.1017/S0034412521000159, which engages Evans's natural-signs framework) — an interpretive lens, not classical terminology, and its exact wording remains an open verification item. Inference-boundary legend used below: **[direct-source]** (verbatim from a named source), **[secondary-reconstruction]**, **[synthesis]** (across sources), **[orthemological extension]** (this project's own mapping).

## 2. The central correction: concrete and sound are not contraries

"Concrete" answers *whether and how something is instantiated*; "sound" answers *whether it is epistemically/normatively successful*. A concrete act of reasoning can be concrete-and-sound or concrete-and-unsound. Any framework in which "concrete" quietly functions as a pejorative — or in which one scalar `SOUND` flag summarizes independent defects — has lost information the orthemological architecture exists to keep. **[orthemological extension]**

### 2.1 The product structure

Every evaluation declares four coordinates:

```
object level  ×  mode of instantiation  ×  normative status  ×  result status
```

- **Object level:** normative specification / repeatable type · represented standard in an actor or institution · case-bound configuration token · actual execution event · resulting judgment or placement.
- **Mode of instantiation:** specified vs concretely instantiated.
- **Normative status (per bearer):** adequate/defective · sound/unsound · valid/invalid · well-functioning/impaired · properly bound/mis-bound · faithful/deviant · justified/unjustified · reliable/unreliable · truth-linked/lucky. These are not interchangeable.
- **Result status:** correct · incorrect · unresolved · route-sufficient only · accidentally correct · correctly supported but later invalidated by version change.

## 3. Reason decomposed into four roles **[secondary-reconstruction + orthemological extension]**

1. **Rational faculty** — an actually instantiated capacity to abstract universals from particulars, issue judgments about particulars, and derive further knowledge by inference (El-Tobgui's reconstruction of reason's functions). Concrete in the actor; healthy or impaired; never identified with its every output.
2. **Governing rational standards** — repeatable rules (non-contradiction; distinguish mental conceivability from external possibility; do not override necessary knowledge by unsupported speculation; interpret terms by actual convention and context; audit inherited premises and authority chains). These *may* be represented as **metaorthemes** when they govern an admitted component of a declared analysis — not every rational truth is automatically metaorthemic.
3. **Concrete reasoning configuration** — a standard materially bound to this argument, vocabulary, premise set, threshold, report corpus, edition, actor, warrant, time, and analysis version: a **metaorthemma** under M1. This is the correct home of most of what looser prose calls a "concrete standard."
4. **Execution and judgment** — the actor's application of the token is the execution/trace; the conclusion is a judgment/placement/placement claim. Neither becomes a repeatable metaortheme merely by concerning reasoning.

## 4. Concrete, ideal, clear, sound

- **Concrete reason (sense A):** a community's historically embodied rationality `ConcreteRationality(C, t)` = ⟨accepted premises; inferential repertoire; semantic conventions; evidential authorities; default abstractions; institutional incentives; habitual exclusions⟩ — a *composite*, sound in some respects and unsound in others; never one ortheme. **(sense B):** one actor's dated, situated reasoning run `ReasonEpisode(e)` — a token that can be sound or unsound. Sliding A→B unannounced is forbidden. **[synthesis]**
- **Ideal reason:** a normative specification or regulative model of rational functioning, not the historically dominant conception of one culture — and not a reified abstract entity. **[secondary-reconstruction]**
- **ʿAql ṣarīḥ:** in the Taymiyyan reconstruction, clear/pure/unadulterated reason operating through sound fiṭrah and valid sources, opposed not to "concreteness" but to reason corrupted by inherited doctrine, whim, conjecture, doubt, ulterior motive, habit, or imitation; not equatable with one modern formal logic, one cultural common sense, or majority opinion. Whether the term names a faculty, a condition, a body of immediate truths, valid reasoning, or a family resemblance among these is **left open** — the sources do not warrant false precision. **[secondary-reconstruction]**
- **Sound reason:** ambiguous until bearer and threshold are declared. Dimensions: (1) faculty condition; (2) premise/source soundness; (3) governing-standard adequacy; (4) token adequacy; (5) execution fidelity; (6) inferential validity; (7) result correctness; (8) truth linkage. "Sound reasoning" as a summary is permissible only after these are visible. **[orthemological extension]**

## 5. Formal mapping to placements and verdicts **[orthemological extension]**

- `PlacementCorrect(p̂, m, A)` iff `p̂` agrees with `O*(m; A)` at the governed level and tolerance.
- `ReasoningPathAdequate(e)`: reasoning-relevant pathway requirements pass — **non-factive** (O2): `PathwayAdequate(e) ↛ RESULT_CORRECT`.
- `ExAnteReasonable(e)`: `EX_ANTE_JUSTIFIED` passes.
- `StrictlySoundReasoning_q(e) := PathwayAdequate(e) ∧ TOKEN_TRUTH_LINKED_q(e)` — factive at the claim level (truth linkage is factive). Aggregation is **claim-wise**; an episode may contain strictly sound and non-strictly-sound placements simultaneously; any episode-level summary must state its quantifier.
- **No primitive `SOUND_REASON` verdict exists or is added**; the registry (Decision 0004) is unchanged.

Four cells stay representable (fixtures CR-1…CR-4):

| Result | Pathway | Description |
|---|---|---|
| correct | adequate | successful, adequately grounded reasoning (CR-1) |
| incorrect | adequate | justified/procedurally adequate rare miss; `EX_ANTE_JUSTIFIED` may pass; strict soundness fails (CR-3) |
| correct | defective | lucky or compensating-error result; truth linkage fails (CR-4) |
| incorrect | defective | compound failure (CR-2) |

## 6. Mapping to metaorthemes, metaorthemmata, executions **[orthemological extension]**

An actor's represented standard is `RepresentedMetaType(α, t, μ_rep)` with adequacy `AdequateMetaType(μ_rep; A)`; the materially case-bound token is `μ̄_{e,j}` (properly/improperly bound, current/stale, adequately/defectively parameterized, right/wrong source set, right/wrong analysis anchor, valid/invalid provenance); the reasoning steps are the execution. Independently representable (and fixture-guarded): adequate type + adequate token + **unfaithful execution**; adequate type + **defective token** + faithful execution. A higher-order faculty outputs placements about episodes, adequacy judgments about represented standards, binding judgments about tokens, candidate revisions — and only an admitted proposal becomes a new metaortheme. One metaorthemma may instantiate several metaortheme types only where the binding map declares each `MetaInst` relation explicitly; undeclared multi-instantiation is a well-formedness failure.

## 7. Anti-reification: mental universals and external particulars **[secondary-reconstruction + orthemological extension]**

The El-Tobgui material emphasizes a Taymiyyan distinction between externally existing individuated particulars and universals abstracted and held in the mind; the same word may apply to many realities without one independently existing universal being ontologically shared. Applied here as a *caution*, not an imported metaphysics: orthemes/metaorthemes are formal repeatable types; objectivity resides in the truth of `Inst_A(m, o)` and `O*(m; A)`; nothing requires a self-standing Platonic universal per type, an eternal metaortheme realm, orthability as an entity beside concrete reality, or an "uncreated grammar" as a second eternal object. (The theological companion grounds eternally known possibilities in Allah's Knowledge — its own school-internal claim, not repeated here.)

## 8. Fiṭrah **[secondary-reconstruction + orthemological extension]**

Fiṭrah is portrayed as an original normative disposition undergirding cognitive and moral faculties — not safely reduced to one faculty, inference rule, or metaortheme. Layered mapping: (1) actor condition — health/impairment of fiṭrah as an orthemic state under a declared cognitive analysis; (2) governing norms for identifying impairment/bias/habituation — possibly metaorthemic; (3) this assessment's calibration and evidence bindings — metaorthemmata; (4) the audit itself — another orthing episode under evaluator symmetry, so the evaluator's own fiṭrah-assessment is auditable rather than presupposed sound (the non-circularity answer: corroboration + symmetric audit, not self-certification). Corruption mechanisms (inherited unexamined commitments; whim; conjecture; doubt; ulterior motive; habit; imitation) are *candidate orthemes of an audit analysis* requiring evidence and scope — not automatic moral diagnoses.

## 9. Tawātur as a worked metaortheme/metaorthemma case **[secondary-reconstruction + orthemological extension]**

Not "many people agree." Metaortheme: a report receives the declared certainty status only when declared source-independence, origin-continuity, competence, scope, corroboration, and anti-collusion conditions are met. Metaorthemma: this claim, source set, chain/origin map, independence assessment, general-vs-specialist reference class, qualitative indicants, edition, evaluator, warrant, time, validity. Evidence: the reports and provenance. Execution: the evaluator's comparison. Placement: "this claim has the declared epistemic status." Negative control (fixture CR-6): many apparent sources copying one upstream authority — *adequate general standard + defective source-set binding + faithful execution + overconfident conclusion*; where the executor wrongly treats dependent sources as independent, the defect moves to execution. Convergence vs copying is decided by the origin map, not the count. Pan-human corroboration and report-tawātur differ and are kept apart pending primary-locus verification.

## 10. Reason–revelation conflict as an audit **[orthemological extension]**

A claimed reason/revelation conflict is a higher-order orthing episode with candidate families: invalid inference; false/speculative premise; ambiguous or shifted terminology; decontextualized interpretation; unauthenticated report; authentic report mis-scoped; mental/external category confusion; analysis mismatch; actual unresolved conflict. The audit asks separately: what is the concrete argument/report complex (orthemma); which defect/success types are candidates (orthemes); which standards govern premise, inference, semantics, authentication, category boundaries (metaorthemes); which bindings tie them to this text/edition/context (metaorthemmata); was execution faithful; is the diagnosis correct; was it truth-linked or lucky. An authority claim is not itself evidence.

## 11. Objections and limits

- **"This is over-typing."** The types earn their keep exactly where one scalar verdict would hide an independent defect (CR-5, CR-6); where no material binding exists, the zero-burden rule (M1) applies and no token is required (CR-8).
- **"Strict soundness makes external facts decide an internal-seeming property."** Yes — deliberately: the factive component is what separates sound reasoning from *ex ante* reasonable reasoning; both statuses are kept, neither absorbs the other.
- **"The Taymiyyan reading may be contested."** Recorded: everything here rides on secondary reconstruction; contested interpretive points (the exact denotation of ʿaql ṣarīḥ; fiṭrah's ontology; which corruption list is textual vs synthetic) are flagged in the verification queue, and no argument in the school-neutral companion depends on resolving them.
- **Which statuses are objective, actor-indexed, analysis-relative:** result correctness and truth linkage — objective given `A`; pathway adequacy — objective given `A` and the governance data; representations, placements, and ex-ante justification — actor-indexed; the whole typing — analysis-relative under D1, without collapsing into relativism (§2's reconciliation in the companion).
