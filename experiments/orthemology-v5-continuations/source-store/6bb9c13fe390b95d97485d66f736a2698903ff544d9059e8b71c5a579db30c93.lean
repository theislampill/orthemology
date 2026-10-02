import MealySolver

namespace Orthemology.Frontier.MealyMeasure
open Set MeasureTheory Filter
open scoped ENNReal Topology BigOperators
open P02A2.Q8Measure

/-- A finite-state deterministic generator presents an eventually periodic target stream. -/
structure Generator (T : Type*) where
  next : T → T
  out : T → Bool

namespace Generator
variable {T : Type*}

def position (G : Generator T) (t : T) : ℕ → T
  | 0 => t
  | n+1 => G.next (position G t n)

def stream (G : Generator T) (t : T) : Cantor := fun n => G.out (position G t n)

end Generator

variable {S T : Type*}

/-- Synchronize original execution with the target generator. Before the first mismatch,
    copy the fresh input bit; after mismatch, enter a permanent constant-output state. -/
def mismatchMachine (M : Mealy S) (G : Generator T) : Mealy (Option (S × T)) where
  next
    | none, _ => none
    | some (s,t), b => if M.out s b = G.out t then some (M.next s b, G.next t) else none
  out
    | none, _ => false
    | some _, b => b

/-- The auxiliary machine's deterministic-output domain is exactly its mismatch sink. -/
theorem mismatch_domain (M : Mealy S) (G : Generator T) (q : Option (S × T)) :
    (mismatchMachine M G).infiniteRel q q ↔ q = none := by
  cases q with
  | none =>
    simp only [iff_true]
    intro n
    induction n with
    | zero => trivial
    | succ n ih => intro b c; exact ⟨rfl, ih⟩
  | some p =>
    simp only [Option.some_ne_none, iff_false]
    intro h
    exact Bool.false_ne_true (h 1 false true).1

theorem pref_succ_eq_iff (n : ℕ) (x y : Cantor) :
    pref (n+1) x = pref (n+1) y ↔ pref n x = pref n y ∧ x n = y n := by
  rw [prefix_eq_iff, prefix_eq_iff]
  constructor
  · intro h
    exact ⟨fun i hi => h i (by omega), h n (by omega)⟩
  · rintro ⟨h, hn⟩ i hi
    by_cases hik : i < n
    · exact h i hik
    · have he : i = n := by omega
      simpa only [he] using hn

/-- Exact state correspondence: sink entry occurs at the first already-read mismatching bit. -/
theorem mismatch_state (M : Mealy S) (G : Generator T) (s : S) (t : T)
    (x : Cantor) (n : ℕ) :
    state (mismatchMachine M G) (some (s,t)) x n =
      if pref n (output M s x) = pref n (G.stream t) then
        some (state M s x n, G.position t n) else none := by
  induction n with
  | zero => simp [state, pref, Generator.position]
  | succ n ih =>
    rw [state, ih]
    by_cases hp : pref n (output M s x) = pref n (G.stream t)
    · simp only [hp, ↓reduceIte, mismatchMachine]
      have he : (pref (n+1) (output M s x) = pref (n+1) (G.stream t)) ↔
          M.out (state M s x n) (x n) = G.out (G.position t n) := by
        rw [pref_succ_eq_iff]
        simp only [hp, true_and, output, Generator.stream]
      simp only [he, state, Generator.position]
    · have hn : pref (n+1) (output M s x) ≠ pref (n+1) (G.stream t) :=
        fun h => hp ((pref_succ_eq_iff _ _ _).mp h).1
      simp [hp, hn, mismatchMachine]

/-- Infinite avoidance of the auxiliary D is exactly equality to the original target output. -/
theorem mismatch_hits_eq (M : Mealy S) (G : Generator T) (s : S) (t : T) :
    hits (mismatchMachine M G) (some (s,t)) = (output M s ⁻¹' {G.stream t})ᶜ := by
  ext x
  constructor
  · rintro ⟨n, hn⟩ he
    have h := (mismatch_domain M G _).mp hn
    rw [mismatch_state] at h
    have hp : pref n (output M s x) = pref n (G.stream t) := congrArg (pref n) he
    simp [hp] at h
  · intro hx
    by_contra hn
    apply hx
    change output M s x = G.stream t
    funext k
    have hp : pref (k+1) (output M s x) = pref (k+1) (G.stream t) := by
      by_contra hp
      apply hn
      refine ⟨k+1, (mismatch_domain M G _).mpr ?_⟩
      simp [mismatch_state, hp]
    exact (prefix_eq_iff _ _ _).mp hp k (by omega)

/-- Exact rational singleton-mass program for a finite-state presented target. -/
def targetMassQ [Fintype S] [DecidableEq S] [Fintype T] [DecidableEq T]
    (M : Mealy S) (G : Generator T) (s : S) (t : T) : ℚ :=
  solveDefect (mismatchMachine M G) (some (s,t))

theorem targetMassQ_correct [Fintype S] [DecidableEq S] [Fintype T] [DecidableEq T]
    (M : Mealy S) (G : Generator T) (s : S) (t : T) :
    (targetMassQ M G s t : ℝ) = (law M s {G.stream t}).toReal := by
  rw [targetMassQ, solveDefect_correct, P02A2.defect, atomic_mass_eq_hitting_probability,
    mismatch_hits_eq]
  have hf : MeasurableSet (output M s ⁻¹' {G.stream t}) :=
    (output_measurable M s) (measurableSet_singleton _)
  rw [law, Measure.map_apply (output_measurable M s) (measurableSet_singleton _)]
  rw [measure_compl hf (measure_ne_top fairCantor _), measure_univ]
  have hle : fairCantor (output M s ⁻¹' {G.stream t}) ≤ 1 := by
    simpa using (measure_mono (μ := fairCantor) (subset_univ (output M s ⁻¹' {G.stream t})))
  rw [ENNReal.toReal_sub_of_le hle (by simp)]
  simp only [ENNReal.toReal_one]
  ring

/-- Finite-state-generated target singletons have rational mass in the actual law. -/
theorem generated_singleton_rational [Fintype S] [DecidableEq S] [Fintype T] [DecidableEq T]
    (M : Mealy S) (G : Generator T) (s : S) (t : T) :
    ∃ r : ℚ, (r : ℝ) = (law M s {G.stream t}).toReal :=
  ⟨targetMassQ M G s t, targetMassQ_correct M G s t⟩

end Orthemology.Frontier.MealyMeasure
