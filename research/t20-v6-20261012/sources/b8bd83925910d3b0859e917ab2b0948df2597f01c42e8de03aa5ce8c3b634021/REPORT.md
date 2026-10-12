# Independent review: stochastic killed-history transfer

## Verdict

**PASS_SCOPED.** The exact frozen candidate proves the claimed killed-law bridge, restricted-history equality, measurable surviving recurrence transfer, and conditional matching-rival parity test. I found no blocking mathematical or semantic defect within that scope.

This review is independent of the five new proof modules. It is bound to candidate manifest SHA-256 `1a43e77c741402e4411bbe6ac9a8462da60e7d2d5775ab7a8b4e5db4f82707c5`. All twenty inherited modules were compared with their declared originals and are byte-identical. The review did not modify the candidate, predecessors, Knowledge packets, or canonical sources.

Fresh verification compiled all **25 custom modules**, with no custom-object reuse, and read back all **318 registered declarations** and their axiom dependencies. Only `propext`, `Classical.choice`, and `Quot.sound` occur. The inherited code emitted eight ordinary linter warnings; no error or proof-hole warning occurred. The five new modules emitted no warnings. Installed official Lean/Mathlib object caches remain part of the disclosed trust boundary.

## What the result actually closes

The premise is equality of full nonnegative normalized feedback rows on a retained pair set, together with one common measurable seeded policy and its common independent seed law. The conclusion is equality of measures on the entire infinite killed observed-history path space. It is not an assumed equality, a finite-test surrogate, or merely equality of action marginals.

The source provenance and proof chain are concrete:

1. `KilledQueryLaw.lean:10–46` proves zero-query agreement directly by induction over the actual evaluator. Before any query the states agree; once querying occurs both counters are positive.
2. `KilledQueryLaw.lean:48–66` makes the killed readout pointwise independent of the unused oracle. It retains the alive/dead sequence and an arbitrary state readout until the first query.
3. `KilledQueryLaw.lean:82–120` proves measurable pushforward factorization through the common initial-state law. The probability assumption on the oracle law is used when integrating out its total mass. The generic initial-state measure is S-finite; the canonical seeded policy instance is a probability measure.
4. `KilledAdaptiveHistory.lean:50–98` identifies this killed evaluator readout with the kill map on actual acquired histories, using the retained action-readout identity.
5. `KilledAdaptiveHistory.lean:103–121` invokes the retained constructed-law embedding twice, using the same stack base `P` for both representations. The `Q` representation is valid because `P` and `Q` agree on retained pairs. Equality then follows from oracle independence, not an assumed law-transfer premise.

The retained embedding is substantive. `PolicyRowEvaluator.lean` defines a policy that reads only the private seed and acquired history. The action is chosen before feedback; an outside query exposes only the selected row coordinate. `PolicyTranscriptFiber.lean`, `FeedbackRequests.lean`, and `FeedbackFiberProbability.lean` connect each fixed transcript to distinct latent product coordinates. `PolicyCylinderProbability.lean` derives its seed-compatibility factor times the actual feedback probabilities. `PolicyObservedLaw.lean` recovers finite prefixes from the complete last history and uses the infinite-sequence measure extension theorem. `PolicyTraceBinding.lean` identifies the generic trace readout with those constructed laws. None of the new main theorem statements contains the desired killed-law or restricted-law equality as a hypothesis.

## Kill timing and retained information

`historyAction d H k` is the action in the head of `H (k+1)`. On an actual run, the retained `action_readout_on_run` theorem proves that this is precisely the action selected from the state at time `k`, not an unrelated label.

`AlivePrefix D d H n` tests exactly the actions with `k<n`. Consequently:

- At time zero, the empty acquired history is alive
- If the first outside action is selected at index `k`, the output at `k` still contains the previous acquired history
- At index `k+1`, the outside action's receipt is suppressed and the output is dead/empty
- All subsequent outputs remain dead/empty
- Every acquired retained-pair action and receipt before that boundary is retained

Thus the potentially different outside receipt never appears in the killed observation. Killing is indexed after the action's selection but before its receipt is exposed in the output. The first outside action's identity is not preserved as a receipt-bearing history entry; its kill time is retained by the flag. This is the actual source definition, rather than a stronger stopped-path convention that would keep the killing transition.

The default action `d` and default outcome only make `historyAction` total on malformed ambient paths. Actual constructed histories have length `n`, and the next history has a real head. The actual action-readout theorem eliminates dependence on that fallback on the relevant runs.

An independently authored Lean control uses actual `observedHistory` runs of the Markov wrapper. A retained transition agrees, the next outside receipt differs, and the correct kill map erases the difference. A one-step-delayed replacement leaks it. Lean rejects the false equality asserted for that delayed replacement. Initial empty-retained-set killing and retained-receipt visibility also pass.

## Seed independence and measure assumptions

The canonical source laws are pushforwards of `ρ.prod (feedbackLaw …)`. The latter feedback law is a product of an independent per-action stack and an independent fresh-row oracle; each is itself an infinite product of normalized probability laws. `seedLaw` is the pushforward of `ρ.prod stackMeasure` into the actual initial evaluator state.

