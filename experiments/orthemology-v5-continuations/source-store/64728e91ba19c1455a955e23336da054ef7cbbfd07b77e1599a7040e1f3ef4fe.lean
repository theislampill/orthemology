import StatisticalRepair
import RepairObstruction

open scoped BigOperators

namespace Orthemology.Tranche2

/-- Literal all-state weak improvement for the disturbed binary forecast. -/
def BinaryGood (a e q : ℝ) : Prop :=
  q ^ 2 ≤ a * ((1 : ℝ)/2+e)^2 + (1-a)*((1 : ℝ)/2)^2 ∧
  (1-q)^2 ≤ a*((1 : ℝ)/2-e)^2 + (1-a)*((1 : ℝ)/2)^2

theorem binary_symmetric_success_disjoint (e q : ℝ)
    (he0 : 0 < e) (he1 : e ≤ (1 : ℝ)/4) :
    ¬ (BinaryGood (1/2-e) e q ∧ BinaryGood (1/2+e) e q) := by
  rintro ⟨hm,hp⟩
  have ham0 : 0 ≤ (1:ℝ)/2-e := by linarith
  have ham1 : (1:ℝ)/2-e ≤ 1 := by linarith
  have hap0 : 0 ≤ (1:ℝ)/2+e := by linarith
  have hap1 : (1:ℝ)/2+e ≤ 1 := by linarith
  have hbm := RepairObstruction.binary_repair_readout (1/2-e) e q 0
    ham0 ham1 he0.le he1 (by rfl) (by simpa using hm.1) (by simpa using hm.2)
  have hbp := RepairObstruction.binary_repair_readout (1/2+e) e q 0
    hap0 hap1 he0.le he1 (by rfl) (by simpa using hp.1) (by simpa using hp.2)
  have hm' := (abs_le.mp hbm).2
  have hp' := (abs_le.mp hbp).1
  nlinarith [sq_pos_of_pos he0]

noncomputable def repairFailure {ι : Type*} [Fintype ι]
    (p : ι → ℝ) (a e : ℝ) (repair : ι → ℝ) : ℝ := by
  classical
  exact ∑ i, p i * (if BinaryGood a e (repair i) then 0 else 1)

/-- An exact kernel-level bridge from actual score inequalities to the
finite Bernoulli testing obstruction. The repair sees n sample bits. -/
theorem bernoulli_repair_lower_bound (n : ℕ) (e : ℝ)
    (he0 : 0 < e) (he1 : e ≤ (1 : ℝ)/4) (repair : Bits n → ℝ) :
    (1-4*e^2)^n/4 ≤
      max (repairFailure (bernoulliMass n (1/2-e)) (1/2-e) e repair)
          (repairFailure (bernoulliMass n (1/2+e)) (1/2+e) e repair) := by
  classical
  let test : Bits n → ℝ := fun w => if BinaryGood (1/2-e) e (repair w) then 1 else 0
  have ht0 : ∀ w, 0 ≤ test w := by intro w; dsimp [test]; split_ifs <;> norm_num
  have ht1 : ∀ w, test w ≤ 1 := by intro w; dsimp [test]; split_ifs <;> norm_num
  have h := symmetric_bernoulli_test_lower_bound n e he0.le (by linarith) test ht0 ht1
  have hm : errorP (bernoulliMass n (1/2-e)) test =
      repairFailure (bernoulliMass n (1/2-e)) (1/2-e) e repair := by
    unfold errorP repairFailure
    apply Finset.sum_congr rfl
    intro w _
    dsimp [test]
    split_ifs <;> ring
  have hp : errorQ (bernoulliMass n (1/2+e)) test ≤
      repairFailure (bernoulliMass n (1/2+e)) (1/2+e) e repair := by
    unfold errorQ repairFailure
    apply Finset.sum_le_sum
    intro w _
    have hw0 := bernoulliMass_nonneg n (1/2+e) (by linarith) (by linarith) w
    dsimp [test]
    split_ifs with hm hp hp
    · exact False.elim (binary_symmetric_success_disjoint e (repair w) he0 he1 ⟨hm,hp⟩)
    · exact le_rfl
    · exact le_rfl
    · simpa using hw0
  rw [hm] at h
  exact h.trans (max_le_max le_rfl hp)

end Orthemology.Tranche2

open MeasureTheory

namespace Orthemology.Tranche2

