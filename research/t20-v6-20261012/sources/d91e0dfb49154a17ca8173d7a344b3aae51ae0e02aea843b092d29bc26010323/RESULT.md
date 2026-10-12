# Exact loss profiles, fixed decisions, and finite typed sidecars

11 October 2026 UTC. A narrow interface corollary of the reviewed uncertainty-inquiry result and inherited continuation/sidecar theorems. Ordinary mathematical proofs and exact controls; no original-source or repository changes, new Lean theorem, psychological memory bound, or programme closure.

## Finding and credit

For the actual C4 moment body and E4 triangle after history 11, preserving every one of the six declared policy losses is equivalent to retaining the pair (t,s). The minimum among continuous real-coordinate encoders is exactly two. If the exact current target posterior q=3t is already retained, exactly one additional real coordinate suffices, and no finite tag alphabet can replace it. The latter obstruction needs no continuity assumption on the tags.

This does **not** imply that solving the one fixed robust game needs two continuously varying inputs. Once its entire uncertainty family, history, price and policy contract are fixed, its minimax policy and value are fixed outputs and can be precomputed. That weaker output contract does not preserve the per-model loss profile.

These are direct restricted-family consequences of machinery already earned: H-Continuation owns the continuous-coordinate lower-bound mechanism; D1–D2 own finite contract refinement and fibre tags; uncertainty_inquiry owns the exact bodies, laws, six-policy game and solved minima. The contribution here is the explicit comparison of their different input/output contracts, including an exact cardinality obstruction on this particular posterior fibre. No new general minimum theorem or field-wide novelty is claimed.

The actual source successors must also be distinguished. PT19's finite-sidecar owner supplies deterministic typed table computation. PT20's rational-kernel successor **already supplies** finite rational joint-law realization by typed deterministic lookup plus an external conditional seed-law premise. Neither is a representation of every real point in C4/E4 by finitely many ordinary tags. A claim that this programme lacks stochastic source-law transport would undercredit PT20.

## 1. The exact profile and its inverse

Use the reviewed contract unchanged: observed X1=X2=1 of common mass 1/3; optional paid observation X3; reserved target Y=X4; wrong-label loss plus price c; one complete model chosen before a private policy coin. Write t=P(111), s=P(1111). The remaining ordered pair law is

    (P00,P01,P10,P11)=(1-6t+3s, 3(t-s), 3(t-s), 3s).

In the order skip0, skip1, query-always0, query-copy, query-invert, query-always1, the loss profile is

    F_c(t,s)=(3t, 1-3t, c+3t, c+6(t-s),
              c+1-6(t-s), c+1-3t).

This follows directly by summing the wrong-report cells. Constant reporting ignores the reading; copy errs on the off-diagonal cells; invert errs on the diagonal cells. For any fixed known c, two entries recover the coordinates:

    t=(1-F_skip1)/3,
    s=t-(c+1-F_invert)/6.

Consequently F_c is injective, of affine rank two, on both domains. Every independent private mixture has the same mixture of these losses, so preserving these six entries preserves every declared randomized-policy expected loss, and conversely the deterministic policies are members of that class. This conclusion holds for every fixed real c, although the original interpretation requires c>=0.

For this specific restricted law family the profile also determines the entire four-bit law: each ordered word with k ones has the inherited probability

    k=0: 1-4t+s; k=1: -1/2+3t-s; k=2: 1/3-2t+s;
    k=3: t-s; k=4: s.

Thus it preserves every model-independent bounded path loss on that same finite experiment. This equivalence is special to the declared family and informative policy menu; an arbitrary policy set need not determine its path law. New semantic costs, permissions or provenance predicates are not supplied by the probability coordinates.

## 2. Two continuous coordinates are necessary and sufficient

The domains are the inherited compact sets

    C4: 2/9<=t<=5/18,
        12t^2-4t+4/9 <= s <= -6t^2+5t-2/3;
    E4: convex hull of (1/6,0),(1/4,1/4),(1/3,1/3).

