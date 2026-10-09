# Independent review: full face-threshold KL rate

8 October 2026 UTC. Scratch-only mathematical review. No protected integration, empirical validation, novelty certification, or closure.

## Verdict and binding

**PASS**, for the stated hard pair and the final face-only observation/cost contract.

Reviewed target: `../full-face-threshold-kl-rate/RESULT.md`

Final SHA-256: `1c2fd5cf4e8006205cbd61562d88eb5da72d4952f335b17952540ec9f1a1d544`.

The proved assertion is

    n^4 KL(P1 || P0) -> 1/2,

where one observation is the pair of coordinate minimum thresholds under the specified n-route reference and (n+1)-route Joe alternative. The finite-face-word information bound and expected number of independent retained vectors follow under the final section 6 contract. I found no unresolved mathematical blocker.

This review initially inspected hash `a656796442d47c68dd59ca8d9ddad809f055db0a02620d8cbe497961b39c7672`. The parent strengthened section 6 to actual-action prefixes and started-vector charging, producing `c7ad091437784fbdfffa81ccd67513a9bb4f8f4cdcd78cd0ed0135152cbaf444`. I reviewed that replacement, requested the narrow clarification excluding reuse of an interior endpoint-only draw, and inspected the final replacement sentence and hash above. The review's final diagnostic run binds the final hash, not either superseded version.

## 1. Source assumptions versus independent checks

Accepted as the problem's stipulated model: independent routes, the alternative per-route threshold CDF H_c(ab), common calibration H_c(t)=1-(1-t)^c, unchanged latent vectors during replay, and the specified observation interface. The Joe family name and bibliographic provenance are inherited; I did not conduct an external literature or novelty search.

I independently checked the consequences needed here:

- H_c(ab) is a valid continuous bivariate threshold law. Its interior mixed derivative is c(1-ab)^(c-2)(1-c ab)>0, its coordinate margins are H_c, and its grounded/total-mass boundary values are correct.
- Inclusion-exclusion gives the one-route joint threshold tail S=x^c+y^c-(x+y-xy)^c. Route independence gives F1=S^m and F0=x^n y^n. Since mc=n, both coordinate margins are x^n.
- The stated S_x, S_y and S_xy formulas are correct. Differentiating S^m gives the predecessor's density. Exhausting the interior by compact rectangles accounts for all mass; continuous margins rule out boundary mass. Thus no singular remainder is missing.
- The inherited positive double integral follows directly by integrating the negative second derivative of z^c over the rectangle with base xy and side lengths x(1-y), y(1-x). Dividing by (xy)^c and scaling to a unit square gives precisely equation (6), with A=e^(u/n)-1 and B=e^(v/n)-1 in the correct positions.
- The global envelope f1_XY<=C_n/(xy) is valid. In particular S_x<=c/x, S_y<=c/y, S_xy<=c/(xy), S<=1 and m>=2 imply C_n=m(m-1)c^2+mc=n^2+n/(n+1).
- The inherited infinite-chi-square argument is sound: the shrinking lower-corner probability ratio tends to (2-2^c)^m>0, contradicting localized Cauchy-Schwarz if the likelihood ratio were in L2(P0). This is a fixed-n statement and gives no contradiction to the KL asymptotic.
- The fresh endpoint absence functions agree: [1-H_c(ab)]^m=(1-ab)^n. This equality contributes zero conditional KL only with the stipulated fresh independence and discard rule.

The predecessor's optimized two-face coefficient is not needed to prove the new theorem. I read its compact/escape proof and comparison language, but the present review does not re-certify its broader ancestry, earlier all-wrong-count upper bound, empirical interpretation, or external references.

## 2. Common transform and exact density ratio

The common map uses n in both worlds: U=-n log X and V=-n log Y. Reversing both coordinate inequalities gives the survival function G1=F1(e^(-u/n),e^(-v/n)), not a CDF. Since mc=n,

    G1=e^(-u-v) exp(H), H=m log[S/(xy)^c].

