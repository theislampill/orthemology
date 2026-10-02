import CandidateSource
import Sigma2RowLaw

/-! The recovered compile_sigma2 construction, using its exact first-block
register layout and the second fresh block obtained by a proved register
renaming. Binary sequence/skip normalizes source list sequences; byte/numeric
serialization is a separate boundary. -/
namespace P02A2.Sigma2Compiled
open P02A2.ObserverCore P02A2.LoopRenaming P02A2.LoopPrimrec
open P02A2.CandidateCompiler P02A2.CandidateSource P02A2.SurvivorCandidates
open P02A2.Sigma2SourceMatrix

def secondMap (base r : ℕ) : ℕ :=
  if r = 3 then 4 else if r = 4 then 3 else if r < 5 then r else r + (base-5)

@[simp] theorem secondMap_zero (base : ℕ) : secondMap base 0 = 0 := by simp [secondMap]
@[simp] theorem secondMap_one (base : ℕ) : secondMap base 1 = 1 := by simp [secondMap]
@[simp] theorem secondMap_three (base : ℕ) : secondMap base 3 = 4 := by simp [secondMap]
@[simp] theorem secondMap_four (base : ℕ) : secondMap base 4 = 3 := by simp [secondMap]

theorem secondMap_injective (base : ℕ) (hb : 5 ≤ base) : Function.Injective (secondMap base) := by
  intro a b he
  unfold secondMap at he
  split_ifs at he <;> omega

def secondBase (body : Stmt) (output : ℕ) : ℕ := 11 + (registerList body output).length

theorem renamedCandidate_value (ρ : ℕ → ℕ) (hρ : Function.Injective ρ)
    (body : Stmt) (output parameter : ℕ) (stage : Expr) (τ : Store) :
    exec (renameStmt ρ (sourceCandidate body output parameter stage)) τ (ρ 3) =
      candidate (matrix body output parameter) (evalExpr stage (fun r => τ (ρ r))) := by
  let code := sourceCandidate body output parameter stage
  let R := insert 3 (stmtRegs code)
  have hs : stmtRegs code ⊆ R := Finset.subset_insert _ _
  have h := exec_rename ρ code R hρ.injOn hs (fun r => τ (ρ r)) τ (fun _ _ => rfl)
  exact (h 3 (Finset.mem_insert_self _ _)).trans
    (sourceCandidate_value body output parameter stage (fun r => τ (ρ r)))

theorem renamedCandidate_preserves (ρ : ℕ → ℕ) (hρ : Function.Injective ρ)
    (body : Stmt) (output parameter : ℕ) (stage : Expr)
    (r : ℕ) (hr : r < 5) (h3 : r ≠ 3) :
    Preserves (renameStmt ρ (sourceCandidate body output parameter stage)) (ρ r) := by
  intro τ
  let code := sourceCandidate body output parameter stage
  let R := insert r (stmtRegs code)
  have hs : stmtRegs code ⊆ R := Finset.subset_insert _ _
  have h := exec_rename ρ code R hρ.injOn hs (fun j => τ (ρ j)) τ (fun _ _ => rfl)
  exact (h r (Finset.mem_insert_self _ _)).trans
    (sourceCandidate_preserves body output parameter stage r hr h3 (fun j => τ (ρ j)))

def previousBlock (body : Stmt) (output parameter : ℕ) : Stmt :=
  renameStmt (secondMap (secondBase body output))
    (sourceCandidate body output parameter (.sub (.reg 0) (.constant 1)))

theorem previousBlock_value (body : Stmt) (output parameter : ℕ) (τ : Store) :
    exec (previousBlock body output parameter) τ 4 =
      candidate (matrix body output parameter) (τ 0 - 1) := by
  have hρ := secondMap_injective (secondBase body output) (by unfold secondBase; omega)
  simpa only [previousBlock, secondMap_three, evalExpr, secondMap_zero] using
    renamedCandidate_value _ hρ body output parameter (.sub (.reg 0) (.constant 1)) τ

theorem previousBlock_preserves_zero (body : Stmt) (output parameter : ℕ) :
    Preserves (previousBlock body output parameter) 0 := by
  have hρ := secondMap_injective (secondBase body output) (by unfold secondBase; omega)
  simpa only [previousBlock, secondMap_zero] using
    renamedCandidate_preserves _ hρ body output parameter (.sub (.reg 0) (.constant 1)) 0 (by decide) (by decide)

theorem previousBlock_preserves_one (body : Stmt) (output parameter : ℕ) :
    Preserves (previousBlock body output parameter) 1 := by
  have hρ := secondMap_injective (secondBase body output) (by unfold secondBase; omega)
  simpa only [previousBlock, secondMap_one] using
    renamedCandidate_preserves _ hρ body output parameter (.sub (.reg 0) (.constant 1)) 1 (by decide) (by decide)

theorem previousBlock_preserves_three (body : Stmt) (output parameter : ℕ) :
    Preserves (previousBlock body output parameter) 3 := by
  have hρ := secondMap_injective (secondBase body output) (by unfold secondBase; omega)
  simpa only [previousBlock, secondMap_four] using
    renamedCandidate_preserves _ hρ body output parameter (.sub (.reg 0) (.constant 1)) 4 (by decide) (by decide)

