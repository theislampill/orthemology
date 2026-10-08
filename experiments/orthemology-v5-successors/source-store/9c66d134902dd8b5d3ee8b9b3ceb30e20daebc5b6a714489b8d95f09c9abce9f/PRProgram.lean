import LoopPrimrec

/-! Concrete callable programs in the unchanged P02-L1 grammar. Private
register blocks are reset before every invocation. The following is an
explicit compiler construction, not a semantic oracle expression. -/
namespace P02A2.PRProgram
open P02A2.ObserverCore P02A2.LoopRenaming P02A2.LoopPrimrec

structure Program (arity : ℕ) where
  body : Stmt
  output : ℕ

def denote {k : ℕ} (p : Program k) (args : Fin k → ℕ) : ℕ := exec p.body (extend args) p.output

def inputAssignments {k : ℕ} (args : Fin k → Expr) : List (ℕ × Expr) :=
  List.ofFn (fun i => (i.val,args i))

theorem sourceLoad_targets (assignments : List (ℕ × Expr)) (caller initial target : Store)
    (hv : ∀ a ∈ assignments, evalExpr a.2 caller = target a.1)
    (hi : ∀ r, r ∉ assignments.map Prod.fst → initial r = target r) :
    sourceLoad assignments caller initial = target := by
  induction assignments generalizing initial with
  | nil => funext r; exact hi r (by simp)
  | cons a assignments ih =>
      apply ih
      · intro b hb
        exact hv b (List.mem_cons_of_mem _ hb)
      · intro r hr
        by_cases he : r = a.1
        · subst r
          simpa [Function.update_self] using hv a (by simp)
        · rw [Function.update_of_ne he]
          apply hi r
          simpa [he] using hr

theorem sourceLoad_inputs {k : ℕ} (args : Fin k → Expr) (caller : Store) :
    sourceLoad (inputAssignments args) caller (fun _ => 0) =
      extend (fun i => evalExpr (args i) caller) := by
  apply sourceLoad_targets
  · intro a ha
    rcases List.mem_ofFn.mp ha with ⟨i,he⟩
    rw [← he]
    simp [extend, i.isLt]
  · intro r hr
    have hn : ¬ r < k := by
      intro h
      apply hr
      exact List.mem_map.mpr ⟨(r,args ⟨r,h⟩), List.mem_ofFn.mpr ⟨⟨r,h⟩,rfl⟩,rfl⟩
    simp [extend, hn]

def bound {k : ℕ} (p : Program k) : ℕ := programBound k p.body p.output

def call {k : ℕ} (p : Program k) (start : ℕ) (args : Fin k → Expr) (destination : ℕ) : Stmt :=
  inlineCode (fun r => start+r) (List.range (bound p)) (inputAssignments args) p.body p.output destination

theorem call_correct {k : ℕ} (p : Program k) (start : ℕ) (args : Fin k → Expr) (destination : ℕ)
    (hfresh : ∀ i r, r ∈ exprRegs (args i) → r < start) (caller : Store) :
    exec (call p start args destination) caller destination =
      denote p (fun i => evalExpr (args i) caller) ∧
    ∀ r, r < start → r ≠ destination → exec (call p start args destination) caller r = caller r := by
  let R := (List.range (bound p)).toFinset
  have hR : R = Finset.range (bound p) := by
    ext r
    simp only [R, List.mem_toFinset, List.mem_range, Finset.mem_range]
  have hρ : Set.InjOn (fun r => start+r) (↑R : Set ℕ) := by
    intro a ha b hb he
    exact Nat.add_left_cancel he
  have hb : stmtRegs p.body ⊆ R := by
    rw [hR]
    exact programBound_registers k p.body p.output
  have hout : p.output ∈ R := by
    rw [hR]
    exact Finset.mem_range.mpr (programBound_output k p.body p.output)
  have ha : ArgsFresh R (fun r => start+r) (inputAssignments args) := by
    intro a ha
    rcases List.mem_ofFn.mp ha with ⟨i,he⟩
    rw [← he]
    constructor
    · rw [hR]
      exact Finset.mem_range.mpr (lt_of_lt_of_le i.isLt (programBound_arity k p.body p.output))
    · apply Finset.disjoint_left.mpr
      intro r hr himage
      rcases Finset.mem_image.mp himage with ⟨j,hj,heq⟩
      have hlt := hfresh i r hr
      omega
  have h := inlineCode_correct (fun r => start+r) (List.range (bound p)) (inputAssignments args)
    p.body p.output destination hρ hb hout ha caller
  constructor
  · have he := h.1
    rw [sourceLoad_inputs] at he
    exact he
  · intro r hr hdest
    apply h.2 r hdest
    intro himage
    rcases Finset.mem_image.mp himage with ⟨j,hj,he⟩
    omega

theorem call_value {k : ℕ} (p : Program k) (start : ℕ) (args : Fin k → Expr) (destination : ℕ)
    (hfresh : ∀ i r, r ∈ exprRegs (args i) → r < start) (caller : Store) :
    exec (call p start args destination) caller destination = denote p (fun i => evalExpr (args i) caller) :=
  (call_correct p start args destination hfresh caller).1

theorem call_frame {k : ℕ} (p : Program k) (start : ℕ) (args : Fin k → Expr) (destination : ℕ)
    (hfresh : ∀ i r, r ∈ exprRegs (args i) → r < start)
    (r : ℕ) (hr : r < start) (hdest : r ≠ destination) (caller : Store) :
    exec (call p start args destination) caller r = caller r :=
  (call_correct p start args destination hfresh caller).2 r hr hdest

def zeroProgram (k : ℕ) : Program k := ⟨.set k (.constant 0), k⟩
def successorProgram : Program 1 := ⟨.set 1 (.add (.reg 0) (.constant 1)), 1⟩
def projectionProgram (k : ℕ) (i : Fin k) : Program k := ⟨.set k (.reg i.val), k⟩

theorem zeroProgram_correct (k : ℕ) (args : Fin k → ℕ) : denote (zeroProgram k) args = 0 := by
  simp [denote, zeroProgram, exec, evalExpr]

theorem successorProgram_correct (args : Fin 1 → ℕ) : denote successorProgram args = args 0 + 1 := by
  simp [denote, successorProgram, exec, evalExpr, extend]

theorem projectionProgram_correct (k : ℕ) (i : Fin k) (args : Fin k → ℕ) :
    denote (projectionProgram k i) args = args i := by
  simp [denote, projectionProgram, exec, evalExpr, extend, i.isLt]

def sequence : List Stmt → Stmt
  | [] => .skip
  | s::ss => .seq s (sequence ss)

theorem exec_sequence (ss : List Stmt) (σ : Store) :
    exec (sequence ss) σ = ss.foldl (fun τ s => exec s τ) σ := by
  induction ss generalizing σ with
  | nil => rfl
  | cons s ss ih => exact ih (exec s σ)

end P02A2.PRProgram
