# Exact opaque-repair portfolios and root/attempt tradeoffs

This extends the **same** versioned interlock model, without adding observation
or trust resources. It does not revisit Sixth's static message-alphabet problem.
All commitments, revocations, gate occurrences, and causal path selection remain
charged as in MODEL_AND_PROOFS.md. Counting only signatures is still insufficient.

## 1. Exact reduction for arbitrary feasible thresholds

Fix n,B,q,r satisfying the three threshold inequalities, with q>=1. For a
candidate repair path L, write A=R\L and k=n-q. If C is the lifetime taint set,

    L is entirely untainted  iff  C is contained in A.

Thus a path portfolio guarantees at least one untainted attempt exactly when
its k-element complements cover every B-subset of R. Covering maximal fault sets
also covers smaller sets, since any smaller set extends to a B-subset. Write
C(n,k,B) for the minimum size of such a covering. The exact optimal worst-case
sequential opaque-failure attempt count is

    M(n,B,q,r) = C(n,n-q,B).

Upper bound: choose a minimum covering and attempt its complementary paths.
Some path is untainted; all attempts are adequate repair or identity, so the
fixed prepare/execute/cancel batch works without trusted effect receipts.
Cancellation needs B+1 acknowledgements from selected-path roots, uses the same
budget and independent control-port premise, and closes a withheld attempt
before the next one. M counts macro-attempts; their bound is 3M logical phases
when all three declared phase bounds are one. The threshold inequality still
protects every one of these paths against every allowed revocation quorum.

Lower bound: let faulty roots give all truthful preparation and cancellation messages with
the same timings as intact roots, and let a tainted path fail with no root
attribution. Before success an adaptive policy
has only the same failure outcome, so its choices along that history form one
ordered portfolio. If its first m complements do not cover all B-sets, choose
one uncovered C as a **fixed** lifetime fault set. Every one of those m attempts
then fails. Hence adaptivity cannot beat the covering number on this observation
interface. For an almost-sure randomized cap, put a uniform distribution on the
finite maximal fault sets, independently of the policy coins. Every m<C(n,k,B)
failure-history portfolio leaves at least one fault set uncovered; its averaged
failure probability is at least 1/choose(n,B). Some fixed C therefore has positive
failure probability, contradicting the cap. The adversary need not see coins.

If a failed attempt discloses a reliable failed-root identity, or a common gate
can be tested once and then removed from all supports, this lower argument does
not describe that different interface. If failures destroy future paths, its
upper argument no longer applies. This theorem depends on both restrictions.

Covering designs are established mathematics. This is a model-specific exact
reduction and resource-accounting consequence, not a claim to discover covering
numbers or a new general distributed-computing lower bound.

## 2. Revocation size changes the available repair portfolio

For fixed n,B,r the smallest safe q is

    q_min = n+B-r+1.

It is feasible only when q_min<=n-B, equivalently r>=2B+1. Increasing r decreases
the number of serial gates required for each path, and enlarges its complement
block. Availability still limits r<=n-B.

For fixed n and B, every feasible q is at least 2B+1. Minimum sequential attempts
among these threshold choices are therefore attained at

    r = n-B,       q = 2B+1,
    M_opt(n,B) = C(n,n-2B-1,B).

Proof of optimality: a covering with smaller blocks can be extended to blocks of
size n-2B-1 without losing coverage. Hence increasing the allowed complement
size cannot make the optimum worse. Taking maximum available r realizes that
size. This optimizes attempt count, not every resource simultaneously: its
revocation certificates use r labels, and each path uses q live gate occurrences.

A selected m-path portfolio can be deployed as m prebuilt branches, with qm
gate occurrences owned by n roots. The selector may choose among those branches
but cannot bypass their gates; all-good selected branches remain independently
addressable. This reduces unused branch deployment relative to constructing all
choose(n,q) branches. It does not create qm independently failing roots.

## 3. Exact small-family frontier with ordinary lower proofs

For B=1, n>=4, q=3, r=n-1:

    M_opt(n,1) = ceil(n/(n-3)).