def emitComparison : Stmt := .seq (.set 2 (.constant 0))
  (.branch (.eq (.reg 3) (.reg 4)) .skip (.set 2 (.mod (.reg 1) (.constant 2))))

theorem emitComparison_value (σ : Store) :
    exec emitComparison σ 2 = if σ 3 = σ 4 then 0 else σ 1 % 2 := by
  by_cases h : σ 3 = σ 4 <;> simp [emitComparison, exec, evalExpr, h]

def compiled (body : Stmt) (output parameter : ℕ) : Stmt :=
  .seq (sourceCandidate body output parameter (.reg 0))
    (.seq (.set 4 (.constant 0))
      (.seq (.branch (.reg 0) (previousBlock body output parameter) .skip) emitComparison))

theorem compiled_value (body : Stmt) (output parameter : ℕ) (σ : Store) :
    exec (compiled body output parameter) σ 2 =
      if innovation (matrix body output parameter) (σ 0) then σ 1 % 2 else 0 := by
  let σa := exec (sourceCandidate body output parameter (.reg 0)) σ
  let σb := Function.update σa 4 0
  let σc := if σb 0 = 0 then σb else exec (previousBlock body output parameter) σb
  have ha0 : σa 0 = σ 0 := sourceCandidate_preserves body output parameter (.reg 0) 0 (by decide) (by decide) σ
  have ha1 : σa 1 = σ 1 := sourceCandidate_preserves body output parameter (.reg 0) 1 (by decide) (by decide) σ
  have ha3 : σa 3 = candidate (matrix body output parameter) (σ 0) :=
    sourceCandidate_value body output parameter (.reg 0) σ
  have hb0 : σb 0 = σ 0 := by simpa [σb] using ha0
  have hb1 : σb 1 = σ 1 := by simpa [σb] using ha1
  have hb3 : σb 3 = candidate (matrix body output parameter) (σ 0) := by simpa [σb] using ha3
  have hc1 : σc 1 = σ 1 := by
    dsimp only [σc]
    split_ifs
    · exact hb1
    · exact (previousBlock_preserves_one body output parameter σb).trans hb1
  have hc3 : σc 3 = candidate (matrix body output parameter) (σ 0) := by
    dsimp only [σc]
    split_ifs
    · exact hb3
    · exact (previousBlock_preserves_three body output parameter σb).trans hb3
  have hc4 : σc 4 = previous (matrix body output parameter) (σ 0) := by
    dsimp only [σc]
    rw [hb0]
    by_cases h : σ 0 = 0
    · simp [h, σb, previous]
    · simp only [h, ↓reduceIte, previousBlock_value, hb0, previous]
  change exec emitComparison σc 2 = _
  rw [emitComparison_value, hc1, hc3, hc4]
  by_cases h : candidate (matrix body output parameter) (σ 0) = previous (matrix body output parameter) (σ 0)
  · simp [innovation, h]
  · simp [innovation, h]

def prefixValue (body : Stmt) (output parameter n word : ℕ) : ℕ :=
  exec (compiled body output parameter) (binaryStore n word) 2

theorem prefixValue_eq (body : Stmt) (output parameter n word : ℕ) :
    prefixValue body output parameter n word =
      P02A2.SurvivorPrimrec.prefixFunction (matrix body output) parameter n word := by
  simpa only [prefixValue, binaryStore, ↓reduceIte, Nat.one_ne_zero,
    P02A2.SurvivorPrimrec.prefixFunction] using compiled_value body output parameter (binaryStore n word)

def observer (body : Stmt) (output parameter : ℕ) := ObserverCore.output (prefixValue body output parameter)

theorem observer_eq (body : Stmt) (output parameter : ℕ) :
    observer body output parameter = P02A2.Sigma2RowLaw.observer (matrix body output) parameter := by
  funext x n
  unfold observer P02A2.Sigma2RowLaw.observer ObserverCore.output
  rw [prefixValue_eq]

noncomputable def law (body : Stmt) (output parameter : ℕ) :=
  P02A2.Q8Measure.fairCantor.map (observer body output parameter)

theorem law_eq (body : Stmt) (output parameter : ℕ) :
    law body output parameter = P02A2.Sigma2RowLaw.rowLaw (matrix body output) parameter := by
  unfold law P02A2.Sigma2RowLaw.rowLaw
  rw [observer_eq]

theorem zero_defect_iff (body : Stmt) (output parameter : ℕ) :
    defect (law body output parameter) = 0 ↔ ∃ s, ∀ t, matrix body output parameter s t := by
  rw [law_eq]
  exact P02A2.Sigma2RowLaw.defect_zero_iff_witness _ _

theorem one_defect_iff (body : Stmt) (output parameter : ℕ) :
    defect (law body output parameter) = 1 ↔ ¬ ∃ s, ∀ t, matrix body output parameter s t := by
  rw [law_eq]
  exact P02A2.Sigma2RowLaw.defect_one_iff_no_witness _ _

theorem prefixValue_primitive_recursive (body : Stmt) (output parameter : ℕ) :
    Primrec₂ (prefixValue body output parameter) := binary_program_primrec (compiled body output parameter) 2

end P02A2.Sigma2Compiled
