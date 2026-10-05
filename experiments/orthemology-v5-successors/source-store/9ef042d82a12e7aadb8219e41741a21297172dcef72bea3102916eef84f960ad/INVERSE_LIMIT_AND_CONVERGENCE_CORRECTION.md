# Infinite backward realizations and forward convergence

3 October 2026 UTC. Self-contained mathematical review supplement. No implementation, external contact, publication, or metaphysical-possibility claim.

## Result

For a general self-map of a complete bounded metric space, three properties must be distinguished:

1. Only one state survives every finite backward-depth test.
2. Exactly one compatible infinite backward realization exists.
3. Every forward orbit converges to one fixed point.

The first implies the second, but the converse can fail. Neither of the first two implies the third. The third does not imply either of the first two. Completeness, boundedness, and continuity do not remove these failures.

There is a clean positive repair. For a continuous self-map of a nonempty compact metric space, the first two properties are equivalent to **uniform** convergence of all forward orbits to one fixed point. Pointwise forward convergence remains too weak, even for a homeomorphism of a compact metric space.

Bounded strict-contraction sufficiency remains valid. The correction changes neither that sufficient result nor the existential null-preservation lemma. It prevents mathematical uniqueness from being inferred using an invalid general equivalence.

## Source and interpretation boundary

The source owner, bibliographic identity, proof-witness status, bounded exposition, and original application review are `INDEPENDENT_REVIEW_v1.md` §§1 and 7 and Appendix A. This supplement adds no historical synopsis or quotation. Relevant primary locators are B printed p474, note 13 and conditions CN1–CN2; p482, note 16; and Appendix A, pp499–500, numbered lines 1203–1229. Additional domain controls are at pp471–474, numbered lines 398–413 and 486–492; the nearby-world restriction is at pp478–480.

The results below concern a declared state space X and its self-map f. They do not equate that state space with metaphysically possible worlds. A range restricted in advance to jointly realized states is a different domain; §7 states exactly what changes under that reading.

## 1 Definitions

Let X be a nonempty set and f:X→X a total function. Use natural-number indices starting at 0. Let f⁰ be the identity and fⁿ the n-fold iterate.

Define the nested ranges

K_n = fⁿ(X),

and their surviving intersection

S = intersection of K_n over all n≥0.

A point in S has some predecessor of every finite depth. The predecessors chosen at different depths need not belong to one compatible infinite path.

Define the set of infinite backward realizations

B = { (x_0,x_1,...) : x_i=f(x_(i+1)) for every i≥0 }.

Let C be the set of zeroth coordinates of elements of B. An element of C has a compatible infinite ancestry. With a fixed self-map, each later coordinate of any realization is also in C, because its tail is another realization.

When X is a metric space, distinguish:

- **Pointwise attraction to e:** fⁿ(x)→e for every fixed x in X.
- **Uniform attraction to e:** sup over x in X of d(fⁿ(x),e)→0.

In the uniform-attraction statements below, e is required to be a fixed point. Suprema may initially be infinite on unbounded spaces; convergence to 0 requires them to become finite and small. On a bounded space this qualification is automatic.

Exactly one realization means one actually exists. At-most-one permits an empty solution set and is insufficient for the conclusions below.

## 2 Algebraic facts requiring no topology

### Proposition 1 Compatible ancestry implies finite-depth survival

C is a subset of S.

Proof. If x_0 is the first coordinate of a realization, repeated substitution gives x_0=fⁿ(x_n) for every n. Thus x_0 belongs to every K_n. The same reasoning applies to every coordinate.

### Proposition 2 The surviving intersection is forward invariant

f(S) is a subset of S.

Proof. If x belongs to every K_n, then for every n, f(x) belongs to f(K_n)=K_(n+1). These ranges are nested, so f(x) belongs to all K_n as well.

### Proposition 3 Singleton survival gives fixedness and unique realization

If S={e}, then f(e)=e, e is the unique fixed point, and B contains exactly the constant all-e realization.

