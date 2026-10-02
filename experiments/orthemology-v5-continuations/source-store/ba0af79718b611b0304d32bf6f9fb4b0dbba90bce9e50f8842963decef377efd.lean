import CriticalZero
import FiniteLPCertificates

noncomputable section
open Set CriticalZero
open scoped BigOperators

namespace IndependentBoundaryAudit

def quadGain (a b eps : ℝ) : ℝ :=
  ((1/2+eps-a)^2+(1/2-a)^2)/2-(1/2+eps/2+eps^2*b-a)^2

def nonlinearGain (a b eps : ℝ) : ℝ :=
  CriticalZero.div a (1/2+eps)+CriticalZero.div a (1/2)-
    2*CriticalZero.div a (1/2+eps/2+eps^2*b)

def actualGain (b eps : ℝ) : Fin 4 → ℝ :=
  ![quadGain 0 b eps,quadGain 1 b eps,nonlinearGain 0 b eps,nonlinearGain 1 b eps]

def remainder (b eps : ℝ) : Fin 4 → ℝ :=
  ![-b-eps*b^2,-b-eps*b^2,fRem 0 b eps,fRem 1 b eps]

/-- The same four LP rows are exact coefficients of the actual four score gains. -/
theorem actual_four_rows (b eps : ℝ) (i : Fin 4) :
    actualGain b eps i = eps^2*(leading b i+eps*remainder b eps i) := by
  fin_cases i <;>
    simp [actualGain,remainder,leading,quadGain,nonlinearGain,CriticalZero.div,psi,dpsi,fRem] <;> ring

def constants : Fin 4 → ℝ := ![1/4,1/4,3/4,-1/4]
def rows : Fin 4 → (ℝ →ₗ[ℝ] ℝ) :=
  ![LinearMap.id, -LinearMap.id, LinearMap.id, -LinearMap.id]
def weights : Fin 4 → ℝ := ![1/2,0,0,1/2]

lemma row_binding (b : ℝ) (i : Fin 4) :
    FiniteLPCertificates.margin constants rows b i = leading b i := by
  fin_cases i <;> simp [FiniteLPCertificates.margin,constants,rows,leading] <;> ring

lemma weight_nonneg (i : Fin 4) : 0 ≤ weights i := by
  fin_cases i <;> norm_num [weights]
lemma weight_mass : ∑ i, weights i = 1 := by norm_num [weights,Fin.sum_univ_succ]
lemma weight_balance (b : ℝ) : ∑ i, weights i*rows i b = 0 := by
  simp [weights,rows,Fin.sum_univ_succ]
lemma dual_objective : ∑ i, weights i*constants i = 0 := by
  norm_num [weights,constants,Fin.sum_univ_succ]

/-- Explicit dual witness checks the critical upper bound through the generic library. -/
theorem critical_generic_dual_bound (b tau : ℝ) (h : ∀ i, tau ≤ leading b i) : tau ≤ 0 := by
  have hh := FiniteLPCertificates.dual_bound constants rows weights weight_nonneg
    weight_mass weight_balance b tau (by simpa only [row_binding] using h)
  simpa only [dual_objective] using hh

theorem critical_generic_no_strict : ¬ ∃ b : ℝ, ∀ i, 0 < leading b i := by
  have hh := FiniteLPCertificates.zero_dual_excludes_strict constants rows weights
    weight_nonneg weight_mass weight_balance (le_of_eq dual_objective)
  simpa only [row_binding] using hh

/-- The zero optimum and nonlinear impossibility belong to exactly the same data. -/
theorem bound_zero_but_no_exact :
    (∀ i : Fin 4, 0 ≤ leading (1/4) i) ∧
    (∀ b tau : ℝ, (∀ i : Fin 4, tau ≤ leading b i) → tau ≤ 0) ∧
    (∀ eps : ℝ, 0 < eps → eps ≤ 1/100 →
      ¬ ∃ q ∈ Icc (0:ℝ) 1, q^2 ≤ baselineG eps ∧ loss q ≤ baselineF eps) := by
  exact ⟨second_order_optimum_zero.1,critical_generic_dual_bound,no_exact_repair⟩

/-- Curvature and its slope at the context agree with the claimed critical data. -/
theorem critical_curvature_value : curvature (1/2) = 1 := by norm_num [curvature]
theorem critical_curvature_slope : HasDerivAt curvature 4 (1/2) := by
  have h := (hasDerivAt_id (1/2 : ℝ)).sub_const (1/2)
  convert ((hasDerivAt_const (1/2 : ℝ) 1).add (h.const_mul 4)).add ((h.pow 2).const_mul 12) using 1 <;>
    simp [curvature] <;> ring

#check @CriticalZero.no_exact_repair
#check @CriticalZero.actual_second_order_F
#check @CriticalZero.actual_second_order_G
#check @CriticalZero.second_order_optimum_zero
#check @FiniteLPCertificates.dual_bound
#check @FiniteLPCertificates.negative_dual_excludes_weak
#check @FiniteLPCertificates.zero_dual_excludes_strict
#check @actual_four_rows
#check @critical_generic_dual_bound
#check @critical_generic_no_strict
#check @bound_zero_but_no_exact
#print axioms actual_four_rows
#print axioms critical_generic_dual_bound
#print axioms critical_generic_no_strict
#print axioms bound_zero_but_no_exact
#print axioms critical_curvature_slope
#print actualGain
#print constants
#print rows
#print weights
end IndependentBoundaryAudit
