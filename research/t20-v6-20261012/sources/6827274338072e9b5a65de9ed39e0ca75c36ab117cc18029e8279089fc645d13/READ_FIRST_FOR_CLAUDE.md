# Orthemology — exact theorem sources for Claude's mathematical review

9 October 2026. Reader packet copied verbatim from available owner research archives. No modification to GitHub, formal theorem statement or historical research record. This packaging is not new mathematical proof, fresh Lean compilation, external peer review, or an originality certification.

**Recommended reading order:**
1. `hessian/GENERAL_ADMISSIBILITY.md` §§1, 6–7; `hessian/SCALAR_CONTINUATION_IFF.md` §3 and §5a.
2. `identification/README.md`, `identification/CalibratedPanels.lean`, `Calibration.lean`, `HitTransform.lean`.
3. `continuation/continuation_complete_orthing_full.md`, Theorem 2 §§5–6, especially part (e).
4. `nonseparable/RESULT.md`, Theorems 1 and Propositions 2–3 and §7; see its internal review and targeted prior-art note.

## A. Original Hessian classification — exact scoped theorem

Inherited score assumptions: finitely many coordinate generators `f_i`, continuous on `[0,1]`, twice differentiable on `(0,1)` in the declared derivative-witness sense, with continuous strictly positive curvature `h_i=f_i''`. On the open cube `U=(0,1)^n`, set

```
F(b) = Σ_i f_i(b_i),      z = Σ_i b_i,
q_i(x) = 1/h_i(x),        V_i(b) = (1−z)q_i(b_i).
```

For `n ≥ 2`, original-clock **scalar projected-velocity closure**, namely existence of a function `R` such that `dz_b[V(b)] = R(z(b))` on every point of the full cube, holds iff the reciprocal curvatures have a common affine slope:

```
q_i(x) = a*x + c_i,   shared a, each c_i,
q_i(x)>0 on (0,1),   R(z)=(1−z)(a*z + Σ_i c_i).
```

This is a statement about the **same original clock and the same scalar output**, not about all individual trajectories' boundary exits or all DAEE corrections.

For `n ≥ 3`, **all-start forward interior safety** for the canonical field holds iff `lim_(x↓0) f_i'(x) = −∞` for *every* coordinate. Joining both classifications yields exactly

```
q_i(x)=a*x (shared a>0),
f_i(x)=(x log x−x)/a + beta_i*x + gamma_i
```

(equivalent to `x log x/a` up to affine terms). The resulting original-clock flow is radial: `b_i(t)=b_i(0)*lambda(t)` and `z'=a*z*(1−z)`. For `n=2` the all-start safety classification has an exception. The normalized-clock field `V/Σq_i` gives `dz/dtau=1−z` for every score family, but its change of clock is not free when time or stopping behaviour matters. Reviewed written proof and exact controls, **not** newly Lean-verified analytic ODE theorems.

The meaning of `z` is the **coherence sum**. The claim that this is a desirable sufficient statistic for a particular noetic application needs an independently justified future-query/clock contract; it is not a universal normative requirement. The classic local-proper-score theorem is not identical in hypotheses.

## B. An important subsequent Hessian development — nonseparable family

The earlier entropy uniqueness is **only for the separable generator / fixed-field classification**. Later T20 work (`nonseparable/RESULT.md`) establishes a larger family on the **positive cone** `C=R_{++}^n`. For `s=Σb_i`, `p=b/s`, `Δ°={p>0:Σp_i=1}`, and `F:C→R` strictly convex and `C¹`, **first-argument Bregman projection** onto the simplex equals ordinary normalization for every `b` iff

```
F(s*p) = s*f(p) + a(s),
f = F|_{Δ°}, a(1)=0.
```

For a suitable `C²` potential with positive-definite Hessians on tangent simplex directions and `a''(s)>0`, the full Hessian metric is positive definite and canonical gradient correction is radial:

```
H_F(s*p)^(-1) * 1 = p/a''(s),
db/dt = −(s−1)*p/a''(s),  dp/dt=0,
ds/dt = −(s−1)/a''(s).
```

An explicit **non-entropy/Brier** example is

