import LoopRenaming
import Mathlib.Computability.Primrec

/-! Fixed-program primitive-recursive denotations for the actual LOOP grammar.
The finite-register evaluator is proved to simulate ObserverCore on every
program whose used registers fit the chosen bound. This is not a uniformly
primitive-recursive universal evaluator indexed by arbitrary program code. -/
namespace P02A2.LoopPrimrec
open P02A2.ObserverCore P02A2.LoopRenaming

abbrev FinStore (k : ℕ) := Fin k → ℕ

def extend {k : ℕ} (σ : FinStore k) : Store :=
  fun r => if hr : r < k then σ ⟨r,hr⟩ else 0

def writeFin {k : ℕ} (r : ℕ) (σ : FinStore k) (v : ℕ) : FinStore k :=
  fun i => if i.val = r then v else σ i

theorem read_primrec (k r : ℕ) : Primrec (fun σ : FinStore k => extend σ r) := by
  by_cases hr : r < k
  · simpa [extend, hr] using (Primrec.fin_app.comp Primrec.id (Primrec.const (⟨r,hr⟩ : Fin k)))
  · simpa [extend, hr] using (Primrec.const (α := FinStore k) 0)

theorem writeFin_primrec (k r : ℕ) : Primrec₂ (@writeFin k r) := by
  change Primrec (fun p : FinStore k × ℕ => writeFin r p.1 p.2)
  apply Primrec.fin_curry.mpr
  apply Primrec₂.swap
  apply Primrec.fin_curry₁.mpr
  intro i
  by_cases hi : i.val = r
  · simpa [writeFin, hi] using (Primrec.snd : Primrec (fun p : FinStore k × ℕ => p.2))
  · simpa [writeFin, hi] using
      (Primrec.fin_app.comp (Primrec.fst : Primrec (fun p : FinStore k × ℕ => p.1)) (Primrec.const i))

