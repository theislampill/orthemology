# Independent derivation: effective exponential-tail transport

2026-10-10 UTC. Ordinary mathematical review notes, prepared before reading the author's new proof. These notes do not alter protected or inherited sources and carry no integration, kernel, novelty, empirical, or closure authority.

## 1. Exact representation and target

The input is a probability measure μ on [0,∞), represented by uniformly computable moment names m_r=∫x^r dμ: an algorithm takes (r,p) and returns a rational within 2^(−p) of m_r. Also supplied are computable reals a>0 and M≥∫exp(ax)dμ. M is only an upper bound. It is not a name for that integral or an endpoint exponential-tail modulus.

For a computable real u promised to satisfy u>−a, write A_r(u)=∫x^r exp(−ux)dμ and Z(u)=A_0(u). The target is a uniform name for every normalized moment A_r(u)/Z(u).

## 2. Independent finite-step proof

Find rational δ,H,B with 0<δ<min(a,a+u), H>M, and B>|u|, B>0. The strict gap promise makes the first search effective without deciding the sign of u. Choose an integer N>2B/δ. Put h=u/N and v_i=ih, 0≤i≤N. Every point of the segment has a+v_i>δ.

The elementary exponential-series inequality gives, for every n≥0,

A_n(v_i) ≤ H n! δ^(−n).

Indeed x^n≤n!δ^(−n)exp(δx), and δ−v_i<a. Consequently each local series

A_r(v_i+h)=Σ_(k≥0) (−h)^k A_(r+k)(v_i)/k!

is absolutely integrable and absolutely convergent. Its omitted terms starting at k=K obey

|tail| ≤ H δ^(−r) Σ_(k≥K) ((r+k)!/k!) 2^(−k).

For K≥max(1,2r), the summand ratio is ((r+k+1)/(k+1))/2≤3/4 throughout the tail. Therefore

|tail| ≤ 4H δ^(−r) ((r+K)!/K!) 2^(−K).

This rational bound tends effectively to zero; it is enough to increase K until the requested strict bound holds. A local approximation uses finitely many uniformly named input moments, finitely many computable-real coefficients, and ordinary effective arithmetic with the displayed magnitude bounds. Induction in the finite number N supplies a uniform moment oracle at every stage. There is no appeal to abstract analytic continuation, and no requirement that the single Taylor series at zero converge at a large positive target u.

For normalization, choose a rational B_1≥max(1,m_1) and rational U≥max(0,u). Markov's inequality gives μ([0,2B_1])≥1/2, hence

Z(u)≥(1/2)exp(−2UB_1)>0.

A positive rational lower bound d_0 for the right side can be computed. Set C_r=H r!δ^(−r). If rational approximations q,z to A_r(u),Z(u) each have error at most ε≤d_0/2, then z≥d_0/2 and

|q/z−A_r(u)/Z(u)|≤2ε/d_0+2C_r ε/d_0².

Thus quotient precision is effective uniformly in r and the requested output precision. No efficiency or conditioning bound is claimed.

## 3. One computable input with a noncomputable endpoint law

Fix a standard computable bijective pairing of machine index e≥0 and time t≥0 with integers, and let j=1+pair(e,t). The predicate that machine e first halts at exactly t is decidable. Put w_e=4^(−e−1), so Σ_e w_e=1/3. Define

μ=p_0 δ_0+Σ_(e halts) w_e exp(−a j_e) δ_(j_e),

p_0=1−Σ_(e halts) w_e exp(−a j_e).

Then p_0≥2/3. All events with j≤J can be decided by finitely many finite simulations. For a rational 0<α<a, the unexamined original mass is at most (1/3)exp(−αJ). For r≥1, the unexamined r-th moment is at most

(1/3) r!(2/α)^r exp(−αJ/2).

This follows from x^r exp(−αx/2)≤r!(2/α)^r and Σw_e≤1/3. The bound is uniform in r and J. It proves that p_0 and all original moments are uniformly computable. Reassigning the unexamined mass to zero gives computable finite laws converging effectively even in total variation.

At u=−a,

Z(−a)=p_0+W, where W=Σ_(e halts)4^(−e−1), and 1≤Z(−a)≤4/3.

W is noncomputable: after removing already decoded terms below index e, the remaining value is at most w_e/3 when e does not halt and at least w_e when it does. A sufficiently accurate value therefore decides the halting set, successively. Since p_0 is computable, Z(−a) is noncomputable despite the valid supplied upper bound M=4/3.

The endpoint's atom at zero has mass p_0/Z(−a), which is noncomputable. Since zero is separated by distance at least one from every other support point, this mass is the integral of a bounded computable continuous function equal to one at zero and zero on [1,∞). Thus the endpoint probability law itself is noncomputable in the usual weak representation.

