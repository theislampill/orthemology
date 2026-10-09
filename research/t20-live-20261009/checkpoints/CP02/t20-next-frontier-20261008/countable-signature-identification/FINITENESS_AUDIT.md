# What an exact rational readout says about finitude

This audit extends the response model to countably many independent routes. Each route still has a nonempty finite positive support and emits the designated observed effect. It is a mathematical hypothesis test, not a claim that infinitely many actual productive occurrences or necessary originals exist.

## A computable infinite mimic

Write f_e=1-4^(-e). Fix E>=1 and target q=f_E. Starting from Q_E=1, for each e>E choose the largest nonnegative integer n_e for which

Q_(e-1) f_e^n_e >= q,

and set Q_e to that product. Then

q <= Q_e < q/f_e,
so 0 <= Q_e-q < q/(4^e-1).

Consequently Q_e converges to q with an explicit effective error bound.

Each digit n_e is at most4. To see this, put t=4^(-e)<=1/16. Expanding gives

(1-t)^5 <=1-5t+10t² <1-4t,

hence f_e^5<f_(e-1). Since Q_(e-1)<=q/f_(e-1), multiplying by five copies of f_e would already go below q. The initial stage has equality in that preceding bound; later stages have strict inequality.

The root's initial candidate message had this last factor inequality reversed. It was corrected during independent appraisal before use. The proof requires f_e^5<f_(e-1); the earlier wording was never treated as a proof or preserved as a theorem.

There are infinitely many nonzero digits. If only finitely many were nonzero, a finite product of f_e with e>E would equal f_E, contradicting the finite multiplicative independence proved using Zsigmondy. Each individual support has bounded multiplicity, and

sum_(e>E) n_e 4^(-e) <=(4/3)4^(-E)<infinity.

Thus this is not a zero-product pathology. Under the countable independent-route law, the no-effect probability is the positive infinite product q=f_E, exactly the same as one finite route with code E. The finite prefixes differ from q; the code does not present any prefix as the infinite process itself.

For E=1 the exact rational readout is3/4 in both cases. The finite decoder returns one route at port0, but that is a correct conclusion only under its finite-model premise. In the infinite model every support code is greater than1.

Prime valuations cannot be passed through this real limit. The finite prefixes have increasing numerator valuations at3 and increasing powers of four in the denominator, while their real limit3/4 has fixed finite valuations. This locates the failure of the finite proof. A finite denominator of the limiting probability is not evidence that the underlying weighted route count is finite.

## A second exact query can certify finitude in the unguarded class

Suppose an exact positive rational all-issued readout q admits the finite decoder's candidate. Let R0 be the finite union of that candidate's positive supports. Issue only the ports in R0, retaining their same calibrated rates, and obtain q_R0. Assume throughout that there are no absence guards, every route affects the absence event being compared (the designated common effect, or no output anywhere in a complete finite catalogue), and the stipulated route independence and positive success probabilities hold.

If q_R0=q>0, no actual route can touch a port outside R0. Any such route has a strictly positive success probability s. Its failure is independent of the event that all inside routes fail; therefore q<=q_R0(1-s)<q_R0, a contradiction. This argument does not require the outside routes to be finite in number.

There are only finitely many nonempty support subsets of the finite R0. If infinitely many route occurrences remained inside, some support would occur infinitely often. Its identical positive success probability would force the no-effect probability to zero, contradicting q_R0>0. Hence the actual route inventory is finite. The finite identification theorem then proves that the candidate histogram is the actual one within this model class.

Every genuinely finite model yields such a certificate. This is a sound conditional finite witness, not an algorithm deciding whether every arbitrary real probability law has a rational representation. The protocol is specified when its exact rational readouts and candidate are available. It does not decide arbitrary irrational infinite-product cases from approximations.

The infinite greedy mimic fails the second query. If P0 is the binary support of E, every greedy support has code greater than E and therefore cannot be contained in P0. Its restricted no-effect probability is1, whereas the full probability is f_E<1.

## Exact equality and the unguarded condition are essential

No fixed positive near-equality tolerance works uniformly across unbounded indices. Choosing E=2^i makes the finite candidate and its infinite mimic differ on the restricted query by only4^(-2^i). With the full readout already exact and its candidate root set fixed, however, an additional discrete inside-count bound supplies a candidate-dependent positive gap. That can certify the second equality at sufficiently high finite precision; see `ORACLE_AND_EXTENSION_BOUNDARIES.md`.

Guards can defeat the certificate even when both supplied probabilities agree exactly. Add to the infinite greedy tail one route with positive support P0 and an absence guard containing an index outside P0. At the all-issued profile this new route is disabled and the tail has probability f_E. At the P0-only issued profile the whole tail is disabled while the guarded route is enabled, again giving f_E. This intervention changes the issued profile and reevaluates guards; merely setting outside incidence rates to zero while keeping all ports issued would leave the guarded route disabled. The two-query equality now coexists with infinitely many routes active at the full profile. This does not refute the certificate: it violates its unguarded premise.

Unknown dependence can likewise invalidate the reasoning. Infinitely many perfectly correlated route occurrences need not drive a no-effect probability to zero. Correct occurrence aliasing and the route-success independence law remain substantive prerequisites.

These positive and negative results sharpen the scope of the exact readout. They do not establish that the candidate routes are causally real, that the ports name underived bearers, or that the source permits the profiles and attenuation scheme.
