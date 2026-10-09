# Boundary probes remove the interior finite-panel gauge

This is a stronger instrument than RESULT.md's interior/zero grid. It permits unit commands and retains the predecessor's exact endpoint-preserving calibration premise. It does not claim that four interior interaction values identify absolute factors, and does not identify complete calibration functions between sampled commands.

## Conditional finite-command theorem

In the fixed finite unguarded one-effect independent-route model, suppose a root i belongs to at least one **promised positive** support S with |S|>=2. Fix finitely many desired interior commands for that root, and available auxiliary ordered interior levels for the other needed roots. Certified population Cauchy access to finitely many endpoint command vectors, now allowing some unit coordinates, suffices to compute r_i at those desired commands to any requested accuracy. No route-count ceiling is required.

The inventory's whole positive-support pattern need not be discovered for this procedure. It uses the specified positive S, and positivity of reduced supports follows from that promise. All multiplicities are finite integers. The common coordinatewise calibration and independent-route premises remain essential.

## Step 1: recover the positive interaction count and ratios

If n_S is not already known, recover it using the predecessor's four isolated interaction values and half-integer determinant cuts. This requires finitely many distinct interior command vectors and potentially many precision refinements. Once n_S is known, the original S contrasts give its true products P_S and all required sampled within-root ratios.

## Step 2: decide unary presence using the deterministic corner

At the command with coordinate i equal to one and every other coordinate zero,

Q_i(1)=0 if n_{i}>0,
Q_i(1)=1 if n_{i}=0.

Only a unary i route can succeed there. Endpoint preservation makes the alternatives exactly zero and one. A certified probability enclosure of error less than 1/4 separates them; this is not a generic approximate zero test. In the ideal stochastic model the corner endpoint is itself deterministic, but the rest of the algorithm still requires the stronger population-probability oracle.

This detects unary presence only. It is not a procedure for deciding every multi-root support's absence, and it is unavailable under the interior-only observation contract.

## Step 3a: positive unary support

If n_i>0, its two-level interaction ratio and solo probabilities satisfy ANCHORED_UNARY_COUNT.md. Recover n_i by nonzero half-integer cuts. Then every desired point is

r_i(x)=1-Q_i(x)^(1/n_i).

No boundary log subtraction is needed.

## Step 3b: absent unary support

If n_i=0, hold coordinate i equal to one and regard Q as a response field on the remaining roots. Every raw value needed with those other roots either zero or interior is strictly positive. Indeed a surely successful route would have to be the absent unary i route; every other active route has at least one strictly interior coordinate.

This reduced field is another finite unguarded independent-route model. For every nonempty support T among the remaining roots its multiplicity is

tilde_n_T=n_T+n_(T union {i}).

Routes not containing i retain their support; routes containing i lose a factor r_i(1)=1. Distinct route occurrences remain independent. The empty-support contribution would be n_i and has been excluded by the unary-presence decision.

Put T=S without {i}. Then tilde_n_T>=n_S>0.

- If |T|>=2, apply the inherited positive-interaction finite-panel decoder to T in the reduced field. It returns tilde_n_T without knowing its summands or any other support counts.
- If T={j}, first decide n_j=0 or positive using its unary corner. If positive, recover n_j by the original S two-level ratio and ANCHORED_UNARY_COUNT.md; otherwise n_j=0 is already known. Then tilde_n_T=n_j+n_S is known.

The reduced isolated contrast can now be inverted:

P_T=1-(E_T^(i=1))^(1/tilde_n_T)
   =product_(j in T) r_j(x_j).

It is positive at the fixed other-root reference values. For every requested interior command x_i, compare with the original positive S contrast at those same other-root values:

r_i(x_i)=P_S(x_i,x_T)/P_T(x_T).

Every denominator is positive. This determines the desired point without an endpoint limit and without separately determining each factor in P_T.

## Why the computation is finite under this oracle

Only finitely many roots, requested levels, mask contrasts, unary decisions and positive-support count searches are used. Every integer search terminates by its promised positive finite count and nonzero half-integer signs. Every required quotient is of positive computable reals, and every root/power computation has certified interval refinement. Thus any finite requested output accuracy is reached in finite computation under the population Cauchy contract.

The precision demand and number of oracle refinements are not uniformly bounded. The statement is not a finite-sample calibration theorem, does not claim efficient runtime, and does not certify the common endpoint law in a physical system. Endpoint calibration errors, non-homeomorphic maps, guards, mixtures, cross-talk or shared occurrence gates can invalidate the procedure.

## Relation to the rank theorem

A single AB support has a genuine reciprocal gauge on every finite interior/zero grid. If its unary supports are absent, however, Q(1,x_B) and Q(x_A,1) expose calibrated factors after the positive AB count is known. The added unit-coordinate observations are not preserved by the reciprocal rescaling's endpoint-fixed interpolating homeomorphisms. Thus the two theorems concern different retained records and do not conflict.

For a known full inventory the reduced aggregate counts are already known, simplifying Step 3b. The stated procedure also works when only the positive interaction promise is supplied, because it recovers the required aggregate or unary counts rather than assuming them. It makes no general absence-discovery or whole-function claim.
