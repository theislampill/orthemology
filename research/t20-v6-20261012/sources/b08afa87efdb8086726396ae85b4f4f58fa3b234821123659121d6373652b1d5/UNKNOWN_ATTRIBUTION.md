# Unknown fault-root attribution: a bounded observable-interface result

This is a new bounded extension of the fresh versioned-interlock family, not a
reconstruction of missing Seventh work. Its starting checkpoint is v2 archive
SHA-256 `ac63a34c92479385771f3b3c9d292a728ca8d2b7aacf0dbf215a391bd7d08644`.
v2 is author-verified and, when this extension begins, independently under review.
Its physical, institutional, timing, cancellation and persistence premises are
retained; none is discharged by the result below.

## 1. A fixed hidden root map, not moving roots

There are m authenticated observable interface labels A={0,...,m-1}, m>=3.
Exactly one unknown pair P={a,b} labels the same actual root; all other labels
name distinct roots. Thus there are m-1 actual roots, a fact the actor knows.
The possible map family contains every choice of the one aliased pair. Fix the
map before the session; it never changes. At most **one actual root** is tainted
over the whole claimed horizon. It may affect all of that root's labels and
copies together. No probability or independence premise is used.

Root authentication is now only label authentication. The ordinary preparation,
cancellation and owner-transition transcripts do not identify which labels
share a fault root. In the worst case every label supplies identical correct
content and timing, with correctly label-authenticated messages. No available
query is a warranted label-to-fault-root oracle. Merely knowing m-1 actual roots
does not identify four or more independent witnesses in a particular packet.

For a label set L, write pi(L) for its actual-root image. A correct actual root
coherently owns all of its gate copies and local revocation/cancellation state:
an authenticated effective revocation delivered on either alias closes all of
that root's old-epoch copies. This gives the positive interface its strongest
natural case. If common fault provenance does not also provide this coherent
correct-root control, the image-intersection criterion below is not sufficient;
that would be a different implementation contract.

The actor chooses actual label-indexed physical paths from a fixed family F and
the owner completes epoch revocations using a fixed accepted label-quorum family
G. These families are visible and do not change with an unobserved pi. Every
path remains a live serial interlock; independently authenticated control access,
full payload and recipient binding, and charged cancellation are as in v2.
The claim is about these fixed observation-compatible families, not every
unrestricted adaptive reconfiguration protocol.

## 2. Exact robust lifting of the interface conditions

With one actual-root fault, cross-epoch safety requires and, under the retained
v2 causal premises, is ensured by

    for every possible pi, every L in F and S in G:
        |pi(L) intersect pi(S)| >= 2.                         (RS)

At least one shared actual root is then untainted and vetoes an old command.
Conversely, if their root images share at most one root, corrupt that shared
root (or use no fault if the intersection is empty). The other revocation roots
close only copies outside the repair path. A genuine-looking old commitment and
an effective revocation can then coexist with an open stale path. This is the
same exact mechanism counterexample, evaluated under one fixed compatible map.

Repair and revocation availability require, respectively,

    for every pi and actual root c, some L in F has c not in pi(L);  (RA)
    for every pi and actual root c, some S in G has c not in pi(S).  (VA)

All actual-root support roles must remain accounted; a logical image calculation
does not erase a common selector or control-port blocker. Cancellation similarly
needs a label-acknowledger set K whose image has at least two actual roots, and
enough intact selected roots/ports to supply it. Claims are warranted uniformly
over the maps compatible with the received evidence. Replacing pi by a guessed
map would not be this robust criterion.

## 3. Five labels over four roots: no fixed family can meet all three conditions

Use labels 0,1,2,3,4. In the map aliasing {0,1}, let that aliased root be faulty.
RA requires an allowed path L contained in {2,3,4}. In another admissible map
aliasing {2,3}, let its aliased root be faulty. VA requires an allowed quorum S
contained in {0,1,4}.

Because F and G are fixed observable families, both L and S are allowed under
every compatible map. Return to the first map, aliasing {0,1}. For these two
chosen sets their actual-root images intersect in at most the one root carrying
label 4. This violates RS. Therefore no pair of fixed label-only families can
supply robust repair availability, revocation availability and cross-version
safety. The argument allows nonuniform set sizes, overlapping portfolios, and
arbitrarily many paths; it is stronger than a threshold-only failure.

A concrete illustration matches the intuition. Every 4-label path intersects
every possible faulty alias pair, so it cannot guarantee an intact repair path.
For 3-label paths, take L={0,1,2}, S={2,3,4}, pi aliasing {0,1}, and corrupt the
single actual root carrying 2. The actual root images are {01,2} and {2,3,4};
the only shared root is faulty. It falsely acknowledges revocation while leaving
its gate open, and all other path roots retain their old local grant. The stale
operation lands. It is not a failure caused by exceeding the one-root budget.

