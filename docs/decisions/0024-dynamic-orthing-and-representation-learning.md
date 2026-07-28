# Decision 0024 — Dynamic orthing and representation learning

**Date:** 2026-07-21 · **Authority:** R7B owner authorization (Opus candidate pass) · **Status:** proposed-candidate · **Reopens nothing:** Decisions 0001–0023 stand. This **extends** Decision 0015's static latent-state boundary with an update/learning architecture. It adds no school-neutral core primitive; it is a bounded application-level extension under `applications/latent-state-orthing/`.

**Provenance:** OPUS CANDIDATE — REQUIRES FRESH FABLE REVIEW BEFORE MERGE.

## Problem

Decision 0015 correctly separated the static objects — occurrence $m_t$, latent
model state $z_t$, observation $x_t$, posterior/belief $b_t$, internal
representation $y_t$, inferred orthemic profile $\hat p_t$ — and refused to
define orthemes by vector orthogonality. But it is a **boundary note, not a
theory of dynamics**. The OSM/CSCG source (the OSM source (Sun et al., Nature 2025, DOI 10.1038/s41586-024-08548-w; local extraction `opendataloader-output/s41586-024-08548-w.md` is evidence provenance only))
reports progressive decorrelation into an orthogonalized state machine, learned
transitions among latent states, endpoint performance that **underdetermines**
learning mechanism (CSCG uniquely reproduced both the final states *and* the
learning trajectory; LSTM/transformers/vanilla RNNs did not), and adaptation
under altered cues. The corpus had no way to represent *how representations,
repertoires, and analyses change over time* without conflation.

## Decision

**1. Four update levels are named and kept strictly separate.** No change at one
level silently transports to another.

```math
\begin{aligned}
\text{episode inference:} \quad & b_t \to b_{t+1}, \quad \hat p_t \to \hat p_{t+1} \\
\text{representation / model learning:} \quad & \theta_t \to \theta_{t+1} \\
\text{metaortheme / repertoire revision:} \quad & \mu_t \to \mu_{t+1}, \quad \mathcal{O}_{A,t} \to \mathcal{O}_{A,t+1} \\
\text{analysis-version change:} \quad & A_t \to A_{t+1}
\end{aligned}
```

Episode inference moves belief within a fixed analysis/model as evidence
arrives. Representation learning changes the actor/model's internal
representation, transition, or emission structure. Repertoire revision changes
which metaorthemes/routes exist, under governed revision. An analysis-version
change (task, tolerance, boundaries, representation family, merger family,
governance) yields $A_{t+1}$ and blocks silent transport of placements,
validations, and verdicts (the Decision 0005 §2.5 transport discipline, now made
dynamic).

**2. World transition and learner update are different edges.**

```math
m_t \xrightarrow{a_t} m_{t+1} \quad \text{(occurrence/world lineage)} \qquad \theta_t \xrightarrow{U_A(e_t)} \theta_{t+1} \quad \text{(learner update)}
```

The first changes the occurrence lineage (Decision 0005 successor edges); the
second changes the model/actor. Conflating them is the error `DYN-2` guards.

**3. Optional dynamic record (model-specific, not a core primitive).**

```math
D_A = \langle Z_A, X_A, Y_A, B_A, \Theta_A, P_A, \operatorname{Emission}_A, U_A, \operatorname{Revision}_A \rangle
```

with $x_t = \Omega_A(m_t)$, $b_t \in \Delta(Z_A)$ (a distribution over latent
states), $y_t = f_{\theta_t}(\text{history})$, $\hat p_t \in \Pi_A^\partial$,
$a_t = \pi_{\bar\mu_t}(\hat p_t, H_t)$, $m_{t+1} \in \operatorname{Succ}_{a_t}(m_t)$,
$\theta_{t+1} = U_A(\theta_t, e_t)$. This is one candidate instrument, not a
commitment; a system may realize dynamics without it.

**4. Ortheme admission is by declared ablation, never by latent split.** A
latent/model distinction earns orthemic status **only** when a declared
merge/ablation test shows that collapsing it changes warranted prediction,
action, routing, validation, closure, or loss beyond tolerance $\epsilon_A$.
Consequently there is **no** assumed one-to-one map between $Z_A$ and
$\Pi_A$: one latent state may encode a whole profile; several may share one
profile; one orthemic distinction may be distributed over many model dimensions;
an overcomplete model may invent splits; an underfit model may hide consequential
ones.

