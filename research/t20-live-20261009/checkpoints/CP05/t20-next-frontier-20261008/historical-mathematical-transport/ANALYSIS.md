# Exact-decision inheritance, calibration quotients, and a failed stochastic transport

## 1. Version-bound answer

The archived manuscripts were read as mathematics, not inferred from their titles:

- *Information, Composition, and Self-Revision: Local Descriptions and Operative Access*, 12 pages, SHA-256 `75527bc45892a3447b8d9f554f8e55ea464790f43a172b784c6761367089cf70`.
- *The Cost of a Decisive Revision: Evidence, Reuse, and Self-Application*, 4 pages, SHA-256 `4e5eb8e7559c4daaf1757386a5a101bfc399bf0ba77c769e025512bd2f6ac5c3`.

Both were fetched at [the immutable archived commit](https://github.com/theislampill/orthemology/tree/3a0bdeaa1394c656245cae9599adcb143e885059/theory/lineages/h-ics-v5). [PR 32](https://github.com/theislampill/orthemology/pull/32) and its provenance README confirm the archival role. Git blob identities, byte lengths, and SHA-256 hashes were verified locally. The branch ref also pointed to that commit when checked, but the comparison is bound to the commit, not future `main`.

The existing companion TeX has the different title *Reflexive Revision under an Evidence Budget*. Its exact SHA-256 is `bf8490a82b45fbf8a5be11ecd7a7ee90a0e49cbb383b86f60a5993a54782d1af`, matching the README. A byte-identical TeX-to-PDF build is not asserted. Both complete PDFs, rather than an assumed equivalent TeX edition, supply the historical theorem statements used here.

Seven current proof documents are bound in `SOURCE_BINDINGS.json`: the four named siblings' main results, the interaction finite-panel appendix, the grouped global-scale corollary, and the calibration polynomial-efficiency appendix. All seven were read completely. This note does not rewrite any of them.

There is one useful inherited algorithmic corollary, one precise failed transport, and an attribution clarification. None closes the calibration gauges, supplies a new stochastic sampling bound, or supersedes the independently developed proofs.

## 2. What the historical theorems actually assume

The companion's Section 1 fixes a finite nonempty situation set C, a Boolean target g, and a finite menu of deterministic response maps h:C->Y_h. Every probe has a fixed finite positive price, remains available, and leaves the situation unchanged or uses resettable copies. Protocols are deterministic. The tables and meanings are supplied premises; policy computation and model validation are outside the charged cost.

Its Theorem 1, page 2, identifies the minimum worst-case sound decision cost with the minimax decision-tree recursion. If a retained record has unchanged meaning, its actual value restricts C to a fibre before new probe costs are paid. The theorem is explicitly a standard decision-tree optimization, not a new universal method of inquiry. Its address-function example proves that one particular exact query task has an adaptive advantage; it does not assert an advantage for every task.

The main manuscript's Proposition 6, page 5, instead concerns a finite input configuration space, a linear record A on signed laws, and a stochastic transition channel T. On the nonempty feasible fibre M={mu>=0: mass(mu)=1, A mu=m}, output determination is equivalent to T annihilating D=span(M-M). It identifies D as the record-kernel directions supported on the union of feasible supports. Only with a full-support feasible law may one replace D by the entire kernel of A. This proposition accommodates probabilities, but is an output-law determination theorem, not an adaptive sample-cost theorem.

The main manuscript's Theorems 7 and 8, pages 6-8, use finite states, deterministic state-changing actions, and exact observations. Observation congruence preserves histories; a finite labelled-belief backward-reachability construction characterizes sure finite decision without erasing needed initial labels. Those hypotheses do not silently become noisy Bernoulli sampling hypotheses. The manuscript itself makes that boundary explicit in its conclusion.

## 3. A genuine finite-quotient transport of the decision-cost theorem

### 3.1 The new panel supplies the response maps

Fix a promised positive interaction support and the four isolated panel values from `interaction-calibration-anchor/FINITE_PANEL_APPENDIX.md`. Its determinant theorem says that for every positive real m,

    sign Delta(m) = sign(m-n),

where n is that support's positive integer multiplicity. Consequently a completed sign determination at m=k+1/2 has response

    h_k(n) = 1{n<=k}.

This is not an assumed calibration measurement: the new rigidity/sign theorem is what proves the response descends to the count quotient. The historical manuscript does not prove that sign theorem.

Suppose the retained valid evidence gives a finite integer bracket l<=n<=u, either by an independently supplied bound or after the appendix's terminating doubling stage. Let the decision be a supplied Boolean g(n). All unknown calibrations compatible with the panel model can be collapsed to the finite quotient C={l,...,u}: each permitted completed-cut response and the target factor through n. Such quotienting is sound for responses because of the strict sign theorem.

To preserve cost too, separately stipulate an interface that exposes only these completed binary cuts, charges a fixed positive price c_k for h_k, and offers no additional informative replies. The panel is internal to that interface: the controller receives its bracket and completed cut history, not raw exact panel values or approximation intervals that could reveal additional information. Then every decision tree in the quotient is a tree in this interface, with exactly the same responses and charged path costs. Conversely every interface tree projects to the count quotient. The finite C, deterministic responses, fixed availability, unchanged state, fixed prices, and target of the historical Theorem 1 are all preserved. The retained bracket is the historical theorem's record fibre.

For an interval [l,u], the exact inherited recurrence specializes to

    V(l,u)=0                                  if g is constant on [l,u],
    V(l,u)=min_(l<=k<u) {c_k+max(V(l,k),V(k+1,u))} otherwise.

This supplies an optimal next completed cut and a stopping rule. It is a direct application of the old theorem to a response family justified by the new panel theorem, not a new decision-tree theorem.

### 3.2 Unit-price closed form and a nonuniform-price example

If every completed cut costs one, let R be the number of maximal contiguous constant runs of g on the current ordered candidate interval. Then

    V(l,u)=ceiling(log_2 R),

with V=0 when R=1.

Proof: a threshold-query leaf contains an interval of candidates. A sound leaf cannot span two different constant runs, so at least R leaves are necessary. A binary tree of maximum depth d has at most 2^d leaves, giving the lower bound. Split the ordered runs as evenly as possible by a threshold at a run boundary and recurse; this produces a sound tree of depth ceiling(log_2 R). This is an elementary ordered-threshold corollary of the historical decision-tree theorem. No separate universal-discovery credit is claimed.

For full count identification the same tree argument gives ceiling(log_2(u-l+1)); that is the straightforward finite-label extension, not literally the historical Boolean statement. For the Boolean threshold decision n<=K, one nontrivial cut suffices, whereas parity on the candidate interval has one run per candidate.

Nonuniform prices give a useful reason to retain the full recurrence. Let C={1,...,6}, g=0,0,1,1,0,0, and prices (c_1,...,c_5)=(100,10,1,10,100). Querying the cheap central cut h_3 first, then h_2 or h_4 according to its answer, costs exactly 11 in the worst case. A first query at either decision-run boundary costs 20 in the worst case. The recurrence proves 11 is optimal: first cuts 1 or 5 already cost 100; first cut 2 must subsequently separate 4 from 5, requiring the price-10 cut 4, and symmetrically for first cut 4; first cut 3 has cost 1 plus a branch optimum 10. Splitting inside a constant run can therefore be optimal when probe prices differ.

### 3.3 What this does not price

The original panel oracle supplies approximations to population probabilities, potentially with numerical information beyond a completed sign. The comparator-interface lower bound is not a lower bound for every algorithm using those richer replies or reusing already computed intervals. Restricting to the completed-cut interface is consequential.

Most importantly, costs need not descend through the count quotient in the original problem. At the same n, different homeomorphic calibrations can make the determinant at a fixed half-integer arbitrarily close to zero. Certifying its sign can require arbitrarily different precision and computation. The original Cauchy-oracle proof guarantees individual termination, not a uniform fixed price c_k. The historical theorem cannot manufacture such a price, charge only the final bit while overlooking refinements, or convert a population probability oracle into a Bernoulli sample oracle. Unit-price cuts are an explicitly stronger accounting contract.

If a practical sign computation reaches a precision or time cap before its interval excludes zero, its result is **INCONCLUSIVE**. It is neither a completed Boolean response nor evidence against a count candidate. No branch may be pruned, candidate rejected, or successful abstract probe counted on that basis. The failed computation may still have consumed real resources; it supplies no rejection credit. Mathematical termination under the positive-support promise supplies no uniform bound at which a capped implementation must finish.

Thus the transported corollary closes the abstract next-cut/decision-cost problem under that contract. It does not close the statistical cost or physical calibration residuals.

## 4. Failed transport: finite endpoint evidence versus uniform zero error

Consider two distinct positive pure counts n and m with exact known identity calibration. At nominal command x the no-hit mean is q_j(x)=(1-x)^j. At 0<x<1 both endpoint outcomes have positive probability under both counts. At x=0 both models return no hit surely; at x=1 both return a hit surely. Their endpoint kernels therefore have the same support at every command.

Allow any observation-based randomized adaptive command policy. Conditional on a common past, its next action-selection kernel is the same in both worlds. The two conditional endpoint kernels are mutually absolutely continuous at every possible action. Induction shows that the complete finite history laws under n and m are mutually absolutely continuous. This argument handles a continuum of command choices; one need not assign positive probability to individual real-valued transcripts. It also includes randomized decisions by retaining the protocol's common randomization or by including its common decision kernel.

Suppose a zero-error procedure reports n after finitely many endpoints with positive probability in world n. The event is the countable union over N of 'stop by time N and report n', so one finite-N event has positive probability under n. Mutual absolute continuity gives positive probability of the same event under m, which is an error. Hence a uniformly zero-error procedure cannot make a correct finite positive-probability report in either world. In particular, no zero-error identifier can terminate almost surely under both worlds.

The argument already holds in an exactly calibrated subfamily; unknown calibration is not needed for this obstruction. For a pure interaction support use its single-route success probability p(x) in place of x: again both counts have shared deterministic endpoint cases when p=0 or 1, and both bits have positive probability when 0<p<1. The multiroot balanced hard pair also has common endpoint support at every action: where the added route is disabled the laws agree, interior enabled laws have both bits positive, and a surely successful baseline makes both endpoint laws identical. It does not acquire a finite zero-error certificate through adaptation.

This does not contradict the modern finite budgets for error delta>0 or the finite-panel population-Cauchy procedure. The former permits a controlled error probability; the latter requests certified accuracy about population probabilities from a stronger observation instrument. Neither is the deterministic exact-probe model used in the historical Theorem 1. Augmenting the hidden state with an unobserved random tape does not make that tape supplied finite known state, deterministic exact measurements, or fixed costs.

The conclusion is about the stipulated uniform certainty target. It is not a claim that finite evidence cannot warrant belief, knowledge, action, or a calibrated confidence statement under other standards. No philosophical epistemic impossibility is inferred.

## 5. Exact linear-record overlap, with its domain kept honest

There is a concrete connection to the historical Proposition 6, rather than only a shared use of the word 'information'. At t=1-x, take three finite catalogue states whose no-hit curves are

    q_1=t,  q_2=t^2,  q_3=(t+t^2)/2.

The first two are counts one and two with identity calibration. The third is count one with the alternative static homeomorphic calibration r_3(x)=3x/2-x^2/2 used in the current grouped-invariants countermodel; its derivative is 3/2-x>0 and its endpoints are preserved. Let mu=(1/2,1/2,0), nu=(0,0,1), and d=mu-nu.

At each command, the one-trial record has rows 1 and q. It annihilates d: the mean endpoint laws are identical, even over all commands. At x=1/2,

    q=(1/2,1/4,3/8),
    q^2 dot d=1/64.

The two-held-repeat transition channel has four rows q^2, q(1-q), q(1-q), (1-q)^2. Its output difference on d is (1,-1,-1,1)/64. Thus T_2 d is nonzero. For this auxiliary finite catalogue's unconstrained linear-law fibre, (mu+nu)/2=(1/4,1/4,1/2) is full support, and the historical Proposition 6 applies exactly: the old record does not determine the new grouped output law.

The general-command all-no-hit difference is t^2(1-t)^2/4, the same witness already stated in `grouped-calibration-invariants/RESULT.md`. This is a prior-framework attribution and exact channel realization of that existing countermodel; it is not a newly discovered mixture counterexample.

One domain restriction matters. Arbitrary distributions over all three catalogue states can mix different calibration types. They are legitimate inputs to this auxiliary finite channel, but need not belong to the modern restricted class with one shared calibration across latent counts. Both endpoint models mu and nu do belong to that modern class separately. We do not use the auxiliary fibre's full-support condition to assert a necessary-and-sufficient theorem over the nonlinear common-calibration family. The precise two-model witness transfers; unrestricted convex closure of the modern model does not.

Freshly resampling the catalogue state before each endpoint is another process. Conditional repetition given one retained state produces the linear kernel T_2; independently resampling produces products of mixture means. These are different channels, so the historical criterion reinforces, rather than removes, the new persistence premise.

## 6. Consequences for the four current results and scientific credit

- **Interaction calibration anchor:** the old fibre criterion explains what identification means, but does not supply log-mask inversion, multiplicative rigidity of the calibration change, or the strict finite-panel determinant sign. The completed-sign policy is the exact inherited corollary in Section 3. None of the old theorems selects the actual isolated unary count or recovers a whole calibration map from a finite panel.
- **Grouped calibration invariants:** the scalar atom matching, primitive integer vector, rational rescaling, and global scale-radius formulas are not present in either historical paper. Proposition 6 gives the exact older linear-record framework for the stated held-versus-fresh witness. Parity of proper marginals is not a substitute for the moment, common-calibration, and positivity assumptions used here.
- **Global calibration ambiguity:** the historical record-factorization obstruction applies once an all-command indistinguishable pair is supplied. It neither constructs the static maps nor proves the sharp radius, catalogue separation, or polynomial-versus-superpolynomial calibration scale. Extending equality to adaptive stochastic histories requires the response-kernel coupling used in the current proof; historical deterministic observation congruence is not itself that proof.
- **Multi-root adaptive bound:** the historical exact decision-cost recurrence and address-function separation do not yield the per-action KL estimate, transcript divergence budget, or matched fixed-histogram exponent. Those depend on the present endpoint kernel, action menu, balanced hard pair, and matched upper class. A task with a classical adaptive advantage cannot force one in this different experiment.

No claim in these seven compared proof texts required a discovered numerical correction. The useful prior-attribution correction is narrower: record-fibre sufficiency, linear output determination, and the minimax exact decision-tree policy are inherited tools already explicitly acknowledged as classical by the historical manuscripts. Their use should not receive fresh general-theorem credit. The modern concrete calibration and sampling arguments remain separately earned results under their own premises. This note supplies no independent review verdict on them and no field-wide priority claim.

## 7. Evidence and stopping boundary

`exact_controls.py` independently implements the finite minimax recurrence, exhaustively checks the unit-price Boolean-runs formula on all Boolean labelings up to ten candidates, verifies the heterogeneous-price example, evaluates the finite linear-channel witness over exact rational commands, and checks finite randomized adaptive endpoint-history supports with rational arithmetic. General proofs above, not these finite checks, support the statements for all finite catalogues and adaptive policies.

The source-bindings replay verifies that every compared modern proof is still the exact version read. Historical PDFs/TeX are held outside this deliverable for local reading; only source identities, locators, concise descriptions, and original analysis are retained here. No repository/PR mutation, package work, scientific acceptance, integration or T20 closure was requested or performed.
