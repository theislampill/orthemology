# Related work — sequential latent-variable inference under ambiguous observations

**Status:** bounded related-work note (Decision 0015). Analytic; **no empirical claim is made by this project**, and nothing here is validation of orthemology. Notation follows `docs/notation-registry.yaml`; verdicts follow `docs/verdict-registry.yaml`. Bibliography: `references/orthemology.bib` (the R4 independent review merged the former `latent-state-additions.bib` fragment into the main database and retired it, so no bibliography surface escapes CI resolution); per-claim source status: rows LAT-1..LAT-3 in `references/source-status.yaml`.

**Inference-boundary legend** (as in `companion/CONCRETE-AND-SOUND-REASON.md` §1 and the R3 sourcing ledger): **[direct-source]** (reported from a named source), **[secondary-reconstruction]**, **[synthesis]** (across sources), **[orthemological extension]** (this project's own mapping). Every substantive claim below carries a tag.

## 1. What the neighbouring literature is

A family of models treats behaviour and neural activity as **sequential latent-variable inference under ambiguous observations**: a system receives observations that do not uniquely determine the underlying situation, maintains a distribution or candidate set over hidden states, and disambiguates using sequence and context. We use that neutral phrasing throughout, in preference to any of the field's theory-laden labels.

Three sources are in view:

- **Sun et al. 2025**, "Learning produces an orthogonalized state machine in the hippocampus," *Nature* 640(8057):165–175, doi:10.1038/s41586-024-08548-w (open access, CC BY 4.0; PMC11964937). **[direct-source]**
- **George et al. 2021**, "Clone-structured graph representations enable flexible learning and vicarious evaluation of cognitive maps," *Nature Communications* 12:2392, doi:10.1038/s41467-021-22559-5. **[direct-source]**
- **Vasudeva Raju et al. 2024**, "Space is a latent sequence: A theory of the hippocampus," *Science Advances* 10(31):eadm8470, doi:10.1126/sciadv.adm8470. **[direct-source]**

**Model object.** The clone-structured graph (CSCG) is a hidden Markov model variant in which multiple "clone" hidden states share a single deterministic emitted observation — in the 2025 study, 100 clones per symbol, with transitions learned by Baum–Welch EM. This is the observational-aliasing mechanism: identical observations, distinguishable hidden states, disambiguated by history. **[direct-source]** The 2021 paper expands CSCG as clone-structured *cognitive* graph; the 2024/2025 literature uses clone-structured *causal* graph. **[direct-source]**

**What the 2025 study reports.** Eleven mice; dorsal CA1; two-photon calcium imaging; roughly 3,954 neurons per animal tracked across weeks. The task is a **visual** virtual-reality two-alternative cue-delay-choice (2ACDC) task with an indicator cue, a 2-second dark delay, and near/far reward zones. **There is no odour component.** Four sensorily identical grey track regions were moderately correlated in session 1 and significantly decorrelated by session 3; population structure under UMAP progresses unstructured → hub-and-spoke → ring → split-shank ring. **[direct-source]**

**Model comparison as reported.** Vanilla RNNs (ReLU/sigmoid), LSTMs, and transformers reached high next-input prediction accuracy **without** developing globally orthogonalized representations; the paper's stated reason is that task performance requires orthogonality only within the low-dimensional task-relevant readout subspace. **Nuance:** RNNs with softmax activation *did* produce fully orthogonalized representations when fully trained. **[direct-source]**

**Trajectory result.** The animals showed an **ordered** decorrelation sequence (off-diagonal → pre-R2 → pre-R1). Among the compared models, only CSCG reproduced that trajectory; vanilla and Hebbian RNNs reached a decorrelated endpoint by different sequences (the Hebbian RNN matching the endpoint with non-monotonic dynamics). The paper treats trajectory as the more stringent constraint. This is **unique among the compared models under the reported evaluation** — never a universal uniqueness claim. **[direct-source]**

**Single-unit picture.** Single cells are described as a **continuum** of place/splitter responses with plastic tuning, with neurons changing functional role across learning; the authors caution against rigid cell-type readings. **[direct-source]**

## 2. Mapping table

Each row states how the paper/model object is **treated** in this framework. The right column is this project's own typing; it is not a claim about the papers.

| Paper / model object | Orthemological treatment | Legend |
|---|---|---|
| the concrete situation at time `t` | orthemma `m_t ∈ M_A` — a concrete, situated, time-indexed occurrence | [orthemological extension] |
| hidden task/world state `z_t` (clone, HMM state) | **optional, model-specific latent-state abstraction declared inside `A`**; `z_t ∈ Z_A` with `P_A(z′∣z,a)`; non-primitive | [orthemological extension] |
| sensory observation `x_t` | `x_t = Ω_A(m_t)`, or the emission `P_A(x ∣ z)` on the model side | [orthemological extension] |
| posterior / set of consistent hidden states | typed **latent candidate set** `C^latent_t ⊆ Z_A` and/or belief `b_t(z)` — never ground truth | [orthemological extension] |
| neural or model hidden representation `y_t` (population vector, hidden layer) | **concrete internal representation** — a concrete token with a geometry, not a type and not a profile | [orthemological extension] |
| "the state the animal/model is in," as an evaluable fact | `O*(m_t; A)` — the true profile under the declared analysis; locally, the inferred **partial** profile `p̂_t(m) ∈ Π_A^∂` | [orthemological extension] |
| decorrelation / orthogonalization of representations | a geometric property of `y`, evidence about a representation only | [synthesis] |
| clone-per-symbol aliasing | the model-side mechanism corresponding to a non-injective `Ω_A` | [synthesis] |

**Rule (Decision 0015 §1):** `m ≠ z ≠ x ≠ b ≠ y ≠ p̂`. These are six distinct object kinds; substituting one for another is a typing error, not a shorthand. The bridge `ProfileOf_A ⊆ Z_A × Π_A` is partial and not one-to-one, so no row above licenses reading any other row off it. **[orthemological extension]**

## 3. Endpoint vs trajectory — a concrete neighbouring illustration

The reported result that several model families reach a decorrelated **endpoint** while only one reproduces the observed **trajectory** is a clean external illustration of a distinction this project already draws for its own reasons: the separation of **result** from **pathway** (Decision 0003 / O2). **[synthesis]**

Two statements, kept apart:

- **Endpoint agreement does not establish mechanism agreement.** Matching a final representational geometry is compatible with arriving by a materially different process. In this framework's own terms, a correct result is not a pathway-adequacy finding, and pathway adequacy is not inferred from correctness. **[orthemological extension]**
- **Trajectory carries discriminating evidence that endpoint tests lack.** An ordered sequence of intermediate states is a strictly stronger constraint than the terminal state: models indistinguishable at the endpoint separate on the path. This is the same reason the framework audits episodes and not only outputs. **[orthemological extension]**

The illustration is **neighbouring**, not evidential: it shows that the result/pathway distinction has purchase in an unrelated empirical setting. It does not confirm any orthemological claim, and no orthemological claim depends on it. **[orthemological extension]**

## 4. Scope limits — what this note does NOT claim

- **Empirical scope of the primary study:** 11 mice; one dorsal-CA1 visual VR task; model-supported proposals; the authors' own listed limitations — upstream plasticity may contribute and CA1 may inherit orthogonalization from CA3; the RNN models are abstractions of CA3, not circuit models; the learning rule is uncertain and CSCG is a **leading, not settled** model. Their stated future work includes whether reward is necessary versus sensory prediction alone, replay, hippocampal–neocortical interaction, and flexibility under task alterations. **[direct-source]**
- **No validation.** This literature does **not** validate orthemology, its ontology, its verdict registry, or any of its decisions. The direction of use is one-way: the framework supplies a typing discipline for reading such work; the work supplies no support for the framework. **[orthemological extension]**
- **No transfer.** There is **no conceptual and no empirical transfer** from this material to: human rational faculties; fiṭrah; the concrete-vs-sound-reason distinction; metaphysical orthability; a Necessary Being; or divine attributes and divine Speech. Claims in those areas rest on their own sources and stand or fall independently. **[orthemological extension]**
- **This is NOT etymological validation of the word "ortheme."** The appearance of "orthogonalized" in a paper title is a coincidence of vocabulary about vector geometry; it bears no relation to the term "ortheme," supplies no etymological support, and must never be cited as though it did. **[orthemological extension]**
- **No biological or procedural claim** is made or extended here; no experimental procedure is described beyond what is needed to bound the scope of the cited result.
- **No neural localization.** Per Decision 0015 §7: no "ortheme cells," no one-neuron-one-type reading, no claim that any orthemological object is realized at any anatomical locus. The continuum/plastic-tuning finding is precisely why. **[synthesis]**

## 5. The bounded claim

Stated in full, the corpus's claim from these papers is: *there exists an active, independently motivated empirical and modeling literature on sequential latent-variable inference under ambiguous observations, in which observation, latent state, belief, internal representation, and evaluable ground truth are handled as distinct objects; that literature furnishes a neighbouring illustration of the result/pathway distinction; and it supplies no evidential support for any orthemological thesis.* Nothing beyond this sentence is licensed. **[orthemological extension]**
