# Exact identification with unknown finite input signature

The root-proposed design is valid for finitely many unguarded routes on a countably indexed port alphabet. This is a conditional mathematical observation theorem. It does not establish countably many necessary originals or physical access to the stated oracle.

## Fixed calibration and model

Index possible input ports by i=0,1,2,... . Fix, once and for all,

x_i = 4^(-2^i).

Every productive route has a nonempty finite positive support S and emits the same designated visible effect. Its success probability is the product of its port probabilities. Different route successes are independent. There are finitely many actual route occurrences, with natural multiplicities. No upper bound on their number, supports or largest port index is supplied to the decoder. Initially there are no absence guards.

Encode support S by e(S)=sum over i in S of 2^i. This bijects nonempty finite subsets of the port alphabet with positive integers. Repeated representations of one support member do not add another power of two. The route succeeds with probability 4^(-e), and its failure factor is

f_e = (4^e-1)/4^e.

With n_e the finitely supported natural multiplicity function, the exact all-issued no-effect probability is q=product_e f_e^n_e. A support code e is an integer index, not a created effect identity or intrinsic act token.

## The primary arithmetic input

Zsigmondy's original specialised order theorem, printed p.283, provides a prime of order e for base4 for every e>=1. Its exceptional bases and exponents do not include this case; the following paragraph explicitly uses base4. The original was visually checked at that page. [Zsigmondy 1892 original scan](https://zenodo.org/records/2131326/files/article.pdf?download=1).

