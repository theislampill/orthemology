# Final author-packet review: audit continuation transport

10 October 2026 UTC. This is a second, separately bound independent review. The earlier `REVIEW.md`, input bindings, independent checker, and results are preserved unchanged. This review covers the final author packet; it does not authorize integration, protected edits, release, T20 closure, or a field-novelty claim.

## Finding

**No mathematical or executable blocker found in the reviewed scope.** The final packet faithfully transports the finite source-audit experiment, retains the necessary admissible cone, distinguishes fixed rereads from fresh verifier experiments, and states the posterior-only tensor/feasibility criterion consistently with the previously reviewed root candidate. The added binary-audit boundary classification and continuous-coordinate lower-bound application are valid with their explicit domain qualifications.

The reviewed author result is `../audit-continuation-transport-20261010/RESULT.md`, SHA-256 `3add44ffbe7e0bf188f870259bce338387385e1e5c04a5d98a3716cb2c2a84cc`.

The reviewed author checker is `../audit-continuation-transport-20261010/verify.py`, SHA-256 `962b8dc227918f460c6ede1f6e4cf2fe4bfc93632229e6c10efabb0248f3da2c`.

The independently reproduced author control output is `../audit-continuation-transport-20261010/CONTROL_RESULTS.json`, SHA-256 `179e0faf24cbf33d7e2885b044e17ac6dc4f64fd93f2d95bd7bc338417545866`.

## Substantive checks

### Predictive transport and its state domain

For full row-rank `B`, the invariant-space equations `BM_a=T_aB`, `u=νB`, and `C=LB` define a valid commuting reduction. The `T_a` are unique in the selected row basis. The domain `K=B R_+^n` is essential: arbitrary coordinate vectors can represent signed, inadmissible latent laws even when their target and audit marginals look plausible. Because `νBr=ur`, mass is nonnegative on `K`, and a zero-mass element of `K` must be zero. This also proves pointedness and validates the impossible-branch convention.

Cone preservation means `T_a K⊆K`; it does not require an onto map. The packet's following calculation correctly establishes this into-cone meaning. Signed entries in the basis-coordinate transition matrices do not invalidate the construction.

The stated full predictive equivalence is exact for normalized laws. For live unnormalized laws it is the normalized reduced coordinate `Br/(ur)` that determines conditional future behavior; absolute evidence mass is a different, stronger contract. The packet keeps these distinct. Its inherited `k−1` continuous-coordinate bound remains a full-simplex statement and is explicitly not assigned to the two reachable neutral histories.

### Faithfulness to the source audit

The bound source-audit snapshot explicitly uses uniform independent target/type, report accuracy `9/10` or `1/2` according to type, a conditionally independent `4/5`-accurate verifier, and audit `A=(T,1[V≠Y])`. The final packet retains those variables and meanings. The diagonal projectors represent revelation of that same fixed random variable.

The eight-mass map `G` groups by `(Θ,T,D)`. Its four commuting equations and target-readout factorization hold exactly. Target indicators multiplied by audit projectors span rank eight. Including future report readings over the unrestricted latent-law domain yields rank sixteen, since `(Θ,T,Y,D)` identifies every original state. These claims are about the declared domain and observation repertoire, not an assertion that a subject must retain sixteen states or a literal transcript.

On the known-Bad slice, the four masses of `(Θ,D)` give the sufficient quotient. The two report histories have identical target and audit marginals but different target–audit joint numerators, producing `4/5` and `1/5` after `D=1`. The Walsh moment update formulas in §4 are correct for arbitrary retained moments. The inadmissible vector `(1,0,0,2)` reconstructs signed masses and gives the displayed negative target probability; excluding it is a state-domain requirement.

### Fixed versus fresh verifier identity

The old audit projectors are idempotent, and opposite readings multiply to zero. Consequently a matching reread has conditional probability one and leaves posterior `1/5`. The alternative likelihood matrices really describe fresh conditionally independent verifier draws. Two fresh disagreements after `Y=1,Bad` give `(1−α)^2/((1−α)^2+α^2)`, hence `1/17` at `α=4/5`. This is a change of experiment, not a contradiction or permission to substitute one instrument for the other.

### Posterior-only comparison and nonlinear quotient

