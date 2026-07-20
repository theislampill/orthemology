# Orthemma–Ortheme Systems: An Analysis-Relative Architecture for Auditable Classification and Handling

> **Provenance.** Multi-model draft lineage with successive review passes; original headers preserved verbatim in
> [`docs/provenance/document-history.md`](../docs/provenance/document-history.md); nothing here is experimentally validated.

**Revised manuscript draft — July 2026 (revision R2). Not peer reviewed.**

## Abstract

This paper proposes and analyzes an orthemma–ortheme system: an information-processing architecture that encounters concrete occurrences, infers which repeatable operational
state-types they instantiate, preserves uncertainty when that identity is unresolved, routes each occurrence by its sufficiently validated profile, and revises its types and
governing rules when recurring error shows the current mapping inadequate. The two poles are a token and a type: an *orthemma* is a concrete situated occurrence — this utterance,
this word-token, this patient presentation, this build report for this commit — and an *ortheme* is a repeatable operational state-type it instantiates, relative to a declared,
versioned *analysis* (of which the task is one component; ground truth is analysis-relative, never task-only and never actor-relative). The thesis is stated at the outset as an
**integration discipline**: every facet of the architecture has an established neighbor (multi-label classification, POMDP belief states, the reject option,
value-of-information stopping, risk registers, ticket state machines, provenance records, process reliabilism), and the claimed contribution is not any
single facet but the union, the placement lifecycle that connects the facets, and one further object — the reified handling *episode* carrying a joint verdict vector that separates
result correctness from pathway adequacy and robustness on a single auditable record. The formal core is extended by six additions: versioned identity with labeled lineage;
analysis/actor/time indexing; typed, scoped, expiring evidence channels; factorized candidate structure with route composition; per-burden closure status; and episode reification.
The verdict remains conditional: nothing here is experimentally validated. The design was motivated by an internal casebook and one internal longitudinal engineering record,
neither of which is independently auditable or published; they function as design motivation, not validation. The coined vocabulary must beat matched established terminology on a
preregistered benchmark before any term is adopted.

**Keywords:** classification lifecycle; type–token distinction; analysis-relative ground truth; auditable episodes; process reliabilism; selective prediction; provenance; pathway adequacy; metamorphic testing; governance.

---

## 1. Introduction

### 1.1 Four concrete occurrences

Consider four concrete occurrences.

- A person says something, here and now, that reaches a listener as an ambiguous acoustic stream — compatible with "olive juice" and with "I love you."
- A learner meets an Arabic word-token whose segmentation, lemma, morphology, attached clitics, and syntactic role are not yet settled.
- A patient arrives vomiting red material; the presentation is compatible with several risk states and several causes.
- A build system emits "all tests pass" for this commit, which may mean the behaviour was genuinely exercised, or merely that files exist, or that the evidence is stale.

Each is a concrete situated occurrence. In none of them is the system's first task to decide whether two *other* cases may be merged. Its first task is to apprehend *this*
occurrence: to determine which repeatable, consequence-bearing state-types it instantiates, to act on the part of that identity it has established, and to hold the rest open. That
is the phenomenon this paper is about.

### 1.2 Two poles

We give the phenomenon a type–token vocabulary:

- **orthemma** = the concrete situated occurrence;
- **ortheme** = the repeatable operational state-type it instantiates.

An orthemma–ortheme system is an architecture built around the relation between them: concrete occurrences are encountered, apprehended, investigated, classified, represented,
routed, validated, dispositioned, and learned from by determining which orthemes they instantiate. The primary object is the relation and its lifecycle, not an isolated type and
not a bare partition boundary.

### 1.3 The thesis, stated as an integration discipline

**Central thesis.** An orthemma–ortheme system is an *integration discipline* for the token side of classification and handling work: an information-processing architecture that
encounters concrete occurrences, infers which repeatable operational state-types they instantiate, preserves uncertainty when that identity is unresolved, routes each occurrence
according to its sufficiently validated orthemic profile, dispositions every residual obligation explicitly, records each handling episode as an auditable object distinct from its
result, and revises its orthemes and governing rules when recurring error shows the current mapping inadequate.

We concede up front that each facet of this architecture has an established neighbor. Plural profiles are multi-label and hierarchical classification. The maintained candidate set
is a POMDP belief state. Abstention and escalation are the reject option and selective prediction. Deciding when to stop investigating is value-of-information stopping. Residual
obligations are risk registers; placement statuses are ticket state machines; lineage is provenance; correct-result-through-defective-process is process reliabilism; perturbation
probes are metamorphic testing. None of these facets is claimed as new. What is claimed is threefold: (i) the **union** — no one of those frameworks supplies the others, and no
practice in our (internal, non-auditable) observational record assembled all of them by default; (ii) the **lifecycle** — the explicit connection of disclosure, evidence, representation, routing, validation, closure, and
revision to the placement status of a single concrete occurrence and its successors; and (iii) the **joint episode-verdict object** — a reified handling episode on which result
correctness, evidential support, truth-connection, rule adequacy, executor fidelity, route safety, closure truthfulness, and robustness are simultaneously definable and separately
adjudicable.

### 1.4 The redundancy critique, answered inline

The strongest objection is the redundancy critique: *a composite of POMDP belief states, the reject option, multi-label classification, value-of-information stopping, a risk
register, and a ticket state machine would act identically; the residual is a glossary.* Our answer, developed in Section 12 and maintained throughout, is: the critique is correct
about each facet taken separately, and it is correct that the type-individuation mathematics is inherited. It fails at exactly one point. The six-framework composite it invokes is
a union that no member framework names and that no practice in our (internal, non-auditable) observational record assembled by default, and even the composite has no object on which a joint verdict about result and pathway can be
recorded — the composite agent can be right for the wrong reasons and possess no record on which that fact is expressible. The one longitudinal engineering case in our record
(Section 11.4) shows a maximally disciplined, lean-vocabulary operation *discovering and building*, at the cost of roughly fifty governed stops, exactly the machinery the composite
is supposed to already have. That is corroboration, not validation — it is one case, from an internal record that is not independently auditable — but it is a reason to think the union is not free.

### 1.5 Contributions and claim levels

Relative to the prior manuscript, this revision makes six formal additions:

| # | Formal addition | What it closes |
|---|---|---|
| 1 | Versioned identity and labeled lineage on the occurrence domain | "right finding, wrong copy"; verdicts silently transported across mutations |
| 2 | Analysis / actor / time indices on profiles and candidate sets | ground truth only relative to a declared analysis; cross-actor divergence as a stop signal |
| 3 | Typed, scoped, expiring evidence channels | green-but-mis-scoped validators; stale evidence treated as current |
| 4 | Factorized candidate structure with route composition | one occurrence, several independent defects, each with its own route |
| 5 | Per-burden closure status with residual dispositions | false closure as a type error; scalar "percent complete" banned |
| 6 | Episode reification with a joint verdict vector | correct-by-luck placements; pathway adequacy separable from result correctness |

