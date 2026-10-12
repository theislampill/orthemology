import PythonRunnerSyntax

namespace P02.PythonRunner
open P02.PythonExpr P02A2.ObserverCore

/-- Supporting forward-iteration fact, already used by the Eighth abstract
statement machine; it receives no new Python-refinement credit here. -/
def forward {α : Type*} (f : ℕ → α → α) : ℕ → ℕ → α → α
  | _, 0, a => a
  | k, n+1, a => forward f (k+1) n (f k a)

theorem forward_succ_last {α : Type*} (f : ℕ → α → α) (k n : ℕ) (a : α) :
    forward f k (n+1) a = f (k+n) (forward f k n a) := by
  induction n generalizing k a with
  | zero => simp [forward]
  | succ n ih =>
      change forward f (k+1) (n+1) (f k a) = _
      rw [ih]
      change f (k+1+n) (forward f (k+1) n (f k a)) =
        f (k+(n+1)) (forward f (k+1) n (f k a))
      congr 1; omega

theorem forward_runLoop (body : Store → Store) (r n : ℕ) (σ : Store) :
    forward (fun i τ => body (Function.update τ r i)) 0 n σ = runLoop body r n σ := by
  induction n with
  | zero => rfl
  | succ n ih => rw [forward_succ_last, runLoop, ih]; simp

theorem repeatSummary_store (body : Dictionary → Summary) (f : Store → Store)
    (h : ∀ d, dictionaryRead (body d).store = f (dictionaryRead d))
    (r k n : ℕ) (d : Dictionary) :
    dictionaryRead (repeatSummary body r k n d).store =
      forward (fun i σ => f (Function.update σ r i)) k n (dictionaryRead d) := by
  induction n generalizing k d with
  | zero => rfl
  | succ n ih =>
      change dictionaryRead (repeatSummary body r (k+1) n (body (dictionaryWrite d r k)).store).store = _
      rw [ih, h, dictionary_read_write]
      rfl

mutual
/-- Pure variadic source summary agrees with the original functional-store
semantics, independently of any finite meter budget. -/
theorem commandSummary_store (trace : Bool) (s : Command) (d : Dictionary) :
    dictionaryRead (commandSummary trace s d).store = exec (lowerCommand s) (dictionaryRead d) := by
  cases s with
  | set r e => simp [commandSummary, lowerCommand, exec, dictionary_read_write, value_correct]
  | seq ss =>
      change dictionaryRead (commandsSummary trace ss d).store =
        exec (P02.Codec.sequenceList (lowerCommands ss)) (dictionaryRead d)
      rw [P02.Codec.sequenceList_execution]
      exact commandsSummary_store trace ss d
  | loop r e body =>
      change dictionaryRead
        (repeatSummary (commandSummary trace body) r 0 (value e (dictionaryRead d)) d).store = _
      rw [repeatSummary_store _ _ (fun d => commandSummary_store trace body d), forward_runLoop]
      simp [lowerCommand, exec, value_correct]
  | branch e s t =>
      simp only [commandSummary, lowerCommand, exec, charge, value_correct]
      split_ifs
      · exact commandSummary_store trace t d
      · exact commandSummary_store trace s d
termination_by sizeOf s

theorem commandsSummary_store (trace : Bool) (ss : Commands) (d : Dictionary) :
    dictionaryRead (commandsSummary trace ss d).store =
      (lowerCommands ss).foldl (fun σ s => exec s σ) (dictionaryRead d) := by
  cases ss with
  | nil => rfl
  | cons s ss =>
      change dictionaryRead (commandsSummary trace ss (commandSummary trace s d).store).store = _
      rw [commandsSummary_store, commandSummary_store]
      rfl
termination_by sizeOf ss
end

theorem commandSummary_pops_pos (trace : Bool) (s : Command) (d : Dictionary) :
    0 < (commandSummary trace s d).pops := by
  cases s <;> simp [commandSummary, charge]

theorem repeatSummary_pops_pos (body : Dictionary → Summary) (r k n : ℕ) (d : Dictionary) :
    0 < (repeatSummary body r k n d).pops := by
  cases n <;> simp [repeatSummary, charge]

theorem taskSummary_pops_pos (trace : Bool) (t : Task) (d : Dictionary) :
    0 < (taskSummary trace t d).pops := by
  cases t with
  | stmt s => exact commandSummary_pops_pos trace s d
  | «repeat» r count k body => exact repeatSummary_pops_pos _ _ _ _ _

theorem tasksSummary_pops_zero_iff (trace : Bool) (ts : List Task) (d : Dictionary) :
    (tasksSummary trace ts d).pops = 0 ↔ ts = [] := by
  cases ts with
  | nil => simp [tasksSummary, unchanged]
  | cons t ts =>
      have h := taskSummary_pops_pos trace t d
      simp only [tasksSummary, follow, List.cons_ne_nil, iff_false]
      omega

end P02.PythonRunner