This does not contradict v2's four-root construction. That construction has
warranted root attribution, so its sets are actual-root sets. The present actor
has five labels and only an unresolved map family. A stronger oracle identifying
the aliased pair would change the evidence interface.

## 4. Six labels over five roots still fail; seven labels suffice

For m=6, partition labels into P={0,1}, Q={2,3}, T={4,5}. Availability under a
faulty P-alias root forces some L contained in Q union T. Availability under a
faulty Q-alias root forces some S contained in P union T. Evaluate both under the
compatible map aliasing T. Their images intersect in at most the one T-root.
Again RS fails. For m<=4 there are at most three actual roots, so even a known
map cannot satisfy the familiar one-fault cross-intersection/availability
conditions: choose a path avoiding one root and a quorum avoiding a second;
their intersection is contained in the remaining at-most-one root.

For m=7, take every 5-label path and accept every 5-label revocation quorum.
Their label intersection has at least three labels. A single aliased pair can
collapse at most one of those distinctions, leaving at least two actual roots.
Hence RS holds. One faulty actual root affects at most two labels, leaving at
least five good labels, so RA and VA hold. Every 5-label path contains at least
four actual roots, so its containment support cannot be wholly tainted.

Cancellation uses **three label acknowledgements**, not two. Three labels have
at least two actual roots, including an untainted veto. A selected 5-label path
retains at least three good labels even when the faulty root supplies two of its
labels. Independent authenticated control access therefore provides the three
replies. The same full-command tombstone, race, scope and phase arguments apply.
Two acknowledgements could be exactly the two labels of the bad alias root and
would not prove closure.

Thus seven labels over six actual roots is the exact minimum in this declared
one-unknown-pair family, even when fixed families may be nonuniform. With a known
map, four actual roots would suffice. The difference is an attribution-warrant
cost in this interface; it is not evidence that labels become fault roots.

For uniform threshold families at any m>=5, the exact constraints are

    q+r >= m+3,       q<=m-2,       r<=m-2.

Sufficiency follows from the preceding counting. Necessity of availability
follows by corrupting an aliased root. If q+r<=m+2, choose q- and r-subsets with
at most two shared labels. With two shared labels choose them as the aliased
pair, leaving one shared actual root. With at most one shared label choose an
alias pair that does not create a second shared actual root. Such a choice
exists for m>=5: either alias two labels in one exclusive side, or use a label
outside the union; in the full-union case one exclusive side has size at least
two. This violates RS. The three inequalities are jointly feasible exactly
when m>=7. At m=7, q=r=5 uniquely.

## 5. Exact opaque trial bound for the seven-label construction

There are 21 possible alias pairs P. In the world where P is aliased and that
one actual root is faulty, an all-intact 5-label path must be exactly A\P.
Corrupt labels can give the same valid preparation/cancellation messages and
timings as all others while withholding only the attempted execution. Every
failed path then excludes exactly one such world, namely the world whose pair
is its complement. Therefore 21 macro-attempts are necessary in the worst case
and the full 21-path batch attains that cap. The same finite averaging argument
as v2 rules out a smaller almost-sure randomized cap against every fixed world.
Single-label faulty-root worlds are also covered by that portfolio.

The declared resources are: six actual root modules behind seven label ports;
five physical gate occurrences per tested path; five label acknowledgements per
effective epoch transition; three per-command cancellation acknowledgements;
and a 21-path portfolio (105 gate occurrences if all branches are prebuilt).
Three logical phases per macro-attempt give an upper phase budget, with the
same stable-delivery boundary and residual-old-attempt qualification as v2.
These are correlated ports, not seven independent roots.

## 6. Warrant, prior art, and limits

The broad mathematical method is established Byzantine fail-prone/quorum
reasoning; Malkhi–Reiter's primary text already treats nonuniform correlated
failure sets. No novel quorum threshold or combinatorial method is claimed.
The local contribution is the exact observation-compatible map lift and this
bounded separation: the true count of actual roots need not yield a selectable
robust protocol when their attribution to executable labels is unresolved.

There is no fresh mapping oracle. Revealing the actual alias pair would permit
choosing one representative per root and applying v2 at four roots, but that is
an explicitly stronger input requiring its own independent warrant. Numerical
carrier identity, root provenance, descriptor correctness and control authority
remain different coordinates. No sourcehood or truthful-agency theorem is used.
Nothing here enlarges the fixed R5 resource set or establishes its defeat.

Finite checks enumerate the declared maps and label sets. The added Lean file
proves that the preimage of one faulty actual root has at most two labels and
derives a sound cross-quorum witness from that counted bound. The ordinary
five-/six-label nonuniform impossibility proofs and the 21-world lower bound
remain explicit ordinary proofs, rather than being labelled fully kernel-checked.
