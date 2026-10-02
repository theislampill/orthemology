import AtomicPattern

open Set MeasureTheory
namespace OrthemologyMeasure

instance lossStageMeasurableSpace : MeasurableSpace (Option ℕ) := ⊤
instance lossClassMeasurableSpace : MeasurableSpace (Option (Option ℕ)) := ⊤


/-- `none` means no finite loss; `some n` is the first false coordinate. -/
noncomputable def firstLoss (b : ℕ → Bool) : Option ℕ := by
  classical
  exact if h : ∃ n, b n = false then some (Nat.find h) else none

theorem firstLoss_none (b : ℕ → Bool) :
    firstLoss b = none ↔ ∀ n, b n ≠ false := by
  classical
  simp [firstLoss]

theorem firstLoss_some (b : ℕ → Bool) (n : ℕ) :
    firstLoss b = some n ↔ b n = false ∧ ∀ k < n, b k ≠ false := by
  classical
  unfold firstLoss
  split
  next h => simp [Nat.find_eq_iff]
  next h =>
    constructor
    · intro he; contradiction
    · intro he; exact False.elim (h ⟨n, he.1⟩)

theorem firstLoss_measurable : Measurable firstLoss := by
  apply measurable_to_countable'
  intro x
  cases x with
  | none =>
      have he : firstLoss ⁻¹' {none} = ⋂ n, {b : ℕ → Bool | b n ≠ false} := by
        ext b
        simp [firstLoss_none]
      rw [he]
      apply MeasurableSet.iInter
      intro n
      exact ((measurable_pi_apply n : Measurable (fun b : ℕ → Bool => b n)) (measurableSet_singleton false)).compl
  | some n =>
      have he : firstLoss ⁻¹' {some n} = {b : ℕ → Bool | b n = false} ∩
          ⋂ k, ⋂ (_ : k < n), {b : ℕ → Bool | b k ≠ false} := by
        ext b
        simp [firstLoss_some]
      rw [he]
      apply MeasurableSet.inter ((measurable_pi_apply n : Measurable (fun b : ℕ → Bool => b n)) (measurableSet_singleton false))
      exact MeasurableSet.iInter fun k => MeasurableSet.iInter fun _ =>
        ((measurable_pi_apply k : Measurable (fun b : ℕ → Bool => b k)) (measurableSet_singleton false)).compl

/-- Full atom takes precedence; otherwise record the first finite loss or infinity.
Output none = retained full atom, some none = infinite residual,
some (some n) = initial/finite-stage loss. -/
noncomputable def lossClass (b : Option ℕ → Bool) : Option (Option ℕ) :=
  if b none = true then none else some (firstLoss fun n => b (some n))

theorem lossClass_measurable : Measurable lossClass := by
  classical
  apply Measurable.ite
  · exact (measurable_pi_apply none : Measurable (fun b : Option ℕ → Bool => b none)) (measurableSet_singleton true)
  · exact measurable_const
  · exact (measurable_from_top (f := (some : Option ℕ → Option (Option ℕ)))).comp (firstLoss_measurable.comp
      (measurable_pi_lambda _ fun n => measurable_pi_apply (some n)))

end OrthemologyMeasure
#print axioms OrthemologyMeasure.firstLoss_measurable
#print axioms OrthemologyMeasure.lossClass_measurable