Twice differentiating the survival function yields a positive density with

    f1/f0=exp(H)[1-H_u-H_v+H_u H_v+H_uv].

The mixed-survival derivative has a positive sign. There is no missing Jacobian: f1_UV=f1_XY xy/n^2, while f0_UV=e^(-u-v). The same invertible map in both worlds preserves KL. A separate alternative transform using m would not establish this formula; the target does not make that mistake.

## 3. Growing-box derivative remainder

I checked the total-order-at-most-two norm estimates, including the axes u=0 or v=0. The integrand has denominator W>=1 and is smooth there, so no endpoint derivative exception occurs.

For t=1/n, tL<=1 and p=1+L:

- The bounds for E=(e^(tu)-1)/t and E-u follow from the ordinary exponential Taylor remainder and its first two derivatives; the corresponding F bounds are identical.
- q=c-2 lies in [-3/2,-1). Differentiating the unit-square integral once or twice produces exactly the W powers and A', A'', B', B'' factors claimed. Their displayed constants are loose but valid. Consequently ||I||_2<=K and ||I-1||_2<=Ktp hold uniformly.
- The four-term decomposition of cEFI-uv and the product norm bound give ||J-t^2uv||_2<=Kt^3p^3 and ||J||_2<=Kt^2p^2. The identity m(1-c)=1 and 1/m<=t then give ||h||_2<=Kt^3p^2.
- For phi(h)=log(1+h)-h, h>=0 ensures |phi|<=h^2/2, |phi'|<=h and |phi''|<=1. The second-derivative composition contains both phi''(h)h_i h_j and phi'(h)h_ij; both are bounded by K||h||_2^2. Therefore m||phi(h)||_2<=Kt^5p^4. The target includes both terms and obtains the valid, deliberately weaker remainder Kt^3p^4 for H-t^2uv.

For L=C log n, the additional ratios needed for the density expansion vanish: t^3p^2->0, tp^2->0 and ||H||_2->0. Expanding the exact density, rather than only the survival function, gives

    R-1=t^2(1-u)(1-v)+r,  sup |r|<=Kt^3p^4.

The linear differential operator is H-H_u-H_v+H_uv, so the kernel is uv-v-u+1 with the stated signs. Products of H or its derivatives are O(t^4p^4). No step introduces a global L2 assertion.

## 4. Dependence-safe entropy tail and mass cancellation

The density envelope transforms to f1_UV<=1+1/[n(n+1)]<=3/2. Thus log R<=log(3/2)+u+v globally. This upper bound and the common Exp(1) margins are sufficient; independence of U,V under P1 is never needed.

For the potentially dangerous cross-tail term, I independently checked

    E1[U 1_{V>L}] <= integral_0^infinity min(e^(-s),e^(-L)) ds
                      =(L+1)e^(-L).

Together with its exchanged version and the two same-coordinate tail moments, the union bound gives the stated 4(L+1)e^(-L) first-moment envelope. The negative entropy contribution is bounded separately by f0/e on R<1. The target therefore establishes absolute integrability, not just an upper bound for a conditionally defined signed integral.

The centered entropy psi(R)=R log R-R+1 is especially appropriate. Since both densities have mass one,

    KL(P1||P0)=integral f0 psi(R).

On the tail, f0 psi(R)<=f1(log R)_+ +f0. The resulting bound [2 log(3/2)+4(L+1)+2]e^(-L) tends to zero after multiplication by n^4 whenever C>4. The far tail can still destroy chi-square integrability because the latter weights R^2 rather than R log R.

No unaccounted first-order bulk mass survives. Either use psi directly, as the target does, or express the bulk integral of R-1 as minus the tail mass discrepancy. Integrating a pointwise expansion of R log R without this cancellation would be insufficient; that error is absent.

## 5. Coefficient and remainder integration

On the growing box sup|R-1|->0, so psi(1+delta)=delta^2/2+O(|delta|^3) uniformly. With k=(1-u)(1-v), the target's error estimates follow from direct expansion:

    sup |t^(-4)delta^2-k^2| <=K(tp^6+t^2p^8),
    t^(-4) integral_box f0 |delta|^3 <=Kt^2p^6.

