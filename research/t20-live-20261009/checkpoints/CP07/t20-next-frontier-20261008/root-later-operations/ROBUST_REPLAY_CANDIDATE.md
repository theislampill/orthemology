# Prospective four-coordinate robust replay certificate

2026-10-08 16:18 UTC. Candidate sent to the finite-panel author for adversarial verification in a new sibling. Excluded from sixth intermediate checkpoint; not a reviewed theorem.

Goal: turn the exact four-probability count certificate into a positive neighbourhood excluding all wrong finite counts, without imposing an upper bound on count. This is conditional on shared marginal calibrations, independent route pairs, calibrated/selectable reference commands, and genuine unchanged-threshold replay.

For larger alternative count m, face probabilities A,B force p=A^(1/m), q=B^(1/m); put s=p+q-1. Product expansion yields J >= F_m=s^m+(1-Q)s^(m-1). Near the reference with s in (0,1), partial derivatives in A,B are bounded by 2/A_min,2/B_min and the derivative in Q by 1, uniformly for m>=2. The exact certificate supplies a positive baseline gap delta_n*J0.

For smaller m, use m times the Holder residual A^(1/m)+B^(1/m)-Q^(1/m)-J^(1/m). Its coordinate derivatives are bounded by 1/x_min. At the reference, strong convexity of x^(n/m) gives negative residual magnitude at least t^2(1-t)^(2n+2), with t=1/[3(n+1)]. No unknown joint law is differentiated.

Candidate crude bounds: A0>=2/3, Q0>=35/36, J0>=4/9. For sufficiently small coordinate errors, larger-count total perturbation cost <=10 epsilon, smaller-count cost <=12 epsilon. Delta_n >=1/[180(n+1)^2], so larger baseline gap >=1/[405(n+1)^2]. Smaller gap >=4/[81(n+1)^2]. Candidate epsilon=1/[10000(n+1)^2] should leave both strict. These constants are proposed, not certified here.

If established, a reference-consistency test with simultaneous bounded-variable confidence intervals could give a finite-sample false-acceptance bound against all wrong-count models in this class. It would not certify global gate independence, the validity of the physical observation contract, arbitrary unknown model membership, or unknown nominal calibration. Large constants and lack of optimality must remain explicit.
