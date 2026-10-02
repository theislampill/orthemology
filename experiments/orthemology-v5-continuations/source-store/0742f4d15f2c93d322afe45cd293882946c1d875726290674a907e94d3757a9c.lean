import IndexedRuntime

/-! An executable finite-table compiler to the retained P02 source grammar.
Registers 0/1 retain the acquired stage/word; 2 is finite state, 3 loop index,
and 4 output. Every source tick recomputes from its literal finite prefix. -/
namespace Orthemology.RuntimeBridge
open Orthemology.Frontier Orthemology.Frontier.MealyMeasure
open P02A2.ObserverCore P02.Codec
open Orthemology.CertifiedObserver
open MeasureTheory
open P02A2.Q8Measure (fairCantor)

variable {N : ℕ}

def bitNat (b : Bool) : ℕ := if b then 1 else 0

def transitionCode (M : Mealy (Fin N)) (s : Fin N) (b : Bool) : Stmt :=
  .seq (.set 4 (.constant (bitNat (M.out s b))))
    (.set 2 (.constant (M.next s b).val))

def bitExpr : Expr :=
  .mod (.div (.reg 1) (.pow2 (.sub (.reg 0) (.reg 3)))) (.constant 2)

def rowCode (M : Mealy (Fin N)) (s : Fin N) : Stmt :=
  .branch (.eq bitExpr (.constant 1)) (transitionCode M s true) (transitionCode M s false)

def dispatch (M : Mealy (Fin N)) : List (Fin N) → Stmt
  | [] => .skip
  | s :: ss => .branch (.eq (.reg 2) (.constant s.val)) (rowCode M s) (dispatch M ss)

def stepCode (M : Mealy (Fin N)) : Stmt := dispatch M (List.finRange N)

def compiled (M : Mealy (Fin N)) (s : Fin N) : PackedProgram where
  arity := 2
  output := 4
  body := .seq (.set 2 (.constant s.val))
    (.loop 3 (.add (.reg 0) (.constant 1)) (stepCode M))

def index (M : Mealy (Fin N)) (s : Fin N) : ℕ := programIndex (compiled M s)

def wordBits (stage word : ℕ) : Cantor :=
  fun k => decide (word / 2^(stage-k) % 2 = 1)

theorem transition_value (M : Mealy (Fin N)) (s : Fin N) (b : Bool) (σ : Store) :
    exec (transitionCode M s b) σ 2 = (M.next s b).val ∧
    exec (transitionCode M s b) σ 4 = bitNat (M.out s b) := by
  simp [transitionCode, exec, evalExpr]

theorem transition_frame (M : Mealy (Fin N)) (s : Fin N) (b : Bool)
    (σ : Store) (r : ℕ) (h2 : r ≠ 2) (h4 : r ≠ 4) :
    exec (transitionCode M s b) σ r = σ r := by
  simp [transitionCode, exec, evalExpr, Function.update_apply, h2, h4]

theorem dispatch_value (M : Mealy (Fin N)) (ss : List (Fin N)) (s : Fin N)
    (hs : s ∈ ss) (σ : Store) (hσ : σ 2 = s.val) :
    exec (dispatch M ss) σ = exec (rowCode M s) σ := by
  induction ss with
  | nil => simp at hs
  | cons q qs ih =>
      by_cases he : s = q
      · subst q
        simp [dispatch, exec, evalExpr, hσ]
      · have hn : s.val ≠ q.val := fun hh => he (Fin.ext hh)
        have hm : s ∈ qs := by simpa [he] using hs
        simpa [dispatch, exec, evalExpr, hσ, hn] using ih hm

theorem row_value (M : Mealy (Fin N)) (s : Fin N) (σ : Store) :
    exec (rowCode M s) σ =
      exec (transitionCode M s (wordBits (σ 0) (σ 1) (σ 3))) σ := by
  by_cases h : σ 1 / 2^(σ 0-σ 3) % 2 = 1 <;>
    simp [rowCode, wordBits, bitExpr, exec, evalExpr, h]

