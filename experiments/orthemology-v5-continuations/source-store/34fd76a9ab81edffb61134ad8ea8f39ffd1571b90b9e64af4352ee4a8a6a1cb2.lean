import Q8Machine
import P02A2.ObserverCore

/-! Structural refinement of compile_q8's fixed-register LOOP program.
The binary sequence below is the fold of the Python implementation's list
sequence. This file does not establish byte encoding/decoding correctness. -/
namespace P02A2.Q8Compiler
open P02A2.ObserverCore P02A2.Q8Machine

-- Register layout is exactly Builder(3) in recovered code/prcodec.py.
def counterReg (r : Fin 2) : ℕ := 7 + r.val

def compileInstruction {n : ℕ} : Instruction n → Stmt
  | .halt => .set 5 (.constant 1)
  | .inc r next => .seq
      (.set (counterReg r) (.add (.reg (counterReg r)) (.constant 1)))
      (.set 3 (.constant next.val))
  | .dec r zero next => .branch (.eq (.reg (counterReg r)) (.constant 0))
      (.set 3 (.constant zero.val))
      (.seq (.set (counterReg r) (.sub (.reg (counterReg r)) (.constant 1)))
        (.set 3 (.constant next.val)))

def Matches {n : ℕ} (σ : Store) (s : Config n) : Prop :=
  σ 3 = s.pc.val ∧ σ 5 = (if s.halted then 1 else 0) ∧
  σ 7 = s.counter 0 ∧ σ 8 = s.counter 1

theorem instruction_matches {n : ℕ} (i : Instruction n) (σ : Store) (s : Config n)
    (hs : Matches σ s) : Matches (exec (compileInstruction i) σ) (execute i s) := by
  rcases hs with ⟨hpc, hh, h0, h1⟩
  cases i with
  | halt => simp [compileInstruction, exec, evalExpr, execute, Matches, hpc, h0, h1]
  | inc r next =>
      fin_cases r <;> simp [compileInstruction, exec, evalExpr, execute, Matches,
        counterReg, hpc, hh, h0, h1, Function.update_apply]
  | dec r zero next =>
      fin_cases r
      · by_cases h : s.counter 0 = 0 <;>
          simp [compileInstruction, exec, evalExpr, execute, Matches,
            counterReg, hpc, hh, h0, h1, Function.update_apply, h]
      · by_cases h : s.counter 1 = 0 <;>
          simp [compileInstruction, exec, evalExpr, execute, Matches,
            counterReg, hpc, hh, h0, h1, Function.update_apply, h]

theorem instruction_preserves {n : ℕ} (i : Instruction n) (σ : Store) (r : ℕ)
    (h3 : r ≠ 3) (h5 : r ≠ 5) (h7 : r ≠ 7) (h8 : r ≠ 8) :
    exec (compileInstruction i) σ r = σ r := by
  cases i with
  | halt => simp [compileInstruction, exec, Function.update_apply, h5]
  | inc c next => fin_cases c <;>
      simp [compileInstruction, exec, Function.update_apply, counterReg, h3, h7, h8]
  | dec c zero next => fin_cases c <;>
      simp [compileInstruction, exec, evalExpr, Function.update_apply, counterReg,
        h3, h7, h8] <;> split_ifs <;> simp [Function.update_apply, h3, h7, h8]

def scan {n : ℕ} (M : Machine n) : List (Fin n) → Stmt
  | [] => .skip
  | i::is => .seq
      (.branch (.eq (.reg 4) (.constant i.val)) (compileInstruction (M i)) .skip)
      (scan M is)