Five kinds of claim stay separate throughout — conceptual framework, formal definition, empirical hypothesis, metaphysical thesis, and design vocabulary. We defend the first two
(the framework's coherence and the formal definitions); the design vocabulary is *proposed but not defended* — every coined term is benchmark-gated (Section 14) and the paper's
content survives its removal; the empirical hypotheses are stated with their tests and none has been run (Section 13); and no metaphysical thesis is defended here (the modal and
metaphysical material is split to companion papers, with only the ordinary-words relational property — analysis-relative resolvability under perturbation — retained where it
motivates the robustness fixtures).

---

## 2. Core Objects

### 2.1 Occurrence, type, and the instantiation relation

**Definition 1 (Orthemma).** An orthemma is a concrete situated occurrence — an event, object, utterance, token, episode, or artifact — considered as something to be apprehended:
this utterance now, this word-token on the page, this patient episode, this build report for this commit.

**Definition 2 (Ortheme).** An ortheme is a repeatable operational state-type that an orthemma may instantiate, relative to a declared analysis (Definition 3 and Section 2.6 — the domain and task are among its components). It is a type whose confusion
with another type would change a warranted classification, prediction, investigation, route, validation condition, closure condition, or evaluation.

**Definition 3 (Analysis-relative instantiation).** Let `M` be a domain of concrete orthemmata (plain gloss: the concrete cases) and `O` a repertoire of repeatable orthemes (the
state-types in play). The primitive instantiation relation is analysis-relative: `Inst_A ⊆ M × O`, where `(m, o) ∈ Inst_A` reads: the orthemma `m` instantiates the ortheme `o`, relative to the
declared analysis `A` — the explicit, versionable index defined in Section 2.6, whose components include the task `T = task(A)`. (Notation note: the prior manuscript used a task-indexed primitive, now retired — see the notation registry's `retired_symbols`; the letter `I` is reserved for the individuation component of the governed-component key,
Section 6. The task-subscripted `Inst_T` survives only under the abbreviation convention below.) The **orthemic profile** of `m` is its fibre,

    O*(m; A) = { o ∈ O : (m, o) ∈ Inst_A }.

The occurrence `m` and its worldly facts are not created by the analysis. What is analysis-relative is which profile of consequence-bearing operational state-types truly describes `m` in the declared repertoire; the actual profile `O*(m; A)` remains distinct from the observation of `m`, from the system's inferred profile, from the evidence available, and from any actor's belief.

**Abbreviation convention (task-relative shorthand).** `O*_T(m)` is permitted only as local scoped shorthand: after the text has explicitly fixed one analysis `A` with `task(A) = T`, and within that scope only, `O*_T(m) := O*(m; A)` — likewise `Inst_T`, `Π_T`, `𝒦_T`, `ℛ_T`, and `𝒲_T` for their `A`-indexed counterparts (`Π_A`, `𝒦_A`, `ℛ_A`, `𝒲_A`), and the unsubscripted `M`, `O` for the analysis-active domain `M_A ⊆ 𝓜` and repertoire `O_A ⊆ 𝓞`. The shorthand must not be presented as a globally well-defined function of `T` alone: two analyses can share one task while differing in tolerance, representation, boundaries, or merger family. It is **forbidden wherever more than one analysis is live** — higher-order audits, multi-actor evaluation (Section 10), cross-version comparisons, differing tolerances or governance boundaries, and comparisons between base execution and reviewer analysis — where the full `O*(m; A)` form is required. **Standing scope for this paper:** except where a passage explicitly introduces a second analysis, one declared analysis `A` is fixed with `T = task(A)`, and task-subscripted notation below is that licensed shorthand, not a second primitive. No separate task-to-analysis bridging law is introduced: there is one ground-truth primitive, and the task-relative form is abbreviation only.

The profile is generally not a singleton. One orthemma instantiates several orthemes at once and at different descriptive levels; the relation may be hierarchical, compositional,
overlapping, and temporarily unresolved. A single Arabic word-token can simultaneously instantiate a lexeme, a lemma, a morphological pattern, several affixes or clitics, a
syntactic role, a semantic contribution, and a discourse function. A build report can simultaneously instantiate a test-outcome type, an evidence-scope type, and a
provenance-currency type. An orthemma is not assigned to one mutually exclusive box.

### 2.2 Observation is not the orthemma

The occurrence and the signal it presents are different objects. Let `Ω : M ⇀ X` be the (partial, typed) observation map and `x = Ω(m)` the presently available observation of `m`.
The observation may be impoverished, aliased, or misleading; the orthemma is the concrete event that produced or occasioned it. Apprehension runs

    m --Ω--> x --evidence H_t--> p̂_t(m) --placement--> a_t --creates--> Succ ⊆ M
                                                          |______________________|
                                                        (feedback: successors re-enter M)

where `p̂_t(m)` is the system's current inferred profile (belief), `a_t` is the resulting interpretation, investigation, route, or action, and — new in this revision — the action's
**successor set** `Succ` closes the loop back into the occurrence domain (Section 2.5). The ground truth `O*_T(m)` and the belief `p̂_t(m)` are distinct; so are the observation `x`
and the occurrence `m`.

### 2.3 Known orthemma, unresolved identity

A system may know that an orthemma occurred while not knowing its orthemic identity: `m` is encountered, yet `p̂_t(m)` remains open. The right description is

    m is encountered; p̂_t(m) remains unresolved,

not "an unknown ortheme floats free." Types do not hover independently of occurrences; what is unresolved is the placement of a present, concrete case. This also separates the four
things "the hidden distinction" can mean, as facets of one relation: the actual profile `O*_T(m)` (ground truth), the evidence and candidate structure (Section 5), the inferred
profile `p̂_t(m)` (belief), and the way the belief is encoded (representation). None entails the others.

### 2.4 Placement and apprehension

**Definition 4 (Placement and apprehension).** Placement is the assignment of an inferred profile `p̂_t(m)` to an orthemma. Apprehension is the whole process of Section 2.2:
encountering `m`, observing `x`, accumulating typed evidence, narrowing the candidate structure, placing `p̂_t(m)`, routing `a_t`, and dispositioning what remains. Placement is
provisional until validated and may be revised.

### 2.5 Versioned identity and lineage (formal addition 1)

The prior manuscript said "this build report *for this commit*" and warned that "a correct classification attached to stale provenance is not a valid placement of the current
artifact" — but gave those phrases no formal object. This subsection promotes them.

**Definition 5 (Identity key and version).** Every orthemma carries an identity key `κ = id(m)` (plain gloss: *which thing this is*, surviving change) and a version `v = ver(m)`
(*which state or edition of that thing*). Two orthemmata may share `κ` and differ in `v` (the same file before and after an edit); two may share an observation and differ in `κ` (a
reused storage slot occupied by a new file).

**Definition 6 (Labeled successor edges).** An action `a` performed in the handling of `m` creates a labeled successor set

    Succ_a(m) ⊆ M,   each element reached by an edge labeled with the action that produced it,

of size **zero, one, or many**. (A read-only classification creates none; an edit creates one; a split, broadcast, or build creates many. An earlier formulation forcing a single
successor `m′ = succ(m, a)` is corrected.)

**Transport principle.** Placement validity is bound to `(κ, v)`. A placement or validation established for `(κ, v)` does **not** transport across a successor edge to `(κ, v′)` —
or to a different `κ` behind the same observation — without a lineage argument and, where the edge could have changed the placed property, fresh evidence. This makes "right
finding, wrong copy" a well-formed, detectable error rather than an invisible one: the finding was valid, and it is attached to an occurrence that no longer exists in the relevant
version. Observed instances in the casebook include a reused inode treated as the same file, verdicts silently carried across a tree substitution, ordinal position mistaken for
identity, and a stale checkout evaluated as the current one.

### 2.6 Analysis, actor, and time indices (formal addition 2)

Ground truth is only defined relative to a **declared analysis** `A`: the system and governance boundary, task, evidence and action repertoire, policy class, loss, hard
constraints, horizon, tolerance, representation family, and permitted-merger family. This section is the definition site of the index Definition 3 takes as primitive: `A` must be **explicit and versionable** — it carries an identifier and version `ver(A)`, and a change to any component above yields a new analysis version. Profiles and beliefs are therefore indexed:

    O*(m; A)       — actual profile under analysis A (ground truth relative to A);
    p̂_{A,α,t}(m)   — the profile actor α infers at time t under A;
    C_{A,α,t}(m)   — the candidate structure actor α maintains at time t.

There is no second, task-only ground truth alongside this one: `O*_T(m)` is Definition 3's scoped abbreviation, licensed only while a single fixed `A` with `task(A) = T` is in force.

Two clarifications guard the index. **Analysis relativity is not actor relativism:** the analysis is a *declared, versioned, public* index, not anyone's belief state — once `A` is fixed, `O*(m; A)` is an objective matter that every actor can be wrong about, and disagreement between actors is disagreement about one analysis-relative fact, not the coexistence of private truths. **Analysis-version transport:** a change to any component of `A` yields `ver(A)+1`, and placements, validations, and verdicts established under one analysis version do **not** transport to another without a declared transport argument (which components changed, and why the placed claims are invariant under that change) — the exact discipline Section 2.5 imposes on occurrence versions, applied to the analysis index itself.

Placement status is **actor-indexed**: a clinician can hold a distinction absent from the record; a developer can know a failure the release gate cannot express; a reviewer can
carry a verdict the pipeline has no field for. **Cross-actor divergence** — two actors' inferred profiles for the same `(κ, v)` disagreeing consequentially — is promoted in this
revision from an aside to a first-class stop signal: it is itself diagnostic and is a legitimate trigger for the governed interruption of Section 7.5, independent of either actor's
confidence. Multi-actor evaluation is developed further in Section 10.

### 2.7 The orthemic contrast, and the inherited results

**Definition 7 (Orthemic contrast).** Fix a declared analysis `A`. Two orthemes are operationally non-equivalent, `o_i ≢_A o_j`, when confusing their concrete instances would alter
a warranted classification, prediction, investigation, route, validation condition, closure condition, or evaluation beyond the accepted tolerance. An orthemic contrast is such a
non-equivalence: a criterion by which two candidate types must not be collapsed.

The contrast is a relation on types. It explains why two orthemes must remain distinguishable; it does not, by itself, tell a system what a present orthemma is. Contrast
individuates the types; instantiation constitutes the system.

Formally, for candidate types realised by evidence histories `h_i, h_j` with mixture weights `λ, 1−λ`, let `Rep_A^{i=j}` be the family of representations that place the two histories
identically (plain gloss: all the ways of treating them as one), and `Rep_A` the unrestricted family. The **merger gap** is

    Δ_A(o_i, o_j) = inf_{χ ∈ Rep_A^{i=j}} L_A*(χ)  −  inf_{χ ∈ Rep_A} L_A*(χ),

with `L_A*(χ)` the best attainable risk under representation `χ` and hard-constraint violations counted as infinite risk. Then `o_i ≢_A o_j` at tolerance `ε_A` iff
`Δ_A(o_i, o_j) > ε_A`. The individuation is relative to the representation and merger families — components of `A`, which is why the contrast subscript follows the analysis (under Definition 3's convention, `≢_T` may abbreviate `≢_A` once a single `A` is fixed). Another architecture can make the same type distinction feasible or unnecessary.

Three inherited results, kept and presented as inherited (none is a new theorem):

1. **Static operational separation.** Force two placements to share an action, and if their best individual actions differ enough, the forced merger incurs excess risk above
   tolerance — infinite if no common admissible action exists.
2. **Predictive separation under a strictly proper score.** If the task is forecasting and two placements imply different conditional distributions, one shared forecast is strictly
   worse than separate truthful forecasts; predictive difference individuates types only when prediction is the declared task.
3. **Finite-horizon safe merger (controlled bisimulation).** States with identical admissible actions, immediate losses, class-transition probabilities, and terminal losses have
   equal optimal value; the quotient preserves value. This licenses *just-in-time placement*: leave `p̂_t(m)` coarse now, run a discriminating test, and refine before the
   consequential action — preservation of a distinction can be procedural, not a persistent label.

Threshold closeness is non-transitive (`h_1 ≈_{ε_A} h_2`, `h_2 ≈_{ε_A} h_3`, yet `h_1 ≉_{ε_A} h_3`), so there is generally no unique smallest repertoire; several incomparable repertoires can
be equally adequate.

**Definition 8 (Route-sufficient apprehension, retained).** `p̂_t(m)` is route-sufficient when it pins down enough of `O*(m; A)` to select an admissible near-optimal route, even
though other orthemes in the profile remain unresolved. It is distinct from identity-complete apprehension, in which the full profile is established for the relevant purpose.
Route-sufficiency ≠ complete orthemic resolution. (Hematemesis can alter urgency and routing while the bleeding source stays open; an Arabic token's root and lemma can license
dictionary lookup before every clitic is settled.)

**Definition 9 (Under- and over-segmentation, retained).** A repertoire under-segments an orthemma when it collapses orthemes in `O*(m; A)` whose separation the task requires
(excess risk above tolerance or a constraint violation). It over-segments when it assigns distinctions the orthemma does not support, or splits at no out-of-sample benefit net of
complexity, latency, coordination, fairness, and contestability costs.

*Remark (demotion).* The prior draft's rate–distortion analogue for segmentation is demoted to this remark: its terms were undefined as stated, and a compression framing in any
case supplies no semantics and no legitimate ends. It may be reinstated if formalized.

---

## 3. Aliasing and Identity Uncertainty

The type–token framing exposes three related but distinct uncertainty patterns. The prior manuscript distinguished the first two; this revision adds the third as its own column,
because casebook evidence shows it is neither of the others.

| | Inter-orthemma aliasing | Intra-orthemma uncertainty | Identity uncertainty |
|---|---|---|---|
| **Pattern** | Distinct occurrences produce the same or confusable observation while instantiating operationally different types | One encountered occurrence remains compatible with several candidate types | It is unresolved *which occurrence* (which `κ`, or which version `v`) is actually in hand |
| **Formally** | `Ω(m_1) = Ω(m_2)`, `O*(m_1; A) ≠ O*(m_2; A)` | `C^profile ⊇ {p_1, …, p_k}`, several profiles licensing non-equivalent routes | `C^id(m) ⊆ M` non-singleton: candidates for the case's own identity/version |
| **Example** | Two jars of white powder look identical; one is flour, one is cornstarch | One acoustic stream compatible with "olive juice" and "I love you" | The log line may describe this commit's build or the previous one's; the file at this path may be the original or a reused slot |
| **Wrong reduction** | Treating it as one case with an open profile | Treating it as two cases | Treating it as profile uncertainty about a known case |

The first concerns observational equivalence across concrete cases; the second concerns unresolved placement of a present case; the third concerns unresolved *reference* — the
case's own identity key or version is among the open questions. Identity uncertainty is the pattern behind "right finding, wrong copy": there is nothing wrong with the placement as
a placement; what is open is which `(κ, v)` it is a placement *of*. A system that maintains only profile uncertainty will misfile identity uncertainty as confidence about the wrong
object — which is precisely how verdicts transport across mutations undetected. The typed candidate families of Section 5 give each pattern its own slot.

---

## 4. Evidence: Typed, Scoped, Expiring Channels (formal addition 3)

The prior manuscript's single observation map `Ω` is replaced by a family of **typed evidence channels** `{Ω_k}`, each partial (not every channel applies to every occurrence) and
each carrying declared metadata. An evidence item obtained through channel `k` is a record

    h = ⟨ channel k;  property class τ;  scope σ;  provenance;  validity/expiry ⟩

with components glossed:

- **Property class** `τ` — the three **core cross-domain classes** are `{structural, behavioral, provenance}`. Structural evidence attests to form (the file parses, the schema matches, the artifact
  exists); behavioral evidence attests to exercised behaviour (the test ran this code path on this input and observed this output); provenance evidence attests to origin and
  currency (this artifact was produced by that process from that version). An analysis may declare **domain-specific subclasses** of these (e.g., histological vs serological within a clinical behavioral/structural scheme); what it may not do is admit evidence carrying *no* declared class, or let one class's pass silently discharge another class's obligation. Exhaustiveness of the three core classes across all domains is a working hypothesis of the framework, not a theorem; the subclass mechanism is the sanctioned extension point. **Authorization is not an evidence property class.** Whether an actor was *permitted* to place, route, or
  close is a separate **warrant gate** `W` (Section 6), with warrant states such as {authorized, factually established, both, neither}: authorization can be present while nothing
  is established, and a claim can be established that nobody authorized acting on. Treating an authorization record as if it were evidence for the placed claim launders permission
  into support; the two are never merged.
- **Scope** `σ` — the set of claims, occurrence versions, and levels the item can bear on at all (plain gloss: what this check is even *about*).
- **Provenance** — which process produced the item, from which `(κ, v)`.
- **Validity/expiry** — the conditions under which the item remains current; evidence expires when the occurrence it attests to acquires a successor along an edge that could have
  changed the attested property.

**Green-but-mis-scoped.** A validator can pass while supporting nothing:

    mis-scoped pass  ≡  pass ∧ (σ(h) ∩ claim = ∅).

The check is green, and its scope does not intersect the claim being closed. Observed instances: a hash validator that establishes integrity being read as establishing semantic
validity; a stage validator whose scope was the previous stage's output being read as covering the current stage. A mis-scoped pass is not weak evidence — it is *no* evidence for
that claim, and under Section 7 it cannot contribute to closure. Symmetrically, stale evidence (valid in its day, expired by lineage) is not weak evidence for the current version;
it is evidence about a different occurrence.

Validation discipline follows from the typing: a structural check does not validate a behavioral claim; symptom relief does not establish a cure; a fluent gloss does not establish
a correct source-linked parse. Each placed claim declares the property class and scope of evidence that could support it, and an evidence-status map records, per claim: validated,
provisional, stale, or absent.

---

## 5. Candidate Structure (formal addition 4)

### 5.1 Typed candidate families

The prior manuscript's single candidate set `C_t(m)` is split by uncertainty axis into **typed candidate families**, indexed like everything else by analysis, actor, time, and
descriptive level:

| Family | Ranges over | Open question |
|---|---|---|
| `C^id` | `M` | *which occurrence* (identity/version) is in hand — Section 3's third column |
| `C^profile` | `Π_A` (profile space) | *which profile* the case instantiates — competing hypotheses may themselves be whole profiles, never coerced into single orthemes |
| `C^cause` | `𝒦_A` (cause repertoire) | *which cause* produced the state |
| `C^route` | `ℛ_A` (route repertoire) | *which operation/owner* should receive the case |
| `C^warrant` | `𝒲_A` (warrant states) | *which warrant state* obtains — authorized, established, both, neither |

Each family carries an **exclusivity marking**: elements are flagged as *alternatives* (at most one obtains — this powder is flour or cornstarch, not both) or as *co-holding
components* (several may obtain together — this one occurrence has an identity defect *and* a quantity defect). Collapsing co-holding components into alternatives forces a false
choice; the reverse collapse hides a disjunction. Optional weights over alternatives are permitted but never required; a family is consequentially open when it contains more than
one element whose members would license non-equivalent routes. An open family must carry its **evidence-to-resolve clause**: which channel, in scope, would discriminate the
alternatives. (A list of possibilities with no path to adjudication was judged a defect in the observational record, and the definition adopts that norm.)

### 5.2 The profile space and partial profiles

**Definition 10 (Profile space, partial profiles — general form first, R3).** Fix a declared analysis `A` with active repertoire `O_A`. In its most general form the **profile space** is

> `Π_A ⊆ 𝒫(O_A)` — the set of **admissible complete profiles** under the constraints declared by `A`,

where a complete profile is a subset of the repertoire that the analysis's declared constraints admit as a candidate way the occurrence could totally be, at the analysis's level of description. This general form makes no claim that every domain is naturally factorized: hierarchical, compositional, and holistically-constrained profile spaces are all instances (the R3 formal audit and counterexample ledger record the attacks that forced this generality).

**Factorized representation (one permitted family, not a universal ontology).** An analysis *may* declare its repertoire organized into **axes** (symptom, cause, severity, evidence-scope, …), each carrying the exclusivity marking of Section 5.1 and an **applicability condition**. In a factorized representation a complete profile: (i) on each **applicable** *alternatives*-marked axis selects **exactly one** admissible value; (ii) on an axis that is **objectively inapplicable** to the case records the explicit value `not-applicable` — a declared null, which is a *fact about the case under `A`*, never a representation of uncertainty; (iii) on a *co-holding* axis contains any declared-admissible subset of values, **including the empty set** where the analysis declares objective absence admissible; and (iv) violates no declared cross-axis **consistency constraint**. Whether axes partition the repertoire or overlap is itself a declaration of `A`; overlapping axes are admissible only with declared reconciliation constraints. Five states that a factorized representation must never conflate: **objective absence** (the axis applies; nothing on it obtains — an empty co-holding set), **objective inapplicability** (the axis does not apply — the `not-applicable` value), **epistemic openness** (the actor has not resolved the axis — a property of `p̂`, never of `O*`), **evidence absence** (no evidence bears on the axis — a property of `H`), and **candidate plurality** (several complete profiles remain live — a property of `Ĉ`). The first two live in profiles; the last three never do.

A **partial profile** leaves one or more axes (or, in the general form, one or more admissibility questions) undetermined: formally, an assignment of a *set* of still-admissible resolutions (the whole domain when nothing is known), and `Π_A^∂` is the space of partial profiles; every complete profile is the special case with everything determined, so `Π_A ⊆ Π_A^∂`. An **empty complete profile** (nothing in the repertoire obtains) is admissible exactly where `A`'s constraints admit it — analyses whose repertoires exhaust the possibilities may exclude it by constraint; the framework does not exclude it by fiat.

Four objects now stand in definite relations, and none may be conflated with another:

- the **true profile** `O*(m; A) ∈ Π_A` — one complete profile, fixed by the occurrence and the analysis, independent of anyone's evidence;
- the **candidate set** `Ĉ_{A,α,t}(m) ⊆ Π_A` (the typed family `C^profile`) — the set of complete profiles the actor has not yet ruled out; correctness of maintenance means `O*(m; A) ∈ Ĉ` whenever the evidence so far is veridical, and investigation shrinks `Ĉ`;
- the **inferred partial profile** `p̂_{A,α,t}(m) ∈ Π_A^∂` — what the actor currently *places*: determined on the resolved axes, open on the rest. A partial profile corresponds to the set of its completions, so `p̂` and `Ĉ` are inter-constrained (`Ĉ ⊆ completions(p̂)` when both are maintained honestly) — but **a candidate set is not one inferred profile**: `Ĉ = {p_1, p_2}` with two live complete profiles is a different epistemic state from a single vaguer `p̂`, and collapsing the former into the latter loses exactly the alternatives structure that routes and discriminating tests act on;
- optional **belief weights** — a distribution over `Ĉ` (or over an axis's alternatives). Weights are *permitted, never required* (Section 5.1), and an unweighted candidate set is a legitimate terminal representation, not an unfinished one.

This subsection supplies the definition the corpus previously used implicitly (`Π_A` appeared in the candidate-family table without a definition site); it is A-indexed through the repertoire, exclusivity markings, and constraint declarations, all components of `A` (Decision 0007).

### 5.3 Factorized profiles and route composition

Profiles factorize over axes: a placement may be resolved on the symptom axis, open on the cause axis, and resolved on the severity axis. Routes then compose. Let `r_1 ⊕ r_2`
denote the **route composition** of the operations licensed by independently resolved factors, with the semantics:

- factors with disjoint operational footprints compose freely (treat the identity defect *and* correct the quantity defect);
- where composed routes conflict, declared priority applies, and **hard constraints dominate**: a safety constraint on one factor overrides a near-optimal route on another;
- an unresolved factor contributes no route, but may contribute a containment obligation (Section 7) that composes like a route.

This is what makes route-sufficient action well-formed in the plural case: the system acts on the resolved factors' composed route while the open factors persist as explicitly
dispositioned residuals rather than being forgotten or blocking all action.

---

## 6. Metaorthemes: The Split Normal Form

### 6.1 Definition

The prior draft defined a metaortheme as a higher-order distinction "acting on" the system's machinery. This revision adopts a single, narrower normal form, aligned with the core
formalization.

**Definition 11 (Metaortheme, split normal form).** A metaortheme is a **metaorthemic configuration**

    μ = ⟨ g;  S_μ;  select_μ;  prov(μ);  ver(μ) ⟩

paired with a separable **meta-policy** `π_μ`, where:

- `g` is the **governed component** — which part of the mapping/handling machinery this distinction governs (Section 6.2);
- `S_μ` is the set of **declared competing higher-order states** the governing context may occupy, specified *in advance*, not read off one incident (e.g., {appearance-grade,
  provenance-grade} for evidence; {current, stale} for version);
- `select_μ` is the **selecting evidence** procedure that determines which state in `S_μ` actually obtains;
- `prov(μ) = ⟨authority, warrant, scope, ver(μ)⟩` is the rule's own provenance — a rule of unknown provenance is a stale-evidence problem one level up;
- `ver(μ)` is the rule's version, recorded per episode so audits can scope which placements ran under which edition;
- `π_μ`, the meta-policy, is the **conduct rule** that consults the configuration and prescribes behaviour conditional on the obtaining state ("quarantine on stale," "never place
  on appearance alone").

The distinction the rule consults and the rule that consults it are two objects. Two different meta-policies (quarantine vs re-derive) can consult the *same* configuration
(current-vs-stale); that shared consultable distinction is what a rules-only account cannot express. A metaortheme *change* induces a transformation of the mapping subsystem — the
transformation is the effect of revising `μ`, not `μ` itself.

**Anti-vacuity conditions (part of the definition, not advice).** A candidate `μ` is admitted only if: (i) `g` is named; (ii) `S_μ` is declared in advance; (iii) switching the
obtaining state changes validated placement, risk, or constraints in at least one episode class; and (iv) it is not a first-order ortheme, nor a tunable parameter of an ordinary
policy in disguise. A good policy that consults no in-advance-declared competing higher-order states is just a good policy. (Whether the *word* "metaortheme" earns keep over
ordinary words is a separate question, decided only by the terminology benchmark — Section 14; a real distinction may be admitted while its word is retired.)

### 6.2 Governed components, glossed

`g ∈ {O, I, E, D, R, V, W}`, in plain language:

- **O — repertoire:** which state-types exist and may be posited or retired;
- **I — individuation:** what counts as the same case; identity keys, versioning, lineage;
- **E — evidence:** what evidence counts, of which property class, at what grade;
- **D — disclosure:** what may be left open, and how open questions must be declared (uncertainty handling);
- **R — routing:** where cases are sent, and what happens when the correct route is unavailable;
- **V — validation/closure:** what may be called done, at what standard, and when a completion claim must be reopened;
- **W — warrant-classification:** which warrant states exist (authorized vs factually established and their combinations) and what each licenses.

**Excluded as governed components:** objectives and loss functions; the task `T` itself (changing the task changes the problem — rules are task-*indexed*, never task-*governing*);
and the governance meta-level (the precedence order among rules and the rights to revise them are parameters fixed at the declared governance boundary, where the regress terminates
and which another inquiry may reopen).

**Negative example (calibration).** In a widely discussed exchange, a conversational system's instruction of the form "be maximally truth-seeking" was described as if it were a
governing distinction of this kind. It fails every anti-vacuity condition: it names no governed component, declares no competing higher-order states in advance, specifies no
selecting evidence, and is not separable into a consultable distinction and a conduct rule. It is an *objective* — and objectives are excluded from `g` by construction. The
exchange is retained as the standing negative example of an objective mislabeled a metaortheme.

### 6.3 Worked configurations

Five configurations, each passing the minimum-specificity test:

| Configuration | `g` | `S_μ` | `select_μ` | Meta-policy examples |
|---|---|---|---|---|
| Evidence grade | E | {appearance-grade, provenance-grade} | source record or discriminating test | choose which test to run before placing |
| Version currency | I | {current, stale} | lineage check of `ver(m)` against latest | quarantine on stale; or re-derive on stale |
| Depth of resolution | R, V | {route-sufficient, identity-complete} | task declaration + risk class | release the route while holding residuals open |
| Closure standard | V | per-burden dispositions vs "all done" | the residual ledger (Section 7) | claim completion only at the ledger's level |
| Warrant state | W | {authorized, established, both, neither} | authorization record vs validating evidence | tag warrant type; never launder one into the other |

### 6.4 Plurality, conflict, precedence

A typical episode runs under several metaorthemes at once — a version rule, an evidence-grade rule, and a closure rule — written `μ⃗ = ({μ_1, …, μ_k}, ≼)` with `≼` a declared
strict partial precedence order. Configurations governing disjoint components compose freely (their constraints conjoin). Two rules conflict at an episode when their meta-policies
prescribe incompatible constraints on the same component under the states that actually obtain; resolution is only via `≼`, and a conflict unresolved by `≼` is a stop condition
(Section 7.5) — silent override is itself a metaorthemic error. Metaorthemes can become first-order orthemes for a higher audit (Section 8.1); the regress stops at the declared
governance boundary.

---

## 7. Closure, the Lifecycle, and Revision (formal addition 5)

### 7.1 The lifecycle, recast per burden

The prior draft drew the lifecycle as one line — encountered → unresolved → candidate profile → investigated → provisionally placed → validated → routed → integrated. The line
survives as a *typical trajectory of a single burden*, but the object that matures is not the case as a whole; it is each **burden** — each claim to be established and each
obligation to be discharged — separately. A case has no scalar completion state, and scalar "percent complete" reporting is banned as ill-typed: it averages incommensurable burden
states into a number that licenses nothing.

### 7.2 Failure modes as relation failures (retained taxonomy)

These are failures in the relation among occurrence, type, evidence, representation, and operation — not merely partition errors:

- **non-disclosure** — the system never notices that `m` requires a distinction;
- **orthemic underdetermination** — several consequential candidates remain open;
- **misidentification** — `m` is placed under the wrong ortheme;
- **under-segmentation** — several orthemes in `O*(m; A)` are collapsed;
- **over-segmentation** — distinctions are assigned that `m` does not support;
- **misplacement** — a valid description is attached to the wrong occurrence, component, level, or temporal version (the lineage failures of Section 2.5, including
  review-transport: a verdict formed about one artifact carried by the review process onto another);
- **representational failure** — the correct ortheme is recognised but cannot be encoded;
- **misrouting** — the correct ortheme is assigned but `m` is sent to the wrong operation;
- **validation failure** — the placement or repair is not genuinely tested;
- **false closure** — `m` is treated as fully resolved though consequential parts of its profile or its burden ledger remain open.

Each has a distinct remedy; they need not share a cause. Low confidence is not the only abstention trigger: broken provenance, an unavailable route, or a hard safety conflict can
be decisive under a confident placement.

### 7.3 Per-burden residual dispositions; false closure as type error

**Definition 12 (Residual disposition).** Every burden of an episode carries, at closure time, exactly one disposition from

    { unresolved, deferred, transferred, owner-assigned, risk-accepted, validated-resolved }

glossed: still open with no plan (unresolved); open with a declared later trigger (deferred); moved to another party with traceable ownership (transferred); waiting on a named
owner's decision (owner-assigned); consciously left open under an accepted, recorded risk (risk-accepted); or closed on in-scope, current, sufficient evidence (validated-resolved).
The six dispositions are **mutually exclusive by fiat** — each burden carries exactly one — with a precedence rule for the one genuinely overlapping pair: a burden that has been
handed to a named decision-maker whose *choice* is what is awaited is **owner-assigned**; a burden whose *work* has been handed to another party is **transferred**. When both
descriptions apply (work moved to a party who must also decide something), owner-assigned takes precedence, because the blocking condition is the decision. A disposition change is
an event on the ledger, never a reinterpretation of the old record.

**Definition 13 (False closure, retained and typed).** False closure is a completion claim that collapses distinct dispositions — unresolved, deferred, transferred, owner-assigned,
or risk-accepted — into "validated-resolved." In this revision it is a **type error in the record/schema sense** (no type-theoretic machinery is invoked): the completion claim quantifies over the burden ledger, and it is well-formed only when every
burden's disposition admits it — a checkable well-formedness condition on the closure record, violated exactly when the claim and its own ledger disagree. "Done" uttered over a ledger containing a deferred burden is not an optimistic judgment; it is a claim whose type its own ledger refutes. Closure is
legitimate exactly when every required burden is validated-resolved, or explicitly deferred/transferred/ owner-assigned/risk-accepted under an admissible policy, and the evidence
supports the declared level of completion. Safe closure is reopenable by record; false closure accrues silent exposure.

*Remark (demotion).* The prior draft's "orthemic debt" register is demoted to a speculative instrument: it remains unvalidated against ordinary defect counts, hazard registers, and
technical-debt metrics, and nothing in the observational record supports it. It is no longer part of the core proposal.

### 7.4 The claim ledger and required success surfaces

Closure quantifies over an explicit **claim ledger** `Q`: per claim, the record holds the proposition; the target occurrence and version `(κ, v)` it is about; the property class of
evidence that could support it (Section 4); the **required success surface**; the supporting evidence items by identifier; the warrant where relevant; the verification status; and
explicit non-claims (what is *not* being asserted, recorded to block later inflation).

The **required success surface** is the declared locus where the claim's success must be observable: a repair claim's success surface is the live behaviour of the current version,
not the repository diff; a migration claim's surface is the serving system, not the migration log. A claim verified anywhere other than its declared surface is at best provisional.
(The observational record's "repo-green, surface-broken" case is the canonical instance: every check the repository could express passed, and the user-visible surface was broken —
the claim had been verified off-surface.)

### 7.5 Generalized ANDON: stop on risk, not on surprise (retained)

A generalized ANDON event is a governed interruption when safe continuation or closure is not warranted under the current placement, evidence, model, route, or objective. Its
signals are heterogeneous — observation novelty, intra-orthemma underdetermination, identity uncertainty, transition surprise, structural contradiction, evidence insufficiency or
expiry, routing or capacity failure, validation failure, false-closure detection, cross-actor divergence (Section 2.6), unresolved metaorthemic conflict (Section 6.4), and safety
conflict — and they are not the same signal. Stopping should track continuation risk, not anomaly:

**Proposition (ANDON sufficiency, retained framing).** If stopping or escalating is admissible with conditional risk at most `θ_stop`, while every continuation action exceeds risk `θ_stop`
or violates a hard constraint, then every risk-minimising admissible policy stops or escalates. *(The stop/escalate action has lower conditional risk than every admissible
continuation and meets the constraints, so no continuation is optimal.)*

The loop ends when residual obligations in the ledger have been reread — not when the original alarm disappears.

### 7.6 Revision as a governed mode

The prior draft's "revise" was one word. The record shows it needs its own machinery. A **revision operator**

    ρ : (μ, lesson) ↦ μ′        (and analogously for repertoire revisions ρ : (O, lesson) ↦ O′)

is governed by:

- **a formal trigger** — a recurring error class attributable to the current distinction or rule, not a single incident (one miss licenses a hypothesis, not a revision);
- **a complexity penalty** — the revised rule or repertoire pays for its added distinctions against out-of-sample benefit (Definition 9's over-segmentation costs apply to rules as
  well as types);
- **hysteresis** — revision and reversal thresholds differ, so the repertoire does not churn on boundary noise;
- **impact-scoped reopening** — `ρ` increments `ver(μ)` and computes the set of *affected* prior episodes: exactly those whose placement consulted the revised state-distinction or
  selector where the two editions disagree. Only those episodes' evidence status is downgraded from validated to provisional pending re-check. Blanket reopening of everything that
  ever ran under the old edition is rejected as unscoped;
- **a second-order variant** — when a *pattern across occurrences* (not any single case) shows the state space itself was under-specified, revision enters an enumeration mode: the
  alternatives are listed exhaustively against the record rather than patched one neighbor at a time. The observational record contains one such tranche, where serial
  one-neighbor-per-review revision was escalated to enumeration after repeated single-case patches failed to converge.

---

## 8. Episode Reification: Orthing Episodes and the Verdict Layer (formal addition 6)

### 8.1 The process type, the concrete token, and the reification embedding

**Orthing** (gloss: the doing of apprehension-and-handling) is a process TYPE: the rule-governed, evidence-updating operation kind by which an orthemma is individuated, observed,
assigned typed candidate families and an inferred profile, routed, validated, dispositioned, and revised under one or more metaorthemes. It stands to its runs as "compilation"
stands to "the 14:32 build of commit `abc123`." An **orthing episode** `e` is a concrete TOKEN: one dated, situated run, with an actor, a time, an input occurrence, and a result;
two episodes are distinct occurrences even when inputs and outputs agree.

When a higher audit asks "was this placement made correctly, on adequate evidence, under an adequate rule?", the episode is itself apprehended, via an explicit **reification
embedding** `ι_n : E^(n) ↪ M^(n+1)` — yesterday's classification act, re-cast as today's case. This is a modeling step, not set membership: an episode is a different kind of thing
from a jar of powder and becomes a base occurrence of the higher audit only by being cast as one. The audit's orthemes at level `n+1` are pathway state-types — evidence-sufficient
placement, stale-rule placement, false closure — precisely the verdicts below. No separate noun ("meta-orthemma") is coined for the reified episode: against the paper's own
anti-vacuity standard, the new noun changes no representation, evidence, routing, or prediction that the embedding does not already provide. The regress stops, as always, at the
declared governance boundary.

### 8.2 The episode signature (cited compactly)

Following the core formalization, an orthing episode is a record

    e = ⟨ id;  m, κ, v;  x, H;  α, w, A, T, t;  μ⃗, MetaTok, π;  C⃗, p̂;  r;  estatus;  𝒬;  δ;  hand_in, hand_out;  a, Succ ⟩

— in words: which run this is; the concrete case with its identity key and version; what the episode saw, and the ordered typed evidence gathered (each item with property class,
scope, provenance, validity); who or what executed (`α` — populated even for mechanical executors) and under what warrant (`w`, distinct from both evidence and executor identity);
the declared analysis `A` (identifier and version — the index against which result correctness is judged), its task `T = task(A)` retained as a separate readable component, and the time; the governing metaorthemic configurations with precedence; `MetaTok(e)` — the concrete **metaorthemmata** (Decision 0002): case-bound configuration tokens of those governing types, each recording or referencing its identity and lineage, type-and-version via `MetaInst(μ̄, μ)`, analysis compatibility `Compatible(μ̄, A(e))`, occurrence anchor `(κ, v)`, governed component, case-specific binding map, scope with the claims that depend on it, policy/evidence-selector/instrument-and-calibration references, the binder with its binding warrant (kept distinct from the designated executor), binding time, and validity — referencing but never absorbing the episode's evidence and trace, and omitted entirely where no material case-specific binding exists (then V3c is inapplicable); the concrete policy executed under them; the typed candidate families and the
inferred placement `p̂` (profile-valued, never coerced to a singleton ortheme); the route; the per-claim evidence-status map; the claim ledger with required success surfaces; the
per-burden residual-disposition map; the incoming and outgoing handoff records; and the action with its labeled successor set. Components are defined *where applicable*: a
read-only classification episode has no action, no successors, an empty residual map — and the governance-derived required set `ReqPath(e)`, together with a recorded
`not-applicable` reason for every excluded verdict, keeps "deliberately none" distinct from "omitted." Where the pathway verdicts below must be adjudicated from the episode's own record, a bounded ordered trace of states and updates is also required, at a
granularity governance declares — trivial cases carry no trace, and maximal logging is never a blanket requirement.

Three separations, stated once: the **episode is not its output** (episodes with identical outputs can differ in pathway and hence in every verdict); the **episode is not the
policy** (the policy is repeatable and undated; reliability claims attach to the policy and its governing rules, correctness claims to the episode); a **placement inside an episode
is not the episode** (the convenient one-placement notation `e ⊨_μ (m : ô)` is derived, not definitional).

### 8.3 The verdict vector

The verdicts diagnose distinct dimensions and are not identified with one another; they are NOT assumed pairwise logically independent — every definitional implication is declared explicitly, and the only one these definitions introduce is the claim-wise `V2b-T_q → V1_q` (full implication table: core formalization §4.1; Decision 0003, superseding the earlier "none entails another"). Verdict labels follow the normative registry (`docs/verdict-registry.yaml`, Decision 0004): semantic IDs — `RESULT_CORRECT`, `EVIDENCE_SUPPORT`, `PROCEDURE_RELIABLE`, `TOKEN_TRUTH_LINKED`, `EVIDENCE_CURRENT`, `GOV_CONFIG_ADEQUATE`, `GOV_POLICY_ADEQUATE`, `GOV_TOKEN_ADEQUATE`, `EXECUTION_FAITHFUL`, `EX_ANTE_JUSTIFIED`, `ROUTE_ADMISSIBLE`, `ROUTE_QUALITY`, `CLOSURE_TRUTHFUL`, `ROBUST_NEIGHBORHOOD` — are authoritative in machine-readable records; the `V…` display aliases below are the prose forms. Pathway adequacy conjoins over the RESULT-FREE governed core `CorePath = {V2a, V2b-P, V2c, V3a, V3b, V3c, V3d, V3e, V4a, V5, V6}` — V1 (result), V2b-T (factive), and route near-optimality are excluded. The required set `ReqPath(e)` is DERIVED from the declared analysis, episode shape, risk class, claims, and governance (never a discretionary list; "not tested" is never "not applicable"; every exclusion carries a recorded reason), and each verdict carries a status in {pass, fail, undetermined, not-applicable}: `PathwayAdequate(e)` iff every required verdict passes; `PathwayDefective(e)` iff one fails; `PathwayUndetermined(e)` when none fails but something required is unevaluated — a missing assessment is never silently a pass.

| Verdict | Question it answers |
|---|---|
| **V1 — result correctness** | Does the placed profile agree with `O*(m; A(e))` — the actual profile under the analysis recorded in the episode — at the governed level (or, weaker, is it route-sufficient with every placed claim true)? **Result-side: never a conjunct of pathway adequacy.** |
| **V2a — evidential support** | Does the typed evidence, within its declared scopes, meet the declared standard for each placed claim? |
| **V2b-P — configured-procedure truth-conduciveness** (pathway-side; NON-FACTIVE) | Does the procedure family actually instantiated here — under its governing configuration, applicable metaorthemmata, and execution mode — satisfy the predeclared reliability criterion over its DECLARED reference class (per-claim `RelSpec_q`: reference class, stratum, metric, threshold, perturbation/comparison family, protocol, reliability evidence, version/validity)? The reference class and threshold are fixed independently of this episode's outcome; one current correct result cannot by itself establish it; **it does not entail V1** — a reliable configured procedure may produce a rare error. Default criterion: sensitivity; declared variants admissible. |
| **V2b-T — token-level truth linkage** (result-side annotation; EXCLUDED from the pathway core) | Was THIS placed claim correct through the truth-relevant evidential mechanism rather than merely alongside it? FACTIVE and claim-wise: `V2b-T_q → V1_q`; a profile-level reading requires every placed claim covered plus an explicit aggregation rule. Reportable for stopped-clock/Gettier diagnoses; excluded from `PathwayAdequate` precisely because its factivity would re-import result correctness. Non-factive token-local defects belong under V2a/V2b-P/V2c/V3a/V3b/V3c/V3d/V6, never under V2b-T alone. |
| **V2c — evidence currentness** | Is each load-bearing evidence item current for `(κ, v)` and of admissible provenance — not stale, not unsourced? |
| **V3a — configuration adequacy** | Was each governing configuration adequate for the case's risk class — do its declared states separate what this case class can occupy, and can its selecting evidence actually discriminate them? |
| **V3b — policy adequacy** | Was the meta-policy/procedure well-formed for the configuration it ran under? (A sound rulebook can carry an ill-formed procedure.) |
| **V3c — governing-token adequacy** (Decision 0002) | Was every applicable concrete metaorthemma — the case-bound configuration token of a governing type (§8.2) — correctly instantiated, analysis-compatible, occurrence-anchored, correctly scoped to its claims, current, provenanced, and bound under authority? Per-token statuses are preserved alongside the episode-level conjunction; with no applicable token, V3c ∉ ReqPath(e) (zero-burden rule; status recorded not-applicable, with reason). Isolates: correct standard + sound policy + faithful execution + **defective case-specific binding** (wrong reference plane, wrong-role tolerance, expired calibration, wrong fixture or success surface). The Decision-0004 lettering matches the conceptual order: V3a → V3b → V3c (binding) → V3d (execution) → V3e. |
| **V3d — executor fidelity** | Did the actor actually execute the procedure as written? (Adequate rule + adequate policy + infidelic executor routes to a different remedy: retrain or replace the executor, not rewrite the rule.) |
| **V3e — ex-ante justification** | At decision time, on exactly the evidence then available, was the placement the reasonable one under the declared standard? (Blameless-at-the-time; indexed to decision time, unlike V2a/V2b-P/V2b-T, which are audit-time verdicts.) |
| **V4a — route safety** | Was the route admissible under the constraints in force? Correct-route-unavailable is recorded as routing failure, not diagnostic uncertainty. (A finer near-optimality verdict may be recorded separately: safe ≠ best.) |
| **V5 — closure truthfulness** | Does every residual carry an admissible disposition with traceable ownership, and does the completion claim match the ledger — no collapse of deferred/transferred/risk-accepted into "resolved"? |
| **V6 — robustness** | Over the declared perturbation neighborhood of the episode — same policy, same rules, inputs from a declared perturbation family (version bumped, marker removed or spoofed, evidence reordered, near-identical sibling substituted) — is the V1 failure rate below tolerance? Paired metamorphic probes are V6's operational estimator. |

### 8.4 The result × pathway matrix

The matrix applies only after the pathway status resolves as adequate or defective; `PathwayUndetermined` episodes remain outside the four cells until audited. (Decision 0003: the earlier parenthetical committing token-level truth-connection to the conjunction is superseded — the incorrect-result/adequate-pathway cell is genuinely representable.)

| | **PathwayAdequate** | **PathwayDefective** |
|---|---|---|
| **Result correct (V1)** | **Nominal.** A release gate runs the behavioural suite against the exact commit it gates, on current artifacts, correctly bound (V3c where applicable), under a reliable configured procedure; it passes; the build is in fact good. Nothing to fix. | **Correct + defective (stopped clock / compensating error / governing-side luck).** The answer is right; the failure locus is V2b-P, V3a, V3b, V3c, V3d, or V6. The remedy targets the procedure, rule, or binding — not the verdict. Worked example below. |
| **Result incorrect (¬V1)** | **`AdequatePathError(e) := ¬V1(e) ∧ PathwayAdequate(e)`** — the justified rare miss of a non-perfect but sufficiently reliable process used correctly. A triage router places a failing test under "infrastructure flake" because every available signal points there; the true cause is a rare race in new code: V3e holds, the procedure met its declared reference-class reliability (V2b-P), and the pathway IS certified adequate; `V2b-T` fails for the claim (it is false). Where V3e ∈ ReqPath(e), `JustifiedMiss(e) := AdequatePathError(e)` (V3e's pass is already inside PathwayAdequate). Remedy: a new discriminating evidence source; no rule or executor blame. Orthemic adequacy does not establish moral, legal, institutional, or theological blamelessness. | **Compound failure.** A deploy gate reads a cached test result from the previous commit and approves the current one: wrong placement via a defective pathway (¬V1; V2c, V3a fail). Remedy: both the placement and the lineage machinery. |

Deterministic fixtures establishing all four resolved cells (plus the undetermined state, the stale-directive case, and safe-but-suboptimal routing) are given in the core formalization §4.2 (F1–F7) with machine-checkable encodings in `tests/verdict-fixtures.json`.

### 8.5 Worked example: the stopped-clock validator

A scan validator's rule is: *pass iff the output log contains the marker string* `SCAN-CLEAN`. On today's artifact it passes, and the artifact happens to be genuinely compliant.

- **V1 holds:** the placed claim ("compliant") is true.
- **V2a arguably holds by the letter:** the declared standard — marker presence — was met.
- **V2b-P fails at the default sensitivity criterion:** over its declared reference class, had an artifact been non-compliant with the marker present (a tool version that always prints it; a spoofed log), the
  procedure as configured would still have supported the claim — the configured procedure is not truth-conducive. (**V2b-T also fails as a result-side diagnosis:** this claim was correct, but not *through* the truth-relevant mechanism — the stopped-clock signature.)
- **V6 fails:** the perturbation neighborhood exposes it directly — compliant-without-marker is rejected; non-compliant-with-marker is passed. The paired probes are exactly the
  metamorphic fixture pair.
- **V3a fails:** the governing evidence configuration is inadequate for the risk class — its selecting evidence cannot discriminate the states it is supposed to separate.

This is the operational analogue of the stopped clock that shows the right time twice a day: correct result, defective pathway, high neighboring-case failure risk. The verdict
layer expresses this on the episode record itself; a system tracking only result correctness has no object on which the defect is even statable, and will discover it only when a
neighbor arrives.

### 8.6 The novelty claim, stated narrowly

The defensible claim is exactly this and no more: **the prior manuscript, and the operational discipline it describes, did not explicitly represent the concrete
classification/handling episode as an auditable occurrence distinct from its result.** It is *not* claimed that episodes are inexpressible elsewhere. Process reliabilism names
precisely the correct-result-through-unreliable-process structure and the truth-connection idea — for *beliefs*; it offers no operational record schema (no typed evidence, route,
residual disposition, successor set, or perturbation estimator for agent and validator episodes). Provenance and audit-trail systems (W3C PROV, audit logs, ML lineage) are
operational and token-level — who did what to which artifact when — but typically carry no candidate structure, plural inferred profile, per-claim evidence status,
residual-disposition ledger, or verdict layer separating result correctness from pathway adequacy and robustness. Assurance practice (control-effectiveness vs outcome testing) and
metamorphic testing each contain one verdict without the joint object. The residual contribution is the **integrated joint verdict layer on one auditable object**; whether that
integration pays for itself over "audit the validator when suspicious" is an open empirical question (Section 13.2), not a settled fact.

---

## 9. Mechanical and Distributed Orthing

### 9.1 Consciousness is not required

Nothing in the episode signature or the verdicts quantifies over awareness. Any rule-governed, evidence-updating executor — a predictive-text decoder resolving an ambiguous
keypress sequence, a CI validator, a triage pipeline, a review chain, an institution — executes orthing, and its episodes bear all *applicable* verdicts. Stopped-clock analogues
arise mechanically: a decoder emits the right word from a frequency prior that would misfire on the neighboring input — correct message, defective pathway, no conscious subject
anywhere. The actor field `α` is therefore populated with the mechanical executor — never left empty — and executor identity is distinct from any warrant or authority index.
Semantic depth (hard-coded check < model-based inference over declared alternatives < reflective capacity to propose rule revisions) is a real axis of the *executor*, orthogonal to
every verdict on the *episode*: shallow executors can run adequate pathways and deep ones defective pathways. Depth matters operationally in one place only: which revisions the
executor may perform locally versus must escalate across the governance boundary.

### 9.2 Distributed episodes: the token-level DAG

One case handled across sensors, validators, agents, routers, a human sign-off, and downstream consumers is modeled as a finite **DAG** `Γ_E = (E, ⇝)` whose nodes are episodes
(each with the full signature — its own actor, its own governing configuration) and whose edges are **typed**:

- **handoff** — a projection of one episode's output (a partial profile, an evidence item with its scope, a route, a disposition) appears in the input or evidence of the next;
  handoffs are the loci of transport error — a verdict crossing an edge without its scope and version is how stale evidence propagates;
- **supersession** — a later episode revises an earlier one's conclusions;
- **retry-of** — a later episode re-attempts an earlier one's task.

**Why a DAG despite retries and review loops:** nodes are *dated tokens*; every edge is oriented from the earlier node to the later node with the semantics carried by its label (the later node of a supersession edge revises the earlier; the later node of a retry-of edge re-attempts the earlier's task), so the token graph is acyclic by construction. A rework loop does
not add a back edge — it creates a *new* episode node reached by a retry-of or supersession edge from its predecessor. The genuinely cyclic structure (the same policy re-entered; review
returning work to an author role) lives at the TYPE/policy level, represented as repeated instantiation of the same policy, never as cycles among tokens.

### 9.3 Composition conditions

The graph composes into ONE boundary-level episode `e_Γ = comp(Γ_E)` iff:

1. **one case, one analysis** — all sub-episodes address `m` or its successor-lineage under a single declared analysis `A` (hence one task `T = task(A)`; sub-episodes sharing a task but differing in tolerance, representation, or boundary do NOT compose without an explicitly declared fusion analysis);
2. **a declared boundary** — governance names the composite actor (pipeline, team, institution) and the composite governing configuration, including precedence across sub-episode
   rules;
3. **a declared fusion rule** — the composite placement, evidence-status map, and residual ledger are a stated aggregation of sub-outputs (e.g., profile union with per-claim status
   equal to the weakest status along its supporting path; merged ledgers with surviving ownership) — well-defined, not read off the last node.

When condition 2 or 3 fails there is only the graph, and talk of "the system decided" is unwarranted composite attribution. Composite verdicts do not reduce to conjunctions: the
composite can be correct while a sub-episode was wrong (a downstream validator caught it), and every sub-episode can be correct while the composite fails (each verdict true in
scope, the composition transporting one out of scope). The composite level must be audited separately.

---

## 10. Multi-Actor and Competitive Settings

### 10.1 One occurrence, many evaluations

The actor and analysis indices of Section 2.6 already imply that a single concrete occurrence supports several simultaneous evaluations: the same `(κ, v)` is apprehended by different
actors, each under its **own declared analysis** `A_α` — sharing frame components where the actors share a game or institution, and differing at least in task `T_α = task(A_α)` — each with its own inferred profile and candidate structure. This is a multi-analysis context: Definition 3's task-relative abbreviation is forbidden here, and ground truth is written in full, `O*(m; A_α)`, per evaluating analysis. This section develops the special case where the actors' interests diverge. In imperfect-information games the divergence begins one level earlier, at OBSERVATION: the one concrete deal `m` is shared, but each actor observes only `x_α = Ω_α(m)` — the paper's own observation/occurrence distinction (§2.2), applied per actor. A player's information set is therefore an OBSERVATION, never part of the occurrence's identity key; perfect-information games are the special case of full, equal observation.
Everything here is a **derived extension of the existing actor/analysis indices — not a seventh formal addition**; no new primitive is introduced.

### 10.2 Target profiles

**Definition 14 (Target profile set).** For actor `α` under its declared analysis `A_α` with task `T_α = task(A_α)`, the target profile set `𝒢_{α,A_α} ⊆ Π_{A_α}` is the SET OF PROFILES that `α`, under `T_α`, aims to make some future occurrence in the lineage instantiate — each member of `𝒢_{α,A_α}` is one complete profile (normative typing, aligned with the core formalization §5.3; a win-ortheme such as "White checkmates Black" labels the FAMILY of terminal profiles realizing it). `𝒢_{α,A_α}` is the grounded instantiation at `α` of a PARAMETRIC ortheme schema `GoalSchema(α)` ("win for α"): the schema is one form under role substitution; the grounded targets are distinct; and target-set overlap is a third, independent relation (empty for zero-sum win-sets, total for cooperation).

Three separations keep this well-typed:

- `𝒢_{α,A_α}` is **not the current descriptive profile** `O*(m; A_α)`: the descriptive profile says what the occurrence *is*; the target profile says what some successor should
  *become*. A chess position's descriptive profile may include "material equality, White to move"; neither player's target is a description of the present board.
- `𝒢_{α,A_α}` is **not the objective/loss**: the loss is the task's evaluation function over outcomes; the target profile is the *state-type content* of what the actor pursues — a
  set of orthemes over future occurrences, usable in placement and routing like any other type. (Objectives are excluded from metaorthemic governance, Section 6.2; target profiles,
  being typed state-sets under the actor/analysis index, are ordinary indexed objects.)
- `𝒢_{α,A_α}` is **not a metaortheme**: it names no governed component and declares no competing higher-order states about the machinery.

### 10.3 Structural isomorphism is not identity of targets

In symmetric games, a role substitution (swap the colors, relabel the players) maps one actor's target set onto the other's: the targets are **structurally isomorphic**.
Declared prose abbreviation for this section and the next: the role labels **White** and **Black** name the formal actors `α` and `β` respectively, with per-actor analyses `A_α, A_β` and tasks `T_α = task(A_α)`, `T_β = task(A_β)`.
Isomorphism under role substitution is *not* identity: `𝒢_{α,A_α} ≠ 𝒢_{β,A_β}` even though each is the image of the other under the color swap. Conflating them is a placement
error at the actor index — precisely the error a non-indexed formalism cannot even state, because it has only one profile slot per occurrence.

### 10.4 Worked example: chess

The shared concrete occurrence `m` is *this board position in this game*, where the occurrence's identity includes the position, the full move history, and the player to move
(castling and en-passant rights are functions of that history). Both players apprehend the same `m`: one occurrence, two actor/analysis-indexed evaluations `p̂_{A_α,α,t}(m)` and
`p̂_{A_β,β,t}(m)` (the §10.3 role-label convention: White = `α`, Black = `β`), and two target profiles `𝒢_{α,A_α}` (state-types realizing a win for White) and `𝒢_{β,A_β}`.

The example also calibrates what is and is not a metaortheme:

- the **transition rules** (legal moves) are part of the *domain* — they define the successor structure of `M`;
- the **utility** (win/draw/loss values) is the *task*;
- **minimax search** is a *policy* — both players may use similar policies over the shared transition rules;
- **none of these is a metaortheme.** A metaorthemic configuration in a game would govern, for example, *what counts as evidence of the opponent's information state* (in
  imperfect-information games: governed component E, competing states such as {revealed, inferred-from-tempo, unknown}, selecting evidence declared in advance), or *when analysis
  may stop* (governed components D and V: a declared stopping standard for search — quiescence reached vs time-budget exhausted — whose variation changes which placements may be
  acted on). These pass the anti-vacuity conditions; the rules, the utility, and the search policy do not.

### 10.5 Draws, cooperation, and conflict predicates

**Draws exist:** not every terminal occurrence realizes a player's positive target. The two target sets do not partition the terminal states; there is a third region realizing
neither. Any formalization that forces every terminal state into some actor's target set has mis-specified the game.

Over a set of actors with target profiles `{𝒢_{α_i,A_i}}`, the predicates are well-typed across profile spaces — the target sets live in *different* spaces (`𝒢_{α,A_α} ⊆ Π_{A_α}`), so they are never compared by bare set intersection. With `Reach(m)` the occurrences reachable from `m`:

- **Compatibility:** `Compat_m(𝒢_1, 𝒢_2)` iff `∃ m′ ∈ Reach(m): O*(m′; A_1) ∈ 𝒢_1 ∧ O*(m′; A_2) ∈ 𝒢_2` — one shared occurrence, evaluated under each analysis separately;
- **Conflict:** `Conflict_m(𝒢_1, 𝒢_2)` iff no such reachable `m′` exists — zero-sum chess targets conflict by construction;
- **Cooperation (special case):** a shared target profile, `𝒢_{α_1,A} = 𝒢_{α_2,A}` under one shared analysis — the actors may still differ in evidence, roles, and routes (that is what the
  distributed-episode machinery of Section 9.2 is for), but their targets coincide.

Mixed-motive settings sit between: targets partially overlap, and the conflict/compatibility predicates apply region by region. All of this is bookkeeping over indexed profiles and
lineage — the machinery of Sections 2 and 9 — which is why it is derived, not primitive.

---

## 11. Examples

Each example is one architecture: orthemma → typed candidate families → typed evidence → validated placement → composed route → dispositioned residuals. The framework is
substrate-neutral only as a design heuristic; it claims no shared mechanism across the domains. For each case the analyst must name the physical and social information carriers,
boundary, decision rights, and validation.

### 11.1 The build report

The orthemma is *this build report for this commit* — with identity key (the commit) and version (the artifact set actually built). The observation is the string "all tests pass."
The candidate structure is typed: `C^profile` contains "behaviour genuinely exercised" and "files merely exist" as alternatives on the evidence-scope axis; `C^id` contains "report
describes this commit" and "report describes the previous commit" (identity uncertainty, Section 3); `C^warrant` records whether the release is authorized, established, both, or
neither. The discriminating evidence is typed: a behavioural channel (the suite demonstrably executed these paths on this artifact) versus a structural channel (the log line
exists) versus a provenance channel (the log was produced by this run from this commit). A green check whose scope does not intersect the release claim is a mis-scoped pass and
contributes nothing to closure. The route composes over resolved factors — release, repair, or reject — and closure quantifies over the burden ledger: a release with a deferred
flake-investigation burden is closed *with a deferred residual*, not "done."

### 11.2 The Arabic word-token

The orthemma is *this word-token* on this page. Its candidate profile spans segmentation, lemma, lexeme, morphological pattern, clitics, syntactic role, and vocalisation —
co-holding components, not alternatives: a future particle plus imperfect verb plus plural marking plus object clitic is one composed placement, and Arabic computational morphology
explicitly separates tokenisation, lemmatisation, features, clitics, and contextual disambiguation. Root and lemma can be route-sufficient for dictionary lookup before every
dependency is resolved — the factorized profile acts on resolved axes while the syntactic-role axis stays open with a declared evidence-to-resolve clause (more context). A fluent
gloss does not validate a source-linked parse: the gloss is evidence on the semantic axis whose scope does not intersect the morphological claim.

### 11.3 Clinical case (abstract only)

A patient presentation is an orthemma whose factorized profile includes a symptom axis, a risk/urgency axis, a cause axis, and a severity axis. The symptom-axis placement can
become route-sufficient — altering urgency and routing — while the cause axis stays open as an explicitly maintained candidate family with a discriminating test declared. Shared
symptoms do not establish shared etiology (an evidence-grade configuration), and orthemic accuracy is not clinical or ethical goodness: a system can place correctly and route
unjustly. The example is retained in this abstract form only; no clinical detail is load-bearing anywhere in the paper.

### 11.4 Case study: the launch pipeline

> **Case study — single-project longitudinal record; corroborating, not validating.**
>
> One software launch pipeline (internally, "Branch 11") was tracked longitudinally across roughly fifty governed stops in a single, maximally disciplined, lean-vocabulary
> engineering operation. The record is transcript-verified, single-owner, and single-project; it is reported here as one occurrence chain exhibiting the paper's distinctions, and
> it carries no cross-domain weight.
>
> **Identity.** A storage slot was reused and the new occupant treated as the same file (identity key confused with location); elsewhere an ordinal position was mistaken for an
> identity key. Both are `C^id` failures — identity uncertainty misfiled as confidence about the wrong object. **Admission.** A case was admitted for handling on the basis of a
> stale checkout: evidence valid for `(κ, v)` was applied to `(κ, v′)` — a lineage-transport violation, not a wrong judgment. **Authority-binding.** An authorization was present
> but not bound to the parameters actually used: the warrant's scope did not cover the executed action — a warrant-gate failure that no evidence channel could have expressed,
> because authorization is not evidence. **Settlement.** A validator returned green while its scope did not intersect the claim being settled (hash-valid read as semantically
> valid): a mis-scoped pass, detected only because scopes were by then explicit. **Closure.** A terminal state was declared while residuals remained owner-gated: the completion
> claim collapsed owner-assigned burdens into "resolved" — the false-closure type error, caught by the per-burden ledger. **Revision.** After repeated single-neighbor patches
> failed to converge, revision escalated to the enumeration mode of Section 7.6 — the second-order variant observed once, in this record.
>
> The operation *built* this machinery in response to these failures; it did not have it in advance. That is the sense in which the record corroborates the claim that the
> six-framework union is not assembled by default — and the full extent of what one case can show.

### 11.5 The stale steer (recovered directive without current force)

A system recovers an earlier governing instruction — after context compaction, a crash, or a handover — and follows it. The recovery is textually faithful, the instruction was genuinely issued under proper authority, and it had been superseded in the interim. Five claims must be kept apart: that the directive *exists*, that this copy is *authentic*, that it was *recovered* through a declared channel, that its issuer was *authorized*, and that it is *in force* now — and evidence for any one is not evidence for the next. The verdict layer needs no new machinery: currentness of the governing evidence fails (V2c), the bound governing token is not current (V3c), the executor is faithful (V3d passes — faithful execution under a defective governing token), and a closure claim of "acted under current instructions" fails V5. The full directive record, the five predicates, and the deterministic fixture (F6) are given in `examples/compaction-stale-steer.md` (Decision 0006).

---

## 12. Related Work

Established constructs largely theorise the type side, and each facet of the present architecture has a nearest neighbor, conceded here facet by facet:

| Facet of this paper | Nearest established neighbor |
|---|---|
| Plural, hierarchical profiles | multi-label and hierarchical classification (Tsoumakas & Katakis 2007; Silla & Freitas 2011) |
| Maintained candidate structure | POMDP belief states (Kaelbling, Littman & Cassandra 1998); predictive-state representations (Littman, Sutton & Singh 2001) |
| Abstention, escalation, quarantine | reject-option classification (Chow 1970); selective prediction (El-Yaniv & Wiener 2010; Geifman & El-Yaniv 2017); open-set recognition (Scheirer et al. 2013); OOD detection (Hendrycks & Gimpel 2017) |
| Deciding when to stop investigating | value-of-information (Howard 1966) and sequential/optimal stopping (Wald 1947) |
| Residual obligations with owners | risk registers and risk-management guidelines (ISO 31000:2018); hazard logs |
| Placement statuses and transitions | ticket/workflow state machines (commodity practice; no single citable origin is load-bearing here) |
| Lineage, versions, audit records | W3C PROV-DM (Moreau & Missier 2013); audit trails; ML lineage systems |
| Correct result through defective process | process reliabilism, for beliefs (Goldman 1979; the structure of Gettier 1963) |
| Perturbation probes for weak rules | metamorphic testing (Chen, Cheung & Yiu 1998; Chen et al. 2018) |
| Rule adequacy vs outcome testing | assurance practice: tests of controls vs substantive procedures (ISA 330) |
| Type individuation and safe merger | sufficient statistics (Fisher 1922); causal states (Crutchfield & Young 1989; Shalizi & Crutchfield 2001); bisimulation and MDP state abstraction (Larsen & Skou 1991; Givan, Dean & Greig 2003); automata minimisation (Hopcroft 1971) |

The type-individuation mathematics is inherited outright. The claimed residual is exactly three things. (1) **The union:** no listed framework supplies the others, and the
observational record shows a disciplined practice assembling the union piecewise at real cost rather than possessing it by default. (2) **The lifecycle:** the explicit,
single-object connection of disclosure, evidence typing, representation, routing, validation, per-burden closure, and governed revision to the placement status of a concrete
occurrence and its successors. (3) **The joint verdict layer:** process reliabilism names truth-connection for beliefs but has no operational record; provenance systems have
operational records but no verdict layer; assurance and metamorphic testing each hold one verdict without the joint object. The orthing episode is the one object on which result
correctness, evidential support, truth-connection, currentness, rule adequacy, policy adequacy, executor fidelity, ex-ante justification, route safety, closure truthfulness, and
robustness are simultaneously definable — and that integration, not any component, is what remains after the concessions. Whether the integration pays for itself is Section 13's
question, not this section's claim.

---

## 13. Empirical Program

Three evaluations, kept strictly separate. **Nothing in this paper is experimentally validated.** The current evidence is analytic (the formal coherence of Sections 2–10) plus
observational (a 33-case cross-project casebook and the single longitudinal case of Section 11.4). The programs below are designed; none has run.

### 13.1 Headline: the preregistered false-closure / selective-prediction benchmark

Environments with planted inter-orthemma aliasing, planted identity uncertainty, and validator-scope traps. **Treatment:** an agent maintaining typed candidate families and
per-burden closure (the machinery of Sections 5 and 7). **Baseline:** argmax placement with a confidence threshold. **Primary endpoints:** false-closure rate; the area under the risk–coverage curve (AURC) of the selective-prediction literature. (The metric name is corrected from an earlier draft's "risk–coverage AUROC", which named no established metric. Methodological criticisms of AURC — its dependence on the evaluation set's coverage grid and its incomparability across error rates — will be weighed when the benchmark is finalized, and any change of endpoint must happen before, never after, the protocol freeze.)
Fixtures are laptop-scale and cheap; the benchmark targets the claimed residual directly (does the union behave differently from the composite?), not the vocabulary.

**Decision rule — three outcomes, preregistered:**

- **adopt** the treatment's machinery claims on an adequately powered win at the preregistered effect size;
- **not supported yet** on insufficient or underpowered evidence — including every underpowered null and every ordinary nonsignificant tie;
- **retire** the behavioural claim **only** on adequately powered equivalence or demonstrated harm.

An underpowered miss is never read as refutation; an unpowered tie is never read as adoption. This supersedes the prior draft's bare "no improvement over established labels"
failure criterion, which conflated the second and third outcomes.

### 13.2 The product fixture suite (separate product test)

A fixture suite of the E1–E5 class exercises the product behaviour of an implementation: baseline-versus-treatment runs with pinned versions and run hygiene, culminating in **E5**,
the metamorphic pathway fixture — a weak rule (pass iff the output contains a marker string) that returns the correct current result, paired with neighboring perturbations
(correct-without-marker; incorrect-with-marker), scored to separate current-answer correctness from pathway adequacy. E5 carries no theory vocabulary and is the operational test of
episode reification's practical delta over "audit the validator when suspicious" (Section 8.6). It is a product test; success or failure here transfers no verdict to the benchmark
of 13.1 or the terminology test of 13.3.

### 13.3 The terminology benchmark (explicitly secondary)

The three-arm benchmark of the terminology evaluation spec: **Arm A** (ordinary language), **Arm B** (the operational distinctions expressed without neologisms), **Arm C** (the
coordinated coined vocabulary with a matched primer), counterbalanced, exposure-matched, with construct-specific co-primary endpoints (false-closure detection; pathway-defect
detection), preregistered minimum important effects, noninferiority and harm margins, and per-term three-outcome decision rules. This benchmark is **secondary and cannot be rescued
by 13.1**: a machinery win in the headline benchmark is an Arm-B-versus-Arm-A result about *distinctions* and transfers nothing to the *words*; only Arm C versus Arm B adjudicates
the vocabulary. The converse holds too: a vocabulary win would not validate the machinery.

### 13.4 Evidence status, stated plainly

Analytic: the definitions and separations of Sections 2–10 cohere and the six additions close gaps the prior text named only in words. Observational: the failure patterns the
machinery addresses are real and recurrent — the casebook's cross-project cases for stale evidence and lineage, validator scope, closure trichotomy, plural profiles, and
failure-origin confusion; the single longitudinal case for the assembled union. Experimental: none. No stronger claim is made anywhere in this paper, and any sentence read as
making one should be corrected against this section.

---

## 14. Terminology Status

Every coined term in this paper — **orthemma, ortheme, metaortheme, orthing,** and the companion-paper candidate **orthable** — is a **candidate** pending the matched benchmark of
Section 13.3. None is adopted; none is retired. The paper's own governing principle applies:

**Design Principle 1 (Terminological utility, retained).** The vocabulary is warranted only if, under matched training time, attention, and access to evidence, it improves at least
one preregistered outcome — placement accuracy, inter-rater agreement, defect discovery, repair traceability, transfer, calibration, or false-closure prevention — without
unacceptable over-segmentation or governance cost, relative to established terminology. Adjudication follows the three-outcome rule: adopt on an adequately powered win; do not
adopt yet on insufficient evidence; retire only on adequately powered equivalence or harm.

Two facts are recorded without tension. First: **every distinction in this paper is fully expressible in ordinary words** — occurrence and version, state-type, governing rule and
the distinction it consults, handling episode and pathway verdict. The reader who strikes every coinage loses no content. Second: **paraphrasability does not settle the question**
— an earlier claim that expressive redundancy of the words was "established analytically" conflated paraphrasability with redundancy and is retracted. "Gettier case" is the
standing existence proof that a fully paraphrasable coined term can earn permanent keep through compression and coordination. Whether these terms do is exactly what the benchmark
measures, and no argument in this paper substitutes for it. The distinctions have observational support; the vocabulary has no matched comparative evidence in either direction.

---

## 15. Limitations and Honest-Evidence Appendix

### 15.1 Limitations

The decision-theoretic core is inherited, and the terminology may add load rather than value. Task specifications can be incomplete, contested, or imposed; exact equivalence is
rarely estimable; approximate equivalence need not be transitive; local irreducibility depends on representation and merger families; system boundaries can be chosen
opportunistically. Cross-domain analogies establish no shared mechanism. The formalism is conditional on objectives, losses, constraints, authority, and affected-party weights and
cannot derive their legitimacy: a system can place every task-relevant ortheme correctly and still serve harmful ends — orthemic adequacy is not ethical goodness, and governance
must permit contestation of the task, the loss, the authority, and the category itself. Orthemic debt is demoted to a speculative instrument (Section 7.3); the metaphysical and
theological extensions are split to a companion paper and no result here depends on them. Metaorthemes remain higher-order control; the episode-verdict layer's practical delta is
untested (fixture E5); and no study yet demonstrates incremental utility of anything in this paper.

### 15.2 Evidence tiers

| Tier | Content | Status |
|---|---|---|
| **Analytic** | Formal coherence of the six additions; the split metaortheme normal form; verdict separability; the DAG/composition conditions; the derived multi-actor extensions | Consistency shown by construction (deterministic fixtures); establishes no empirical claim |
| **Observational, cross-project** | Stale-evidence/lineage failures; validator-scope failures; closure trichotomy; plural profiles; failure-origin confusion (≥2 domains each, with negative controls) | Real and recurrent; base rates unknown |
| **Observational, single-longitudinal** | The assembled-union claim; enumeration-mode revision; authority-binding | **One case (Branch 11).** Single-project, single-owner, transcript-verified record. Corroborating, not validating; carries no cross-domain weight |
| **Experimental** | Machinery benefit (13.1); episode-reification delta (13.2); vocabulary utility (13.3) | **None.** All three designed, none run |

Three honesty notes close the paper. *Branch 11 is one case:* fifty governed stops inside one tightly-coupled project are one case, not fifty domains, and every sentence that leans
on it says so. *Base rates are unknown:* the casebook establishes existence and recurrence of the failure patterns, not their frequency in any population of projects; nothing here
estimates how often the machinery would matter. *The record is single-owner:* the longitudinal record was produced and curated within one operation by one owner, and independent
replication of even the observational tier does not yet exist.

---

## 16. Conclusion

This paper proposed the orthemma–ortheme system as an integration discipline for the token side of classification and handling work. Its center of gravity is one relation — a concrete occurrence instantiating repeatable operational state-types relative to a declared, versioned analysis — and one further object built on that relation: the orthing episode, an auditable record on which result correctness and pathway adequacy are separately adjudicable. Around these, six formal additions close gaps the prior text could only gesture at: versioned identity with labeled lineage makes "right finding, wrong copy" a statable error; analysis/actor/time indexing makes ground truth explicit and disagreement diagnosable; typed, scoped, expiring evidence makes the green-but-mis-scoped validator visible; factorized candidates with route composition make partial action well-formed; per-burden closure makes false closure a checkable record defect; and episode reification with the registry-normalized verdict vector makes the stopped clock, the justified rare miss, the defective binding, and the stale directive all first-class, machine-checkable cases (fixtures F1–F7).

What the paper deliberately does not claim is as much a result as what it claims. Every facet has a conceded neighbor; the type-individuation mathematics is inherited; the internal records that motivated the design are not independently auditable and validate nothing; the coined vocabulary is fully paraphrasable and strictly benchmark-gated; and the three designed studies — the false-closure benchmark, the episode-reification fixture suite, and the terminology comparison — have not been run. The framework's standing is therefore: analytically coherent (deterministically checked), operationally motivated, empirically unvalidated. The next honest step is not more theory but the execution of Section 13 as preregistered — and the framework has been built so that a negative result would be recordable, on its own terms, as exactly what it is.

## 17. Data and Materials Availability

All public materials of this project — the formal core, this manuscript, the multi-actor note, machine-readable schemas and worked examples, deterministic fixtures and validators, the verdict and notation registries, decision records, and the designed (unrun) terminology-evaluation packets — are available in the public repository (`theislampill/orthemology` on GitHub), with a SHA-256 release manifest under `docs/provenance/`. **Not available:** the internal casebook and the internal longitudinal engineering record referenced as design motivation (Sections 1.4, 11.4, 13.4). They contain private working material, are not rights-cleared for publication, and are therefore not independently auditable; no quantitative claim in this paper rests on them, and they are cited only as motivation. No human-subject data exists; no experiment has been conducted.

## References

- Chen, T. Y., Cheung, S. C., & Yiu, S. M. (1998). *Metamorphic testing: a new approach for generating next test cases.* Technical Report HKUST-CS98-01, Department of Computer Science, HKUST.
- Chen, T. Y., Kuo, F.-C., Liu, H., Poon, P.-L., Towey, D., Tse, T. H., & Zhou, Z. Q. (2018). Metamorphic testing: a review of challenges and opportunities. *ACM Computing Surveys*, 51(1), 4:1–4:27. doi:10.1145/3143561
- Chow, C. K. (1970). On optimum recognition error and reject tradeoff. *IEEE Transactions on Information Theory*, 16(1), 41–46. doi:10.1109/TIT.1970.1054406
- Crutchfield, J. P., & Young, K. (1989). Inferring statistical complexity. *Physical Review Letters*, 63(2), 105–108. doi:10.1103/PhysRevLett.63.105
- El-Yaniv, R., & Wiener, Y. (2010). On the foundations of noise-free selective classification. *Journal of Machine Learning Research*, 11, 1605–1641.
- Fisher, R. A. (1922). On the mathematical foundations of theoretical statistics. *Philosophical Transactions of the Royal Society A*, 222, 309–368. doi:10.1098/rsta.1922.0009
- Geifman, Y., & El-Yaniv, R. (2017). Selective classification for deep neural networks. *NeurIPS 30*.
- Geifman, Y., Uziel, G., & El-Yaniv, R. (2019). Bias-reduced uncertainty estimation for deep neural classifiers. *ICLR*. (Derivation of AURC/E-AURC.)
- Gettier, E. L. (1963). Is justified true belief knowledge? *Analysis*, 23(6), 121–123. doi:10.1093/analys/23.6.121
- Givan, R., Dean, T., & Greig, M. (2003). Equivalence notions and model minimization in Markov decision processes. *Artificial Intelligence*, 147(1–2), 163–223. doi:10.1016/S0004-3702(02)00376-4
- Goldman, A. I. (1979). What is justified belief? In G. S. Pappas (Ed.), *Justification and Knowledge* (pp. 1–23). D. Reidel. doi:10.1007/978-94-009-9493-5_1
- Hendrycks, D., & Gimpel, K. (2017). A baseline for detecting misclassified and out-of-distribution examples in neural networks. *ICLR*.
- Hopcroft, J. (1971). An n log n algorithm for minimizing states in a finite automaton. In *Theory of Machines and Computations* (pp. 189–196). Academic Press.
- Howard, R. A. (1966). Information value theory. *IEEE Transactions on Systems Science and Cybernetics*, 2(1), 22–26. doi:10.1109/TSSC.1966.300074
- International Auditing and Assurance Standards Board (2009). *ISA 330: The Auditor's Responses to Assessed Risks.* IFAC.
- International Organization for Standardization (2018). *ISO 31000:2018 Risk management — Guidelines.*
- Kaelbling, L. P., Littman, M. L., & Cassandra, A. R. (1998). Planning and acting in partially observable stochastic domains. *Artificial Intelligence*, 101(1–2), 99–134. doi:10.1016/S0004-3702(98)00023-X
- Larsen, K. G., & Skou, A. (1991). Bisimulation through probabilistic testing. *Information and Computation*, 94(1), 1–28. doi:10.1016/0890-5401(91)90030-6
- Littman, M. L., Sutton, R. S., & Singh, S. (2001). Predictive representations of state. *NIPS 14*.
- Moreau, L., & Missier, P. (Eds.) (2013). *PROV-DM: The PROV Data Model.* W3C Recommendation, 30 April 2013. https://www.w3.org/TR/prov-dm/
- Scheirer, W. J., Rocha, A., Sapkota, A., & Boult, T. E. (2013). Toward open set recognition. *IEEE TPAMI*, 35(7), 1757–1772. doi:10.1109/TPAMI.2012.256
- Shalizi, C. R., & Crutchfield, J. P. (2001). Computational mechanics: pattern and prediction, structure and simplicity. *Journal of Statistical Physics*, 104, 817–879. doi:10.1023/A:1010388907793
- Silla, C. N., & Freitas, A. A. (2011). A survey of hierarchical classification across different application domains. *Data Mining and Knowledge Discovery*, 22, 31–72. doi:10.1007/s10618-010-0175-9
- Traub, J., Bungert, T. J., Lüth, C. T., Baumgartner, M., Maier-Hein, K. H., Maier-Hein, L., & Jaeger, P. F. (2024). Overcoming common flaws in the evaluation of selective classification systems. *NeurIPS 37*. arXiv:2407.01032
- Tsoumakas, G., & Katakis, I. (2007). Multi-label classification: an overview. *International Journal of Data Warehousing and Mining*, 3(3), 1–13. doi:10.4018/jdwm.2007070101
- Wald, A. (1947). *Sequential Analysis.* John Wiley & Sons.
- Wetzel, L. (2018). Types and Tokens. In E. N. Zalta (Ed.), *The Stanford Encyclopedia of Philosophy.* https://plato.stanford.edu/entries/types-tokens/

Machine-readable database with per-claim verification status: `references/orthemology.bib` and `docs/sourcing/SOURCING-LEDGER.md`.

---

## Glossary of Proposed Terms (all candidates; none adopted)

- **Orthemma.** A concrete situated occurrence considered as something to be apprehended, carrying an identity key and version. The token pole.
- **Ortheme.** A repeatable operational state-type an orthemma instantiates, relative to a declared task. The type pole.
- **Instantiation relation `Inst_A`.** `(m, o) ∈ Inst_A`: `m` instantiates `o` under the declared, versionable analysis `A` (with `T = task(A)`); the fibre `O*(m; A)` is the actual profile. `Inst_T` / `O*_T(m)` are licensed local shorthand once a single `A` with `task(A) = T` has been fixed; forbidden in multi-analysis contexts (Definition 3).
- **Typed candidate families `C^id, C^profile, C^cause, C^route, C^warrant`.** Open alternatives per uncertainty axis, with exclusivity marking and an evidence-to-resolve clause.
- **Placement / apprehension.** Assigning an inferred profile / the whole encounter-to-disposition process.
- **Route-sufficient apprehension.** Enough of the profile to route safely while other axes stay open; ≠ identity-complete resolution.
- **Labeled successor set `Succ_a(m)`.** The zero, one, or many occurrences an action creates; placement validity does not transport across an edge without re-evidence.
- **Metaorthemma (candidate term; object adopted by Decision 0002).** The episode-local, case-bound configuration TOKEN of a metaortheme: `MetaInst(μ̄, μ)`; binds case-specific values (reference frame, tolerance value, instrument + calibration, fixture, success surface, scope) within the declared analysis (`Compatible(μ̄, A(e))`); its binder-with-warrant is distinct from the executor; judged by V3c; omitted where no material binding exists. The WORD remains a benchmark-gated candidate (ordinary-language equivalent: "instantiated governing-configuration token"); the OBJECT is part of the episode record.
- **Metaortheme.** A metaorthemic configuration `⟨g, S_μ, select_μ, prov(μ), ver(μ)⟩` paired with a separable meta-policy; governed component in {repertoire, individuation, evidence,
  disclosure, routing, validation, warrant-classification}; objectives, the task, and the governance meta-level excluded.
- **Residual disposition.** Per burden: unresolved / deferred / transferred / owner-assigned / risk-accepted / validated-resolved.
- **False closure.** A completion claim collapsing other dispositions into "validated-resolved"; a type error against the burden ledger.
- **Orthing / orthing episode.** The process type of rule-governed, evidence-updating apprehension-and-handling / one dated, situated, record-valued run of it, bearing the verdict
  vector.
- **Verdict vector (V1–V6, registry-normalized).** Result: V1 correctness, V2b-T factive truth linkage. Pathway core: V2a support; V2b-P procedure reliability; V2c currentness; V3a configuration, V3b policy, V3c token-binding, V3d execution, V3e decision-time adequacy; V4a route safety; V5 closure truthfulness; V6 robustness. Advisory: V4b route quality. Semantic IDs and aliases: `docs/verdict-registry.yaml` (Decision 0004).
- **Generalized ANDON event.** A governed interruption when continuation or closure is not warranted under the current placement, evidence, route, warrant, or ledger.
- **Target profile `𝒢_{α,A_α}`.** The state-types an actor aims to make some successor occurrence instantiate, under the actor's own analysis `A_α`; distinct from the descriptive profile, from the objective, and from any
  metaortheme.

*End of revised draft. Prior version: the original manuscript (see `docs/provenance/document-history.md`). Companion formal text: `theory/orthemic-core-formalization.md`. Terminology evaluation protocol: `terminology/`.*
