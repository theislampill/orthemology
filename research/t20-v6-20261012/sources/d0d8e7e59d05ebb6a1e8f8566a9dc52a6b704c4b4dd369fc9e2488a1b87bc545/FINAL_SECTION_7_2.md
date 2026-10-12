### 7.2 A computable full moment name can identify a noncomputable law

The following sharpened control was developed with a participating reviewer; it is a new-to-this-packet construction using classical halting encoding, not an independent reviewer rediscovery or a field-priority claim. A different reviewer independently checked this subsection; that scoped check is recorded separately in `hidden-mass-independent-review-20261010/REVIEW.md`.

Keep the exact support in §7.1. Fix an effective machine enumeration and its undecidable diagonal halting set H. Let

    w_e=4^−(e+1),    α=Σ_(e∈H) w_e,    0≤α≤1/3.

The real α is noncomputable. Indeed, after deciding the earlier digits, the residual at e is at least w_e if e∈H and at most w_e/3 if e∉H. Approximations of a computable α with error, say, w_e/12 would decide these alternatives successively using threshold 2w_e/3, and hence decide H.

Use the Cantor bijection `⟨e,t⟩=(e+t)(e+t+1)/2+t` from ℕ² to ℕ. Assign each positive index uniquely by `j=1+⟨e,t⟩`, and define

    p_j = w_e if machine e on input e first halts at exactly stage t,
          0 otherwise,                                      j≥1;
    p_0 = 1−α.

A stage convention starts with the initial configuration at t=0; whether the first halt is exactly t is determined by simulating the finite t steps and checking prior configurations. Thus the positive-index coordinates are uniformly computable rationals, their total is exactly α, and p is a probability. But p_0, hence the ℓ¹ law p, is noncomputable.

Nevertheless all tensor moments have the uniformly computable formula

    M_r(p) = κ_0^⊗r
             + Σ_(j≥1) p_j (κ_j^⊗r−κ_0^⊗r).                 (3)

For r≥1, the maximum-norm error after retaining 1≤j<N is at most

    Σ_(j≥N) p_j r2^−j ≤ r2^−N Σ_(j≥N)p_j ≤ r2^−N.

For strict error less than 2^−k, take `L=min{ℓ≥0:2^ℓ≥r}` and `N=k+L+1`. Every retained coefficient and tensor is rational and exactly computable by finite simulation. Grade zero is one. This is a single uniform algorithm for all grades and coordinates. The noncomputable baseline mass has cancelled from (3); pretending to evaluate p_0 directly would miss the point of the construction.

Now supply c_0=1 and c_j=p_j for j≥1. These cap coordinates are uniformly computable, c is classically summable with `C=1+α≤4/3`, and p∈K_c. There can be no computable cap-tail modulus, since it would compute C and hence α. The bound 4/3 is computable; the exact total C is not. Supplying a computable exact total would restore an effective tail by §2 and is expressly excluded from this control. Thus replacing effective summability by coordinate computability plus classical summability makes C4 false even for a fixed computable support and a genuinely valid computable complete moment name. Lemma C2 still gives unique indexed-law determination.

The small cap total does not contradict the inherited stationary-law contraction result: no computable row-dominated Markov operator having this p as its stationary law is supplied here. A constant-row operator with row p would itself have a noncomputable entry. The moment-inverse and selected-operator input contracts are different.

