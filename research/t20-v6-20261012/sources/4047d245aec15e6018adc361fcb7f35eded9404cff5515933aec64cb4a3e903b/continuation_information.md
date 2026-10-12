# Apoautotic continuation: what must be preserved, and what may be reacquired?

## 1. Status and the exact question

This is a conditional mathematical supplement to the interrupted consolidation, not an approved replacement for its full report. The original every-source-line requirement remains in force. The claims below are self-contained derivations under declared finite models. Their appearance here is not a finding of historical novelty, a physical demonstration, or repository adoption.

The owner's definition is retained: **apoautosis occurs only when reachability is composed with state preservation, executable continuation, dependency exclusion, and maintained operation.** The underlying transductive faculty lets an organisation treat heterogeneous physical media as candidate interfaces to further realisations. Candidate recognition, usable interface, adequate realisation, reachable transition, and maintained continuation are different achievements.

The additional question is not whether those words can be arranged into a conjunction. It is whether a transition that meets a present operational contract can destroy the information or access required for subsequent transitions. The answer is yes in an explicit finite model. To understand the answer, one must distinguish preservation of the current task from preservation of a specified future capability family.

An initial apoautotic transition need not preserve every imaginable future opportunity. Requiring that would change the owner's definition. We therefore call the stronger, explicitly indexed claim **future-capability-preserving apoautosis**, and use **recursive apoautosis** only when an iteration policy and its preservation/progress obligations are supplied.

Source basis: The Last Moat, Edition 3 (LM3), §§6, 12, 14, 15 and 18, already separates realisation, migration, support exclusion, viability and progress. Graded Representations, Witnessed Revision, and Inquiry Landscapes (GF1), §11, already separates present adequacy from future-safe abstraction. Information, Composition, and Self-Revision v5 (ICS5), §5, already distinguishes immediate access from a reachable repertoire and handles destructive inquiry. The Cost of a Decisive Revision (CDR), §§2–3, already prices evidence and denies universal sufficiency to an unrestricted lossy record. These are ancestors, not discoveries of this supplement.

## 2. The contract must say what continues

Write a task contract as K=(Q,I,O,Delta,Lambda), with admitted histories, state/output semantics, timing, disturbances, resource accounting and permission conditions fixed separately. A physical realisation r has state x, an operative state abstraction rho_r, a transition Phi_r and an operative readout lambda_r. The familiar exact obligations are

    rho_r(Phi_r(x,a)) = Delta(rho_r(x),a),
    lambda_r(x) = Lambda(rho_r(x)).

A migration mu_rs has the additional obligation

    rho_s(mu_rs(x)) = rho_r(x).

Those equations apply on their certified domains, with admitted input ordering and side effects preserved. Neither equality of current displays nor equality of benchmark scores is a substitute. LM3 §§6.1, 6.4–6.7 and 14.1 supplies this foundation.

The resource boundary includes preparation, input coupling, observation, control, calibration, timing, memory, power, repair and maintenance whenever they are needed. Excluding an original host H means excluding its required support after cutover; it does not mean absence of all physical support. LM3 §§13.3 and 15 makes this distinction explicit.

Let z include the operative physical state, available evidence, resource levels, configuration identities and applicable authority. Let F be a declared family of later tasks. Current continuation concerns K. Future capability concerns whether the post-transition z still permits an acceptable policy for each specified member of F. F is a target family, not an assertion that every conceivable future inquiry will remain possible.

The same contract distinction also prevents a computational shortcut: a decoder that secretly consults an excluded host, a reference log, or a source-dependent controller is part of the implementation. Its information does not become free merely because it is outside the newly named processor.

## 3. A finite counterexample: the current task survives, the next discrimination does not

The organisation presently stores a parity bit b. Its current contract is to retain b, update it by XOR on admitted inputs, and report it correctly. A migration copies b to an independently supported realisation. Assume the required input, output, timing and maintenance obligations for this small contract hold.

The organisation also has access to a sensor whose response to a later environmental bit c is

    y = c XOR k,

where k is a fixed but initially calibrated polarity bit. Before migration, the organisation knows k. The selected migration preserves b but discards k, and the old calibration record belongs to the excluded host.

The current parity contract can still be realised exactly. But after migration, observing y=0 is compatible with (c,k)=(0,0) and (c,k)=(1,1). The required answer c differs. A method restricted to this observation cannot uniformly recover c.