theorem evalExpr_primrec (k : ℕ) (e : Expr) :
    Primrec (fun σ : FinStore k => evalExpr e (extend σ)) := by
  induction e with
  | constant n => exact Primrec.const n
  | reg r => exact read_primrec k r
  | add a b iha ihb => exact Primrec.nat_add.comp iha ihb
  | sub a b iha ihb => exact Primrec.nat_sub.comp iha ihb
  | mul a b iha ihb => exact Primrec.nat_mul.comp iha ihb
  | div a b iha ihb => exact Primrec.nat_div.comp iha ihb
  | mod a b iha ihb => exact Primrec.nat_mod.comp iha ihb
  | le a b iha ihb => exact Primrec.ite (Primrec.nat_le.comp iha ihb) (Primrec.const 1) (Primrec.const 0)
  | eq a b iha ihb => exact Primrec.ite (Primrec.eq.comp iha ihb) (Primrec.const 1) (Primrec.const 0)
  | pow2 a ih => exact (Primrec₂.unpaired'.mp Nat.Primrec.pow).comp (Primrec.const 2) ih

def runLoopFin {k : ℕ} (body : FinStore k → FinStore k) (r : ℕ) : ℕ → FinStore k → FinStore k
  | 0,σ => σ
  | n+1,σ => body (writeFin r (runLoopFin body r n σ) n)

def execFin (k : ℕ) : Stmt → FinStore k → FinStore k
  | .skip,σ => σ
  | .set r e,σ => writeFin r σ (evalExpr e (extend σ))
  | .seq s t,σ => execFin k t (execFin k s σ)
  | .loop r e s,σ => runLoopFin (execFin k s) r (evalExpr e (extend σ)) σ
  | .branch e s t,σ => if evalExpr e (extend σ)=0 then execFin k t σ else execFin k s σ

theorem runLoopFin_primrec (k r : ℕ) (body : FinStore k → FinStore k)
    (hb : Primrec body) : Primrec₂ (fun σ n => runLoopFin body r n σ) := by
  have hg : Primrec₂ (fun (_ : FinStore k) (p : ℕ × FinStore k) => body (writeFin r p.2 p.1)) :=
    (hb.comp ((writeFin_primrec k r).comp (Primrec.snd.comp Primrec.snd)
      (Primrec.fst.comp Primrec.snd))).to₂
  apply (Primrec.nat_rec Primrec.id hg).of_eq
  intro σ n
  induction n with
  | zero => rfl
  | succ n ih => simpa only [Nat.rec_add_one, runLoopFin, ih]

theorem execFin_primrec (k : ℕ) (s : Stmt) : Primrec (execFin k s) := by
  induction s with
  | skip => exact Primrec.id
  | set r e => exact (writeFin_primrec k r).comp Primrec.id (evalExpr_primrec k e)
  | seq s t ihs iht => exact iht.comp ihs
  | loop r e s ih => exact (runLoopFin_primrec k r _ ih).comp Primrec.id (evalExpr_primrec k e)
  | branch e s t ihs iht =>
      exact Primrec.ite (Primrec.eq.comp (evalExpr_primrec k e) (Primrec.const 0)) iht ihs

theorem extend_writeFin {k r : ℕ} (hr : r < k) (σ : FinStore k) (v : ℕ) :
    extend (writeFin r σ v) = Function.update (extend σ) r v := by
  funext j
  by_cases hj : j < k
  · by_cases he : j = r
    · subst j
      simp [extend, writeFin, hr]
    · simp [extend, writeFin, hj, he, Function.update_apply]
  · have he : j ≠ r := by intro he; subst j; exact hj hr
    simp [extend, hj, he, Function.update_apply]

theorem runLoopFin_simulation {k r : ℕ} (hr : r < k)
    (bodyFin : FinStore k → FinStore k) (body : Store → Store)
    (hb : ∀ σ, extend (bodyFin σ) = body (extend σ)) (n : ℕ) (σ : FinStore k) :
    extend (runLoopFin bodyFin r n σ) = runLoop body r n (extend σ) := by
  induction n with
  | zero => rfl
  | succ n ih => rw [runLoopFin, hb, extend_writeFin hr, ih, runLoop]

theorem execFin_simulation (k : ℕ) (s : Stmt) (hR : stmtRegs s ⊆ Finset.range k)
    (σ : FinStore k) : extend (execFin k s σ) = exec s (extend σ) := by
  induction s generalizing σ with
  | skip => rfl
  | set r e =>
      have hr : r < k := Finset.mem_range.mp ((Finset.insert_subset_iff.mp hR).1)
      exact extend_writeFin hr σ _
  | seq s t ihs iht =>
      have hs := (Finset.union_subset_iff.mp hR).1
      have ht := (Finset.union_subset_iff.mp hR).2
      simp only [execFin, exec, iht ht, ihs hs]
  | loop r e s ih =>
      have hr : r < k := Finset.mem_range.mp ((Finset.insert_subset_iff.mp hR).1)
      have hs := (Finset.union_subset_iff.mp (Finset.insert_subset_iff.mp hR).2).2
      exact runLoopFin_simulation hr _ _ (fun σ => ih hs σ) _ σ
  | branch e s t ihs iht =>
      have hs := (Finset.union_subset_iff.mp (Finset.union_subset_iff.mp hR).2).1
      have ht := (Finset.union_subset_iff.mp (Finset.union_subset_iff.mp hR).2).2
      simp only [execFin, exec]
      split_ifs
      · exact iht ht σ
      · exact ihs hs σ

theorem fixed_program_primrec (k : ℕ) (s : Stmt) (output : Fin k)
    (hR : stmtRegs s ⊆ Finset.range k) :
    Primrec (fun σ : FinStore k => exec s (extend σ) output.val) := by
  apply (Primrec.fin_app.comp (execFin_primrec k s) (Primrec.const output)).of_eq
  intro σ
  have h := congrFun (execFin_simulation k s hR σ) output.val
  simpa [extend, output.isLt] using h

def programBound (arity : ℕ) (s : Stmt) (output : ℕ) : ℕ :=
  max arity (max output ((stmtRegs s).sup id)) + 1

theorem programBound_registers (arity : ℕ) (s : Stmt) (output : ℕ) :
    stmtRegs s ⊆ Finset.range (programBound arity s output) := by
  intro r hr
  apply Finset.mem_range.mpr
  have hs : r ≤ (stmtRegs s).sup id := Finset.le_sup (f := id) hr
  unfold programBound
  omega

theorem programBound_output (arity : ℕ) (s : Stmt) (output : ℕ) :
    output < programBound arity s output := by unfold programBound; omega

theorem programBound_arity (arity : ℕ) (s : Stmt) (output : ℕ) :
    arity ≤ programBound arity s output := by unfold programBound; omega

def inputFin {arity : ℕ} (k : ℕ) (args : FinStore arity) : FinStore k :=
  fun i => extend args i.val

theorem inputFin_primrec (arity k : ℕ) : Primrec (@inputFin arity k) := by
  apply Primrec.fin_curry.mpr
  apply Primrec₂.swap
  apply Primrec.fin_curry₁.mpr
  intro i
  exact read_primrec arity i.val

theorem extend_inputFin {arity k : ℕ} (hk : arity ≤ k) (args : FinStore arity) :
    extend (inputFin k args) = extend args := by
  funext r
  by_cases hrk : r < k
  · simp [extend, inputFin, hrk]
  · have hra : ¬ r < arity := by omega
    simp [extend, hrk, hra]

theorem program_denotation_primrec (arity : ℕ) (s : Stmt) (output : ℕ) :
    Primrec (fun args : FinStore arity => exec s (extend args) output) := by
  let k := programBound arity s output
  let o : Fin k := ⟨output, programBound_output arity s output⟩
  have hp := (fixed_program_primrec k s o (programBound_registers arity s output)).comp
    (inputFin_primrec arity k)
  apply hp.of_eq
  intro args
  rw [extend_inputFin (programBound_arity arity s output)]

def binaryInput (p : ℕ × ℕ) : FinStore 2 :=
  fun i => if i.val = 0 then p.1 else p.2

def binaryStore (stage word r : ℕ) : ℕ :=
  if r = 0 then stage else if r = 1 then word else 0

theorem binaryInput_primrec : Primrec binaryInput := by
  apply Primrec.fin_curry.mpr
  apply Primrec₂.swap
  apply Primrec.fin_curry₁.mpr
  intro i
  fin_cases i
  · simpa [binaryInput] using (Primrec.fst : Primrec (fun p : ℕ × ℕ => p.1))
  · simpa [binaryInput] using (Primrec.snd : Primrec (fun p : ℕ × ℕ => p.2))

theorem extend_binaryInput (p : ℕ × ℕ) : extend (binaryInput p) = binaryStore p.1 p.2 := by
  funext r
  by_cases h0 : r = 0
  · subst r; simp [extend, binaryInput, binaryStore]
  · by_cases h1 : r = 1
    · subst r; simp [extend, binaryInput, binaryStore]
    · have h2 : ¬ r < 2 := by omega
      simp [extend, binaryStore, h0, h1, h2]

theorem binary_program_primrec (s : Stmt) (output : ℕ) :
    Primrec₂ (fun stage word => exec s (binaryStore stage word) output) := by
  apply ((program_denotation_primrec 2 s output).comp binaryInput_primrec).of_eq
  intro p
  rw [extend_binaryInput]

end P02A2.LoopPrimrec
