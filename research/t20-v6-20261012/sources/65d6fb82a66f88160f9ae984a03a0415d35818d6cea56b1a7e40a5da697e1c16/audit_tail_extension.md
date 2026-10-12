## 15. Source audits also consume a tail-validity budget

A flow can preserve a useful tail class while a later source revision leaves that class. This is an additional interface to the full-law, exponential-tail, determinacy and effectivity fronts. It is not captured by posterior error or coordinate error alone.

### Theorem L: an audit-and-transport envelope transfer

Let \(\mu\) be an origin law and let \(\Psi\ge0\) be an origin envelope satisfying

\[
\int e^{\beta\Psi(a)}\,d\mu(a)\le M<\infty.
\]

Suppose a nonnegative audit factor has positive finite normaliser \(Z_R\), and

\[
R(a)\le C e^{\gamma\Psi(a)},\qquad C>0,\quad\gamma\ge0.
\]

Let \(q_t\) be a retained transport, and suppose its output envelope obeys

\[
\Omega(q_t(a))\le A_t\Psi(a)+B_t,
\qquad A_t,B_t\ge0.
\]

Then, whenever \(\eta\ge0\) and \(\eta A_t+\gamma\le\beta\),

\[
\boxed{\int e^{\eta\Omega(y)}\,d[(q_t)_\#B_R\mu](y)
\le\frac{C e^{\eta B_t}M}{Z_R}.}
\]

**Proof.** Pull the integral back to origins, insert the audit density, and use the two pointwise bounds:

\[
\frac1{Z_R}\int e^{\eta\Omega(q_t(a))}R(a)\,d\mu(a)
\le\frac{C e^{\eta B_t}}{Z_R}
\int e^{(\eta A_t+\gamma)\Psi(a)}\,d\mu(a)
\le\frac{C e^{\eta B_t}M}{Z_R}.
\]

The last inequality uses \(\Psi\ge0\) and the available exponent budget. ∎

If \(A_t>0\), an output exponent up to \((\beta-\gamma)/A_t\) remains available. If \(A_t=0\), the output envelope is bounded by \(B_t\), so any finite output exponent is allowed. A useful strictly positive output exponent requires the appropriate strict budget margin unless the transport has that bounded-output property.

The bound can also include an accumulated corrective reweighting factor: multiply it into \(R\) and account for its own upper envelope. A nonnegative damping potential may give an accumulated factor bounded by one; an amplifying factor requires a positive growth allowance.

### Composing several additions and removals

If the declared positive source factors satisfy

\[
|\log L_j(a)|\le b_j+\gamma_j\Psi(a),
\]

then the audit word \(R=\prod_jL_j^{\sigma_j}\) has an upper envelope with

\[
C=\exp\!\left(\sum_j|\sigma_j|b_j\right),\qquad
\gamma=\sum_j|\sigma_j|\gamma_j.
\]

This supplies a compositional source-revision budget. It does not assert that actual sources satisfy such bounds, nor that arbitrary source reports factor independently. The likelihood and factorisation models still need their own warrant.

To turn existence of a bound into an effective numerical guard, retain usable bounds on its constants and, where required, a positive lower bound on \(Z_R\). A bare assertion that all these quantities exist does not supply an effective modulus.

This transfer lemma preserves the **specific envelope hypothesis** fed into another theorem. It does not assert that every envelope, for every exponent or domain, has the same moment-determinacy or recovery consequences. Apply the precise existing T20 theorem whose hypotheses have actually been retained.

### A fully explicit loss-of-tail-class example

Let origins be integers \(n\ge0\), with prior

\[
\mu(n)=\frac{1}{C_0(n+1)^2},\qquad
C_0=\sum_{n=0}^{\infty}\frac1{(n+1)^2}<\infty.
\]

This is a genuine probability law, but it has no positive exponential moment: for every \(\beta>0\), the terms \(e^{\beta n}/(n+1)^2\) do not even tend to zero.

Take the valid discrete-report likelihood

\[
L(n)=\frac{(n+1)^2}{4^n}.
\]

It lies in \((0,1]\), since \(n+1\le2^n\) for all integers \(n\ge0\). Its posterior is proportional to \(4^{-n}\), and therefore has exponential moments for every \(\beta<\log4\).

Removing that source exactly restores the original, proper heavy-tailed law. Probability realisability survives; the exponential-tail guard does not. No coordinate-positivity failure, arithmetic error or disappearance of the true prior is required.

The operational lesson is positive and specific: **retain or recompute the tail certificate when a source revision changes the weighting**. A current law may remain entirely legitimate while no longer belonging to the class in which a particular effective recovery or gradient-preservation theorem was established.

