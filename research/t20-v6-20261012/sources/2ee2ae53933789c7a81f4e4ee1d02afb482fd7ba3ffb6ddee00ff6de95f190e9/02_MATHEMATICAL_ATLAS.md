# Mathematical atlas — existing results, interfaces and limits

This guide separates inherited mathematics, programme-specific constructions, written conditional results, original recorded kernel checks and proposed interfaces. Consult the actual statement and dependencies before reusing a theorem. The present handoff freshly verifies publication identity, not all mathematics listed here.

## 1. Typed records and graded tensors

Primary inherited locator: `theory/lineages/h-formalisation/orthing_formalisation_v1.md`, *Graded Representations, Witnessed Revision, and Inquiry Landscapes*, 8 September 2026. The supplied conversation discusses it continuously at thread1 lines 301–688; the older assessment enumerates its source-scoped results. Use the pinned current repository locator in `inventory/REPOSITORY_SOURCE_LOCATORS.json` when retrieving the original.

A declared analysis A fixes the intended roles, identities and distinctions. For a suitable role-typed vector space V, the tensor algebra is

\[
T(V)=\bigoplus_{n\ge0}V^{\otimes n}.
\]

The episode representation is of the form

\[
\rho_A(e)=\eta_A(\xi_A(e))+\iota_A(e),
\]

where the first channel encodes a finite structured record and the second selected interactions. Under the source's finiteness assumption, each represented episode has finite support and degree. This does not prove a uniform bound for all episodes, unbounded degree across the programme, or that the permitted episode image is itself a subalgebra.

The ordered factors are semantic roles, not interchangeable coordinates. An actor accepting a claim is not the same relation as evidence warranting it. A fourth-order source–witness–witness–claim relation can represent shared provenance not encoded by two separate witness–claim pairs. That is an illustrative application of the declared representation, not proof that arbitrary prose has already been correctly tensorised.

The project does not claim to have invented tensor algebra. It also rejects a privileged tensor ontology inferred from a representational convenience. Tensor order, tensor rank, dimension, record size and audit level are different quantities. A payoff tensor need not be a metric tensor, and its factor spaces need not be tangent spaces of a manifold.

## 2. Recoverability and the fibre criterion

For a representation r and target q, exact recovery by a decoder is possible precisely when q is constant on each fibre of r:

\[
r(x)=r(y)\Longrightarrow q(x)=q(y).
\]

Equivalently, q factors through r. This elementary but powerful condition appears in several lineages. Reusing it is not a new theorem each time it is renamed.

The condition can establish that a summary is inadequate: two source states receive the same representation but require different answers. It can also certify a reduction at the stated target. It does not tell us without further work which observable matters, whether the source states are genuine possibilities, or whether the chosen semantic interpretation is correct.

For a composite geometric representation, check the actual retained channel. If

\[
x=\psi_N\circ\pi_N\circ\rho_A
\]

is used alone, q must factor through x. If the full state is `(κ,x)` and κ retains exact identity, authority, evidence and history, factorisation through the pair may suffice. Do not demand that every source identifier live in smooth coordinates. Conversely, a claim inferred from geometry alone cannot quietly borrow information that only κ provides.

## 3. Higher-order interaction and contraction

The parity construction uses distributions on binary n-tuples of the form

\[
P_\pm(x)=2^{-n}\left(1\pm(-1)^{\sum_i x_i}\right).
\]

They agree on every proper marginal while differing completely on joint parity. This gives an exact information-loss counterexample: all lower-order agreement need not determine a target depending on the full interaction. It does not establish that a particular real-world argument, mind or institution necessarily has that interaction; the application still needs a map.

Marginalisation can be represented by contraction. The source also distinguishes general algebraic contraction from a semantically warranted simplification and observes the limits of a nonzero deletion functional invariant under every basis change. These facts oppose the inference “a valid contraction means no important information was lost,” not the use of contraction itself.

Witnessed degree lowering records which obligations persist, are replaced or receive a disposition. The no-disappearance invariant is conditional on record-valid transitions. It is not a proof that the original obligations were complete, every disposition was substantively correct, or an adequate historical trace preserves all information needed for future questions.

## 4. Continuation-complete inquiry

Primary locator: `theory/lineages/h-continuation/continuation_complete_orthing.md`.

