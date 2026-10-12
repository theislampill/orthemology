# Independent review: actual observed-history target operation

## Verdict and source identity
PASS_SCOPED. The five new modules pass source inspection and a fresh serialized 70-module/744-readback replay. Thirteen independent Lean controls and three actual core-source mutations pass their intended checks. The earlier run was interrupted on the parent's resource-serialization request before qualification; its interrupted receipt is retained and is not counted as a mathematical failure or success.

Candidate manifest: `50e6a8ccec70ac8737b9cfef91def37570a660a56397ed46451b69c9151a1741`, 70 custom modules, 744 registered readbacks. The new sources are RoundRobinSchedule, RoundRobinPolicy, RoundRobinRecurrence, ActualTargetPolicy and RoundRobinControls. The author packet remains unchanged.

## Exact mathematical contract
The model is the same finite observed-state controlled Markov source with normalized rational full rows. The total action policy reads the entire ordinary action/receipt history. It uses the initial state on empty history and the latest observed receipt afterward; the departure count reconstructs how often that state has previously been the source. Each state cycles through its own retained action menu. The policy ignores the private seed and has no hidden-model or priority argument.

A supplied component is genuinely nonempty, successor-closed and strongly connected in the actual row support. The initial observed state must be a used component state. The fallback action makes the policy total off the retained states but is unreachable on supported runs from the stated initial condition. Finite action/state instances, measurable singleton structures, an inhabited state type, and a supplied fallback action are explicit assumptions. An empty action type cannot be silently instantiated.

`roundRobin_markov_recurrent` proves exact equality of the actual recurrent pair set with the retained component under `markovHistoryLaw`. This directly closes the prior auxiliary-operating-kernel versus actual-policy gap. The theorem does not assume fairness or an equality of operating and policy laws.

`computed_target_actual_policy` starts with membership in the actual executable finite target output. It obtains a qualifying component containing the given state and proves actual parity success of its one cycling policy for every full-row-matching live rival. Its quantified conclusion remains conditional on row matching. If the candidate is outside the live set the theorem does not by itself assert success under that candidate; ordinary algorithm uses have the candidate live.

A separate `matchingTargetWinningPolicy` builds the full lawful AS witness when every live model matches that retained component and its pairs satisfy the original hard menu. The support stays exactly unchanged on every feasible compatible history, so original history-level `Lawful` is established rather than substituted by a path-only certificate. Singleton matching is automatic and yields `computed_singleton_target_semanticWinning`, on a Unit seed space. The underlying recurrence/parity theorem accepts any supplied probability seed law, which is ignored by this policy.

The action enumeration uses `Fintype.equivFin` in a noncomputable section. This is a concrete deterministic mathematical history policy, not extracted executable bytecode or a compiled controller. The finite target computation and this classical policy construction are distinct claims.

## Source audit
The visit counter starts at zero before the initial departure. On a new history record, it increments the source reconstructed from the preceding older history, not the new receipt. The newest-first append convention is respected. `stack_historyVisits` identifies this reconstructed count with the actual source trajectory's departure count.

For every infinitely recurring source state, the least-crossing proof consumes every visit index. Arithmetic progression indices hit every retained action in the finite cyclic enumeration. Thus `stack_roundRobin_fair` proves recurrence of every retained pair at recurrent states, without probabilistic fairness as an input.

Actual supported feedback and component closure keep every issued pair inside the component. The previously proved raw independent tape recurrence and sequential per-pair consumption then derive the actual recurrent end component. `fair_closed_subset_eq` proves that any nonempty closed recurrent subset containing all retained actions at its used states must fill the whole original strongly connected component: reachability propagates membership in its used states, and cycling fills their actions. A mere closed subset without this derived fairness would be insufficient.

The stack-to-canonical action-law theorem and history-action readout transport this exact recurrence to `markovHistoryLaw`. For a qualifying component and a matching live rival, normalized numerical row equality and the zero-exit adapter derive equality of the actual and internal successor graphs. The checked minimum-even predicate then supplies parity. No auxiliary uniform Markov chain is substituted for the actual cycling policy.

For lawfulness, induction on every feasible compatible history chooses a surviving model, uses its positive recorded transition, proves the chosen source/action is retained, and derives both preserved support and retained next observed state. The all-live no-exit/closure assumptions are discharged from full-row matching. The hard menu is consequently evaluated at the original support and actual current state. A nonmatching model may invalidate this argument; the theorem retains that guard.

## Independent controls
A standard-library exhaustive graph oracle checks 926 retained-component/initial-state systems and all their 926 reachable bottom classes. Its state includes the observed state and the per-state cyclic counters. Every bottom class projects to the entire retained pair set. It independently rejects replacing per-source counters by the physical clock: on alternating sources, global-clock cycling omits half the actions and can leave only odd recurrent priorities despite an even component minimum. A constant allowed selector similarly need not fill the component.

A separate full-support two-model countercontrol keeps the same positive graph while changing full numerical rows and giving the candidate even priority but the nonmatching rival odd priority. It demonstrates why the matching condition cannot be removed. Exact graph controls are corroboration, not an infinite-law proof.

Thirteen reviewer Lean controls bind the recurrent-set equality directly to the actual one-state law and show that the odd-priority-3 action recurs infinitely under the same winning policy. They also probe departure versus receipt counting, seed independence, and the existence of a proper closed subset without fairness. They additionally prove a normalized full-support unequal-row component qualifies for the candidate while every trajectory fails the nonmatching rival’s always-odd parity objective. Their kernel result and axiom readbacks are recorded separately.

## Limits and provenance
This is local target operation only. It does not construct the global support/state region's navigation, hypothesis tests, rejecting phases or recursive policy handoffs. It is not a full stochastic iff. No finite expected odd-visit count, detectable stopping time, global finite-memory theorem or controller compiler is inferred. The policy may be represented more economically, but such an executable realization is outside this packet.

Only the standard foundational axioms propext, Classical.choice and Quot.sound are permitted in replay. Official Lean 4.19.0 and pinned Mathlib objects remain trusted. No proof hole, unsafe declaration or native_decide qualification is accepted. All source and dependency identities are verified independently; older freezes are unchanged.

## Qualification and replay
The final candidate source census and all 70 independently produced object fingerprints were rechecked against the terminal cold-v2 receipt. All thirteen reviewer readbacks use only the permitted standard axioms. Mutants replace per-state visits by the physical clock, freeze the visit counter at zero, or select the same cyclic index every time; the first affected source is rejected in each case. Only verified unaffected reviewer objects are reused. No author objects are imported.

The source-only archive includes the entire 70-module closure, exact cold/type/axiom receipts, reviewer controls, finite oracle, source-mutant evidence and portable replay script. Fresh extraction is checked against its complete manifest, and the small finite oracle is replayed from that extraction. The composite full-cold archive driver is supplied, but a second 70-module cold run is intentionally not counted: the already completed cold run is bound to the exact same source bytes, and host-wide cold replays are serialized.

```
PYTHONDONTWRITEBYTECODE=1 python checks/verify_packet.py
PYTHONDONTWRITEBYTECODE=1 python checks/replay_review.py --env /path/to/pinned/environment --out /fresh/absent/outside-packet
```

The reviewer previously authored some retained controlled-iid stack ancestry and a separate SCC selector. These five new target-policy modules were independently authored, frozen before review and never edited here. This disclosure distinguishes fresh source review from wholly disjoint authorship of every imported library.
