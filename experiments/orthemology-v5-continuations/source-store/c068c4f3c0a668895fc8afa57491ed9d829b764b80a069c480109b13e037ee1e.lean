import ObserverAbstraction

namespace Orthemology.CertifiedObserver
open Orthemology.Frontier Orthemology.Frontier.MealyMeasure
open Set MeasureTheory
open scoped ENNReal
open P02A2.Q8Measure (fairCantor)
variable {S T : Type*}

/-- Local abstraction can fail on an explicitly declared transition guard. -/
structure GuardedSimulation (C : Mealy S) (A : Mealy T) where
  relates : S → T → Prop
  bad : S → T → Bool → Prop
  out_eq : ∀ {s t}, relates s t → ∀ b, ¬ bad s t b → C.out s b = A.out t b
  next_rel : ∀ {s t}, relates s t → ∀ b, ¬ bad s t b → relates (C.next s b) (A.next t b)

noncomputable def badMonitor {C : Mealy S} {A : Mealy T} (R : GuardedSimulation C A) :
    Mealy (S × T) where
  next z b := (C.next z.1 b, A.next z.2 b)
  out z b := by classical exact decide (R.bad z.1 z.2 b)

theorem badMonitor_state {C : Mealy S} {A : Mealy T} (R : GuardedSimulation C A)
    (s : S) (t : T) (x : Cantor) (n : ℕ) :
    state (badMonitor R) (s,t) x n = (state C s x n, state A t x n) := by
  induction n with
  | zero => rfl
  | succ n ih =>
      change (C.next (state (badMonitor R) (s,t) x n).1 (x n),
        A.next (state (badMonitor R) (s,t) x n).2 (x n)) = _
      rw [ih]
      rfl

def badAt {C : Mealy S} {A : Mealy T} (R : GuardedSimulation C A)
    (s : S) (t : T) (n : ℕ) : Set Cantor :=
  {x | R.bad (state C s x n) (state A t x n) (x n)}

def badRun {C : Mealy S} {A : Mealy T} (R : GuardedSimulation C A)
    (s : S) (t : T) : Set Cantor := ⋃ n, badAt R s t n

theorem badAt_measurable {C : Mealy S} {A : Mealy T} (R : GuardedSimulation C A)
    (s : S) (t : T) (n : ℕ) : MeasurableSet (badAt R s t n) := by
  classical
  have h := (measurable_pi_apply n).comp (output_measurable (badMonitor R) (s,t))
  have he : badAt R s t n = (fun x => output (badMonitor R) (s,t) x n) ⁻¹' {true} := by
    ext x
    simp only [badAt, mem_setOf_eq, mem_preimage, mem_singleton_iff]
    change _ ↔ decide (R.bad (state (badMonitor R) (s,t) x n).1
      (state (badMonitor R) (s,t) x n).2 (x n)) = true
    rw [badMonitor_state]
    simp
  rw [he]
  exact h (measurableSet_singleton true)

theorem badRun_measurable {C : Mealy S} {A : Mealy T} (R : GuardedSimulation C A)
    (s : S) (t : T) : MeasurableSet (badRun R s t) :=
  MeasurableSet.iUnion (badAt_measurable R s t)

/-- Outside the declared whole-run guard, induction preserves the relation. -/
theorem guarded_states {C : Mealy S} {A : Mealy T} (R : GuardedSimulation C A)
    {s t} (h : R.relates s t) {x : Cantor} (hx : x ∉ badRun R s t) (n : ℕ) :
    R.relates (state C s x n) (state A t x n) := by
  have hb : ∀ n, ¬ R.bad (state C s x n) (state A t x n) (x n) := by
    intro n hn
    exact hx (mem_iUnion.mpr ⟨n,hn⟩)
  induction n with
  | zero => exact h
  | succ n ih => exact R.next_rel ih (x n) (hb n)

theorem guarded_output {C : Mealy S} {A : Mealy T} (R : GuardedSimulation C A)
    {s t} (h : R.relates s t) {x : Cantor} (hx : x ∉ badRun R s t) :
    output C s x = output A t x := by
  funext n
  apply R.out_eq (guarded_states R h hx n) (x n)
  intro hn
  exact hx (mem_iUnion.mpr ⟨n,hn⟩)

/-- Literal solver error from a local guarded simulation, with measurable
whole-path failure event derived by the synchronous monitor. -/
theorem guarded_defect_error [Fintype T] [DecidableEq T] [Nonempty T]
    {C : Mealy S} {A : Mealy T} (R : GuardedSimulation C A) {s t}
    (h : R.relates s t) :
    |P02A2.defect (law C s) - (solveDefect A t : ℝ)| ≤
      (fairCantor (badRun R s t)).toReal :=
  certified_defect_error C A s t (badRun R s t) (fun _ hx => guarded_output R h hx)

/-- Only a summable whole-run budget licenses a uniform infinite-law error.
These are probabilities of the actual coupled run's bad-at-n events. -/
theorem badRun_le_tsum {C : Mealy S} {A : Mealy T} (R : GuardedSimulation C A)
    (s : S) (t : T) (ε : ℕ → ℝ≥0∞)
    (hε : ∀ n, fairCantor (badAt R s t n) ≤ ε n) :
    fairCantor (badRun R s t) ≤ ∑' n, ε n :=
  (measure_iUnion_le _).trans (ENNReal.tsum_le_tsum hε)

theorem guarded_defect_error_budget [Fintype T] [DecidableEq T] [Nonempty T]
    {C : Mealy S} {A : Mealy T} (R : GuardedSimulation C A) {s t}
    (h : R.relates s t) (δ : ℝ) (hδ : 0 ≤ δ) (ε : ℕ → ℝ≥0∞)
    (hε : ∀ n, fairCantor (badAt R s t n) ≤ ε n)
    (budget : (∑' n, ε n) ≤ ENNReal.ofReal δ) :
    |P02A2.defect (law C s) - (solveDefect A t : ℝ)| ≤ δ := by
  apply (guarded_defect_error R h).trans
  have hm := (badRun_le_tsum R s t ε hε).trans budget
  have ht := ENNReal.toReal_mono ENNReal.ofReal_ne_top hm
  simpa only [ENNReal.toReal_ofReal hδ] using ht

end Orthemology.CertifiedObserver
