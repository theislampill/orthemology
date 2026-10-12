# Closed convex probability constraints preserved by one fixed channel

10 October 2026 UTC. Separate mathematical research packet. Ordinary complete proofs and small exact rational controls. No protected edit, integration, formal-kernel certification, empirical source claim, or programme closure. The root supplied the repeatable-positive-channel candidate; the worker supplied the extreme-point sharpening that removes physical repeatability. The nonnegative-channel extension was then identified by both. This is joint author verification, not independent review.

## 1. Result and the essential quantifier

Fix one finite observation channel for an unchanged finite target. Partition target states according to equality of their entire outcome distributions. A nonempty closed convex probability family is preserved by **every defined outcome update, at every prior in the family**, exactly when it is the convex hull of arbitrary closed convex families supported inside those indistinguishable blocks.

Consequently a single state-separating channel already forces every such invariant family to be a coordinate face. The channel can be noisy and strictly positive. Neither access to every positive likelihood nor an actual ability to repeat the experiment is necessary. In fact, strict positivity is unnecessary too, provided zero-probability branches are left undefined.

The proof uses classical Bayes plausibility and compact-convex extreme-point geometry. It sharpens the inherited interface, rather than inventing a new general probabilistic or convex-geometric mechanism. In particular, the preceding fixed-prior theorem already says that an extreme feasible prior cannot admit an informative complete feasible experiment. Applying that fact to **every extreme point of one globally preserved family** supplies the decisive step here.

The statement is much stronger than feasibility at the current prior. A curved three-state disk below admits a complete positive informative experiment at its centre, while the very next fresh repetition exits the disk. That first experiment is genuinely feasible and must not be rejected by substituting the stronger global contract.

All claims are conditional on C having independently been justified as a probability constraint. A constraint on permitted actions is not automatically a probability equation or a zero-probability event. Numerical compatibility does not establish source reliability, evidence availability, acquisition permission, actual warrant, or noetic restoration.

## 2. Exact finite-channel theorem

Let X={1,...,n}, with n>=1, and let Y be a nonempty finite outcome set. Let

    K(y|i)>=0,                 sum_y K(y|i)=1 for every i.

The target X is not changed by the observation. Write Delta_n for its probability simplex. For p in Delta_n define

    alpha_y(p)=sum_i p_i K(y|i),
    B_y(p)_i=p_i K(y|i)/alpha_y(p),       only when alpha_y(p)>0.

Call a nonempty C subset of Delta_n **K-stable** when B_y(p) belongs to C for every p in C and every y with alpha_y(p)>0. This is forward inclusion, not an assumed equality.

Define i~k when K(y|i)=K(y|k) for every y. Let I_1,...,I_m be the resulting nonempty blocks and kappa_j(y) their common columns. Let

    Delta_(I_j)={p in Delta_n: p_i=0 outside I_j},
    C_j=C intersect Delta_(I_j).

Empty C_j are allowed and are omitted from unions and convex combinations. For p(I_j)>0, write p^j=p(.|I_j), viewed as a law on all n states, zero outside I_j.

**Theorem 1.** For nonempty closed convex C subset of Delta_n, the following are equivalent:

1. C is K-stable.
2. Every extreme point of C is supported inside one I_j.
3. C=conv(union_j C_j).
4. For every p in C and each j with p(I_j)>0, the law p^j belongs to C.

Thus all such stable families are obtained by choosing arbitrary nonempty closed convex C_j inside any chosen nonempty collection of the block faces, then taking their convex hull. There are no additional restrictions on those within-block families.

### Two elementary ingredients

**Bayes plausibility.** Directly from column normalization,

    p=sum_(y:alpha_y(p)>0) alpha_y(p) B_y(p).                 (1)

The omitted zero-alpha outcomes contribute the zero vector before normalization. The coefficients in (1) are positive and sum to one. If p is extreme in a convex C and all displayed posteriors belong to C, every one of them equals p: otherwise, grouping one branch against the remaining branches gives a nontrivial segment representation of p. A sole positive-probability branch already equals p by (1).

**Finite compact-convex generation.** Every nonempty compact convex Q in finite-dimensional Euclidean space is the convex hull of its extreme points. Here is a complete finite-dimensional argument, to make the geometric input explicit.

Work in A=aff(Q), and induct on d=dim(A). A point is the d=0 case. If x is a relative boundary point of Q, choose z_r in A outside Q tending to x, and choose a nearest point a_r in Q to z_r. Compactness supplies a_r. The minimizing property, applied along the segment from a_r to any q in Q, gives

    (z_r-a_r) dot (q-a_r)<=0.