Proof. Forward invariance puts f(e) in {e}, proving fixedness. Every fixed point belongs to every iterated range, so no other fixed point exists. Proposition 1 puts every coordinate of every realization in {e}. The constant all-e sequence exists because e is fixed.

No arbitrary-preimage inference is needed. Indeed, f(y) belonging to S need not imply y belongs to S. On the two-point space {e,a}, let f(e)=e and f(a)=e. Then S={e}, although f(a) belongs to S and a does not. This countercontrol is finite, compact, and continuous; even those conditions do not justify the arbitrary-preimage step.

### Proposition 4 Unique realization itself gives a unique fixed point

If B has exactly one element b, then b is constant at a unique fixed point e.

Proof. The tail of b is another element of B and so equals b. Therefore b_i=b_(i+1) for every i. The recurrence gives f(e)=e. Every other fixed point would provide another constant realization.

This proves a fixed-point necessity result without identifying S with C and without making any forward-convergence claim.

## 3 Countercontrols on complete bounded metric spaces

All discrete metrics in this section assign distance 1 to unequal points. They are complete and bounded, and every self-map is continuous.

### Control A Singleton survival without forward convergence

Take X={e} disjoint union N. Define f(e)=e and f(n)=n+1.

For n≥0,

K_n = {e} union {m in N : m≥n}.

Hence S={e}, and Proposition 3 gives exactly one infinite backward realization. Directly, any natural-number coordinate would require a predecessor of 0 after sufficiently many backward steps, which is impossible.

But fⁿ(0)=n and d(n,e)=1 for every n. The orbit does not converge to e. The same failure occurs starting from 1, which already belongs to f(X); restricting starting points merely to the function's image does not help. Thus singleton survival and unique infinite realization do not require pointwise convergence of all forward orbits. The ranges have intersection {e} but remain at Hausdorff distance 1 from {e}.

The function is even injective. Finite fibers or a compatible-ancestry condition alone therefore cannot repair the convergence inference.

### Control B Unique realization without singleton survival

Take

X = {e,r} union { (n,k) : n≥1 and 1≤k≤n }.

Define f(e)=e, f(r)=e, f(n,1)=r, and f(n,k)=(n,k−1) for k≥2. The points (n,1),...,(n,n) form a finite predecessor branch of length n above r. There are arbitrarily long branches, but every particular branch is finite.

The point r belongs to every K_m: choose a branch of length at least m and use its m-th point as a depth-m predecessor. The point e also belongs to every range. A branch point (n,k) has only finitely many further predecessors, so it does not belong to S. Consequently S={e,r}.

Nevertheless B has exactly one element, the all-e realization. Starting from r requires choosing one particular finite branch, which eventually runs out. Starting from a branch point also runs out. A realization starting from e cannot eventually leave e backwards without entering r and then a finite branch. It must therefore remain at e forever.

Every forward orbit reaches e after finitely many steps. Thus this control has pointwise attraction and unique realization, yet nonsingleton finite-depth survival. It specifically refutes the unrestricted identification of finite-depth survival with compatible infinite ancestry.

### Control C Pointwise convergence with many backward realizations

Let

X = {0} union {1/n,−1/n : n≥1}

with its ordinary Euclidean metric. This is a compact metric space. Set f(0)=0, and define

- f(1/n)=1/(n+1) for n≥1;
- f(−1)=1;
- f(−1/n)=−1/(n−1) for n≥2.

Every nonzero point is isolated. At 0, both one-sided sequences and their images approach 0. Hence f is continuous. It is bijective, so it is a homeomorphism.

Its only fixed point is 0. Every positive orbit approaches 0. Every negative orbit reaches −1 after finitely many steps, then 1, and then approaches 0. Thus every forward orbit converges to the same fixed point.

