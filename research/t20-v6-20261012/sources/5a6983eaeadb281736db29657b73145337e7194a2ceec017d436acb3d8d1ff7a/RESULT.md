# Exact stopping under stochastic inquiry: the hidden-state continuation boundary

10 October 2026 UTC. Additive scratch-only research. Written mathematics and exact finite executable controls; no new kernel verification, source-authentication result, human-knowledge impossibility, protected edit, integration or T20 closure.

## Result first

**The exact finite-decision question can now be answered for arbitrary finite hidden-state stochastic instruments, even when an action creates several hidden successors under the same visible receipt.** A greatest-fixed-point algorithm decides whether one lawful observation-history policy can eventually issue a correct initial-label verdict with probability one. It retains the initial target through destructive state changes, intersects permissions over every currently possible state, and tests progress on **actual labelled state × current support**, rather than assigning fictitious fixed probabilities to a graph of supports.

This is a targeted extension of the named H-ICS sure-decision interface, using classical qualitative POMDP reasoning. It is not a newly invented general reachability mechanism. The earlier programme already has sophisticated almost-sure hidden-model/observed-state control, a posterior-deterministic (PD) embedding, and finite-history zero-error impossibility. Those are expressly preserved. The present statement removes the PD restriction for the narrower objective of observable, zero-error, finite stopping; it does not extend their general hidden parity or finite-cost theorems.

The actual recent audit instrument gives a useful application: all five reachable supports after the report Y=1 retain both target values, so no exact terminating verdict exists under repeated readings of that fixed imperfect audit. The four-mass known-Bad quotient has the same stopping result. Fresh imperfect verifiers change posteriors but still cannot create a finite zero-error verdict. A perfect comparator can; a repeated partially revealing comparator can permit almost-sure stopping without any uniform finite depth. These are distinct acquisition contracts. The probabilities remain stipulated model inputs, not actual source reliability estimates.

## 1. What was already owned, including the broader successor work

The comparison was not limited to H-ICS.

1. H-ICS v5, “A strategy must preserve the needed distinctions,” gives the finite deterministic labelled-belief attractor. Its target is an initial label; its destructive experiment explicitly keeps two opposite labels at one observed current sink. The paragraph after the theorem reserves noise, stochasticity and state-dependent permissions for further arguments.
2. H-Continuation Theorem 2 already carries stochastic instruments, branch probabilities, target numerators, positive-branch normalization and bounded policy expectations. The 10 October audit-continuation packet implements this on the actual source-audit example and adds posterior-only continuation equivalence. These answer what a state must preserve; they do not supply this exact-stopping policy-existence algorithm for arbitrary evolving hidden states.
3. The v5 continuation registry and the PD review preserve a general common-policy parity criterion with finite hidden model, fully observed evolving state and hard menus. The PD embedding specifically requires at most one positive successor for each (hidden state, action, observation). Its public descriptor keeps each possible initial tag's unique current state and the last observation. Its complexity and law-transport achievements are not rediscovered here.
4. The historical-mathematical-transport report, §4, already proves finite-history mutual-absolute-continuity obstruction to zero-error stopping, including shared randomized adaptive policies and continuous command spaces. The controlled-restoration source already separates eventual correct conduct from a finite zero-error declaration, treats root copies versus fresh samples, and preserves common permission constraints. The positive-likelihood argument below is an audit-specific application of that inheritance.
5. The older measure, atomicity and productive-observer results address different questions; almost-sure statements were already first-class mathematics. This packet does not introduce probability-one reasoning to the programme.

Exact retained inputs are listed in INPUT_BINDINGS.json. Broader repository searches for “almost-sure,” “hidden-state,” “posterior-deterministic embedding,” “finite stopping,” “zero-error,” and “belief-support” identified these controlling predecessors. Search results are discovery aids, not proof of corpus-wide absence. The new-to-this-operation claim concerns the explicit theorem/interface and application below, not historical priority or an exhaustive inventory of every project result.

The proposed all-proper-score/Blackwell route was also screened. It would mainly restate classical posterior-law determination and inherited observable closure. It was not developed as a new contribution.

## 2. The actual contract

