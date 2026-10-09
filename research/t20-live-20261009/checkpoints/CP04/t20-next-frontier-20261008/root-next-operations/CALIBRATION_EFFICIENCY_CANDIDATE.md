# Prospective calibration-efficiency lower bound

2026-10-08 13:03 UTC. Sent for independent verification; no completed theorem claim.

Use the midpoint calibration maps from GLOBAL_CALIBRATION_CANDIDATE, writing r*_k(x)=x+d(x), r*_(k+1)(x)=x-d(x), d>=0. Define clipped maps r_k=min(r*_k,x+eta), r_(k+1)=max(r*_(k+1),x-eta). Both should remain static monotone endpoint-preserving maps within uniform error eta.

Where d<=eta, the two count worlds have identical endpoint laws. Concavity's tangent inequality t^(k/(k+1)) <=(1+kt)/(k+1) implies d(x)<=x/(2k+1). Therefore d>eta implies x>(2k+1)eta. On that region the count-k no-hit probability is (1-x-eta)^k, larger than the count-(k+1) no-hit probability but bounded above by exp[-k(x+eta)]<=exp[-2k(k+1)eta]. Boundaries are valid because active clipping occurs only where x+eta<r*_k<=1 and x-eta>r*_(k+1)>=0.

Thus the conditional endpoint TV difference is uniformly <=exp[-2k(k+1)eta] under every command. A common adaptive policy cannot increase fixed-budget transcript TV beyond N times that bound. Uniform binary error <=delta<1/2 consequently requires N>=(1-2delta)exp[2k(k+1)eta]. Identical-law threshold remains a stronger impossibility where eta>=eta_star.

If valid this distinguishes robustness-identifiability from efficiency: error eta=c/k below the sharp threshold still incurs exponential worst-case sample cost; a family with polynomial sample budget necessarily has eta=O(log k/k²). It does NOT assert k^-2 is a universal ceiling on every polynomial-budget calibration scheme. A matching logarithmic-tolerance construction is a further question, not established here.