Both have nonempty planar interior. For C4, at t=1/4 the strict gap is 5/24-7/36=1/72; an intermediate s and continuity of the boundary functions give a small open neighbourhood. The E4 vertices are noncollinear.

Suppose E:D->R^d is continuous and an arbitrary decoder recovers F_c exactly for every point of D, where D is either domain. Injectivity of F_c forces E to be injective. For d=1, restrict E to a small circle contained in the interior. A continuous injection from a circle to the real line is impossible: its minimum and maximum occur at distinct points, and each of the two arcs joining them must, by the intermediate value theorem, contain a preimage of every strictly intermediate value. The two distinct preimages contradict injectivity. d=0 is immediate. The identity encoder (t,s) attains d=2.

This elementary circle proof is the two-dimensional instance of H-Continuation's topological argument. Its full-simplex formula cannot simply be copied numerically onto a restricted curved moment body; the interior/injectivity argument above justifies the restriction directly. No regularity of the decoder is required. Discontinuous arbitrary-precision encodings into one real number are outside the continuous-encoder theorem; no bit, word, physical-storage, tensor-factor, or human-cognitive lower bound follows.

## 3. One extra real coordinate over the posterior; finite tags fail

The current target posterior is q=P(Y=1|11)=3t. Retaining (q,s), or equivalently (q,3s), suffices: 3s is the target–reading joint-success probability. At the common posterior q=3/4, the possible fourth coordinates are

    C4: s in [7/36,5/24],
    E4: s in [1/6,1/4].

For either nondegenerate interval, different s give different query-copy and query-invert losses. Thus q alone fails. Adding one continuous real coordinate s succeeds, so the relative minimum number of added real coordinates is one.

More strongly, suppose only a tag k in a finite alphabet of size M is added to q, with arbitrary assignment and arbitrary decoder. Choose M+1 distinct s in the displayed fixed-q interval. At least two have the same tag and q but different query losses. Hence no such scheme works. Indeed a countable alphabet also fails for the whole interval. Continuity of k is unnecessary. This is a cardinality argument about the exact numerical profile, not the original finite D2 theorem applied outside its finite-state hypotheses.

An exact discriminating C4 pair is

    (t,s)=(1/4,7/36) and (1/4,5/24).

Both have q=3/4 and skip1 risk 1/4. Their copy error probabilities are 1/3 and 1/4; their invert errors are 2/3 and 3/4. At c=1/10 the invert losses are 23/30 and 17/20. The posterior collision changes a declared query loss by exactly 1/12 while leaving every skip loss unchanged. These points are genuinely realizable by the reviewed lower/upper boundary constructions, not merely positive pair tables detached from the fixed earlier moments.

## 4. The weaker fixed-game contract

For the fixed full-family robust game the reviewed values and policies are

    C4: V=1/3, skip/report1 (uniquely for c>0);
    E4: V=min(1/2,2/5+c/5).

For 0<c<1/2, E4's unique distribution over complete plans uses skip/report1 with probability 4/5 and query/invert with probability 1/5. These are inherited solved-game results, not new optimizations here.

For a fixed family and price, an encoder whose only obligation is to return that optimal policy and robust value can be constant: no per-model numerical input is needed. At c=1/10 it returns respectively (skip1,1/3) or (the stated mixture,21/50). If the family identifier is variable, it must still be supplied; if c or the loss/menu changes, that changed contract must still be supplied. Precomputing a result does not erase those inputs or the evidence certifying its validity.

There are three distinct objects: a per-model law/profile; the uncertainty set over such profiles; and the minimax answer for one fixed set and objective. The two-coordinate theorem addresses the first. It is not a lower bound on storage needed for the third, nor a claim that two numbers encode every possible uncertainty subset. Also, t and s are representation coordinates for Nature's candidate law, not lawful information disclosed to the decision maker. Letting the policy observe the selected model's coordinates would change the robust game.