However f is onto, so K_n=X for every n and S=X. Every starting point has a compatible infinite backward orbit obtained by repeatedly applying f's inverse. There are many such realizations. Furthermore sup over X of |fⁿ(x)|=1 for every n, so the convergence is not uniform.

This preserves the warning that pointwise global convergence and a unique fixed point are insufficient for unique infinite realization. It also shows why replacing general completeness with compactness does not make pointwise convergence sufficient.

## 4 Compact continuous repair

### Theorem 5

Suppose X is a nonempty compact metric space and f:X→X is continuous. Then C=S, and the following are equivalent:

1. B contains exactly one infinite backward realization.
2. S is a singleton {e}.
3. There exists a fixed point e such that fⁿ converges uniformly on X to the constant function e.

Each condition implies that e is the unique fixed point and every forward orbit converges to e. Those last two conclusions alone are not sufficient, by Control C.

### Proof that C=S

Every K_n is nonempty and compact, and the K_n form a decreasing sequence. Their intersection S is therefore nonempty and compact. Proposition 1 gives C⊆S.

Fix y in S. For each n, let

A_n = {x in K_n : f(x)=y}.

Because y belongs to K_(n+1)=f(K_n), A_n is nonempty. Continuity makes each A_n closed in the compact set K_n, hence compact. These sets are nested, so their intersection is nonempty. Any x in that intersection belongs to S and satisfies f(x)=y.

Thus f restricted to S is surjective. Starting from any y in S, successively choose a predecessor in S. Ordinary countable dependent choice gives an infinite backward realization beginning at y. Equivalently, one may use compactness of the compatible finite-path sets. Therefore S⊆C.

Notice that this proves existence of an appropriate predecessor in S. It still does not show that every predecessor of y lies in S.

### Proof of 1 iff 2

Condition 2 implies condition 1 by Proposition 3. Conversely, C=S ensures that every point of S begins a realization. If B has exactly one element, Proposition 4 makes its first coordinate e; hence C={e} and S={e}.

### Proof of 2 implies 3

Proposition 3 gives f(e)=e. Suppose uniform attraction failed. There would be some ε>0 and, for arbitrarily large n, points y_n in K_n with d(y_n,e)≥ε. Compactness supplies a convergent subsequence with limit y.

For any fixed m, all sufficiently late members of that subsequence lie in K_m. This set is closed, so y belongs to K_m. Hence y lies in every K_m and therefore in S={e}. But continuity of distance gives d(y,e)≥ε, a contradiction.

Thus sup over y in K_n of d(y,e) tends to 0. This is exactly sup over x in X of d(fⁿ(x),e) tending to 0.

### Proof of 3 implies 2

Since e is fixed, e belongs to every K_n. If y belongs to S, then for every n,

d(y,e) ≤ sup over x in X of d(fⁿ(x),e).

The right side tends to 0, so y=e. This direction requires no compactness or continuity once fixedness and uniform attraction are given.

### Eventual compactness is sufficient

The full state space need not itself be compact. It suffices that K_m=fᵐ(X) be nonempty and compact for some finite m, and that f restricted to K_m be continuous. The set K_m is forward invariant. Apply Theorem 5 there.

Every coordinate of every full backward realization already lies in K_m, since x_i=fᵐ(x_(i+m)). The surviving intersection is unchanged by deleting the first m ranges. Uniform attraction on K_m becomes uniform attraction on X after the finite delay m. Thus the same equivalences hold.

These are sufficient repairs, not claims of logically weakest possible hypotheses. The exact algebraic condition needed for 1 iff 2 is that every point surviving all finite-depth tests extend to a compatible infinite realization. The compact continuous hypotheses earn that condition and independently earn uniform shrinkage of the nested ranges.

## 5 Strict-contraction sufficiency survives

Let X be a nonempty complete metric space. Suppose f is k-Lipschitz for some 0≤k<1, and f(X) has finite diameter D.

Choose any x_0 and form x_n=fⁿ(x_0). For m>n, the triangle inequality gives

