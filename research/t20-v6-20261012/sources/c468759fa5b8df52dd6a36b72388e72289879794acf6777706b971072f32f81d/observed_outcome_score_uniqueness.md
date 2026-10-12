# A positive conditional score-fixing theorem

This is a refinement of the accuracy-bridge analysis, not a new source-ascent argument. It supplies an independently intelligible extra restriction that can fix a comparison rule, rather than presuming that all admissibility classes must remain plural.

## Statement and proof

Let there be m≥3 categorical outcomes. Reports q and true distributions p range over the **relative interior of the full probability simplex**. A reward score is observed-outcome-local if `S(q,i)=f_i(q_i)`, with each f_i differentiable on (0,1). Assume strict propriety: for every p, expected score under that fixed p is uniquely maximized by q=p.

**Theorem A4.** Exactly such scores have the form `S(q,i)=c log(q_i)+d_i`, with common c>0 and arbitrary outcome constants d_i. This is the maximizing-reward convention; the corresponding minimizing-loss form is `d_i−c log(q_i)`.

**Proof.** At the relative-interior constrained maximum q=p, first-order conditions give `p_i f_i′(p_i)=p_j f_j′(p_j)` for all i,j. For any x,x′∈(0,1), choose a distinct coordinate j and a positive y smaller than both 1−x and 1−x′. The third or remaining coordinates absorb the positive remainder. Thus `x f_i′(x)=y f_j′(y)=x′f_i′(x′)`. Each function t f_i′(t) is constant, and the constants agree across i. Integration yields f_i(t)=c log(t)+d_i. If c=0 there is no strict optimum; if c<0 p is not a maximum. For c>0, the expected advantage of p over q is c times KL(p||q), strictly positive for q≠p. This follows from the strict logarithmic Jensen inequality, with equality only at p=q. ∎

This classical result is stated in loss-sign convention in Dawid, Lauritzen and Parry's discrete scoring paper, §3.2. Their more general neighbourhood-locality theories should not be collapsed into this realized-coordinate condition. [Primary source](https://www.stats.ox.ac.uk/~steffen/papers/AOS972.pdf)

The theorem fixes rankings among reports at a fixed realized outcome, and expected rankings under a fixed p, up to harmless positive scale and outcome-only constants. It does not fix the numerical units, the constants, the true p, or the report-independent outcome law. It also does not derive probabilistic coherence: its domain already consists of coherent probability distributions. A1–A2 in the main note address a different conditional bridge from unconstrained credence vectors to coherence.

## Why the extra premise has content

A defender can motivate observed-outcome locality by saying the observed outcome supplies the verification event, so its assigned probability should determine the report's score without independent penalties on unrealized alternatives. The resulting log rule aligns with likelihood comparison and information-sensitive assessment.

A rival can reject that evaluative premise without rejecting truth aim. When outcomes have meaningful distance or structure, the distribution assigned to unrealized nearby and distant possibilities may matter to forecast quality. The ordinary multicategory Brier reward `2q_i−Σ_jq_j²` is strictly proper yet depends on the other coordinates. Holding the realized-outcome probability at 1/2, reports (1/2,1/4,1/4) and (1/2,49/100,1/100) receive respectively 5/8 and 2549/5000. Locality forbids that distinction; it does not prove it normatively irrelevant merely by naming the score “truth-directed.”

The relation to Orthemology is conditional and useful: if the application independently warrants this locality property and the other premises, the admissible score class collapses to a comparison-equivalent family. P15's disclosure should then report determination, not insist on disagreement. Establishing the premises carries the substantive warrant.

## Deletion controls

1. **Binary exception.** With two outcomes, the other probability is determined by the realized one. The strictly proper binary Brier reward can be written `f(q_i)=−2(1−q_i)²`; this is local but not logarithmic. Thus m≥3 is essential to the stated uniqueness route. The symmetric quadratic/quartic reversal in the main note survives binary observed-outcome locality.
2. **Locality deleted.** Multicategory Brier is strictly proper and differentiable, yet is not logarithmic. The quoted pair displays its nonlocality exactly.
3. **Strict propriety deleted.** A constant reward is local and weakly proper but cannot elicit a unique report. Merely scoring assigned probability linearly is local and symmetric, but rewards a mode-seeking report rather than generally eliciting p.
4. **Full simplex deleted.** Stationarity over a restricted report family need not connect arbitrary coordinate values; the proof no longer licenses the global logarithmic form. A separate restricted-domain theorem would be required.
5. **Fixed law deleted.** If the report changes the distribution of the outcome, the expected-score comparison used in propriety changes. The main note's report-dependent Bernoulli example applies.
6. **Boundary changed.** The theorem is stated on the relative interior. Extending log scores to zero probabilities may require infinite penalties or support conventions. No finite continuous closed-simplex extension is silently assumed.

A concrete dimensional deletion is instructive. Extending the binary local Brier formula unchanged to three outcomes fails propriety. At p=(1/2,3/10,1/5), change the report to q=(51/100,3/10,19/100). Its expected reward increases by 173/50000, even though q≠p. The binary exception is therefore structural rather than an unexamined technical caveat.

## Keep the two meanings of locality separate

Observed-outcome scoring locality restricts which coordinates a numerical score uses. Constitutive bearer-locality concerns the entity in which an attribute or thought token inheres. They are different predicates over different domains. The logarithmic-score theorem supplies no inference from one to the other, no thinker at the ultimate ground, and no norm-authoring source. Any such bridge still needs a separately defended ontological relation.