This construction proves finite endpoint normalization only. Its endpoint polynomial moments are Σw_e j_e^r/Z(−a), whose finiteness has not been established. It must not be presented as a counterexample within an endpoint-all-moments-finite class.

## 4. Author-proposed stronger family, independently checked before the artifact

The author separately proposed the following family. If machine e first halts at time t, set j=t+2 and

ν_e=(1−1/j)δ_0+(1/j)δ_j.

If it never halts, set ν_e=δ_0. Define the reverse-damped law

μ_e=exp(−ax)ν_e/D_e,

D_e=∫exp(−ax)dν_e.

In the halting case, D_e=1−1/j+exp(−aj)/j≥1/2, the positive atom of μ_e has mass exp(−aj)/(j−1+exp(−aj)), and

m_r(μ_e)≤2j^(r−1)exp(−aj), r≥1.

If a halt has not occurred through a large time cutoff, these estimates give computable, uniform input moment errors. Also

Z_e(−a)=1/D_e≤2,

0≤Z_e(−a)−1≤1/(j−1).

The latter, slower bound makes even exact Z_e uniformly computable by finite simulation. Calling this part exponential damping would be imprecise: the computability of Z_e uses the effective reciprocal-time bound.

Every endpoint ν_e has finite support and all finite moments. Nevertheless m_1(ν_e) is exactly 0 in the nonhalting case and 1 in the halting case. A uniform algorithm for the endpoint first moment would decide halting by requesting error below 1/4. This is a genuine obstruction to a uniform endpoint-moment operator even under the all-moments-finite promise and with a name for Z_e supplied.

The quantifiers matter. Each endpoint measure and each of its moments is individually computable; the obstruction is to uniform extraction of their moments from the provided inputs. In fact the endpoint laws ν_e are uniformly computable even in total variation, since a late positive atom has mass 1/j. This is compatible with failure of uniform unbounded-moment integration.

## 5. Endpoint law versus endpoint moments

Once μ is available as a computable probability law, a supplied computable value Z(−a) is sufficient to compute the normalized endpoint law. Choose increasing computable continuous compactly supported cutoffs ψ_n↑1. The integrals I_n=∫exp(ax)ψ_n(x)dμ are computable and increase to Z(−a). Using the supplied name for Z, search for n with Z−I_n below the requested error; strict inequalities of computable reals are semidecidable and convergence ensures termination. This supplies an effective weighted tail bound for bounded-observable integration.

Conversely, if the endpoint law ν is computable, the bounded computable function exp(−ax) has computable ν-integral equal to 1/Z(−a). Its strict positivity makes inversion effective. Thus, for the fixed input under discussion, endpoint-law computability and Z(−a) computability are equivalent. This does not compute unbounded endpoint moments without additional effective integrability information.

The new artifact must explicitly justify obtaining the input law μ from its moments and tail certificate if it uses this equivalence. One valid route is: the interior algorithm computes Z(n) uniformly for integers n; these are the moments of the pushforward by y=exp(−x) on [0,1]; effective Bernstein approximation computes that compact law; inversion on (0,1] is effective after a tightness search, or by the original exponential-tail bound.

## 6. Inherited scope

The directly read predecessor `measure-moment-continuation-boundary-20261009/RESULT.md` §§2,3,6 distinguishes law determination from effective reconstruction and gives the half-line normalized tilt, compact moment determination, and the sufficient positive-exponential-moment determinacy condition. The present derivation adds an explicit algorithm and its endpoint representation boundary for that declared numerical interface. It does not reattribute classical determinacy or the inherited actual-update congruence requirement.

## 7. Update after reading the author's actual proof

The author's E3 supplies a valid argument stronger than the deliberately conservative restriction in §3 above: every positive endpoint moment in that example is infinite. If only finitely many halting indices e had halting time t_e>4^(e+1), simulation up to that computable bound together with a finite hard-coded list of exceptions would decide the diagonal halting set. Therefore infinitely many do. For each of them j_e≥t_e and w_e j_e^r>1 for every r≥1. The corresponding positive-term series diverges. This independently checked divergence proof replaces uncertainty about the endpoint's moment class; it does not move E3 into the finite-moment class.

The author's E4 was communicated by the author and a participating checker, then independently checked here. Its construction should not be described as independently discovered by this reviewer. The independent work is the validation of its uniform input algorithms, the exact normalization bounds, and its reduction from a hypothetical uniform endpoint-mean operator to halting.

The full author draft, the capped tensor predecessor §8, and Hoyrup–Rojas §4.3 were subsequently inspected directly. The primary source supports the bounded-integration/weak-measure representation ancestry: Proposition 4.3.1 and Corollary 4.3.1 give integration characterizations, and the following bounded-function corollary gives uniform computable integration with supplied uniform bounds. The new algorithm and endpoint reductions are checked from their displayed proofs, rather than attributed to that source. Source: https://members.loria.fr/MHoyrup/random_metric.pdf, printed pp. 13–14.