This is not a failure of the parity migration theorem. The lost polarity was not included in that narrow contract. It is a failure of a stronger claim that the organisation retained the specified future discrimination capability. The distinction matters when that discrimination is needed to assess or control another realisation.

There are two different repairs:

1. Preserve the calibrated k in an operative, independently supported record.
2. Retain a lawful, reliable reference interface that can expose k after migration, for example the stipulated response to a known reference input c=0.

The second repair is unavailable when the reference actuator itself depended on the removed host. A mathematical statement that such a reference experiment would be informative does not establish that it remains physically executable.

This example combines the unknown-polarity obstruction in LM3 §9.4 with its host-exclusion account and GF1 §11's future-adequacy distinction. It is classified as **SAME_MECHANISM_NEW_CONSEQUENCE / APPLICATION**, pending comparison with the complete frontier corpus. No new physical device or channel is claimed.

## 4. Relation-valued selection: enough information need not identify the world

Fix a finite nonempty situation set W and a finite candidate set C. For each w in W, let A(w) be a nonempty subset of C: the candidates acceptable in that situation under the fixed contract. These sets are model inputs. Their physical accuracy, normative legitimacy and evidence basis are not inferred from the notation.

For a nonempty residual possibility set B, define

    Common(B) = intersection of A(w) over w in B.

A single candidate can be selected soundly on the present evidence exactly when Common(B) is nonempty. Complete identification of w is sufficient but not necessary.

This is the same essential selection problem that stage one proposed for evidence-limited equilibrium choice. A candidate c may be a strategy profile, an approved revision, a stipulated migration plan, or a continuation configuration. These are different typed applications; they are not physically interchangeable just because the same finite decision relation can represent them.

Define the covering number

    kappa(A) = min {|D| : D subset C and, for every w in W, D intersects A(w)}.

It is finite because W and C are finite and every A(w) is nonempty. Equivalently, the sets W_c={w:c in A(w)} admit a minimum cover of W with kappa(A) selected candidates.

### Proposition 4.1 — Exact retained-state requirement without later observation

Suppose an unrestricted encoder e:W->Z may be chosen, and a fixed decoder selects d(e(w)) in A(w). Then the smallest possible number of nonempty record values is kappa(A). Consequently a fixed-length binary record needs at least ceil(log2(kappa(A))) bits, and that many suffice in this unrestricted finite encoding model.

**Proof.** Each nonempty record fibre must have a common acceptable candidate, namely its decoded value. The distinct decoded candidates cover W, so there must be at least kappa(A) nonempty fibres. Conversely choose a cover D of size kappa(A), and encode each w by one selected c in D intersect A(w). The decoder returns c. This gives at most kappa(A) values, hence exactly the minimum by the lower bound. Standard binary labels encode this many values in the stated fixed length. ∎

The proposition is an elementary covering argument. It does not prove that the encoder can be built at a stated physical cost, that the input w is initially known, or that a physical replacement can store the record robustly. The encoder may be computationally expensive, and its access to w must be justified in an application.

### Why pairwise compatibility is insufficient

Take three situations with acceptable sets

    A(1)={a,b}, A(2)={b,c}, A(3)={a,c}.

Every pair has a common acceptable candidate, but all three together do not. There is no zero-information uniformly acceptable selection. Yet kappa(A)=2, not 3: two candidate values suffice to cover the three situations.

A graph connecting only pairs with disjoint acceptable sets has no edges here and misses the obstruction. An exact description uses the hyperedges B for which Common(B) is empty, or directly uses the covering problem. Neither pairwise compatibility nor world-identification cardinality gives the correct answer in general.

## 5. A retained-information plus reacquisition bound — for one fixed target

The following result has a deliberately narrow information model. There is one fixed decision relation A. An initial retained record has at most m nonempty values. After reading it, a deterministic observation-based policy performs at most d binary probes on any run, then selects a candidate. All information entering that policy must be represented in the record or in the probe responses. In particular, controller initial state, destination identity, timing signals and advice cannot carry uncounted w-dependent information.

### Proposition 5.1 — Necessary fixed-target leaf bound

If the policy always terminates within d binary probes and always selects an element of A(w), then

    kappa(A) <= m * 2^d.