Also ||a_r-x||<=2||z_r-x||, so a_r tends to x. The unit vectors (z_r-a_r)/||z_r-a_r|| have a convergent subsequence with unit limit u in the direction space of A. Passing to the limit gives u dot (q-x)<=0 for every q in Q. The equality set F is a nonempty compact convex face of Q. It is proper, since otherwise aff(Q) would lie in a proper affine hyperplane of A. It therefore has smaller dimension. By induction x is a finite convex combination of extreme points of F, each of which is extreme in Q: any strict Q-segment through a point of F has both endpoints in F by the supporting equality.

If x is in the relative interior of Q and d>0, any line through x in A meets Q in a compact interval with two relative boundary endpoints, with x between them. Each endpoint has the preceding representation. Mixing these representations proves the assertion for x. This completes the induction. No infinite-dimensional extreme-point theorem is needed. Q=C is compact because it is closed in the finite simplex.

### Proof of Theorem 1

**1 implies 2.** Let p be extreme. By (1), every defined posterior equals p. For i in supp(p) and an outcome with alpha_y(p)>0, cancelling p_i in B_y(p)_i=p_i gives

    K(y|i)=alpha_y(p).

If alpha_y(p)=0, nonnegativity of every p_i K(y|i) forces K(y|i)=0 for each i in supp(p). Therefore every column indexed by supp(p) has the same value at every outcome, including the zero-alpha outcomes. The support lies in a single block.

**2 implies 3.** Compact-convex generation gives C=conv(ext(C)). Each extreme point belongs to some C_j by 2, so C is contained in conv(union_j C_j). The reverse inclusion follows from convexity of C.

**3 implies 4.** Write p as a finite mixture of laws drawn from the C_j. Restrict to I_j. Since the blocks are disjoint, only the mixture terms from C_j remain. If p(I_j)>0, dividing by that mass represents p^j as a convex combination of those terms, so p^j belongs to C_j.

**4 implies 1.** Put w_j=p(I_j). For a defined outcome y,

    B_y(p)=sum_(j:w_j>0) [w_j kappa_j(y)/alpha_y(p)] p^j.    (2)

The weights are nonnegative and sum to one; zero terms are omitted. Every p^j belongs to C, so convexity proves B_y(p) in C.

Finally, starting with any chosen closed convex block families, their finite convex hull is compact: it is the continuous image of the product of those compact sets with the finite weight simplex under the mixture map. Formula (2) proves its stability, and disjoint supports ensure its intersection with each selected block face is precisely the chosen family. This proves the classification. QED.

Strict positivity merely makes every outcome defined at every prior. There is no unsupported conditioning operation at a zero denominator.

## 3. Consequences that follow without repeated evidence

### State separation and the old universal theorem

If all columns of K are distinct, every block is a singleton. Its only nonempty probability family is {e_i}, so Theorem 1 says precisely

    C=Delta_S for some nonempty S subset of X.                (3)

Conversely every coordinate face is preserved by every defined Bayes update. A positive binary channel can have pairwise distinct columns for any fixed finite number of states: choose distinct t_i in (0,1) and rows K(+|i)=t_i, K(-|i)=1-t_i. Thus one such channel is enough for (3); arbitrary positive likelihood vectors are unnecessary. Distinct columns do not mean that a realised single receipt identifies the state.

If K has identical columns everywhere, there is one block and every defined update is the identity. The theorem then permits every nonempty closed convex C, as it must.

### The smallest stable closed convex family containing a prior

For an arbitrary p define the finite simplex

    H_K(p)=conv{p^j: p(I_j)>0}.                              (4)

It contains p by its block decomposition, and (2) proves that it is K-stable. Any nonempty closed convex K-stable family containing p must contain every p^j by Theorem 1, hence must contain (4). Therefore (4) is exactly the smallest such family.

The vertices in (4) have disjoint supports, so their convex weights are uniquely their block masses. When K separates states, (4) is Delta_supp(p). This is a closure **inside the class of closed convex stable families**, not a characterization of the posteriors actually reachable after one or finitely many observations.

### Forward inclusion becomes equality in the positive case

For a strictly positive K, formula (2) rescales each block mass by a positive constant and leaves each within-block conditional unchanged. Rescaling by its reciprocal is an inverse on the unrestricted block-weight simplex. Thus every outcome has B_y(C)=C for a globally stable closed convex C. More generally, every positive likelihood constant on each I_j preserves C bijectively, even if that likelihood is not an available outcome of the declared channel.

