import CodecProgram
import UniformComputabilityNumeric

/-!
# Faithful finite-register, explicit-stack LOOP execution

This is a mathematical statement/repeat stack machine for the actual decoded
syntax, with strict natural values in an association-list register file.
Its count is captured at loop entry and the loop index is written before the
body. Fuel exhaustion returns `none`, never a semantic zero. Expression
arithmetic, decoding, and host storage are not metered here, so this is not a
claim about the Python `Meter.steps` number or host-resource exceptions.
No uniform Mathlib `Computable` theorem for the complete interpreter is claimed.
-/
namespace P02.Codec.UniformComputability
open P02A2.ObserverCore

abbrev RegFile := List (ℕ × ℕ)

def readRegs : RegFile → Store
  | [], _ => 0
  | (r,v)::rs, j => if j = r then v else readRegs rs j

def writeRegs (rs : RegFile) (r v : ℕ) : RegFile := (r,v)::rs

@[simp] theorem readRegs_write (rs : RegFile) (r v : ℕ) :
    readRegs (writeRegs rs r v) = Function.update (readRegs rs) r v := by
  funext j
  simp [readRegs, writeRegs, Function.update_apply]

def evalRegs : Expr → RegFile → ℕ
  | .constant n, _ => n
  | .reg r, rs => readRegs rs r
  | .add a b, rs => evalRegs a rs + evalRegs b rs
  | .sub a b, rs => evalRegs a rs - evalRegs b rs
  | .mul a b, rs => evalRegs a rs * evalRegs b rs
  | .div a b, rs => evalRegs a rs / evalRegs b rs
  | .mod a b, rs => evalRegs a rs % evalRegs b rs
  | .le a b, rs => if evalRegs a rs ≤ evalRegs b rs then 1 else 0
  | .eq a b, rs => if evalRegs a rs = evalRegs b rs then 1 else 0
  | .pow2 a, rs => 2 ^ evalRegs a rs

theorem evalRegs_correct (e : Expr) (rs : RegFile) :
    evalRegs e rs = evalExpr e (readRegs rs) := by
  induction e <;> simp_all [evalRegs, evalExpr]

/-- Forward iteration with a captured remaining count and a separate index. -/
def repeatFrom {α : Type*} (f : ℕ → α → α) : ℕ → ℕ → α → α
  | _, 0, s => s
  | k, n+1, s => repeatFrom f (k+1) n (f k s)

theorem repeatFrom_succ_last {α : Type*} (f : ℕ → α → α) (k n : ℕ) (s : α) :
    repeatFrom f k (n+1) s = f (k+n) (repeatFrom f k n s) := by
  induction n generalizing k s with
  | zero => simp [repeatFrom]
  | succ n ih =>
      change repeatFrom f (k+1) (n+1) (f k s) = _
      rw [ih]
      change f (k+1+n) (repeatFrom f (k+1) n (f k s)) =
        f (k+(n+1)) (repeatFrom f (k+1) n (f k s))
      congr 1 <;> omega

theorem repeatFrom_runLoop (body : Store → Store) (r n : ℕ) (σ : Store) :
    repeatFrom (fun i τ => body (Function.update τ r i)) 0 n σ = runLoop body r n σ := by
  induction n with
  | zero => rfl
  | succ n ih => rw [repeatFrom_succ_last, runLoop, ih]; simp

def execRegs : Stmt → RegFile → RegFile
  | .skip, rs => rs
  | .set r e, rs => writeRegs rs r (evalRegs e rs)
  | .seq s t, rs => execRegs t (execRegs s rs)
  | .loop r e s, rs =>
      repeatFrom (fun i τ => execRegs s (writeRegs τ r i)) 0 (evalRegs e rs) rs
  | .branch e s t, rs => if evalRegs e rs = 0 then execRegs t rs else execRegs s rs

theorem repeatFrom_read (body : RegFile → RegFile) (denote : Store → Store)
    (h : ∀ rs, readRegs (body rs) = denote (readRegs rs)) (r k n : ℕ) (rs : RegFile) :
    readRegs (repeatFrom (fun i τ => body (writeRegs τ r i)) k n rs) =
      repeatFrom (fun i τ => denote (Function.update τ r i)) k n (readRegs rs) := by
  induction n generalizing k rs with
  | zero => rfl
  | succ n ih => simp only [repeatFrom, ih, h, readRegs_write]

