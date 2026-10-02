import CandidateCompiler
import Sigma2SourceMatrix

/-! Bind the candidate control proof to the source Builder.inline allocation.
Registers are the sorted union of arity-three inputs, output and all syntax
registers; fresh addresses are 11 plus each register's index in that list. -/
namespace P02A2.CandidateSource
open P02A2.ObserverCore P02A2.LoopRenaming P02A2.LoopPrimrec
open P02A2.CandidateCompiler P02A2.Sigma2SourceMatrix

def registerSet (body : Stmt) (output : ℕ) : Finset ℕ :=
  Finset.range 3 ∪ insert output (stmtRegs body)

def registerList (body : Stmt) (output : ℕ) : List ℕ := (registerSet body output).sort (· ≤ ·)

def registerMap (body : Stmt) (output : ℕ) (r : ℕ) : ℕ :=
  11 + (registerList body output).idxOf r

def matrixValue (body : Stmt) (output parameter s t : ℕ) : ℕ :=
  exec body (extend (tripleInput ((parameter,s),t))) output

def matrixCall (body : Stmt) (output parameter : ℕ) : Stmt :=
  inlineCode (registerMap body output) (registerList body output)
    [(0,.constant parameter),(1,.reg 6),(2,.reg 7)] body output 10

theorem registerList_mem (body : Stmt) (output r : ℕ) :
    r ∈ registerList body output ↔ r ∈ registerSet body output := Finset.mem_sort _

theorem registerMap_injective_on (body : Stmt) (output : ℕ) :
    Set.InjOn (registerMap body output) (↑(registerList body output).toFinset : Set ℕ) := by
  intro r hr s hs he
  apply (List.idxOf_inj (List.mem_toFinset.mp hr) (List.mem_toFinset.mp hs)).mp
  exact Nat.add_left_cancel he

theorem registerMap_fresh (body : Stmt) (output r : ℕ) : 11 ≤ registerMap body output r :=
  Nat.le_add_right 11 _

theorem controller_not_private (body : Stmt) (output r : ℕ) (hr : r < 11) :
    r ∉ (registerList body output).toFinset.image (registerMap body output) := by
  intro h
  rcases Finset.mem_image.mp h with ⟨s,hs,he⟩
  have hf := registerMap_fresh body output s
  omega

theorem matrixArgs_fresh (body : Stmt) (output parameter : ℕ) :
    ArgsFresh (registerList body output).toFinset (registerMap body output)
      [(0,.constant parameter),(1,.reg 6),(2,.reg 7)] := by
  intro a ha
  have hinputs (r : ℕ) (hr : r < 3) : r ∈ (registerList body output).toFinset := by
    apply List.mem_toFinset.mpr
    apply (registerList_mem body output r).mpr
    exact Finset.mem_union_left _ (Finset.mem_range.mpr hr)
  simp only [List.mem_cons, List.mem_nil_iff, or_false] at ha
  rcases ha with rfl | rfl | rfl
  · exact ⟨hinputs 0 (by decide), by simp [exprRegs]⟩
  · exact ⟨hinputs 1 (by decide), by
      simpa [exprRegs] using controller_not_private body output 6 (by decide)⟩
  · exact ⟨hinputs 2 (by decide), by
      simpa [exprRegs] using controller_not_private body output 7 (by decide)⟩

theorem matrix_sourceLoad (parameter : ℕ) (σ : Store) :
    sourceLoad [(0,.constant parameter),(1,.reg 6),(2,.reg 7)] σ (fun _ => 0) =
      extend (tripleInput ((parameter,σ 6),σ 7)) := by
  funext r
  by_cases h0 : r = 0
  · subst r; simp [sourceLoad, evalExpr, extend, tripleInput]
  · by_cases h1 : r = 1
    · subst r; simp [sourceLoad, evalExpr, extend, tripleInput]
    · by_cases h2 : r = 2
      · subst r; simp [sourceLoad, evalExpr, extend, tripleInput]
      · have h3 : ¬ r < 3 := by omega
        simp [sourceLoad, evalExpr, extend, h0, h1, h2, h3, Function.update_apply]

theorem matrixCall_spec (body : Stmt) (output parameter : ℕ) :
    CallSpec (matrixCall body output parameter) (matrixValue body output parameter) := by
  have hb : stmtRegs body ⊆ (registerList body output).toFinset := by
    intro r hr
    apply List.mem_toFinset.mpr
    apply (registerList_mem body output r).mpr
    exact Finset.mem_union_right _ (Finset.mem_insert_of_mem hr)
  have ho : output ∈ (registerList body output).toFinset := by
    apply List.mem_toFinset.mpr
    apply (registerList_mem body output output).mpr
    exact Finset.mem_union_right _ (Finset.mem_insert_self _ _)
  have hc (σ : Store) := inlineCode_correct (registerMap body output) (registerList body output)
    [(0,.constant parameter),(1,.reg 6),(2,.reg 7)] body output 10
    (registerMap_injective_on body output) hb ho (matrixArgs_fresh body output parameter) σ
  constructor
  · intro σ
    have he := (hc σ).1
    rw [matrix_sourceLoad] at he
    exact he
  · intro σ r hr
    exact (hc σ).2 r (by omega) (controller_not_private body output r (by omega))

def sourceCandidate (body : Stmt) (output parameter : ℕ) (stage : Expr) : Stmt :=
  candidateBlock (matrixCall body output parameter) stage

theorem sourceCandidate_value (body : Stmt) (output parameter : ℕ) (stage : Expr) (σ : Store) :
    exec (sourceCandidate body output parameter stage) σ 3 =
      P02A2.SurvivorCandidates.candidate (matrix body output parameter) (evalExpr stage σ) :=
  candidateBlock_value _ _ (matrixCall_spec body output parameter) stage σ

theorem sourceCandidate_preserves (body : Stmt) (output parameter : ℕ) (stage : Expr)
    (r : ℕ) (hr : r < 5) (h3 : r ≠ 3) : Preserves (sourceCandidate body output parameter stage) r :=
  candidateBlock_preserves _ _ (matrixCall_spec body output parameter) stage r hr h3

end P02A2.CandidateSource
