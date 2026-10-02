import TargetMass

namespace Orthemology.Frontier.MealyMeasure
open Set MeasureTheory Filter
open scoped ENNReal Topology BigOperators

variable {S T : Type*}

/-- Drive the original machine by a deterministic finite input generator. -/
def drivenGenerator (M : Mealy S) (G : Generator T) : Generator (S × T) where
  next p := (M.next p.1 (G.out p.2), G.next p.2)
  out p := M.out p.1 (G.out p.2)

theorem drivenGenerator_position (M : Mealy S) (G : Generator T) (s : S) (t : T) (n : ℕ) :
    (drivenGenerator M G).position (s,t) n =
      (state M s (G.stream t) n, G.position t n) := by
  induction n with
  | zero => rfl
  | succ n ih =>
    rw [Generator.position, ih]
    rfl

theorem drivenGenerator_stream (M : Mealy S) (G : Generator T) (s : S) (t : T) :
    (drivenGenerator M G).stream (s,t) = output M s (G.stream t) := by
  funext n
  change (drivenGenerator M G).out ((drivenGenerator M G).position (s,t) n) = _
  rw [drivenGenerator_position]
  rfl

/-- A finite input driver reads u and then emits false forever; its position saturates. -/
def prefixDriver (u : List Bool) : Generator (Fin (u.length+1)) where
  next i := ⟨min (i.val+1) u.length, Nat.lt_succ_of_le (Nat.min_le_right _ _)⟩
  out i := extend u i

theorem prefixDriver_position (u : List Bool) (n : ℕ) :
    ((prefixDriver u).position 0 n).val = min n u.length := by
  induction n with
  | zero => simp [Generator.position]
  | succ n ih =>
    change min (((prefixDriver u).position 0 n).val + 1) u.length = min (n+1) u.length
    rw [ih]
    omega

theorem prefixDriver_stream (u : List Bool) : (prefixDriver u).stream 0 = extend u := by
  funext n
  change extend u (((prefixDriver u).position 0 n).val) = extend u n
  rw [prefixDriver_position]
  by_cases hn : n < u.length
  · rw [Nat.min_eq_left (Nat.le_of_lt hn)]
  · rw [Nat.min_eq_right (by omega)]
    simp [extend, List.getElem?_eq_none (by omega : u.length ≤ n)]

/-- Every positive output atom has an explicit finite generator: follow a hitting prefix,
    then drive the source forever with constant false input. -/
theorem positive_atom_finite_generator [Finite S] [Nonempty S]
    (M : Mealy S) (s : S) (y : Cantor) (hy : y ∈ P02A2.positive (law M s)) :
    ∃ u : List Bool, (drivenGenerator M (prefixDriver u)).stream (s,0) = y := by
  obtain ⟨x, hout, n, hn⟩ := (positive_iff_hitting_prefix M s y).mp hy
  let u := pref n x
  refine ⟨u, ?_⟩
  rw [drivenGenerator_stream, prefixDriver_stream]
  apply Eq.trans _ hout
  apply hitting_prefix_determines_output M s x n hn
  have h := prefix_extend u
  simpa only [u, prefix_length] using h

/-- Rationality of each positive singleton, now derived from an explicit finite target
    and the kernel-verified executable mismatch solver. -/
theorem positive_singleton_mass_rational [Fintype S] [DecidableEq S] [Nonempty S]
    (M : Mealy S) (s : S) (y : Cantor) (hy : y ∈ P02A2.positive (law M s)) :
    ∃ r : ℚ, (r : ℝ) = (law M s {y}).toReal := by
  obtain ⟨u, hu⟩ := positive_atom_finite_generator M s y hy
  obtain ⟨r, hr⟩ := generated_singleton_rational M (drivenGenerator M (prefixDriver u)) s (s,0)
  exact ⟨r, by simpa only [hu] using hr⟩

end Orthemology.Frontier.MealyMeasure