theorem execRegs_correct (s : Stmt) (rs : RegFile) :
    readRegs (execRegs s rs) = exec s (readRegs rs) := by
  induction s generalizing rs with
  | skip => rfl
  | set r e => simp [execRegs, exec, evalRegs_correct]
  | seq s t ihs iht => simp [execRegs, exec, ihs, iht]
  | loop r e s ih =>
      simp only [execRegs, exec, evalRegs_correct]
      rw [repeatFrom_read _ _ ih, repeatFrom_runLoop]
  | branch e s t ihs iht =>
      simp only [execRegs, exec, evalRegs_correct]
      split_ifs <;> simp [ihs, iht]

inductive Task where
  | stmt : Stmt → Task
  | repeat : ℕ → ℕ → ℕ → Stmt → Task
  deriving DecidableEq, Repr

abbrev Config := List Task × RegFile

/-- One statement/repeat transition; terminal configurations stutter. -/
def step : Config → Config
  | ([], rs) => ([], rs)
  | (.stmt .skip :: ts, rs) => (ts, rs)
  | (.stmt (.set r e) :: ts, rs) => (ts, writeRegs rs r (evalRegs e rs))
  | (.stmt (.seq s t) :: ts, rs) => (.stmt s :: .stmt t :: ts, rs)
  | (.stmt (.loop r e s) :: ts, rs) => (.repeat r 0 (evalRegs e rs) s :: ts, rs)
  | (.stmt (.branch e s t) :: ts, rs) =>
      (Task.stmt (if evalRegs e rs = 0 then t else s) :: ts, rs)
  | (.repeat _ _ 0 _ :: ts, rs) => (ts, rs)
  | (.repeat r k (n+1) s :: ts, rs) =>
      (.stmt s :: .repeat r (k+1) n s :: ts, writeRegs rs r k)

/-- Only exhausted fuel gives `none`; every returned value is a genuine run. -/
def runFuel (fuel : ℕ) (ts : List Task) (rs : RegFile) : Option RegFile :=
  let c := step^[fuel] (ts,rs)
  if c.1 = [] then some c.2 else none

private def Reaches (a b : Config) : Prop := ∃ fuel, step^[fuel] a = b

private theorem reaches_refl (c : Config) : Reaches c c := ⟨0,rfl⟩
private theorem reaches_step (c : Config) : Reaches c (step c) := ⟨1,rfl⟩
private theorem reaches_trans {a b c : Config} (hab : Reaches a b) (hbc : Reaches b c) :
    Reaches a c := by
  obtain ⟨n,hn⟩ := hab
  obtain ⟨m,hm⟩ := hbc
  refine ⟨m+n, ?_⟩
  rw [Function.iterate_add_apply, hn, hm]

private theorem repeat_reaches (s : Stmt)
    (hs : ∀ ts rs, Reaches (.stmt s :: ts, rs) (ts, execRegs s rs))
    (r k n : ℕ) (ts : List Task) (rs : RegFile) :
    Reaches (.repeat r k n s :: ts, rs)
      (ts, repeatFrom (fun i τ => execRegs s (writeRegs τ r i)) k n rs) := by
  induction n generalizing k rs with
  | zero => exact reaches_step _
  | succ n ih =>
      apply reaches_trans (reaches_step _)
      apply reaches_trans (hs _ _)
      exact ih _ _

private theorem stmt_reaches (s : Stmt) (ts : List Task) (rs : RegFile) :
    Reaches (.stmt s :: ts, rs) (ts, execRegs s rs) := by
  induction s generalizing ts rs with
  | skip => exact reaches_step _
  | set r e => exact reaches_step _
  | seq s t ihs iht =>
      exact reaches_trans (reaches_step _) (reaches_trans (ihs _ _) (iht _ _))
  | loop r e s ih =>
      exact reaches_trans (reaches_step _) (repeat_reaches s ih r 0 (evalRegs e rs) ts rs)
  | branch e s t ihs iht =>
      apply reaches_trans (reaches_step _)
      by_cases h : evalRegs e rs = 0
      · simpa [step, execRegs, h] using iht ts rs
      · simpa [step, execRegs, h] using ihs ts rs

/-- Every finite statement finishes on this explicit stack with enough fuel. -/
theorem runFuel_complete (s : Stmt) (rs : RegFile) :
    ∃ fuel, runFuel fuel [.stmt s] rs = some (execRegs s rs) := by
  obtain ⟨fuel,h⟩ := stmt_reaches s [] rs
  exact ⟨fuel, by simp [runFuel,h]⟩

def taskDenote : Task → Store → Store
  | .stmt s, σ => exec s σ
  | .repeat r k n s, σ =>
      repeatFrom (fun i τ => exec s (Function.update τ r i)) k n σ

def tasksDenote : List Task → Store → Store
  | [], σ => σ
  | t::ts, σ => tasksDenote ts (taskDenote t σ)

