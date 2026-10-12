# Cross-lane adversarial synthesis review

Date: 2026-09-30. Review basis: Orthemology commit `03e2604dfcef278b01c60d19b05370fcec4194b6`, with the separate research returns described below. This is an intermediate, independent mathematical/philosophical review. It does not close the wider research programme, discharge its time requirement, alter owner statuses, or add kernel credit.

## Findings first

1. **One material implementation overreach was found and repaired before the control seal.** A finite randomized controller realization can pre-sample future action coins into private memory. If the destination adversary can inspect that memory while the source adversary cannot, equality of the unexposed controller laws does not justify the `|Z|M` / `|Q||R|M` memory-bound upgrade. An explicit finite prediction game changes restoration probability from one to zero under that exposure. The behavioral fresh-current-action coupling theorem itself survives. The final control archive contains the restricted statements and an explicit correction record.
2. **The Köpf–Basin iteration discrepancy survives primary-source and hypothesis checks.** The literal old-partition operator, initialized at the full block, takes three strict rounds on two states and five on three states. A new genuinely nondeterministic, input-enabled four-state control also takes five. Removing one preprocessing round, changing the queried initial state, or insisting on genuine nondeterminism does not rescue the paper's literal `|S|` bound. The sharp `2m−1` claim remains local to this independently quantified operator and its partial-equivalence lattice. It is not a blanket discovery, priority, or failure-of-the-paper claim.
3. **No further contradiction was found in the core claims at their stated scopes.** D1/D2, the adapted Hall/violation threshold, HS1, the fresh-draw SR1 proof, AR2's countable-episode argument, private/public composition, the displayed stationary-accuracy family, finite-polyhedral scalarisation, exact rational sign-cell disclosure, weighted-quadratic coherence and local logarithmic-score characterisation survived the attacks recorded below.
4. **The philosophical result is a genuine conditional advance, not a source ascent.** The accuracy premises do derive a nontrivial coherence constraint; stronger scoring premises do fix a comparison-equivalent score family. Neither supplies constitutive hosting at an ultimate bearer. Conversely, a formal rival expansion is not thereby a metaphysically adequate impersonal explanation. The current synthesis appropriately preserves both limits.

### Reviewed final identities

- Control archive: `disturbed-restoration/Control_Restoration_Research_Return.zip`
- Control SHA-256: `1cf3325433b10ea66099570adeb9b3e2e55e4015ecd9609025519e919bd3b721`
- Independently reopened: 73 members; CRC check clean; corrected SR1, SR2, interface map and correction record byte-identical to the reviewed working files
- Source/intentionality archive and all inspected input identities are recorded in `REVIEWED_INPUTS.json`
- Canonical sources and both sealed returns were not edited by this review

The earlier extensive Lean/native build audits were not rerun. This review concentrates on ordinary proofs, interface quantifiers, fresh finite controls and primary literature. Existing author test counts are not represented as new reviewer test runs.

## F1. Randomized realization and adversarial memory exposure

**Severity:** material implementation boundary; corrected in the final control seal. **Not a refutation of SR1's behavioral theorem.**

### Exact affected claim

`disturbed-restoration/stochastic_refinement.md`, §4, line 75, formerly gave a finite-memory product bound for an M-state realization without sufficiently restricting how that realization's internal randomness becomes visible. Its §5 adversarial paragraph, now line 107, allows the destination adversary to see the controller's memory. `private_interface_composition.md`, §3, line 103 carried the corresponding composite bound.

The source policy in SR1 is a behavioral kernel on source observation/action histories. Current actions are sampled freshly after that history is fixed. The source disturbance may depend on the full source state/action history. These premises do not automatically cover a different realization whose private state contains future action randomness that a destination disturbance can inspect.

### Concrete finite countermodel

The physical plant has four states: prediction phase `P`, locked-prediction phases `Q0,Q1`, and an absorbing good state `G`. Only `G` is target. Observations distinguish `P`, `Q`, `G`, but hide the bit in `Qh`. All actions are safe and licensed.

A finite controller has private bit `r`, fair initially and refreshed independently at each return to `P`.

1. At `P`, the controller executes `wait`
2. The disturbance chooses prediction `h`, moving to `Qh`
3. At `Qh`, the controller responds `r`; the transition goes to `G` if `r≠h`, and otherwise returns to `P` and refreshes `r`
4. The response transition has a singleton disturbance menu, so the earlier prediction cannot be revised after seeing the response