In a finite reference model, let \(\mathscr V\) be the retained observable/statistic space and \(\mathscr C_h\) the space needed by the authorised horizon-h continuation contract. Exact recovery requires inclusion of the relevant continuation span in the retained span. A representation adequate for today's target can fail tomorrow's permitted action–observation question.

The manuscript relates a moment-information defect to

\[
d_{\mathscr V}(f)=\min_{g\in\mathscr V}\|f-g\|_\infty,
\]

with its stated normalisation; for a binary target the displayed defect runs from zero to one half. Preserve the distinction between the source's defect and a full interval width rather than silently changing a factor of two.

The minimum continuous predictive-memory dimension, under the finite full-law and continuity assumptions, is

\[
d_{\min}=\dim\mathscr C_h-1.
\]

The additional continuous statistics needed for exact augmentation are

\[
a_{\min}=\dim(\mathscr V+\mathscr C_h)-\dim\mathscr V.
\]

These are not automatically minimum RAM bits, runtime, number of experiments or length of a proof. Free access to an external archive changes the retained representation/access-cost model. Discontinuous encodings are not silently covered by a continuous-encoder lower bound.

The source's pairwise sign-model example has a Walsh span through degree at most h+1 and dimension

\[
\sum_{k=0}^{\min(n,h+1)}\binom nk,
\]

with the full-horizon dimension reaching \(2^n\). This is a result for the specified action model, not a universal law that every two-body interaction creates the same memory burden. Later graph-continuation work makes permitted-action structure even more explicit: combinatorial order alone need not determine which information is exposed first.

## 5. Communication, composition and decision

Three older lineages must stay connected to the current inquiry programme:

**The Last Moat, Edition 3** — `theory/lineages/h-moat-e3/the_last_moat_e3.tex`. The manuscript explicitly cites Shannon and develops admissible encoders, receiver observations, conditional mutual information, noninterference and information-cut bounds. Its information budget is of the form

\[
\mathsf I_{\mathcal R}(A\to B;T)=\sup_{\text{admissible encoders}}I(M;Y_B^{0:T}\mid Z).
\]

A receiver-side computation cannot recover new information about a message from a channel conditionally independent of it, under the model. The communication result is not a theorem that a faithfully transmitted assertion is true.

**Information, Composition, and Self-Revision** — `theory/lineages/h-ics-v5/information-composition-and-self-revision-v5.tex`. It connects local information, global relational constraints, factorisation, observational congruence and finite sure-decision strategies. A destructive-query example matters: every pair of possibilities can be distinguishable in isolation while no one adaptive strategy decides the full problem, because observing one distinction can erase another. Pairwise tests do not automatically compose into a uniformly successful procedure.

**Reflexive Revision under an Evidence Budget** — `theory/lineages/h-reflexive-v3/reflexive_revision_evidence_budget_v3.tex`. This already defines a minimum worst-case probe cost:

\[
V_g(S)=\begin{cases}
0,&|g(S)|=1,\\
\min_{h:\,|h(S)|>1}\left(c_h+\max_{a\in h(S)}V_g(S_{h,a})\right),&\text{otherwise}.
\end{cases}
\]

The source's finite-model assumptions and unavailable/empty-minimum cases matter. It proves optimality for a uniformly sound decision procedure under its exact observation/cost contract and analyses retained evidence. Its address-function example separates five adaptive queries from twenty nonadaptive queries. That is an exact example, not benchmarked performance of an actual philosophical debate system.

The decision-tree recurrence has established mathematical ancestry. The research opportunity is its accurate integration with semantic interpretation, proof obligations, source commitments and executable inquiry—not pretending optimal finite querying has just been invented.

## 6. Games and dynamics

The September formalisation contains covariant payoff tensors, mixed-strategy contractions and conditional finite Nash existence. The equilibrium theorem uses the relevant standard fixed-point ancestry. Equilibrium is not automatically truth, warrant, justice or a prediction that a human must end at one specific life outcome.

It also contains conditional continuous/discrete dynamics, coupled-energy estimates, damping and invariant error bounds. A bound on a declared trajectory is different from a proof that the trajectory exists indefinitely or that the inquiry is epistemically improved. These contributions are not a Navier–Stokes result.

General vector fields are not automatically gradients. The historical inquiry landscape `L_t` is not automatically a scalar loss or the owner's project Lagrangian. Use a separate J when specifying a potential. A discovered obligation may enlarge a burden ledger while improving the inquiry, so raw burden count is not a universal correction objective.