If the retained record is b fixed-length binary bits, then

    b+d >= ceil(log2(kappa(A))).

**Proof.** For each possible retained value, the policy is a binary decision tree of depth at most d and therefore has at most 2^d leaves. A leaf's output must be acceptable for every initial situation producing that leaf. Selecting the output associated with every nonempty leaf gives a cover of W by at most m*2^d candidate values. The definition of kappa gives the inequality. The bit form follows from m<=2^b and integrality of b+d. ∎

Variable-length trees cause no difficulty when d is a worst-case depth bound. Expected depth alone is not the same premise. Randomisation with a positive error allowance requires a different theorem. A probe with many response values cannot be counted as one bit. A real-valued observation without a precision model is outside the finite binary accounting.

### Necessity is not sufficiency for an actual repertoire

Let W={0,1}, A(0)={0}, A(1)={1}. Suppose no initial record is retained and every permitted probe returns the same symbol in both situations. Taking d=1 satisfies the numerical inequality 0+1>=1, but no permitted policy can decide the target. The required branching capacity exists in the abstract binary-tree bound, not in the available observations.

With entirely unrestricted noiseless binary questions, the cover index in Proposition 4.1 can be communicated in ceil(log2(kappa(A))) bits. That establishes a tight abstract information bound. It does not establish a physical transducer or a permitted query interface.

## 6. The important quantifier repair: a future question is not a simultaneous answer vector

A future-capability claim often says: **after a question q is supplied, the organisation can answer that question.** It need not say: **the organisation can produce answers to every possible question using one shared d-bit observation transcript.** Applying Proposition 5.1 to the second task while describing the first is an error.

Let W={0,1}^k and let a later query q be any coordinate in {1,...,k}. The requested answer is w_q. Suppose that after migration the organisation retains no w-dependent record but still has an exact, lawful interface for reading the requested coordinate. It needs one binary response to answer any particular query, independently of k.

Thus it can have

    retained bits b=0,
    worst-case probes per requested coordinate d=1,
    arbitrary k>=2.

Nevertheless answering **all k coordinates at once**, without more observations, requires k bits in the unrestricted zero-error model. The inequality b+d>=k is false for the first task and correct for the second. The difference is the quantifier and accounting horizon, not a contradiction in information theory.

### Proposition 6.1 — No-probe preservation of a future task family

For a finite future query set Q and nonempty acceptable answer sets A_q(w), define the set of complete acceptable answer policies at w by

    A_F(w) = product over q in Q of A_q(w).

A retained record supports every q without any subsequent observation exactly when each of its fibres B satisfies

    for every q in Q, intersection over w in B of A_q(w) is nonempty.

The minimum number of unrestricted record values is kappa(A_F).

**Proof.** A decoder receiving the retained value and q supplies one answer for each q. Those answers form a complete answer policy. Such a policy is acceptable for every w in a record fibre exactly under the displayed coordinatewise intersection condition. Apply Proposition 4.1 to the candidate space of complete answer policies. ∎

For coordinate queries on bit strings, no-probe decoding of every coordinate makes the record injective, so k bits are required. When later q-specific probes are available, the product-policy covering number does **not** automatically yield a b+d lower bound with d interpreted as a per-query budget. Distinct q values may use distinct experiments and distinct transcripts.

This matters directly to apoautosis. A replacement can preserve future capability by retaining either the relevant information or appropriately accessible means of acquiring it. But one must specify whether the capability is a one-query service, a sequence of requests with cumulative resource consumption, or simultaneous recovery of a complete future-relevant state.

The exact family problem with a fixed observation repertoire is closer to a data-structure or interactive decision problem than to one unqualified state-size formula. No general optimal tradeoff for that stronger problem is claimed here.

## 7. Destructive inquiry and current feasibility

The leaf bound remains a necessary information constraint for a fixed initial-state target even when probes alter the system, provided that the actual observable branches are still counted. It does not become sufficient. A probe may disclose a bit while destroying the ability to perform the selected continuation.

Use a labelled belief B consisting of pairs (w,x), where w identifies the relevant initial situation and x is the current operative state. A permitted action a updates x and produces an observation o. If the transition depends on w, that dependence belongs in the specified transition map. The successor belief retains all compatible pairs with the same observation.

