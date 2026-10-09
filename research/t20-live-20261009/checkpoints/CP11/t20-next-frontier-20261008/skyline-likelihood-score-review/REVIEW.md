# Independent review: localized retained-skyline likelihood score

8 October 2026 UTC. Bounded, scratch-only mathematical review. This packet is a new sibling, outside the tenth checkpoint. It makes no protected-integration, physical-access, empirical, kernel-assurance, historical-floor, or closure certification. No predecessor or archive was overwritten.

## Verdict

**PASS for the localized expansion and the explicitly limited localization claims.** The reviewed author result is `../skyline-likelihood-score/RESULT.md`, SHA-256:

`ba6345d03e5fe9d2735f221ee45f5ee6b6f05508ce4d96f8ba9a86ceb3da5b5f`.

For the actual fixed-count pair, with m=n+1, e=1/m, c=1−e, 1≤k≤n, a=k/m≤1/2, and U≤1/2, the signs and coefficients in

    log L = ((k−mU)²−k)/(2m²) + 2(Σ_i x_i y_i/m−M1) + R

are correct. The author's bound |R|≤40(a+U)³ is proved by its stated inequalities. The independent derivation below gives the stronger safe estimate

    |R| ≤ (2/3)a³ + 7aU² + (43/9)U³ ≤ 5(a+U)³,

which is supplementary evidence, not a requested change to the frozen author packet. Constants have not been optimized.

The exact fixed-count first-moment identities, Markov localization under both worlds, and boundary obstruction also check out. None yields a KL, Hellinger, total-variation, sample-complexity, or optimality rate for this score. No Poisson approximation, random-sample experiment, or new field-wide novelty claim is involved.

## 1. Sources and precise scope

The review reads the exact likelihood in `../retained-skyline-likelihood/RESULT.md`, the author's complete result and deterministic controls, and the mean identities in `../skyline-count-information/RESULT.md`. `SOURCE_BINDINGS.json` binds these inputs. The likelihood is the **unnormalized common-stratum likelihood** g1/g0 for P0 with n uniform routes and P1 with m Joe routes. It is not the likelihood of P1 conditioned on K≤n: that conditional likelihood would add the constant −log(1−p_n) to log L.

The alternative-only stratum K=m remains singular relative to P0. The expansion is stated only on 1≤K≤n and the small-area/count window. All coordinates are strictly interior and tie-free as in the predecessor. The observable is the ideal retained skyline; this is not a claim of finite-probe exact reconstruction or physical implementation.

## 2. Independent geometric bounds

Write the lower staircase as E={(x,y):0≤y≤h(x)}, ignoring measure-zero boundaries. The height h is nonincreasing. Set

    H(x)=∫_0^x h(v) dv, U=H(1), M_r=∫_E (xy)^r dxdy.

Because H(x)≥xh(x), for each integer r≥1,

    U^(r+1)=(r+1)∫_0^1 H(x)^r h(x) dx
             ≥(r+1)∫_0^1 x^r h(x)^(r+1) dx
             =(r+1)² M_r.

In particular M1≤U²/4 and M2≤U³/9. Also [0,x]×[0,y] lies in the closure of E whenever (x,y) does; hence xy≤U, including at all skyline points.

For the ordered skyline and x_(k+1)=1, direct strip integration gives

    U=x_1+Σ_i(x_(i+1)−x_i)y_i,
    M1=[x_1²+Σ_i(x_(i+1)²−x_i²)y_i²]/4.

This independently confirms the requested moment formula, its denominator 4, and the inclusion of the initial full-height strip.

## 3. Independent uniform density bound

Let t=xy and g_e(t)=f_c(t)/c. From the exact density,

    g_e(t)=(1−t)^(−e)[1+et/(1−t)]
          =Σ_(j≥0) (j+1)(e)_j t^j/j!,

where (e)_j is the rising factorial. For j≥2, the coefficient divided by e is nonnegative and increasing in e. Consequently

    [g_e(t)−1−2et]/(et²)

is nonnegative and coordinatewise nondecreasing for positive e,t≤1/2. At e=t=1/2 it equals 12(√2−1)<5. Thus throughout the required range,

    0≤g_e(t)−1−2et≤5et².                              (A)

Integrating (A), write

    Dc=D0+eB,
    B=U−2cM1−η,       0≤η≤5cM2≤5U³/9.

The geometric bounds imply

    U≥B≥U−U²/2−5U³/9≥(11/18)U≥0.                    (B)

This positivity is convenient for the independent proof. The author's proof does not need it: its separate bounds −e≤(Dc−D0)/D0≤e are already correct, following from f_c≥c integrated separately on D and E.

## 4. Independent fixed-count remainder calculation

Let w=M1, T=Σ_i t_i, d=1−U and W=B/d. The exact predecessor likelihood is

    log L = A + S + C,
    A=−log(1−a)+k log(1−e),
    S=Σ_i log g_e(t_i),
    C=log(1−U)+(1−a)e^(−1) log(1+eW).

This retains the fixed sample sizes n=m−1 and m throughout.

### Count factor

For r(z)=−log(1−z)−z−z²/2, the nonnegative power series gives

    A=(a²−ae)/2+ρ_A,
    ρ_A=r(a)−k r(e),
    0≤ρ_A≤r(a)≤(2/3)a³.

Indeed a=ke and k≥1 imply a^j≥k e^j termwise. The negative −ae/2=−k/(2m²) term is therefore indispensable.

### Visible-point factor

Using log g_e=e[−log(1−t)]+log(1+et/(1−t)), log(1+v)≤v, and

    0≤−log(1−t)+t/(1−t)−2t≤3t²,