## 5. Positive finite repairs and exact typed-source boundary

For a **nonempty finite selected model set** Q within either domain, distinguish models only up to identical (t,s). Relative to retaining t, the exact loss-profile tag minimum is

    max_t |{s : (t,s) in Q}|.

Necessity is the same fibre argument; sufficiency labels the finitely many distinct s separately within each fibre. This is D2's finite labelling mechanism specialized to the loss-profile equivalence, not a claim that a weaker loss-profile quotient always satisfies D1's stronger one-step joint-kernel contract. When a continuation contract is wanted, its actual reachable history states and joint transitions must also be represented.

PT19 uses natural coarse/tag data with a fixed proof slot, not real posterior data. On a finite Q the distinct retained posterior values can be assigned natural codes. Declared numerical outputs may likewise be represented by finite natural lookup codes; exact rational numerators/denominators can be tabulated when applicable. This does not prove an intrinsic real-number evaluator or silently equate real values with natural numerals.

For a finite **rational** Q, all sixteen path probabilities are rational. PT20 already realizes these finite laws by externally seeded typed lookup: draw a complete four-bit word once from the chosen model's rational row and thereafter use deterministic coordinate-reading transitions; alternatively use exact conditional rational rows at positive histories. The joint next-state/outcome law must remain coupled, and the model/hidden-word implementation state must not become visible to the policy. The independent private policy coin has its own lawful timing; the 1/5 coin is rationally realizable under the same external seed-law discipline. This is an application of the inherited counting theorem, not a newly compiled source construction in this packet.

A finite collection with irrational law entries is not covered by PT20's fixed finite-uniform-seed architecture. More generally, a fixed D-element uniform seed produces only n/D probabilities. Since 3t varies over an interval on the whole C4/E4 class, no one such fixed interface can reproduce all those laws. Even a rational continuum restriction can have unbounded denominators. This is an architecture-specific obstruction, not impossibility for alternative real representations, nonuniform external seeds, or unbounded random-bit algorithms. Finite-state capacity is not the same as finite program description: rational pairs can be encoded by unbounded natural data and decoded by suitable rational arithmetic. Nothing here establishes an expressivity impossibility for original Has, or rules out variable-denominator computation. PT20 proves its specified finite interface; the continuous-coordinate theorem and finite-tag obstruction cannot replace an analysis of a different unbounded-data source implementation.

If exact continuum profile preservation remains the requirement, the mathematical positive repair is (q,s) plus the law-family and finite-horizon contract. Actual source execution over all real points needs an additional representation/computation interface; the finite-tag and finite-uniform-seed owners do not supply it. If only the already-solved fixed-game output is needed, retain its certified answer and contract instead. Approximation or menu narrowing changes the obligation and must be stated explicitly.

## 6. Horizon and source limits

Four moments preserve this four-bit experiment. A fresh success takes unnormalised m_j to m_(j+1), and a failure to m_j-m_(j+1), followed by normalization on positive branches and a reduction of the supported remaining horizon. No four-coordinate invariant filter for arbitrary fresh continuation follows. The reviewed fifth-moment collision already supplies an exact counterexample to that extension. Re-reading a fixed bit remains deterministic and does not create a fresh trial.

All conclusions concern stipulated laws, observations and losses. They neither identify human warrant with expected classification loss nor estimate anyone's cognitive retention. The affirmative philosophical findings and the source-specific semantic obligations are unchanged.

## Evidence status

READ_LEDGER.json binds the actual owner texts and read scopes. check_exact.py independently evaluates complete-word losses, reconstructs both coordinates, checks the two posterior fibres and a finite-tag pigeonhole fixture, and checks inherited fixed-game certificates at c=1/10. Normal and optimized positive runs and deliberately false claims are recorded in CHECKS.json. Finite controls supplement the written continuum/cardinality arguments; they do not prove them by sampling. No independent review of this packet is claimed.