theorem scan_exec {n : ℕ} (M : Machine n) (is : List (Fin n))
    (hi : is.Nodup) (pc : Fin n) (σ : Store) (hσ : σ 4 = pc.val) :
    exec (scan M is) σ = if pc ∈ is then exec (compileInstruction (M pc)) σ else σ := by
  induction is generalizing σ with
  | nil => simp [scan, exec]
  | cons i is ih =>
      have hn := List.nodup_cons.mp hi
      by_cases hp : pc = i
      · subst i
        have hframe : exec (compileInstruction (M pc)) σ 4 = pc.val := by
          rw [instruction_preserves _ _ 4 (by decide) (by decide) (by decide) (by decide), hσ]
        simp only [scan, exec, evalExpr, hσ, ↓reduceIte, Nat.one_ne_zero]
        rw [ih hn.2 _ hframe]
        simp [hn.1]
      · have hval : pc.val ≠ i.val := by exact fun h => hp (Fin.ext h)
        simp only [scan, exec, evalExpr, hσ, hval, ↓reduceIte]
        rw [ih hn.2 _ hσ]
        simp [hp]

def compiledStep {n : ℕ} (M : Machine n) : Stmt :=
  .branch (.eq (.reg 5) (.constant 0))
    (.seq (.set 4 (.reg 3)) (scan M (List.finRange n))) .skip

theorem matches_update_scratch {n : ℕ} (σ : Store) (s : Config n)
    (hs : Matches σ s) (r v : ℕ) (h3 : 3 ≠ r) (h5 : 5 ≠ r)
    (h7 : 7 ≠ r) (h8 : 8 ≠ r) : Matches (Function.update σ r v) s := by
  simpa only [Matches, Function.update_of_ne h3, Function.update_of_ne h5,
    Function.update_of_ne h7, Function.update_of_ne h8] using hs

