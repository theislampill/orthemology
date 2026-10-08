# Covering and opaque-repair kernel closure

## Status and scope

This is additive Priority 8 verification work on the already accepted Seventh result. It contributes no new mathematical theorem novelty count, no stronger fault budget, and no strengthened world/mapping observations. It leaves every accepted source byte unchanged.

The targeted ordinary assertions are COVERING_TRADEOFF.md §1 and GENERAL_UNKNOWN_CLASS_THEOREM.md Theorem E, with Theorem B's maximal-taint realization used to connect the search worlds to actual roots. The proof goal is a generic kernel theorem, not a finite enumeration of selected parameters.

Labels form any finite type α. Write m=|α|, q for selected path size, k for maximal bad-label size, and b=m−q for complement block size. For the unknown-class source, k=B+c−1 with c≥1, B≥1, B<m−c+1. Mathematical feasibility of the covering construction is k≤b≤m. The accepted safety/availability interface additionally imposes q≥1, q+r>m+k and q,r≤m−k. The counting proof does not replace these safety premises.

## Explicit definitions

- Uniform q F: F is a finite set of label sets, and each member has cardinality q.
- Available k F: every label set T of cardinality k is disjoint from some P∈F.
- Covers k G: every such T is contained in some A∈G.
- complements F: image of F under finite-universe complementation. Complementation is involutive and injective, so cardinality is preserved.
- coveringNumber α b k: infimum of the set of cardinalities of b-uniform covers of all k-subsets. Attainment is separately proved under k≤b≤m; infeasible parameters use Nat's empty-infimum convention and are not advertised as covering optima.
- C(m,b,k): coveringNumber (Fin m) b k. Equivalence transport proves label names do not matter.

These definitions contain neither an optimality conclusion nor a physical repair guarantee. SuccessWithin explicitly means that one selected support is disjoint from T before the bound. In the source's canonical withheld-effect worlds, this is exactly a successful repair intervention. Its use as a lower bound on target-state achievement chooses an initially defective canonical world. An already-correct target requires zero attempts; no positive target-achievement lower bound is claimed there. For an upper bound it is a sufficient success condition under the retained all-intact-path service contract. Tainted paths that happen to succeed can only improve an upper bound.

## Complete action and observation interface

OpaqueActions.lean is the primary adaptive lower-bound interface.

An Action is arbitrary data. It may include the full selected command, nonce, recipient, descriptor, selected label path, and any policy-private command choices. support : Action → Finset α extracts the chosen label path. Every action's support belongs to one fixed prepared family F. The policy is an arbitrary function of the complete action/observation history. Fixing the complete random seed gives such a deterministic policy. No finite bound on the set of commands or seeds is imposed.

The observation type Obs is arbitrary and can encode every authenticated preparation reply, effect receipt, cancellation reply, and logical timing coordinate. Actual observations are functions of a fixed T, the complete prior history, and the submitted action. Failed replies may likewise depend on the complete history/action. Thus the formalization does not assume that nonces or command bodies are determined by the path, that timing is absent, or that a policy ignores cancellation information.

Actions.Opaque states only that, on an all-failure prefix still compatible with T, the actual next failed observation equals the common failed observation. It constrains no successful reply and no unreachable history. The proof derives equality of the entire actual/failure histories and the first-success equivalence; that conclusion is not embedded in Opaque.

This is exactly the common-failed-transcript hypothesis constructed by the accepted source, with its full-command cancellation, fresh nonces, quiescent suffix, no additional probes, and fixed mapping/fault budget. The kernel proves consequences of this observation interface. Physical permission to realize these replies remains the source's conditional protocol premise, not a consequence of a type definition.

FullCommandInterface.lean supplies a typed full command with selected Path F, natural-number nonce, and repair body. Its upper-bound enumeration preserves one body and proves nonce n at attempt n. The abstract canonical reply constructor carries arbitrary full control payload and an optional truthful effect/no-effect receipt; it is proved opaque. That constructor demonstrates the symbolic observation law, not real authentication or gate coherence.

## Main quantified claims

1. A uniform q-path portfolio is available exactly when its (m−q)-complement blocks cover every k-set. All attainable cardinalities correspond; consequently the least portfolio cardinality is C(m,m−q,k).
2. For the successful-intervention objective (or target achievement from a defective canonical start), every deterministic adaptive full-command policy satisfying the failed-transcript interface and repairing every maximal world within N attempts has C(m,m−q,k)≤N. Repeated attempts cannot evade the bound: the set of distinct supports on the failure spine has cardinality at most N.
3. A minimum cover is attained. Enumerating its complementary paths issues fresh full commands and hits an intact path within C(m,m−q,k), including all nonmaximal actual fault sets. Cancellation/service correctness and the charged phase budget remain the accepted execution contract.
4. When b=k, every covering block must equal the k-set it covers. The cover is exactly all k-sets, so C(m,k,k)=choose(m,k). In particular m=3k+1, q=2k+1 gives choose(3k+1,k).
5. For a fixed probability law on complete coin outcomes and a fixed finite family of maximal bad sets, almost-sure success for each fixed world gives a common conull set of seeds succeeding for every world. A seed in that set invokes the deterministic lower bound. Thus randomization cannot lower the almost-sure worst-case cap.
6. If N<C, one particular compatible root class A and actual-root fault set S (|A|=c, |S|=B) fails the cap on a non-null set of seeds. A and S are existentially selected outside the almost-everywhere coin quantifier. No adversary access to private coins is assumed.

The separate probability utility also proves a 1/|W| outer-measure bound for arbitrary failure predicates covering the seed space. For measurable failure events that is a probability bound. The covering theorem only needs the AE intersection argument; no expected-attempt optimum is claimed.

## Retained boundary

Not proved here: physical interlocks, authentication, root coherence, actual authorization or cleanup rights, bounded control service, phase duration, stable delivery, finite-horizon sufficiency, residual-old-work accounting, absence of unmodeled channels, or the empirical correctness of the possible-map family. No cancellation mechanism is added. No dynamically learned/rebuilt family, partial-cancellation probe, out-of-path old-command query, gate-state readout, physical correlation experiment, owner-transition coordination, unrestricted mobile faults, R5 expansion, N2/T0 conclusion, metaphysical source claim, or whole-program closure is supplied.

No claim is made that the classical covering formulas are novel. Exact small covering frontiers beyond b=k (such as C(9,4,2)=8) are not newly mechanized by this packet.

## Defective-start state bridge

RepairStateBridge.lean encodes only the target-state coordinate of the canonical identity-or-repair execution: a failed attempt preserves it, and a hit sets it true. The generic theorem after_true_iff proves that after N attempts it is true exactly when it was initially true or a hit occurred before N. defective_start_iff_successWithin instantiates this with the full action trace. correct_start_already_done explicitly proves the zero-attempt already-correct case. This small bridge does not mechanize the full physical state machine; the source contract must justify the identity/repair interpretation. The cover upper construction is valid from any safe initial state under the retained adequate-repair-or-identity contract.
