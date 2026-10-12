# Joint concavity in a finite mixed team model

## Exact result

For the ordinary independent mixed extension of a finite team payoff table, **joint concavity on the entire product of mixed simplices is equivalent to additive separability of that payoff table**. Therefore joint concavity cannot be added as a harmless general repair for the gap between unilateral stability and global team optimality while retaining genuine payoff interactions.

This is an elementary multi-affine fact. The contribution here is its application to the proposed epistemic-faculty/team bridge, not a claim to a new general optimization theorem. It is an independently proved research result; it is not P14/P15 checkpoint admission or canonical adoption.

## Setting

Let n be finite, let every pure-response set S_i be finite and nonempty, and let w on S = product_i S_i be a real-valued common payoff. The ordinary independent mixed extension is

    W(p_1,...,p_n) = sum_{s in S} w(s) product_i p_i(s_i),

on the full product X = product_i Delta(S_i). The word “independent” is mathematical here: the implemented joint law is the product of the marginals.

All conclusions concern the supplied payoff W. They do not establish that W is truth-directed, normatively authoritative, or an adequate model of a cognitive architecture.

## Theorem

The following are equivalent:

1. W is jointly concave on X
2. W is jointly convex on X
3. W is affine on X
4. There are a constant c and functions v_i on S_i such that

       w(s) = c + sum_i v_i(s_i).

No differentiability assumption needs to be added.

### Proof that joint concavity forces separability

Fix two distinct players i and j, fix pure responses of all other players, and choose responses a,a' of i and b,b' of j. Denote the four resulting pure payoffs by w_ab, w_ab', w_a'b and w_a'b'. The midpoint of the product profiles (a,b) and (a',b') is the mixed profile giving probability one half to each selected response of each player. Its expected payoff is the mean of all four corner payoffs.

Joint concavity applied to that diagonal gives

    (w_ab + w_ab' + w_a'b + w_a'b') / 4
        >= (w_ab + w_a'b') / 2.

Apply joint concavity again to the other diagonal, (a,b') and (a',b). It has the same midpoint and gives the reverse inequality between the two diagonal sums. Consequently,

    w_ab + w_a'b' = w_ab' + w_a'b.

Thus every conditional two-player rectangle has zero mixed difference.

Choose a pure baseline r in S. The rectangle identity says that the payoff increment from changing player i's response from r_i to s_i is independent of any other player's response. Change those other responses one at a time; the increment remains unchanged. Telescoping a path from r to s therefore gives

    w(s) = w(r) + sum_i [w(r_-i,s_i) - w(r)].

Set c = w(r) and v_i(s_i) = w(r_-i,s_i) - w(r). This is condition 4.

Condition 4 makes W equal to

    c + sum_i sum_{a in S_i} p_i(a) v_i(a),

which is jointly affine. Hence it is both jointly concave and jointly convex. Starting from joint convexity gives the same rectangle equality by reversing both midpoint inequalities. This completes the equivalence.

If X contains at least two distinct points, W therefore cannot be strictly jointly concave under the theorem's assumptions. Degenerate singleton strategy factors cause no problem; when X itself is a singleton, strictness conventions are vacuous.

## What the result excludes

For every finite game, each expected payoff is affine in a player's own mixture while the others are fixed. That is the separate concavity used in ordinary equilibrium-existence arguments. It is much weaker than joint concavity of one common W. Confusing the two would make virtually every team game appear to satisfy an optimality premise it does not satisfy.

If W is additively separable, its unilateral maximizers can be chosen independently and a common-interest Nash equilibrium is globally W-optimal. That positive result is genuine. But the payoff no longer contains strategic trade-offs across the players' responses. Other causal or representational interactions in the cognitive architecture can still exist; the theorem removes interactions in this particular scalar payoff, not every possible architectural dependence.

## A nontrivial coordination control

Take the common payoff table

    w(0,0)=2,   w(0,1)=0,
    w(1,0)=0,   w(1,1)=1.

Both pure diagonal profiles are Nash equilibria, but (1,1) is suboptimal. If p and q denote the probabilities of response 0, then

    W(p,q) = 1 - p - q + 3pq.

The rectangle difference is 3. At the midpoint of (1,1) and (0,0) in probability coordinates, W is 0.75, below the average diagonal value 1.5; concavity fails. At the midpoint of the two off-diagonal probability profiles, W is again 0.75, above their average value 0; convexity fails.

This control retains a real common objective, meaningful expected utility and genuine response interaction. The failure of global optimality is not produced by absent or ill-defined payoffs.

## Changing the policy geometry

If a coordinated controller can choose a joint law q on the entire response-profile space, its objective is

    L(q) = sum_s q(s) w(s),

which is linear on the joint simplex even when w has arbitrary interactions. This does not contradict the theorem: q ranges over joint laws, whereas p ranges over marginal vectors that implement product laws. The product-law subset is generally not convex in the space of joint laws.

There are two essential qualifications.

First, with no constraints, correlation does not raise the maximal expected common payoff. A payoff-maximizing pure joint response is already a product of pure marginals. Both optimization domains attain max_s w(s). The advantage of the joint formulation concerns geometry, coordination and constrained implementation, not an automatic increase in the unconstrained optimum.

Second, fixed marginals or other implementation requirements can change the feasible value. In the example, requiring p=q=1/2 fixes the independent law and gives W=0.75. A joint law with the same marginals, assigning one half to each diagonal, gives L=1.5. If the target is the set of diagonal responses, the independent law leaves the target with probability one half on each trial, whereas the diagonal joint law never leaves it. Any repeated-use restoration claim must still state its temporal dependence assumptions.

This is a substantive coordination difference, not evidence that the common objective is normatively correct or that the coordinated bearer is a person.

## Full product is load bearing

The theorem need not hold on a proper coupled subset of the product domain. For the example, restrict p+q=1. Then W=3p(1-p), which is concave on that segment despite the interacting original table. Such a restriction changes the feasible-policy model. In particular, a single player's deviation holding the other fixed may no longer be feasible. One cannot import the original unconstrained Nash interpretation unchanged.

Likewise, a psychologically graded state with nonlinear value need not be the multilinear expectation of a finite response table. Joint concavity could be meaningful in that different model, but it requires the mixture semantics to be supplied independently. A simplex shape does not establish those semantics.

## Effect on the normative bridge

The easiest valid bridge from unilateral stability to global optimality is sometimes too restrictive for the intended architecture. The appropriate alternatives are to:

- justify a different objective/mixture model in which genuine joint concavity is independently warranted
- use a global coordinator with an explicitly authorized feasible joint-law set
- prove a weaker performance guarantee for interacting best-response dynamics
- retain stability without claiming global normative optimality

Choosing between these is an architectural and substantive question. A formally verified optimum still optimizes the supplied objective; it does not establish that objective's authority.
