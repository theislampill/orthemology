# Exact price of one unknown correlated-root class

## Frozen extension and notation

Retain every mechanism and authorization premise of the accepted conditional
dynamic-interlock v2 checkpoint. The actor is given m authenticated interface
labels, and the following **fixed map family**, not an actual-root oracle.
Exactly one unknown class A of c labels belongs to one actual root; all other
labels belong to distinct singleton roots. Here

    c >= 1,   B >= 1,   B < m-c+1,   k = B+c-1.

For c=1 there is no genuine aliasing and this specializes to warranted distinct
root labels. There are n=m-c+1 actual roots. At most B actual roots are tainted
over the entire declared horizon. The map and taint envelope are fixed for that
horizon; no unrestricted root churn or mobile-fault premise is added. A correct
root coherently controls all of its labelled copies and their revocation and
full-command cancellation state. Control-port dependencies, authorization,
non-bypassability, phase service and horizon obligations remain charged as in v2.

Let pi_A send every label in A to its root and all other labels to their own
roots. The possible A are **all** c-subsets. Label-authenticated evidence does
not distinguish them: tainted roots can give the same preparation/cancellation
content and timing as intact ones. The protocol uses fixed observable repair
and revocation families F,G. Every allowed pair of paths/quorums must be safe
in every compatible world. This is not a theorem about arbitrary protocols that
obtain new mapping evidence, impose new owner-transition coordination, or add
unrestricted stateful reconfiguration.

The one-pair examples in UNKNOWN_ATTRIBUTION.md are c=2,B=1 instances. The
general theorem below subsumes them rather than relying on a guessed extension
of their numbers.

### Exact observation and adaptivity boundary

The data available during a macro-attempt are: the chosen label path and full
command; authenticated label-specific preparation replies and their logical
phase timings; an optional truthful effect/no-effect receipt; and authenticated
label-specific cancellation replies and timings. Preparation/cancellation use
the full selected path, as in the protocol. Each new attempt has a fresh nonce.
There is no root-identity attestation channel, partial-cancellation probe,
out-of-path old-command query, internal gate-state readout, or physical-correlation
side channel. Admitted F and G are fixed before this evidence; the actor may
choose the order of trials adaptively within F. Extra probing that refines the
map family and then redesigns F/G is outside this theorem, even if a richer
device interface would make such probing possible.

The covering lower bound uses a quiescent suffix with no owner transitions.
For each maximal label-fault set T, choose a canonical c-subset A of T as the
aliased class and corrupt that root plus the B-1 singleton roots in T\A. On a
tested path meeting T, all labels send the same valid preparation replies; a
tainted gate withholds the physical operation; then all labels send the same
valid cancellation acknowledgements at the same allowed times. Correct roots
really close, and tainted roots may mimic that closure too. Because cancellation
is bound to the entire command and future nonces are fresh, it changes no
subsequent trial's grant behavior. This constructs an identical all-failure
transcript for every still-uncovered T, including the newly visible cancellation
replies. A successful path separates worlds only by whether it avoids T.

Coherent root state can reveal aliasing under additional experiments, especially
partial epoch-delivery probes. Such experiments are not claimed impossible; they
are not observations in the fixed-family/macro-attempt lower-bound contract.

## Theorem A: exact robust cross-image condition

For label sets P,R, write I=P intersect R and s=|I|. Under one c-class A,

    |pi_A(P) intersect pi_A(R)|
      = s - |A intersect I| + 1[A meets both P and R].       (1)

Every shared label outside A gives its own shared root. The one class contributes
one shared root exactly when it meets both sets. Equation (1) also captures a
class bridging disjoint label sets, a corner case that cannot be ignored.

If s>0, minimizing (1) over all c-subsets A gives

    min_A |pi_A(P) intersect pi_A(R)| = max(1,s-c+1).        (2)

Proof: include min(c,s) labels of I in A, filling A from outside I if needed.
Then the class contributes one shared root and collapses as many original
distinctions as possible. No map can collapse more than c labels to one, and a
nonempty I always has at least one image, so this attains the lower bound.

If s=0, the minimum is either zero or one. It is one precisely when every
c-subset must meet both P and R, equivalently

    c > m - min(|P|,|R|).

This forced bridging does not rescue safety because B>=1. Consequently, **for
all cases including empty intersection**, the exact robust condition is

    for every A, |pi_A(P) intersect pi_A(R)| > B
        iff |P intersect R| >= B+c = k+1.                 (3)

The B>=1 restriction matters: (3) is not asserted for zero-fault models, where
a forced bridge can suffice. A compatible map is selected once for a violating
world; no mapping changes during its execution.

## Theorem B: exact observable availability condition

A B-root taint set affects at most k=B+c-1 labels: if it includes the alias
root, at most c+(B-1) labels are affected; otherwise at most B singleton labels
are affected. Every k-subset T of labels is realizable as a maximal tainted-label
set: choose any c-subset A of T as the unknown class and taint its root plus the
B-1 singleton roots in T\A. This is a valid fixed map and a valid B-root fault
set. The assumption B<m-c+1 ensures k<m.

Therefore a fixed repair family F is available in every compatible world iff

    every k-subset T is disjoint from some P in F.          (4)

