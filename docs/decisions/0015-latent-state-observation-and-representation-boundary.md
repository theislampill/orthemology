# Decision 0015 — Latent-state, observation, and representation boundary

**Date:** 2026-07-20 · **Authority:** R4 owner authorization (latent-state amendment) · **Status:** adopted · **Does not reopen:** D1 (0001), M1 (0002), O2 (0003), D3 (0004), D4 (0005), O3 (0006), Π_A (0007), C′ (0008), type/token + concrete reason (0009), orthability sense boundary (0010).

## Problem

Sequential latent-variable models of cognition — hidden Markov models, clone-structured graphs, recurrent networks — supply objects that *look* like orthemological objects and are not. A model's hidden state `z_t` resembles an ortheme; a model's emitted observation `x_t` resembles an orthemma; a network's hidden activity vector `y_t` resembles a profile; a posterior over hidden states resembles a candidate set. Left unregulated, four conflations follow: (i) the model's latent label is read as the repeatable operational state-type; (ii) the observation is read as the concrete occurrence; (iii) the posterior is read as ground truth; (iv) geometric properties of a representation (orthogonality, decorrelation, clustering) are read as facts about worldly state identity or about orthemic distinctness. A fifth follows from the first four: every remapping of a cue to a state gets called a metaorthemma, dissolving the M1 material-binding discipline.

This decision fixes the boundary. It adds **no primitive** to the settled ontology.

## Decision

### 1. The six-way typed distinction

Under a declared analysis `A`, the following are **six distinct object kinds** and are **not interchangeable**:

| # | Object | Type | Status |
|---|---|---|---|
| 1 | `m_t ∈ M_A` | concrete situated occurrence (orthemma), time-indexed | **primitive** (D1) |
| 2 | `A` | the declared, versioned analysis | **primitive** (D1) |
| 3 | `z_t ∈ Z_A` | model-specific latent state, with transitions `P_A(z′ ∣ z, a)` | **OPTIONAL, NON-PRIMITIVE** |
| 4 | `x_t = Ω_A(m_t)` (or emission `P_A(x ∣ z)`) | observation | derived (Ω already in the registry) |
| 5 | `C^latent_t ⊆ Z_A` and/or belief `b_t(z)` | latent candidate set / posterior | **OPTIONAL, NON-PRIMITIVE** |
| 6 | `p̂_t(m) ∈ Π_A^∂` | inferred partial orthemic profile | derived (0007) |
| 7 | `y_t` | concrete internal representation (activity vector, embedding, hidden layer) | **NON-PRIMITIVE**, concrete token |

(Rows 3, 5, 7 are the additions; rows 1, 2, 4, 6 are restatements of settled objects. The latent layer is a *modeling convenience declared inside `A`*, never a second ontology, never a hidden second analysis.)

**Rule:** `m ≠ z ≠ x ≠ b ≠ y ≠ p̂`. No document, schema, fixture, or record may substitute one for another, and none of them is `O*(m; A)`.

**Non-primitivity clause.** `Z_A`, `P_A`, `C^latent`, `b`, and `y` are optional apparatus. Every claim statable with them must remain statable without them (in terms of `m`, `A`, `Inst_A`, `O*`, `p̂`, episodes and verdicts) or it is not a claim of this framework. Declaring a latent layer is a **version event on `A`**, recorded like any other.

### 2. Admission test for latent distinctions

A latent distinction `z_i ≠ z_j` is **orthemically consequential under `A`** only if merging `z_i` and `z_j` would, beyond the declared tolerance, alter at least one of:

1. a warranted prediction,
2. a classification/placement,
3. an investigation (what evidence must be gathered),
4. a route,
5. a validation step,
6. a closure condition,
7. an evaluation,

**or** would violate a hard constraint in force. If no such change follows, the distinction is a *model-internal* distinction only: it may be retained for modeling reasons, but it licenses no new ortheme, no new profile component, and no new verdict. This is the anti-vacuity standard of the core formalization applied to the latent layer; it is the same test that refused a new noun class in §1 of the formalization.

### 3. The partial bridge relation

    ProfileOf_A ⊆ Z_A × Π_A

`ProfileOf_A` relates a latent state to orthemic profiles under `A`. It is explicitly **NOT required to be total** (a latent state may correspond to no declared profile) and **NOT required to be one-to-one** (several latent states may share a profile; one latent state may be compatible with several). Consequently:

- from `z_i ≠ z_j` nothing follows about `O*(m_i; A)` vs `O*(m_j; A)` without an exhibited bridge;
- from a profile difference nothing follows about latent-state count;
- any claim of the form "this cluster **is** that worldly state" requires the bridge to be **declared**, not assumed.

**Non-identifiability.** Latent states are identified only up to permutation and relabelling (and, for clone-structured models, up to which clone of a shared emitted symbol is occupied). A latent label is an index in a fitted model, not a name of anything. Two fits of the same model family on the same data may assign different labels to the same structure; the labels therefore carry no cross-model, cross-version, or cross-analysis meaning.

### 4. Anti-orthogonality rules

Let `RepresentationalOrthogonality(y_i, y_j)` be a geometric property of concrete internal representations (decorrelation, near-orthogonality, cluster separation).

