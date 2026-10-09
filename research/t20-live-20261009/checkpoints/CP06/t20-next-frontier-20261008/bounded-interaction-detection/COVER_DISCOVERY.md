# A promised finite interaction cover replaces the count ceiling

8 October 2026 UTC. This is a separately scoped second sufficient contract in the same fixed finite independent-route model. It uses the covered-root gap in RESULT.md section 7 and the previously reviewed positive-count procedures. No total route ceiling is assumed in this note.

## 1. Promise and conclusion

The root universe R is known and finite. The inventory is fixed and finite in each world, with unguarded nonempty supports, one effect, independent route successes and one common coordinatewise continuous strictly increasing endpoint-preserving calibration per root. The oracle provides certified positive-error rational approximations to population Q at requested rational commands.

Assume additionally:

    Every root i in R belongs to at least one positive support S with |S|>=2.

The positive supports themselves and their counts are not supplied. Under this structural coverage promise, a terminating Cauchy-oracle procedure discovers enough positive interactions to decide every support's presence and recover every route multiplicity. It requires no total count ceiling, effective calibration modulus or exact-real equality test.

If R is empty, the only allowed inventory is empty and the conclusion is immediate. A nonempty one-root universe cannot satisfy the displayed promise. The proof does not silently discard unused or uncovered declared roots to force coverage.

## 2. Sound finite-support positivity searches

Fix one common rational interior base vector b, for example every b_i=1/2. Enumerate the finitely many candidate supports S contained in R with |S|>=2.

For each candidate, its ordinary zero/interior multiplicative contrast is

    E_S(b_S)=product_(T subset S) Q(b_T,0_else)^((-1)^(|S|-|T|))
            =(1-product_(i in S)r_i(b_i))^n_S.

Every raw Q in this expression is positive, since every enabled route has an interior true-rate factor and the inventory is finite. Certified input intervals can therefore eventually be propagated through the product and quotient. Under the model,

    E_S=1 if n_S=0;
    E_S<1 if n_S>0.

Refining until a certified upper endpoint is below one is a sound positivity semidecision. It eventually succeeds for every genuine positive support, but is not expected to stop for an absent support.

Use a fair schedule across the finite candidate family; for example at stage k request progressively finer raw-Q enclosures at the common base masks and give every unwitnessed contrast a refinement attempt. All contrasts can reuse the same finite raw base panel. The schedule never waits for an absent candidate to finish before examining another candidate.

Whenever a positive interaction is witnessed, recover its integer count using the earlier four-isolated-value, half-integer-cut procedure. It terminates under exactly the positive-support promise just certified. Without a supplied ceiling, use its integer-bound doubling step followed by binary search. These count computations may be scheduled fairly alongside the searches, or completed one at a time: every initiated count computation has a valid positive support and terminates, and there are only finitely many candidates.

Maintain the union D of supports whose positivity has been certified AND whose counts have been recovered. Stop the discovery phase only when D=R. Mere failure to witness an additional support is never used as evidence of its absence.

## 3. Why coverage is eventually certified

For each root i, the promise supplies at least one actual positive interaction S_i containing i. There are finitely many roots, so these S_i constitute a finite cover, even though the algorithm does not know it initially.

Each S_i has a strictly positive contrast gap at the fixed interior base. Fair certified refinement therefore eventually witnesses it. Its positive count procedure then terminates. There are finitely many such witnessing and count-recovery completion times, so their maximum is finite. By that time D=R, unless the algorithm has already completed through a different certified cover.

The proof assumes no common lower bound on the positive gaps, no common count ceiling and no uniform completion-time bound. It proves termination for each admissible world and every valid Cauchy name under the coverage promise.

## 4. Complete the count recovery

Once D=R, use the recovered counts of the certified cover to compute their positive support products at the same common base. Refine to rational positive lower bounds and propagate them to every covered root as in RESULT.md section 7. Because every declared root is covered, the separated midpoint test decides every nonempty support's zero/positive status.

Recover every further positive multi-root count with the previously reviewed positive-count procedure. All unary absences are now known. Every positive unary root belongs to a certified interaction, so the imported ANCHORED_UNARY_COUNT.md ratio/sign theorem recovers its integer count with unbounded integer bracketing and half-integer cuts.

No full-rank condition on a support-incidence matrix is needed: each known product supplies a lower bound for every factor even when a finite product panel does not determine the individual factors uniquely.

Thus every multiplicity is returned after finitely many population queries and finite computations for this input. There is no isolated-unary count ambiguity: every root is interaction-anchored by the promise and its actual certificate. This conclusion concerns counts and supports. It does not reconstruct entire calibration functions from finitely many values.

The algorithm uses zero/interior masks and interior interaction/unary panels. Unlike the bounded algorithm's first phase, it does not use unit Boolean corners to discover the cover. The standing model assumptions remain unchanged; this observation is not a theorem for a different calibration class.

## 5. Without the promise

Run the same discovery process without assuming coverage. Every positivity certificate, recovered count, lower bound and eventual full-cover completion remains sound. It completes only after obtaining an actual known-count positive cover of the whole declared finite root universe.

If some declared root is not in any positive interaction, that completion condition never occurs. This is a sound partial procedure, not a total detector for arbitrary unbounded inventories. Nontermination, elapsed time or failure to obtain a certificate yields no conclusion about absent supports or unused roots.

The unrestricted absence obstruction remains applicable to its class: its absent base has an unused B root and supplies no positive interaction cover. The present structural promise excludes that base rather than contradicting the earlier theorem. Known finite R is essential to this completion argument; no countably infinite-root or unknown-root-universe version is claimed.

This consequence was proposed by the parent after the covered-root gap was independently reviewed. It is credited as a constructive extension of that same mechanism, not another proof of the inherited sign lemmas. No uniform precision/runtime/sample guarantee, physical validation, inference of the coverage promise, protected integration or T20 closure follows.
