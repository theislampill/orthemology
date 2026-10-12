import LiteralShiftSyntax

/-! Kernel proofs for the exact sorted compressed inline block and replay emitted
by the original `compile_shift`.  The semantic renaming argument is inherited
from `LoopRenaming.inlineCode_correct`; only the literal Seq-list grouping,
finite allocation, argument freshness, and caller-independent reset are proved
here. -/
namespace P02.LiteralShift
open P02A2.ObserverCore P02A2.LoopRenaming
open P02.Codec (sequenceList sequenceList_execution)

@[simp] theorem registerList_toFinset (body : Stmt) (output : ℕ) :
    (registerList body output).toFinset = sourceRegisters body output := by
  simp [registerList]

@[simp] theorem mem_registerList (body : Stmt) (output r : ℕ) :
    r ∈ registerList body output ↔ r ∈ sourceRegisters body output := by
  simp [registerList]

theorem registerMap_injOn (body : Stmt) (output : ℕ) :
    Set.InjOn (registerMap body output) (↑(sourceRegisters body output) : Set ℕ) := by
  intro r hr s hs he
  apply (List.idxOf_inj ((mem_registerList body output r).mpr hr)
    ((mem_registerList body output s).mpr hs)).mp
  exact Nat.add_left_cancel he

theorem registerMap_ge (body : Stmt) (output r : ℕ) :
    12 ≤ registerMap body output r := by
  simp [registerMap]

theorem not_mem_registerImage_of_lt (body : Stmt) (output j : ℕ) (hj : j < 12) :
    j ∉ (sourceRegisters body output).image (registerMap body output) := by
  intro hm
  rcases Finset.mem_image.mp hm with ⟨r, hr, he⟩
  have hge := registerMap_ge body output r
  omega

theorem sourceRegisters_body (body : Stmt) (output : ℕ) :
    stmtRegs body ⊆ sourceRegisters body output := by
  intro r hr
  simp [sourceRegisters, hr]

theorem tailArgs_fresh (body : Stmt) (output : ℕ) :
    ArgsFresh (sourceRegisters body output) (registerMap body output) tailArgs := by
  intro a ha
  simp only [tailArgs, List.mem_cons, List.not_mem_nil, or_false] at ha
  rcases ha with rfl | rfl
  · constructor
    · simp [sourceRegisters]
    · apply Finset.disjoint_left.mpr
      intro j hj
      simp only [exprRegs, Finset.union_empty, Finset.mem_singleton] at hj
      subst j
      exact not_mem_registerImage_of_lt body output 9 (by decide)
  · constructor
    · simp [sourceRegisters]
    · apply Finset.disjoint_left.mpr
      intro j hj
      simp only [exprRegs, Finset.mem_singleton] at hj
      subst j
      exact not_mem_registerImage_of_lt body output 10 (by decide)

/-- Grouping consecutive children of the literal variadic Seq preserves exec. -/
theorem sequenceList_append_exec (ss ts : List Stmt) (σ : Store) :
    exec (sequenceList (ss ++ ts)) σ =
      exec (sequenceList ts) (exec (sequenceList ss) σ) := by
  simp only [sequenceList_execution, List.foldl_append]

theorem sequenceList_resets_exec (ρ : ℕ → ℕ) (rs : List ℕ) (σ : Store) :
    exec (sequenceList (rs.map (fun r => Stmt.set (ρ r) (C 0)))) σ =
      exec (resetList ρ rs) σ := by
  rw [sequenceList_execution]
  induction rs generalizing σ with
  | nil => rfl
  | cons r rs ih =>
      simpa only [List.map_cons, List.foldl_cons, resetList, exec] using
        ih (Function.update σ (ρ r) 0)

theorem sequenceList_args_exec (ρ : ℕ → ℕ) (args : List (ℕ × Expr)) (σ : Store) :
    exec (sequenceList (args.map (fun a => Stmt.set (ρ a.1) a.2))) σ =
      exec (loadArgs ρ args) σ := by
  rw [sequenceList_execution]
  induction args generalizing σ with
  | nil => rfl
  | cons a args ih =>
      rcases a with ⟨r,e⟩
      simpa only [List.map_cons, List.foldl_cons, loadArgs, exec] using
        ih (Function.update σ (ρ r) (evalExpr e σ))

/-- Literal Python Seq-list lowering is executionally the inherited inlineCode. -/
theorem literalInline_exec_eq (body : Stmt) (output : ℕ) (σ : Store) :
    exec (literalInline body output) σ =
      exec (inlineCode (registerMap body output) (registerList body output)
        tailArgs body output 11) σ := by
  simp only [literalInline, sequenceList_append_exec, sequenceList_resets_exec,
    sequenceList_args_exec, sequenceList, inlineCode, exec]

