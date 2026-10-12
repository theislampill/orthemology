# Participating proof: all admissible moment-hierarchy solutions

10 October 2026 UTC. Proposed and developed by the root in dialogue with the author; not independent review or kernel certification.

Let T>0, m_0=1, and every m_r be continuously differentiable on [0,T), with right derivatives at zero, satisfying m'_r=-m_(r+1)+m_1 m_r. Assume each time's sequence is realized by a probability law on [0,infinity) with all finite moments. Define a_0(t)=exp(-integral_0^t m_1(s)ds) and a_r=a_0 m_r. Then a'_r=-a_(r+1), every a_r is nonnegative, and bootstrapping gives all finite derivative orders.

Backward Taylor expansion with nonnegative integral remainder gives, for 0<b<t and each finite N,

sum_(n=0)^N a_(r+n)(t)b^n/n! <= a_r(t-b).

In particular a_n(t)<=n! a_0(t-b)/b^n. Neighbourhood-uniform versions give factorial derivative estimates and real analyticity of every a_r on (0,T). This is interior analyticity, not analyticity at the initial boundary.

Fix s in (0,T) and a representing finite measure lambda_s with mass a_0(s) and moments a_r(s). Monotone convergence of the positive exponential series gives integral exp(bx) d lambda_s <= a_0(s-b) for every b<s. Consequently g(u)=integral exp(-(u-s)x) d lambda_s is real analytic for all u>0. Its derivatives at s equal those of a_0, so local analytic uniqueness and the identity theorem give g=a_0 throughout (0,T). Differentiation gives a_r(u)=integral x^r exp(-(u-s)x) d lambda_s.

As u decreases to zero, monotone convergence and continuity of each a_r give integral x^r exp(sx) d lambda_s=m_r(0), including total mass1 at r=0. Thus mu=exp(sx)lambda_s is a representing initial probability and m_r(u)=integral x^r exp(-ux)dmu / integral exp(-ux)dmu. The entire admissible trajectory comes from an actual initial law. Positive-time exponential determinacy and invertibility of weighting make that initial law unique for the trajectory. Conversely every initial representing law generates such a trajectory. Hence the solution set is in bijection with the initial moment fibre; initial determinacy exactly characterises unique admissible continuation. No Banach-space Lipschitz theorem or uniform growth norm is assumed.

The proof in fact appears to require only nonnegative coordinates everywhere and moment realizability at one positive time. This strengthening requires separate careful review; the original all-times-realizable statement remains the natural source-state contract.

Countercontrols: L(t)=1-epsilon exp(-1/t), with its smooth extension L(0)=1 and 0<epsilon<1, yields m_r=(-1)^r L^(r)/L solving the unguarded hierarchy from the delta0 initial sequence. But m_2<0 for small t>0, so it is not admissible. The nonnegative hierarchy m_1=1/(T-t), m_r=0 for r>=2 has impossible moment inequality m_1^2<=m_2; its initial sequence is ALSO invalid, so it cannot establish independent necessity of all-time realizability when valid initial data is separately assumed.

This is a project-relative classification strengthening of the inherited lognormal nonuniqueness example and the new determinate-moment computability theorem. Classical Taylor, analytic uniqueness and Laplace determinacy mechanisms remain credited ancestry. No cognitive, metaphysical, empirical, field-priority or implementation claim follows.
