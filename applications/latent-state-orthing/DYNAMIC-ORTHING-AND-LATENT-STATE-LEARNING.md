# Dynamic orthing and latent-state learning

**Status:** DRAFT — application-level extension (Decision 0024). OPUS CANDIDATE —
REQUIRES FRESH FABLE REVIEW BEFORE MERGE. Establishes no empirical, human, or
metaphysical claim. The OSM/CSCG source is used for its reported abstract
computational structure only (Sun et al., *Nature* 2025,
doi:10.1038/s41586-024-08548-w). The retained access copy is custody evidence
only (SHA-256 `0D097CBA7BBB25A949E2BF95AF28B5A2259BD8D60B0E5FAC5A74CDF7D05AA814`);
its extraction lines are not journal pagination. MAP decode is separately
corroborated by the pinned official code at
`sprustonlab/OSM_Paper_Figures@c1d1788b54c737efe24402e02762eee10da0d0d7`.
No biological procedure and no human/noetic/metaphysical transfer is imported.

This note adds a **learning/update architecture** to Decision 0015's static
latent-state boundary. Diagrams render on GitHub (MathJax) and through the
Decision 0023 pipeline; they use only the notation registry.

## 1. The static boundary (Decision 0015), unchanged

```math
m_t \neq z_t \neq x_t \neq b_t \neq y_t \neq \hat p_t
```

This compact inequality abbreviates a larger typed firewall. In the Task 8
contract, world/task state, concrete occurrence, biological sensory observation,
model observation symbol, biological single-cell response, biological population
representation, CSCG clone, latent posterior, model parameter state, model
representation output, derived representation geometry, inferred orthemic
profile, and actual orthemic profile are thirteen distinct objects. Nothing
below merges them; the dynamics act *within* and *between* typed relations.

## 2. Four update levels (kept separate)

```math
\begin{aligned}
\textbf{episode inference} \quad & b_t \to b_{t+1}, \ \hat p_t \to \hat p_{t+1} && \text{(fixed } A, \theta) \\
\textbf{representation learning} \quad & \theta_t \to \theta_{t+1} && \text{(model changes)} \\
\textbf{repertoire revision} \quad & \mu_t \to \mu_{t+1}, \ \mathcal{O}_{A,t} \to \mathcal{O}_{A,t+1} && \text{(what exists changes, governed)} \\
\textbf{analysis-version change} \quad & A_t \to A_{t+1} && \text{(blocks silent transport)}
\end{aligned}
```

## 3. Diagrams

### D1 — world occurrence and observational aliasing

```math
m \xrightarrow{\Omega_A} x \qquad m' \xrightarrow{\Omega_A} x \qquad (m \neq m')
```

Two distinct occurrences can present the same observation $x$: the observation
is impoverished, aliased, or misleading. This is Decision 0015's occurrence /
observation gap, not deformation.

### D2 — biological observation, model symbol, and latent candidates

```math
x \ \longmapsto\ \{ z^{(1)}, z^{(2)}, \dots, z^{(k)} \} \subseteq Z_A
```

A biological sensory observation and the model's discrete observation symbol
are related by a declared abstraction, not identity. In the CSCG, a fixed model
symbol is emitted by several latent states (clones). Belief
$b_t \in \Delta(Z_A)$ is a distribution over the clones, not any clone, world
state, or orthemic profile.

### D3 — history-dependent disambiguation

```math
b_{t+1} = \operatorname{update}(b_t, x_{t+1}, H_t) \qquad H_t = (x_1, a_1, \dots, x_t)
```

History $H_t$ narrows the candidates: the same $x$ resolves to different latent
states depending on the path. This is inference, not learning; $\theta$ is fixed.

### D4 — occurrence transition vs learner update (different edges)

```math
m_t \xrightarrow{a_t} m_{t+1} \qquad\text{vs}\qquad \theta_t \xrightarrow{U_A(e_t)} \theta_{t+1}
```

The left edge changes the world lineage; the right edge changes the model. DYN-2.

### D5 — endpoint vs learning trajectory