This is a mathematical consequence, not permission to acquire fictitious signals. For a general nonnegative channel, a defined outcome may remove entire blocks, so surjectivity onto C need not hold.

## 4. Two small exact controls beyond affine equalities

### A globally preserved inequality family

Take three states and

    C={p in Delta_3:p_1>=p_2},
    K(+|.)=(3/4,3/4,1/4),   K(-|.)=(1/4,1/4,3/4).

The blocks are {1,2} and {3}. The first block family is the segment from e_1 to (1/2,1/2,0); the second is {e_3}. Their convex hull is exactly C. Both updates preserve the inequality because its two sides receive the same likelihood factor and denominator.

At p=(1/2,1/4,1/4), the outcome probabilities and posteriors are

    alpha_+=5/8,   q_+=(3/5,3/10,1/10),
    alpha_-=3/8,   q_-=(1/3,1/6,1/2).

Both are feasible and different. C is not a family defined only by affine equalities intersected with the simplex: it has the full affine hull of Delta_3 but is a proper subset. It is also not a coordinate face. This is a positive control for genuinely greater scope than the earlier affine-equality classifier.

### A curved family feasible at one prior but not globally

Let u=(1/3,1/3,1/3), and set

    D={p in Delta_3: sum_i (p_i-1/3)^2<=1/18}.

This is a nonempty closed convex disk with a genuinely curved boundary. It is entirely inside the positive simplex: the squared distance from u to a simplex boundary is 1/6, larger than 1/18. Use the state-separating positive binary channel

    K(+|.)=(3/4,1/4,1/2),   K(-|.)=(1/4,3/4,1/2).

At u, each outcome has probability 1/2 and

    q_+=(1/2,1/6,1/3),      q_-=(1/6,1/2,1/3).

Each squared distance from u is exactly 1/18, so the **complete first experiment** is D-feasible and informative. If a second observation is genuinely fresh and conditionally independent given the same fixed X, another + gives

    alpha_(+|+)=7/12,
    q_++=(9/14,1/14,2/7),
    sum_i (q_++(i)-1/3)^2=1/6>1/18.

This gives an explicit finite global failure witness: q_+ belongs to D but B_+(q_+) does not. No limit or large search is needed. The other second outcome gives q_+-=(3/10,3/10,2/5), with squared distance 1/150. The pair has conditional barycenter q_+, as Bayes plausibility requires.

The points q_+ and q_- are extreme in D, by strict convexity of the squared Euclidean norm. This directly displays the theorem's mechanism: a nontrivial complete experiment cannot remain in D when starting at either such extreme point. Feasibility at the centre does not imply feasibility at those boundary priors.

## 5. Boundaries that the classification does not erase

**Closedness.** For n>=2 and a strictly positive state-separating channel, the open simplex Delta_n^circ is convex and invariant but contains no coordinate vertex. It is not the convex hull of its intersections with the singleton block faces. Compact-convex generation is unavailable. Its closure is a stable face, which is a different family.

**Convexity.** The closed set {e_1,e_2} is preserved by every defined Bayes update but is not the convex hull of its block intersections. The mixture between its points is deliberately excluded.

**All outcomes of a normalized channel.** The single likelihood L=(2,1) preserves {p in Delta_2:p_1>=1/2}, mapping it into a proper subset. Realizing the same update as one row L_+=(2/3,1/3) requires the complementary row L_-=(1/3,2/3). At p=(1/2,1/2), the latter gives (1/3,2/3), outside the family. One selected likelihood does not supply identity (1) with all terms feasible.

**Current prior versus global preservation.** The disk control separates these using exact values. The preceding fixed-prior/minimal-face theorem remains the correct contract when only the current prior and its complete next experiment are at issue. A user-specified time horizon or permitted history family must not silently be replaced by global invariance.

**Physical nonrepeatability and copied evidence.** Nonrepeatability is not a counterexample to Theorem 1; its premise already quantifies over every p in C for one channel. But interpreting B_+B_+(p) as actual evidence requires the appropriate conditional channel. If the second reading is an exact copy of the first disk-control receipt, its conditional likelihood after + is (1,1,1), and the posterior stays q_+, rather than becoming q_++. Algebraic iteration is possible even when physical fresh observations are unavailable. No such physical availability is needed in the main proof.