The common initial representation in the proof therefore contains the same private seed and the same `P` stack law for both models. The only changed factor is the oracle law. No model label or priority enters the policy arguments. The policy may have arbitrary measurable private-seed space and unbounded history dependence; its measurability and shared law are explicit hypotheses.

The required full-row equality is stronger than equal support and stronger than equality after renormalizing to internal successors. There is no positivity/full-support assumption on all transition entries; zero probabilities are admitted, while nonnegativity and normalization remain explicit.

Independent exact rational controls confirm why the retained qualifications matter:

- 8,000 two-step cases cover all binary two-seed deterministic policies on their reachable depth-two histories, over a five-value rational probability grid. Full retained-row agreement gives identical complete killed-prefix laws in every case
- Delaying killing by one receipt destroys the equality
- Equal retained supports with different retained probabilities do not suffice
- Different seed laws can change observed action histories even with identical transition rows
- The same seed marginal and same full-row marginal do not suffice when seed and feedback are correlated differently. This is outside the product construction

These finite controls test semantics independently. The infinite-path theorem is established by the separate kernel-checked measure proof, not by the 8,000 cases.

## Restricted events and recurrence

`KilledRecurrentTransfer.lean:16–78` proves measurability of staying in the retained set and the exact preimage identity:

`killedHistory ⁻¹ aliveHistoryEvent(C) = C ∩ HistoryStays`.

On never-killed paths, the second coordinate reconstructs the complete original history. This justifies transferring every measurable history event restricted to survival, including events depending on outcomes rather than only actions. `canonical_history_restrict_eq` proves equality of the restricted measures. It does not normalize them or silently assert survival has probability one.

`SurvivingRecurrent` is the intersection of the exact recurrent-pair event with **never** selecting an outside pair. Measurability uses the retained countable recurrence-event construction. `matching_model_even_on_positive_surviving_recurrence` transfers positivity to the rival, intersects it with the rival's almost-sure parity event, and obtains a path whose recurrent set is exactly the specified set. The even minimum is then a deterministic consequence of that path. This step is sound and does not assume fairness or almost-sure recurrence of a stationary policy.

The scope is important: this is a surviving event from the current experiment's start. It does not yet transfer an arbitrary eventual-tail event after a possibly informative prefix. The omitted residual-prefix seed cancellation is exactly what would be needed to justify a suitable restarted common-law experiment.

## Actual Markov interface and finite-target scope

`MarkovKilledBridge.lean:15–54` derives the source-state coordinate from the latest observed successor, or from the given initial state at the empty history. Its policy sees the complete action/observed-state history after removing redundant source labels. The step theorem proves that the next history is the selected state/action pair together with the actual fresh-row outcome, prepended to the old history.

`realRows` preserves the exact rational rows as real probabilities; the cast lemmas prove nonnegativity, normalization, and full-row matching. `markovHistoryLaw` is defined using those rows and the actual state-consistent policy. The wrapper is therefore not an abstract action process with externally asserted state consistency.

The final `markov_matching_parity_valid` theorem concludes the retained `Valid` predicate, comprising an end-component condition and every matching live rival's even-minimum test. It explicitly takes the end-component condition as a premise. It does **not** by itself prove `MarkovQualifying`, membership in the full target solver, licensing of the pair set, or zero candidate exit. Those require the separate allowed-pair/no-exit inputs and adapter results. This distinction agrees with the README's narrower description of the full matching-rival parity test.

Likewise, pair killing does not inspect a separate support-update label. Its no-exit application must use the independent normalized-row adapter's candidate no-exit property and full-row preservation. No unobserved support label is inserted into the policy.

## Findings and retained obligations

No blocking finding. One low-severity documentation ambiguity remains: the copied `THEOREM_CONTRACT.md` says “This source is not part of candidate-v1” inside a directory itself called `candidate-v1`. It appears to refer to the earlier finite-target candidate, but the referent should be named explicitly in a subsequent documentation version. This does not affect the manifest-bound code or proof.

The following remain open and must not be treated as consequences of this acceptance:

1. Positive-prefix residual seed cancellation and construction of the restarted common seed law
2. Almost-sure closure and strong connectivity of the recurrent pair set for arbitrary adaptive policies
3. Fair/positive stationary operation visiting every retained pair infinitely often almost surely
4. Proper-support recursive winning regions, navigation/statistical rejection, and the full hidden-parity equivalence
5. Polynomial MEC implementation and optimal memory claims

## Reproduction and evidence

`SOURCE_BINDING.json` binds every candidate file. `INHERITED_IDENTITY.json` records all twenty exact comparisons. `evidence/REPLAY_RESULT.json` is the independent cold-run receipt; `evidence/PortableReadback.log` contains the 318 exact declaration types and axiom readbacks. `controls/` contains independently authored Lean and Python controls and their runners; `evidence/` includes their results and logs.

The cold replay command uses the candidate's inspected portable driver, pinned Lean 4.19.0 and Mathlib revision `c44e0c8ee63ca166450922a373c7409c5d26b00b`, `--suites killed_markov_parity`, `--no-reuse`, and an absent output outside the candidate. The controls then use only custom objects freshly built by that independent cold run, checked against its recorded hashes. No author object directory was used.

This verdict authorizes only the stated review conclusion. It does not alter canonical status, publish anything, or promote the bounded bridge to the complete programme.
