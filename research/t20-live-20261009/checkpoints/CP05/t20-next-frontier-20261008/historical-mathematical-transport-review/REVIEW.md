# Independent review of historical mathematical transport

8 October 2026 UTC. Reviewed author analysis: SHA-256 `c70ade3f34431728761e0f1e0c3493823b43703120a45c85c096fea1064f235c`.

## Verdict

The completed-cut decision-cost transport, the finite-history zero-error obstruction, and the concrete linear-record application are mathematically sound under their stated contracts. The historical theorem-scope paragraph has one nonblocking omission: it does not explicitly retain Proposition 6's mass-preserving-record hypothesis. `SCOPE_ADDENDUM.md` supplies the governing qualification for the frozen text. Read this verdict with that addendum; the unqualified general kernel paraphrase is not endorsed.

No correction to the comparator formula, weighted example, stochastic impossibility proof, or 1/64 linear-channel witness was found. This is independent review of this historical-transport sibling, not independent re-review of all seven modern proofs, a field-wide priority assessment, repository integration, owner acceptance, or T20 closure. No author file or repository/PR state was changed.

## 1. Version and historical-source verification

`REVIEW_BINDINGS.json` fixes all six author files, all seven compared modern proof identities, and the archived manuscripts at commit `3a0bdeaa1394c656245cae9599adcb143e885059`. The author manifest matches the current author files, and the author control replay is byte-identical to its saved output.

I independently fetched the two PDF records and the lineage README through the GitHub connector at that exact commit. Their returned git blob identities agree with locally recomputed git blob SHA-1 identities; their byte lengths and SHA-256 values agree with the archive and author bindings:

