# Independent review: global support-changing hidden-parity necessity

## Verdict and source identity
PASS_SCOPED. All nine new mathematical modules pass end-to-end source review, the full 66-module/720-readback independent cold replay, 31 reviewer readbacks, five core-source mutations and 512 exact finite-system comparisons. No semantic gap or author-source correction was found.

Input: `candidate-v1/MASTER_MANIFEST.json`, SHA256 `6d3b8fb4aa3ebaa0341d43cf72dfff79ad17ebcbc5d433fda9914aadb0deb80f`. The packet has 66 custom modules and 720 registered declaration readbacks. The exact principal endpoints are `winning_policy_mem_winningRegion` and `computed_losing_excludes_common_policy` in `HiddenParity.Necessity`.

## Exact theorem assumptions
There are finite observed state and action types, an inhabited state type, decidable equality, and measurable singleton structure. Models range over an arbitrary decidable type, with a finite nonempty live support. Each hidden model supplies a fixed nonnegative normalized rational transition row for every observed state/action pair. The next receipt is the next observed state. The same initial observed state is used under every model. Natural-number priorities may depend on the hidden model and observed pair; neither the model label nor its priority is feedback.

A hard menu depends on the exact finite live support and current observed state. One arbitrary measurable seed probability law and one measurable full-history action policy are chosen before the true model. The seed is independent of the actual source. The policy can use unbounded memory, time and all observed action/state history. The supplied default pair `d` is only a history readout fallback, unreachable on real positive-length histories; supplying it excludes an empty action type. The theorem does not manufacture a default for an empty action space. The algorithm itself rejects empty support; `WinningPolicy` explicitly requires nonempty support, so there is no vacuous policy-existence promotion.

`WinningPolicy` contains only support nonemptiness, an actual seed law, its probability instance, the measurable policy, direct lawfulness and all-live-model almost-sure parity under `markovHistoryLaw`. It has no supplied safe region, successor certificate, target, recurrent component or postfixed-set premise.

Lawfulness is almost-sure compatible-seed lawfulness at every finite history with nonempty exact live support. The new equivalences identify it with zero actual illegal-next-action probability after every finite history, or only after histories of positive actual probability. The next receipt is not included in that event. Null private seeds and incompatible recorded histories do not impose extra pointwise constraints.

## Dependency qualification
The adaptive predecessor derives arbitrary-policy recurrent end components from actual iid per-pair tapes and sequential consumption, without policy fairness. Its stable-support theorem is only used after the new stage proof has established all-time no-exit in the no-reachable-exit case.

The separate conditional-AS review is freshly accepted at `tranche5/continuation-as-independent-review`: archive SHA256 `187f883a8efaed93189e677026cbf8aacf8009f5ba03ce2a104d05170d071dfa`, manifest `af697ac824445933059b985fd07b8a578c63929b4a0f3b0adc282935a5efca0e`. It binds author manifest `cd17a13ef361de796b590ab37579d11ae235efbdc75a28750f4e0db9f53bd55d`. The archive and exact report/manifest/seal bytes were independently checked here. All global packet source origins are checked against their actual files. Its seven conditional-source copies preserve the same actual compatible-seed posterior, conditional observed-law binding and AS shift theorem.

The review does not assume a raw latent-tail marginal theorem. The necessary interface is the proved law of the observed continuation, with latest observed state, original policy right-appended to the fixed prefix, and common normalized compatible-seed posterior.

## End-to-end proof audit
### Lawfulness and the observed prefix
`liveHistory` filters the original support by positivity of each recorded full row; its cons and right-append identities match newest-first histories. Current-state append is proved with the same convention. An inconsistent source/action record is incompatible with `pairPolicy`, so positive likelihood alone is never mistaken for a positive actual prefix.

