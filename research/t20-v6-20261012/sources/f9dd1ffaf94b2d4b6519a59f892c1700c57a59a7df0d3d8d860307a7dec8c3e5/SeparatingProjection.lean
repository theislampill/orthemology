import MomentRecovery
import Mathlib.Algebra.Polynomial.Roots

noncomputable section

open scoped BigOperators

namespace FiniteMoment

variable {K : Type*} [Field K] {N d : ℕ}

/-- Encode a finite vector by its coordinate polynomial. -/
def coordinatePolynomial (x : Fin d → K) : Polynomial K :=
  ∑ j : Fin d, Polynomial.monomial j.val (x j)

theorem coordinatePolynomial_coeff (x : Fin d → K) (j : Fin d) :
    (coordinatePolynomial x).coeff j.val = x j := by
  classical
  simp [coordinatePolynomial, Polynomial.finset_sum_coeff,
    Polynomial.coeff_monomial, Fin.val_inj]

theorem coordinatePolynomial_injective :
    Function.Injective (coordinatePolynomial (K := K) (d := d)) := by
  intro x y h
  funext j
  have hc := congrArg (fun p : Polynomial K => p.coeff j.val) h
  simpa only [coordinatePolynomial_coeff] using hc

theorem coordinatePolynomial_eval (x : Fin d → K) (t : K) :
    (coordinatePolynomial x).eval t = ∑ j : Fin d, t ^ j.val * x j := by
  simp [coordinatePolynomial, Polynomial.eval_finset_sum, Polynomial.eval_monomial, mul_comm]

/-- A single scalar linear projection, represented in coordinates. -/
def projection (v x : Fin d → K) : K := ∑ j, v j * x j

/-- The coordinate formula is a genuine K-linear functional. -/
def projectionLinearMap (v : Fin d → K) : (Fin d → K) →ₗ[K] K where
  toFun := projection v
  map_add' x y := by simp [projection, mul_add, Finset.sum_add_distrib]
  map_smul' c x := by
    simp [projection, Finset.mul_sum, mul_left_comm]

/-- Every finite family of distinct vectors over an infinite field has a
separating direction on the polynomial curve (1,t,...,t^(d-1)). -/
theorem exists_separating_parameter [Infinite K] (x : Fin N → Fin d → K)
    (hx : Function.Injective x) :
    ∃ t : K, Function.Injective (fun i => projection (fun j => t ^ j.val) (x i)) := by
  classical
  let pairs : Finset (Fin N × Fin N) := Finset.univ.filter (fun ij => ij.1 ≠ ij.2)
  let p : Polynomial K := ∏ ij ∈ pairs,
    (coordinatePolynomial (x ij.1) - coordinatePolynomial (x ij.2))
  have hp : p ≠ 0 := by
    apply Finset.prod_ne_zero_iff.mpr
    intro ij hij
    apply sub_ne_zero.mpr
    intro heq
    exact (Finset.mem_filter.mp hij).2 (hx (coordinatePolynomial_injective heq))
  have ht : ∃ t : K, p.eval t ≠ 0 := by
    by_contra hn
    push_neg at hn
    exact hp (Polynomial.zero_of_eval_zero p hn)
  obtain ⟨t, ht⟩ := ht
  refine ⟨t, ?_⟩
  intro i j hij
  by_contra hne
  have hpair : (i, j) ∈ pairs := by simp [pairs, hne]
  have hfactor : (coordinatePolynomial (x i) - coordinatePolynomial (x j)).eval t = 0 := by
    simpa [Polynomial.eval_sub, coordinatePolynomial_eval, projection, sub_eq_zero] using hij
  apply ht
  rw [show p = ∏ ij ∈ pairs,
    (coordinatePolynomial (x ij.1) - coordinatePolynomial (x ij.2)) from rfl,
    Polynomial.eval_prod]
  exact Finset.prod_eq_zero hpair hfactor

/-- Existence has no nonempty-support or positive-dimension premise. -/
theorem exists_separating_projection [Infinite K] (x : Fin N → Fin d → K)
    (hx : Function.Injective x) :
    ∃ v : Fin d → K, Function.Injective (fun i => ∑ j, v j * x i j) := by
  obtain ⟨t, ht⟩ := exists_separating_parameter x hx
  exact ⟨fun j => t ^ j.val, ht⟩

/-- The separating projection may equivalently be returned as a bundled
scalar linear functional, with linearity proved in projectionLinearMap. -/
theorem exists_separating_linearMap [Infinite K] (x : Fin N → Fin d → K)
    (hx : Function.Injective x) :
    ∃ f : (Fin d → K) →ₗ[K] K, Function.Injective (fun i => f (x i)) := by
  obtain ⟨v, hv⟩ := exists_separating_projection x hx
  exact ⟨projectionLinearMap v, hv⟩

/-- A support-dependent direction with explicit reconstruction of arbitrary
weights from its degrees 0 through N-1. -/
theorem exists_projection_recovery [Infinite K] (x : Fin N → Fin d → K)
    (hx : Function.Injective x) :
    ∃ v : Fin d → K,
      Function.Injective (fun i => projection v (x i)) ∧
      ∀ w : Fin N → K,
        recover (fun i => projection v (x i))
          (record (fun i => projection v (x i)) w) = w := by
  obtain ⟨v, hv⟩ := exists_separating_projection x hx
  exact ⟨v, hv, fun w => recover_record _ hv w⟩

/-- The same chosen direction makes its retained finite moment tuple injective
in the weights. No separating-direction premise remains. -/
theorem exists_injective_projected_record [Infinite K] (x : Fin N → Fin d → K)
    (hx : Function.Injective x) :
    ∃ v : Fin d → K, Function.Injective (record (fun i => projection v (x i))) := by
  obtain ⟨v, hv⟩ := exists_separating_projection x hx
  exact ⟨v, record_injective _ hv⟩

/-- One support-dependent scalar projection reconstructs every fixed
vector-valued observable by the inherited explicit coefficients. -/
theorem exists_projected_observable_reconstruction [Infinite K]
    {E : Type*} [AddCommGroup E] [Module K E]
    (x : Fin N → Fin d → K) (hx : Function.Injective x) :
    ∃ v : Fin d → K,
      Function.Injective (fun i => projection v (x i)) ∧
      ∀ (w : Fin N → K) (f : Fin N → E),
        ∑ i, w i • f i =
          ∑ r : Fin N, moment (fun i => projection v (x i)) w r.val •
            (∑ i, recoveryCoefficient (fun i => projection v (x i)) i r • f i) := by
  obtain ⟨v, hv⟩ := exists_separating_projection x hx
  exact ⟨v, hv, fun w f => vector_observable_reconstruction _ hv w f⟩

end FiniteMoment