- [Main manuscript](https://github.com/theislampill/orthemology/blob/3a0bdeaa1394c656245cae9599adcb143e885059/theory/lineages/h-ics-v5/information-composition-and-self-revision-v5.pdf): 12 pages, 341285 bytes, SHA-256 `75527bc45892a3447b8d9f554f8e55ea464790f43a172b784c6761367089cf70`.
- [Companion manuscript](https://github.com/theislampill/orthemology/blob/3a0bdeaa1394c656245cae9599adcb143e885059/theory/lineages/h-ics-v5/the-cost-of-a-decisive-revision.pdf): 4 pages, 221506 bytes, SHA-256 `4e5eb8e7559c4daaf1757386a5a101bfc399bf0ba77c769e025512bd2f6ac5c3`.
- [Archive README](https://github.com/theislampill/orthemology/blob/3a0bdeaa1394c656245cae9599adcb143e885059/theory/lineages/h-ics-v5/README.md): confirms archival, research-draft status and the unverified source-to-PDF relationship.

Both PDFs were independently re-extracted and read. The companion Theorem 1 page and main Proposition 6 page were freshly rendered and visually inspected. The two locally available TeX sources were independently rehashed, but were not substituted for the PDF theorem statements or rebuilt. The companion TeX's different title is preserved as an explicit provenance limitation. I did not recheck current main or PR lifecycle status; the review depends on the immutable commit, not those moving facts.

Actual historical scope:

1. Companion Section 1 and Theorem 1, pp. 1-2: finite nonempty situation set, supplied Boolean target, finite deterministic response menu, fixed positive finite prices, fixed availability, unchanged situations or resettable copies, deterministic protocols, and no charge for validating the model or computing the policy. The theorem is minimax exact decision-tree optimization, including conditioning on a retained record of unchanged meaning.
2. Main Proposition 6, p. 5: finite input configuration space; a linear record retaining total mass; a nonempty probability-law fibre; and a specified stochastic transition. It characterizes output-law constancy using the span of feasible differences, rather than automatically all ambient record-kernel directions. The mass qualification and full-support simplification are stated precisely in the addendum.
3. Main Theorems 7-8, pp. 6-8: finite deterministic state dynamics, exact observations, initial-state target labels, observation-based controllers, and a finite backward-reachability calculation. They are not noisy-sampling or stochastic-stopping theorems.

The papers themselves attribute decision trees, record/fibre reasoning, and finite-state identification to established antecedents. Archival preservation is neither scientific acceptance nor a new claim of priority.

## 2. Completed sign probes and the finite quotient

The finite-panel appendix proves sign Delta(m)=sign(m-n) for a promised positive interaction multiplicity. At m=k+1/2, the determinant cannot vanish because n is an integer. A completed sign therefore gives exactly h_k(n)=1{n<=k}. The appendix's positivity, strict interior ordering, common separable calibration, and population-Cauchy oracle assumptions are essential; no noisy frequency estimate is being silently upgraded to that oracle.

The strict-sign argument is coherent: the function f(s)=s/(1-exp(-s)) is strictly increasing, so the elasticity of H_c has the sign required for the mixed log derivative. Integrating over the strictly ordered rectangle gives the claimed determinant sign without differentiating an unknown calibration. The rational-root construction at half-integers uses a nonzero sign comparison, not an equality oracle.

Once the available count candidates form a nonempty finite bracket, the target g and every completed threshold response factor through n. This is a genuine response quotient. To make it a cost quotient as well, the interface must disclose only the bracket and completed bits, have fixed positive prices c_k, and withhold additional precision, raw-value, or timing information that could alter the decision problem. ANALYSIS.md line 44 explicitly stipulates the restricted interface. Under that contract, interface trees and quotient trees have identical response paths and charged costs.

The inherited recurrence is therefore exact:

    V(l,u)=0 if g is constant on [l,u]; otherwise
    V(l,u)=min over l<=k<u of c_k+max(V(l,k),V(k+1,u)).

All threshold residual sets are intervals. Out-of-bracket cuts are constant and can be discarded under fixed availability and positive prices. The result is additional cost after the bracket is obtained; it does not price an unbounded preliminary doubling search. A coarser externally supplied bracket is a stipulated candidate set, not a claim that stronger hidden evidence has been optimally used.

### Unit prices and weighted cuts

For R maximal constant runs of a Boolean target, every sound threshold leaf is an interval contained in one run. At least R leaves are necessary, hence depth at least ceil(log2 R). Recursively bisecting the ordered runs at their boundaries attains that depth. The endpoint cases R=1 and a singleton candidate set both give zero. Count identification similarly requires one leaf per candidate, giving ceil(log2(u-l+1)); the author correctly labels it a finite-label extension of the historical Boolean statement.

The weighted example is correct. Full ordered-tree enumeration gives first-cut optimum costs [111,20,11,20,111] for labels 001100 and prices [100,10,1,10,100]. The unique optimal first cut is the cheap cut inside the central constant run. Compressing the target to run boundaries before optimizing unequal costs would incorrectly return 20. The reason is informational geometry: the cheap interior cut chooses which of the two expensive decision boundaries still needs to be queried.

### Why actual sign costs do not descend

Here is an exact margin family supplementing the author's explanation. Set n=3, m=3/2, K=1, a_1=b_1=epsilon and a_2=b_2=2epsilon, for 0<epsilon<1/2. Then H_(n/m)(z)=2z-z^2 and

    Delta(3/2)=-8 epsilon^6.

Each pair of ordered interior values can be extended to an endpoint-preserving homeomorphism at fixed ordered nominal points. Thus the same count and cut have a fixed negative answer while their determinant margin tends to zero. The raw panels also differ within a single count fibre. Neither raw numerical observation nor its sign-refinement cost is identified with the completed-bit interface by this quotient argument.

This is a conditioning obstruction to extracting a uniform price from the theorem, not an assertion that every implementation must spend the same large amount. In particular, an approximation cap that leaves zero in the determinant interval is inconclusive and cannot reject a count. The author explicitly preserves that boundary.

## 3. Adaptive randomized endpoint histories

For two positive counts j and k, the known-calibration response q_j(x)=(1-x)^j has exactly the same two-point support as q_k(x) at every x in [0,1]. At x=0 and x=1 both laws are the same point mass; at an interior command both outcomes have positive probability.

A measure-level argument is needed because real-valued actions need not have atoms. Let P and Q be equivalent laws of a finite past, let pi(da|h) be the same observation-based action kernel under both models, and let K_j(db|h,a), K_k(db|h,a) be equivalent endpoint kernels at each common history/action. If a measurable event in the extended history has zero Q pi K_k mass, its sections have zero K_k mass for Q pi-almost every history/action. Equivalence transfers those null sets to P pi, and endpoint-kernel equivalence gives zero P pi K_j mass. Reverse the roles for the converse. Induction proves equivalence for every finite horizon.

Protocol randomization is required to be model-independent. It can be included in the history/controller state, or represented through common action, stopping, and reporting kernels. This treats private randomization without assuming that every individual real-valued transcript has positive probability. Stopped processes can be padded by a common absorbing symbol so events of stopping by time N are measurable at a fixed finite horizon.

For a uniformly zero-error procedure, let E_N be the event of stopping by N and reporting j. If a correct finite report has positive probability under j, some E_N has positive probability there because the finite-report event is a countable union. Finite-history equivalence forces positive probability of E_N under k, contradicting zero error. This is stronger than the requested impossibility of almost-surely finite identification under both models: no positive-probability finite correct report is possible while retaining zero error on both alternatives. The same argument applies to any target assigning those alternatives different labels.

The pure-interaction extension uses q=(1-p)^j with a common route success p. The balanced multi-root pair also has common endpoint support: a disabled added route leaves identical laws; a surely successful baseline leaves the same deterministic endpoint; otherwise enabled interior laws assign positive probability to both possible endpoints. This uses the fixed-histogram fresh conditional response-kernel premise of the modern model. It is not a conclusion for arbitrary cross-trial dependence or additional internal observations.

The limits are important and correctly retained:

- Zero versus positive count is outside the pair: at x=1 it is exactly distinguishable.
- Finite-history equivalence does not assert equivalence of infinite-history laws. Infinite repeated observations can distinguish distinct Bernoulli parameters.
- Positive-error inference is allowed. As an exact control, 32 repetitions at x=1/2 distinguish counts 1 and 2 by reporting 1 when the no-hit count is at least 12. The two errors are approximately 0.05509 and 0.08043, both below 0.1 and strictly positive. This is an illustrative fixed two-model calculation, not a new general sample bound.
- A population-Cauchy oracle is a stronger instrument than Bernoulli endpoint samples. Finite termination with the former does not contradict impossibility with the latter.
- The theorem concerns uniform zero-error identification under a specified experiment. It supplies no philosophical impossibility about finite evidential warrant, practical knowledge, justified action, or confidence statements.

## 4. Proposition 6 and inherited attribution

The three-state auxiliary catalogue is legitimate: q=(t,t^2,(t+t^2)/2), with the last coordinate realized by the count-one calibration r_3(x)=3x/2-x^2/2. That map fixes endpoints and has strictly positive derivative on [0,1]. The record with rows 1 and q annihilates d=(1/2,1/2,-1). This also holds simultaneously for all commands.

Holding a catalogue state for two conditionally independent endpoints defines a fixed linear channel with rows q^2, q(1-q), q(1-q), and (1-q)^2. Its columns are probability laws. Its image of d is

    t^2(1-t)^2/4 times (1,-1,-1,1),

which is nonzero at every interior command and equals (1,-1,-1,1)/64 at x=1/2. The feasible midpoint (1/4,1/4,1/2) has full support. Because A explicitly retains mass, all the actual historical Proposition 6 hypotheses are met. The optional counterexample of zero singleton marginals confirms why an arbitrary unsupported kernel direction would be insufficient without this support check.

The full three-state convex fibre is an auxiliary mathematical catalogue: its mixtures can combine calibration types and need not satisfy one common calibration across latent counts. The two witness models individually do satisfy the modern model, so their endpoint indistinguishability and held-repeat distinction transfer. Convex closure of that modern model does not transfer. The author's line 108 explicitly preserves this restriction.

Fresh independent resampling produces products of mixture means. As a map of the input law, that repeated-output operation is generally nonlinear; it is not the same fixed linear channel on one retained catalogue state. Proposition 6 is being applied to the held-state channel, not to that nonlinear map. Thus it explains why a retained record can fail to determine a new observable, without proving persistence or removing the persistence assumption.

The scalar countermodel and its variance gap already appear in the bound grouped-invariants RESULT. The new note provides an exact realization in the historical framework and properly assigns inherited credit. The historical manuscripts do not contain the current finite-panel sign theorem, primitive integer mixture invariants, calibration-radius calculations, or balanced-pair KL exponent. Conversely, the historical decision-tree theorem and fibre criterion should not receive new general-theorem credit merely because they are instantiated here.

## 5. Checks and review boundary

`independent_controls.py` was written for this review. It reads but never writes author artifacts. It checks the bound bytes and replays the author controls, then independently enumerates full ordered binary trees rather than relying only on the author's recurrence implementation.

Fresh exact results in `CONTROL_RESULTS.json`:

- All six frozen author files and seven modern source identities match; author control output is byte-identical.
- 510 unit-price Boolean catalogues checked by full-tree enumeration; 3110 weighted label/price cases checked against the recurrence; eight finite-label identification cases checked.
- The weighted example's five root costs are exactly [111,20,11,20,111].
- Sixteen exact vanishing-margin cases and 171 rational linear-channel cases pass.
- Three Proposition 6 scope controls cover missing mass retention, unnecessary full-support strength, and inadmissible boundary-support directions.
- 160 adaptive randomized stopped-law comparisons and 12440 exact likelihood-ratio checks pass. These include fresh randomized actions, randomized stopping, and randomized final reports.
- 1008 balanced multi-root support cases pass, including boundary rates.
- The positive-error two-count control has both exact errors strictly below 1/10.

The general proofs above establish the arbitrary finite bracket, measurable adaptive-policy, and linear-record statements. The finite tests are corroboration and negative controls, not proofs by exhaustive enumeration of the infinite classes.

Current-source reading was targeted: the finite-panel appendix, grouped-invariants RESULT, and multi-root RESULT were read fully for the transported premises and witness. All seven modern identities were checked, but this review does not substitute for their own independent mathematical reviews or repeat the author's assertion that no other correction exists in them.

No repository write, PR action, integration, closure, physical validation, or epistemic/metaphysical upgrade is part of this review.