d(x_m,x_n) ≤ d(x_1,x_0) kⁿ/(1−k).

Thus x_n is Cauchy and has a limit e. Lipschitz continuity gives f(e)=e. If p is another fixed point, d(p,e)≤k d(p,e), so p=e.

For n≥1, the diameter of fⁿ(X) is at most k^(n−1)D. Since e belongs to every iterated range,

sup over x in X of d(fⁿ(x),e) ≤ k^(n−1)D.

Uniform attraction follows. Therefore S={e}, and B has exactly one realization by Proposition 3. No compactness of X is needed.

Boundedness of the image does real work for global backward uniqueness. On X=R, f(x)=x/2 is a strict contraction with a unique fixed point 0, and every forward orbit converges to 0. Yet f is onto, so S=R, and for each a the sequence x_i=2ⁱa is an infinite backward realization. This does not refute strict-contraction fixed-point uniqueness; it distinguishes that result from uniqueness of an entire infinite backward history.

## 6 What set convergence can mean

For decreasing ranges, the statement that their intersection is {e} is a set-theoretic statement. It does not by itself imply that all members of late ranges lie close to e.

When e belongs to every K_n, Hausdorff convergence of the nonempty ranges to {e}, if expressed through the usual finite-distance formula, is precisely

sup over y in K_n of d(y,e)→0.

This is uniform attraction, not merely pointwise attraction or setwise intersection. In Control A the intersection is {e} but these suprema are always 1. In Control C each point's forward orbit tends to 0 but the ranges never shrink.

Accordingly, treating range convergence as setwise intersection makes the subsequent forward-convergence inference invalid. Treating it as Hausdorff or uniform convergence requires a separate justification of equivalence with singleton intersection. Theorem 5 supplies such a justification under its explicit compactness and continuity hypotheses.

## 7 Scope of the source comparison

The mathematical correction applies when X is the declared domain of item-values on which f is defined, including states that need not extend to complete infinite realizations. It does not automatically apply to a domain redefined as only the coordinate values that occur in already admitted complete realizations.

If X is replaced by C, the unique-realization case immediately leaves X={e}. Universal convergence over that restricted domain then says only that the fixed point stays fixed. This is consistent, but it is a different and much weaker claim about the flow. It provides no information about excluded local states.

The inspected worked-domain locators in the opening source-boundary section are relevant to deciding between these readings. Their function domains and their complete-realization ranges are distinguishable. Restricting a modal-variable map X_i to a selected class Ω of worlds also does not, by itself, redefine the entire domain of its transition function f as Im(X_i restricted to Ω).

An additional semantic condition is needed to infer algebraic uniqueness from agreement across Ω: Ω must adequately represent the candidate solutions whose exclusion is being claimed. If Ω contains only one selected realization, its coordinate maps are constant regardless of how many other algebraic realizations exist. Conversely, the extra algebraic realizations in the controls are not thereby metaphysically possible worlds.

The prudent source verdict is therefore exact: the displayed unrestricted general metric-domain equivalences require correction; an explicit realized-range reinterpretation or added compact continuous hypotheses can avoid the counterexample, but must be stated. No broad rejection of the source's philosophical position or its sufficient contraction examples follows.

## 8 Relation to existential explanation

The new correction strengthens the requirement to state a theorem's domain and completeness conditions. It does not establish that an actual existential inventory is rooted or unrooted. None of the controls is asserted to describe a metaphysically possible cosmos.

The original null result remains simpler. If the represented all-absence assignment is admitted and all full constraints preserve it, it is an actual algebraic solution; no convergence theorem is needed. If a contraction model also claims a distinct positive fixed point, null cannot simultaneously remain in that same strictly contractive metric domain, because two fixed points would contradict contraction. One must expose the changed domain, added existential constraint, or failure of null preservation.

This is a precise mathematical aid to the philosophical source-to-programme comparison. It does not supply the missing same-E collective nonpresupposition premise, nor any new necessary participant.