For every nonanticipating source adversary blind to the current private bit, `r` is conditionally fair at each prediction phase, even given the full plant/action past. Conditional failure per round is exactly `1/2`. Failure through n rounds has probability `2^-n`, and reaching `G` is almost sure.

A destination adversary exposed to controller memory selects `h=r`. It keeps the system outside `G` forever with probability one. Physical kernels, observations, licenses and labels can be identical on the two sides. Identity plant couplings do not repair the leaked future randomness.

The narrower behavioral implementation samples `r` freshly at `Q`, after the prediction is locked. No future coin exists in memory at `P`, so it retains almost-sure success even against the permitted memory-visible adversary.

**Executable evidence:** `private_coin_exposure_countermodel.py` constructs the finite controller-product Markov chains. Both blind constant predictors have the sole reachable bottom SCC `{G}`. The exposed copying predictor has a closed four-state bad SCC. Exact finite laws give `2^-n` versus `1` survival through 12 rounds. The all-history blind-adversary assertion has the separate conditional-fairness proof above; enumerating two constant predictors is not offered as proof of that universal assertion.

### Verified repair

The sealed §4 now requires fixed initial memory, deterministic history updates, and fresh current-action draws for the M-state bound. Other randomized-memory realizations require an exposure-compatible behavioral-kernel proof. SR2 repeats the restriction. `INTERFACE_MAP.json` and `REVIEW_CORRECTIONS.md` also record it.

This is sufficient: deterministic source memory is already determined by source observation/action history, and interface-private state does not reveal future action draws. The marginal source action distribution therefore remains σ under the joint-history construction. The finite interface checker still does not certify an arbitrary controller realization. That remains an explicit external obligation.

## Control-lane proof attacks and surviving ceilings

### C1. Hidden histories, finite-memory existence and bounded visits

**Anchors:** `research.md:93–145`, H1/H2 in §§1–3, and H3 at `research.md:285–304`.

The max-vector update stores the greatest bad-visit count among actual finite hidden witnesses ending at each current state. The next-step maximum extends one such witness by a declared edge; it does not combine mutually inconsistent histories. Safety and authority are checked on the complete support, not on a convenient witness. The fixed-bound safety reduction is sound, including the initial-state visit.

I attacked the existence equivalence with H3's increasing b-block policy. It is sure winning but has no uniform bad-count bound. This does not contradict D2: the same plant has the distinct `a^ω` bounded winner. The theorem explicitly quantifies over existence of a strategy, not over every accepted strategy. H1 separately blocks a deterministic last-bad-time conclusion.

The universal hidden-history objective is ω-regular over public action/observation words: the existential bad-history language is recognized by a finite nondeterministic Büchi automaton, then determinized and complemented. Its product with exact belief/custody information supplies a finite perfect-information parity game. That is the right use of positional determinacy. A coBüchi label on beliefs is not a substitute.

