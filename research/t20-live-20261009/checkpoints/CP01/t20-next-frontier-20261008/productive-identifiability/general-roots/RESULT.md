# Instrument design beyond two root indices

This separate extension follows the identified limitation of the two-root prime probe. It is a mathematical design question at a fixed issued profile. It does not introduce a third original into the theological argument or claim an additional source-faithful world. All independent-incidence, calibration, fixed-guard and exact-probability assumptions of the parent result remain in force.

## Exact rational design criterion

For r active root indices let n_P count routes with each nonempty positive support P. A probe specifies rational incidence-survival rates x_i. Its no-effect probability is

q(x) = product over nonempty P of (1 - product over i in P of x_i)^n_P.

Assume every factor is positive. For finitely many probes, form an integer matrix M: columns are nonempty supports P; rows are probe/prime pairs; an entry is the prime valuation of that probe's known route-failure factor. Only primes actually occurring in those rational factors are needed. Taking valuations of the observed probabilities gives the ordinary linear system v(q)=M n.

**The instrument identifies all unrestricted finite nonnegative multiplicity vectors exactly if and only if M has full column rank over the rationals.** If it has full rank, the linear solution is unique, and one checks integer nonnegativity and reconstructs every readout. If it lacks full rank, take a nonzero rational kernel vector, clear denominators, and split the resulting integer vector into positive and negative parts. Those are different nonnegative route inventories with identical readouts. A common productive baseline can be added to both.

The necessity is for the unrestricted finite-count class. A small bounded subclass can happen to be injective even when the matrix is rank deficient. The implementation tests that distinction rather than promoting a sufficient rank test into an unconditional bounded-class lower bound.

No hidden route label is observed; the known columns are possible support types. The prescribed generative class and incidence-level actuator still require external warrant.

## Three-root failure and repairs

The seemingly natural single probe (1/2,1/3,1/5) has seven support columns but rank five. A particularly small collision is

failure(B) = 2/3 = failure(C) × failure(AB) = (4/5)(5/6).

Thus one B-only route and independent C-only plus AB routes give the same exact no-effect probability. Adding the same singleton-route baseline for A,B,C to both alternatives makes every root actually occur in both declared supports while preserving the collision. Their numerical endpoint remains one designated effect under the same convention.

A second probe (1/2,1/3,1/7) repairs this design: the stacked matrix has rank seven. That second probe alone has rank six. More probes are therefore not automatically required by root count; their algebraic separations matter.

A different single probe (1/2,1/5,1/7) already has rank seven. Exhaustive tests recover all 128 binary-support multiplicity models from it and from the repaired two-probe panel. This is an exact design comparison, not a claim that the chosen good probe is statistically optimal or physically available.

## Guarded routes and all issued profiles

The fixed-profile failure also extends to the full guarded class; this prevents a misleading repair by pointing to untested solo profiles. Let z_P be a nonzero integer kernel vector of the full-profile valuation matrix. For every absence guard N disjoint from P put

delta(P,N) = (-1)^|N| z_P.

At issued profile S, only P contained in S and N contained in R minus S are enabled. For each such P, the aggregate signed count is

z_P × sum over N subset of R minus S of (-1)^|N|.

It is zero at every proper profile and equals z_P at the full profile. At the full profile its readout exponents vanish because Mz=0. Splitting delta into its positive and negative parts therefore gives two genuinely nonnegative route inventories with equal readouts at every issued profile, for every probe in the deficient panel. The signs are coefficients of a comparison; neither model contains negative productive causes. A common unconditional singleton-route baseline ensures output and participation at every nonempty profile without disturbing equality. Both independent integer kernel vectors of the bad three-root probe pass this all-profile test.

Conversely, a full-rank full-profile matrix suffices for all guarded counts when the panel includes every nonempty issued profile. Decode, at each S, the aggregated support count m_P(S), extending it by zero for P not contained in S. For fixed P let D=R minus P. For V contained in D,

m_P(R minus V) = sum over N subset of V of n_(P,N).

A second Boolean-lattice inversion recovers each absence-guard count. Full-column rank for the whole support matrix also supplies injectivity on any subset of its columns. The implementation reconstructs thirty-two generated three-root guarded inventories under both the good single probe and the repaired two-probe panel.

Thus the full-profile rank criterion is necessary and sufficient for identification of the unrestricted guarded class from this all-profile oracle. It remains a criterion for the declared calibrated, independent-route response law. It does not supply an admission argument for changing necessary original activity.

## Constructive design for any finite number of roots

A universal finite design avoids guessing suitable primes. Keep the issued profile fixed, and for each nonempty subset T of roots set incidence survival to 1/2 on T and to zero outside T. A zero rate suppresses incidence efficacy; it does not remove an issued root or alter absence guards.

Only supports P contained in T can survive. Consequently

q_T = product over nonempty P subset of T of (1 - 2^(-|P|))^n_P.

Because 2^|P|-1 is odd, the 2-adic valuation is

v_2(q_T) = - sum over nonempty P subset of T of |P| n_P.

Boolean-lattice inversion therefore gives

n_P = -(1/|P|) sum over T subset of P of (-1)^(|P|-|T|) v_2(q_T),

with v_2(q_empty)=0. This is a constructive separating family of 2^r-1 probes. It is an upper bound, not a minimal probe count: the single good three-root probe already does better. The implementation checks full rank and both independent decoding methods through four root indices.

This intervention family varies attenuation masks while keeping issued roots fixed. It does not evade the parent's lower bound requiring different issued profiles to recover absence guards that are otherwise never enabled.

## Symbolic response boundary

If the full symbolic polynomial q(x) were available, its factorisation uniquely identifies every n_P. Each factor 1-product(x_i for i in P) is irreducible in Q[x_1,...,x_r]: choose one variable in P, regard it as a primitive degree-one polynomial over the ring in the remaining variables, use irreducibility over that ring's fraction field, and apply the primitive-polynomial lemma. Distinct support factors are not associates, since their constant terms are all one and their monomials differ. Unique factorisation then fixes the multiplicities.

A symbolic response oracle is stronger than one or several measured rational evaluations. The rank criterion states exactly when specified rational evaluations retain the multiplicities; the rank-five collision shows why symbolic identifiability does not automatically survive a chosen numerical probe.

All algebra here is standard. New credit is the explicit instrument-design application, failed three-root transfer, constructed repair and universally separating incidence-mask family. It neither certifies causal realism nor closes the original productive-ground adequacy question.