## 7. The existing Hessian/Bregman research

Current pinned primary sources were directly inspected during this review:

- `docs/provenance/v5-research-continuations/notes/1a5d94a8d7a2bca031de09dafcb3fc929797b94488d10836ddb696b0e6a1be0d.md` — common endpoint repair versus infinitesimal nudging;
- `docs/provenance/v5-research-continuations/notes/71156aa5eb3f520e004fd15b3c8eb5a994bbf87c9735c00e0ea9c921f409e10e.md` — exact kernel-verification scope;
- `experiments/orthemology-v5-continuations/source-store/50968a1703261df4e2794636cbdddca8e0e1a5867854a27e543bc83b0a9afc46.lean` — actual `NudgeRigidity.lean` source, including the canonical gain proof and universal theorem setup.

For a finite categorical outcome space and an additive score potential

\[
F(b)=\sum_i f_i(b_i),\qquad f_i''(b_i)>0,
\]

the canonical direction at an interior, incoherent b is

\[
d_i(b)=\frac{1-\sum_k b_k}{f_i''(b_i)}.
\]

The actual Bregman state-loss derivative obeys

\[
\nabla_bD_F(e_j,b)\cdot d(b)=-\left(\sum_i b_i-1\right)^2
\]

for every truth vertex j under the declared Score assumptions. This is genuine infinitesimal common improvement, not route-ranking metaphor.

The universal nudge classification concerns **two fixed coordinate-additive generator families**, at least three genuine categorical outcomes, every coherent interior context, and arbitrarily small positive perturbations along the specified coordinate direction. Under those quantifiers, common local nudges, positive-scale/coordinate-affine equivalence, and the relevant universal common-endpoint-repair condition coincide. A separate wrapper treats directions towards coherent endpoints.

**Do not drop the quantifiers.** A pointwise common improving direction can exist without a common dominating coherent endpoint. The source preserves an exact separator. The result is not a theorem for arbitrary truth polytopes, changing generators across contexts or higher-dimensional normal spaces. Konek's prior common-improvement work is explicitly credited; the proof is not a theorem-priority certificate.

The wider spine includes LocalRigidity, RepairObstruction, SmoothScalar, SmoothRigidity, GeneratorRigidity, BregmanProjection, SmoothRobustness, finite-hull necessity/approximate-iff and intrinsic-barycentric interfaces. The original receipts identify Lean 4.19.0, pinned Mathlib and standard axioms. Some full dependency-block classification and quantitative claims remain ordinary proof only. All philosophical and normative interpretations remain outside kernel certification.

### Riemannian interpretation: an explicit deduction, not an invented repo status

Take the **ambient open cube**, not the already-normalised simplex, and define

\[
E(b)=\tfrac12(\sum_i b_i-1)^2,\qquad
g_b(u,v)=\sum_i f_i''(b_i)u_iv_i.
\]

With sufficient metric smoothness,

\[
-\operatorname{grad}_gE(b)=d(b).
\]

For a local solution of the declared flow,

\[
\dot b=-\operatorname{grad}_gE(b),\quad
\frac{dE}{dt}=-(\sum_i b_i-1)^2\sum_i\frac1{f_i''(b_i)}.
\]

This is an ordinary mathematical interpretation of the existing nudge. It supplies a literal gradient model in a restricted case; it is not proof that Orthemology already publishes one universally governing noetic flow. On the coherent simplex itself E is identically zero, so using that as the ambient domain for an incoherence-repair flow would miss the point. Original positive-C²/continuous-Hessian hypotheses must not silently become all standard smooth-flow existence/uniqueness hypotheses. Neither boundary avoidance, global convergence nor truth/warrant of the corrected credences follows from this identity alone.

## 8. T20 causal reconstruction trajectory

The mathematical line grew from a philosophical production question into independent identification research:

```text
loss of productive-route distinctions → exact reconstruction panels
→ declared whole-route Bernoulli forward model → noisy/bounded recovery
→ restricted measurement lower bounds → persistent/grouped observations
→ countable-index and information-frontier investigations
```

Exact identifiability under rational observations is not physical availability of interventions. A valid route-count bound and calibration contract do substantive work. Polynomial sample cost can still be enormous. A lower bound for one measurement family does not rule out every other method. Countably indexed inputs do not imply that arbitrary infinitely complex systems are identified by finitely many measurements.