The bounded solver implements D1 only. A failed k-instance is not a proof of no sure winner without the actual global cutoff/determinization construction. No unrestricted almost-sure synthesis result follows. The primary bounded-synthesis paper explicitly separates finite-state annotations and deterministic-parity existence bounds: [Schewe–Finkbeiner, §§3.2–3.3](https://intranet.csc.liv.ac.uk/~sven/atva07b.pdf). The unrestricted/finite-memory POMDP boundary is also confirmed in [Chatterjee–Chmelík–Tracol, Theorem 1 and §3](https://arxiv.org/pdf/1309.2802).

### C2. Hall, incentives and adapted events

**Anchors:** `correlated_restoration.md`, §§1–4; especially lines 43–98 and 100–152.

CR1's residual completion is valid: a positive residual row and column joined by an allowed edge would augment the maximum supported subflow. Thus the unrestricted weighted Hall deficit is attained. Hard-license and incentive constraints can destroy that completion, so δ is only a lower bound for δ*.

The conditional Borel–Cantelli proof uses the correct predictable denominator `1+A_(t+1)` because `p_t` is measurable before the sampled violation. Its square-variation bound follows from the decreasing integrand; convergence plus Kronecker on divergent compensator paths and summation by parts on finite ones gives the advertised event equality.

The strongest filtration attack is the fixed hidden bad bit with public conditional probability `1/2` forever. Infinite physical badness then has probability `1/2`, not one. It does not satisfy adaptation to that public filtration. The report includes precisely this guard. Enlarging the filtration requires recomputing conditional hazards; one cannot preserve the half-probabilities after revealing the bit.

**Integration ceiling:** a Hall deficit for `Good_k` obstructs that prescribed-marginal fixed-k public certificate. It does not establish physical coBüchi impossibility, failure of every k, or absence of another policy. The deterministic-schedule iff relies on actual implementability of the selected coupling. Endogenous future contexts need policy-level analysis.

**Further application guard:** the displayed correlated-equilibrium inequalities are the static recommendation-obedience contract. A later application giving players additional current private signals, sequential access to others' actions, or a different deviation menu must condition incentive constraints on that information. The present research does not purport to solve those richer games. Likewise, a history-dependent feasible-polytope process must be predictable/measurable; in the finite-history setting this is straightforward, but not a reason to ignore the requirement in a continuous extension.

### C3. Hidden-standard learning and accuracy

**Anchors:** `hidden_standard_learning.md`, §§1–6; `memory_accuracy_boundary.md`, §§2–4; `switching_innovation_threshold.md`.

HS1's finite-memory impossibility is a common-support bottom-SCC argument over a **fixed finite time-homogeneous controller**. I tried to promote it to zero restoration probability for every finite controller. A four-sample commit controller defeats that promotion: under the plus hypothesis, tie-to-minus commitment restores with probability `16/27`, although not one. This agrees with the original statement and its limit-sure approximation clause.

The unbounded majority policy uses summable exponential errors and therefore legitimately proves eventual permanent correctness. Equal one-step support does not preserve its qualitative outcome under changed probabilities; the support theorem is only for already compiled finite homogeneous controllers. Zero-error finite stopping is ruled out by mutual absolute continuity on finite histories, not by an inability to learn asymptotically.

I checked the apparent conflict with recent MEMDP results against the primary theorem. [ICALP 2025, Theorem 4 and definitions](https://drops.dagstuhl.de/storage/00lipics/lipics-vol334-icalp2025/html/LIPIcs.ICALP.2025.150/LIPIcs.ICALP.2025.150.html) uses one objective over a shared observed state space. HS1's acceptance depends on the unobserved fixed environment, so it is outside that theorem. Exposing the hidden standard or changing to a common target changes the problem.

The sticky-walk stationary weights and Bayes-error formula are correct. For each positive ε, the wrong endpoint is recurrent under each hypothesis, making restoration probability zero despite arbitrarily small stationary error. Setting ε to zero changes communicating classes, so the noncommuting limits are genuine. This does not prove a universal optimality theorem across machines; that remains credited to the cited literature.

**Minor editorial issue only:** `memory_accuracy_boundary.md:30` states the first-edge downward probability as `1−p`, which applies for S≥3. At S=2 the sole edge's downward probability is `ε(1−p)`; the ratio is still r, so the displayed stationary formula and probes remain correct. A future revision can say “for S≥3” in that edge-by-edge derivation and handle S=2 directly. No seal reopening is necessary for the mathematical claims.

SW1's fresh innovation law is conditioned after the controller selects its current action. This prevents the policy from predicting a supposedly fresh innovation through shared randomness. Copying one earlier innovation violates that premise and correctly defeats a marginal-only nonsummability argument.

### C4. Stochastic gluing, recovery and composition

**Anchors:** `stochastic_refinement.md`, §§2–5; `regenerative_refinement.md:23–84`; `private_interface_composition.md:5–105`.

Apart from F1's repaired realization upgrade, the gluing proof is sound. Full initial and step marginals prevent favorable-path normalization. The action kernel agrees on matched source histories. Marginalizing a destination-dependent choice of source kernel produces a randomized **full-source-history** disturbance. Replacing that source adversary class by a public-history-only one is not licensed.

A random existential source state is proof data, not a destination observation. I checked that the controller formula never calls the coupling witness to choose its action. Source-menu conformance must hold counterfactually at every reachable interface history; it is not certified by the local transportation checker.

AR1 correctly budgets **occupancy mismatch**, not departures. The absorbing-fault example has at most one departure but restoration probability only `1/2`. AR2 then supplies the missing detection, recovery and complete reentry-law/memory premises.

The dangerous “condition at the last fault” argument is not used. For each candidate episode and entry history, the proof extends the source law autonomously after a flag. It bounds the joint event “this episode never flags and the destination is bad infinitely often” inside an unconditioned legal law. A countable union identifies the eventual final episode. Thus no claim that the last fault is a stopping time or that no-future-fault conditioning preserves source laws is required.

The ordinary proof is delivered for the inherited discrete finite-alphabet history model, allowing unbounded history memory. An extension with arbitrary continuous random recovery memory should use regular conditional kernels/integration, rather than claim that all memory-bearing histories are countable. This is an extension boundary, not a counterexample in the stated finite setting.

SR2's glued law uses the **same** middle marginal and the same successor witness in both relations. The product private mode computes both reconstructed observations without reading the hidden middle state. Its public projection is the C-side projection only; intermediate virtual actions do not become public warrant. Readout relations beyond the bad/safe labels are rightly left for a separate same-witness composition proof.

## Epistemic/normative proof attacks and surviving ceilings

### E1. Finite Pareto scalarisation is genuinely positive

**Anchors:** `disturbed-restoration/P14/research.md`, ET05-A/B/C; `source-intentionality/team_concavity_boundary.md`.

The strictly positive scalarisation converse uses a finitely generated **closed** cone of unilateral gains. If it met the nonnegative simplex, rescaling would yield a dominating feasible mixed deviation. Strong separation from the compact simplex yields strictly positive weights supporting the selected efficient profile. Player-specific and profile-dependent weights are sufficient; one canonical weight vector is not claimed.

The finite/polyhedral premise does real work. A compact convex curved frontier can have an efficient point supported only by a boundary weight. The report gives exactly such a deletion example. Thus the result cannot be exported to arbitrary continuous policy spaces, and finite primitive action alphabets do not make temporal policy spaces finite.

The team-concavity result is also correct on the full independent product of simplices: midpoint comparisons on both diagonals force each conditional mixed difference to vanish; telescoping then yields additive separability. A coupled feasible subset or a joint-law simplex is different geometry. These qualifications prevent a spurious “concavity solves interacting team convergence” import.

### E2. P15 and rational-polytope certificates

**Anchors:** `source-intentionality/P15/research.md:27–61,100–145`; `polytope-successor/research.md:7–47,65–95`; `polytope_disclosure.py`.

I tried the principal boundary attacks: endpoint-only evaluation, strict inequalities with zero optimum slack, lower-dimensional ties, constant atoms, very small rational margins, empty domains, and a verifier accidentally relying on the producer's search. The sign-cell theorem and three certificate alternatives address all of them.

The independent control uses the plane `w1=w2`, a zero atom, and a positive constant atom of margin `10^-18`. All nine sign patterns are covered and the target is invariant true. The already produced certificate still verifies with both search procedures replaced by exceptions. This is fresh narrow evidence, not a replay of the existing 423-instance suite.

The rational certificate completeness proof is sound for bounded rational polyhedra, including lower-dimensional ones: feasible compact polytopes have rational extreme points; zero-slack optima admit exact dual bounds; empty closures admit Farkas contradictions. Finite conic Carathéodory reduction supports the explicitly inefficient enumeration. The current three-variable grammar's raw-coordinate construction does not introduce hidden coefficient-growth beyond the stated bit-bound argument.

A certificate binds the supplied syntax and input identity. It does not certify that the descriptive/mixed partition is correctly interpreted, that the admissibility class is exhaustive, or that a formally permitted model is metaphysically possible. Empty-domain status must remain operationally distinct from invariant truth. The source interface preserves these ceilings.

### E3. Accuracy coherence, robust repair and local log scores

**Anchors:** `accuracy-bridge/research.md:15–109,125–150`; `accuracy-bridge/observed_outcome_score_uniqueness.md:7–38`.

A1's projection inequality is correct for a finite nonempty allowed truth-state space and strictly positive quadratic weights. A2's expectation argument needs only one probability distribution representing the coherent point; it does not need full support or a uniquely identified true probability. Therefore the per-score undominated region really is the coherence polytope. The anti-dominance norm and availability are additional normative/practical premises, not concealed definitions of coherence.

The two-standard repair obstruction is exact. My independent calculation gives the reported minima `63/400` and `97/400`; these force incompatible bounds `t>3/5` and `t<1/2`. The narrow interval `[9/20,11/20]` with `(11/20,9/20)` has minimum gain `3/500`. Randomized common repair cannot escape because its coherent mean is no worse by Jensen. Thus `∀w∃c` does not become `∃c∀w`, while positive common repair remains possible under suitably bounded uncertainty.

A4's first-order proof is sound on the relative interior of the **full** simplex with at least three outcomes. A spare coordinate links arbitrary component probabilities, forcing `t f_i'(t)` to be one common constant. Strict propriety fixes its positive sign. The binary exception, boundary behavior and report-independent outcome law are all essential and explicitly retained. The primary source confirms precisely this realized-coordinate locality statement, distinct from general neighborhood locality: [Dawid–Lauritzen–Parry, §3.2](https://arxiv.org/pdf/1104.2224).

The resulting equivalence is for rankings of reports at a fixed realized outcome or under one fixed p. Outcome-only constants do not order arbitrary different-outcome cases identically. A4 already states this restriction. It assumes coherent probability reports; it cannot be substituted for A1's derivation of coherence from unconstrained credences.

### E4. Source, hosting and agency: argument versus countermodel

**Anchors:** `intentional_hosting_and_source_ascent.md:78–132,153–181`; `truth_at_world_and_hosting_addendum.md:9–32,58–79`; `source_ascent_integration.md:9–57`; `SOURCE_ASCENT_RESEARCH_INTERFACE.json`.

The necessary-particular/essential-host conditional is valid. It needs the **same rigid particular** to exist throughout the modal range and essentially belong to the same bearer. A necessarily true proposition, a necessary type, or a type tokened by different contingent bearers does not supply that premise. Grounding the actual host is not itself hosting its thought.

The primary Anderson–Welty paper explicitly addresses changing contingent hosts through essential ownership in footnote 31. The synthesis correctly acknowledges that response instead of attributing an elementary unnoticed quantifier mistake to it. The live dispute concerns proposition ontology, the truth-at-world/existence bridge and applicability of token ownership. [Anderson–Welty, §§8–9, n.31](https://www.proginosko.com/docs/The_Lord_of_Non-Contradiction.pdf)

The Speaks rival is a substantive semantic proposal retaining Serious Actualism and contingency, not merely an arbitrary false flag. Its distinction between evaluation with respect to a world and local property possession supports the stated burden challenge. It does not prove the metaphysical possibility of a mindless world or establish its adequacy as an explanation. [Speaks, §§1–2 and later semantic development](https://www3.nd.edu/~jspeaks/papers/2012nonexistentprops.pdf)

The strengthened actual-existence PSR genuinely derives necessity from actual underivedness. It pays for that derivation with a stronger explanatory premise; it does not discharge the original weaker owner's burden. Possible grounding plus actual underivedness is insufficient, as the rotating-root models show. Neither modal conditional supplies intellect or the identity of the ultimate ground.

The B8 warning is balanced: under a defended theory identifying genuine original understanding with a subject's activity, conceding such understanding while denying all subjecthood can be incoherent. Minimal subjecthood still does not establish practical agency, de se integration, unrestricted knowledge, Wisdom or revealed identity. These are philosophical and constitutive questions. The finite structures do not adjudicate them.

The JSON and integration note preserve these distinctions. No inference from mathematical scoring locality to ontological bearer locality, from a truth-frequency law to normative authority, or from a narrowed source-relative class to authenticated source truth was found.

## F2. Köpf–Basin: exact literature ceiling

**Reviewed primary source:** [author-hosted ESORICS manuscript](https://boriskoepf.de/papers/esorics06.pdf), Definition 1; §3.2 Definition 5 and Φ; Theorem 3; Corollary 2 proof; Appendix A. PDF text extraction gives pages 3, 10–11, 19–20 in one-based PDF numbering. A requested screenshot was unavailable, so this review does not claim a new visual/typesetting or publisher-version collation.

The machine model is finite, input-enabled, synchronous and permits nondeterminism. Universal input equivalence and equality output equivalence are valid equivalence relations. The displayed Φ computes the new relation from the old classes and excluded set. Theorem 3 initializes with `{S},∅`; the Corollary 2 proof asserts at most `|S|` applications.

### Attempts to rescue the numerical claim

- **Deterministic instances excluded?** Deterministic total machines are ordinarily a subclass of the given transition-relation model. Even an exclusive reading is insufficient: clone state 0 of the three-state witness into states 0 and 3 and nondeterministically choose either clone wherever the old transition entered 0. All four states are reachable from state 1, and the genuine nondeterministic instance needs five strict rounds.
- **Only queried security diagonal matters?** Choose the state whose diagonal disappears last. The two-state B diagonal survives round 2; the three-state state-1 diagonal survives round 4.
- **One initial output-filtering round is preprocessing?** Three states still need four further rounds, exceeding three.
- **Equality-detection application counted differently?** Detecting equality adds one round; it cannot lower the three/five strict decreases to two/three.
- **In-place propagation?** It would be a different update schedule. The paper's displayed operator and its old-R class comparison description do not define or justify that alternative.
- **Identical-input bisimulation instead?** That replaces the independent quantification over related input pairs and changes the specification. It is not the operator being reviewed.

The finite controls are in `independent_controls.py`; they do not call either pre-existing CV-C or Köpf–Basin probe implementation.

For any strict descending chain of partial equivalence relations on m states, `2(m−d)+c` increases, from initial 1 to at most 2m. This proves a `2m−1` upper bound, and the reported deterministic family attains it. Replacing m by `2m−1` preserves the paper's O(m) iteration factor and stated polynomial big-O bound. The fixed-point characterization and broader security methodology are not refuted by this numerical counterexample.

**Safe wording:** “A reproducible counterexample to the literal numerical iteration bound in the inspected author-hosted formulation, with a sharp bound for that operator.” Avoid “first discovery,” “the paper is invalid,” a general bisimulation sharpness theorem, or an assertion that no erratum exists. This review did not repeat the prior historical/erratum search or independently inspect every version named in the addendum.

## Concise integration-risk map

| Boundary | Safe import | Forbidden promotion / remaining obligation |
|---|---|---|
| D1 → D2 | A found finite-k winner is a sure coBüchi winner | Failed single k → general impossibility; belief-only acceptance; unrestricted AS solver |
| Support → probability | Fixed finite homogeneous controller BSCC/MEC analysis | Same support → unrestricted learning equivalence; infinitesimal varying exits treated as uniform progress |
| Hall → deployment | Exact coupling minimum under declared marginals and feasible set | Hypothetical joint law → available sampler, incentive obedience with extra signals, or real authority |
| Public certificate → physical target | Certificate-supported actions are sufficient under declared target link | Repeated certificate failures → repeated hidden physical failure |
| SR1/SR2 → runtime | Full laws, uniform implementable information interface, exposure-compatible fresh-draw realization | Hidden-state action oracle; pre-sampled future coin exposure; local checker → policy conformance |
| Approximation → persistence | Finite occupancy defect or AR2 with public detection and lawful recovery/reentry | Summable departure hazards alone; last-fault postselection; refreshed favorable priors |
| Hidden learning → permission | Conditional statistical identification under the supplied iid model | High posterior confidence → elimination from support or operational license |
| P14/P15 → normative application | Exact consequences of the declared finite geometry and bridge regime | Positive weights → canonical authority; equilibrium → convergence/truth; formal rival → metaphysical possibility |
| Accuracy → common repair | Score-relative coherence plus separately checked robust transition | Per-standard existence → one shared repair; log-score theorem → coherence without its own premises |
| Norm/content → source | Valid hosting conditional with identified object, relation and bearer | Truth accuracy → ultimate intentional host, agency, Wisdom, authenticated source or revealed identity |
| Literature → contribution claim | Local literal-operator discrepancy and reproduction | Priority, global novelty, or wholesale invalidation of prior theory |

## Recommended disposition

1. Accept the repaired control seal as the review target, preserving F1's exposure restriction in any implementation handoff
2. Keep the prediction-game regression in this independent review evidence; a future controller adapter should test the exposure contract explicitly
3. Preserve all negative and positive result types when merging the research narrative: exact theorem, conditional theorem, implementation checker, countermodel, philosophical challenge, primary-source access and open warrant are distinct
4. Do not reopen immutable packets for the minor S=2 prose caveat; record it in a successor errata list if those notes are revised
5. Do not change canonical owner status, call the research programme complete, or claim new kernel verification on this review's authority

## Reproduce this review's fresh controls

Run in a disposable copy of this directory:

```sh
python private_coin_exposure_countermodel.py
python independent_controls.py
```

The second script reads the unchanged, hash-bound copy of the polytope checker in `reference/` and disables bytecode writes. Both scripts are portable standard-library replays. The reference file is copied from the recorded source return; it is not a reviewer rewrite of that checker. Results are exact rational/set computations. No finite experiment is used as proof of an infinite-horizon theorem.