gives log g_e−2et≤3et². The lower bound log g_e−2et≥0 follows, for example, by differentiating: its derivative before subtracting 2et is

    e/(1−t)+e/[(1−t)(1−ct)]≥2e.

Hence

    S=2eT+ρ_S,       0≤ρ_S≤3aU².

### Dominated-mass factor

By (B), 0≤W≤U/(1−U)≤2U. Algebra gives

    W=U+U²−2w+ρ_W,
    ρ_W=[U³−2Uw+2ew−η]/(1−U).

The triangle inequality, w≤U²/4, η≤5U³/9, and 1/(1−U)≤2 yield

    |ρ_W|≤(37/9)U³+eU².

Also

    |log(1−U)+U+U²/2|≤(2/3)U³,
    |(1−a)e^(−1)[log(1+eW)−eW]|≤2eU².

After substitution, the remaining cross term is −aU²+2aw, with absolute value at most aU². Therefore

    C=U²/2−aU−2w+ρ_C,
    |ρ_C|≤(43/9)U³+aU²+3eU²
          ≤(43/9)U³+4aU²,

using e≤a. Adding A, S and C gives precisely the claimed leading score and

    |R|≤(2/3)a³+7aU²+(43/9)U³≤5(a+U)³.

The last comparison is coefficientwise. In particular the requested constant 40 is safe, including a=1/2 and U=1/2. There is no asymptotic restriction on m beyond the declared integer m≥2.

## 5. Audit of the author's proof

The original proof remains correct without the stronger auxiliary bounds above:

- Its density bound (7) follows by expanding exp(ea(t))(1+eb(t)); 9e²t²≤(9/2)et² supplies the stated loose constant 8.
- Its separate bound |z|≤e≤1/2 correctly justifies the logarithm expansion; the looser |z|≤10eU by itself would not suffice.
- The four contributions to its equation (10) are bounded by 2U³, 2aU², 4U²(a+U), and 16U³+8eU², respectively.
- Its combined coefficients (68/3)U³+118aU²+(4/3)a³ are covered by 24U³+120aU²+2a³, which is coefficientwise at most 40(a+U)³.
- Every occurrence of e≤a uses the stated k≥1. No empty-skyline extension is silently taken.

No blocking correction was found in the final author result.

## 6. Fixed-count localization and the boundary obstruction

For a deterministic point (x,y), the probability it lies in E equals (1−xy)^n under P0. Under P1 it equals

    [1−F_c(x,y)]^m=(1−xy)^(cm)=(1−xy)^n.

This is an exact equality for fixed route counts, not a Poisson void formula. Tonelli proves the equality of expected weighted lower-set integrals under the two laws. In particular,

    E_j U=H_m/m,
    E_j M1=(H_(m+1)−1)/[m(m+1)],       j=0,1.

The cited count result gives E0 K=H_n≤H_m. Its exact alternative mean also implies E1 K≤H_m directly: for n>1,

    E1 K−H_n=(H_n−1)/(n²−1)≤1/(n+1),

and the n=1 formula (1+ζ(2))/2<3/2 handles the exceptional case. Thus Markov gives

    P_j(K+mU>B)≤2H_m/B.

For B≤m/2 the event automatically excludes K=m and satisfies the expansion hypotheses. The author's fixed-probability and tending-to-one localization statements follow. The phrase O_P((log m)³/m³) is valid in the expressly localized sense used there; it does not make the unconditioned singular likelihood finite or bound its integrated tails.

For the proposed counterfamily k=1, x=1−ε, y=1/2, U→1, and the exact fixed-count likelihood has

    log L=(1/m)log ε+O_m(1)→−∞.

The displayed leading polynomial actually tends to zero for this y. Thus no globally bounded C(k/m+U)³ remainder is possible, even at fixed m. This is an exact obstruction to dropping the window, not evidence against the localized result.

No second moments of this score, likelihood-tail uniform integrability, KL/TV/Hellinger rate, better testing cost, or comparison to the completed count test is proved here. The author's scope guards are appropriate.

## 7. Executable evidence and its limits

`independent_controls.py` was written independently and imports no author code. It checks:

- 468 deterministic admissible skylines at m=2 through 4096, including exact U=1/2, a=1/2 where applicable, very small coordinates, multiple staircase shapes, and exact rational lower-set moment inequalities for r=1,…,4;
- the independent 5-cubic bound and the more detailed remainder envelope at 110-digit working precision;
- density remainder controls through the corner e=t=1/2;
- exact strip mass versus independently integrated lower-staircase mass for three cases;
- fixed-count first-moment integrals and count-mean bounds;
- deliberately incorrect candidates omitting the −k correction or reversing either geometric-term sign, each rejected by the claimed 40-cubic bound at a deterministic m=2²⁰ configuration;
- the invalid-window boundary family ε=10^(−4),10^(−16),10^(−64), whose exact log likelihoods are approximately 2.06718, −0.27534, and −14.05737 for m=8.

All controls passed. The largest observed |R|/(a+U)³ was about 0.553668. This finite maximum is **not** asserted to be a universal optimal constant.

The author controls were copied into `author_replay/` and rerun there, avoiding any write to the source directory. They passed, and their generated `CONTROL_RESULTS.json` was byte-identical to the author's source output. `CONTROL_RUN.log`, `CONTROL_RESULTS.json`, the author replay, and the verification receipt retain the evidence.

These checks are deterministic model arithmetic, not simulations, empirical trials, or certified interval proofs. The written inequalities establish the all-configuration statement. Review acceptance is bound to the stated input hashes and does not extend to future modifications or additional statistical claims.
