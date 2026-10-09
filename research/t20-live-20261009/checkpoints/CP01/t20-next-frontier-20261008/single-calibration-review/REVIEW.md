# Independent review: one rational calibration

8 October 2026. This review is separate from the earlier frozen identification review. It examines the new single-calibration-design sibling and does not modify that earlier result, integrate protected work, or certify source-level causal adequacy.

## Verdict

The construction is correct for every known finite root signature with r >= 1 and finite nonnegative integer route multiplicities. One fixed rational rate vector makes every positive-support failure factor have a private prime. The corresponding valuation matrix has positive diagonal and zero off-diagonal entries, so one exact no-effect probability identifies the active anonymous support histogram.

No counterexample or unresolved mathematical blocker was found. The implementation correctly divides by private valuations greater than one. The theorem does not establish identification of arbitrary real intensities, practical experimental feasibility, approximate-rate robustness or complete actual productive ground.

## Proof attack and resolution

For a selected support P of size k, use k-1 coefficients +1, one coefficient -(k-1), and +k outside P. A subset wholly inside P has zero sum only when empty or equal to P. Any subset containing an outsider has sum at least k-(k-1)=1. This includes singleton P: its member has coefficient zero and outsiders have coefficient one. Absolute subset sums are bounded by r².

Choose distinct primes q_P with q_P-1>r² and primitive roots modulo them. Modular exponentiation turns that unique-zero subset property into a selector: a nonempty S has residue product one modulo q_P exactly when S=P. The strict bound rules out modular wraparound. There are finitely many supports, so arbitrarily many primes and the cyclicity of each nonzero prime residue group provide all selectors.

CRT yields representatives b_i modulo M=product(q_P). They are nonzero because all prescribed residues are nonzero. Setting D=M+1 therefore gives 1<=b_i<M<D and rates b_i/D strictly inside (0,1). This does not require knowing any actual route identity or multiplicity.

For support S, its unreduced failure numerator is D^|S|-product(b_i). It is strictly positive. At q_P, D is congruent to one, so that numerator is divisible by q_P exactly when S=P. Since q_P does not divide D, fraction reduction cannot remove the private valuation. Thus e_P=v_qP(f_P)>0 while v_qP(f_S)=0 for S≠P.

Finite multiplicative readouts then give v_qP(q)=e_P n_P. Dividing by the known e_P identifies every integer count. The recomposition check in the decoder matters: checking only the private-prime quotients would not reject unrelated extra factors in a purported readout.

An initially proposed binary selector is also valid. The simpler linear selector was independently suggested during review and adopted before the author freeze. The reviewer subsequently used incremental CRT, while the author used the direct CRT sum; they produce the same calibration. This shared mathematical construction is not claimed as two independent discoveries.

## Important edge cases and scope

- The private valuation need not equal one. In the reviewed six-root calibration, support mask 1 has private prime 41 with valuation 2; support mask 16 has private prime 107 with valuation 2. The implementation handles both.
- The r=1 case works. With the implemented prime choice q=3, b=1, D=4, the rate is 1/4 and failure is 3/4. The empty-root signature is excluded; it has no nonempty support counts to identify.
- One calibration does not mean one scalar for the complete guarded, multi-effect problem. Every necessary issued profile and every retained joint-absence coordinate still belongs to its prior oracle. The same vector is reused across them.
- At a fixed full issued profile, nonempty absence guards are disabled. The single readout identifies active support aggregates, not those invisible guarded routes. All-profile guard inversion supplies the separate recovery claim.
- Unknown extra roots, hidden effects, correlated route successes, wrong aliases or unknown calibration remain outside the identification theorem. A route emitting only outside the observed catalogue remains invisible to all observed absence probabilities.
- The prime construction supplies an exact rational channel for an integer lattice of multiplicities. It is not a continuous scalar encoding of arbitrary real weights, nor a finite-bit or finite-sample observation claim.

## Statistical claims checked

For at most K routes, a product readout has denominator dividing D^(rK), since each route contributes at most r root incidences. Injective predicted panels therefore have at least D^(-rK) sup-norm separation. The earlier finite-class classification argument can use this very conservative margin; it need not be practically useful.

For unbounded counts at any fixed strictly interior rate x, k versus k+1 identical singleton-support routes have absence separation x(1-x)^k. The product-law total-variation bound gives no uniform finite sample budget as k grows. There is no conflict between that limit and exact rational injectivity. Approximate empirical frequencies cannot be prime-decoded as exact population probabilities.

The calibration numerator/denominator sizes and exact rate premises remain real costs. No universal conditioning, optimality, low-complexity calibration or physical actuator claim has been inferred.

## Frozen verification

The author files are frozen in frozen/. Their original-path hashes are in results/AUTHOR_SOURCE_HASHES.txt and matched after the independent replay.

- All 11 author control groups pass against the frozen implementation.
- Four independently implemented CRT control groups pass.
- 502 zero-sum support patterns are checked through eight roots.
- 5,214 private-prime matrix entries are checked through six roots.
- 60 readouts are reconstructed by the independent decoder through five roots.
- The independent incremental-CRT and author direct-CRT calibrations agree through six roots. A further 60 independently generated readouts are decoded by the frozen author implementation through six roots.

These numbers report verification coverage, not additional discoveries, physical observations or proof of the external causal law. The general existence claim is supported by the written argument, rather than extrapolation from tested root counts.

Review assignment began at 07:29:31 UTC. No historical floor or active-duration certificate is claimed. Ordinary CRT, primitive-root existence, finite products and valuations are standard mathematics; this review makes no literature-priority claim. The bounded-count noise-aware design requested afterward is a separate research step, not part of this frozen result.