At a terminal belief, selection of c requires both

    c in A(w) for every (w,x) in B,

and the declared current executability/permission condition for c at each x. It is usually cleaner to put both requirements into a single versioned relation Good(w,x,c), while retaining which part concerns the original target and which concerns present resources.

For a bounded number of actions, define winning beliefs by backward induction. W_0 contains exactly the terminal beliefs admitting a common currently acceptable candidate. W_{n+1} adds beliefs with an action legal throughout the belief, preserving all required invariants, and taking every nonempty observation branch into W_n. Then membership in W_n characterises uniformly successful policies of at most n actions under this finite deterministic model.

**Proof sketch with its full dependency.** A terminal witness gives the zero-action policy. At positive rank, choose the witnessing action and continue with the corresponding smaller-rank policy; every possible observation was included. Conversely any bounded successful policy has a first action legal on all compatible states, and each continuation has one less remaining action. Induction recovers membership. This is standard finite backward reachability, not a novel game-solving theorem. ∎

A cheap observation cannot be treated as free when it consumes a battery, alters a calibration, destroys a sample, or removes an interface needed for the intended transition. ICS5 §5.3 already supplies the destructive-information side of this argument. CDR's simpler cost recurrence presupposes fixed non-destructive or resettable probes; it must not be reused unchanged for state-mutating experiments.

## 8. From one transition to recursive apoautosis

Define a candidate transition record at a declared boundary to include:

- current and target realisation identities and classes;
- the operational contract and its current state;
- the actual accessible input/readout/control interfaces;
- a state/export relation preserving the declared future behaviour;
- the exact original support H being excluded;
- the complete post-cutover support account at the declared scope;
- applicable evidence, calibration, error and timing bounds;
- a continuation policy meeting safety and required progress;
- the future task family F whose capability is claimed to persist;
- current permission and contract-permitted termination.

This list is a proposed assessment interface, not an adopted schema and not evidence that an implementation satisfies it. It must be compared with the existing core, frontier schemas and LM3 contracts before any claim of additional expressiveness.

For a finite sequence of transitions, a sufficient compositional argument is straightforward: each transition preserves K and maps its admitted pre-state into a certified domain of the next realisation; the future tasks needed for the next transition remain decidable and executable there; support exclusion is checked against the cumulative specified exclusion boundary; and each step meets timing and progress conditions. Induction gives the stated finite continuation.

For indefinite recursion, finite induction is not enough. Resource replenishment, absence of unhandled accumulation of transitions, continued availability, future observation sufficiency and a viable policy need their own arguments. The definition does not supply them. Nor does the existence of a replacement for each individual support imply a simultaneous support-free realisation.

A particularly useful negative control is to preserve the current task perfectly while disabling the only reference input required to calibrate the next medium. That control refutes a recursive-capability claim without refuting the successful first migration.

## 9. What this does and does not add to the equilibrium synthesis

The shared mathematical object is an evidence-limited selection relation, not an identification of physical and strategic objects. In an equilibrium application, let candidates be profiles from a justified finite library and let

    A(w) = {p : p meets the declared epsilon-Nash and joint-feasibility conditions in G_w}.

In a continuation application, let candidates be specified continuation plans with contract and support conditions. The Common(B) condition tests which candidate can be selected uniformly on existing information in either application. Additional dynamics determine whether a decentralised household or organisation actually selects it.

GF1 §8 already proves conditional mixed-Nash existence and payoff-error regret transport. Its theorem expressly supplies neither selection nor convergence. The frontier manuscripts must determine how much of the evidence-limited extension is already present. This supplement does not replace that source comparison with an absence claim.

A fixed potential game with asynchronous certified improvements is one possible selection dynamics. Random-scan logit dynamics is another specified stochastic model. Neither follows from the existence of a payoff tensor. A stationary law over visited joint states may be correlated; multiplying its marginals generally changes the law and may change regrets. Its status cannot be decided by calling both objects mixed strategies.

The owner's PoLA statement remains a probabilistic/explanatory hypothesis about why agent adaptation might favour economical trajectories under compatibility and roughly stable constraints. This supplement neither derives that tendency from physical stationary action nor dismisses it for lacking a direct derivation. It identifies evidence, preservation and policy conditions that an instantiated explanation must respect.

## 10. Meniscus relevance, without a false promotion