theorem step_value (M : Mealy (Fin N)) (s : Fin N) (σ : Store)
    (hσ : σ 2 = s.val) :
    exec (stepCode M) σ 2 = (M.next s (wordBits (σ 0) (σ 1) (σ 3))).val ∧
    exec (stepCode M) σ 4 = bitNat (M.out s (wordBits (σ 0) (σ 1) (σ 3))) := by
  rw [stepCode, dispatch_value M _ s (List.mem_finRange s) σ hσ, row_value]
  exact transition_value _ _ _ _

theorem dispatch_frame (M : Mealy (Fin N)) (ss : List (Fin N))
    (σ : Store) (r : ℕ) (h2 : r ≠ 2) (h4 : r ≠ 4) :
    exec (dispatch M ss) σ r = σ r := by
  induction ss with
  | nil => rfl
  | cons q qs ih =>
      by_cases he : σ 2 = q.val
      · simp only [dispatch, exec, evalExpr, he, ↓reduceIte, Nat.one_ne_zero]
        rw [row_value]
        exact transition_frame _ _ _ _ _ h2 h4
      · simpa only [dispatch, exec, evalExpr, he, ↓reduceIte] using ih

theorem step_frame (M : Mealy (Fin N)) (σ : Store) (r : ℕ)
    (h2 : r ≠ 2) (h4 : r ≠ 4) : exec (stepCode M) σ r = σ r :=
  dispatch_frame _ _ _ _ h2 h4

def loopStore (M : Mealy (Fin N)) (s : Fin N) (stage word k : ℕ) : Store :=
  runLoop (exec (stepCode M)) 3 k (Function.update (binaryStore stage word) 2 s.val)

theorem loop_inputs (M : Mealy (Fin N)) (s : Fin N) (stage word k : ℕ) :
    loopStore M s stage word k 0 = stage ∧ loopStore M s stage word k 1 = word := by
  induction k with
  | zero => simp [loopStore, runLoop, binaryStore]
  | succ k ih =>
      change exec (stepCode M) (Function.update (loopStore M s stage word k) 3 k) 0 = stage ∧
        exec (stepCode M) (Function.update (loopStore M s stage word k) 3 k) 1 = word
      rw [step_frame _ _ 0 (by decide) (by decide), step_frame _ _ 1 (by decide) (by decide)]
      simpa using ih

theorem loop_state (M : Mealy (Fin N)) (s : Fin N) (stage word k : ℕ) :
    loopStore M s stage word k 2 = (state M s (wordBits stage word) k).val := by
  induction k with
  | zero => simp [loopStore, runLoop, state]
  | succ k ih =>
      change exec (stepCode M) (Function.update (loopStore M s stage word k) 3 k) 2 = _
      have hs : Function.update (loopStore M s stage word k) 3 k 2 =
          (state M s (wordBits stage word) k).val := by simpa using ih
      rw [(step_value M _ _ hs).1]
      simp only [Function.update_of_ne (by decide : 0 ≠ 3),
        Function.update_of_ne (by decide : 1 ≠ 3), Function.update_self,
        (loop_inputs M s stage word k).1, (loop_inputs M s stage word k).2, state]

theorem loop_output (M : Mealy (Fin N)) (s : Fin N) (stage word k : ℕ) :
    loopStore M s stage word (k+1) 4 = bitNat (output M s (wordBits stage word) k) := by
  change exec (stepCode M) (Function.update (loopStore M s stage word k) 3 k) 4 = _
  have hs : Function.update (loopStore M s stage word k) 3 k 2 =
      (state M s (wordBits stage word) k).val := by simp [loop_state]
  rw [(step_value M _ _ hs).2]
  simp only [Function.update_of_ne (by decide : 0 ≠ 3),
    Function.update_of_ne (by decide : 1 ≠ 3), Function.update_self,
    (loop_inputs M s stage word k).1, (loop_inputs M s stage word k).2, MealyMeasure.output]

theorem decode_compiled (M : Mealy (Fin N)) (s : Fin N) :
    decodeIndex (index M s) = some (compiled M s) := decodeIndex_programIndex _

