# T20 cross-front synthesis: operation-preserving representations
## New deductions, a finite reference construction, and explicit limits

**Status:** ordinary mathematical arguments developed for this consolidation, plus a new exact-arithmetic reference implementation. These are not new Lean proofs, not externally peer-reviewed results, and not a claim of field-wide novelty. Several constituent theorems are standard abstraction, observability or differential-geometric mathematics. The contribution claimed here is their explicit combination into a testable interface for the concrete distinctions exposed across T20.

**Source boundary:** inherited examples and results are named as such. Possible duplication of a theorem inside the large corpus has not been ruled out by an exhaustive literature or source-level novelty audit. Tool outputs became invisible in the resumed execution, so executable status belongs to the generated receipts and requires visible readback. No repository was changed.

---

## 0. The question this synthesis answers

T20 now contains results about retained proof supports, evidence withdrawal, conditional answers, inquiry value, almost-sure termination, moment realisability, computability, geometric projection and proof-system completion.

A tempting but incorrect synthesis would say that they all establish “information preservation”. That is too coarse. Each concerns a different observable or permissible operation.

A better question is:

> Given a deliberately compressed representation, what additional state must be retained so that a specified family of future operations remains faithful?

This document gives a precise finite answer, quantifies the smallest finite sidecar, and supplies a compatible geometric condition. It also proves why approximate agreement, moment positivity and low spectral variance do not replace the exact contract.

The intended use is constructive. Instead of demanding that numerical coordinates encode the entire past, retain the smallest complement needed for the operations actually in scope. Conversely, do not call that complement sufficient for operations that were never declared.

---

## 1. A finite controlled contract

Let S be a nonempty finite set of **declared information states**. Depending on the application, a state can include a current belief, retained evidence support, a proof catalogue, a source-permission configuration and a model-validity witness. We do not identify S with inaccessible physical truth unless an application establishes that interpretation.

For each s in S specify:

- a finite observable label l(s), including the verdicts or certificate statuses that must survive;
- the set A(s) of enabled actions;
- a nonnegative cost c(s,a) for each enabled action;
- a finite outcome set O;
- a kernel K_a(s,o,t) with nonnegative entries and sum over o,t equal to one.

K includes the joint distribution of the observed outcome and the next information state. This is deliberately stronger than separately retaining a conditional answer and the probability of an audit. Their correlation can matter.

A proposed compression is r:S→Z. A partition P is **contract-preserving relative to r** when states in the same block have:

1. the same r-value and required label;
2. the same enabled actions;
3. the same immediate costs for corresponding actions;
4. for every enabled a, outcome o and block C of P,