def configDenote (c : Config) : Store := tasksDenote c.1 (readRegs c.2)

theorem step_preserves (c : Config) : configDenote (step c) = configDenote c := by
  rcases c with ⟨ts,rs⟩
  cases ts with
  | nil => rfl
  | cons t ts =>
      cases t with
      | stmt s =>
          cases s <;> simp [step, configDenote, tasksDenote, taskDenote, exec,
            evalRegs_correct, repeatFrom_runLoop]
          split_ifs <;> rfl
      | «repeat» r k n s =>
          cases n <;> simp [step, configDenote, tasksDenote, taskDenote, repeatFrom]

theorem iterate_preserves (fuel : ℕ) (c : Config) :
    configDenote (step^[fuel] c) = configDenote c := by
  induction fuel generalizing c with
  | zero => rfl
  | succ fuel ih => rw [Function.iterate_succ_apply, ih, step_preserves]

/-- A successful run equals the original functional-store semantics. -/
theorem runFuel_sound (fuel : ℕ) (s : Stmt) (rs out : RegFile)
    (h : runFuel fuel [.stmt s] rs = some out) :
    readRegs out = exec s (readRegs rs) := by
  have hi := iterate_preserves fuel ([Task.stmt s],rs)
  simp only [runFuel] at h
  split_ifs at h with he
  · have ho := Option.some.inj h
    simpa [configDenote, he, ho, tasksDenote, taskDenote] using hi

def binaryRegs (n word : ℕ) : RegFile := [(0,n),(1,word)]

@[simp] theorem readRegs_binary (n word : ℕ) :
    readRegs (binaryRegs n word) = P02.Codec.binaryStore n word := by
  funext r
  simp [readRegs, binaryRegs, P02.Codec.binaryStore]

/-- Numeric syntax errors and arity mismatch return `some 0`; resource fuel
exhaustion returns `none` and is not silently reinterpreted as zero. -/
def evaluateIndexFuel (fuel index n word : ℕ) : Option ℕ :=
  match decodeIndex index with
  | none => some 0
  | some p => if p.arity = 2 then
      (runFuel fuel [.stmt p.body] (binaryRegs n word)).map (fun rs => readRegs rs p.output % 2)
    else some 0