The same criterion holds for G. Necessity uses the realizing world just given.
For sufficiency, extend any actually tainted-label set of size at most k to a
k-subset and use its disjoint path. It is not assumed that arbitrary labels fail
independently. Universal uncertainty over maps is what makes every maximal
k-subset a possible world.

## Theorem C: sharp arbitrary-family threshold

There exist fixed F,G satisfying robust safety (3) and both availability
conditions (4) iff

    m >= 3k+1 = 3(B+c-1)+1.                                (5)

Lower proof, allowing nonuniform families: if m<=3k, choose k-subsets T1,T2 with
union size min(m,2k). Availability forces some P in F disjoint from T1 and some
R in G disjoint from T2. Hence

    |P intersect R| <= m-|T1 union T2| = max(0,m-2k) <= k.

By Theorem A, those allowed sets violate robust safety in one compatible map.
The final counterexample uses one fixed map and at most B fixed actual faults;
the other maps enter only in forcing the protocol's universally available sets.
This is a universal-protocol argument, not an illicit assembly of separate
world models into one state.

Construction: if m>=3k+1, choose every (m-k)-subset as both a path and a quorum.
Their intersection has at least m-2k>=k+1 labels; every k-set has a disjoint
(m-k)-set. At the minimum m=3k+1 this is q=r=2k+1. The general fixed-threshold
conditions are exactly

    q+r>m+k,       q<=m-k,       r<=m-k.                    (6)

The root-image proof, rather than the bare label count, supplies the enduring
untainted physical veto in every compatible world.

At minimum m, the actual-root count is

    n_min = m-c+1 = 3B+2c-1.

Known root attribution needs 3B+1 actual roots in this interface. Thus the exact
additional actual-root cost of the unresolved c-class is **2(c-1)**. This is a
price of this fixed observation-compatible interface; it is not a universal
cost of provenance uncertainty in all possible systems.

## Theorem D: cancellation is charged at the same lifted budget

A certificate with k+1 distinct labels has at least (k+1)-(c-1)=B+1 actual
roots. At least one is untainted, so authenticated full-command cancellation
has an enduring physical veto. A q=2k+1 selected-label path retains at least
q-k=k+1 good labels and, under the retained independent control-port premise,
can obtain that certificate. Actual-root coherence means the correct root
closes every copy of that exact command before acknowledging on a label.

A smaller uniform label threshold d<=k is unsound for unconditional closure:
choose a compatible map and at most B actual faults covering all d labels (if
d<c, complete the alias class outside the certificate; if d>=c, put a c-class
inside it and use at most B-1 other roots). Those acknowledgers can all falsely
promise cancellation. Thus d=k+1 is the minimum sound label count and it is
available at the threshold construction. The class may supply c labels from
one actual root; those signatures are never counted as c independent roots.

As before, only the authenticated original recipient may cancel its unique
nonce/path command; a raced lawful landing remains adequate, and a completed
certificate blocks later landing. There is no new global cancellation oracle.

## Theorem E: exact attempt cost and covering reduction

For a feasible fixed q/r label-threshold interface, the exact worst-case opaque
macro-attempt count is

    C(m,m-q,k).

Complementary (m-q)-label blocks must cover every possible maximal tainted-label
set T. The proof is v2's covering argument with the realization in Theorem B:
each uncovered T is an actual fixed-map, B-root counterexample, not a fictional
independent-label fault assignment. Preparation and cancellation observations
can be identical in all these worlds; only actual effect is withheld. A safe
cancel closes each failed trial before the next, without revealing a bad root.

At m=3k+1 and q=2k+1, the complement size is exactly k. Each path succeeds in
exactly one of the canonical maximal-taint worlds, so the sharp cap is

    N = choose(3k+1,k).

Exhaust all N paths for the upper bound. A failure-only adaptive history with
fewer than N distinct tests leaves some maximal world untested; use that fixed
map and fault set for the lower bound. Uniformly average over those worlds to
rule out a smaller almost-sure randomized cap. No adversary access to private
coins is assumed. Three charged phases per macro-attempt give an upper phase
budget; stable-delivery origin, residual old work, bounded correct service and
remaining-horizon conditions are exactly those of v2.

Examples at the minimum:

| B actual faults | c correlated labels | k maximal bad labels | m labels | actual roots | q=r | cancel labels | N |
|---|---|---|---|---|---|---|---|
| 1 | 1 | 1 | 4 | 4 | 3 | 2 | 4 |
| 1 | 2 | 2 | 7 | 6 | 5 | 3 | 21 |
| 2 | 1 | 2 | 7 | 7 | 5 | 3 | 21 |
| 1 | 3 | 3 | 10 | 8 | 7 | 4 | 120 |
| 2 | 2 | 3 | 10 | 9 | 7 | 4 | 120 |

## Premise and contribution audit

The new premise is a warranted **family** of possible static root maps, not the
true map. Under that weakened attribution interface the theorem derives an
exact robust criterion and resource price. Revealing a map, probing an additional
root-identity channel, or coordinating owner transitions to avoid particular
path/quorum pairs is a strengthened interface; none is provided for free.

Standard quorum/fail-prone and covering mathematics supplies the proof method.
The 3k+1 and covering formulas themselves are not new mathematics. The bounded
contribution is the exact alias-class/root-image reduction, including forced
bridging and maximal fault-set realizability, and the resulting physical-root,
cancellation and execution costs for this source-attribution question.
No metaphysical source conclusion or fixed-R5 defeat follows.
