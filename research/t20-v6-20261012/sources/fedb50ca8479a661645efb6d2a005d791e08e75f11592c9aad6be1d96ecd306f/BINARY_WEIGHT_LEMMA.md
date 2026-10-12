# Rational row weights: exact ordinary derivation

11 October2026 UTC. Root collaborative lemma for the proposed alternative original-L1 reduction. This is ordinary algebra; no kernel credit yet and no new ordinary hierarchy classification.

Fix natural a,b with b>0 and 0≤a<b. Put A_n=floor(2^n a/b), d_n=A_(n+1)−2A_n. Divide 2^n a=b A_n+r_n, 0≤r_n<b. Then A_(n+1)=2A_n+floor(2r_n/b), hence d_n∈{0,1}. Equivalently d_n=(floor(2^(n+1)a/b)) mod2. Natural exponentiation, multiplication, division by the fixed positive b and remainder are primitive recursive; the formula is jointly primitive recursive in all natural inputs when total division is used, with semantic hypotheses b>0 and a<b.

For N≥0 the weighted prefix telescopes:

    Σ_(n<N) d_n / 2^(n+1) = A_N/2^N − A_0 = A_N/2^N.

The last equality uses a<b. Its exact error is r_N/(b2^N), between0 inclusive and2^-N exclusive. Thus the infinite weighted sum is a/b. Terminating dyadics use eventual zeros automatically; no ambiguous expansion convention is needed. q=0 has all digits0. q=1 must be handled separately (all rows diffuse); applying the a<b telescoping formula without its hypothesis would incorrectly produce0.

Assign unary-tag row n to a fair diffuse observer if d_n=1, and to the same base observer otherwise. If the original tagged-mixture law and disjoint injective tag mass theorem apply to these actual row observers, their defect is q*1+(1−q)*d_base. This is conditional on the actual row-program and output-law bridge, which the binary sum alone does not establish. It is an alternative construction, not verification of the literal Python compile_shift.

For compiling a lower reduction, a fixed jointly primitive-recursive family may be composed with this selector. One must not infer a universal primitive-recursive interpreter from that fact. If the base observer varies as a numeric arbitrary program, its uniform evaluator is only Computable in the inherited formal result; this remains a separate compiler-assurance issue.