**Changing target.** The theorem concerns passive evidence about one fixed X. For a concrete obstruction to misusing it, let the old state i in {1,2} produce a noisy state-separating receipt with K(+|.)=(3/4,1/4), while an intervention independently resets the new state X' to r=(1/2,1/2). The joint instrument is

    M_y(i,i')=K(y|i) r(i').

Every posterior about X' is r, so the singleton {r} is invariant for the current-state updates, although it is not a coordinate face. This does not contradict Theorem 1: the receipt distinguishes the old state, and the successor law is not a diagonal Bayes update of that same target. Questions about the old state require retaining its label, as in the inherited instrument results.

**Structural closure is not perfect disclosure.** With binary positive rows (3/4,1/4) and (1/4,3/4), a full-support prior stays full-support after every finite fresh receipt word. At prior (1/2,1/2), the posterior odds are 3^(number of + minus number of -). Even the full-support law (2/5,3/5), whose odds are 2/3, is never an exact finite-word posterior. Nevertheless its smallest closed convex stable family is all Delta_2. In particular, the classification does not make this noisy channel Blackwell-equivalent to perfect state or block disclosure, and yields no finite zero-error identification procedure. The inherited exact-stopping obstruction remains intact.

No sampling rates, optimized experiment policies, asymptotic complexity, or actual source-availability claim is needed or supplied. An arbitrary description of C also need not provide an effective procedure for finding its extreme points; this is a structural theorem, not a general algorithm for nonlinear constraint descriptions.

## 6. Short crosswalk to inherited continuation observables

For the passive diagonal instrument D_y=diag(K(y|.)), take the inherited H-Continuation starting readout to be the constant function 1. Its invariant span is

    A_K=span{1, K(y_1|.) ... K(y_r|.): r>=1}.

This is the unital algebra generated by the likelihood rows: products concatenate words. Every element is constant on each I_j. Conversely, for each pair j!=k choose an outcome y(j,k) at which kappa_j and kappa_k differ. The polynomial function

    f_j(i)=prod_(k!=j)
      [K(y(j,k)|i)-kappa_k(y(j,k))] /
      [kappa_j(y(j,k))-kappa_k(y(j,k))]

is 1 on I_j and 0 on every other block. For one block the empty product is 1. Therefore A_K is exactly the space of block-constant functions. The f_j are its block-indicator idempotents; Theorem 1 describes the stable law families split along these same blocks. This is finite separating interpolation applied to the inherited observable-span construction, not a new general moment or predictive-state theorem.

Under the formal repeated passive instrument, ideal word probabilities are p dot (K(y_1|.) ... K(y_r|.)). Their linear combinations recover p(I_j)=p dot f_j, and no such observable distinguishes within-block conditional laws. Thus three claims must stay separate: distinct columns identify state labels as different observation laws; ideal word-probability data recover block masses (the full prior law if blocks are singletons); a realised finite positive-likelihood history still cannot certify one of several supported blocks with zero error. The last claim does not follow from either of the first two. Treating those products as the law of actual repeated evidence still requires the fresh conditional-independence premise.

## 7. Optional connection to the root's repeated-word argument

For strictly positive K, the original proposal provides a second proof of the block-conditioning implication. Fix p and a supported block j. Choose integer outcome counts n_y(N) summing to N with n_y(N)/N tending to kappa_j(y). Such counts exist by rounding, and they define finite words. For a distinct block k, the corresponding likelihood ratio satisfies

    (1/N) log[prod_y kappa_k(y)^n_y(N) /
                    prod_y kappa_j(y)^n_y(N)]
       -> sum_y kappa_j(y) log[kappa_k(y)/kappa_j(y)]
        = -KL(kappa_j || kappa_k)<0.

For completeness, strict positivity and log t<=t-1 give KL(a||b)>=0 for probability vectors a,b, with equality only when they coincide. Hence all distinct supported block likelihood ratios tend to zero. Within a block the likelihood factors agree, so the posterior sequence tends to p^j. Global stability puts every finite algebraic iterate in C; closedness then puts p^j in C. Convexity gives the decomposition.

These words are mathematical witnesses. Their physical likelihood is the displayed product only under fresh conditional independence for the unchanged target. The extreme-point proof makes this whole asymptotic construction unnecessary for the classifier and works when likelihoods have zeros. No consistency or rate theorem is imported.

## 8. Inherited comparison and primary-source ancestry

The bounded local comparison used the following exact reports, whose hashes and reading scopes are recorded in INPUT_BINDINGS.json:

- The Bayes-feasibility packet already classifies preservation under every positive likelihood, gives the exact support-restricted affine diagonal/incidence test for specified likelihoods, and separates current-prior first-step success from unchanged repetition. The present increment is one normalized finite channel and arbitrary closed convex C, including the exact block decomposition and smallest stable family.
- The constrained-learning packet already proves splitting, minimal-face reachability, and nonextremality as the fixed-prior condition for informative complete feasible experiments. Its extreme-prior implication is the probabilistic core of the shorter proof here. The new work applies it globally and completes the block classification; it does not claim a new splitting lemma.
- The warranted-learning packet already supplies the barycenter identity, source-factorization and duplicate-evidence controls. The state-changing and fixed-source boundaries remain inherited obligations.
- H-Continuation Theorem 2 already supplies general stochastic instruments and invariant observable spans; the exact-inquiry and quotient-transport packets already distinguish support, finite certificates, almost-sure stopping, and predictive probabilities. Those are not consequences newly introduced by this convex-family classifier.
- The posterior-inquiry-value packet already proves that conditional answers alone do not preserve expected inquiry value. No expected-value or optimal-inquiry result is added here.
- The measure-Bayes-face packet concerns universal likelihood preservation on infinite spaces with topology-dependent conclusions. No infinite-state or infinite-outcome extension is claimed here.

The mathematical ancestry is explicit:

1. Kamenica and Gentzkow, [Bayesian Persuasion (2011)](https://web.stanford.edu/~gentzkow/research/BayesianPersuasion.pdf), section I.B, Proposition 1, gives the posterior-mean restriction and converse signal construction. Those passages were inspected. Here only the elementary posterior-mean identity is needed, and it is proved directly. The earlier fixed-prior packet owns the fuller splitting comparison.
2. Compact-convex representation by extreme points is classical finite-dimensional convex geometry. Krein and Milman's [On extreme points of regular convex sets (1940)](https://www.impan.pl/en/publishing-house/journals-and-series/studia-mathematica/all/9/1/93490/on-extreme-points-of-regular-convex-sets) is the primary broad ancestry record. The publisher's bibliographic entry was inspected; its download returned 403, so no original theorem numbering or full-text inspection is claimed. The finite-dimensional proof needed here is supplied completely above.
3. Recursive convex Bayesian belief-set methods also predate this packet. Phelan and Skrzypacz, [Beliefs and Private Monitoring (2012)](https://web.stanford.edu/~skrz/phelanskrzypacz.pdf), introduction and the set-operator/Lemma 2 passages, treats extreme beliefs and recursive convex sets in finite-state repeated games. This is relevant methodological ancestry, with evolving strategic states rather than the present fixed-target channel. No whole-paper absence or priority claim is made.
4. A recent title match, Bayraktar and Wang, [Convex order and preservation of convexity for Bayesian posterior updates (2026)](https://arxiv.org/html/2609.05065v1), was checked in its abstract and introduction. Its convexity concerns expected functions of a scalar posterior statistic under exponential-family observations. That inspected scope is different from a closed convex subset of the full finite belief simplex being preserved outcome by outcome. No broader non-overlap claim is needed.

This is a bounded source comparison, not an exhaustive literature or repository search. The mathematical statement is an elementary synthesis and a useful sharpened interface; no field-level novelty is claimed.

## 9. Verification and provenance

Run from this directory:

    python3 verify.py

The script uses fractions.Fraction throughout and checks nine small control groups: the globally stable inequality example; the curved local-versus-global disk; a zero-likelihood block channel and impossible branch; the explicit minimal-hull components and reweighting; nonclosed/nonconvex boundaries; a single-likelihood/complementary-outcome discriminator; copied versus fresh receipts; a state-changing instrument; and exact block-indicator interpolation. It also verifies unchanged hashes of the bound inherited inputs. CHECK_RESULTS.json and verification.txt record the run. These controls corroborate the calculations; the complete proof establishes the universal theorem.

The root supplied the original repeatable-positive-channel conjecture, the minimal stable-family consequence, the simple inequality control, and the inherited observable-algebra crosswalk. The worker replaced repetition by the extreme-point proof, supplied the complete geometric lemma, curved exact discriminator, detailed crosswalk proof, and source comparison. Both then identified the nonnegative-channel extension. These are joint derivation and author checks, not independent assessment or audit closure. All outputs are confined to this separate scratch packet.
