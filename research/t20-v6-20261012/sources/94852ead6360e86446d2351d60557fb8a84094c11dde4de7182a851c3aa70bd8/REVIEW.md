# Independent review: computable moments with noncomputable indexed mass

10 October 2026 UTC. Bounded ordinary mathematical proof review of `capped-tensor-recovery-20261010/RESULT.md`, §7.2, with the support and norm conventions in §§2 and 7.1. This review is independent of the participating reviewer who proposed the construction. No broad source search, large test, formal kernel claim, or review of the other positive theorems is included.

## Verdict

The counterexample is mathematically sound. Coordinatewise computable nonnegative caps with a computable upper bound on their finite total do not suffice for the stated indexed-law recovery theorem. The supplied example has a uniformly computable complete tensor-moment name but a noncomputable zeroth indexed weight. Its exact cap total is noncomputable and it has no computable cap-tail modulus.

One minor notation clarification was requested and verified in the revised draft: the first-halt definition now explicitly runs machine e on input e, matching the diagonal halting set. The author also inserted the explicit strict-error cutoff checked below. No unresolved mathematical issue remains in the reviewed subsection.

## Independent checks

1. **Uniform cap coordinates and normalization.** Use the computable Cantor bijection j=1+⟨e,t⟩ for j≥1. A finite simulation of machine e on input e decides whether its first halt occurs at stage t, including the fixed convention for stage zero. Consequently p_j is an exactly computable rational, uniformly in j≥1. Every halting e contributes its weight w_e=4^(−e−1) at exactly one index and every nonhalting e contributes nothing. Thus Σ_(j≥1)p_j=α, where α=Σ_(e∈H)w_e≤1/3. Setting p_0=1−α gives a probability law. The cap c_0=1, c_j=p_j for j≥1 is uniformly coordinate-computable and dominates p.

2. **Noncomputability of α and p_0.** Suppose α were computable. Inductively decide H below e, and subtract the known earlier weights from α. The residual is at most Σ_(n>e)w_n=w_e/3 when e∉H and at least w_e when e∈H. A rational approximation with error ≤w_e/12 is at most 5w_e/12 in the first case and at least 11w_e/12 in the second; comparison with 2w_e/3 therefore decides e∈H. This would decide the diagonal halting set. Hence α and p_0=1−α are noncomputable. An ℓ¹ name computes every indexed coordinate because |q_0−p_0|≤‖q−p‖₁, so p has no computable ℓ¹ name.

3. **Baseline cancellation and tensor norm.** For κ_0=(0,1) and κ_j=(2^(−j),1−2^(−j)), the two coordinates are in [0,1] and their differences from κ_0 have maximum absolute value 2^(−j). Telescoping each ordered r-fold tensor coordinate yields

       ‖κ_j^⊗r−κ_0^⊗r‖∞ ≤ r·2^(−j),  r≥1.

   This is the maximum over the 2^r ordered coordinates, not the tensor ℓ¹ norm. Since p_0=1−Σ_(j≥1)p_j, absolute convergence gives the exact identity

       M_r(p)=κ_0^⊗r+Σ_(j≥1)p_j(κ_j^⊗r−κ_0^⊗r).

   Retaining exactly 1≤j<N leaves error at most

       r·2^(−N) Σ_(j≥N)p_j ≤ (r/3)·2^(−N) ≤ r·2^(−N).

   For an explicit strict-error algorithm at requested accuracy 2^(−k), let L be the least nonnegative integer with 2^L≥r and choose N=k+L+1. The displayed weaker bound is then ≤2^(−k−1)<2^(−k). Every retained term is rational and found using only finitely many halting-stage tests. Grade zero is exactly one. This computes all grades and ordered coordinates uniformly; it never evaluates p_0 or decides eventual halting.

4. **Exact total versus upper bound.** The cap has classical total C=1+α≤4/3. The rational bound 4/3 is computable, but C is not. A computable tail modulus, together with the uniformly computable coordinates, would compute C by finite partial sums and hence compute α, a contradiction. Conversely, for a nonnegative uniformly computable sequence, a computable exact total does supply a computable tail modulus: search for a finite partial sum with a certified strict gap below the desired tail tolerance. The exact-total qualifier is essential, and the draft states it.

5. **Correct conclusion and scope.** The support is uniformly computable, pairwise distinct, and lies in the compact binary simplex. Complete moments still uniquely determine the Borel mixing measure and therefore every indexed weight, using the already stated compact moment-determinacy argument. The failure is effective recovery of the indexed law, not moment nondeterminacy. No computable Markov operator with stationary law p is constructed; the constant-row operator with row p has the noncomputable entry p_0 and would not qualify. The example therefore does not contradict the separate computable stationary-selection result.

## Evidence limit

This is a direct universal proof check. Finite simulations establish individual coefficient values only; no finite test can establish the undecidability reduction or the universal absence of a computable tail modulus. No computational experiment is relied on for those claims.

Initial reviewed source SHA-256: `d0ed8d0f6e428693ae95df2cfe3adb46b3cbe419a636a2a2a77379c91f752843`.

Revised source SHA-256 after verifying those two clarifications: `d02613fe462d57599e4b2432c8c80b3ef691ac060d7f71aff9ece9730dffd78e`.

## Final frozen readback

The complete final §7.2 was reread on 10 October 2026 UTC. Its mathematical construction and proof remain unchanged in substance from the revised version reviewed above, and the verdict remains sound with no unresolved issue. The attribution paragraph now correctly calls the constructor a participating reviewer and separately identifies this independent scoped check. The explicit diagonal input, strict-error cutoff, noncomputable exact cap total, and stationary-operator boundary are retained. This readback does not extend the review to §8, §9, other theorems, controls, or manifest contents.

- Final source `capped-tensor-recovery-20261010/RESULT.md` SHA-256: `262503e92380ec868f28670b18939d701cd51808aedc65f7fe6f2fa57e0dbf6d`.
- Author `capped-tensor-recovery-20261010/MANIFEST.json` SHA-256 (identity binding only): `40315f75e0136493b8706aefdf7bc17a9844a5a38ba60e5d6dd630f84128aad1`.
- Exact final §7.2 bytes, from its heading up to but excluding the §8 heading, SHA-256: `d0d8e7e59d05ebb6a1e8f8566a9dc52a6b704c4b4dd369fc9e2488a1b87bc545`.
- Mathematical body beginning “Keep the exact support in §7.1.”, excluding the heading and attribution paragraph, SHA-256: `679b9c1c4f40deece75eae3603632bedaa2a739354e1adacd42d6b13f2a6b218`.
- Exact subsection snapshot: `FINAL_SECTION_7_2.md`; scoped receipt: `FINAL_SCOPE_RECEIPT.json`.

The two earlier whole-source hashes above identify historical review stages; this final binding supersedes them as the reviewed frozen target. The final readback is a direct text/proof check, not a claim of mechanical comparison against an archived historical source snapshot.