theorem evaluateIndexFuel_sound {fuel index n word value : ℕ}
    (h : evaluateIndexFuel fuel index n word = some value) :
    value = evaluateIndex index n word := by
  unfold evaluateIndexFuel evaluateIndex at *
  cases hd : decodeIndex index with
  | none => simpa [hd] using h.symm
  | some p =>
      by_cases ha : p.arity = 2
      · simp only [hd, ha, ↓reduceIte] at h ⊢
        cases hr : runFuel fuel [Task.stmt p.body] (binaryRegs n word) with
        | none => simp [hr] at h
        | some rs =>
            simp only [hr, Option.map_some', Option.some.injEq] at h
            rw [← h, runFuel_sound _ _ _ _ hr, readRegs_binary]
      · simpa [hd, ha] using h.symm

theorem evaluateIndexFuel_complete (index n word : ℕ) :
    ∃ fuel, evaluateIndexFuel fuel index n word = some (evaluateIndex index n word) := by
  cases hd : decodeIndex index with
  | none => exact ⟨0, by simp [evaluateIndexFuel, evaluateIndex, hd]⟩
  | some p =>
      by_cases ha : p.arity = 2
      · obtain ⟨fuel,h⟩ := runFuel_complete p.body (binaryRegs n word)
        refine ⟨fuel, ?_⟩
        simp [evaluateIndexFuel, evaluateIndex, hd, ha, h, execRegs_correct]
      · exact ⟨0, by simp [evaluateIndexFuel, evaluateIndex, hd, ha]⟩

end P02.Codec.UniformComputability

namespace P02.Codec.UniformComputability
open P02A2.ObserverCore

private theorem terminal_iterate (fuel : ℕ) (rs : RegFile) :
    step^[fuel] ([],rs) = ([],rs) := by
  induction fuel with
  | zero => rfl
  | succ fuel ih => simpa [Function.iterate_succ_apply, step] using ih

/-- More transition fuel cannot change or destroy an already successful run. -/
theorem runFuel_mono {fuel more : ℕ} {ts : List Task} {rs out : RegFile}
    (hle : fuel ≤ more) (h : runFuel fuel ts rs = some out) :
    runFuel more ts rs = some out := by
  have hc : step^[fuel] (ts,rs) = ([],out) := by
    simp only [runFuel] at h
    split_ifs at h with he
    exact Prod.ext he (Option.some.inj h)
  obtain ⟨extra,rfl⟩ := Nat.exists_eq_add_of_le hle
  have hh : step^[fuel+extra] (ts,rs) = ([],out) := by
    rw [Nat.add_comm, Function.iterate_add_apply, hc, terminal_iterate]
  simp [runFuel, hh]

theorem evaluateIndexFuel_mono {fuel more index n word value : ℕ}
    (hle : fuel ≤ more) (h : evaluateIndexFuel fuel index n word = some value) :
    evaluateIndexFuel more index n word = some value := by
  unfold evaluateIndexFuel at *
  cases hd : decodeIndex index with
  | none => simpa [hd] using h
  | some p =>
      by_cases ha : p.arity = 2
      · simp only [hd, ha, ↓reduceIte] at h ⊢
        cases hr : runFuel fuel [Task.stmt p.body] (binaryRegs n word) with
        | none => simp [hr] at h
        | some rs =>
            rw [runFuel_mono hle hr]
            simpa [hr] using h
      · simpa [hd, ha] using h

/-- One fuel threshold works for every later resource budget. -/
theorem evaluateIndexFuel_eventually (index n word : ℕ) :
    ∃ fuel, ∀ more, fuel ≤ more →
      evaluateIndexFuel more index n word = some (evaluateIndex index n word) := by
  obtain ⟨fuel,h⟩ := evaluateIndexFuel_complete index n word
  exact ⟨fuel, fun more hle => evaluateIndexFuel_mono hle h⟩

/-- A nonterminating fuel search has no semantic value; here completeness
proves that this search does terminate for every numeric index and input. -/
def evaluateIndexSearch (index n word : ℕ) : Part ℕ :=
  Nat.rfindOpt (fun fuel => evaluateIndexFuel fuel index n word)

theorem evaluateIndexSearch_exact (index n word : ℕ) :
    evaluateIndexSearch index n word = Part.some (evaluateIndex index n word) := by
  apply Part.eq_some_iff.mpr
  apply (Nat.rfindOpt_mono (fun hle h => evaluateIndexFuel_mono hle h)).mpr
  exact evaluateIndexFuel_complete index n word

/-- The precise remaining effectivity obligation. Proving the numeric bounded
machine computable suffices for the actual universal evaluator, with no new
termination assumption. This is conditional, not the missing full theorem. -/
theorem evaluateIndex_computable_of_fuel
    (h : Computable₂ (fun (input : ℕ × ℕ × ℕ) fuel =>
      evaluateIndexFuel fuel input.1 input.2.1 input.2.2)) :
    Computable (fun input : ℕ × ℕ × ℕ => evaluateIndex input.1 input.2.1 input.2.2) := by
  apply (Partrec.rfindOpt h).of_eq_tot
  intro input
  change evaluateIndex input.1 input.2.1 input.2.2 ∈
    evaluateIndexSearch input.1 input.2.1 input.2.2
  rw [evaluateIndexSearch_exact]
  exact Part.mem_some _

@[simp] theorem evaluateIndexFuel_invalid (fuel index n word : ℕ)
    (h : decodeIndex index = none) : evaluateIndexFuel fuel index n word = some 0 := by
  simp [evaluateIndexFuel, h]

theorem evaluateIndexFuel_wrong_arity (fuel index n word : ℕ) (p : PackedProgram)
    (h : decodeIndex index = some p) (ha : p.arity ≠ 2) :
    evaluateIndexFuel fuel index n word = some 0 := by
  simp [evaluateIndexFuel, h, ha]

theorem evaluateIndexFuel_programIndex (fuel : ℕ) (p : P02A2.PRProgram.Program 2)
    (n word : ℕ) :
    evaluateIndexFuel fuel (programIndex (pack p)) n word =
      (runFuel fuel [.stmt p.body] (binaryRegs n word)).map (fun rs => readRegs rs p.output % 2) := by
  simp [evaluateIndexFuel, decodeIndex_programIndex, pack]

/-- Even a semantic one is not zeroed when the resource budget is exhausted. -/
theorem exhausted_one :
    evaluateIndexFuel 0 (programIndex ⟨2,2,.set 2 (.constant 1)⟩) 0 0 = none ∧
    evaluateIndex (programIndex ⟨2,2,.set 2 (.constant 1)⟩) 0 0 = 1 := by
  constructor
  · simp [evaluateIndexFuel, decodeIndex_programIndex, runFuel]
  · simp [evaluateIndex, decodeIndex_programIndex, exec, evalExpr]

end P02.Codec.UniformComputability
