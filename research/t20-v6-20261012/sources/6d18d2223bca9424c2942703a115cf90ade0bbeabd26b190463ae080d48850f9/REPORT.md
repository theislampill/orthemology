# Independent review: actual adaptive recurrence and stable-support necessity

## Verdict
PASS_SCOPED. The frozen 51-module candidate derives actual arbitrary-policy recurrent end components and the stated stable-support/no-exit necessity endpoints. No proof gap or source correction was found. This is not a review of the separately frozen global support-changing necessity or global sufficiency.

Candidate: `candidate-v1/MASTER_MANIFEST.json`, SHA256 `97ee94fae1cb429617fd97be5baa95319f39ad8ce50a5aaac18739e270b4b727`. All 51 custom sources were copied, source-origin checked and independently cold-compiled; 566 registered declarations received type and axiom readbacks. No author objects were reused. Official Lean 4.19.0 and the pinned Mathlib installed object cache are trusted. This is not an upstream-source bootstrap.

## Exact accepted contract
The observed state and action types are finite with decidable equality, the state type is inhabited, and the finite observation spaces have measurable singletons. The seed space is arbitrary measurable; its probability law is selected together with one measurable policy before quantifying the true live model. A finite live support sits in a decidable model type. The main necessity endpoint uses nonnegative normalized rational rows and their exact real casts. Priorities are natural numbers indexed by hidden model and observed state/action pair. They are not policy inputs.

The policy reads the complete newest-first action/receipt history. `pairPolicy` binds the issued pair's source to the latest observed state, or the supplied initial state on empty history. Erasing redundant source labels retains every action and receipt. The default pair used by history readout is unreachable on actual nonempty histories and need not itself have the initial source. The private seed and all source tapes have their actual independent product law. Merely giving every model the same seed marginal would be insufficient.

`canonical_markov_recurrent_end_component` has no fairness, stationary-policy or finite-memory assumption. Under the actual canonical pair law, the exact infinitely recurring pair set is almost surely a nonempty end component of the actual positive-row support graph. `markov_recurrent_end_component` transports this to the complete observed-history law. `canonical_markov_supported_path` includes the initial source and every positive consecutive edge.

`stable_support_path_to_computed_target` additionally assumes:
1. the one policy and seed law are almost-sure minimum-even-parity successful under every model in the finite live support;
2. under the selected candidate model, every issued pair lies in the supplied allowed set almost surely, at every physical time;
3. every candidate-positive successor of every allowed pair remains positive under every live rival.

The theorem derives a concrete qualifying component and an internal finite path from the supplied initial state to the actual executable target set. It does not receive a component, target, path, postfixed region or recurrence premise.

`support_preserving_policy_path_to_target` instead assumes that every actually selected candidate pair is allowed and candidate-zero-exit almost surely. Filtering the allowed set to these zero-exit pairs discharges the previous stability condition, and target-filter idempotence identifies the original target. These are all-time assumptions under the candidate law. Neither follows merely from eventual support stabilization or from a positive no-exit tail. They also do not assert pointwise lawfulness at every null/off-policy history.

## Proof audit
### Raw tapes and sequential consumption
`RawTapeRecurrence` obtains positive-symbol recurrence by second Borel–Cantelli on the proved independent product coordinates. Every coordinate event has its row's positive mass, hence their sum is infinite. Finite pair/symbol quantification gives one probability-one event; zero-mass symbols are absent from all countably many cells almost surely.

`SequentialTapeConsumption` uses the actual occurrence counter in the recorded history. It starts at zero and increases by one exactly when that pair is selected. Infinite pair selection makes this count unbounded; the least crossing argument proves that each deterministic tape index is consumed. The review adds strict increase between selected occurrences and uniqueness of a consumed index. Raw-tape recurrence then implies observed successor recurrence through arbitrary adaptive gaps, without conditioning an iid estimate on a selected sample count.

The graph proof first removes finitely occurring pairs from a sufficiently late suffix. Recurrent successors occurring after that cutoff prove closure. Actual supported finite path segments between late recurring pair occurrences prove strong connectivity. Nonemptiness follows from finiteness and an infinite trajectory. Source consistency is established by the actual policy wrapper. The canonical-law lift uses the retained exact stack/action-law identity, not a replacement oracle with an assumed law.

### Matching rivals and the target
The proof selects an exact recurrent-set event of positive candidate probability. Candidate stability supplies zero exit and identifies the candidate support graph with the common internal graph. For every full-row-matching rival, a positive exact recurrent-tail event is intersected with the all-allowed-action guard. The retained safe relative-tail transfer then preserves positivity. Almost-sure rival parity forces the minimum rival priority on that same recurrent set to be even.

