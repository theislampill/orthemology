# Corroborating check of the imported unary lemma

The general positive-unary sign lemma is owned by `../finite-hypergraph-calibration/ANCHORED_UNARY_COUNT.md` and its separate review. The bounded detector imports that final bound statement. The derivation below was checked independently in this lane and by its reviewer; it is retained only as corroboration, not a second discovery or separately owned general theorem. It applies only after support positivity and an incident interaction count have been established.

### Unary counts on interaction-anchored roots

Detection already gives every absent unary count as zero. Suppose i participates in some positive interaction S and its unary count m=n_{i} is positive. The count n=n_S is now known. Fix other coordinates of S at interior commands. At two ordered nominal commands on i, write their actual rates as 0<a_1<a_2<1. The corresponding isolated interaction values satisfy

    Z_k=(1-K a_k)^n,  K>0.

Thus their computable positive transforms are

    P_k=1-Z_k^(1/n)=K a_k.

The two unary response values are U_k=(1-a_k)^m. For any candidate h>0 define

    R_k(h)=1-U_k^(1/h)=H_(m/h)(a_k),
    H_c(z)=1-(1-z)^c.

The determinant-like contrast is

    D(h)=R_2(h)P_1-R_1(h)P_2
        =K a_1a_2 [H_c(a_2)/a_2-H_c(a_1)/a_1], c=m/h.         (8)

For c>1, H_c is strictly concave with H_c(0)=0, so H_c(z)/z strictly decreases on (0,1). For 0<c<1 it is strictly convex and the ratio strictly increases. For c=1 the ratio is one. Therefore D(h) has strict sign(h-m), and vanishes only at h=m.

Half-integer cuts again avoid equality. Rational positive-root interval computations and the known interaction count make D(h) Cauchy-computable, and each required sign search terminates. Binary search in 1,...,M recovers m. If M=1 and positivity is known, the count is already one and no cut is needed.

This recovers anchored unary counts through a finite collection of population values, without first reconstructing the whole calibration map or asserting an effective rate for a boundary limit.