The complements must cover the n individual roots and have size n-3. Counting
gives the lower bound. Partition the n roots into that many groups of size at
most n-3, then pad any small group to a distinct (n-3)-subset. These blocks cover
all roots. Thus n=4,5,6 require respectively 4,3,2 attempts; every n>=6 requires
2. One attempt is impossible because its nonempty path contains some potentially
faulty root. The corresponding prebuilt gate counts are 12,9,6, with r=3,4,5.

For B=2, maximum available r and q=5 give these exact values:

| n | r | complement size k | minimum attempts | prebuilt gate occurrences |
|---|---|-------------------|------------------|---------------------------|
| 7 | 5 | 2 | 21 | 105 |
| 8 | 6 | 3 | 11 | 55 |
| 9 | 7 | 4 | 8 | 40 |
| 10 | 8 | 5 | 6 | 30 |

The machine-readable witnesses in COVERING_WITNESSES.json supply upper bounds.
They were found locally and verified by a separate standard-library checker.
Optimality rests on the following ordinary lower proofs, not on floating-point
solver status or on a web table.

### Pair-incidence lower bound

In any (v,k,2)-cover with m blocks, a point must occur in at least
ceil((v-1)/(k-1)) blocks, because each such block can pair it with only k-1 other
points. Counting point-block incidences gives

    m >= ceil( v * ceil((v-1)/(k-1)) / k ).

This standard covering bound gives 21 for (7,2,2), 11 for (8,3,2), and 6 for
(10,5,2). Combined with the explicit upper witnesses it establishes those exact
values. For (9,4,2) it gives only 7; the following argument rules 7 out.

### A standalone proof that seven 4-blocks cannot cover all pairs of 9 points

Suppose seven 4-subsets cover all pairs. Each point occurs at least three times.
There are 28 incidences, so exactly one point x occurs four times and the other
eight occur three times. (A cover with fewer than seven blocks is already
excluded by the incidence bound.) A point y!=x has nine companion slots in its
three blocks but must meet eight other points. Thus it has exactly one repeated
companion, counted with multiplicity.

Consider the four blocks containing x. Each other point must occur in one or
two of them; occurrence three would repeat x twice, exceeding its repetition
allowance. Those four blocks have twelve other-point slots. Consequently four
points A occur twice and four points D occur once. Every A-point has used its
entire repetition allowance on x, so it may meet each other point only once.
It occurs in exactly one of the three blocks not containing x.

Represent an A-point by the pair of x-blocks in which it occurs. These are four
distinct edges of a simple graph on the four x-blocks: two identical edges would
make those A-points meet twice. Any four distinct edges on four vertices contain
two disjoint edges. To see this, an intersecting family of edges has size at
most three: if all share one vertex this is immediate; otherwise three form a
triangle and no fourth edge meets all of them.

Let a,b be the two A-points with disjoint x-block pairs. They do not meet in an
x-block, so their pair must lie in a common non-x block. This block needs two
more points. No third A-point can join it: its pair of x-blocks intersects at
least one of a's or b's pairs, so that companion pair would repeat. No D-point
can join it either: its one x-block belongs to exactly one of the two disjoint
pairs, again creating a repeat with a or b. x is excluded by definition. There
are no remaining kinds of point, a contradiction. Eight blocks are necessary,
and the supplied eight-block witness proves sufficiency.

The small graph fact has all 15 four-edge cases checked independently and also
as a kernel-checked finite Lean proposition. The incidence/repetition reduction
is the ordinary argument above; it is not labelled fully Lean-formalized.

## 4. What the tradeoff changes

The minimal-root design can be expensive to execute because its only good path
is the complement of the entire hidden maximal fault set. A few additional
independently justified roots allow one harmless test to succeed for several
possible fault sets. This is a causal-support gain, not extra disclosure bits.
The gain is purchased by more genuine root modules, more revocation witnesses,
and a correctly mediated selected-branch deployment. Copies of existing roots
do not buy it; neither does moving selection outside the charged support map.

No claim is made that these small covering numbers are new. The independent
primary-source comparison in PRIOR_ART.md expressly records known quorum and
covering theory. The useful result is their exact place in this fully declared
versioned repair contract, with distinct proof and engineering obligations.