`illegal_prefix_factorization` factors the real prefix-plus-illegal-next-selection event into its illegal compatible-seed mass and the prefix row likelihood. A live model makes that likelihood positive. Conversely, positive actual prefix mass places the true model in the live set. These facts establish the lawfulness equivalences, including the null-prefix cases.

`lawful_restart` restricts the original lawfulness statements to the common compatible-seed posterior. Compatibility concatenation, support concatenation and current-state concatenation identify the restart's menu with the original menu. It does not reset the seed to its unconditioned law.

`restartWinningPolicy` takes an actual positive observed prefix. Its posterior is a probability measure, is the same for every surviving model, and makes that same prefix positive under each survivor. The independently proved observed restart law and actual parity tail invariance derive AS success for every survivor. The resulting child witness is a genuine `WinningPolicy` on the original seed space.

### Every positive action branch is safe for every live successor
`positive_action_branch_safe` starts with a positive compatible-seed action branch at a same-support history. A lawful seed on that branch certifies its hard-menu membership and actual source. Prefix factorization makes the current state semantically winning. For each observation with nonempty child support, choose any child model: its old prefix likelihood and its selected transition probability are positive. Thus the extended recorded history is positive under that model, and the common restart wins for every model surviving that extension. This supplies every nonempty child, not just a favourable candidate-specific branch.

Zero-mass seed/action branches are removed only almost surely. Finitely many actions and countably many finite histories yield one full-measure seed event. Actual stack histories are compatible by construction. The proved unchanged-support-prefix identity then derives `winningPolicy_safe_until_exit` under the real canonical pair law. It is not an assumed controller invariant.

### The target-or-exit alternative
`ReachableExit` requires a same-support reachable allowed pair, a candidate-positive observation and a nonempty proper live-support update. If such an exit exists, the stage condition uses it directly; it does not falsely demand a positive no-exit event.

If no exit is reachable, every reachable allowed pair is candidate-zero-exit. Induction over actual supported transitions shows that the same-support prefix and internal reachability persist at every time. The supplied until-exit membership is consequently all-time allowed/no-exit membership. Only now is the previously proved support-preserving necessity invoked. This derives a computed target and path. The revealing example, which refutes unconditional stable-support necessity, is therefore handled by the exit branch rather than incorrectly excluded.

### The actual finite computed region
`regionAllowed` checks source membership in the current state region, the hard menu, all same-support successors in that region, and every nonempty proper successor in its computed child region. `regionStep` retains precisely those current states from which each live candidate reaches a qualifying computed target or a candidate-positive proper-support exit.

Target monotonicity is proved through the exact qualifying-component characterization, not guessed from a pruning implementation. Together with path/exit monotonicity it proves region-step monotonicity. Contraction and finite cardinal decrease prove state descent stabilizes after at most the number of observed states. Any semantic postfixed subset survives the descent.

`semanticAllowed_subset_regionAllowed` uses only strict-child necessity. The real semantic winning set is then proved postfixed from the derived target-or-exit theorem. Support-fuel induction supplies every strict-child premise, using strict cardinal decrease. Thus the final public endpoint has no postfixed/safety/target assumption.

`computedRegion_fuel_irrelevant` shows that all fuel at least the support cardinality agrees. Its proof observes that the stage only consults proper child regions; same-support transitions use the current state approximation. `winningRegion_fixed` then identifies the result with a fixed point whose lower regions are the canonical `winningRegion` values, rather than fuel-relative approximations.

## Independent adversarial controls
The reviewer extends the adaptive revealing fixture to a genuine lawful common `WinningPolicy`. Its original-support target is empty, its candidate-positive exit exists, the public theorem places its initial state in the global computed region under its actual law. A separate two-state one-action revealing fixture isolates the fuel boundary: fuel one loses initial state zero, exact support-cardinality fuel admits it, and arbitrary excess fuel is proved irrelevant.

A null-seed fixture is lawful under a Dirac seed law while a different compatible null seed selects an illegal action. This distinguishes the accepted AS lawfulness from unclaimed pointwise legality. A separate exact event calculation gives illegal initial selection probability one before any next receipt is observed.

