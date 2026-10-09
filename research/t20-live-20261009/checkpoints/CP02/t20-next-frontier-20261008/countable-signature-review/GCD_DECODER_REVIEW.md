# Factorization-free decoding and its complexity boundary

8 October 2026. This reviews the new gcd-based improvement for the base-4 finite-histogram problem. It does not change the observation model or certify actual finitude from one readout.

## Correctness

Write A_e=4^e-1 and let G be the product of A_d for d<e. Starting with A_e, repeatedly divide by gcd(current,G) while that gcd exceeds one. The result K_e retains exactly the complete prime-power factors of A_e whose primes do not divide G. Existing primes are removed completely; new primes are untouched.

Zsigmondy's theorem guarantees K_e>1. A useful mechanical certificate consists of K_e>1, K_e dividing A_e, gcd(K_e,G)=1, and gcd(K_e,A_e/K_e)=1. The last condition matters: a truncated prime-power divisor can pass the first three tests but make maximal composite-power counting return the wrong multiplicity. For example, 3 divides 45 but does not contain its full 3-adic power.

After all larger generators have been removed from a valid numerator, every prime in K_e occurs with valuation n_e times its valuation in K_e. No lower-index generator contains those primes. Hence the maximal power K_e^k dividing the residual has k=n_e, even when K_e is composite. Count that power using a temporary copy, then remove the full A_e^n_e from the original residual. Exact reconstruction, nonnegative counts and the denominator-weight identity close the membership check.

The independent implementation uses an LCM of earlier generators rather than their product. It has exactly the same prior prime support; repeated gcd stripping therefore yields the same K_e. This supplies a separate implementation without calling a factorization or primality routine.

## Early discovery

Strip the input numerator itself successively against A_1,A_2,..., removing all powers of each shared prime. For valid finite data, all numerator primes have appeared by the largest active exponent E. Conversely, a primitive prime of A_E remains uncovered at every earlier step. The first complete coverage step is therefore exactly E, not merely an upper bound.

An invalid rational input might have uncovered factors beyond its denominator-weight limit M. The implementation must stop at M and reject that input rather than searching indefinitely. Unit numerator with positive M is also invalid. The empty model q=1 is handled separately.

## Polynomial expanded-bit bound

For a reduced finite-model rational N/4^M, M is at most half the explicit denominator bit length. A_e has O(M) bits for e<=M, while G has O(M²) bits. Each nontrivial stripping division removes an integer factor at least two, so an A_e requires at most O(e) stripping steps. Across all e<=M there are polynomially many gcd, division, multiplication and power operations on polynomial-bit integers.

Descending extraction and final reconstruction are also polynomial in that explicit input length. The implementation checks the recovered weighted count before building an excessive full factor. Standard exact integer arithmetic therefore supplies a polynomial bit-time algorithm, without a generic integer-factorization subroutine. No optimized polynomial degree is claimed.

This is not a polynomial bound in a compact expression such as 4^(2^i), in the latent route description, in the largest root index, or in a sample budget. A high-index single route already has an exponentially long expanded rational denominator. The algorithm recognizes and decodes a special multiplicative family; it does not provide an algorithm for factoring arbitrary integers.

## Verification and interpretation

The independent LCM-history implementation reconstructs 55 test models, including support code 32 and 1,000 copies of the exponent-1 route. In the latter case early discovery stops at exponent 1 although the denominator-weight bound is 1,000. Invalid denominator, unmatched numerator and inconsistent weight examples are rejected.

The full-weight variant can produce selector checks for every exponent up to M. The early-stop variant relies on the established primitive-divisor theorem to justify completeness outside the scanned prefix. Neither variant upgrades a matching finite candidate to an actual finite inventory in the expanded infinite-route model: the positive infinite-product mimic still shares that finite rational readout. The separate profile certificate retains its own unguarded, independence, visibility and exact-observation premises.

No new kernel formalization, physical measurement, general-purpose factoring result, global-priority claim or protected integration is asserted here.
