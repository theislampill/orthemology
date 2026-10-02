import PERRefinement
import Mathlib.Logic.Equiv.Sum

/-! Exact identification of the checked doubled-state potential with the original
`2 * (m - |domain|) + number_of_active_equivalence_classes` formula. -/

namespace Orthemology.Frontier.PER
variable {S : Type*}

abbrev Active (R : PER S) := {s : S // R.rel s s}
abbrev Inactive (R : PER S) := {s : S // ¬ R.rel s s}

def activeSetoid (R : PER S) : Setoid R.Active where
  r s t := R.rel s.val t.val
  iseqv := ⟨fun s => s.property, fun h => R.symm h, fun h₁ h₂ => R.trans h₁ h₂⟩

noncomputable def domainCount (R : PER S) : ℕ := Nat.card R.Active
noncomputable def activeClassCount (R : PER S) : ℕ := Nat.card (Quotient R.activeSetoid)

noncomputable def classifyRep (R : PER S) (x : S × Bool) :
    Quotient R.activeSetoid ⊕ (R.Inactive × Bool) := by
  classical
  exact if hx : R.rel x.1 x.1 then
    Sum.inl (Quotient.mk _ ⟨x.1, hx⟩) else Sum.inr (⟨x.1, hx⟩, x.2)

theorem classifyRep_sound (R : PER S) (x y : S × Bool)
    (h : R.completion.r x y) : R.classifyRep x = R.classifyRep y := by
  classical
  rcases h with rfl | h
  · rfl
  · have hx := R.trans h (R.symm h)
    have hy := R.trans (R.symm h) h
    simp only [classifyRep, dif_pos hx, dif_pos hy]
    exact congrArg Sum.inl (Quotient.sound h)

noncomputable def classify (R : PER S) :
    Quotient R.completion → Quotient R.activeSetoid ⊕ (R.Inactive × Bool) :=
  Quotient.lift R.classifyRep (R.classifyRep_sound)

noncomputable def reassemble (R : PER S) :
    Quotient R.activeSetoid ⊕ (R.Inactive × Bool) → Quotient R.completion :=
  Sum.elim
    (Quotient.lift (fun s : R.Active => Quotient.mk R.completion (s.val, false))
      (fun _ _ h => Quotient.sound (Or.inr h)))
    (fun x => Quotient.mk R.completion (x.1.val, x.2))

theorem reassemble_classify (R : PER S) (q : Quotient R.completion) :
    R.reassemble (R.classify q) = q := by
  classical
  refine Quotient.inductionOn q ?_
  intro x
  by_cases hx : R.rel x.1 x.1
  · simp only [classify, Quotient.lift_mk, classifyRep, dif_pos hx, reassemble]
    exact Quotient.sound (Or.inr hx)
  · simp [classify, classifyRep, hx, reassemble]

theorem classify_reassemble (R : PER S)
    (q : Quotient R.activeSetoid ⊕ (R.Inactive × Bool)) :
    R.classify (R.reassemble q) = q := by
  classical
  cases q with
  | inl q =>
    refine Quotient.inductionOn q ?_
    intro a
    simp [classify, classifyRep, reassemble, a.property]
  | inr q =>
    rcases q with ⟨a, b⟩
    simp [classify, classifyRep, reassemble, a.property]

noncomputable def completionEquiv (R : PER S) :
    Quotient R.completion ≃ Quotient R.activeSetoid ⊕ (R.Inactive × Bool) where
  toFun := R.classify
  invFun := R.reassemble
  left_inv := R.reassemble_classify
  right_inv := R.classify_reassemble

/-- Exact source-paper potential identity, including empty active domains. -/
theorem potential_formula [Finite S] (R : PER S) :
    R.potential = 2 * (Nat.card S - R.domainCount) + R.activeClassCount := by
  classical
  have hsplit : Nat.card R.Active + Nat.card R.Inactive = Nat.card S := by
    rw [← Nat.card_sum]
    exact Nat.card_congr (Equiv.sumCompl (fun s => R.rel s s))
  have hinactive : Nat.card R.Inactive = Nat.card S - Nat.card R.Active := by omega
  have hb : Nat.card Bool = 2 := by simp [Nat.card_eq_fintype_card]
  rw [potential, Nat.card_congr R.completionEquiv, Nat.card_sum, Nat.card_prod, hb,
    hinactive]
  simp [domainCount, activeClassCount, Nat.mul_comm, Nat.add_comm]

end Orthemology.Frontier.PER
