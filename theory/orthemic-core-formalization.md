# Orthemic Core Formalization — Orthing, Episodes, Metaorthemes, Pathway Adequacy

> **Provenance.** Multi-model draft lineage with successive review passes;
> the original headers are preserved verbatim in
> [`docs/provenance/document-history.md`](../docs/provenance/document-history.md),
> and model contributions in
> [`docs/provenance/model-contributions.md`](../docs/provenance/model-contributions.md).
> Nothing here is experimentally validated.

**Status (revision R6, 2026-07-20; fresh-session repository review completed; not external human peer review; not empirically validated):** canonical formalization of the
orthing layer (episodes, metaorthemes, metaorthemmata, pathway adequacy),
companion to the main manuscript's definitions. All claims are
definitional/analytic unless marked empirical; nothing is experimentally
validated — the deterministic fixture suite checks consistency only, and
the Arm A/B/C terminology benchmark is designed but not run.

**Inherited notation** (normative registry:
[`docs/notation-registry.yaml`](../docs/notation-registry.yaml)). `𝓜`,
`𝓞` = the universal occurrence and ortheme universes; a declared analysis
`A` activates a domain `M_A ⊆ 𝓜` of orthemmata (concrete occurrences) and
a repertoire `O_A ⊆ 𝓞` of orthemes (repeatable operational state-types);
under the standing single-analysis scope these are written `M`, `O`.
`Inst_A ⊆ M_A × O_A` = analysis-relative instantiation — the primitive;
the manuscript's Definition 3 and §2.6 define the declared, versionable
analysis `A`, whose components include the task `T = task(A)`;
`O*(m; A)` = actual profile (ground truth relative to `A`);
`Π_A` = the complete-profile space and `Π_A^∂` the partial-profile space
(manuscript Definition 10); `p̂_t(m) ∈ Π_A^∂` = inferred profile (belief;
`Ô` survives only as the derived flattening of `p̂`, §2.2);
`Ĉ_t(m)` = candidate set of complete profiles; `Ω` = observation
map; `μ` = a metaortheme; `o-hat` = an inferred ortheme.
**Abbreviation convention:** once a single analysis `A` with
`task(A) = T` is fixed by explicit declaration, task-subscripted forms
(`Inst_T`, `O*_T(m)`, `Π_T`, `𝒦_T`, `ℛ_T`, `𝒲_T`) and the unsubscripted
`M`, `O` abbreviate their `A`-indexed counterparts. The shorthand is
**forbidden** wherever more than one analysis is live — level-indexed
audits (§1, §5.2), multi-actor episodes (§5.3), cross-version comparisons,
execution-vs-review comparisons — where the full `O*(m; A)` form is
required. (This block supersedes the earlier statement that treated the
task-indexed relation as primitive; the retired symbols are listed in the
notation registry's `retired_symbols`.)

---

## 1. Type/token resolution (2A)

**Orthing** (gloss: the doing of apprehension-and-handling) is a process
TYPE: the rule-governed, evidence-updating operation kind by which an
orthemma is individuated, observed, assigned a candidate and then inferred
profile of orthemes, routed, validated, dispositioned, and revised under
governing metaorthemes. It stands to its runs as "compilation" stands to
"the 14:32 build of commit `abc123`." **An orthing episode** `e` (gloss:
one dated, situated run of that operation) is a concrete TOKEN: it has an
actor, a time, an input occurrence, and a result, and two episodes are
distinct occurrences even when inputs and outputs agree.

**Level-indexing.** Let `M^(0)` be the base domain of orthemmata and
`E^(0)` the class of episodes placing members of `M^(0)`. When a higher
audit asks "was this placement made correctly, on adequate evidence, under
an adequate rule?", the episode is itself apprehended. This is an explicit
**reification embedding**, not literal set inclusion — an episode is a
different kind of thing from a jar of powder, and becomes a base occurrence
of the higher audit only by being cast as one: for each level `n`,

    ι_n : E^(n) ↪ M^(n+1)   (injective; ι_n(e) is "the episode e, considered
                             as a case to be audited")

(gloss: yesterday's classification act, re-cast as today's case). Writing
`⊇` here would falsely assert episodes are already members of the base
domain; the embedding records that a modeling step turns one into the
other. The audit's
orthemes at level `n+1` are pathway state-types — *evidence-sufficient
placement*, *stale-rule placement*, *false closure* — precisely the §4
verdicts. This applies the manuscript's own licensed move ("metaorthemes
can become first-order orthemes for a higher audit," §6) to the token
side; the regress stops, as there, at a declared governance boundary.

**Why no separate "meta-orthemma" term.** The originating project notes float the noun
"meta-orthemma" for the concrete operation. It is not adopted. Against the
manuscript's own anti-vacuity standard, a new noun class must change at
least one of representation, evidence, routing, or prediction; it changes
none. *Representation:* the embedding `ι_n : E^(n) ↪ M^(n+1)` already types
the reified episode as an orthemma of the higher domain. *Evidence:* what
audits an episode is its signature record (§2) — a property of the domain,
not of a new noun. *Routing:* audits route episodes through the same
lifecycle as any orthemma. *Prediction:* nothing sayable with
"meta-orthemma" is unsayable with "the reified episode `ι_n(e) ∈ M^(n+1)`."

**The one honest counterargument, and its answer.** Episodes are unusual
orthemmata: unlike a jar of powder, an episode carries a canonical,
system-authored observation of itself — its trace. One might argue this
structural difference deserves a name. Answer: the difference is real but
is a *subtype constraint on the domain* (episodes are orthemmata equipped
with signatures), not a new pole of the type–token architecture. Register
the subtype; do not coin the noun. If audits over episodes later prove to
need operations generic placement lacks, revisit under the same test.

**Qualification (Decision 0002).** The rejection above
concerns "meta-orthemma" as a name for the REIFIED EPISODE. Decision 0002 later adopted a different object in the same name-neighborhood: the
**metaorthemma** `μ̄` — an episode-local, case-bound CONFIGURATION TOKEN
of a repeatable metaortheme (§2.2, §3, V3c in §4.1). It is not the whole
episode and not the execution event; the rejection above stands for its
original referent and does not adjudicate the token object (its revisit
clause was exercised). The WORD "metaorthemma" remains a benchmark-gated
candidate term; the OBJECT is adopted.

---

## 2. Episode signature (2B)

### 2.1 Candidate formulations compared

**Candidate F (function style).** `e_μ(m) = o-hat`: an episode governed by
metaortheme `μ` maps orthemma `m` to one ortheme; correct when
`o-hat = o*`. Virtues: minimal, mnemonic, correctness in one equation.
Defects, each fatal for the paper's own commitments: (i) singleton output
contradicts plural profiles (Def. 3) and route-sufficient apprehension
(Def. 7); (ii) the episode is identified with its output — the function's
*value* — leaving no object to audit when the answer is right but the
pathway defective; (iii) evidence, actor, time, route, residuals, and the
successor occurrence have no slot; (iv) `μ` is one subscript, but real
episodes run under several governing rules at once (§3.4).

**Candidate R (record/state-producing style).** The episode is a
structured record — an element of a typed domain `E` — with named
components and projections; "output" is a designated sub-record. Virtues:
audit-ready, plural by construction, separates run from result. Cost:
heavier notation; needs a convention for the common quick case.

**Resolution:** adopt R as the definition; retain F as *derived* notation
for one placement inside an episode (2.3).

### 2.2 Recommended signature (formal)

An **orthing episode** is a record

$$e = \langle\, \mathrm{id};\ m, \kappa, v;\ x, H;\ \alpha, w, A, T, t;\ \vec{\mu}, \mathrm{MetaTok}, \pi;\ \vec{C}, \hat{p};\ r;\ \mathrm{estatus};\ \mathcal{Q};\ \delta;\ \mathrm{hand}_{\mathrm{in}}, \mathrm{hand}_{\mathrm{out}};\ a, \mathrm{Succ} \,\rangle$$

with components (each glossed in ordinary language):

| Component | Type | Gloss |
|---|---|---|
| `id` | episode identifier | which run this is (referenced by handoffs and audits) |
| `m` | `M` | the input orthemma — the concrete case handled |
| `κ = id(m)` | identity key | which thing this is (survives change) |
| `v = ver(m)` | version | which state/edition of that thing |
| `x = Ω_e(m)` | observation | what the episode actually saw |
| `H` | ordered typed evidence sequence | the evidence gathered in order, each item with property class, scope, provenance, and validity/expiry |
| `α` | actor | who/what executed (human, validator, model, pipeline, institution — populated even for mechanical executors) |
| `w` | episode warrant | who/what authorized acting, with scope (the #12 hook); distinct from evidence and from executor identity |
| `A` | declared analysis (identifier + version) | the analysis the placement is relative to (manuscript §2.6); result correctness (V1) is judged against `O*(m; A)`; within the episode's scope the task-subscripted spaces below abbreviate their `A`-indexed forms |
| `T = task(A)` | task | the task component of `A`, retained as a separate readable component |
| `t` | time interval | when the episode ran |
| $\vec{\mu} = (\mu_1, \dots, \mu_k; \preceq)$ | metaorthemic configuration | the governing rules in force, with precedence order `≼` |
| `MetaTok(e) = {μ̄_1,…,μ̄_j}` | concrete metaorthemmata (Decision 0002) | the case-bound CONFIGURATION TOKENS of governing types actually applied. Each `μ̄` records/references: its own identity and lineage; `(μ, ver(μ))` via the internal typing `MetaInst(μ̄, μ)`; `(A(e), ver(A(e)))` with `Compatible(μ̄, A(e))` — the token binds case-specific values WITHIN the declared analysis, references any value `A` fixes uniquely, and never overrides `A` without an explicit new analysis version; the target `(κ, v)`; governed component `g`; the case-specific binding map `B` (reference frame, tolerance value, fixture, success surface, …); scope `σ` incl. the claims in `𝒬` that depend on it; references to policy, evidence selector, instrument/tool and calibration provenance; the **binder** (actor/process that made the binding) with binding warrant `w_bind`, kept DISTINCT from the designated executor; binding time `t_bind`; validity/expiry/supersession. The token REFERENCES the episode's evidence `H`, trace, and output — it never absorbs them (the application-event view `ApplyEvent(μ̄, e) = ⟨μ̄, Trace_e\|_μ̄⟩` is derived, not primitive). **Zero-burden rule:** a configuration with no material case-specific binding, non-default scope, instrument/calibration, or independent validity condition gets no explicit token, and `V3c ∉ ReqPath(e)` (status recorded not-applicable, with reason) |
| `π` | policy | the concrete procedure executed under $\vec{\mu}$ |
| $\vec{C}$ | typed candidate families | open alternatives per uncertainty axis: `C^id ⊆ M` (which occurrence), `C^profile ⊆ Π_A` (which profile), `C^cause ⊆ 𝒦_A` (which cause), `C^route ⊆ ℛ_A` (which route), `C^warrant ⊆ 𝒲_A` (which warrant state) — competing hypotheses may themselves be PROFILES, so candidates are not forced into single orthemes |
| `p̂ ∈ Π_A^∂` | inferred placement | **exactly one partial profile** — the profile actually placed, determined on resolved axes and open on the rest; **never a set of complete profiles** (live alternatives belong in `Ĉ ⊆ Π_A`, and optional weights in the separate belief layer) and **never coerced to a singleton ortheme**; `Ô ⊆ O` survives only as the derived flattening of `p̂`. (R4 repair, Decision 0012: the pre-R4 gloss "or a bounded set of profiles if unresolved" typed one symbol into two spaces and is withdrawn; archived patches retain it as history.) |
| `r` | route | the operation/owner the case was sent to |
| `estatus` | evidence status map | per placed claim: validated / provisional / stale / absent |
| `𝒬` | claim ledger | per claim: proposition; target occurrence/version; property class (#3); required success surface (#14); evidence IDs; warrant where relevant; verification status; explicit non-claims |
| `δ` | residual disposition map | per obligation: unresolved / deferred / transferred / owner-assigned / risk-accepted / validated-resolved (issue #6's six values). Claims (`𝒬`) are assertions; residuals (`δ`) are obligations — never merged |
| `hand_in, hand_out` | handoff records | incoming/outgoing packets: packet id+version, sender/receiver episode ids, subject identity, state claims, evidence references, authority claims (the #15 hook) |
| `a` | action | what was done to or with the case |
| `Succ ⊆ M` | successor set | the occurrences the action created/affected, as LABELED lineage edges (which action produced which successor) — zero, one, or many; the earlier forced single `m′ = succ(m,a)` is corrected |

`Π_A` — with `Π_T` its licensed shorthand under the standing convention —
is the **profile space** of manuscript Definition 10, R3 general form:
`Π_A ⊆ 𝒫(O_A)`, the set of admissible complete profiles under the
constraints declared by `A`. Factorized axes are one *permitted
representation family*, not a universal ontology: where declared, a
complete profile selects exactly one admissible value per **applicable**
alternatives-marked axis, records an explicit `not-applicable` value on
an objectively inapplicable axis (a fact about the case, never
uncertainty), and contains any declared-admissible — possibly empty —
subset per co-holding axis, consistent with the declared cross-axis
constraints. Objective absence, objective inapplicability, epistemic
openness, evidence absence, and candidate plurality are five distinct
states; only the first two live in profiles. `Π_A^∂` is the
partial-profile space (resolutions may be left undetermined), with
`Π_A ⊆ Π_A^∂` (gloss: every complete way the case could be placed, and
every honest partial state of knowledge about it). This and the labeled
successor edges close the arrow the manuscript lacks from action back
into `M`: placements verified for `(κ, v)` do not transport to `(κ, v′)`
without a lineage argument.

**Plain-language key for governed-component letters used below:** `O` =
the ortheme repertoire (which state-types exist); `I` =
individuation/identity (what counts as the same case, versioning); `E` =
evidence procedure (what evidence counts, at what grade); `D` =
disclosure/uncertainty handling (what may be left open and how it is
declared); `R` = routing (where cases are sent); `V` =
validation/closure (what may be called done, at what standard); `W` =
warrant/authorization-state classification (which warrant states exist —
authorized vs factually established — and what each licenses).

### 2.2a Endpoint plus bounded trace

The record above is the REQUIRED endpoint. Because orthing is defined as
evidence-updating, an endpoint alone cannot always adjudicate pathway
verdicts; where those verdicts (V2b-P truth-conduciveness, V3d executor
fidelity, V6 robustness — §4) must be adjudicated from the episode's own
record, an ordered **trace** is also required:

    Trace_e = (s_0, u_1, s_1, …, u_k, s_k)

where each state `s_i` snapshots the current evidence, candidate families,
inferred placement, route, and open residuals, and each update `u_i`
records an evidence acquisition, selection, routing, action, or revision
step (with the rule edition `ver(μ)` in force). **Governance declares the
trace granularity**; trivial cases carry no trace, and maximal per-event
logging is never a blanket requirement.

**Partial applicability.** Not every episode has a route, a mutation, a
closure claim, or open residuals. Components are defined **where
applicable**: a read-only classification episode has `a = ⊥` (no action),
`Succ = ∅` (no successor created), possibly `r = ⊥` (no downstream route),
and an empty `δ`. Where a component is `⊥`, the verdicts that quantify
over it (V4a route, V5 closure — §4) are **not asserted of that episode**
rather than counted as failures; formally, pathway adequacy conjoins over
the governance-DERIVED required set `ReqPath(e)` (§4.1, Decision 0003) —
applicability is derived from the declared analysis, episode shape, risk
class, claims, and governance, never a discretionary post-hoc list, and
every verdict excluded from `ReqPath(e)` carries a recorded
`not-applicable` reason on the episode record. So "no route" (deliberately
none, with reason) is distinguished from "route omitted" (a defect), and
"not tested" is never "not applicable".

### 2.3 Three separations, stated once

1. **Episode ≠ output.** `out(e) = ⟨p̂, r, estatus, 𝒬, δ, a⟩` is a projection of
   `e`; episodes with identical outputs can differ in pathway and hence in
   every §4 verdict.
2. **Episode ≠ policy.** `π` is repeatable and undated; `e` is one dated
   execution of `π`. Reliability claims attach to `π` (and $\vec{\mu}$);
   correctness claims attach to `e`.
3. **Placement inside an episode ≠ the episode.** The compact function
   style becomes the derived judgment

$$e \models_{\mu} (m : \hat{o}) \iff \hat{o} \in \hat{O}(e) \ \text{and}\ \mu \in \vec{\mu}(e)\ \text{governed that placement}$$

   (gloss: "in episode `e`, under rule `μ`, the case was placed under
   `o-hat`"). One placement is correct iff `o-hat ∈ O*(m; A(e))`; the placed
   profile is correct at the governed level iff `p̂(e)` agrees with
   `O*(m; A(e))` restricted to that level, or the weaker route-sufficient
   variant (§4) — `A(e)` being the analysis recorded in the episode (§2.2).

---

## 3. Metaortheme semantics (2C)

**Type vs token (Decision 0002).** This section describes
the REPEATABLE side: the metaortheme type `μ` and its paired meta-policy
`π_μ`. Their concrete, case-bound instantiation inside an episode is the
**metaorthemma** `μ̄` (§2.2), typed by the internal relation
`MetaInst(μ̄, μ)` — a typing of tokens, not a second ground-truth
primitive — and subordinated to the episode's analysis by
`Compatible(μ̄, A(e))`. Four layers stay separate: type `μ`; policy
`π_μ`; token `μ̄` (binding); execution of the token (episode trace,
judged by V3d). The corresponding adequacy questions are independent:
adequate type, adequate policy, correctly bound token, faithful
execution.

### 3.1 Three models

- **(A) Higher-order STATE/TYPE.** A metaortheme is an ortheme *of the
  governing context*: the context instantiates one of several competing
  higher-order states (e.g., evidence is provenance-grade or
  appearance-grade), and that state governs.
- **(B) Higher-order handling RULE.** A metaortheme is a repeatable rule
  over the machinery: "never place on appearance alone," "quarantine on
  stale version." The rule *is* the object.
- **(C) Split model.** A metaortheme is a **metaorthemic configuration**
  `μ = ⟨g, S_μ, select_μ, prov(μ), ver(μ)⟩` — governed component `g`, declared
  competing higher-order states `S_μ`, selecting-evidence procedure `select_μ`
  that determines which state obtains, provenance, version — together
  with a distinct **meta-policy** `π_μ` prescribing conduct conditional on
  the state (gloss: the *distinction the rule consults* and the *rule that
  consults it* are two objects, as Def. 9 already insists in prose).

  **Governed-component boundary (adjudicated; one boundary for all
  documents).** `g ∈ {O, I, E, D, R, V, W}` — the mapping/handling
  components plus warrant/authorization-state classification (plain-
  language key in §2.2; `W` is required by worked example 5). Excluded as
  governed components: **objectives/loss** (the Grok exchange remains the
  standing negative example of an objective mislabeled a metaortheme);
  the **task** `T` (changing the task changes the problem — rules are
  task-*indexed*, never task-*governing*); and the **governance
  meta-level itself** (the precedence order `≼` and revision rights are
  parameters fixed at the declared governance boundary, where the regress
  terminates). The paper memo's earlier Def-9 "transformation" framing is
  reconciled as: a metaortheme *change* induces a transformation of the
  mapping subsystem — the transformation is the effect of revising `μ`,
  not `μ` itself.

### 3.2 Minimum-specificity test against the five worked examples

| Owner example | Governed | Competing states | Selecting evidence | Counterfactual difference | Policy relation |
|---|---|---|---|---|---|
| appearance-only vs provenance/discriminating evidence | `E` (evidence procedure) | {appearance-grade, provenance-grade} | source record or discriminating test | appearance-grade placements are reversible on test; provenance-grade support closure | policy chooses which test to run before placing |
| current vs stale version | identity/versioning on `M` | {current, stale} | lineage check `ver(m)` vs latest | verdicts on stale versions do not transport | policy quarantines or re-derives on stale |
| route-sufficient vs identity-complete | `R`,`V` (routing, validation) | {route-sufficient, identity-complete} | task declaration + risk class | act-now vs investigate-further diverge | policy releases the route while holding residuals open |
| closure-safe vs false closure | `V` (closure) | per-burden {resolved, deferred, transferred, risk-accepted} vs "all done" | residual ledger `δ` | falsely closed cases silently accrue debt; safe closure is reopenable by record | policy may claim completion only at the ledger's level |
| authorized vs factually established | `W` (warrant-state classification) | {authorized, established, both, neither} | authorization record vs validating evidence | authorized-but-unestablished placements must carry a revisit obligation | policy tags warrant type and never launders one into the other |

Verdict per model: **A** captures competing states but has no slot for the
last column — a state with no conduct attached governs nothing. **B**
captures conduct but fails the manuscript's anti-vacuity clause (iv) — a
rule renamed as a noun — and cannot say what two rules consulting the
*same* distinction (quarantine vs re-derive on staleness) have in common.
**C** fills every cell of every row; the state/policy split is load-bearing
exactly where B collapses (same `S_μ`, different `π_μ`).

### 3.3 Recommendation

**Adopt (C).** It is the only model under which all five worked examples
pass minimum specificity; it matches Definition 9's prose; it makes
rule-adequacy (§4, V3a) a predicate on `μ` separable from executor error in
`π_μ`; and it gives lesson-lift a target (revise `S_μ` or `select_μ`) distinct
from retraining conduct (revise `π_μ`).

**Preserved downsides of (C):** two objects per rule is real bookkeeping;
most working systems will implement (B) and only reconstruct the split
when audited — (C) is the audit-grade description, not a claim about how
practitioners write rules; boundary cases blur state and policy (a numeric
threshold is at once a state boundary and a conduct trigger); and the
split invites proliferation — every `if`-statement can be dressed as
configuration-plus-policy — which the safeguards below must block.

### 3.4 Plurality, conflict, precedence, provenance, revision, safeguards

- **Several metaorthemes per episode.** $\vec{\mu}(e) = (\{\mu_1, \dots, \mu_k\}, \preceq)$.
  Configurations governing *disjoint* components compose freely (their
  constraints conjoin); a typical episode runs under a version rule, an
  evidence-grade rule, and a closure rule at once.
- **Conflict and precedence.** `μᵢ, μⱼ` conflict at `e` when their
  meta-policies prescribe incompatible constraints on the same component
  under the states that actually obtain. Resolution only via the declared
  strict partial order `≼` (gloss: which rule outranks which, fixed by
  governance in advance). A conflict unresolved by `≼` is an ANDON
  condition — stop or escalate; silent override is itself a metaorthemic
  error.
- **Provenance of the governing rule.** `prov(μ) = ⟨authority, warrant,
  scope, ver(μ)⟩`. A rule of unknown provenance is a stale-evidence problem
  one level up; episodes record `ver(μ)` so audits can scope which
  placements ran under which edition. Governing *instructions* recovered
  from records obey the same discipline: existence, authenticity,
  recovery, authorization, and current force are five distinct predicates,
  and an authentic recovered directive may be stale as governance — the
  worked stale-steer case, with its directive record and fixture F6, is
  `examples/compaction-stale-steer.md` (Decision 0006).
- **Revision after lesson-lift (impact-scoped).** `ρ : (μ, lesson) ↦ μ′`
  increments `ver(μ)` and computes an **impact function**
  `affected(μ, μ′) →` the set of dependent claim/episode scopes: exactly
  the prior episodes whose placement CONSULTED the revised
  state-distinction or selector where the two editions disagree. Only
  those episodes' `ε` is downgraded from validated to provisional pending
  re-check (gloss: when the rule was wrong, the wins that depended on the
  wrong part are reopened — not every episode that ever ran under the
  edition). Blanket reopening of the whole edition cohort is corrected to
  this scoped form.
- **State families need not partition, and selection may be
  undetermined.** `S_μ` declares the competing higher-order states, but
  nothing forces them to be mutually exclusive or jointly exhaustive
  unless the configuration declares them so (an exclusivity marking, as
  for profile axes); and `select_μ` is a partial procedure — on a given
  episode it may return one state, several co-holding states, or
  **undetermined**. An undetermined selection is handled like any other
  unresolved placement: the meta-policy must declare conduct for it
  (stop, escalate, default conservatively), and silently assuming a
  partition where none was declared is a configuration defect (V3a).
- **Safeguards against inflation.** Admit a candidate `μ` only if: (i) `g`
  is named; (ii) `S_μ` is declared *in advance*, not read off one incident;
  (iii) switching the obtaining state changes validated placement, risk, or
  constraints in at least one episode class; (iv) it is not a first-order
  ortheme or a tunable parameter of `π` in disguise. This is the
  manuscript's anti-vacuity test with (ii)–(iii) sharpened to episode
  classes. A good policy that consults no in-advance-declared competing
  higher-order states is just a good policy. **Concept admission vs word
  utility are separate tests:** the four conditions above admit the
  DISTINCTION; whether the *word* "metaortheme" (or any coinage) earns
  keep over ordinary words is decided ONLY by the terminology benchmark
  (the terminology evaluation protocol under `terminology/`) — a real distinction may be
  admitted while its word is retired. (The former safeguard (v), which
  mixed the two tests, is deleted.)

---

## 4. Pathway adequacy (2D)

### 4.1 Separate verdicts

All verdicts are predicates on an episode `e` (some claim-indexed). **The
verdicts diagnose distinct dimensions and are not identified with one
another; they are NOT assumed pairwise logically independent.** Every
definitional or logical implication is declared explicitly in the
implication table at the end of this section; no implication may be
inferred merely from proximity in the verdict numbering (Decision 0003;
this supersedes the earlier "none entails another"). Verdict labels
follow the normative registry
([`docs/verdict-registry.yaml`](../docs/verdict-registry.yaml), Decision
0004): semantic IDs are authoritative in machine-readable records, and
the display aliases below are the prose forms.
**Compact core (main text):** result correctness; evidential support;
procedure truth-conduciveness; rule adequacy; executor fidelity; route
safety; closure truthfulness; robustness. **Full vector (this table)** —
the finer splits matter to audits; ordinary discussion may use the
compact core:

- **V1 — placement/profile correctness.** `correct(e)`: `p̂(e)` agrees
  with `O*(m; A(e))` at the governed level; weaker `route-correct(e)`: `p̂(e)`
  is route-sufficient and every placed claim is in `O*(m; A(e))` (gloss: the
  answer was right, for enough of the profile to act on — judged against
  the analysis the episode itself records). **Aggregation, stated once:**
  V1 is claim-wise at bottom — `V1_q(e)` holds iff placed claim `q` is
  true of `(m; A(e))` — and the episode-level verdict aggregates by
  CONJUNCTION over the claims placed at the governed level (for
  `correct(e)`, additionally requiring that the placed profile is
  determined at that level); the route-sufficient reading conjoins over
  the placed claims only. No averaging or majority rule is admissible for
  V1. **Result-side: V1 is never a conjunct of `PathwayAdequate`.**
- **V2a — evidential support.** The typed evidence `H`, within its
  declared scopes, meets the DECLARED standard for each placed claim
  (gloss: enough of the right kind of evidence, by the rulebook's own
  bar).
- **V2b-P — configured-procedure truth-conduciveness (pathway-side;
  Decision 0003).** NON-FACTIVE. The procedure family
  actually instantiated in this episode — under its governing
  configuration $\vec{\mu}$, applicable metaorthemmata `MetaTok(e)`, and
  execution mode — satisfies the predeclared reliability criterion over
  its DECLARED reference class. This is not an unrestricted claim about
  the abstract procedure type. For each placed claim `q`, the reliability
  specification records or references
  `RelSpec_q(e) = ⟨declared reference class; relevant case/risk stratum;
  reliability metric; threshold or tolerance; perturbation or comparison
  family where applicable; evaluation protocol; evidence used to
  establish reliability; version and validity conditions⟩`. The reference
  class, criterion, and threshold must be fixed independently of this
  episode's outcome — never selected after seeing the result merely to
  rescue or condemn it. The current episode's correctness may contribute
  to LATER aggregate reliability evidence, but one current correct result
  cannot by itself establish V2b-P. **`V2b-P(e)` does not entail
  `V1(e)`:** a reliable configured procedure may produce a rare error.
  *Default criterion:* a **sensitivity**-style counterfactual (the check
  passes because claims of this class are true, not alongside them);
  soundness, completeness, calibration, and perturbation-stability
  variants are admissible declarations, and fixtures may test each.
- **V2b-T — token-level truth linkage (result-side audit annotation;
  EXCLUDED from the pathway core).** FACTIVE and claim-wise:
  `V2b-T_q(e)` holds when THIS placed claim `q` was correct through the
  truth-relevant evidential mechanism rather than merely correct
  alongside it; by definition `V2b-T_q(e) → V1_q(e)` (truth of that
  claim). One claim-level `V2b-T_q` does not by itself entail
  correctness of the whole profile — a profile-level reading requires
  every placed claim covered and an explicit aggregation rule. It remains
  reportable for stopped-clock/Gettier diagnoses; its factivity is
  exactly why it sits outside `PathwayAdequate` (including it would
  re-import result correctness). Token-local PROCEDURAL defects are not
  represented by V2b-T alone: non-factive defects must appear under the
  appropriate pathway verdicts (V2a, V2b-P, V2c, V3a, V3b, V3c, V3d,
  or V6).
- **V2c — evidence currentness/provenance.** Each load-bearing evidence
  item is current for `(κ, v)` and carries admissible provenance (gloss:
  not stale, not unsourced — separated from V2a because evidence can meet
  the standard's *strength* while being the wrong vintage).
- **V3a — governing-configuration adequacy.** $\operatorname{adeq}(\vec{\mu}, e)$: each `μᵢ` in
  force is adequate for the case's risk class — `S_μ` separates the
  higher-order states this case class can occupy and `select_μ` can actually
  discriminate them (gloss: the rulebook was strong enough, whoever
  executed it).
- **V3b — meta-policy adequacy.** The meta-policy `π_μ`/procedure `π` is
  well-formed for the configuration it runs under (a sound rulebook can
  carry an ill-formed procedure).
- **V3c — governing-token adequacy (Decision 0002).**
  `V3c(e) ⟺ ∧_{μ̄ ∈ MetaTok(e)} TokenAdequate(μ̄, e)`, where
  `TokenAdequate(μ̄, e) ⟺ MetaInst(μ̄, μ) ∧ Compatible(μ̄, A(e)) ∧
  Anchored(μ̄, κ(e), v(e)) ∧ ScopeCorrect(μ̄, 𝒬(e)) ∧ Current(μ̄, t(e)) ∧
  Provenanced(μ̄) ∧ AuthorizedBinding(μ̄)` — every applicable concrete
  metaorthemma was correctly instantiated, analysis-compatible,
  occurrence-anchored, correctly scoped to the claims it served, current,
  provenanced, and bound under authority. PER-TOKEN statuses are preserved
  alongside the episode-level conjunction (the auditor must see WHICH
  governing application failed, e.g. `μ̄_2: stale calibration; μ̄_3: wrong
  claim scope`). Isolates the failure mode the vector previously could
  not name: correct standard (V3a) + sound policy (V3b) + faithful
  execution (V3d) + **defective case-specific binding** — wrong reference
  plane, wrong-role tolerance, expired calibration, wrong fixture or
  success surface. `MetaTok(e) = ∅ ⟹ V3c ∉ ReqPath(e)` (zero-burden
  rule; status recorded not-applicable, with reason). The Decision-0004
  lettering matches the conceptual adequacy chain: V3a (configuration) →
  V3b (policy) → **V3c (binding)** → V3d (execution) → V3e
  (decision-time).
- **V3d — executor fidelity.** The actor `α` actually executed `π` as
  written. An adequate rule + adequate policy + infidelic executor is a
  distinct failure mode routing to a different remedy (retrain/replace
  the executor, not rewrite the rule).
- **V3e — ex-ante procedural justification.** At decision time `t`, given
  exactly the evidence then available, the placement was the reasonable
  one under the declared loss/decision standard (gloss: blameless-at-the-
  time — indexed to decision time, unlike V2a/V2b-P/V2b-T which are audit-time
  verdicts about support and truth-connection).
- **V4a — route safety/admissibility.** `r` is admissible under the
  constraints in force; correct-route-unavailable is recorded as routing
  failure, not diagnostic uncertainty.
- **V4b — route near-optimality.** `r` is near-optimal given `p̂(e)` and
  the constraints (gloss: safe ≠ best; a safe but wasteful route fails
  V4b only).
- **V5 — closure truthfulness.** Every residual in `δ` has an admissible
  disposition with traceable ownership, and the completion claim matches
  the ledger — no collapse of {deferred, transferred, risk-accepted} into
  "resolved."
- **V6 — robustness under neighboring perturbations.** Robustness is
  always relative to a declared **perturbation specification**
  `PerturbSpec(e) = ⟨varied fields; invariant fields; generator or
  enumeration; size or measure; tolerance⟩`: which episode/input fields
  are deliberately varied (input version bumped, marker string removed or
  spoofed, evidence reordered or withheld, near-identical sibling
  substituted), which are held invariant (the policy `π`, the governing
  configuration $\vec{\mu}$, the analysis `A` and its version), and how the
  neighborhood is generated. This induces the perturbation relation
  `P ⊆ E×E` and neighborhood `N(e) = {e′ : (e, e′) ∈ P}` (gloss: the same
  machine on the cases next door). `robust(e)` holds iff EITHER (i) the
  declared neighborhood is finite and enumerated and the empirical
  proportion of V1 failures over it is at or below the declared
  tolerance, OR (ii) the specification declares a probability measure
  over the perturbation family and the failure probability under that
  measure is at or below tolerance — an undeclared "failure rate" over an
  unspecified infinite neighborhood is not a well-formed V6 claim.
  **Metaorthemma rebinding under perturbation:** where a perturbation
  bumps the input version, each governing token `μ̄` is re-bound to the
  perturbed occurrence by its own binding rule; a token that CANNOT be
  coherently re-bound (its anchor names the unperturbed version
  essentially) makes that perturbation inadmissible for V6 and reportable
  under V3c instead — silence about rebinding is not permitted.
  Metamorphic fixtures (paired correct-without-marker /
  incorrect-with-marker probes) are V6's operational estimator under
  clause (i). **V6 is not V2b-P:** V2b-P asks whether the configured
  procedure is truth-conducive over its declared reference class and
  criterion; V6 asks whether the episode is stable under a declared
  neighboring perturbation family. One test suite may supply evidence for
  both; the questions differ, and these definitions introduce no
  entailment between them.

**Result-free pathway core (Decision 0003).**

    CorePath = { V2a, V2b-P, V2c, V3a, V3b, V3c, V3d, V3e, V4a, V5, V6 }

Excluded by construction: **V1** (result correctness), **V2b-T**
(factive token-level truth linkage — entails claim truth), and **V4b**
(route near-optimality — an advisory/quality verdict recorded separately;
a route can be safe and adequate without being optimal).

**Governed applicability.** Pathway applicability is DERIVED, never a
discretionary post-hoc list — an executor cannot exempt a failing or
untested verdict by omitting it:

    ReqPath(e) = CorePath ∩ RequiredBy( A(e), episode-shape(e),
                   risk-class(e), claims(e), governance(e) )

Minimum derivation rules: **V3c** is required exactly when
`MetaTok(e) ≠ ∅` (the M1 zero-burden rule is preserved:
`MetaTok(e) = ∅ ⟹ V3c ∉ ReqPath(e)`); **V4a** is required when the
episode selects or authorizes a route; **V5** is required when the
episode makes a closure/completion claim or dispositions residuals;
**V6** is required when `A(e)` or the risk class predeclares a robustness
obligation. **"Not tested" is not "not applicable":** every verdict
excluded from `ReqPath(e)` carries a recorded applicability reason on the
episode record. (`ReqPath(e)` is the sole pathway requirement function;
the earlier separately recorded applicability set `App(·)` is retired by
Decision 0005 — nothing it expressed is lost, since exclusions now live
in the per-verdict `not-applicable` statuses and reasons.)

**Machine-readable derivation and honest status (R3).** The repository
ships `RequiredBy` as a machine-readable governance rule table
(`docs/governance-requirements.yaml`) over a typed episode-shape input
contract (`has_meta_tokens`, `selects_route`, `makes_closure_claim`,
`robustness_obligation`, `risk_class`), and `scripts/derive_reqpath.py`
derives `ReqPath(e)` from it with a per-verdict derivation trace
(required / not-required, governing rule, rationale); fixtures in
`tests/reqpath-fixtures.json` pin the derivation, including an
omission-attack case in which a declared path missing a derivable
requirement is detected rather than tolerated. Honest scope: the shipped
table is *one* complete, deterministic governance instance. `RequiredBy`
in general remains a **governance-supplied parameterized interface** —
the theory does not claim a closed universal calculus over every
conceivable governance regime, and this part of the formalism is
accordingly an open parameter, not "closed."

**Verdict status is not Boolean.**

    Status_i(e) ∈ { pass, fail, undetermined, not-applicable }

    PathwayAdequate(e)      iff every V_i ∈ ReqPath(e) has status pass
    PathwayDefective(e)     iff some  V_i ∈ ReqPath(e) has status fail
    PathwayUndetermined(e)  iff no required verdict fails and at least
                            one required verdict is undetermined

A missing assessment is `undetermined` — never silently counted as pass,
never silently removed as not-applicable.

**Declared implication/dependency table** (complete; nothing else is
asserted, and pairwise independence is NOT claimed where unproven):

| Relation | Status |
|---|---|
| `V2b-T_q(e) → V1_q(e)` | **Definitional entailment** (factive, claim-wise) |
| `V2b-P(e) → V1(e)` | **No** — non-factive by construction |
| `V3e(e) → V1(e)` | **No** — decision-time reasonableness is result-free |
| `PathwayAdequate(e) → V1(e)` | **No** — the core excludes V1 and V2b-T |
| `V1(e) → PathwayAdequate(e)` | **No** — stopped-clock and defective-binding cases |
| `V1(e)` at the governed level vs claim-wise `V1_q(e)` | Definitional: profile-level V1 aggregates the placed claims per the declared level |
| `PathwayAdequate(e) ↔ ¬PathwayDefective(e)` | **Not asserted** — `undetermined` is a third state |
| V6 vs V2b-P | **No entailment either way** (distinct questions; shared evidence possible) |
| All other pairs | No definitional implication introduced by these definitions; empirical correlation is never entailment |

### 4.2 Result × pathway matrix

The matrix applies only AFTER the pathway status is resolved as adequate
or defective; `PathwayUndetermined` episodes remain outside the four
resolved cells until audited. (Decision 0003: this
supersedes the earlier parenthetical that committed the token-level truth-connection verdict to
the conjunction — the incorrect-result/adequate-pathway cell is genuinely
representable.)

| | **PathwayAdequate** | **PathwayDefective** |
|---|---|---|
| **Result correct (V1)** | *Nominal.* A current behavioral validator, correctly bound to the current artifact (V3c pass where applicable), under a sufficiently reliable configured procedure, returns the correct result. Nothing to fix. | *Correct + defective (stopped-clock, compensating error, or governing-side luck).* Possible failure loci: V2b-P, V3a, V3b, V3c, V3d, or V6 — the marker validator that happens to be right today; the mis-bound metaorthemma whose wrong reference plane locally coincides with the right one. Remedy targets the procedure, rule, or binding — not the verdict. |
| **Result incorrect (¬V1)** | `AdequatePathError(e) := ¬V1(e) ∧ PathwayAdequate(e)` — the justified rare miss of a non-perfect but sufficiently reliable process used correctly: a genuine, representable cell, expected whenever such a process runs. Where V3e ∈ ReqPath(e), `JustifiedMiss(e) := AdequatePathError(e)` — V3e's pass is already inside PathwayAdequate, so no redundant conjunct is added. Remedy, if any: a new discriminating evidence source; no rule or executor blame. **Note:** orthemic adequacy does not establish moral, legal, institutional, or theological blamelessness — "blameless" is not a formal predicate here. | *Compound failure.* Wrong placement via a defective pathway — e.g., a deploy gate reads a cached test result from the previous commit and approves the current one (¬V1 with V2c and V3a failures). Remedy: both the placement and the rulebook/lineage machinery. |

**Worked verdict fixtures (deterministic; the four resolved cells are all
satisfiable, plus the undetermined state — machine-checkable encodings in
`tests/verdict-fixtures.json`, validated by
`scripts/validate_verdict_semantics.py`):**

| Fixture | Setup | Expected statuses |
|---|---|---|
| **F1 — nominal** | Current behavioral validator, correctly bound (V3c pass where applicable), reliable configured procedure, correct result | V1 pass; every ReqPath verdict pass ⇒ **PathwayAdequate** |
| **F2 — stopped clock** | SCAN-CLEAN marker validator happens to be correct today but fails its declared reliability and perturbation criteria | V1 pass; V2b-P fail; V6 fail ⇒ **PathwayDefective** (V2b-T may also fail as a result-side diagnosis: correct, but not through the truth-relevant mechanism) |
| **F3 — justified rare miss** | Properly configured, faithfully executed procedure meeting its declared reference-class reliability threshold errs on this token | V1 fail; V2b-P pass; V3a/V3b/V3c/V3d/V3e pass where applicable ⇒ **PathwayAdequate**; V2b-T_q **fails** (the placed claim is false — a false claim's truth-linkage verdict fails by factivity; it is never recorded "unavailable" absent an explicit declared applicability rule). *This fixture is mandatory: it proves the lower-left cell is no longer definitionally blocked.* |
| **F4 — defective metaorthemma, lucky result** | Sound standard and policy, faithful execution; the concrete token binds the wrong reference plane / tolerance / fixture / success surface / calibration; the result happens to be correct | V1 pass; V3a pass; V3b pass; V3d pass; **V3c fail** ⇒ **PathwayDefective** |
| **F5 — unresolved audit** | The result is known, but required robustness or provenance evidence has not yet been evaluated | one required verdict `undetermined` ⇒ **PathwayUndetermined**; neither PathwayAdequate nor PathwayDefective is asserted |
| **F6 — stale directive** (Decision 0006; worked case in `examples/compaction-stale-steer.md`) | A recovered governing directive is authentic but superseded; the executor follows it faithfully; the closure claim asserts it was in force | V1 fail; V2c fail; **V3c fail** (token not Current); V3d pass; V5 fail ⇒ **PathwayDefective** — faithful execution under a defective governing token |
| **F7 — safe but suboptimal route** | The chosen route is admissible but demonstrably wasteful | V4a pass; **V4b fail** (advisory, outside the core) ⇒ **PathwayAdequate** — safe ≠ best, and route quality never defeats adequacy |

### 4.3 Epistemic constraint and nearest neighbors

The defensible novelty claim is exactly this and no more: **the prior
manuscript, and the operational discipline it describes, did not
explicitly represent the concrete classification/handling episode as an
auditable occurrence distinct from its result.** It is *not* claimed that no established field can represent
episodes. Nearest neighbors, honestly: **process reliabilism**
(epistemology) names precisely the correct-result-through-unreliable-
process structure and the truth-connection idea — for *beliefs*; it offers
no operational record schema (no typed evidence, route, residual
disposition, successor occurrence, or perturbation estimator for
agent/validator episodes). **Audit trails / provenance records** (W3C
PROV, audit logs, ML lineage systems) are operational and token-level —
who did what to which artifact when — but typically carry no candidate
set, plural inferred profile, per-claim evidence status,
residual-disposition ledger, or verdict layer separating result
correctness from pathway adequacy and robustness. **Assurance practice**
(control-effectiveness vs outcome testing) and **metamorphic testing**
each contain one verdict (V3a-like, V6-like) without the joint object. What
the episode signature adds is the *joint* auditable object on which V1–V6
are simultaneously definable; whether that pays for itself over "audit the
validator when suspicious" is an open empirical question (fixture E5), not
a settled fact.

---

## 5. Mechanical and distributed orthing (2E)

### 5.1 Mechanical executors

Nothing in the episode signature or the verdicts quantifies over
awareness. Any rule-governed, evidence-updating executor — a
predictive-text decoder resolving an ambiguous keypress sequence, a CI
validator, a review chain — executes orthing, and its episodes bear **all
applicable verdicts** (`ReqPath(e)` plus recorded not-applicable reasons,
§4.1; the earlier "all six verdicts" contradicted partial applicability
and is corrected). Stopped-clock
analogs arise mechanically (a decoder emits the right word from a
frequency prior that would misfire on the neighboring input), so V6 is
meaningful without any conscious subject. **Consciousness is not
required.** The actor field `α` is populated with the mechanical executor
— never left empty — and executor identity is distinct from any authority
index.

### 5.2 Distributed episodes: graph and composition

Consider one case handled across sensors, validators, agents, routers, a
human sign-off, and downstream consumers. Model it twice, at two levels:

**Sub-episode graph.** `Γ_E = (E, ⇝)` is a finite DAG whose nodes are
episodes `e₁,…,e_n` (each with the full §2 signature — own actor `αᵢ`, own
$\vec{\mu}_i$) and whose edges are typed: **handoffs** (`eᵢ ⇝ eⱼ` iff a projection
of `out(eᵢ)` — a partial profile, an evidence item with its scope, a
route, a disposition — appears in the input or evidence `Hⱼ` of `eⱼ`;
gloss: what one worker concluded is what the next starts from),
**supersession** (a later episode revises an earlier one's conclusions),
and **retry-of**. Handoffs are the loci of transport error: a verdict
crossing an edge without its scope and version is how stale evidence
propagates.

**Edge orientation, one convention.** Every edge of `Γ_E` is oriented
from the EARLIER node to the LATER node; edge LABELS carry the semantics.
A `handoff` edge `eᵢ ⇝ eⱼ` means `eⱼ` consumes a projection of
`out(eᵢ)`; a `supersession` edge `eᵢ ⇝ eⱼ` means the later `eⱼ` revises
`eᵢ`'s conclusions; a `retry-of` edge `eᵢ ⇝ eⱼ` means `eⱼ` re-attempts
`eᵢ`'s task. (Prose like "a supersession edge to its predecessor" reads
the label backward along the same earlier→later edge; the graph stores
one orientation only.)

**Why a DAG is right despite retries and revision loops.** Nodes are
*dated tokens*; every typed edge points forward in time under the
convention above, so the token graph is acyclic by construction. A retry
or rework loop does not add a back edge — it creates a *new* episode
node reached by a `retry-of` or `supersession` edge from its
predecessor. The genuinely cyclic structure
(the same policy re-entered, review returning work to an author-role)
lives at the TYPE/policy level, which the formalism represents as
repeated instantiation of the same `π`, never as cycles among tokens.

**Composition.** The graph composes into ONE episode `e_Γ = comp(Γ_E)` — a
full §2 signature at the boundary level — iff:

1. **One case, one analysis:** all `eᵢ` address `m` or its `succ`-lineage
   under a single declared analysis `A` (hence one task `T = task(A)`;
   two sub-episodes sharing a task but differing in tolerance,
   representation, or boundary do NOT compose without an explicitly
   declared fusion analysis);
2. **A declared boundary:** governance names the composite actor `α_{e_Γ}`
   (pipeline, team, institution) and configuration $\vec{\mu}_{e_\Gamma}$, including
   precedence across sub-episode rules;
3. **A declared fusion rule:** `p̂_{e_Γ}`, `estatus_{e_Γ}`, `δ_{e_Γ}` are a stated
   aggregation of sub-outputs (e.g., profile union with per-claim status =
   weakest status along its supporting path; residual ledger = merged
   ledgers with surviving ownership) — well-defined, not read off the last
   node.

Then `e_Γ` is a token in its own right, and each `eᵢ` becomes an orthemma of
the composite-level audit via the reification embedding
(`ι_n(eᵢ) ∈ M^(n+1)` per §1 — never literal membership). **Answer to one-vs-graph:
both, at different levels.** The graph is the true description at the
component level; the composed episode at the boundary level; `comp` and
its three conditions say when the second description exists. When
condition 2 or 3 fails — no declared boundary, no fusion rule — there is
only the graph, and talk of "the system decided" is unwarranted composite
attribution.

Composite verdicts do not reduce to conjunctions: `correct(e_Γ)` can hold
while some `correct(eᵢ)` fails (a downstream validator caught it), and
every `correct(eᵢ)` can hold while `correct(e_Γ)` fails (each verdict true
in scope, the composition transporting one out of scope). Hence the
composite level must be audited separately.

### 5.3 Multi-actor episodes over one occurrence lineage (derived)

Several actors' episodes can address ONE shared occurrence lineage with
analysis-indexed, possibly opposed evaluations (competitive games are the
clean case; the full stress test and category corrections live in
`orthemic-multi-actor-conflict-note.md`). This is a **multi-analysis
context**: each actor `α` evaluates under its own declared analysis
`A_α` (shared frame components, diverging at least in task
`T_α = task(A_α)`), the task-relative abbreviation is forbidden, and
ground truth is written in full, `O*(m; A_α)`. Actor indices are written
`α, β` here — the letter `A` is reserved for the analysis. Derived
definitions — clarifying extensions of the existing actor/analysis
indices, **not a new formal addition**:

- `x_α = Ω_α(m)` — actor-α's OBSERVATION of the shared occurrence
  (imperfect information is divergent observation over ONE occurrence:
  `Ω_α(m) ≠ Ω_β(m)`; perfect information is the special case of full,
  equal observation) — the observation/occurrence distinction applied per
  actor;
- `p̂(e, α, T_α)` — actor-α's current inferred profile in episode `e`
  under its analysis `A_α` (task `T_α`), inferred FROM `x_α`, never from
  `m` directly;
- `GoalSchema(·)` — a PARAMETRIC ortheme schema (the shared goal-form under role
  substitution); grounded instantiations `GoalSchema(α)`, `GoalSchema(β)` are DISTINCT
  targets even when the schema is one (schema identity ≠ grounded-ortheme
  identity ≠ target-profile overlap);
- `𝒢_{α,A_α} ⊆ Π_{A_α}` — actor-α's grounded target profile set —
  NORMATIVE TYPING: a SET of profiles, each member one complete profile
  (the task's appropriateness rendered as a profile set; targets are
  selected BY the task, which remains an external parameter — a target
  profile is not an objective and an objective is not an ortheme);
- `φ(α→β)` — a role/perspective isomorphism between `Π_{A_α}` and
  `Π_{A_β}` where one exists (goal-schema invariance with disjoint
  extensions: `𝒢_{β,A_β} = φ(𝒢_{α,A_α})`, possibly `𝒢_α ∩ 𝒢_β = ∅`);
- `Conflict_m(𝒢_α, 𝒢_β)` / `Compat_m(𝒢_α, 𝒢_β)` — WELL-TYPED across
  profile spaces: the two target sets live in different spaces
  (`𝒢_α ⊆ Π_{A_α}`, `𝒢_β ⊆ Π_{A_β}`), so they are never compared by bare
  set intersection. With `Reach(m)` the occurrences reachable from `m`
  in the successor structure,

      Compat_m(𝒢_α, 𝒢_β)   iff  ∃ m′ ∈ Reach(m):
                                  O*(m′; A_α) ∈ 𝒢_α  ∧  O*(m′; A_β) ∈ 𝒢_β
      Conflict_m(𝒢_α, 𝒢_β) iff  no such reachable m′ exists

  — one shared occurrence, evaluated under each analysis separately.
  Cooperation is joint realizability with a shared analysis and shared
  target set (`A_α = A_β`, `𝒢_α = 𝒢_β`), or an explicit alignment map
  `φ(α→β)` identifying targets across spaces — never bare equality of
  sets inhabiting different profile spaces. Zero-sum games also admit
  draw successors realizing neither target set.

Coupled episodes are the §5.2 graph over the shared lineage: each actor's
action creates the successor occurrence the other's episode consumes.
Game transition rules are DOMAIN structure, utility is the TASK, minimax
is a POLICY — none is a metaortheme. The LIMITED sense in which
competitors share a metaorthemic configuration: both may consult the same
governing distinctions (terminality, evidence-validity about the
opponent's information state, analysis-sufficiency) while holding opposed
targets — configurations govern HOW placements are made, never WHOSE
target wins. Occurrence identity in games includes position, history, and
player-to-move — worldly facts (#4 applied); a player's INFORMATION SET is
NOT identity but that player's OBSERVATION `x_α = Ω_α(m)` (a correction
adopted after external review — filing it into `κ` would invert the
occurrence/observation line). Not all orthemes are actor-relative —
actor-relativity enters exactly where the task does.

### 5.4 Semantic depth as an orthogonal axis

Define, informally, `depth(e)` as the executor's grasp of the governing
distinctions: hard-coded check < model-based inference over declared
alternatives < reflective capacity to propose revisions `ρ(μ, lesson)`
itself. Depth is orthogonal to every §4 verdict — shallow executors can
run adequate pathways and deep ones defective pathways. Depth matters
operationally in one place only: which revisions the executor may perform
locally versus must escalate across the governance boundary. It is an
axis of the executor, not of the episode's correctness or adequacy.

---

**Optional latent-variable extension (Decision 0015).** A declared analysis `A` may
optionally carry sequential latent-variable apparatus (`Z_A`, transitions `P_A`, latent
candidate sets/posteriors, and concrete internal representations `y`). That apparatus is
**non-primitive and optional**: it adds nothing to the settled ontology of this
formalization, a latent state is not an ortheme, a posterior is not `O*(m; A)`, and
representational geometry is neither necessary nor sufficient for orthemic distinctness
or for pathway adequacy. The bridge `ProfileOf_A ⊆ Z_A × Π_A` is partial and must be
exhibited, never assumed; latent labels are non-identifiable up to relabelling absent
declared anchoring or a validated alignment map. **Every core claim of this formalization
remains statable without the latent layer.** Declaring it is a version event on `A`. See
`docs/decisions/0015-latent-state-observation-and-representation-boundary.md` and
`docs/related-work/LATENT-STATE-INFERENCE-AND-ORTHEMOLOGY.md`.

## Status ledger

**Accepted (analytic/definitional):** level-indexing via `ι_n` with no
episode-referent "meta-orthemma" noun (§1, counterargument recorded; per
the §1 qualification, the Decision-0002 configuration token `μ̄` is a different object, carried in §2.2/§3/§4.1 V3c); the record-style
episode signature with typed candidate families, claim ledger, handoffs,
warrant, and labeled successors (§2.2); endpoint-plus-bounded-trace with
governance-declared granularity (§2.2a); split model (C) with the
`{O,I,E,D,R,V,W}` boundary (§3, downsides preserved); verdict separability
with governance-derived `ReqPath(e)` (§4.1); token-level DAG with typed
edges (§5.2). **Rejected:** literal set inclusion for episodes; forced single
successor; blanket edition-wide revision reopening; safeguard (v)
word-utility test inside concept admission. **Unresolved alternatives:**
safety/reliabilist/calibration variants of V2b-P remain admissible declared
criteria; single-object metaortheme presentation (C1) remains permitted as
user-facing shorthand. **Experimental gates:** episode reification's
practical delta over "audit the validator when suspicious" — fixture E5;
vocabulary utility of every coined term — the Arm A/B/C benchmark
(designed, NOT run). **Evidence tier:** machine-checked internal
agreement over the declared definitions, schemas, examples, and adversarial
fixtures — not a proof of mathematical consistency or completeness;
no public observational dataset exists; operational usefulness is untested;
nothing here is experimentally validated. **Provenance:**
`docs/provenance/document-history.md`; this file is the canonical
integrated body.
