import ContinuumAuditRestoration
import RepairEndpointCells
import Mathlib.MeasureTheory.Integral.Lebesgue.Add
import Mathlib.Analysis.SpecificLimits.Basic

open MeasureTheory Set
open scoped ENNReal BigOperators
open Orthemology.Tranche2
namespace Orthemology.Tranche3
noncomputable section

def constantBits (b : Bool) : (n : ℕ) → Bits n
  | 0 => ()
  | n+1 => (b,constantBits b n)

lemma constantBits_count (b : Bool) (n : ℕ) :
    rationalCount n (constantBits b n)=if b then n else 0 := by
  induction n with
  | zero => cases b <;> rfl
  | succ n ih => cases b <;> simp [constantBits,rationalCount,ih,Nat.add_comm]

lemma constantBits_mass (b : Bool) (n : ℕ) (a : ℝ) :
    bernoulliMass n a (constantBits b n)=(coinMass a b)^n := by
  induction n with
  | zero => simp [bernoulliMass]
  | succ n ih => simp [constantBits,bernoulliMass,ih,pow_succ,mul_comm]

lemma empiricalRepair_constant (b : Bool) (e : ℚ) (n : ℕ) :
    empiricalRepair e n (constantBits b (n+1))=if b then 1/2+e else 1/2 := by
  have hn : (n:ℚ)+1 ≠ 0 := by positivity
  cases b <;> simp [empiricalRepair,empiricalWeight,constantBits_count,hn]

def EmpiricalFailure (a : ℝ) (e : ℚ) (n : ℕ) : Set (ℕ → Bool) :=
  {ω | ¬ LiteralRepairGood a e (empiricalRepair e n (observedPrefix (n+1) ω))}

lemma empiricalFailure_measurable (a : ℝ) (e : ℚ) (n : ℕ) :
    MeasurableSet (EmpiricalFailure a e n) := by
  let E : Set (Bits (n+1)) := {w | ¬ LiteralRepairGood a e (empiricalRepair e n w)}
  exact (Set.toFinite E).measurableSet.preimage (observedPrefix_measurable (n+1))

lemma constant_prefix_failure (a : ℝ) (ha0 : 0<a) (ha1 : a<1)
    (e : ℚ) (he0 : 0<e) (he1 : e≤1/4) (b : Bool) (n : ℕ) :
    {ω | observedPrefix (n+1) ω=constantBits b (n+1)} ⊆ EmpiricalFailure a e n := by
  intro ω hw hg
  have he0' : (0:ℝ)<e := by exact_mod_cast he0
  have he1' : (e:ℝ)≤1/4 := by
    have hh : (e:ℝ)≤((1/4:ℚ):ℝ) := by exact_mod_cast he1
    norm_num at hh ⊢
    exact hh
  rw [hw,empiricalRepair_constant] at hg
  cases b
  · norm_num only [Bool.false_eq_true,if_false,Rat.cast_div,Rat.cast_ofNat] at hg
    have hh := (positive_weight_punctured_cell a e _ ha0 he0' he1' hg).1
    linarith
  · norm_num only [if_true,Rat.cast_add,Rat.cast_div,Rat.cast_ofNat] at hg
    have hh := (below_one_punctured_cell a e _ ha1 he0' he1' hg).2
    linarith

lemma constant_prefix_probability (a : ℝ) (ha0 : 0≤a) (ha1 : a≤1)
    (b : Bool) (n : ℕ) :
    auditSourceLaw a ha0 ha1 {ω | observedPrefix n ω=constantBits b n}=
      ENNReal.ofReal ((coinMass a b)^n) := by
  have hh := auditSource_prefix_mass a ha0 ha1 n (constantBits b n)
  rw [Measure.map_apply (observedPrefix_measurable n) (measurableSet_singleton _)] at hh
  simpa only [mem_singleton_iff,preimage_setOf_eq,constantBits_mass] using hh

/-- Every all-zero and all-one acquired prefix produces an incorrect literal
repair at an interior weight, despite almost-sure eventual restoration. -/
theorem empirical_failure_probability_lower (a : ℝ) (ha0 : 0<a) (ha1 : a<1)
    (e : ℚ) (he0 : 0<e) (he1 : e≤1/4) (n : ℕ) :
    ENNReal.ofReal ((1-a)^(n+1)) + ENNReal.ofReal (a^(n+1)) ≤
      auditSourceLaw a ha0.le ha1.le (EmpiricalFailure a e n) := by
  let Z : Set (ℕ → Bool) := {ω | observedPrefix (n+1) ω=constantBits false (n+1)}
  let O : Set (ℕ → Bool) := {ω | observedPrefix (n+1) ω=constantBits true (n+1)}
  have hm : MeasurableSet O := (measurableSet_singleton _).preimage (observedPrefix_measurable (n+1))
  have hd : Disjoint Z O := by
    apply Set.disjoint_left.mpr
    intro ω hz ho
    have hh := hz.symm.trans ho
    have := congrArg Prod.fst hh
    simp [constantBits] at this
  have hs : Z ∪ O ⊆ EmpiricalFailure a e n :=
    union_subset (constant_prefix_failure a ha0 ha1 e he0 he1 false n)
      (constant_prefix_failure a ha0 ha1 e he0 he1 true n)
  have hh := measure_mono hs (μ := auditSourceLaw a ha0.le ha1.le)
  rw [measure_union hd hm] at hh
  simpa only [Z,O,constant_prefix_probability,coinMass,if_false,if_true] using hh

/-- The same always-emitting policy has a nonuniform expected error cost.
The two geometric terms diverge near the respective degenerate endpoints. -/
theorem empirical_expected_failure_lower (a : ℝ) (ha0 : 0<a) (ha1 : a<1)
    (e : ℚ) (he0 : 0<e) (he1 : e≤1/4) :
    ENNReal.ofReal (1-a) * (1-ENNReal.ofReal (1-a))⁻¹ +
      ENNReal.ofReal a * (1-ENNReal.ofReal a)⁻¹ ≤
      ∫⁻ ω, ∑' n, (EmpiricalFailure a e n).indicator 1 ω
        ∂auditSourceLaw a ha0.le ha1.le := by
  rw [lintegral_tsum (f := fun n => (EmpiricalFailure a e n).indicator
      (1 : (ℕ → Bool) → ℝ≥0∞)) (fun n =>
    ((show Measurable (1 : (ℕ → Bool) → ℝ≥0∞) from measurable_const).indicator
      (empiricalFailure_measurable a e n)).aemeasurable)]
  simp_rw [lintegral_indicator_one (empiricalFailure_measurable a e _)]
  have hh := ENNReal.tsum_le_tsum (fun n =>
    empirical_failure_probability_lower a ha0 ha1 e he0 he1 n)
  simp_rw [ENNReal.ofReal_pow (by linarith : 0≤1-a),ENNReal.ofReal_pow ha0.le] at hh
  rw [ENNReal.tsum_add,ENNReal.tsum_geometric_add_one,ENNReal.tsum_geometric_add_one] at hh
  exact hh


end
end Orthemology.Tranche3
#print axioms Orthemology.Tranche3.empirical_failure_probability_lower

#print axioms Orthemology.Tranche3.empirical_expected_failure_lower