- **R1.** `RepresentationalOrthogonality(y_i, y_j)` does **not** entail `z_i ≠ z_j`. Geometry is evidence about a representation, not a criterion of state identity.
- **R2.** `z_i ≠ z_j` does **not** require global orthogonality. A model or system may carry a genuine state distinction in a low-dimensional or task-restricted subspace while its global representational geometry remains entangled.
- **R3.** `RepresentationalOrthogonality(y_i, y_j)` does **not** by itself entail that `o_i` and `o_j` are non-equivalent under `A`. Orthemic equivalence is fixed by `Inst_A` and `O*(·; A)` at the declared level and tolerance, never read off a geometry.

Corollary (adequacy): **absence of global orthogonalization is not by itself a pathway defect.** A system that meets its declared task requirements without a globally orthogonalized representation fails no verdict on that ground alone. Representational geometry and pathway adequacy (O2) are separate questions.

### 5. The five-way rebinding distinction

When "the mapping changed," exactly which of the following changed must be stated:

1. **Observation/emission rebinding** — `Ω_A` or `P_A(x ∣ z)` changes; a cue now emits from, or is read as, a different symbol. The latent state set is unchanged.
2. **New latent-state creation** — `Z_A` gains a state.
3. **Transition-model revision** — `P_A(z′ ∣ z, a)` changes; `Z_A` and the emission map may be unchanged.
4. **Analysis-version change** — `A` itself is re-versioned (domain, repertoire, task, tolerance, level).
5. **Metaortheme/metaorthemma rebinding** — a governing type is revised (metaortheme) or a case-bound configuration token is bound/rebound (metaorthemma).

**NOT every cue remapping is a metaorthemma.** Categories 1–4 are model-side or analysis-side events. A metaorthemma arises only where the **M1 material-binding criteria** are met — a material case-specific binding, non-default scope, instrument/calibration provenance, or an independent validity condition, with a binder distinct from the executor. Where they are not met, the M1 **zero-burden rule** applies: no token, and `GOV_TOKEN_ADEQUATE` (V3c) is recorded not-applicable with reason. Naming a bare remapping a metaorthemma is a typing error, not a conservative choice.

### 6. Transport rule

Claims established under one observation model, one emission map, one transition model, or one analysis version **do not silently transport** after remapping, perturbation, or model revision. Any claim carried across such a change must be re-established or re-scoped, and the carry must be recorded (which claim, from which version, to which, on what warrant). Silent transport is an `EVIDENCE_CURRENT` (V2c) failure on the transported claim and, where it selected the route or the closure, implicates `ROUTE_ADMISSIBLE` (V4a) and `CLOSURE_TRUTHFUL` (V5). A latent-state label in particular is **never** transportable across model or analysis versions (§3, non-identifiability).

### 7. Continuous-implementation warning

Nothing in this decision licenses:

- **"ortheme cells"** — no unit, neuron, channel, or feature is an ortheme;
- **one-neuron-one-type** — orthemes are repeatable operational state-types individuated by `Inst_A`, not by any single physical or computational element;
- **neural localization** — this framework makes no claim that any orthemological object is realized at any anatomical or architectural locus.

Where a substrate is described in the literature as a *continuum* of graded, plastic response profiles with units changing functional role over time, the correct orthemological reading is that population-level or model-level structure may be discrete under a declared analysis while the implementing elements are continuous and role-mobile. Type–token discipline (0009) forbids reading a discrete type off a single continuous element.

### 8. Citation correction (recorded)

The controlling owner amendment cited the first author of *"Space is a latent sequence: A theory of the hippocampus"* (Science Advances 10(31):eadm8470, 2024, doi:10.1126/sciadv.adm8470) as **"Rajeev V. Raju."** That is **wrong**. The verified first author is **Rajkumar Vasudeva Raju**. The error is a conflation with **Rajeev V. Rikhye**, a co-author of the 2021 Nature Communications clone-structured-graph paper (doi:10.1038/s41467-021-22559-5). The correction is recorded here, applied in `references/latent-state-additions.bib`, and the erroneous form must not be reintroduced.

Related nomenclature note: the 2021 paper expands CSCG as clone-structured **cognitive** graph; the 2024/2025 literature uses clone-structured **causal** graph. Both expansions are in use; neither is a different object, and the expansion used should be stated when the acronym is introduced.

### 9. Scope and non-claims

- This decision **reopens nothing**: D1, M1, O2, D3, D4, O3, Π_A, C′, 0009, and 0010 stand intact. No new primitive, no new registry verdict, no change to `core_path`.
- The cited neuroscience and modeling literature is **related work**, **not empirical validation of orthemology**. Nothing in this corpus is experimentally validated; the fixture suite checks consistency only.
- These papers supply **no evidence whatever** about human rationality, fiṭrah, metaphysical orthability, a Necessary Being, or divine Speech. Any use of them toward those topics is out of scope and unlicensed by this decision.
- The word "ortheme" receives no etymological, empirical, or terminological support from this literature.

## Consequences

New: `docs/related-work/LATENT-STATE-INFERENCE-AND-ORTHEMOLOGY.md` (bounded related-work note with the mapping table and scope limits); `examples/latent-state-sensory-aliasing.md` (worked case); `tests/latent-state-fixtures.json` with `scripts/validate_latent_state_fixtures.py` (fixtures LS-1…LS-7, plus machine-checked anti-conflation assertions); `references/latent-state-additions.bib` (bibliography fragment; three OFFICIAL-PUBLISHER-VERIFIED entries with the Raju correction noted). The validator fails closed on any fixture asserting an identity this decision forbids.