Compare **representation geometry** under a declared analysis (via a typed
observable/representation map $\operatorname{Geom}_A$), never model-specific
parameter vectors — different model families do not share a parameter space:

```math
\operatorname{Geom}_A(\theta^{\text{CSCG}}_{\text{final}}) \approx_A \operatorname{Geom}_A(\theta^{\text{RNN}}_{\text{final}}) \quad\text{yet}\quad \operatorname{Geom}_A(\theta^{\text{CSCG}}_t) \neq \operatorname{Geom}_A(\theta^{\text{RNN}}_t) \ \text{along the trajectory}
```

Several tested settings satisfy a declared similar-final-representational-
structure criterion. Among the tested models under the reported evaluation,
only CSCG consistently matches the reported decorrelation order.
Criterion-level endpoint similarity is not exact representation or parameter
identity and underdetermines trajectory and mechanism. DYN-7. (Corrects R7B's
parameter-equality form; audit B6.1.)

### D6 — latent state / orthemic profile is a partial relation

A **relation**, not a function — one latent state may encode a whole profile;
several may share one; one orthemic distinction may spread over many dimensions:

```math
\operatorname{ProfileOf}_A \subseteq Z_A \times \Pi_A \quad (\text{many-to-many; not a function, not a bijection})
```

DYN-5. (Corrects R7B's function-arrow form; audit B6.2.)

### D7 — ortheme admission is by ablation, not by latent split

A **scalar** merger contrast: the increase in best attainable loss when the
representation family is constrained to merge $z_i, z_j$, versus unconstrained
(loss $L_A^*$ from the registry; over $\operatorname{Rep}_A$):

```math
\Delta^{\text{merge}}_A(z_i, z_j) := \inf_{\chi \in \operatorname{Rep}_A(z_i = z_j)} L_A^*(\chi) - \inf_{\chi \in \operatorname{Rep}_A} L_A^*(\chi), \qquad \text{split admitted} \iff \Delta^{\text{merge}}_A(z_i, z_j) > \epsilon_A
```

A model representing a distinction does not make it an ortheme. DYN-4, DYN-6
(orthogonality does not define an ortheme).

### D8 — cross-domain instantiation (one architecture, four substrates)

```math
\text{determinate input} \xrightarrow{\text{governing rules}} \text{appropriate determinate result}
```

instantiated in the project's comparison by OSM (task-state inference),
Fuṣḥā/Qāmūs (ṣarf/naḥw resolution),
DAEE (noetic diagnosis/route), and software (policy over material). A shared
*form*, not a shared claim: the cross-domain reading has claim role
`computational-analogy`, while project-owned objects and methods have claim role
`orthemological-extension`. Neither validates one domain by another.

## 4. Boundaries

- **Not validation.** OSM/CSCG is external exemplification and constraint. It
  constrains what a dynamic account must represent; it does not support the
  theory, its terminology, human noetics, fiṭrah, metaphysics, a Necessary
  Being, divine attributes, divine Speech, or theology
  (`OSM-CSCG-ORTHEME-CROSSWALK.yaml`, fixture DYN-8).
- **Methods stay typed.** The reported CSCG sequence is Baum–Welch
  expectation-maximization likelihood fit followed by Viterbi-training
  transition refinement; pinned official code separately supports
  max-product/backtrace MAP decode. For the reported vanilla RNNs, BPTT computes
  gradients, Adam updates parameters, and cross-entropy is the objective; Adam
  and cross-entropy occur at the reported LSTM and transformer loci, while the
  Hebbian RNN uses a distinct local timing update.
- **Outcomes stay typed.** Endpoint criterion, trajectory match, task
  performance, biological adaptation, and mechanism are separate. High
  performance without measured global orthogonalization is a neighboring valid
  control. Altered-cue/stretched-track results are bounded CA1 reuse/adaptation;
  new-state creation and observation rebinding remain alternatives and model
  response remains future work.
- **No new core primitive.** This is an application-level extension; the school-
  neutral core is unchanged.
- **Anti-reification.** $Z_A$, $\theta$, orthemes, and metaorthemes are
  modelling/analysis objects, not independently subsisting entities
  (companion note, Decision 0024).