The modern primary research paper by Győry and Smyth states the primitive-divisor result in Theorem13 and the divisibility/order equivalence in Lemma6. Applying it with (a,b)=(4,1), none of its n>=2 exception cases applies: 4+1 is not a power of two, the negative-base case is absent, and the n=6 exceptional positive base is2. The n=1 case is checked directly by prime3. [Győry–Smyth 2010](https://math.colgate.edu/~integers/k27/k27.pdf).

Thus, for every e>=1, some odd prime p_e divides 4^e-1 and no 4^d-1 for 1<=d<e. Equivalently ord_(p_e)(4)=e. An order-e prime divides 4^d-1 precisely when e divides d. These primes are triangular separators; they are not private to one exponent among all larger exponents.

This arithmetic theorem is external mathematical ancestry, not newly proved by the finite controls or newly mechanised here. Source hypotheses and exceptions were checked rather than inferred from an analogous base.

## Finite multiplicative independence

Suppose two finite natural histograms give the same q. Subtract their exponent counts, and choose the largest e with nonzero difference. Take a prime of order e. It divides the numerator of f_e and no denominator, and divides none of the smaller-index numerators. Larger-index count differences are zero by choice. Taking its valuation in the equality therefore forces the e difference to vanish, a contradiction.

Hence the finite histogram is uniquely determined by q under this one fixed calibration, even with no known signature bound.

The choice of base is substantive. The superficially similar base2 design fails:

(1-2^(-6))(1-2^(-1)) = (1-2^(-2))²(1-2^(-3)) = 63/128.

These are different finite nonnegative histograms with the same probability. This checks an actual failure associated with the familiar base2 exception; it does not claim every missing primitive divisor automatically causes such a relation for every base.

## An effective prime-order decoder

All finite-product numerators are odd. Therefore the reduced denominator is exactly 4^H, where H=sum_e e n_e. The rational input itself supplies this weighted-size bound; every active e is at most H. It does not supply the individual counts. For example, three e=1 routes and one e=3 route have the same denominator and different numerators.

For q in (0,1], proceed as follows.

1. Require the denominator to be a power of four and compute H. The case q=1 gives the empty histogram.
2. Factor the odd numerator. For every prime divisor p, compute ord_p(4). Reject an order exceeding H before constructing a potentially huge factor.
3. Let D be the finite set of these orders. Every true active e occurs in D because one of its primitive divisors occurs in the numerator. Some candidates can be proper divisors of true exponents and need not be active.
4. Process D in descending numerical order. Choose a numerator prime p having order e. After all larger exponents have been removed, its remaining valuation equals n_e times its known positive valuation in f_e. Divide, require a nonnegative integer, and remove f_e^n_e.
5. Require residual1, exact probability reconstruction and the original denominator-weight identity.

The candidate primes need not be freshly discovered primitive divisors of the unknown model. Their computed orders provide the required finite candidate set. For q=255/256, the candidate orders are1,2,4; the decoder returns one e=4 route and zeros for1 and2. Arithmetic divisibility of support codes is not inclusion of the corresponding root-support sets.

The implementation uses exact trial division and exact modular order computation, with no probabilistic primality oracle. It is deliberately a correctness implementation, not an efficient integer-factorisation claim. An alternative total finite procedure enumerates the finitely many integer partitions of H, compares their rational products, and uses uniqueness to select the answer. Neither procedure is advertised as practical for large inputs. A subsequent factorisation-free gcd decoder has the stronger explicit-input polynomial bound proved in `GCD_DECODER.md`; the prime-order and partition methods remain independent alternatives.

The largest actual port index is bounded by floor(log2 H) when H>0. That bound is learned from the exact denominator, not supplied as an external finite signature. The data representation may already be enormous: a single route at port i has denominator 4^(2^i), with bit length 2^(i+1)+1.

## Finite observations cannot recover unrestricted unknown guards

Now allow finite absence guards as well as positive supports, still with finitely many routes. Take any finite queried list of issued subsets S1,...,Sn of the natural-number ports. The subsets may themselves be infinite and the attenuation choices may be arbitrary.

Each port receives an n-bit membership pattern. There are finitely many such patterns and infinitely many indices, so two distinct indices i,j have the same pattern. A route requiring i present and j absent is disabled in every queried profile. Add one such route to a common finite baseline; every queried endpoint distribution remains unchanged, regardless of the calibrated survival rates.

This gives a failure of every finite separating profile panel for the unrestricted unknown-index guarded class. It does not assume that queries activate only finitely many ports. The executable witness finds a collision among the first 2^n+1 indices, or among enough indices outside a supplied finite exclusion set, and tests profiles such as all indices, parity classes and residue classes. Fresh indices can therefore be chosen outside the baseline signature.

For a deterministic exact-query algorithm that stops after finitely many queries on a baseline, inspect its finite query history and choose such a pair. The augmented finite model produces the same answers, so the algorithm makes the same subsequent choices and returns the same result on both distinct inventories. Thus no such always-correct finite-stopping identification algorithm exists over the whole guarded class.

This adaptive argument is for deterministic finite stopping. Choosing a witness after observing a random seed is not a fixed-model statistical lower bound; no randomized extension is asserted without further proof. The obstruction also says nothing against known finite signatures, restricted guards, fair limiting inquiry or observing an infinite collection of profiles.

## Sampling and numerical precision

Even known route count1 does not supply a uniform finite-sample guarantee when the port index is unbounded. The one-route models at i and i+1 have effect probabilities p_i=4^(-2^i) and p_i². Their one-trial total variation distance is p_i-p_i²<p_i. After N independent trials, the distance is at most N p_i by coupling. Any fixed N eventually fails a fixed-confidence discrimination requirement as i grows.

Both examples are nonempty finite histograms. Adding the same productive baseline to alternatives gives the same kind of shrinking distinction; the negative result does not depend on an empty model. The exact-rational theorem is not a claim that these tiny probability differences can be measured exactly or cheaply.

The all-issued oracle is also an explicit mathematical idealisation: it supplies the exact response under the globally defined rate scheme on a countable port alphabet. A computable formula for rates is not a demonstration of physical control over infinitely many original agents. No approximate rational frequency may be silently substituted for q.

## Finitude is an assumption until separately certified

The finite proof uses a largest differing exponent and a finite product. Both can fail for infinitely many routes. `FINITENESS_AUDIT.md` constructs a computable infinite-route mimic of a finite rational readout and gives a separately scoped two-query positive finitude certificate. The denominator-weight identity above must not be used to infer finitude before the finite-product premise is justified.

`ORACLE_AND_EXTENSION_BOUNDARIES.md` additionally distinguishes exact rational access, Cauchy approximation and limit learning; audits real coefficients and trial mixtures; and supplies a second-order grouping control. The theorem therefore identifies a finite anonymous histogram within its declared stochastic class. It does not validate actual productive ground, original-bearer identity, source-level complete willing or the admissibility of the probes.