Every right-hand side tends to zero. The box has reference probability at most one, and the integral of k^2 over increasing boxes tends to its full value. Since an Exp(1) variable has E[(1-U)^2]=1,

    (1/2) integral e^(-u-v)(1-u)^2(1-v)^2 du dv=1/2.

The analytic tail bound completes the limit. I find no missing limit interchange, hidden independence assumption, or nonuniform derivative step in sections 2–5.

## 6. Adaptive protocol and expected cost

Every face-only bit is a comparison with one of the two minima. With the common policy randomization, the complete adaptive finite face transcript is therefore a common measurable function of those minima and auxiliary randomness. Data processing bounds its KL by D_n for every selected word, without a numerical length or precision cap.

The final actual-action oracle formulation is sound and stronger in precision than completed-word indexing:

1. Reveal the exact minima and charge one retained vector when its first face probe starts.
2. Continue the original policy using only its original observations, even though the augmented transcript records the additional oracle information.
3. A fresh reveal contributes D_n conditional KL, while later face observations of that same unchanged vector are deterministic given its revealed minima and commands.
4. Distinct, discarded, independent endpoint-only observations have identical conditional laws for this hard pair and contribute zero KL.
5. Finite actual-action prefixes and started-vector cost remain defined even on paths with a nonterminating word.

The final clarification is material to scope: an endpoint-only draw cannot be followed by retained replay unless all its observations were face-only and it is charged from its first observation. In particular an initial interior AB bit cannot be simulated from the minima, so charging that vector alone would not repair such an enlarged interface. The final text expressly excludes it.

The finite-prefix chain rule, binary data processing on rejection by action T, monotone convergence of started-vector counts, and lower semicontinuity of binary KL give D_n E1[N]>=kl(1-alpha,alpha). The event probabilities have the required directions only because correctness is unconditional and includes finite termination. Conditional-on-termination correctness would not suffice. The expectation and KL orientation are consistently under P1.

This is a hard-pair lower bound. It does not show that the minima-only channel identifies count over the whole unknown-calibration class, nor that the information constant is an achievable or minimax sample/probe-cost constant. Zero-information fresh endpoints for this particular pair do not enlarge that conclusion.

## 7. Independent bounded diagnostics

`checks.py` and `CONTROL_RESULTS.json` provide reproducible independent controls:

- Exact symbolic checks of three S derivatives, the survival-density identity, and the leading squared-kernel integral.
- Six 70-decimal-digit point checks comparing the transformed original density with the H-derivative ratio, and the positive integral with the closed formula. The largest observed density discrepancy was below 9e-70; the integral discrepancies were below 4e-71.
- Two deterministic tensor Gauss-Legendre resolutions, 80 and 140 nodes per coordinate, on [0,10 log n]^2 for n=8,16,32,64,128,256,512. The corresponding scaled bulk entropies rise from approximately 0.39666389917 to 0.49805383161. The two resolutions differ by less than 7e-13 in each scaled result. Analytic omitted-tail upper bounds are recorded separately.

These finite diagnostics are not proofs of uniformity, empirical sampling, or certified interval quadrature. In particular the agreement between quadrature resolutions does not certify their numerical error. The mathematical argument above, rather than numerical convergence, supports PASS.

The first symbolic diagnostic attempt stopped because ordinary SymPy simplification did not reduce the first-derivative power identity. Inspection showed algebraically equal powers, not a formula mismatch. The final script explicitly normalizes the integer power shifts on the positive interior domain and reruns all checks. No target or predecessor file was modified by this reviewer.

## 8. Time accounting

`RESEARCH_EVENTS.jsonl` prospectively records three credited active-review intervals: 59 seconds, 84 seconds and 66 seconds, totaling **209 seconds (3 minutes 29 seconds)**. Tool-execution waits after the recorded pauses and report packaging are excluded. Earlier orientation and reading occurred before the first explicit timing record and are deliberately not counted or inferred. This is a bounded logged-time record, not an estimate of total elapsed effort.
