# Independent root controls: coupled credal revision

11 October 2026 UTC. Additive T20 mathematics; finite exact controls and ordinary proofs, not kernel verification or a calibrated account of any actual religious evidence.

## Full-range check

For p in [1/4,3/4], keep audit mass e=1/4 and let x=P(theta=1,audit=1). A joint law in the order (11,01,10,00) is (x,e-x,p-x,1-e-p+x). All four entries remain strictly positive in both segments below.

K: x=1/8. Posterior is 1/2 and audit likelihood ratio is (1-p)/p, with full range [1/3,3].

L: x=2p/5-3/40. Posterior is 8p/5-3/10, with full range [1/10,9/10]. The likelihood ratio is (p-1)(16p-3)/(p(16p-13)). Its derivative is

3(32p^2-32p+13)/(p^2(16p-13)^2)>0.

The quadratic numerator is 32(p-1/2)^2+5; the denominator is nonzero on the admitted interval. Endpoints therefore establish the complete likelihood-ratio range, rather than merely two sampled values. Thus K and L agree on the range of the current target probability, audit probability and likelihood ratio, while yielding different revised sets. Each segment's likelihood and prior must be paired through its common joint model. The example does not establish that every rectangular model family is unjustified; it defeats a representation that replaces a specifically justified coupled family by independent choices of its summaries.

## Compactness does not guarantee an attained conditional endpoint

Consider the compact convex set D of (v,u) with 0<=v<=1/2 and v^2<=u<=v/2. Convexity follows from the epigraph of v^2 intersected with halfspaces. Map it affinely into joint laws:

P(1,1)=u; P(0,1)=v-u; P(1,0)=P(0,0)=(1-v)/2.

Audit mass is v. For every v>0 all four cells are positive, and the audit posterior is u/v in (0,1/2]. Every q in that half-open interval occurs at v=q,u=q^2. Zero cannot occur at positive audit mass because u>=v^2>0. Consequently the conditional image is exactly (0,1/2], despite compactness and convexity of the pre-audit set. Its infimum is zero, but no member attaining that infimum is an admissible positive-event conditional law. Closing the posterior set preserves infima of continuous bounded scalar queries but enlarges the model set; those meanings must be stated separately.

This sharpens the existing null-audit discontinuity control into an attained-versus-limiting credal boundary. It uses the same inherited conditioning mechanism, not a new discovery about general probability. No real report or source is assigned this model.

## Verification scope

check.py uses exact fractions and symbolic derivative checks. Explicit raise statements remain active under Python -O. It checks the full derivative sign by polynomial discriminant/leading coefficient, the endpoints, 202 strictly positive joint laws, and 1100 compact-family points. The universal claims rest on the displayed proofs. Repetition under normal and optimised Python is a runtime control, not an independent second proof.

The authoring worker supplied the K/L collision. The root independently derived the full-range derivative and the compact convex boundary example; this records that attribution without treating collaboration as external validation.
