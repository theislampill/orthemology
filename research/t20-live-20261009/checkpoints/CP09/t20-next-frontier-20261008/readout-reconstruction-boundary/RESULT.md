# Randomised reconstruction boundary for exact minima and a finite interior panel

8 October 2026 UTC. Prospective scratch-only mathematical derivation, conditional on the inherited observation contracts. No protected edits, integration, closure, physical-access claim, efficient sampling claim, or field-wide novelty. This is an application of standard measure-theoretic postprocessing lemmas.

## 1. Experiments and conclusion

Fix n>=1, m=n+1, c=n/m. In world 0 there are n independent product-uniform route thresholds; in world 1 there are m independent Joe route thresholds with joint CDF H_c(ab), H_c(t)=1-(1-t)^c. Retain the entire vector during each experiment.

Let M_i be the law of the exact two-minima readout in world i (equivalently X=1−T_A, Y=1−T_B). Let Q_i be the law of the fixed, strictly interior staircase panel in retained-interior-certificate/RESULT.md §1: m positive sites q_j=(a_j,b_j) and m−1 connectors r_j=(a_j,b_(j+1)), where 0<a_1<...<a_m<1 and 1>b_1>...>b_m>0. Its finite alphabet is the ordered 2m−1 endpoint bits. Write E for all q hits and all r misses. The inherited results give

    M_0 and M_1 mutually absolutely continuous;
    Q_0(E)=0, Q_1(E)=p=m! product_j mu_c(B_j)>0,
    B_j=(a_(j−1),a_j] × (b_(j+1),b_j], a_0=b_(m+1)=0.

A common Markov kernel may depend on the known pair and chosen panel, but not on the unknown world index. Its auxiliary randomness carries no additional information about that index.

**Conclusion.** No common kernel K satisfies M_i K=Q_i for both i=0,1. Conversely, no common kernel J satisfies Q_i J=M_i for both i=0,1. These two specified binary experiments are therefore incomparable under exact randomised postprocessing. This does not assert incomparability of all interior and face interfaces, of arbitrary alternative laws, or of repeated/approximate experiments.

## 2. Standard lemma and minima-to-panel obstruction

If probability laws A_1<<A_0 and K is a Markov kernel, then A_1 K<<A_0 K. Indeed, (A_0 K)(D)=0 implies K(s,D)=0 for A_0-almost every s by nonnegativity; absolute continuity gives the same statement A_1-almost everywhere, so (A_1 K)(D)=0. This proof requires no deterministic decoder or density for the output.

Apply the lemma to M_1<<M_0. Exact reconstruction of Q_0 would force (M_1 K)(E)=0, contradicting Q_1(E)=p. With total variation defined as sup_D |A(D)−B(D)|, every kernel satisfying M_0 K=Q_0 obeys

    TV(M_1 K,Q_1)>=p.

This is a baseline-exact bound, not an unconditional lower bound for kernels allowed error in both worlds. Even a randomised decoder cannot reconstruct both laws. Separately, finite forward KL of M_1 relative to M_0 and infinite forward KL of Q_1 relative to Q_0 provide a compatible data-processing obstruction; the absolute-continuity proof already suffices.

## 3. Converse: finite panel cannot reconstruct the exact minima laws

The preceding obstruction alone would not prove the converse. Two additional facts do.

**Finite-panel reverse domination.** Q_0<<Q_1. To see this, take any baseline-positive transcript atom. Thresholds equal to any of the finitely many queried coordinate values, or lying on the boundary, have baseline probability zero. There is therefore a realization of that transcript with all n route pairs in the open square and off these lines. Every route's answer to every panel query remains fixed in a sufficiently small open neighborhood of its coordinates. Duplicate one of the n routes to obtain m routes: endpoint OR values are unchanged. The resulting m-fold product of small open neighborhoods has positive probability under the independent Joe law, whose density is strictly positive in the open square. All of it produces the same transcript. Thus the atom has positive Q_1 probability.

Because the alphabet is finite, there is a finite constant

    C=max_{s:Q_1(s)>0} Q_0(s)/Q_1(s),

with Q_0<=C Q_1 as measures. Any common kernel J preserves this inequality by integration: Q_0 J<=C Q_1 J. This argument applies to any fixed finite endpoint panel for this hard pair; the staircase structure is needed for the opposite-direction certificate, not for this domination fact.

**The reverse minima likelihood is essentially unbounded.** In the inherited coordinates, let z=x+y−xy and S=x^c+y^c−z^c. On the open square,

    f_0=n² x^(n−1)y^(n−1),
    f_1=m(m−1)S^(m−2)S_x S_y + m S^(m−1)S_xy.

Fix y in I=[1/3,2/3], and 0<x<1/2. The inherited derivative formulas imply S<=x^c and 0<S_x<=c x^(c−1). Also S_xy=c z^(c−2)[1−c(1−x)(1−y)] is positive and uniformly bounded by some finite A=A(n) on this strip: z>=1/3 and the bracket is at most 1. At x=0, S_y(0,y)=0. Integrating S_xy in x, or applying the fundamental theorem of calculus to the explicit smooth expression there, gives 0<=S_y(x,y)<=A x. Consequently

    f_1(x,y)<=A[m(m−1)c+m] x^(c(m−1))
             =A[m(m−1)c+m] x^(n−c).

Meanwhile f_0(x,y)>=n²(1/3)^(n−1)x^(n−1). Hence for a finite B=B(n), uniformly on the strip,

    f_1/f_0<=B x^(1−c) ->0 as x decreases to zero.

Since 1−c>0, every proposed finite C has a positive-area strip on which f_0>C f_1; both densities are positive there. Thus M_0<=C M_1 fails for every finite C. This also covers n=1 (the exponent 1−c is 1/2). The bounded reverse domination required by any Q-to-M kernel is impossible, proving the converse. No unsupported general converse theorem or asymptotic approximation is being assumed.

## 4. Deterministic fibre example and inherited H lineage

The two route configurations

    d={(1/5,3/5),(3/5,1/5)},
    d'={(1/5,1/5),(3/5,3/5)}

both have coordinate minima (1/5,1/5). Their interior endpoint at (2/5,2/5) is respectively 0 and 1. This is a pathwise counterexample to factoring that endpoint through the minima. It is not itself a proof about almost-sure reconstruction in the two continuous-law experiments: individual configurations are null events, and both displayed configurations have two routes.

In the inherited H manuscript, Theorem 4.2 supplies exactly the elementary deterministic fibre criterion applied to this example. Proposition 11.1 explains the scope change: minima preserve all coordinate-face comparisons on a retained vector, while a newly required interior endpoint can fail to factor through them. The stochastic experiment statements in §§2–3 instead use the independently proved Markov-kernel lemmas, not a promotion of that deterministic criterion. The manuscript's deterministic-update Theorem 11.2 is not being applied to stochastic models.

## 5. Scope and assurance

The bounds concern one retained vector and exact law simulation by a world-independent channel. They do not rank every test, identify the most useful practical instrument, establish a sample exponent, simulate an unknown physical system, or supply an efficient count estimator. All proof steps here are written mathematics, not newly kernel-checked Lean results. The inherited panel's existing Lean certificate concerns its deterministic route-count bound, not these new measure-theoretic claims. SOURCE_BINDINGS.json pins the exact local files and sections used; no source bodies are copied into this packet.
