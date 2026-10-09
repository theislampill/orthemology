# A decoder without integer factorisation

The prime-order decoder remains as an independent alternative. A later root-proposed gcd construction removes its generic factorisation requirement and gives deterministic polynomial bit complexity in the ordinary expanded rational input representation.

## Construction and certificate

For input q=N/4^M in reduced form, put A_e=4^e-1. The finite-model denominator identity gives e<=M for every actual support code. Set G_0=1 and build G_(e-1)=product_(d<e) A_d.

Starting from A_e, repeatedly divide by gcd(current,G_(e-1)) until the gcd is one. Call the remainder K_e. This removes every complete prime power whose prime occurred in an earlier generator and leaves the full A_e valuations of every new prime. Zsigmondy's base4 case guarantees K_e>1.

The implementation records four checks for each selector:

- K_e>1;
- K_e divides A_e;
- gcd(K_e,G_(e-1))=1;
- gcd(K_e,A_e/K_e)=1.

The last condition matters. A selector containing only part of a new prime's power could multiply the recovered count. A raw divisor merely coprime to history is not enough. Repeated complete stripping naturally provides the stronger condition.

Now work in descending e. Keep the actual residual numerator unchanged while dividing a temporary copy repeatedly by K_e. The maximal divisibility exponent is n_e: every prime in K_e occurs in no smaller A_d and occurs in K_e with its full A_e valuation. Higher actual generators have already been removed. Require the full A_e^n_e to divide the original residual, then remove it. Finally require residual1 and sum(e n_e)=M, and reconstruct q exactly.

This uses gcd, multiplication, division and comparisons only. It neither factors the large numerator nor computes multiplicative orders.

## Exact early stopping

While constructing A_1,A_2,..., independently strip from the input numerator every prime power shared with each new A_e. When that residual first becomes one, every true active generator has index at most e. Otherwise a primitive prime of a larger active generator would still be present and could not yet have been stripped. Conversely, after the largest active generator has been reached, all numerator factors have appeared. On valid inputs, the stopping index is therefore exactly the largest actual support code.

This is useful for high multiplicity at a small support. The test with5,000 copies at e=1 has denominator weight5,000 but needs only the first selector. A separate full-weight implementation path gives the same result on the smaller controls.

## Complexity scope

Let L be the bit length of the explicitly supplied binary numerator and denominator. The denominator itself has2M+1 bits, so M<=L/2. Each A_e and K_e has O(M) bits; each history product G_e has O(M²) bits. Each stripping loop removes a factor at least2 and therefore has polynomially many iterations in those bit bounds. There are at most M generators and polynomially many exact gcd/division operations. Descending count extraction also has polynomially many divisions, and the weighted-size check prevents construction of a full generator power larger than the input bound permits.

Standard deterministic integer arithmetic therefore gives a polynomial-time decoder in L, with a deliberately loose bound. No optimal exponent or practical complexity claim is made. This is not polynomial in a compact expression such as “4^M”, in the latent histogram description, or in a port index i: the one-route denominator at i already has2^(i+1)+1 bits.

Optional resource caps return `ResourceInconclusive`, distinct from `InvalidReadout`. A refused large input is not evidence against the finite model. The uncapped mathematical algorithm terminates on every finite explicit rational input, accepting exactly the model readouts under the proved arithmetic premises.

## Controls

Six groups compare the gcd and prime-order decoders on all272 weighted histograms through weight12; recover support codes31,127 and256 without calling a factorisation routine; exercise high multiplicity and early stopping; check composite primitive selectors and full prime valuations; compare full-weight and early paths; and distinguish invalid inputs from resource exhaustion.

The new gcd code is an additional implementation in this package. It does not replace or retroactively relabel the earlier prime-order proof, and it does not authenticate the supplied exact probability as an empirical or source-faithful observation.