The final paired test preserves the earlier criterion's essential safeguards: finite explicitly supplied alphabet, all words including the empty word, synchronized same-symbol tensor transitions, fixed target readout, nonnegative live states, exact rational decision scope, and a separate support-language comparison. The stated right multiplication/prepending convention is correct. Common feasible first-symbol updates preserve the equivalence, so a set-theoretic partial continuation quotient exists. No unsupported finite-dimensional or linear parameterization of that quotient is claimed.

The strictness example now uses independent target/source laws and source-only likelihoods. Target answers stay uniform under every word, while event probabilities differ (`3/8` versus `5/8`); this is a valid nondegenerate separation from full predictive equivalence.

For one fixed binary audit with both marginals positive, `(q,q0,q1)` reconstructs the joint law off independence and collapses the audit-frequency fibre on independence. At `t=0` or `t=1`, the feasible language identifies the supported audit value and `q` identifies the remaining joint law. Thus the final boundary extension is valid.

The additional lower-bound paragraph is also valid: parameterize strictly positive laws by `(t,q0,q1)∈(0,1)^3`. The signature map is `((1−t)q0+tq1,q0,q1)` and has Jacobian determinant `q1−q0`. Off independence there is an open three-dimensional set on which the signature is injective. Any continuous globally exact encoder must be injective on that set, so the inherited invariance-of-domain argument excludes fewer than three real coordinates. This is limited to continuous encodings over the full binary joint-law family; it is not a bit bound, generic paired-tensor dimension bound, or three-coordinate lower bound for two histories.

## Replays and independent additional controls

I ran `python audit-continuation-transport-20261010/verify.py` successfully. Its stdout is preserved as `AUTHOR_REPLAY_STDOUT.json` and is byte-identical to the author's `verification.txt`. The regenerated `CONTROL_RESULTS.json` is byte-identical to the initially supplied output. All eight author-bound inherited inputs pass the author's currentness check.

The replay establishes the reported source-model ranks/posteriors, fixed/fresh control, strictness and zero-branch controls, 4,225 fixed-audit law-pair comparisons, 36 seeded rational instruments, 1,740 word-pair checks, 8,136 reduced updates, and 729 support-language controls. These are bounded exact corroboration of the written proof, not an exhaustive proof by sampling.

The separate `final_transport_checks.py` uses SymPy 1.14.0 and imports no author code. It independently verifies the four `G` commuting diagrams, exact ranks eight and sixteen, target-readout factorization, two general Walsh update formulas, the known-Bad law and posterior formulas symbolically in `α`, the fresh-verifier result, and the signature Jacobian. It passed; output is in `FINAL_TRANSPORT_RESULTS.json`. The author's replay remains standard-library-only; this additional independent symbolic checker has the stated SymPy dependency.

## Source/publication scope

The final packet correctly attributes the full predictive closure and continuous full-simplex lower-bound method to H-Continuation, and support-sensitive fibre/congruence results to H-ICS. I inspected the relevant H-ICS probability-channel and observation-congruence statements; they do not themselves assert the new posterior-only interface. The source-audit snapshot owns the numerical countermodel and triple-interaction obstruction. Those mechanisms are not relabelled as newly discovered here.

The final publication account also respects the earlier review's caution: Kiefer et al. is cited for the inspected Kronecker/finite-span machinery, not as an exact posterior theorem. I additionally inspected [Droste and Kuske, *Weighted automata*](https://www.informatik.uni-leipzig.de/theo/pers/droste/papers/Droste-Kuske-AutoMathA-neu.pdf), Lemma 4.3 and its adjacent qualification, plus Theorem 8.3 and Corollary 8.4. The product construction requires the indicated commutation condition, satisfied over the rationals; the finite-generation/computability hypotheses support the zeroness/equivalence ancestry. This is a targeted passage check, not a complete literature search.

The author explicitly limits Tzeng access to abstract/metadata and distinguishes this packet's concrete specialization from field-wide novelty. No unresolved priority claim is silently approved by this review.

## Preservation and disposition

`FINAL_PACKET_BINDINGS.json` binds the final author files, inherited inputs, prior review artifacts, and new review/replay artifacts. The earlier review remains unchanged. The only author output touched by replay was regenerated identically. No protected source, adopted theory, integration state, or programme status was changed.

Disposition: the reviewed final packet is suitable to retain as a bounded, source-attributed mathematical result with reproducible exact controls and this independent review. That disposition does not grant any larger audit, release, or closure authority.