\[
\sum_{t\in C}K_a(s,o,t)=\sum_{t\in C}K_a(s',o,t).
\tag{1}
\]

The fourth condition preserves the *joint* outcome/next-block kernel. It is a branch-labelled strong lumpability or probabilistic-bisimulation condition. The name is not a novelty claim.

### Why proof support and authority appear here

If a rule is enabled only when its premise supports satisfy an ordered guard, that fact must be reflected in A(s), the relevant labels, or an adequately refined state. If withdrawing a source changes what follows next, the withdrawal kernel must preserve that distinction. If shared lemma identities change checking cost, c must reflect those identities.

The theorem does not prove that a source is authentic, that an authority is rightful, or that a premise is true. Those are interpretation obligations for the state and contract. It only prevents a faithful declared distinction from silently disappearing under compression.

---

## 2. Result D1: the coarsest future-faithful refinement exists and is computable

Start with the partition P0 induced by the joint record

\[
(r(s),\ l(s),\ A(s),\ (c(s,a))_{a\in A(s)}).
\]

Given Pi, split every block according to the vector

\[
\left(\sum_{t\in C}K_a(s,o,t)\right)_{a,o,C\in P_i}.
\tag{2}
\]

Call the new partition Pi+1. Keep splitting until no block changes.

### Theorem D1

The iteration terminates after at most |S|−|P0| strict refinements. Its final partition P* is the coarsest contract-preserving refinement of r.

### Proof

Every strict refinement increases the number of blocks, which cannot exceed |S|. Hence termination follows.

At a fixed point, required labels, actions and costs agree by the initial partition, and equation (1) holds by the stable refinement signatures. Thus P* preserves the contract.

Let E be any other contract-preserving partition refining r. It refines P0 because all the components defining P0 are constant on E-blocks. Suppose inductively that E refines Pi. Every Pi-block is a union of E-blocks. Equality of transition mass into each E-block therefore implies equality of transition mass into each Pi-block, separately for every outcome and action. Consequently E refines Pi+1. By induction it refines P*.

Thus every admissible retained representation distinguishes at least the P*-classes. The final partition is coarsest. ∎

### What this contributes to the T20 connection

T20's fibre and continuation results say which distinctions must survive a specified future inquiry. Its proof-cost, audit-value and withdrawal results show that the future contract must include more than the current answer. D1 assembles those requirements into a single finite operation-preserving refinement procedure.

It does **not** say that ordinary trace equivalence and strong bisimulation coincide. Some weaker task-specific representations can preserve a restricted query family without satisfying (1). The minimality here is relative to the stated one-step joint-kernel contract.

---

## 3. Result D2: an exact minimum for the sidecar

Suppose r is a numerical or otherwise fixed record we want to keep. Let N_z be the number of P*-blocks contained in the fibre r−1(z). We may add a finite-valued exact sidecar kappa(s).

### Theorem D2

The smallest common alphabet size for a deterministic sidecar such that (r,kappa) satisfies the contract is

\[
M_* = \max_{z\in r(S)} N_z.
\tag{3}
\]

Accordingly, the minimum fixed-length binary sidecar length is

\[
b_* = \left\lceil\log_2 M_*\right\rceil.
\tag{4}
\]

### Proof

By D1, any contract-preserving joint record must distinguish different P*-blocks. Inside a fixed r-fibre, r supplies no distinction, so kappa must have at least N_z different values. Therefore its common alphabet has size at least max N_z.

Conversely, enumerate the P*-blocks separately inside each r-fibre. Assign them distinct labels from an alphabet of size M*. The same label can be reused in another fibre, because r remains available. The joint record then identifies exactly the P*-block and hence preserves the contract. Binary encoding gives (4). ∎

### Scope of the minimum

This is a finite cardinality and fixed-length bit statement. It is not the continuous-dimension theorem from the earlier continuation paper. It does not claim compression of an arbitrary infinite history into finitely many bits, nor does it identify variable-length expected code cost.

It also depends on retaining r alongside kappa. A sidecar label on its own need not identify the refined state.

### A four-way example joining proof cost and withdrawal

Consider four states with the same visible claim:

- support A with the low shared-check price;
- support A with the high shared-check price;
- support B with the low shared-check price;
- support B with the high shared-check price.

Withdrawing A distinguishes the support dimension. Checking a bundle whose triple overlap is hidden distinguishes the price dimension. If both operations are in scope, all four states must be separated. The minimal sidecar needs two bits.

If only the present accepted claim is in scope, no such extra bit is required. If only withdrawal is added, one bit suffices. This is a concrete instance of operation-relative memory rather than a requirement to preserve the whole narrative history.

### Corollary D2.1: enlarging the contract cannot reduce this minimum

Adding actions or required labels adds constraints. The new coarsest partition refines the old one, so every old r-fibre contains at least as many new blocks. Hence M* and b* cannot decrease.

This is useful for versioned inquiry contracts. A representation that was adequate under version 1 may genuinely need augmentation under version 2 without having been defective for its original scope.

---

## 4. Result D3: the quotient preserves more than present answers

For a P*-block B, define the quotient label, action menu and cost from any representative. Define

\[
\overline K_a(B,o,C)=\sum_{t\in C}K_a(s,o,t),\quad s\in B.
\tag{5}
\]

D1 makes this independent of the representative.

### Proposition D3a: histories under retained-information policies

For every policy whose action choices depend only on the retained block/outcome history, the concrete process and quotient have the same law of all finite block/outcome histories, starting in corresponding blocks.

**Proof.** The initial retained state agrees. Conditional on any matched retained history and the action selected by the same policy, equation (5) gives the same next outcome/block distribution. Induction proves equality for every finite history. Randomised policies are covered by averaging their same action distribution. ∎

This proposition does not allow the quotient policy to use a distinction that was erased, or assume an agent observes the inaccessible hidden physical state.

### Proposition D3b: finite-horizon optimal values

For a finite fully observed contract, let terminal loss be constant on P*-blocks. The optimal finite-horizon cost is also constant on P*-blocks and equals the quotient's value. An optimal policy can be chosen on quotient states.

**Proof.** At horizon zero the claim is the terminal-loss assumption. The Bellman update is

\[
V_{h+1}(s)=\min_{a\in A(s)}\left[c(s,a)+\sum_{o,t}K_a(s,o,t)V_h(t)\right].
\]

By induction Vh is constant on blocks. Grouping the sum by blocks and using (5), together with equal action menus and costs, gives the same update for every representative and for the quotient. ∎

For partially observed applications, the relevant state must instead be a justified information state, such as a sufficient belief state. The theorem cannot be used to optimise actions from hidden information the investigator never has.

### Proposition D3c: almost-sure reachability for a fixed retained policy

Let the target be a union of quotient blocks. Then the probability of ever reaching it is preserved, including whether that probability is one.

**Proof.** The event of reaching it within h steps has the same probability by D3a. These events increase with h and their union is eventual reachability. Taking the limit proves the claim. ∎

### Why the stronger contract matters

The inherited posterior-value example preserves conditional answers but not outcome frequencies; it violates the information required by (5). The inherited stochastic-inquiry obstruction concerns a weaker retained equivalence than full joint-kernel preservation. D3 does not contradict either counterexample. It identifies sufficient additional information to prevent the corresponding failure.

---

## 5. Result D4: approximate preservation has a horizon, and rare evidence matters

Exact finite models are a reference point, not a description of all practical data. Approximation requires its own contract.

Assume equal action menus and a fixed map r. Let all concrete and quotient per-step costs lie in [0,C], terminal costs in [0,R], and suppose

\[
|c(s,a)-\overline c(r(s),a)|\le\delta,
\]

\[
\operatorname{TV}\bigl(K_a(s,\cdot,r^{-1}(\cdot)),\overline K_a(r(s),\cdot,\cdot)\bigr)\le\varepsilon,
\]

with terminal discrepancy at most eta. The TV distance is on the **joint** outcome/next-block distribution.

### Theorem D4a: finite-horizon value error

The concrete and quotient optimal h-step values satisfy

\[
|V_h(s)-\overline V_h(r(s))|
\le \eta+h\delta+
\varepsilon\left(hR+\frac{C h(h-1)}2\right).
\tag{6}
\]

### Proof

Let eh be the maximum discrepancy. At h=0 it is at most eta. For a fixed action, the cost discrepancy is at most delta. Replacing the concrete continuation value with the quotient continuation value costs at most eh−1 in expectation. The quotient continuation function lies in an interval of width at most (h−1)C+R, so replacing its transition law costs at most epsilon times that width by the elementary TV bound on expectations. Taking minima cannot enlarge the maximal fixed-action discrepancy. Thus

\[
e_h\le\delta+e_{h-1}+\varepsilon((h-1)C+R).
\]

Summation gives (6). ∎

The same bound applies to a fixed lifted quotient policy. Comparing that policy with a concrete optimum gives the usual twice-the-value-error regret bound under the same finite fully observed setup.

### No uniform infinite-horizon conclusion follows

Let an unresolved state remain unresolved with probability 1−epsilon each step and succeed with probability epsilon. For every epsilon>0, success occurs almost surely. At epsilon=0 it never occurs. The transition laws can be arbitrarily close in TV while the almost-sure claim differs completely.

Thus “the approximation is very accurate” is not a replacement for a structural infinite-horizon guarantee. A probability-one property needs an appropriate preservation condition, not a finite-horizon numerical tolerance extrapolated indefinitely.

### Theorem D4b: conditioning can amplify small errors

For probability vectors p,q and a likelihood 0≤l≤1, let both event probabilities be at least alpha>0. Then

\[
\operatorname{TV}(p(\cdot\mid l),q(\cdot\mid l))
\le \min\left(1,\frac{2\operatorname{TV}(p,q)}\alpha\right).
\tag{7}
\]

**Proof.** For any event A, write its two conditional probabilities as p(l1A)/p(l) and q(l1A)/q(l). The difference is at most TV(p,q)/p(l) from the numerator plus |p(l)−q(l)|/p(l) from normalisation. Each numerator discrepancy is bounded by TV(p,q) because the relevant function lies in [0,1]. Take the supremum over A and use p(l)≥alpha. The trivial bound one completes (7). ∎

The factor 2 is a safe bound, not a sharp-constant claim.

For a sharp qualitative obstruction, take

\[
p=(1-e,e,0),\qquad q=(1-e,0,e),\qquad l=(0,1,1).
\]

Their prior TV distance is e, but the conditioned laws have disjoint support and TV distance one. The observation has probability e in both.

### Cross-front consequence

Small state-reconstruction error, high average retained variance and close common-case predictions cannot by themselves guarantee preservation of rare decisive evidence. To obtain a quantitative posterior guarantee one needs a suitable error metric, a justified link from representation error to it, and an event-mass or other stabilising condition.

This is particularly relevant to transporting low-rank weight-space results into claims about future model correction. It is not an empirical claim that the uploaded neural-network paper fails a particular benchmark.

---

## 6. Result D5: the geometric condition for exact reduced gradient dynamics

Let U be an open subset of R^n, L:R^n→R^k have full row rank, and r(x)=Lx. Let G(x) be a smooth positive-definite metric matrix. For a smooth coarse objective j, use its pullback J(x)=j(Lx).

The negative metric gradient is

\[
X_j(x)=-G(x)^{-1}L^T\nabla j(Lx).
\]

Its projected velocity is

\[
L X_j(x)=-A(x)\nabla j(Lx),\qquad A(x)=L G(x)^{-1}L^T.
\tag{8}
\]

### Theorem D5

The projected velocity is determined by r(x) for **every** smooth j if and only if A(x) is constant on each fibre of r.

When that holds, A(x)=Abar(r(x)) defines a positive-definite coarse cometric, and the exact coarse metric is

\[
\overline G(z)=\overline A(z)^{-1}.
\tag{9}
\]

### Proof

If A factors through r, equation (8) is exactly the negative gradient field for j under the metric (9). Positivity follows because for nonzero v in R^k, L^T v is nonzero and

\[
v^T A(x)v=(L^Tv)^T G(x)^{-1}(L^Tv)>0.
\]

Smooth factorisation follows locally through linear sections and is consistent globally because A is constant on fibres.

Conversely, choose j(z)=z_i for each coordinate i. Its projected field is the negative ith column of A(x). If these fields are determined by r(x), every column is constant on fibres. ∎

### What the theorem does not say

For one fixed objective, the condition can be weaker: differences in A may be invisible in that objective's gradient direction. The necessity above uses all smooth coarse objectives.

The metric must be positive definite for this Riemannian interpretation. Invertibility alone is insufficient. If the intended objective does not factor through r, equation (8) is not the applicable formula.

### Why the hidden interaction context belongs in the state

If A(x) depends on a retained interaction descriptor kappa as well as z, then the pair (kappa,z) can support faithful dynamics even when z alone cannot. T20's fixed-interaction or leafwise constructions are concrete instances of this modelling strategy.

A simple two-leaf example uses L=(1,0), G0=diag(1,1) and G1=diag(1/2,1). The induced coarse cometrics are 1 and 2. For j(z)=−z, the same visible start z=0 evolves as z=t or z=2t. An event at z=1 occurs at time 1 or 1/2. Retaining the leaf identifier repairs both velocity and deadline prediction; simply changing the clock changes the question.

D2's finite sidecar bit bound applies when the relevant complement is finite. It is not a claim that an arbitrary continuous family of leaves fits into one bit.

---

## 7. Result D6: a conditional hybrid interface, rather than a universal noetic flow

The discrete and geometric theorems can be joined without forcing source identity or proof obligations into smooth coordinates.

Consider finitely many modes. In each mode there is a fine smooth state space, a reduced state space and a map r. Between jumps, states follow a vector field. At a jump, an action produces an outcome and a next mode/state according to a kernel.

Assume on the time horizon considered:

1. fine and reduced flows exist uniquely, and the fine vector field projects to the reduced one;
2. event/permission guards are functions of the retained state;
3. jump kernels have representative-independent pushforwards to the retained state, separately by outcome;
4. running costs, jump costs and required terminal labels are retained;
5. the process makes only finitely many jumps, or a separate non-explosion theorem is available;
6. the policy uses retained history rather than erased information.

### Proposition D6

Under these assumptions, the reduced hybrid model preserves the retained trajectory law, event times, costs and required labels up to the declared horizon.

### Proof

Before the first jump, the derivative of the projected fine trajectory is the reduced vector field. Uniqueness identifies it with the reduced trajectory. Guard values agree throughout, so their specified event times agree. At the jump, the pushed-forward outcome/next-state law agrees by assumption. Restart the same argument from the matched post-jump state. Induction proves the claim for any finite number of jumps. Non-explosion, when separately supplied, permits passage to the corresponding bounded horizon. Costs and terminal labels agree by their factorisation assumptions. ∎

### A useful specification for DAEE research

The modes can represent source-permission or proof-support configurations. Smooth coordinates can represent a justified probability subsystem. Source withdrawal, recognition and support-changing observations can be jumps rather than fictitious infinitesimal motions.

D5 supplies one positive way to satisfy the flow condition. D1–D3 supply a finite exact diagnostic for branch-labelled jumps and discrete decisions. D2 quantifies a finite complement needed by an existing compressed record.

This is an explicit mathematical interface to test—not a claim that existing DAEE already satisfies it. The outstanding task is to establish the representation and actual kernels from the application's sources, rules and semantics. No amount of metric calculation supplies those premises by itself.

---

## 8. Result D7: a systematic realisability-negative control at every finite depth

T20's latest dynamic counterexamples show that positive moment coordinates can leave the cone of probability laws. Here is a small reusable family of static controls for implementations that claim to monitor such validity.

Fix d≥1. Let mu be the uniform law on {1,...,d}, with moments mr. Let

\[
p_d(x)=\prod_{j=1}^d(x-j).
\]

Define an altered finite moment record by keeping m0,...,m2d−1 and replacing m2d with m2d−1/2.

### Proposition D7

Every recorded coordinate remains positive. Every polynomial-square expectation of degree at most 2d−2 remains that of the original valid law. But the altered record assigns expectation −1/2 to p_d(x)^2 and therefore has no representing probability law.

### Proof

All original moments are at least one, so subtracting 1/2 from m2d preserves positivity. The lower square expectations depend only on unchanged moments. The monic polynomial p_d vanishes on the original support, so its original squared expectation is zero. Its square has leading coefficient one and degree 2d. Altering only the top moment decreases its expectation by exactly 1/2. A probability measure cannot give a nonnegative square a negative integral. ∎

### Scope and use

This does not reproduce T20's stronger time-dependent construction, its determinate initial law, or its interval-arithmetic result. It is a separate exact finite family showing why an unrestricted validity claim cannot be justified by any fixed finite set of lower-degree square checks.

The reference implementation generates these witnesses for arbitrary finite d. It can be used to test that a monitoring system reports “passed the declared finite checks” rather than “proved existence of a probability law”.

---

## 9. Result D8: target-aware subspace closure for the external weight-space connection

Let x in R^n be a fine linear state. Let A1,...,Am be allowed linear updates, and let the rows of C be required output functionals. Define

\[
\mathcal W=\operatorname{span}\{c A_{i_h}\cdots A_{i_1}: c\text{ a row of }C,\ h\ge0\}.
\tag{10}
\]

Let Bx be a proposed linear summary.

### Proposition D8

Every required output after every finite allowed update word can be recovered exactly from Bx for all x if and only if W is contained in the row space of B. The smallest number of independent linear summary coordinates is dim W.

### Proof

If W is contained in the row space of B, every continuation functional w is dB for some row d, giving its decoder.

Conversely, if w is not in the row space of B, finite-dimensional linear algebra supplies v in ker B with wv≠0. The states x and x+v then have the same summary but different required continuation outputs. Thus no decoder of Bx can answer that query for both. Taking a basis of W gives a sufficient minimal linear summary. ∎

Compute W by repeatedly adding rows wAi and reducing to a basis. Each strict increase raises dimension, so the process terminates after at most n−rank C increases. The implementation uses exact rational row reduction.

This is classical observability/continuation mathematics, not a new discovery of invariant subspaces. The contribution here is its explicit use as a **task- and update-relative alternative to variance-only compression**.

### A counterexample to a variance-only guarantee

Take states x=(u,v), with u equally likely ±1 and v independently equally likely ±e. Projection onto u retains the variance fraction 1/(1+e²), arbitrarily close to one. It loses the sign of v completely.

For the update

\[
A=\begin{pmatrix}1&1\\0&1\end{pmatrix},\qquad C=(1,0),
\]

the next required output is u+v. Current-output preservation does not preserve even one-step continuation. The closure adds the missing second coordinate.

A positive approximation bound needs stronger information. If each update has norm at most L, output norm is at most M and reconstruction error is uniformly at most delta, then an h-step linear output error is at most M L^h delta. An average spectral-variance percentage alone does not supply a uniform delta, an output margin, or an application-specific L.

### How to use the uploaded paper

Its shared layer-wise bases are a possible compression map. The actual future fine-tuning or corrective operation would supply the update contract. The required behaviour would supply outputs. The missing work is connecting nonlinear neural parameter changes to a justified model of those updates and outputs, including parameter symmetries.

No conclusion about real model performance or universal noetic geometry follows from the linear counterexample alone. It supplies a discriminating question and a reference construction that can be tested in a suitable restricted experiment.

---

## 10. What is genuinely emergent in the synthesis

The strongest combined conclusion is not that all T20 branches are secretly the same theorem.

It is that the combined research supports an explicit design principle:

> **Retain an operation-relative state: enough information to preserve required outputs, permissible transitions, branch probabilities, relevant costs and admissibility—while keeping the epistemic warrant of the interpretation separately accountable.**

The new finite construction makes part of that principle operational. The sidecar theorem gives a minimum for a retained complement. The geometric theorem tells us when the smooth part really projects. The hybrid proposition states the interface conditions rather than merely placing a graph beside a manifold. The approximate and realisability controls show why weaker evidence does not license stronger guarantees.

The type-completion results add a different boundary: even a faithful semantic construction does not determine what an unchanged proof calculus can derive. A future formalisation of D1–D8 must therefore preserve its own object language, extra assumptions and intended semantics rather than crediting a metatheorem as an internal derivation.

The philosophical results determine why particular labels matter—operative grounds, actual source adoption, right authority, wise reasons and genuine recognition. The mathematics can preserve such distinctions once specified. It does not supply their actual-world warrant by naming them.

---

## 11. Implementation and evidence

`research/contracts.py` contains exact finite reference methods for D1–D3, the finite sidecar count, finite-horizon values, fixed-policy almost-sure reachability, the report/audit parity example, inquiry-value reversal, rare-event amplification, D7's moment witnesses, D8's linear closure and a two-dimensional D5 cometric calculation.

`research/test_contracts.py` contains adverse inputs and positive controls, including exhaustive comparison with all partitions of a small model. Tests are written to run under normal and optimised Python. Safety checks use explicit exceptions rather than optimisation-sensitive `assert` statements in the implementation.

The tests corroborate implementations and examples. They do not prove the general analytic statements D4–D6, validate an actual noetic representation, recompile any predecessor Lean development, or settle novelty. The ordinary proofs are given above so they can be reviewed separately.

A `TEST_FIRST.log` is retained for the initial pre-implementation run. Its interpretation, like every replay, depends on the actual recorded exit status; no test-first success is inferred merely from the filename.

See `evidence/` and `verification/` for machine-generated results, exact input identities and the portable inventory verifier. Because tool returns were not visible to the assistant at the end of this execution, this is not described as a fresh independently observed verification seal.