Let X be a nonempty finite set of **labelled hidden states**, A a finite action set and O a finite observation alphabet. A state x includes an immutable answer label b(x) in a finite set L. If the physical state can change or merge, use pairs (physical state, initial answer), rather than relabelling the current physical state after the fact. The target need not identify every initial state: it can be any finite decision about it.

For every action a legal at x, the supplied joint kernel

    K_a(o,x' | x) >= 0,       sum_(o,x') K_a(o,x' | x) = 1

satisfies K_a(o,x'|x)>0 only if b(x')=b(x). The controller sees its chosen actions and receipts o, not x. Kernels are time-homogeneous, conditional on the actual current hidden state and action. This is the Markov instrument contract, not an assumption that observed outputs are independently redrawn. History-dependent availability can be included as a finite state component when justified.

Fix a nonempty initial support B0⊆X. A compatible initial probability gives every x∈B0 positive mass and zero elsewhere. “One policy” means the same observation-history policy under every possible initial x. It may use arbitrary memory and independent private randomization; its seed cannot encode the hidden state. Since B0 is finite with positive weights, almost-sure correctness and stopping under that mixture are equivalent to those properties under every x∈B0 separately, for the same policy. Zero-prior states are not silently added.

At a feasible finite history the exact support is B. Define:

    Legal(B) = intersection_(x∈B) Legal(x)
    Post(B,a,o) = {x' : some x∈B has K_a(o,x'|x)>0}.

Only nonempty successors occur. A permitted action must lie in Legal(B). This is robust model-relative permission on every live possibility. A high posterior probability of permission is not a substitute. A refusal can be modelled as a receipt only when attempting the action is itself permitted; it cannot authorize its own prohibited probe.

Stopping and reporting a verified common label are assumed permitted at every homogeneous support; Legal(B) guards inquiry actions only. If reporting has a separate state-dependent permission, that permission must be added to the terminal predicate before applying this theorem. A support is a **goal** if b is constant on it. Stop there and return its common label. A zero-error policy cannot stop with positive probability at a mixed-label feasible history: the same action/receipt history has positive likelihood under an opposite-label possibility, which gives a positive error probability. Conversely, a goal-support verdict is correct under every live possibility. Thus exact stopping is precisely reaching an observable homogeneous-support goal.

The goal is a declared error-free decision contract. It is not a definition of epistemic knowledge, warrant, justified reliance or sufficient practical confidence.

Let F be the finite family of nonempty supports reachable from B0 under all robustly legal actions, stopping exploration at goals. Equivalently one may use all nonempty subsets of X. Reachable restriction reduces work without restricting any admissible policy before its first goal. At most 2^|X|−1 supports are needed.

## 3. Sure stopping and almost-sure stopping are different questions

### 3.1 Sure finite stopping

Let W0 be the goals and set

    W_(k+1) = W_k union {B∈F : some a∈Legal(B) has every
                            nonempty Post(B,a,o) in W_k}.

Then B0 belongs to the limiting least fixed point iff a sound policy terminates on every supported path. The least rank supplies a finite uniform depth; choose a rank-decreasing action.

For necessity, a deterministic observation-policy tree has finite branching. If all its supported paths terminate, König's lemma gives a finite maximum depth; induction on depth gives membership in the attractor. Supported observation prefixes of arbitrary length have consistent hidden-state realizations by finite branching, so one cannot dismiss an infinite branch merely because its infinite-path probability is zero. Randomization cannot improve this pathwise guarantee: if every choice in its action support must succeed, select one such action at each history. This is the finite stochastic support version of H-ICS's inherited sure attractor, with its semantics made explicit.

### 3.2 Almost-surely finite, zero-error stopping

Here a nonterminating supported infinite path is allowed only if its probability is zero. No common deterministic upper bound on the stopping time is promised. The least sure attractor can therefore reject a genuinely almost-surely solvable problem.

Nor can one simply turn the support-update graph into a finite Markov chain by assigning fixed positive probabilities to all its edges. The posterior weights inside a recurring support change. A receipt can remain possible at every finite stage while its conditional probability tends to zero quickly enough to leave a positive chance of never receiving it. Section 6 supplies an exact instance.

## 4. A complete qualitative algorithm for arbitrary hidden-state instruments

For R⊆F containing its retained goals define

    Safe_R(B) = {a∈Legal(B) : every nonempty Post(B,a,o) lies in R}.

