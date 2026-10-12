# Signed-energy continuation: independent proof-route check

Date: 2026-10-10 (UTC)

## Scope and conclusion

This is an independent participating check of the proposed proof route, not a
digest-bound assessment of a completed author artifact. No author artifact was
inspected or edited.

The claimed moment-uniqueness theorem is correct under the stated hypotheses.
No bound on the energy at positive times, and no positive-time joint representing
measure, needs to be assumed. The proposed argument works with the quantitative
and boundary details below. The only external existence theorem needed is the
one-dimensional Hamburger moment theorem.

Write \(\mathcal P=\mathbb R[x_1,\ldots,x_d]\). Assume \(L_t\) is a real linear
functional on \(\mathcal P\), \(L_t(1)=1\), \(L_t(p^2)\geq0\), each coordinate
\(t\mapsto L_t(p)\) is \(C^1\) on \([0,T)\), and
\[
L_t'(p)=-L_t(hp)+L_t(h)L_t(p).
\]
Assume \(L_0(p)=\int p\,d\mu\), with all absolute polynomial moments and
\(|h|\leq M\), \(\mu\)-almost surely. Then necessarily
\[
L_t(p)=\frac{\int p e^{-th}\,d\mu}{\int e^{-th}\,d\mu}.
\]

## 1. Linearization and smoothness