theorem evaluate_compiled (M : Mealy (Fin N)) (s : Fin N) (stage word : ℕ) :
    evaluateIndex (index M s) stage word = bitNat (output M s (wordBits stage word) stage) := by
  rw [evaluateIndex, decode_compiled]
  change loopStore M s stage word (stage+1) 4 % 2 = _
  rw [loop_output]
  cases output M s (wordBits stage word) stage <;> rfl

end Orthemology.RuntimeBridge

namespace Orthemology.RuntimeBridge
open Orthemology.Frontier Orthemology.Frontier.MealyMeasure
open P02A2.ObserverCore P02.Codec
open Orthemology.CertifiedObserver
open MeasureTheory
open P02A2.Q8Measure (fairCantor)
variable {N : ℕ}

theorem prefix_half (x : Cantor) (n : ℕ) :
    sentinel (pref (n+1) x) / 2 = sentinel (pref n x) := by
  rw [Indexed.sentinel_succ]
  cases x n <;> simp only [Indexed.appendBit, Bool.false_eq_true, ↓reduceIte] <;> omega

theorem prefix_last (x : Cantor) (n : ℕ) :
    sentinel (pref (n+1) x) % 2 = bitNat (x n) := by
  exact P02A2.Q8Compiler.sentinel_prefix_last x n

theorem prefix_digit (x : Cantor) (n i : ℕ) (hi : i ≤ n) :
    sentinel (pref (n+1) x) / 2^(n-i) % 2 = bitNat (x i) := by
  induction n with
  | zero =>
      have he : i = 0 := by omega
      subst i
      simpa using prefix_last x 0
  | succ n ih =>
      by_cases he : i = n+1
      · subst i
        simpa using prefix_last x (n+1)
      · have hn : i ≤ n := by omega
        have hex : n+1-i = (n-i)+1 := by omega
        rw [hex, pow_succ', ← Nat.div_div_eq_div_mul, prefix_half]
        exact ih hn

theorem wordBits_prefix (x : Cantor) (n : ℕ) :
    pref (n+1) (wordBits n (sentinel (pref (n+1) x))) = pref (n+1) x := by
  apply (prefix_eq_iff _ _ _).mpr
  intro i hi
  unfold wordBits
  rw [prefix_digit x n i (by omega)]
  cases x i <;> rfl

theorem wordBits_output (M : Mealy (Fin N)) (s : Fin N) (x : Cantor) (n : ℕ) :
    output M s (wordBits n (sentinel (pref (n+1) x))) n = output M s x n := by
  have h := output_prefix_congr M s (wordBits_prefix x n)
  exact (prefix_eq_iff _ _ _).mp h n (Nat.lt_succ_self _)

/-- The parser-owned source evaluator has exactly the finite Mealy behavior on
all fair-bit streams; no probability, future-bit, or simulation premise. -/
theorem compiled_source_output (M : Mealy (Fin N)) (s : Fin N) :
    P02A2.ObserverCore.output (evaluateIndex (index M s)) = output M s := by
  funext x n
  change decide (evaluateIndex (index M s) n (sentinel (pref (n+1) x)) % 2 = 1) = _
  rw [evaluate_compiled, wordBits_output]
  cases output M s x n <;> rfl

/-- Literal whole-stream equality for the unchanged actual stack evaluator and
its all-input successful per-stage fuel schedule. -/
theorem compiled_runtime_output (M : Mealy (Fin N)) (s : Fin N) :
    Indexed.runtimeOutput (index M s) = output M s := by
  rw [Indexed.runtime_output_exact, Indexed.source_output_exact, compiled_source_output]

/-- The same entire law, not only a finite trace or a marginal. -/
theorem compiled_runtime_law (M : Mealy (Fin N)) (s : Fin N) :
    fairCantor.map (Indexed.runtimeOutput (index M s)) = law M s := by
  rw [compiled_runtime_output]
  rfl

/-- The finite rational defect solver applies to any compiled table. -/
theorem compiled_runtime_defect (M : Mealy (Fin N)) (s : Fin N) :
    (solveDefect M s : ℝ) = P02A2.defect (fairCantor.map (Indexed.runtimeOutput (index M s))) := by
  letI : Nonempty (Fin N) := ⟨s⟩
  rw [compiled_runtime_law]
  exact solveDefect_correct M s

end Orthemology.RuntimeBridge