“Safe” here means remaining inside the candidate winning region and respecting the declared menu. It is not a new physical safety or moral judgment.

Construct a finite directed graph G_R:

- Vertices are (x,B) with B∈R and x∈B.
- Every vertex whose B is a goal is terminal-success.
- From a non-goal (x,B), put an edge to (x',B') whenever some a∈Safe_R(B) and receipt o have K_a(o,x'|x)>0 and B'=Post(B,a,o).

The actual x component is used by the offline correctness test. It is **not given to the controller**. Its role is to avoid confusing a receipt possible from some other state in B with one possible from this actual x.

Let Phi(R) consist of those B∈R for which **every x∈B** has a directed path from (x,B) to a goal vertex in G_R. A goal has a length-zero path. Non-goals with no safe actions are rejected.

Starting from R0=F, repeatedly set R_(k+1)=Phi(R_k), recomputing safe actions and graph paths after each deletion. Phi is monotone and contracting. Finiteness gives a stable region R∞ after at most |F| strict deletion rounds.

### Theorem: exact almost-sure stopping criterion

For the stated finite fixed-kernel model, the following are equivalent:

1. Some lawful observation-history policy, allowing arbitrary memory and independent randomization, stops almost surely and returns the correct initial answer with zero error from every x∈B0.
2. B0∈R∞.
3. The policy that keeps only the current support B, stops at homogeneous B, and otherwise chooses uniformly among Safe_R∞(B) succeeds as in (1).

Thus support memory and stationary randomized action selection suffice for this objective, although a Markov chain on supports alone is not the correctness proof.

### Proof: fixed point gives a real policy

At the stable region, every non-goal B has a nonempty safe menu. The stated controller uses B and a fresh independent random action only. Under the actual instrument, the pair (x,B) is a finite Markov chain. Its positive transition edges are exactly G_R∞, and safe menus make R∞ closed until stopping. All its vertices have paths to goals by the fixed-point condition.

A finite Markov chain with a path to an absorbing goal from every state hits a goal with probability one. Explicitly, choose for each non-goal a simple positive-probability path to a goal. Their finitely many lengths have a finite maximum N, and their finitely many path probabilities have a positive minimum epsilon. Conditional on any uncompleted history, the chance of reaching a goal within N further steps is at least epsilon. Therefore survival beyond kN is at most (1−epsilon)^k, which tends to zero. At a goal the label is correct. This proves (2)⇒(3)⇒(1).

This argument uses actual fixed transition probabilities on the **product chain**, including the controller's fixed positive action probabilities. It does not assume a uniform lower bound on receipt probabilities conditional only on a possibly changing posterior. It implies finite expectation for this constructed finite-chain witness, but supplies no useful uniform numerical runtime across arbitrary kernels and makes no cost-optimization claim.

### Proof: arbitrary-history winners are never pruned

Let W⊆F be all supports from which some single lawful history policy achieves the contract. Winningness depends only on support, not on the exact positive initial weights: for one fixed policy, success probability one under a finite full-support mixture implies success probability one from each constituent state, and conversely.

A positive-probability feasible continuation of a winning policy is again winning from its updated full support. Otherwise at least one supported current state would have positive conditional failure under that continuation, giving positive failure for the original policy. Consequently every action used with positive probability by a winning policy has all its positive-receipt successors in W. It is in Safe_W(B).

Fix any B∈W and x∈B. The winning policy reaches a goal in finite time with probability one from x, so it reaches one by some finite time with positive probability. Finite state/action/receipt branching supplies a positive finite path; along it every policy action lies in Safe_W at the corresponding support. Thus (x,B) has a goal path in G_W. This holds for every x, so W⊆Phi(W). The reverse inclusion is automatic from contraction, hence W is a fixed point.

Inductively, if W⊆R_k, its safe actions and goal paths are also allowed in G_Rk. No member of W is deleted; therefore W⊆R∞. In particular (1) implies (2).

An arbitrary independent seed does not invalidate the argument. With finite observable histories and perfect recall, use the shared behavioral action kernel conditional on that history; the environment likelihood conditional on the recorded actions is independent of the seed and cancels from its conditional distribution. Equivalently retain the common seed when disintegrating the finitely supported histories. A seed carrying hidden-state information is excluded by the contract. ∎

### Effective scope

An exact explicitly supplied rational kernel makes positivity, support updates, legal-menu intersections and graph reachability decidable. After support enumeration each fixed-point round uses finite graph operations. There is no need to calculate posterior probabilities or optimize a score. The algorithm is exponential-size in the hidden-state count; no novel complexity lower bound or sharp complexity classification is claimed. Arbitrary unspecified real numbers do not provide effective zero tests.

The theorem has a narrower objective than general hidden parity. It does not establish a finite-memory result for every liveness property, guarantee success against an adversarial choice of zero-measure paths, or support unknown/drifting transition probabilities.

## 5. A genuine separation from the inherited PD scope

Use labelled states x0,x1 of initial label 0 and x2 of initial label 1, with initial support {x0,x2}. One legal action has these positive-probability cells:

- At x0: (x0,wait) with 1/4, (x1,wait) with 1/4, (x0,reveal0) with 1/2
- At x1: (x1,reveal0) with probability one
- At x2: (x2,wait) with 1/2, (x2,reveal1) with 1/2

After the first wait, the support is {x0,x1,x2}. Receipt reveal0 certifies only the requested initial label, not necessarily the exact hidden state; reveal1 certifies label 1. Every step reveals with probability at least 1/2. Stop at the first revelation. Starting at x0, survival after n>=1 steps is 2·4^−n; starting at x2 it is 2^−n. Thus the algorithm accepts almost-sure stopping and rejects sure finite stopping. The hidden branch is consequential: P(next wait | x0)=1/2, whereas P(next wait | x1)=0. These are not duplicate states with identical future observation laws.

Crucially, the triple (x0,action,wait) has **two** positive successors, x0 and x1. The old PD initial-tag descriptor cannot assign that initial tag one uniquely determined current state from the observation history. The new algorithm does not assume that uniqueness. This is an exact, consequential hypothesis separation: merging x0 and x1 would discard their different next-receipt probabilities. No impossibility of every alternative PD representation is claimed. The general proof and implementation accept arbitrary positive branching without requiring a special representation transformation to be found or warranted.

This example is a theorem control, not an additional source-reliability or cognitive model. The target label is deliberately coarser than hidden-state identity, matching the decision-relative H-ICS contract.

## 6. Why the support-only Markov shortcut is unsound

Let a,b be static opposite labels, with prior 1/2 each. One repeated action emits reveal-a with probability 1/2 under a and never under b; it emits wait otherwise. Every finite wait string leaves support {a,b}. The support graph has a wait self-edge and a goal edge to {a}.

However, after n waits,

    P(no reveal by n) = 1/2 + 2^(−n−1),
    P(next reveal | wait^n) = 1 / [2(2^n+1)].

The survival probability tends to 1/2. The support graph equipped with any fixed positive probability on its reveal edge would predict survival tending to zero and would be wrong. In the product graph, (b,{a,b}) has no path to a goal and remains a closed nonterminal class. The algorithm correctly rejects the initial support.

Adding reveal-b with probability 1/2 under b gives the two-sided control. Survival becomes 2^−n, so almost-sure stopping is possible, while the supported all-wait path defeats sure stopping and every deterministic finite-depth bound. A perfect version with no wait receipt has sure rank one.

These controls arose in shared root/worker derivation; they are not independent proof reviews. The parent supplied the displayed probability controls, which this packet independently recalculates. Their general mechanisms are classical.

## 7. Executed transport to the current source-audit model

The existing source-audit model has X=(Theta,T,Y,V), all binary. T=Good or Bad; Theta and T are independent and uniform; Y is 9/10 accurate under Good and 1/2 accurate under Bad; the independent comparator V is 4/5 accurate. The observed audit is A=(T,1[V!=Y]). These are the inherited model assumptions.

After Y=1 the eight possible hidden states all have positive probability. Reading the **same fixed** A is a diagonal projector, hence it does not redraw V or T. The reachable support family has five elements: the initial eight-state support and its four audit cells. Every audit cell still contains Theta=0 and Theta=1. There is no homogeneous goal support, and both the sure and almost-sure solvers reject. The familiar Bad/disagree posterior remains exactly 1/5; this is already a valid forecast, not an unsuccessful attempt to produce a theorem of Theta=0.

On the known-Bad slice the retained four masses of (Theta,D) have three reachable supports: the initial four-state support and two two-state audit cells. Again none is a goal. The audit quotient therefore preserves this exact-stopping verdict in addition to its previously proved predictive contract. No extra full transcript is demanded.

For **fresh** independent 4/5-accurate comparators, both receipts have positive likelihood under either target. Every finite receipt word retains both target labels. After n successive disagreements with Y=1,

    P(Theta=1 | n fresh disagreements, Bad,Y=1) = 1/(1+4^n),

so n=2 gives 1/17 rather than the fixed-reread 1/5. Nonetheless no finite word reaches an exact goal. The general randomized-stopping obstruction is inherited from the prior finite-history absolute-continuity theorem; the new work is the explicit same-interface application and exact solver check.

Distinct independent likelihoods may support almost-sure limiting learning. Such a limit does not turn any finite positive-likelihood history into a zero-error stopping certificate. This contrast does not establish that human knowledge requires posterior probability one, nor that rational inquiry or ordinary warranted reliance must continue indefinitely.

A **perfect** comparator at known Y, with D=1[V!=Y] and V=Theta, gives Theta=Y xor D and a rank-one exact verdict. That is a changed observation premise, not a certificate derived from repeatedly inspecting the imperfect one. The partially revealing controls of §6 provide the middle regime of zero-error, almost-sure finite stopping without a finite uniform depth.

## 8. Classical ancestry and source-use limits

The primary comparison is Chatterjee, Chmelik, Gupta and Kanodia, *Optimal Cost Almost-sure Reachability in POMDPs*, arXiv:1411.3880, definitions and §4.2, Lemmas 5–6 and their proofs. The inspected proof uses allowed actions and the induced Markov chain on actual state/support pairs. This is direct ancestry for the method. No cost-optimization or claimed complexity result from that paper is imported. Its shorthand reference to a “belief-support MDP” is not used to justify the false fixed-edge-probability shortcut in §6.

The initial-label augmentation, homogeneous stopping target, robust state menus and application to the current audit instrument are explicitly supplied here. They specialize classical reachability to the exact information-preservation task. H-ICS remains the internal source for preserving initial labels through destructive operations. H-Continuation and the current audit result remain the sources for the numerical instruments and quotient semantics.

No complete POMDP literature survey, new field-level theorem or complete repository absence claim is made. Only the named scopes were compared. The old PD result is stronger in its objective and weaker in its transition generality; neither result simply replaces the other.

Verified primary link: https://arxiv.org/pdf/1411.3880

## 9. Verification and useful consequence

Run from this directory:

    python3 -m unittest discover -p 'test_*.py'
    python3 verify.py

The tests cover the one-sided support trap, two-sided almost-sure control, perfect rank-one control, fresh noisy obstruction, non-PD branching, universal live-state permission and destructive-label preservation. The solver was first tested against an intentionally incomplete implementation; RED.log preserves the three expected failing positive cases, and GREEN.log records their corrected run.

A separately written oracle enumerates every stationary randomized action-support assignment for each test model and directly checks the reachable actual-state/support graph. It does not consume the fixed-point solver's supports, transitions, safe menus or graph. Comparison covers all 81 static two-state/two-action support instruments, all 675 label-preserving three-state/one-action instruments, 512 seeded three-state/two-action permission instances, and the explicit non-PD fixture. Results and counts are in CONTROL_RESULTS.json. These are exact finite checks of the implementation, not a proof by enumeration of the universal theorem.

The substantive outcome is a decision procedure and lawful witness policy for a precise previously untransported interface, plus a verified obstruction to a tempting shortcut. It preserves a real positive possibility: uncertainty about the exact hidden physical state need not prevent a correct eventual answer to the requested initial-label question. Its negative audit result identifies exactly which stronger stopping guarantee the retained imperfect instruments cannot provide. It does not downgrade their valid forecasts or any earned source/philosophical warrant.

Attribution: the root and worker independently arrived at the same product fixed-point construction during this investigation, then coordinated the proof and controls; that overlap is shared authorship, not independent verification. The worker implemented the solver and policy-enumeration comparison, recovered the wider PD/control ancestry, and bound the actual audit transport. Independent review, if supplied, must identify the exact snapshot. No protected or previous source was edited.
