# Candidate channel-natural repair classification: root derivation

2026-10-09T22:19 UTC. Ordinary proof proposed for independent checking, not a final review or field-novelty claim. The classical Fisher/Chentsov ancestry is to be attributed by the research author. No source-reading credit is claimed by this derivation.

## Coherent simplex family

For every n >= 2 let f_n be C2 and strictly convex on the open categorical simplex. Suppose its Bregman divergence contracts under every column-stochastic K:n->m with no zero output row. The already proved Hessian discriminator yields h_m(Kp)[Ku] <= h_n(p)[u] on sum-zero tangents. A stochastic split E with deterministic coarsening R and RE=I consequently gives equality, as do permutations.

At the uniform point, permutation invariance makes the quadratic form h_n equal to c_n times the Euclidean tangent norm. One elementary justification extends the form by the projection P=I-11^T/n to all of R^n. The representing symmetric matrix has constant diagonal and constant off-diagonal entries, so on sum-zero vectors it is scalar. Convexity gives c_n >= 0.

Splitting each of n cells uniformly into k cells yields
c_n ||u||^2 = c_nk ||u||^2/k.
Comparing n and m through nm therefore gives c_n/n = c_m/m = c >= 0.

For rational p_i=k_i/N with positive integers k_i, split cell i into k_i equal subcells. Ep is uniform on N cells and Eu has k_i entries u_i/k_i. Thus
h_n(p)[u] = c_N sum_i u_i^2/k_i = c sum_i u_i^2/p_i.
C2 continuity extends this identity to every interior p. Polarisation gives the full bilinear Hessian. Since negative Shannon entropy has precisely that tangent Hessian, f_n-c sum_i p_i log p_i is affine on the simplex. If c were zero, each f_n would be affine, contradicting strict convexity. Hence c>0. Ordinary log-sum/data processing supplies the converse contraction.

This uses a family across arbitrary finite dimensions and reversible refinements. It is not inferred from Bayesian normalization repair alone. In fixed binary dimension, squared Euclidean distance contracts under every binary stochastic channel: writing K columns (a,1-a),(b,1-b), the tangent displacement is scaled by a-b with |a-b|<=1. Thus that restricted hypothesis does not force logarithmic scoring.

## Positive-cone family with normalization repair

The established normalization-repair classification gives
F_n(sp)=s f_n(p)+a_n(s),
with D_Fn(sp,tq)=s D_fn(p,q)+D_an(s,t).
If full-cone divergence also contracts under all such K, proportional inputs sp,tp show D_am(s,t)<=D_an(s,t) for every dimension pair. Reversing the pair using another positive stochastic map gives equality. Therefore all a_n differ by affine functions and share one radial Bregman divergence D_a. Conversely, any common C2 strictly convex a and c>0 give the contracting family
D_Fn(sp,tq)=s c KL(p||q)+D_a(s,t).
Up to ambient affine terms, F_n(b)=c sum_i b_i log(b_i/s)+a(s), s=sum_i b_i.

Normalized-only contraction leaves a_n unconstrained. Full-cone contraction fixes only cross-dimensional agreement of radial divergence, not its shape. Strict convexity does not ensure a''>0 at every point; a Riemannian positive-definite cone metric additionally needs a''>0. The coherent tangent metric is already c times Fisher.

If the cone potential is additionally coordinate-additive, mixed derivatives for i != j vanish. The displayed form gives mixed derivative a''(s)-c/s, forcing a''(s)=c/s and hence a(s)=c s log s plus affine terms. Only with this extra premise does the full cone divergence become c times unnormalised KL. Without it, a quadratic radial potential gives a valid countercontrol.

## Semantic limits

A transported-reference quadratic family carries extra data (mu -> K mu); it is not the anonymous family indexed only by outcome count used above. Its previously proved contraction is therefore unaffected. These are exact representational/geometry hypotheses, not proof of psychological identification, epistemic warrant, a justified prior, unique metaphysical norm, or actual source authority.