Importantly, the transfer patches unused off-allowed rows before global domination. It first proves equality on events whose actually visited actions are all allowed. It does not demand domination of unused unsafe full-row coordinates. The original common seed measure is retained; no model-dependent seed posterior is silently reset. The plain successor-congruence lemma imported from the uniform-operation module has no fairness or stationary-operation premise.

The normalized support adapter derives full `MarkovQualifying`, including allowed membership and zero exit. This closes the explicitly qualified gap in the earlier transfer review, which established only graph-component and matching-parity validity. The proved executable target equality and an actual supported prefix finish the result. Finite-prefix parity invariance is separately proved; it is not itself a conditional restart theorem.

## Independent evidence
- 51 fresh custom modules; 566 author type/axiom readbacks, all allowed axioms only.
- One reviewer module, 19 additional theorem readbacks. It checks strict/unique tape consumption, absence of policy fairness, state/action rather than action-only counters, current-state binding and the unreachable readout default.
- A reviewer theorem constructs a genuine two-model canonical-law revealing policy: initial action zero, then select the latest deterministic model-revealing receipt. It wins almost surely for both models, all pairs are allowed, yet both original-support target sets are empty. Thus dropping support stability would make the proposed necessity false. The global successor must use its proper-support exit alternative to cover this fixture.
- Four actual core-source mutations are rejected after fresh affected-source compilation: physical-time sample count, count starting at one, physical-time receipt index, and recurrence asserted for zero-probability symbols. Only hash-verified, unaffected objects from this review's fresh baseline are reused. Rejection is evidence of these proof boundaries, not an exhaustive mutation guarantee.
- 20,736 independently enumerated finite-controller/support systems yield 26,608 bottom-class projections, all directly checked as end components. 26,340 are proper subsets of available pairs, refuting any gratuitous fairness claim. This finite subclass is corroboration; the universal adaptive result comes from Lean.
- 24,192 exact rational prefix-factorisation checks and 1,152 normalisations compare chronological likelihood with the per-pair tape likelihood for causal seeded policies.
- A correlated seed/receipt countercontrol preserves both marginal laws while revealing the model through their joint value. It fails the required product-independence contract.
- A separate three-state revealing-to-absorbing fixture is eventually zero-exit with a matching tail, but the prefix is impossible under the rival and the initial-support target remains empty. This is an ordinary exact countercontrol to replacing all-time safety by eventual safety.

The wrong physical-index fixture distinguishes two fixed-tape trajectories. It is not a claim that a separately proved fresh-per-physical-time iid construction has a different canonical law; such a construction may have the same law. The present pathwise recurrence bridge specifically needs its proved sequential per-pair consumption.

## Provenance, axioms and limits
The seven new modules are RawTapeRecurrence, SequentialTapeConsumption, RecurrentGraph, AdaptiveMarkovRecurrentGraph, StableSupportParityNecessity, ParityTailInvariance and AdaptiveControls. `SOURCE_ORIGINS.json` and the independent `SOURCE_BINDING.json` bind all 51 exact sources. The complete closure includes retained third-return modules and separately reviewed fifth target/transfer/recurrence sources. No unavailable fourth proof seal was reconstructed. Exact predecessor archive/manifest checks and copied bound review documents are in `dependencies/` and `DEPENDENCY_BINDING.json`.

Only `propext`, `Classical.choice` and `Quot.sound` occur in permitted axiom readbacks. No proof holes, custom axioms, native_decide or unsafe declarations were accepted. Proof-backed executable definitions may have these foundational dependencies; no axiom-free extraction claim is made.

This packet leaves lower-support winning continuations, all-branch dynamic licensing, positive-prefix residual seeds, the outer state-region fixed point and full support-changing necessity/sufficiency to separate successors. It does not prove finite expected odd visits, finite-memory sufficiency, a deployed controller or a polynomial whole-algorithm complexity bound. Its target selector is the inherited exhaustive reference; the separately accepted SCC replacement is not silently substituted here.

The reviewer previously authored parts of the retained controlled-iid stack/tail-transfer ancestry and the separate SCC replacement. The seven new adaptive sources were authored by another worker, frozen before this review and never edited here. This is independent source replay and adversarial mathematical review with that disclosed shared ancestry, not a claim of entirely disjoint authorship of the transitive library.

## Replay
After extracting the source-only review archive to a clean directory:

```
PYTHONDONTWRITEBYTECODE=1 python checks/verify_packet.py
PYTHONDONTWRITEBYTECODE=1 python checks/replay_review.py --env /path/to/recovery-20261001/environment --out /fresh/absent/outside-packet
```

The replay cold-builds all 51 sources, compiles the reviewer module, checks all type/axiom readbacks, runs the finite controls and four core-source mutations, and rechecks the immutable input census. It does not install software. Development failures and corrections to the review harness are retained only as development evidence, not counted as accepted runs.
