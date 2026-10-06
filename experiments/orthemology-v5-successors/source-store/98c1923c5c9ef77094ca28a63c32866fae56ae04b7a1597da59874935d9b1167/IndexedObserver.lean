import GuardedObserver
import UniformComputabilityMachine
import Q8Compiler

/-! The initial state and transition store exactly the acquired prefix. The
actual decoder/evaluator, rather than a supplied initializer, fixes the output. -/
namespace Orthemology.CertifiedObserver.Indexed
open Orthemology.Frontier Orthemology.Frontier.MealyMeasure
open P02.Codec
open Set MeasureTheory
open scoped ENNReal
open P02A2.Q8Measure (fairCantor)

abbrev Config := ℕ × ℕ

def initial : Config := (0,1)

def appendBit (word : ℕ) (b : Bool) : ℕ := 2*word + if b then 1 else 0

def machine (index : ℕ) : Mealy Config where
  next cfg b := (cfg.1+1, appendBit cfg.2 b)
  out cfg b := decide (evaluateIndex index cfg.1 (appendBit cfg.2 b) % 2 = 1)

theorem sentinel_succ (x : Cantor) (k : ℕ) :
    P02A2.ObserverCore.sentinel (pref (k+1) x) =
      appendBit (P02A2.ObserverCore.sentinel (pref k x)) (x k) := by
  unfold pref appendBit
  rw [List.ofFn_succ', List.concat_eq_append, P02A2.Q8Compiler.sentinel_append_bit]
  rfl

/-- Source-state invariant with literal stage and acquired input word. -/
theorem literal_state (index : ℕ) (x : Cantor) (k : ℕ) :
    state (machine index) initial x k = (k, P02A2.ObserverCore.sentinel (pref k x)) := by
  induction k with
  | zero => rfl
  | succ k ih =>
      change ((state (machine index) initial x k).1+1,
        appendBit (state (machine index) initial x k).2 (x k)) = _
      rw [ih, sentinel_succ]

/-- Exact entire behavior of the actual indexed prefix evaluator. -/
theorem source_output_exact (index : ℕ) :
    output (machine index) initial = P02A2.ObserverCore.output (evaluateIndex index) := by
  funext x k
  change decide (evaluateIndex index (state (machine index) initial x k).1
    (appendBit (state (machine index) initial x k).2 (x k)) % 2 = 1) = _
  rw [literal_state]
  change decide (evaluateIndex index k
    (appendBit (P02A2.ObserverCore.sentinel (pref k x)) (x k)) % 2 = 1) = _
  rw [← sentinel_succ]
  rfl

noncomputable def sourceLaw (index : ℕ) : Measure Cantor :=
  fairCantor.map (P02A2.ObserverCore.output (evaluateIndex index))

theorem source_law_exact (index : ℕ) : sourceLaw index = law (machine index) initial := by
  unfold sourceLaw law
  rw [source_output_exact]

instance sourceLaw_probability (index : ℕ) : IsProbabilityMeasure (sourceLaw index) := by
  rw [source_law_exact]
  infer_instance

theorem acquired_prefix_only (index : ℕ) (x y : Cantor) (k : ℕ)
    (h : pref k x = pref k y) :
    state (machine index) initial x k = state (machine index) initial y k := by
  rw [literal_state, literal_state, h]

theorem unbounded_stage (index : ℕ) (x : Cantor) (k : ℕ) :
    (state (machine index) initial x k).1 = k := by rw [literal_state]

/-- A finite abstraction certificate now applies directly to every numeric
index, including the actual decoder's rejection/default conventions. -/
theorem certified_index_defect (index : ℕ)
    {T : Type*} [Fintype T] [DecidableEq T] [Nonempty T] (A : Mealy T)
    (R : Simulation (machine index) A) (t : T) (h : R.relates initial t) :
    (solveDefect A t : ℝ) = P02A2.defect (sourceLaw index) := by
  rw [source_law_exact]
  exact certified_defect_exact R h

theorem certified_index_error (index : ℕ)
    {T : Type*} [Fintype T] [DecidableEq T] [Nonempty T] (A : Mealy T)
    (R : GuardedSimulation (machine index) A) (t : T) (h : R.relates initial t)
    (δ : ℝ) (hδ : 0 ≤ δ) (ε : ℕ → ℝ≥0∞)
    (hε : ∀ k, fairCantor (badAt R initial t k) ≤ ε k)
    (budget : (∑' k, ε k) ≤ ENNReal.ofReal δ) :
    |P02A2.defect (sourceLaw index) - (solveDefect A t : ℝ)| ≤ δ := by
  rw [source_law_exact]
  exact guarded_defect_error_budget R h δ hδ ε hε budget

end Orthemology.CertifiedObserver.Indexed
