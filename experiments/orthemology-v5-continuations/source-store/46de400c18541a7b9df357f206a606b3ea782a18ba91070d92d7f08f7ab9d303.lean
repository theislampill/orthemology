import FiniteMealyCompiler

/-! Source-level transducer composition for unbounded natural memory. Supplied
transition/output programs are literal retained P02 programs with local semantic
certificates; no computability assertion is substituted for actual syntax. -/
namespace Orthemology.RuntimeBridge.Natural
open Orthemology.Frontier Orthemology.Frontier.MealyMeasure
open P02A2.ObserverCore P02A2.PRProgram P02.Codec
open Orthemology.CertifiedObserver
open P02A2.Q8Measure (fairCantor)
open MeasureTheory

/-- Caller-visible registers are disjoint from both reset private call blocks. -/
def args : Fin 2 → Expr := ![.reg 2, RuntimeBridge.bitExpr]

theorem args_fresh : ∀ i r, r ∈ P02A2.LoopRenaming.exprRegs (args i) → r < 8 := by
  intro i r hr
  fin_cases i <;> simp [args, RuntimeBridge.bitExpr, P02A2.LoopRenaming.exprRegs] at hr <;> omega

def stepCode (nextP outP : Program 2) : Stmt :=
  .seq (call outP 8 args 4) (call nextP 8 args 2)

def compiled (nextP outP : Program 2) (initial : ℕ) : PackedProgram where
  arity := 2
  output := 4
  body := .seq (.set 2 (.constant initial))
    (.loop 3 (.add (.reg 0) (.constant 1)) (stepCode nextP outP))

def index (nextP outP : Program 2) (initial : ℕ) : ℕ := programIndex (compiled nextP outP initial)

/-- Separate next-state and Boolean-output contracts only concern one acquired
bit. Programs may use arbitrarily large natural state and private registers. -/
structure Implements (nextP outP : Program 2) (M : Mealy ℕ) : Prop where
  next : ∀ s b, denote nextP ![s, bitNat b] = M.next s b
  out : ∀ s b, denote outP ![s, bitNat b] = bitNat (M.out s b)

theorem bit_value (σ : Store) :
    evalExpr RuntimeBridge.bitExpr σ = bitNat (wordBits (σ 0) (σ 1) (σ 3)) := by
  have h : σ 1 / 2^(σ 0-σ 3) % 2 = 0 ∨ σ 1 / 2^(σ 0-σ 3) % 2 = 1 := by omega
  rcases h with h | h <;> simp [RuntimeBridge.bitExpr, wordBits, bitNat, evalExpr, h]

theorem args_value (σ : Store) :
    (fun i => evalExpr (args i) σ) = ![σ 2,bitNat (wordBits (σ 0) (σ 1) (σ 3))] := by
  funext i
  fin_cases i
  · rfl
  · exact bit_value σ

theorem step_value (nextP outP : Program 2) (M : Mealy ℕ) (h : Implements nextP outP M)
    (σ : Store) :
    exec (stepCode nextP outP) σ 2 = M.next (σ 2) (wordBits (σ 0) (σ 1) (σ 3)) ∧
    exec (stepCode nextP outP) σ 4 = bitNat (M.out (σ 2) (wordBits (σ 0) (σ 1) (σ 3))) := by
  let τ := exec (call outP 8 args 4) σ
  have h0 : τ 0 = σ 0 := call_frame _ _ _ _ args_fresh 0 (by decide) (by decide) σ
  have h1 : τ 1 = σ 1 := call_frame _ _ _ _ args_fresh 1 (by decide) (by decide) σ
  have h2 : τ 2 = σ 2 := call_frame _ _ _ _ args_fresh 2 (by decide) (by decide) σ
  have h3 : τ 3 = σ 3 := call_frame _ _ _ _ args_fresh 3 (by decide) (by decide) σ
  constructor
  · change exec (call nextP 8 args 2) τ 2 = _
    rw [call_value _ _ _ _ args_fresh, args_value, h.next, h0, h1, h2, h3]
  · change exec (call nextP 8 args 2) τ 4 = _
    rw [call_frame _ _ _ _ args_fresh 4 (by decide) (by decide)]
    change exec (call outP 8 args 4) σ 4 = _
    rw [call_value _ _ _ _ args_fresh, args_value, h.out]

theorem step_frame (nextP outP : Program 2) (σ : Store) (r : ℕ)
    (hr : r < 8) (h2 : r ≠ 2) (h4 : r ≠ 4) :
    exec (stepCode nextP outP) σ r = σ r := by
  simp only [stepCode, exec]
  rw [call_frame _ _ _ _ args_fresh r hr h2, call_frame _ _ _ _ args_fresh r hr h4]

def loopStore (nextP outP : Program 2) (s stage word k : ℕ) : Store :=
  runLoop (exec (stepCode nextP outP)) 3 k (Function.update (binaryStore stage word) 2 s)