Single-trial mixtures can conceal differences that paired observations under one persistent hidden arrangement reveal. Associative aggregation can still double-count overlapping provenance. A record's extensionally correct output is not a warrant for its original productive history. These are useful connections to the older higher-order and continuation mathematics; the strength of an application depends on its exact map, not thematic resemblance.

CP08's Boolean-semiring tensor work provides a finite logical transport preserving conjunction, existential projection and shared-variable identity in its declared model. It does not turn arbitrary unapproved natural-language interpretations into mechanically verified premises. See the checkpoint catalogue for the exact RESULT and reviews.

## 9. Warranted completion and residual-certificate frontiers

Current public locators: S01 and CP23 `warranted-discrimination-research-20261009/RESULT.md`, with separately scoped kernel source under `warranted-discrimination-kernel-20261009/`.

Fix a finite evidence-token set E, accessible authenticated inventory K, finite admitted certificate catalogue Γ, scoped verdicts v, certificate support \(S_\pi\) and terminal checking price \(\kappa_\pi\). Authentication and catalogue admission implement declared identity/rule conditions; they are not unrestricted truth or interpretation oracles.

For each verdict retain undominated pairs

\[
R_v(K)=\min_{\subseteq,\le}\{(S_\pi\setminus K,\kappa_\pi):v_\pi=v\}.
\]

The frontier determines the least terminal certificate cost after every additional evidence set U. Equality of frontiers is necessary as well as sufficient when all the stated single-token acquisition continuations are actually available. Residualisation updates exactly by `D → D\T` and deleting dominated pairs. For a narrower real inquiry menu, this full frontier can be sufficient but finer than necessary.

One proof needing n distinct tokens produces \(2^n\) distinguishable future-completion profiles even though present proof availability is only one bit. This counts continuation-control states under the specified retained-information model, not unavoidable physical RAM when an external archive can be queried for free.

For finite, persistent, order-independent, one-use tests with scenario set B and remaining menu Q, the written inquiry theorem uses

\[
D(K,B,Q)=\min\{t_G(K),\min_{a\in Q}[c_a+\max_oD(K\cup\tau(a,o),B(a,o),Q\setminus\{a\})]\}.
\]

It charges acquisition and final certificate checking. Another test can be cheaper than stopping even when a certificate is already available. Offline catalogue compilation and policy-search costs are not included. Guaranteed completion requires every feasible full transcript to supply support for some substantive-goal certificate. An always-available “unresolved” label does not count as success unless that bounded diagnosis is the actual task.

The frontier theorem's recorded Lean verification and the broader written/finite-tested Bellman result must remain separate. The abstract frontier need not retain a concrete proof object's identity. Evidence/proof retrieval and real authentication costs must be represented rather than treated as magic free reconstruction.

## 10. From catalogue assumptions to actual proof compilation

CP23 exposes the question of obtaining a catalogue from the rules. CP24 and the later supplements extend the mathematics to source-sensitive guards and finite proof grammars, then prove minimum attainment, numeric saturation and executable witness correspondence at their respective scopes.

The important refinements are exact judgement-plus-support states, ordered guard-sensitive substitution and nonnegative occurrence prices. Cyclic syntax need not require unbounded representatives in the declared finite grammar: pruning and support-aware bounds can establish finite-height attainment. The bound cannot simply ignore source support, and local Pareto pruning can destroy future guard eligibility or global shared-cost opportunities.

The later executable table and witness work should no longer be described merely as an uncompiled proposal. Its evidence remains original component-specific kernel and runtime records, not a fresh Lean replay by this review. Eager proof enumeration may be huge; stable minimum prices do not imply stable, canonical or smallest-node witnesses.

Finally, once-per-node DAG costs are not occurrence-priced tree costs. The newest shared-cost work gives written Set Cover reductions and finite controls, separates exact-support state expansion from sharing, and shows individual/pairwise overlap summaries can miss joint paid-node cost. Aligned globally compatible node identities can recover a weighted union cost; a label match alone does not establish compatible acyclic sharing.

See `06_POST_CP23_FRONTIER.md` for the exact progression. Do not promote a proof-tree theorem into a DAG optimiser, a semantic truth oracle, an empirically validated investigation policy, or a universal natural-language refutation procedure.