theorem measurable_binaryGood (a e : ℝ) : MeasurableSet {q : ℝ | BinaryGood a e q} := by
  change MeasurableSet ({q : ℝ | q^2 ≤ a*(1/2+e)^2+(1-a)*(1/2)^2} ∩
    {q : ℝ | (1-q)^2 ≤ a*(1/2-e)^2+(1-a)*(1/2)^2})
  apply MeasurableSet.inter
  · exact measurableSet_le (measurable_id.pow_const 2) measurable_const
  · exact measurableSet_le ((measurable_const.sub measurable_id).pow_const 2) measurable_const

/-- The actual failure probability for an arbitrary real-valued randomized
repair kernel conditional on the n observed bits. -/
noncomputable def randomizedRepairFailure (n : ℕ) (a e : ℝ)
    (K : Bits n → Measure ℝ) : ℝ :=
  ∑ w, bernoulliMass n a w * (K w).real {q | ¬ BinaryGood a e q}

lemma randomized_acceptance_disjoint (e : ℝ) (he0 : 0 < e) (he1 : e ≤ 1/4)
    (μ : Measure ℝ) [IsProbabilityMeasure μ] :
    μ.real {q | BinaryGood (1/2-e) e q} +
      μ.real {q | BinaryGood (1/2+e) e q} ≤ 1 := by
  have hd : Disjoint {q : ℝ | BinaryGood (1/2-e) e q}
      {q : ℝ | BinaryGood (1/2+e) e q} := by
    rw [Set.disjoint_left]
    intro q hm hp
    exact binary_symmetric_success_disjoint e q he0 he1 ⟨hm,hp⟩
  rw [← measureReal_union hd (measurable_binaryGood (1/2+e) e)]
  exact measureReal_le_one

/-- The finite-sample lower bound includes arbitrary measurable real-valued
output randomization, rather than merely finite random seeds. -/
theorem bernoulli_randomized_repair_lower_bound (n : ℕ) (e : ℝ)
    (he0 : 0 < e) (he1 : e ≤ 1/4)
    (K : Bits n → Measure ℝ) [∀ w, IsProbabilityMeasure (K w)] :
    (1-4*e^2)^n/4 ≤
      max (randomizedRepairFailure n (1/2-e) e K)
          (randomizedRepairFailure n (1/2+e) e K) := by
  let test : Bits n → ℝ := fun w => (K w).real {q | BinaryGood (1/2-e) e q}
  have ht0 : ∀ w, 0 ≤ test w := fun _ => measureReal_nonneg
  have ht1 : ∀ w, test w ≤ 1 := fun _ => measureReal_le_one
  have h := symmetric_bernoulli_test_lower_bound n e he0.le (by linarith) test ht0 ht1
  have hm : errorP (bernoulliMass n (1/2-e)) test =
      randomizedRepairFailure n (1/2-e) e K := by
    unfold errorP randomizedRepairFailure
    apply Finset.sum_congr rfl
    intro w _
    congr 1
    dsimp [test]
    change 1 - (K w).real {q | BinaryGood (1/2-e) e q} =
      (K w).real ({q | BinaryGood (1/2-e) e q}ᶜ)
    rw [measureReal_compl (measurable_binaryGood (1/2-e) e)]
    simp
  have hp : errorQ (bernoulliMass n (1/2+e)) test ≤
      randomizedRepairFailure n (1/2+e) e K := by
    unfold errorQ randomizedRepairFailure
    apply Finset.sum_le_sum
    intro w _
    apply mul_le_mul_of_nonneg_left
    · have hd := randomized_acceptance_disjoint e he0 he1 (K w)
      dsimp [test]
      change (K w).real {q | BinaryGood (1/2-e) e q} ≤
        (K w).real ({q | BinaryGood (1/2+e) e q}ᶜ)
      rw [measureReal_compl (measurable_binaryGood (1/2+e) e)]
      simp only [measureReal_univ_eq_one]
      linarith
    · exact bernoulliMass_nonneg n (1/2+e) (by linarith) (by linarith) w
  rw [hm] at h
  exact h.trans (max_le_max le_rfl hp)

end Orthemology.Tranche2

#print axioms Orthemology.Tranche2.binary_symmetric_success_disjoint
#print axioms Orthemology.Tranche2.bernoulli_repair_lower_bound
#print axioms Orthemology.Tranche2.bernoulli_randomized_repair_lower_bound
#check Orthemology.Tranche2.bernoulli_randomized_repair_lower_bound