Set
\[
c(t)=\exp\!\left(-\int_0^t L_v(h)\,dv\right),\qquad A_t=c(t)L_t.
\]
Then \(c(t)>0\), \(A_t(1)=c(t)\), \(A_0=L_0\), square positivity is preserved,
and \(A_t'(p)=-A_t(hp)\). Bootstrapping this identity simultaneously for all
polynomials gives
\[
\frac{d^n}{dt^n}A_t(p)=(-1)^n A_t(h^np)
\]
and coordinatewise \(C^\infty\) regularity in the interior.

Fix a real polynomial \(q\), and abbreviate
\[
f(t)=A_t(q^2),\qquad m_n(t)=A_t(q^2h^n)=(-1)^n f^{(n)}(t).
\]
The functional \(r\mapsto A_t(q^2r(h))\) on \(\mathbb R[z]\) is square-positive,
so \(m_{2n}(t)\geq0\).

## 2. Uniform factorial bounds and scalar measures

Choose \(0<a<b<T\) and \(r>0\) such that \([a-r,b+r]\subset(0,T)\). Put
\[
C=\max_{v\in[a-r,b+r]}f(v)<\infty.
\]
For \(t\in[a,b]\), Taylor expansion through degree \(2n+1\), with integral
remainder involving \(f^{(2n+2)}\geq0\), is a lower bound at both \(t+r\) and
\(t-r\). Adding the expansions cancels odd terms, and every even term is
nonnegative. Consequently
\[
0\leq m_{2n}(t)\leq \frac{f(t+r)+f(t-r)}2\frac{(2n)!}{r^{2n}}
\leq C\frac{(2n)!}{r^{2n}}.
\]
The expansion must go through degree \(2n+1\); merely writing a remainder of
order \(2n\) does not directly bound the derivative at its center.

Cauchy--Schwarz for the positive scalar functional gives
\[
|m_{2n+1}(t)|^2\leq m_{2n}(t)m_{2n+2}(t).
\]
Thus, for every integer \(k\geq0\), uniformly on \([a,b]\),
\[
|f^{(k)}(t)|=|m_k(t)|\leq\sqrt2 C\,k!r^{-k}.
\]
For odd \(k\), the precise extra factorial factor is
\(\sqrt{(k+1)/k}\leq\sqrt2\). Taylor's remainder now proves real analyticity
locally, without inferring analyticity just from pointwise bounds.

Hamburger's theorem gives a finite positive measure \(\sigma_t\) with moments
\(m_n(t)\). For every \(0<\alpha<r\), monotone convergence of the nonnegative
cosh series gives
\[
\int e^{\alpha|z|}\,d\sigma_t
\leq2\int\cosh(\alpha z)\,d\sigma_t
\leq\frac{2C}{1-(\alpha/r)^2}.
\]
Every other representing measure obeys the same bound, because it has the same
even moments. Exponential integrability makes the moment problem determinate:
the moments determine the analytic Fourier transform near zero, then throughout
its connected strip, and Fourier uniqueness determines the measure.

## 3. Local transitions and patching

Fix an interior \(u\), and take the above uniform bounds in a neighborhood of
\(u\). For sufficiently small \(\delta\), the analytic function
\[
g(\delta)=\int e^{-\delta z}\,d\sigma_u
\]
has Taylor coefficients \((-1)^nm_n(u)/n!\), exactly those of \(f(u+\delta)\).
Hence these functions agree locally. Differentiating their analytic identity
shows, for every \(n\geq0\),
\[
m_n(u+\delta)=\int z^ne^{-\delta z}\,d\sigma_u.
\]
Differentiation under the integral is justified by exponential integrability,
using a strictly smaller neighborhood than the available exponential radius.
Determinacy therefore gives
\[
\sigma_{u+\delta}=e^{-\delta z}\sigma_u.
\]
On any compact interval in \((0,T)\), a common positive radius follows from the
uniform bounds above. Finite subdivision and composition yield
\[
\sigma_v=e^{-(v-u)z}\sigma_u\qquad(u,v\in(0,T)).
\]
This step does not presuppose a global exponential-moment radius: finite
integrability at each successive endpoint follows from the established local
measure equality.

## 4. Recovery at the initial boundary

Fix \(s\in(0,T)\). For \(0<u\leq s\),
\[
\sigma_u=e^{(s-u)z}\sigma_s.
\]
Define initially a possibly infinite measure \(\sigma_*=e^{sz}\sigma_s\).
For each \(n\geq0\), split the even moment integral into \(z\geq0\) and
\(z<0\). As \(u\downarrow0\), the first integrand
\(z^{2n}e^{(s-u)z}\) increases, so monotone convergence applies. On \(z<0\),
it is bounded by \(|z|^{2n}\), which is integrable against \(\sigma_s\).
Dominated convergence therefore applies there. Since
\(m_{2n}(u)\to m_{2n}(0)<\infty\), it follows that
\[
\int z^{2n}\,d\sigma_*=m_{2n}(0).
\]
The case \(n=0\) proves finiteness of \(\sigma_*\). For every odd power, the
positive half is dominated by its limiting exponential-weighted absolute
integrand, which is integrable by the already established even moments. The
negative half is dominated by the corresponding absolute polynomial moment of
\(\sigma_s\). Thus
\[
\int z^n\,d\sigma_*=m_n(0)\qquad(n\geq0).
\]

The known measure \(\tau_q=h_*(q^2\mu)\) has precisely these moments and is
supported in \([-M,M]\). Compact support makes its Hamburger moment sequence
determinate. Explicitly, for \(R>M\),
\[
\sigma_*(|z|\geq R)
\leq R^{-2n}m_{2n}(0)
\leq \left(\frac MR\right)^{2n}\int q^2\,d\mu,
\]
so \(\sigma_*\) also has that compact support; polynomial approximation then
gives \(\sigma_*=\tau_q\). This argument includes \(M=0\). Consequently
\[
\sigma_s=e^{-sz}\tau_q,\qquad
A_s(q^2)=\int q^2e^{-sh}\,d\mu.
\]

## 5. Zero mass, polarization, and the precise conclusion

Zero scalar mass causes no division issue. If \(m_0(t)=0\), scalar
Cauchy--Schwarz gives \(|m_n(t)|^2\leq m_0(t)m_{2n}(t)=0\); the unique scalar
measure is the zero measure. All transitions and boundary arguments remain
valid. In particular, \(\int q^2\,d\mu=0\) forces zero scalar measure at all
times; no branch can emerge from a null initial square.

Use \(p=((p+1)^2-(p-1)^2)/4\) to recover
\(A_t(p)=\int p e^{-th}\,d\mu\) for every polynomial. Taking \(p=1\) identifies
\(c(t)=\int e^{-th}\,d\mu>0\), proving the claimed normalized formula.

The conclusion determines the polynomial functional and constructs a genuine
positive-time representing law. It does not in general uniquely determine that
law. For example, in dimension two take \(h(x,y)=x\) and
\(\mu=\delta_0\otimes\nu\), with \(\nu\) lognormal and moment-indeterminate.
Different moment-equivalent choices of \(\nu\) give the same stationary
polynomial functional and bounded energy. Compact support of \(\mu\) does imply
joint law uniqueness. Bounded energy also implies compact support when
\(\{|h|\leq M\}\) is compact, including nonconstant univariate polynomial
\(h\); thus the lack of law uniqueness is a general possibility, not a claim
about every bounded-energy example.

## Narrow reference check

The standard one-dimensional existence theorem and the elementary analytic
moment-determinacy criterion were cross-checked against Djalil Chafai's
[moment-problem notes, Theorems 1 and 3](https://djalil.chafai.net/blog/2010/06/28/some-few-moments-with-the-problem-of-moments/).
The quantitative continuation and boundary arguments above were checked
directly; they are not a literature-based assertion of the proposed theorem.

## Supplementary route check: 2026-10-10, 22:20 UTC

This supplement checks the proposed determinacy extension and converse. It
remains a participating proof-route check, not a review of an author artifact.

### A. Weighted initial energy determinacy replaces bounded energy

Replace the initial bounded-energy hypothesis by:
\[
\text{For every real polynomial }q,\quad
\tau_q=h_*(q^2\mu)\text{ is Hamburger moment-determinate.}
\tag{D}
\]
All other original hypotheses remain in force. The theorem continues to hold
on the supplied solution horizon \([0,T)\). More precisely, the existence of
the asserted normalized square-positive hierarchy forces, for every
\(t\in[0,T)\) and every polynomial \(q\),
\[
\int q^2e^{-th}\,d\mu<\infty,
\qquad
A_t(q^2)=\int q^2e^{-th}\,d\mu,
\]
and hence forces the same normalized tilt formula for every polynomial.

Reason: Sections 1--4 up to the identification of \(\sigma_*\) never use
boundedness of \(h\) initially. They construct a finite positive measure
\(\sigma_*\) having exactly the moments of \(\tau_q\). Hypothesis (D) identifies
those measures directly. Inverting the strictly positive multiplier gives
\(\sigma_t=e^{-tz}\tau_q\); its finite mass supplies the required integrability.
The remaining polarization and normalization arguments are unchanged. Zero
initial scalar mass is again included, since the zero measure is determinate.

This is a uniqueness-and-necessary-integrability assertion conditional on a
hierarchy being supplied on its stated horizon. It does not assert global
existence, or existence on an arbitrary prescribed horizon. No boundedness of
positive-time energy is needed.

### B. An initial absolute exponential energy moment suffices

If, for some \(a>0\),
\[
\int e^{a|h|}\,d\mu<\infty,
\]
then, for every polynomial \(q\), Cauchy--Schwarz gives
\[
\int e^{(a/2)|z|}\,d\tau_q(z)
=\int q^2e^{(a/2)|h|}\,d\mu
\leq
\left(\int q^4\,d\mu\right)^{1/2}
\left(\int e^{a|h|}\,d\mu\right)^{1/2}<\infty.
\]
Thus each \(\tau_q\) is determinate by the same exponential-moment criterion.
This sufficient condition supplies (D), not an unrestricted forward-time
integrability assertion.

There is nevertheless automatic local existence: for every \(t<a\), choose
an integer \(k>1\) with \(tk/(k-1)<a\), and apply Holder to
\(|q|^2\) and \(e^{t|h|}\). All polynomial moments and the exponential bound
give \(\int q^2e^{-th}\,d\mu<\infty\). Therefore the converse below constructs
the hierarchy on \([0,a)\). It need not extend globally or include its eventual
right endpoint.

### C. Converse and the initial one-sided derivative

For any genuine initial probability law with all absolute polynomial moments,
assume
\[
\int q^2e^{-th}\,d\mu<\infty
\quad\text{for all real polynomials }q\text{ and every }t\in[0,T).
\tag{I}
\]
Define \(B_t(p)=\int pe^{-th}\,d\mu\), \(Z_t=B_t(1)>0\), and
\(L_t(p)=B_t(p)/Z_t\). Then this is a normalized square-positive hierarchy
with the required differential equation. This existence direction does not
require (D).

To justify differentiation, first note that for any polynomial \(P\) and any
allowed time \(v\), (I) and Cauchy--Schwarz imply
\[
\int |P|e^{-vh}\,d\mu
\leq\left(\int P^2e^{-vh}\,d\mu\right)^{1/2}Z_v^{1/2}<\infty.
\]
At an interior time choose neighboring allowed times \(u<v\). For
\(t\in[u,v]\),
\[
|h^kp|e^{-th}\leq |h^kp|(e^{-uh}+e^{-vh}),
\]
whose right side is integrable. At the initial endpoint, choose
\(0<\varepsilon<T\); for \(0\leq t\leq\varepsilon\), use instead
\[
|h^kp|e^{-th}\leq |h^kp|(1+e^{-\varepsilon h}).
\]
Both terms are integrable by the same argument. Dominated differentiation and
continuity therefore give \(B_t^{(k)}(p)=(-1)^kB_t(h^kp)\), with right
derivatives at zero. In particular the family is coordinatewise \(C^1\) on
\([0,T)\), and differentiating the quotient gives the stated normalized ODE.

### D. Gaussian controls and finite-time obstruction

Take \(\mu=N(0,1)\) on \(\mathbb R\).

* For \(h(x)=x\), completing the square gives
  \(Z_t=e^{t^2/2}\) and \(\mu_t=N(-t,1)\). All weighted polynomial moments
  are finite for every finite \(t\), so the hierarchy exists for all
  \(t\geq0\).
* For \(h(x)=-x^2\), the initial exponential-energy sufficient condition holds
  for every \(0<a<1/2\). For \(0\leq t<1/2\),
  \[
  Z_t=(1-2t)^{-1/2},\qquad
  \mu_t=N\!\left(0,(1-2t)^{-1}\right),\qquad
  L_t(x^2)=(1-2t)^{-1}.
  \]
  At \(t=1/2\), even \(Z_t\) is infinite. Any supplied hierarchy on a horizon
  containing that time would contradict the necessary integrability from A.
  Moreover, its forced second moment diverges as \(t\uparrow1/2\), so even a
  coordinatewise continuous finite-valued extension through that time is
  impossible. The open horizon \([0,1/2)\) is valid.

No gap was found in these extensions. Their essential qualification is that
the determinacy hypothesis forces the tilt only wherever a hierarchy exists;
the Gaussian negative-quadratic control rules out a general global-existence
claim.