theorem sourceLoad_tailArgs (σ : Store) :
    sourceLoad tailArgs σ (fun _ => 0) = initial (σ 9 - 1) (σ 10) := by
  funext r
  by_cases h0 : r = 0
  · subst r
    simp [tailArgs, sourceLoad, initial, evalExpr]
  · by_cases h1 : r = 1
    · subst r
      simp [tailArgs, sourceLoad, initial, evalExpr]
    · simp [tailArgs, sourceLoad, initial, evalExpr, Function.update_apply, h0, h1]

/-- Arbitrary previous source-local values in the caller are removed by the
literal reset block.  The result uses only the two argument expressions. -/
theorem literalInline_correct (body : Stmt) (output : ℕ) (caller : Store) :
    exec (literalInline body output) caller 11 =
      exec body (initial (caller 9 - 1) (caller 10)) output ∧
    ∀ j, j < 11 → exec (literalInline body output) caller j = caller j := by
  have hc := inlineCode_correct (registerMap body output) (registerList body output)
    tailArgs body output 11 (by simpa using registerMap_injOn body output)
    (by simpa using sourceRegisters_body body output)
    (by simp [sourceRegisters])
    (by simpa using tailArgs_fresh body output) caller
  rw [literalInline_exec_eq]
  constructor
  · simpa only [sourceLoad_tailArgs] using hc.1
  · intro j hj
    exact hc.2 j (by omega) (by
      rw [registerList_toFinset]
      exact not_mem_registerImage_of_lt body output j (by omega))

/-- Exact replay result for an arbitrary caller store, without any condition on
its source-local register values.  Natural subtraction is the Python LOOP
semantics and is intentionally retained even for out-of-range stop values. -/
theorem replay_correct (body : Stmt) (output n w stop : ℕ) (caller : Store)
    (h0 : caller 0 = n) (h1 : caller 1 = w) (h6 : caller 6 = stop) :
    exec (replay body output) caller 2 =
      exec body (initial (n + 1 - stop - 1)
        (2^(n + 1 - stop) + w % 2^(n + 1 - stop))) output % 2 := by
  let prepared := Function.update
    (Function.update caller 9 (n + 1 - stop)) 10
    (2^(n + 1 - stop) + w % 2^(n + 1 - stop))
  have h9 : prepared 9 = n + 1 - stop := by simp [prepared]
  have h10 : prepared 10 = 2^(n + 1 - stop) + w % 2^(n + 1 - stop) := by
    simp [prepared]
  have hi := (literalInline_correct body output prepared).1
  rw [h9, h10] at hi
  simpa only [replay, sequenceList, exec, evalExpr, lengthExpr,
    Function.update_self, Function.update_of_ne (by decide : (0 : ℕ) ≠ 9),
    Function.update_of_ne (by decide : (1 : ℕ) ≠ 9), h0, h1, h6,
    prepared] using congrArg (· % 2) hi

/-- Guarded result of the exact finish block. -/
theorem finish_correct (body : Stmt) (output n w : ℕ) (caller : Store)
    (h0 : caller 0 = n) (h1 : caller 1 = w) :
    exec (finish body output) caller 2 =
      if caller 4 ≠ 0 ∧ caller 5 ≠ 0 ∧ caller 6 ≤ n then
        exec body (initial (n + 1 - caller 6 - 1)
          (2^(n + 1 - caller 6) + w % 2^(n + 1 - caller 6))) output % 2
      else w % 2 := by
  let current := Function.update caller 2 (w % 2)
  have hr := replay_correct body output n w (caller 6) current
    (by simpa [current] using h0) (by simpa [current] using h1) (by simp [current])
  by_cases h4 : caller 4 = 0
  · simp [finish, sequenceList, exec, evalExpr, h1, h4]
  · by_cases h5 : caller 5 = 0
    · simp [finish, sequenceList, exec, evalExpr, h1, h4, h5]
    · by_cases h6 : caller 6 ≤ n
      · simpa [finish, sequenceList, exec, evalExpr, h0, h1, h4, h5, h6,
          current] using hr
      · simp [finish, sequenceList, exec, evalExpr, h0, h1, h4, h5, h6]

/-- The same exact finish block stated at the scan invariant boundary. -/
theorem finish_scanAgrees (body : Stmt) (output n w : ℕ) (caller : Store)
    (choice : Option Cut) (h : ScanAgrees caller n w choice) :
    exec (finish body output) caller 2 =
      if foundValue choice ≠ 0 ∧ branchValue choice ≠ 0 ∧ stopValue choice ≤ n then
        exec body (initial (n + 1 - stopValue choice - 1)
          (2^(n + 1 - stopValue choice) + w % 2^(n + 1 - stopValue choice))) output % 2
      else w % 2 := by
  rcases h with ⟨h0, h1, h4, h5, h6⟩
  simpa only [h4, h5, h6] using finish_correct body output n w caller h0 h1

end P02.LiteralShift