theorem compiledStep_matches {n : ℕ} (M : Machine n) (σ : Store) (s : Config n)
    (hs : Matches σ s) : Matches (exec (compiledStep M) σ) (step M s) := by
  have hpc := hs.1
  have hh := hs.2.1
  cases hh' : s.halted
  · have hz : σ 5 = 0 := by simpa [hh'] using hh
    simp only [compiledStep, exec, evalExpr, hz, ↓reduceIte, Nat.one_ne_zero]
    rw [scan_exec M _ (List.nodup_finRange n) s.pc _ (by simp [hpc])]
    simp only [List.mem_finRange, ↓reduceIte]
    simpa only [step, hh', Bool.false_eq_true, ↓reduceIte] using
      instruction_matches (M s.pc) (Function.update σ 4 (σ 3)) s
        (matches_update_scratch σ s hs 4 (σ 3) (by decide) (by decide) (by decide) (by decide))
  · have ho : σ 5 = 1 := by simpa [hh'] using hh
    simpa [compiledStep, exec, evalExpr, ho, step, hh'] using hs

theorem loop_matches {n : ℕ} (M : Machine n) (hn : 0 < n) (σ : Store)
    (hs : Matches σ (initial n hn)) (k : ℕ) :
    Matches (runLoop (exec (compiledStep M)) 6 k σ) (run M hn k) := by
  induction k with
  | zero => exact hs
  | succ k ih =>
      simp only [runLoop, run]
      exact compiledStep_matches M _ _ (matches_update_scratch _ _ ih 6 k
        (by decide) (by decide) (by decide) (by decide))

theorem scan_preserves {n : ℕ} (M : Machine n) (is : List (Fin n)) (σ : Store) (r : ℕ)
    (h3 : r ≠ 3) (h5 : r ≠ 5) (h7 : r ≠ 7) (h8 : r ≠ 8) :
    exec (scan M is) σ r = σ r := by
  induction is generalizing σ with
  | nil => rfl
  | cons i is ih =>
      simp only [scan, exec]
      rw [ih]
      split_ifs
      · rfl
      · exact instruction_preserves (M i) σ r h3 h5 h7 h8

theorem compiledStep_preserves {n : ℕ} (M : Machine n) (σ : Store) (r : ℕ)
    (h3 : r ≠ 3) (h4 : r ≠ 4) (h5 : r ≠ 5) (h7 : r ≠ 7) (h8 : r ≠ 8) :
    exec (compiledStep M) σ r = σ r := by
  simp only [compiledStep, exec]
  split_ifs
  · rfl
  · rw [scan_preserves M _ _ r h3 h5 h7 h8]
    simp [Function.update_apply, h4]

theorem runLoop_preserves (body : Store → Store) (index r : ℕ)
    (hr : r ≠ index) (hbody : ∀ σ, body σ r = σ r) (k : ℕ) (σ : Store) :
    runLoop body index k σ r = σ r := by
  induction k with
  | zero => rfl
  | succ k ih =>
      simp only [runLoop, hbody, Function.update_of_ne hr, ih]

def initCode : Stmt := .seq (.set 3 (.constant 0))
  (.seq (.set 5 (.constant 0)) (.seq (.set 7 (.constant 0)) (.set 8 (.constant 0))))

theorem initCode_matches {n : ℕ} (hn : 0 < n) (σ : Store) :
    Matches (exec initCode σ) (initial n hn) := by
  simp [initCode, exec, evalExpr, Matches, initial, Function.update_apply]

theorem initCode_preserves (σ : Store) (r : ℕ)
    (h3 : r ≠ 3) (h5 : r ≠ 5) (h7 : r ≠ 7) (h8 : r ≠ 8) :
    exec initCode σ r = σ r := by
  simp [initCode, exec, evalExpr, Function.update_apply, h3, h5, h7, h8]

def compiled {n : ℕ} (M : Machine n) : Stmt :=
  .seq initCode (.seq (.loop 6 (.add (.reg 0) (.constant 1)) (compiledStep M))
    (.seq (.set 2 (.constant 0))
      (.branch (.reg 5) (.set 2 (.mod (.reg 1) (.constant 2))) .skip)))

theorem compiled_value {n : ℕ} (M : Machine n) (hn : 0 < n) (σ : Store) :
    exec (compiled M) σ 2 = if boundedFlag M hn (σ 0) then σ 1 % 2 else 0 := by
  let σi := exec initCode σ
  let σl := runLoop (exec (compiledStep M)) 6 (σ 0 + 1) σi
  have hi0 : σi 0 = σ 0 := initCode_preserves σ 0 (by decide) (by decide) (by decide) (by decide)
  have hi1 : σi 1 = σ 1 := initCode_preserves σ 1 (by decide) (by decide) (by decide) (by decide)
  have hlm : Matches σl (run M hn (σ 0+1)) := loop_matches M hn σi (initCode_matches hn σ) _
  have hl1 : σl 1 = σ 1 := by
    change runLoop (exec (compiledStep M)) 6 (σ 0 + 1) σi 1 = σ 1
    rw [runLoop_preserves _ 6 1 (by decide)
      (fun τ => compiledStep_preserves M τ 1 (by decide) (by decide) (by decide) (by decide) (by decide)), hi1]
  have hl5 : σl 5 = if boundedFlag M hn (σ 0) then 1 else 0 := hlm.2.1
  change exec (.seq (.loop 6 (.add (.reg 0) (.constant 1)) (compiledStep M))
    (.seq (.set 2 (.constant 0)) (.branch (.reg 5) (.set 2 (.mod (.reg 1) (.constant 2))) .skip))) σi 2 = _
  simp only [exec, evalExpr, hi0]
  change (if Function.update σl 2 0 5 = 0 then Function.update σl 2 0 else
    Function.update (Function.update σl 2 0) 2 (Function.update σl 2 0 1 % 2)) 2 = _
  simp only [Function.update_of_ne (by decide : 5 ≠ 2),
    Function.update_of_ne (by decide : 1 ≠ 2), hl5, hl1]
  cases boundedFlag M hn (σ 0) <;> simp

def inputStore (stage word r : ℕ) : ℕ :=
  if r = 0 then stage else if r = 1 then word else 0

def programValue {n : ℕ} (M : Machine n) (stage word : ℕ) : ℕ :=
  exec (compiled M) (inputStore stage word) 2

theorem programValue_eq {n : ℕ} (M : Machine n) (hn : 0 < n) (stage word : ℕ) :
    programValue M stage word = if boundedFlag M hn stage then word % 2 else 0 := by
  simpa only [programValue, inputStore, ↓reduceIte, Nat.one_ne_zero] using
    compiled_value M hn (inputStore stage word)

theorem sentinel_append_bit (xs : List Bool) (b : Bool) :
    sentinel (xs ++ [b]) = 2 * sentinel xs + if b then 1 else 0 := by
  simp [sentinel, List.foldl_append]

theorem sentinel_prefix_last (x : ℕ → Bool) (n : ℕ) :
    sentinel (List.ofFn (fun i : Fin (n+1) => x i.val)) % 2 = if x n then 1 else 0 := by
  rw [List.ofFn_succ', List.concat_eq_append, sentinel_append_bit]
  cases h : x n <;> simp [Nat.add_mod, Nat.mul_mod, h]

theorem program_output_switched {n : ℕ} (M : Machine n) (hn : 0 < n)
    (x : ℕ → Bool) (stage : ℕ) :
    output (programValue M) x stage = Q8Measure.switched (boundedFlag M hn) x stage := by
  unfold output
  rw [programValue_eq M hn]
  cases h : boundedFlag M hn stage
  · simp [h, Q8Measure.switched]
  · simp only [h, ↓reduceIte, Nat.mod_mod, Q8Measure.switched]
    rw [sentinel_prefix_last]
    cases x stage <;> rfl

def compiledObserver {n : ℕ} (M : Machine n) : Q8Measure.Cantor → Q8Measure.Cantor :=
  output (programValue M)

theorem compiledObserver_eq {n : ℕ} (M : Machine n) (hn : 0 < n) :
    compiledObserver M = Q8Measure.switched (boundedFlag M hn) := by
  funext x stage
  exact program_output_switched M hn x stage

theorem compiledObserver_measurable {n : ℕ} (M : Machine n) (hn : 0 < n) :
    Measurable (compiledObserver M) := by
  rw [compiledObserver_eq M hn]
  exact Q8Measure.switched_measurable _

noncomputable def compiledLaw {n : ℕ} (M : Machine n) :=
  Q8Measure.fairCantor.map (compiledObserver M)

theorem compiledLaw_eq {n : ℕ} (M : Machine n) (hn : 0 < n) :
    compiledLaw M = Q8Machine.outputLaw M hn := by
  unfold compiledLaw Q8Machine.outputLaw Q8Measure.law
  rw [compiledObserver_eq M hn]

theorem compiled_defect_zero_iff_nonhalting {n : ℕ} (M : Machine n) (hn : 0 < n) :
    defect (compiledLaw M) = 0 ↔ ¬ Q8Machine.Halts M hn := by
  rw [compiledLaw_eq M hn]
  exact Q8Machine.defect_zero_iff_nonhalting M hn

theorem compiled_defect_one_iff_halting {n : ℕ} (M : Machine n) (hn : 0 < n) :
    defect (compiledLaw M) = 1 ↔ Q8Machine.Halts M hn := by
  rw [compiledLaw_eq M hn]
  exact Q8Machine.defect_one_iff_halting M hn

theorem compiled_nonhalting_dirac {n : ℕ} (M : Machine n) (hn : 0 < n)
    (h : ¬ Q8Machine.Halts M hn) :
    compiledLaw M = MeasureTheory.Measure.dirac (fun _ : ℕ => false) := by
  rw [compiledLaw_eq M hn]
  exact Q8Machine.nonhalting_law_dirac M hn h

theorem compiled_halting_singletons_zero {n : ℕ} (M : Machine n) (hn : 0 < n)
    (h : Q8Machine.Halts M hn) (y : Q8Measure.Cantor) : compiledLaw M {y} = 0 := by
  rw [compiledLaw_eq M hn]
  exact Q8Machine.halting_singletons_zero M hn h y

end P02A2.Q8Compiler
