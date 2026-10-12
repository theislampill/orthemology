# Participating derivation: exact cap-only contraction coefficient

Status: ordinary mathematical candidate, sent to author and independent reviewer for checking. This is a refinement of the active P02 U08 effectivity investigation, not a separate theorem campaign. No world-novelty, kernel, empirical or epistemic-warrant claim.

Let c≥0 be summable on N, C=sum c≥1, and Kc={p≥0:sum p=1,p≤c}. Use TV(p,q)=1/2 ||p−q||1.

## Formula

D(c):=sup_{p,q in Kc} TV(p,q)
 = sup_{S subset N} [min(1,c(S))+min(1,C−c(S))−1].

For each S, the largest attainable p(S) is min(1,c(S)); the smallest is max(0,1−c(S^c)). Both extrema are feasible by distributing the prescribed mass proportionally to the cap in each of S and S^c; a zero-cap group receives zero mass. The total capacity C≥1 supplies the remaining mass. The standard discrete identity TV(p,q)=sup_S[p(S)−q(S)] and interchange of two suprema give the formula.

The subset-sum map from {0,1}^N to R, z↦sum c_j z_j, is continuous by uniform tail convergence. Its image is compact, so the supremum is attained. Accordingly D(c)=1 iff some subset S has c(S)≥1 and c(S^c)≥1. This is a capacity partition criterion, not a claim about a particular operator's actual row separation.

For any fixed stochastic operator with every row in Kc, its Dobrushin coefficient is ≤D(c), hence ||pT−qT||1≤D(c)||p−q||1. Conversely arbitrary two cap-admissible rows can be used as rows of an operator (fill remaining rows with either), so no smaller cap-only uniform coefficient is valid.

## Coarse bound and controls

D(c)≤min(1,C−1). Therefore C<2 suffices. This total-mass bound is sharp across caps: c=(1,C−1), 1≤C≤2, permits rows (1,0) and (2−C,C−1) attaining coefficient C−1.

It is not an exact test for a particular cap: c=(9/10,9/10,1/5) has C=2 but D=9/10. The finite subset masses are 0,1/5,9/10,11/10,9/5,2. Their greatest value of min(s,2−s,1) is 9/10.

Pairwise overlap is not a shared minorisation measure: c=(1/2,1/2,1/2) allows rows (1/2,1/2,0),(1/2,0,1/2),(0,1/2,1/2). Here D=1/2 although coordinatewise minimum across all three rows is zero.

## Effectivity

Suppose c is computable coordinatewise with an effective l1-tail modulus. Then C is computable. For finite initial segment J_N, put D_N=max_{S subset J_N} f(c(S)), where f(s)=min(1,s)+min(1,C−s)−1. The function f is 1-Lipschitz on [0,C]: equivalently f(s)=min(1,C−1,s,C−s). Any subset's omitted cap mass is ≤tau_N=sum_{j notin J_N}c_j. Thus D_N≤D(c)≤D_N+tau_N. Finite computable maxima and the tail modulus give an effective name of D(c). This is an existence-of-algorithm result, not a complexity claim; finite subset enumeration is exponential.

Under the promise D(c)<1, search approximations until obtaining a rational certified upper bound rho<1. Then the selected operator has a unique stationary probability and ||pT^n−pi||1≤2rho^n. A posteriori residual gives ||p−pi||1≤||pT−p||1/(1−rho). Both are standard contraction consequences. Merely knowing D(c)≤1 gives neither a strict gap nor a decision algorithm for equality to 1.

## Original correspondence boundary

The fixed selected operator must be supplied effectively. Classical choice from arbitrary nonempty closed row sets is not promoted to an algorithm. Different selected operators can have different fixed points even when the common cap has D<1. The already inherited interval correspondence with each row set Bernoulli([1/3,2/3]) and cap(2/3,2/3) retains its whole stationary interval.

## Universal uniqueness consequence (ordinary mathematics)

D(c)<1 iff every stochastic kernel with all rows in Kc has a unique stationary law. The forward direction is the contraction argument. For the reverse, if D(c)=1 choose an attained subset S with c(S),c(S^c)≥1. Choose p∈Kc supported in S and q∈Kc supported in S^c, for example the cap normalisations within those groups. Define row i to be p when i∈S and q otherwise. Then pT=p and qT=q, and they are distinct. This proves the sharp uniform envelope characterisation. It does not establish that the chosen partition, rows or kernel are computable when the given cap is computable. The algorithmic counterexample is supplied separately by the explicit two-state cap.

Row domination is essential. With c=(3/4,3/4), D(c)=1/2 and Kc is the interval of Bernoulli laws with parameter in [1/4,3/4]. The identity operator maps Kc to itself but fixes every point. Its rows are outside Kc. Therefore mere invariance of the compact envelope must not be substituted for the stronger row-domination hypothesis.