The independent finite oracle enumerates all nonempty pair subsets directly, tests true successor nonemptiness/closure/strong connectivity, zero exit, exact full-row equality and every matching rival's minimum parity. It then performs independent bottom-up support recursion and state fixed-point iteration. It does not import the author's MEC/pruning routines. Its exact comparison count and outcome are recorded in the oracle receipt.

Independent finite-prefix controls directly enumerate four weighted private seeds, causal history policies, rational zero/nonzero transition rows and dynamic menus. They check prefix and illegal-next factorisation, candidate-independent compatible-seed posteriors, and positivity of every live extended branch. They corroborate the measure-theoretic proof but do not replace it for arbitrary seed spaces or infinite trajectories.

Core source mutations probe deletion of proper-child obligations, zero state descent, one-less support fuel, keeping zero-mass models in support updates and dropping compatibility from lawfulness. Every affected source is rebuilt; no stale downstream object can certify a mutant. Exact outcomes are recorded separately.

## Axioms and limits
Readbacks permit only `propext`, `Classical.choice` and `Quot.sound`; this is not an axiom-free extraction claim. Official Lean 4.19.0 and pinned Mathlib objects are trusted. No new toolchain installation or canonical source edit was made.

The accepted mathematical direction is necessity only. A negative computed region excludes any common lawful AS policy in every measurable seed space to which the theorem applies. A positive result is not yet a global policy synthesis or stochastic iff. Local target operation and full navigation/testing/phase composition are separate. No finite expected odd-visit budget follows from parity, and no finite-memory restriction was imposed on policies.

The algorithm currently calls the exhaustive target reference. A separately authored SCC substitution must prove actual equality before replacing it. There is no polynomial claim for the whole support/state recursion here. All zero probabilities and rational rows are exact supplied model data; finite samples cannot certify a probability is exactly zero.

The reviewer has prior authorship in some retained controlled-iid ancestry and the separate SCC solver. The nine new global sources were frozen by another author and not edited in this review. Dependency reviews, new controls, cold replay and source custody are distinguished explicitly.

## Final evidence and portable custody
All 66 input sources and their source-origin files match the recorded digests. Every independently produced object was checked again against the accepted cold receipt. Thirty-one reviewer theorem/witness readbacks use only the permitted standard axioms; the earlier revealing-control module differs from its accepted predecessor solely by replacing one unused control import with its two mathematical imports. That import-only adapter is separately bound.

The independent region oracle matches all 512 systems, giving 2,048 support comparisons including 1,536 nonempty supports. It covers all 256 deterministic eight-row tables and 256 further rational tables, each with declared dynamic menus and hidden priorities. An interrupted first run retained 350 complete matching output rows and one truncated row, which is not counted. A separately recorded continuation drops exactly those 350 indexed cases and completes the remaining 162; definitions and case data are byte-identical. This is two supporting finite runs, not one uninterrupted execution or a proof of the infinite-policy theorem.

The prefix controls pass 12,320 exact prefix/illegal-selection factorisations, 4,498 common-posterior checks and 7,859 positive extended-branch checks across 128 systems. All five core-source mutants are rejected. These controls are evidence for the audited interfaces; the necessity theorem's general validity is supplied by its cold-checked proof.

The complete source-only archive is freshly extracted and checked against every manifest entry. Its portable driver can repeat all stages:

```
PYTHONDONTWRITEBYTECODE=1 python checks/verify_packet.py
PYTHONDONTWRITEBYTECODE=1 python checks/replay_review.py --env /path/to/pinned/environment --out /fresh/absent/outside-packet
```

A second full 66-module cold run after packaging is intentionally not counted. The already accepted cold run is bound to the same extracted source bytes; the composite replay script is supplied, with individual stages validated, while host-wide cold replays are serialized. No compiled objects or unregistered caches are shipped.