The recovered programme charter requires a substantive central result, a real comparison with prior work and strong rivals, integration across at least three milestones, custody, no candidate-specific blocking defect, a frozen packet, a cold audit, repair and a distinct fresh rereview. It explicitly rejects artifact volume, generic fibre lemmas and isolated nonimplications as sufficient evidence of a meniscus break.

The proposed continuation problem has real connections to M3 (dynamic state and representation), M4 (diagnosis and access), M5 (identity and provenance), M6 (transport/adoption/execution), M9 (support-robust temporal continuation), M12 (source-to-world bridges) and M14 (formal/executable checks). These are dependency connections, not completed milestones.

The central research target worth pursuing is an exact characterisation, or a sharp resource bound, for preserving a specified family of future decisions and continuations across support-changing transitions under a restricted, possibly destructive observation repertoire. The bound should account for retained records, post-transition observation access, joint support failures, current executability and a fixed request horizon.

This target must face the strongest ordinary alternatives: contract/refinement methods, finite belief-state reachability, zero-error communication and decision/data-structure complexity. A notational repackaging would not meet the charter. The elementary cover and tree results above are useful components and falsifiers; their standard mechanisms are explicitly acknowledged.

The metaphysical lane is not silently replaced by this engineering target. Nothing in these finite models establishes a necessary being, a numerical identity of conscious subjects, intrinsic intentionality, or a privileged tensor ontology. Those questions remain under the programme's separately warranted bridge and rival obligations.

## 11. Adversarial checkpoints for the next full audit

The following claims must be rejected wherever they occur in a candidate, unless their missing premises are supplied:

- A finite equilibrium theorem predicts actual adaptive convergence.
- A current-state equivalence certificate preserves every future task.
- One per-query observation budget can be added to stored bits to bound simultaneous recovery of an entire future-answer vector.
- Pairwise acceptable-selection overlap guarantees a global common selection.
- A numerical information budget proves the required probes exist.
- A probe can consume a needed resource without changing terminal feasibility.
- The choice of destination, timing, controller state or stored advice is information-free even when it depends on the source state.
- A successful first apoautotic transition establishes indefinite recursive capability.
- A state-preserving abstract map certifies an actual physical apparatus.
- Passing synthetic checks supplies independent novelty, source coverage, empirical benefit or adoption.

The exact verifier accompanying this supplement checks finite instances and counterexamples of the explicitly stated models. It uses ordinary Python with explicit failure exceptions. Its results are deliberately separate from the overall consolidation gate.

## 12. Source anchors and provenance limits

[LM3] The Last Moat, Third Edition, 10 September 2026, supplied PDF: §§6.1 and 6.4–6.7 (contract and operative realisation); §9.4 (unknown polarity); §12.4 (inadequate export); §14 (continuation); §15 (relative support); §§18.1–18.4 (reachability, viability, progress).

[GF1] Graded Representations, Witnessed Revision, and Inquiry Landscapes, Version 1, 8 September 2026, supplied formalisation PDF: §§8.1–8.5 (game declaration, feasibility, equilibrium, regret); §§10.2 and 10.12 (declared dynamics and hybrid scope); §11 (future-safe abstraction).

[ICS5] Information, Composition, and Self-Revision, Local Descriptions and Operative Access, supplied v5 PDF: §5.2 (reconnection and immediate/reachable access); §5.3 (initial labels and destructive inquiry); §§5.4–5.5 (version-sensitive acceptance and authority).

[CDR] The Cost of a Decisive Revision, Evidence, Reuse, and Self-Application, supplied PDF: §2 (fixed-target evidence cost); §3 (future insufficiency and changing objectives); §4 (delivery costs).

[CORE] theislampill/orthemology, theory/orthemic-core-formalization.md, observed commit f50dc1aee52356cc6adbef342387576b02afc124: §§2–5.

[CHARTER] Same pinned repository, docs/project-closure/ar8r-v11/programs/AR8R-ORTHEMOLOGY-MENISCUS-MILESTONE-ARCHITECTURE-V1.md: §§II, V, VII and IX. This is an owner-supplied research charter with its own non-adoptive status, not an automatic authority for new theorem adoption.

The interrupted attempt's source reads and candidate files are preserved separately. This supplement does not count them as newly reread merely because they have been copied into a recovery archive.
