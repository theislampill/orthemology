# Sampling law and KL orientation matter

Separate reviewer corollary, 10 October 2026 UTC. Suggested by the parent after the author packet was frozen and independently checked here. This is an elementary consequence, not a novelty, integration or closure claim.

Under the reviewed theorem, let p>0, q=Π_C(p), V(p)=D(q||p), a_y=α_y(p), and b_y=α_y(q). Positivity of the channel makes both outcome laws strictly positive even when q has zeros. The author's value identity is

    V(B_y p)=V(p)+log(a_y/b_y).

Therefore

    Σ_y a_y V(B_y p)=V(p)+D(a||b),
    Σ_y b_y V(B_y p)=V(p)−D(b||a).

The first expected change is nonnegative and the second is nonpositive; each is strict exactly when a≠b. These are different declared sampling laws. Commutation alone does not license an unqualified claim that evidence lowers expected reverse-KL repair cost. Because each V(B_y p)≥0, the second formula also implies D(b||a)≤V(p), consistent with data processing.

The second identity can alternatively be read from the ordinary joint-law KL chain rule applied to q_i K(y|i) versus p_i K(y|i), with commutation identifying B_y q as the repaired posterior. This observation neither requires choosing which law is true nor makes the repair normatively warranted.

For the opposite orientation, when D(p||q) is finite,

    Σ_y a_y D(B_y p || B_y q)=D(p||q)−D(a||b).

This last identity is the classical forward joint-law KL chain rule; it does not itself need the commutation theorem. Commutation lets one replace B_y q by Π_C(B_y p). With p strictly positive, its finite form requires q strictly positive. Boundary repairs or omitted blocks can make D(p||q)=+∞, so subtracting infinities or claiming a finite reduction there is invalid. The reverse-oriented V identities above remain finite under this packet's hypotheses.

Exact control: the fresh seven-state review example has

    a=(7/18,1/3,5/18),
    b=(2513/5444,1745/5444,593/2722).

They differ, giving strictly positive original-law drift and strictly negative repaired-law drift. Group 8 of `verify_review.py` checks both identities by exact logarithmic arithmetic. It separately checks the finite forward identity on the author's positive five-state curved example. No empirical learning, score, source-truth, proper-function, or warrant claim follows.