```
F_0(b)=||b||²/(2 Σ b_i) + (Σ b_i)²/2.
```

It is nonseparable, has positive-definite full Hessian, preserves coherent Brier divergence and gives normalization by the geometric repair. This is written and internally reviewed mathematical research with finite exact tests; its full general analytic statements were **not** claimed Lean-certified. The note identifies classical scaled-Bregman/perspective ancestry (Nock–Menon–Ong, 2016). This materially changes the scope of any argument that 'radial repair forces entropy': that implication needs separability or additional assumptions.

## C. Exact T20 route-identification theorem (kernel-checked at inherited scope)

Let `E` be an **arbitrary finite type of effects**. Let `H` and `K` each consist of **five** histograms `a,b,c,d,e : Finset E → Nat`, each zero at `∅`. For `U ⊆ E`, define

```
hit_f(U)=Σ_{T subset E, T ∩ U ≠ ∅} f(T).
```

Define **three families of exact rational endpoint observations**, each evaluated for **every nonempty U**:

```
A_H(U)  = (1/2)^(hit_a(U)+hit_d(U))
B_H(U)  = (2/3)^(hit_b(U)+hit_e(U))
AB_H(U) = (1/2)^hit_a(U) * (2/3)^hit_b(U) * (5/6)^hit_c(U)
```

The `CalibratedIdentification.calibrated_panels_identify` theorem in `CalibratedPanels.lean` states

```
(∀ U nonempty, A_H(U)=A_K(U) ∧ B_H(U)=B_K(U) ∧ AB_H(U)=AB_K(U)) → H=K.
```

No upper bound is placed on each natural-number multiplicity, but **E itself is finite**. These are **three profile-indexed complete observation families**, not just three independent scalar observations regardless of effect-set size. The implementation uses rational unique-factorization/prime valuations to invert the calibrated product code, followed by finite Boolean-lattice hit-transform inversion. Original preserved records report Lean 4.19 checking under standard axioms, with failure mutation controls. This copy alone is not a fresh build, and the imports/dependencies need the original pinned environment.

These are **mathematical identification guarantees inside a specified algebraic observational model**. They do not establish that physical causal routes are identifiable from finite noisy samples, that actuators achieve the specified calibrations, that histories possess independent multiplicities, or that route labels equal numerical causal identity. Later noise-aware work has additional assumptions/bounds, not supplied in this short packet.

## D. Continuation Theorem 2 and the continuity question

The paper's own Theorem 2(e) **explicitly** assumes continuous encoders `E:Δ(X)→R^d` with exact recovery for **all laws** over a fixed finite hidden domain `X`. For `r_h=dim(C_h)`, it proves least such continuous dimension `d_min=r_h−1`; its lower bound uses **invariance of domain** on an `(r_h−1)`-dimensional probability simplex. Arbitrarily discontinuous encoders are excluded. The paper cites predictive-state representations, observable invariant spaces, and reward-PSRs as prior work and **does not present general PSR/Hankel rank machinery as newly invented**.

## E. Concrete questions for an independent critic

1. Does the Hessian all-start admissibility plus original-clock scalar-projection iff follow as an exact special case of a located theorem with **the same hypotheses**, or is it a new scoped synthesis of classical lemmas?
2. Is `z` (rather than radiality, source validity, full state, or STOP behaviour) a justified future-query contract in any targeted noetic application? Try a counterexample.
3. Does the nonseparable perspective-generator classifier admit a known **equivalent converse**, not merely the inherited perspective-divergence identity?
4. Which parts of the finite-continuation theorem match PSR/Hankel-rank results exactly, and which exact horizon-specific or information-defect consequences add something independently useful?
5. For calibrated route identification, separate number-theoretic code uniqueness and Boolean-lattice inversion from a justified observation process. Consider signal precision, robustness, adaptive rates, and existing system-identification prior art.

**Status discipline:** Source files below are unchanged copies. Mathematical reviewers in the archives are internal AI reviewers; the statement of a Lean kernel build is inherited from recorded prior runs and not independently repeated by this packaging. Neither application validity nor literature novelty is certified by the supplied packet.