**5. OSM/CSCG claim status is external exemplification and constraint — not
validation.** The source is used only for its reported abstract computational
structure (observation/state separation, hidden-state inference, representation
learning, endpoint-vs-trajectory, altered-cue transport, representation
geometry). It does **not** validate Orthemology, its terminology, human noetics,
or any metaphysical claim. Orthogonalization is **one** representational
geometry, neither necessary nor sufficient for distinct worldly states, distinct
orthemes, pathway adequacy, or strict soundness. No biological, wet-lab,
human-cognition, fiṭrah, or metaphysical content is imported.

## Artifacts and gate

- `applications/latent-state-orthing/DYNAMIC-ORTHING-AND-LATENT-STATE-LEARNING.md` — the worked extension + diagrams (rendered via Decision 0023).
- `applications/latent-state-orthing/OSM-CSCG-ORTHEME-CROSSWALK.yaml` — typed crosswalk with per-row claim status (source-report / model-mechanics / synthesis / orthemology-extension) and non-claims.
- `applications/latent-state-orthing/DYNAMIC-FIXTURES.yaml` — fixtures DYN-1..DYN-8.
- `scripts/validate_dynamic_orthing.py` — enforces the four-level separation, the world-vs-learner edge, ablation-based admission, and the not-validation boundary; wired into CI.

Reopens nothing; establishes no empirical or metaphysical claim.

## R7C amendment (2026-07-21, Opus candidate; audit B6/B7/B8)

- **D5/D6/D7 formal repairs** (`DYNAMIC-ORTHING-AND-LATENT-STATE-LEARNING.md`):
  endpoint compares representation geometry `Geom_A` (not parameters); the
  latent→profile map is a **relation** `ProfileOf_A ⊆ Z_A × Π_A` (not a function);
  ortheme admission uses a **scalar** merger contrast `Δ^merge_A(z_i,z_j) > ε_A`.
- **OSM object separation** (`OSM-CSCG-ORTHEME-CROSSWALK.yaml`): the conflated
  "clones / state cells" row is split into biological state-cell response, CSCG
  clone, latent posterior, and model representation geometry — separately typed.
- **Governed update coupling** (`UPDATE-COUPLING.yaml`): each of the four levels
  declares trigger / authority / input / version / transport / invalidated /
  reopening / rollback; repertoire revision changes what the **declared
  repertoire** can represent, not worldly facts.
- **Failure-family fixtures** DYN-10..DYN-20 (label permutation, overcomplete
  split, underfit merge, OOD, nonstationary map, catastrophic forgetting,
  endpoint-vs-trajectory, model-update-without-profile-change and its converse,
  analysis-vs-model drift, hysteresis/rollback). Gate: `validate_dynamic_orthing.py`.

## R7D dated amendment (2026-07-21, Decision 0033 / Phase I; audit B31–B36, probe P7)

**Provenance:** OPUS CANDIDATE — REQUIRES FRESH FABLE REVIEW BEFORE MERGE.

R7C named the dynamic relations; R7D **defines** them and closes the silent-transport
probe:

- **Gated transport (B34/P7).** `UPDATE-COUPLING.yaml` is now schema-validated
  (`UPDATE-COUPLING.schema.json`): every level's `transport` is a structured object
  requiring `default: no-transport-without-argument` and `argument_required: true`, plus
  a `calibration` and a `catastrophic_forgetting_check`. A silent or blanket-universal
  transport rule fails CI (`validate_dynamic_orthing.py`).
- **Definitions (B31/B32/B33/B35).** `OSM-DYNAMICS-DEFINITIONS.yaml` defines
  `Geom_A(theta)` (extraction, metric, alignment, permutation/rotation/scale invariance,
  uncertainty, distribution); `ProfileOf_A ⊆ Z_A × Π_A` (evidence basis, analysis/model
  version, relation status, many-to-many cardinality, uncertainty, transport); and the
  merger contrast `Delta^merge_A` (model version, merge operation, evaluation
  distribution, horizon, action/loss surfaces, hard constraints, uncertainty interval,
  tolerance source, admission rule). The OSM object map keeps eleven distinct layers.
- **Bounded source claim (B36).** The CSCG comparison stays within the reported
  model/settings comparison; no unique biological mechanism, clone=neuron identity,
  latent=ortheme identity, or human/metaphysical/theological transfer.

This amendment reopens no settled Decision, adopts no terminology, runs no experiment,
and asserts no interior/soul or metaphysical claim.