theorem loop_inputs (nextP outP : Program 2) (s stage word k : ℕ) :
    loopStore nextP outP s stage word k 0 = stage ∧ loopStore nextP outP s stage word k 1 = word := by
  induction k with
  | zero => simp [loopStore, runLoop, binaryStore]
  | succ k ih =>
      change exec (stepCode nextP outP) (Function.update (loopStore nextP outP s stage word k) 3 k) 0 = stage ∧
        exec (stepCode nextP outP) (Function.update (loopStore nextP outP s stage word k) 3 k) 1 = word
      rw [step_frame _ _ _ 0 (by decide) (by decide) (by decide),
        step_frame _ _ _ 1 (by decide) (by decide) (by decide)]
      simpa using ih

theorem loop_state (nextP outP : Program 2) (M : Mealy ℕ) (h : Implements nextP outP M)
    (s stage word k : ℕ) :
    loopStore nextP outP s stage word k 2 = state M s (wordBits stage word) k := by
  induction k with
  | zero => simp [loopStore, runLoop, state]
  | succ k ih =>
      change exec (stepCode nextP outP) (Function.update (loopStore nextP outP s stage word k) 3 k) 2 = _
      rw [(step_value _ _ M h _).1]
      simp only [Function.update_of_ne (by decide : 0 ≠ 3),
        Function.update_of_ne (by decide : 1 ≠ 3), Function.update_of_ne (by decide : 2 ≠ 3),
        Function.update_self, (loop_inputs nextP outP s stage word k).1,
        (loop_inputs nextP outP s stage word k).2, ih, state]

theorem loop_output (nextP outP : Program 2) (M : Mealy ℕ) (h : Implements nextP outP M)
    (s stage word k : ℕ) :
    loopStore nextP outP s stage word (k+1) 4 = bitNat (MealyMeasure.output M s (wordBits stage word) k) := by
  change exec (stepCode nextP outP) (Function.update (loopStore nextP outP s stage word k) 3 k) 4 = _
  rw [(step_value _ _ M h _).2]
  simp only [Function.update_of_ne (by decide : 0 ≠ 3),
    Function.update_of_ne (by decide : 1 ≠ 3), Function.update_of_ne (by decide : 2 ≠ 3),
    Function.update_self, (loop_inputs nextP outP s stage word k).1,
    (loop_inputs nextP outP s stage word k).2, loop_state _ _ M h, MealyMeasure.output]

theorem evaluate_compiled (nextP outP : Program 2) (M : Mealy ℕ) (h : Implements nextP outP M)
    (s stage word : ℕ) :
    evaluateIndex (index nextP outP s) stage word = bitNat (MealyMeasure.output M s (wordBits stage word) stage) := by
  rw [evaluateIndex, show decodeIndex (index nextP outP s) = some (compiled nextP outP s) from decodeIndex_programIndex _]
  change loopStore nextP outP s stage word (stage+1) 4 % 2 = _
  rw [loop_output _ _ M h]
  cases MealyMeasure.output M s (wordBits stage word) stage <;> rfl

/-- General acquired-prefix compilation with unbounded natural memory. -/
theorem compiled_source_output (nextP outP : Program 2) (M : Mealy ℕ) (h : Implements nextP outP M) (s : ℕ) :
    P02A2.ObserverCore.output (evaluateIndex (index nextP outP s)) = MealyMeasure.output M s := by
  funext x n
  change decide (evaluateIndex (index nextP outP s) n (sentinel (pref (n+1) x)) % 2 = 1) = _
  rw [evaluate_compiled _ _ M h]
  have he := output_prefix_congr M s (wordBits_prefix x n)
  have ho := (prefix_eq_iff _ _ _).mp he n (Nat.lt_succ_self _)
  rw [ho]
  cases MealyMeasure.output M s x n <;> rfl

theorem compiled_runtime_output (nextP outP : Program 2) (M : Mealy ℕ) (h : Implements nextP outP M) (s : ℕ) :
    Indexed.runtimeOutput (index nextP outP s) = MealyMeasure.output M s := by
  rw [Indexed.runtime_output_exact, Indexed.source_output_exact, compiled_source_output _ _ M h]

/-- Complete law transport; local P02 program certificates, not global trace
or law equality, are the hypotheses. -/
theorem compiled_runtime_law (nextP outP : Program 2) (M : Mealy ℕ) (h : Implements nextP outP M) (s : ℕ) :
    fairCantor.map (Indexed.runtimeOutput (index nextP outP s)) = fairCantor.map (MealyMeasure.output M s) := by
  rw [compiled_runtime_output _ _ M h]

end Orthemology.RuntimeBridge.Natural

namespace Orthemology.RuntimeBridge.Natural
open Orthemology.Frontier Orthemology.Frontier.MealyMeasure
open P02A2.PRProgram
open Orthemology.CertifiedObserver
open MeasureTheory

/-- Measurability is obtained from the actual acquired-prefix runtime, with no
finite-state premise on the supplied natural-memory machine. -/
theorem implemented_output_measurable (nextP outP : Program 2) (M : Mealy ℕ)
    (h : Implements nextP outP M) (s : ℕ) : Measurable (MealyMeasure.output M s) := by
  rw [← compiled_runtime_output _ _ M h]
  exact Indexed.runtime_output_measurable _

end Orthemology.RuntimeBridge.Natural
