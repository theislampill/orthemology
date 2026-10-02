import MealyHitting

namespace Orthemology.Frontier.MealyMeasure
open Set MeasureTheory Filter
open scoped ENNReal Topology BigOperators
open P02A2.Q8Measure

variable {S : Type*}

def EventuallyPeriodic (y : Cantor) : Prop :=
  ∃ a p : ℕ, 0 < p ∧ ∀ k, y (a+k+p) = y (a+k)

/-- Even without D, a finite machine driven forever by one constant input is eventually periodic. -/
theorem constant_input_eventually_periodic [Finite S] (M : Mealy S) (s : S) :
    EventuallyPeriodic (output M s (fun _ => false)) := by
  let x : Cantor := fun _ => false
  obtain ⟨a, b, hab, he⟩ := Finite.exists_ne_map_eq_of_infinite (fun n => state M s x n)
  have hrep : ∃ a b, a < b ∧ state M s x a = state M s x b := by
    rcases lt_or_gt_of_ne hab with h | h
    · exact ⟨a, b, h, he⟩
    · exact ⟨b, a, h, he.symm⟩
  obtain ⟨a, b, hab, he⟩ := hrep
  refine ⟨a, b-a, Nat.sub_pos_of_lt hab, ?_⟩
  intro k
  have hs : state M s x (a+k) = state M s x (b+k) := by
    rw [state_add, state_add, he]
    rfl
  have hn : a+k+(b-a) = b+k := by omega
  change M.out (state M s x (a+k+(b-a))) false = M.out (state M s x (a+k)) false
  rw [hn, hs]

/-- The unique output from each state in D is ultimately periodic. -/
theorem deterministic_output_eventually_periodic [Finite S] (M : Mealy S) (s : S)
    (hs : M.infiniteRel s s) (x : Cantor) : EventuallyPeriodic (output M s x) := by
  rw [deterministic_output M s hs x (fun _ => false)]
  exact constant_input_eventually_periodic M s

/-- Every genuinely positive singleton in the infinite output law is ultimately periodic. -/
theorem positive_output_eventually_periodic [Finite S] [Nonempty S]
    (M : Mealy S) (s : S) (y : Cantor) (hy : y ∈ P02A2.positive (law M s)) :
    EventuallyPeriodic y := by
  obtain ⟨x, rfl, n, hn⟩ := (positive_iff_hitting_prefix M s y).mp hy
  obtain ⟨a, p, hp, hperiod⟩ := deterministic_output_eventually_periodic M
    (state M s x n) hn (shift n x)
  refine ⟨n+a, p, hp, ?_⟩
  intro k
  have h := hperiod k
  have hs := output_shift M s x n
  have hleft := congrFun hs (a+k+p)
  have hright := congrFun hs (a+k)
  simpa [shift, Nat.add_assoc] using hleft.trans (h.trans hright.symm)

end Orthemology.Frontier.MealyMeasure
