import ExistenceAwareHistory
namespace IndependentExistenceControls
open Orthemology.Tranche3.ExistenceAwareHistory
noncomputable section

theorem no_bound_no_uniqueness :
    HalfHistory 0 (fun n => (2:ℝ)^n) ∧ (fun n => (2:ℝ)^n) ≠ (fun _ => (0:ℝ)) := by
  simpa using nonconstant_unbounded_control 0

theorem bounded_nonhistory :
    (∀ n : ℕ, |(if n=0 then (1:ℝ) else 0)| ≤ 1) ∧
      ¬ HalfHistory 0 (fun n => if n=0 then (1:ℝ) else 0) := by
  constructor
  · intro n; split_ifs <;> norm_num
  · intro h
    have := h 0
    norm_num at this

theorem finite_prefix_bound_does_not_force_constant :
    HalfHistory 0 (fun n => (2:ℝ)^n / 8) ∧
      (∀ n < 4, |(2:ℝ)^n / 8| ≤ 1) ∧ (2:ℝ)^0 / 8 ≠ 0 := by
  refine ⟨?_,?_,by norm_num⟩
  · simpa [mul_div_assoc] using unbounded_family 0 (1/8)
  · intro n hn
    rw [abs_of_nonneg (by positivity)]
    interval_cases n <;> norm_num

theorem absent_vacuous_even_negative_bound :
    ConditionallyBounded 0 (-1) (fun _ => none) := by simp [ConditionallyBounded]

theorem classification_does_not_need_nonnegative_bound (c M : ℝ) (h : ℕ → Option ℝ)
    (hr : LiftedHistory c h) (hb : ConditionallyBounded c M h) :
    (∀ n, h n=none) ∨ (∀ n, h n=some c) := by
  by_cases hm : 0≤M
  · exact bounded_lifted_classification c M h hr hm hb
  · left
    intro n
    cases hh : h n with
    | none => rfl
    | some x =>
      have hx:=hb n x hh
      have hp:=abs_nonneg (x-c)
      linarith

theorem present_zero_is_not_absent : (some (0:ℝ) : Option ℝ) ≠ none := by simp

theorem alternating_existence_violates_lift :
    ¬ LiftedHistory 0 (fun n => if n=0 then none else some 0) := by
  intro h
  have := h 0
  simp [liftHalf] at this

theorem absent_profile_not_derived_actuality :
    LiftedHistory 3 (fun _ => some 3) ∧
      ¬ (∀ _n : ℕ, (some (3:ℝ) : Option ℝ)=none) := by
  exact ⟨(present_history 3).1,by simp⟩

theorem preserving_only_empty_allows_unique :
    ∃! h : Bool, (fun _ : Bool => false) h = h := by
  refine ⟨false,rfl,?_⟩
  intro y hy
  exact hy.symm

theorem preserving_only_active_allows_unique :
    ∃! h : Bool, (fun _ : Bool => true) h = h := by
  refine ⟨true,rfl,?_⟩
  intro y hy
  exact hy.symm

theorem collapsed_names_allow_unique :
    (fun _ : Unit => ()) ()=() ∧ ∃! h : Unit, (fun _ : Unit => ()) h=h := by simp
end
end IndependentExistenceControls
