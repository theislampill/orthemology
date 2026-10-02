import EncodedPolicyHistory
import CallableSourceRuntime

/-! A literal bounded-history replay compiler. Its only semantic premises are
local source-step and final-readout certificates. The loop consumes a base-four
history word; no whole-trace or law certificate is assumed. -/
namespace Orthemology.RuntimeBridge.PhaseUpdate.HistoryFold
open Orthemology.Tranche2.PolicyEmbedding
open P02A2.ObserverCore P02A2.PRProgram
open Orthemology.RuntimeBridge.HistoryRuntime

abbrev History := Orthemology.Tranche2.PolicyEmbedding.History Bool Bool

/-- The acquired encoded history is in register0, the unconsumed word in1;
register2 is the bounded-loop index. Data occupies register3 onward. -/
def Matches {k : ℕ} (rep : History → Fin k → ℕ) (code : ℕ)
    (remaining accumulated : History) (σ : Store) : Prop :=
  σ 0 = code ∧ σ 1 = encodeHistory remaining ∧ ∀ j, σ (3+j.val) = rep accumulated j

def consume (state : History × History) : History × History :=
  match state.1 with
  | [] => state
  | e::h => (h,e::state.2)

/-- Exact finite list clock, including harmless padding at the sentinel. -/
theorem consume_complete (h acc : History) (n : ℕ) (hn : h.length ≤ n) :
    (consume^[n]) (h,acc) = ([],h.reverse ++ acc) := by
  induction h generalizing acc n with
  | nil =>
      induction n with
      | zero => rfl
      | succ n ih => simpa [Function.iterate_succ_apply,consume] using ih
  | cons e h ih =>
      cases n with
      | zero => simp at hn
      | succ n =>
          rw [Function.iterate_succ_apply]
          change (consume^[n]) (h,e::acc) = _
          rw [ih (e::acc) n (by simpa using hn)]
          simp [List.reverse_cons,List.append_assoc]

def foldBody (step : Stmt) : Stmt :=
  .branch (.le (.constant 4) (.reg 1))
    (.seq step (.set 1 (.div (.reg 1) (.constant 4)))) .skip

/-- A local source contract. It sees one accepted action/receipt digit and the
encoded finite sufficient statistics; it cannot assume a whole observed law. -/
def StepImplements {k : ℕ} (step : Stmt) (rep : History → Fin k → ℕ) : Prop :=
  ∀ code e remaining accumulated σ,
    Matches rep code (e::remaining) accumulated σ →
    Matches rep code (e::remaining) (e::accumulated) (exec step σ)

theorem fold_body_exact {k : ℕ} (step : Stmt) (rep : History → Fin k → ℕ)
    (hs : StepImplements step rep) (code : ℕ) (state : History × History) (σ : Store)
    (hm : Matches rep code state.1 state.2 σ) :
    Matches rep code (consume state).1 (consume state).2 (exec (foldBody step) σ) := by
  rcases state with ⟨remaining,accumulated⟩
  rcases hm with ⟨h0,h1,hd⟩
  cases remaining with
  | nil => simpa [foldBody,exec,evalExpr,h1,encodeHistory,consume,Matches] using And.intro h0 (And.intro h1 hd)
  | cons e h =>
      have hp := encoded_positive h
      have hge : 4 ≤ encodeHistory (e::h) := by
        simp only [encodeHistory,appendHistory]
        omega
      have ht := hs code e h accumulated σ ⟨h0,h1,hd⟩
      simp only [foldBody,exec,evalExpr,h1,hge,↓reduceIte]
      simp only [show ¬ (1 = 0) by decide,↓reduceIte]
      refine ⟨?_,?_,?_⟩
      · simpa using ht.1
      · change exec step σ 1 / 4 = encodeHistory h
        rw [ht.2.1]
        exact append_tail _ _ _
      · intro j
        rw [Function.update_of_ne (by omega : 3+j.val ≠ 1)]
        exact ht.2.2 j

theorem loop_exact {k : ℕ} (step : Stmt) (rep : History → Fin k → ℕ)
    (hs : StepImplements step rep) (code : ℕ) (state : History × History) (σ : Store)
    (hm : Matches rep code state.1 state.2 σ) (n : ℕ) :
    Matches rep code ((consume^[n]) state).1 ((consume^[n]) state).2
      (runLoop (exec (foldBody step)) 2 n σ) := by
  induction n with
  | zero => exact hm
  | succ n ih =>
      rw [Function.iterate_succ_apply']
      apply fold_body_exact step rep hs code ((consume^[n]) state)
      refine ⟨?_,?_,?_⟩
      · simpa using ih.1
      · simpa using ih.2.1
      · intro j
        rw [Function.update_of_ne (by omega : 3+j.val ≠ 2)]
        exact ih.2.2 j

theorem length_le_code (h : History) : h.length ≤ encodeHistory h := by
  induction h with
  | nil => simp
  | cons e h ih =>
      have hp := encoded_positive h
      simp only [List.length_cons,encodeHistory,appendHistory]
      omega

def reverseStep : Stmt :=
  .set 3 (.add (.mul (.constant 4) (.reg 3)) (.mod (.reg 1) (.constant 4)))

def reverseRep (h : History) : Fin 1 → ℕ := fun _ => encodeHistory h

theorem append_digit (h : ℕ) (a y : Bool) :
    appendHistory h a y % 4 = 2*Orthemology.RuntimeBridge.bitNat a + Orthemology.RuntimeBridge.bitNat y := by
  cases a <;> cases y <;> simp [appendHistory,Orthemology.RuntimeBridge.bitNat,Nat.add_mod,Nat.mul_mod]

theorem reverse_step_exact : StepImplements reverseStep reverseRep := by
  intro code e remaining accumulated σ hm
  rcases hm with ⟨h0,h1,hd⟩
  refine ⟨?_,?_,?_⟩
  · simpa [reverseStep,exec] using h0
  · simpa [reverseStep,exec] using h1
  · intro j
    have hj : j = 0 := Subsingleton.elim _ _
    subst j
    simp only [reverseStep,exec,evalExpr,show 3+((0:Fin 1):ℕ)=3 by rfl,Function.update_self]
    have h3 : σ 3 = encodeHistory accumulated := hd 0
    rw [h3,h1]
    change 4*encodeHistory accumulated + appendHistory (encodeHistory remaining) e.1 e.2 % 4 =
      appendHistory (encodeHistory accumulated) e.1 e.2
    rw [append_digit]
    simp only [appendHistory]
    omega

def reverseProgram : Program 1 :=
  ⟨.seq (.set 1 (.reg 0)) (.seq (.set 3 (.constant 1))
    (.loop 2 (.reg 0) (foldBody reverseStep))),3⟩

theorem reverse_source_exact (h : History) :
    denote reverseProgram ![encodeHistory h] = encodeHistory h.reverse := by
  let σ := exec (.seq (.set 1 (.reg 0)) (.set 3 (.constant 1)))
    (P02A2.LoopPrimrec.extend ![encodeHistory h])
  have hm : Matches reverseRep (encodeHistory h) h [] σ := by
    refine ⟨?_,?_,?_⟩
    · simp [σ,exec,evalExpr,P02A2.LoopPrimrec.extend]
    · simp [σ,exec,evalExpr,P02A2.LoopPrimrec.extend]
    · intro j
      have hj : j = 0 := Subsingleton.elim _ _
      subst j
      simp [σ,exec,evalExpr,reverseRep,encodeHistory]
  have hl := loop_exact reverseStep reverseRep reverse_step_exact (encodeHistory h)
    (h,[]) σ hm (encodeHistory h)
  rw [consume_complete h [] (encodeHistory h) (length_le_code h)] at hl
  have hd := hl.2.2 0
  simpa only [List.append_nil,reverseRep] using hd

/-- Initial data source runs after the reversed word is installed. -/
def InitImplements {k : ℕ} (init : Stmt) (rep : History → Fin k → ℕ) : Prop :=
  ∀ code remaining σ, σ 0 = code → σ 1 = encodeHistory remaining →
    Matches rep code remaining [] (exec init σ)

def ReadoutImplements {k : ℕ} (readout : Program k) (rep : History → Fin k → ℕ)
    (policy : History → Bool) : Prop :=
  ∀ h, denote readout (rep h) = Orthemology.RuntimeBridge.bitNat (policy h)

def dataArgs (k : ℕ) : Fin k → Expr := fun j => .reg (3+j.val)

theorem data_args_fresh (k : ℕ) :
    ∀ i r, r ∈ P02A2.LoopRenaming.exprRegs (dataArgs k i) → r < k+4 := by
  intro i r hr
  simp only [dataArgs,P02A2.LoopRenaming.exprRegs,Finset.mem_singleton] at hr
  subst r
  omega

def reverseArgs : Fin 1 → Expr := ![.reg 0]

theorem reverse_args_fresh (k : ℕ) :
    ∀ i r, r ∈ P02A2.LoopRenaming.exprRegs (reverseArgs i) → r < k+4 := by
  intro i r hr
  have hi : i = 0 := Subsingleton.elim _ _
  subst i
  simp [reverseArgs,P02A2.LoopRenaming.exprRegs] at hr
  omega

/-- Actual arity-one source compiler for any finite sufficient-statistic vector.
The bound is the supplied history numeral; this is total but not a claim of
practical source fuel or a polynomial-time implementation. -/
def compiled {k : ℕ} (init step : Stmt) (readout : Program k) : Program 1 :=
  ⟨.seq (call reverseProgram (k+4) reverseArgs 1)
    (.seq init (.seq (.loop 2 (.reg 0) (foldBody step))
      (call readout (k+4) (dataArgs k) (k+3)))),k+3⟩

theorem compiled_history_exact {k : ℕ} (init step : Stmt) (readout : Program k)
    (rep : History → Fin k → ℕ) (policy : History → Bool)
    (hi : InitImplements init rep) (hs : StepImplements step rep)
    (ho : ReadoutImplements readout rep policy) (h : History) :
    denote (compiled init step readout) ![encodeHistory h] = Orthemology.RuntimeBridge.bitNat (policy h) := by
  let σ := P02A2.LoopPrimrec.extend ![encodeHistory h]
  let τ := exec (call reverseProgram (k+4) reverseArgs 1) σ
  have h0 : τ 0 = encodeHistory h := by
    dsimp only [τ]
    rw [call_frame _ _ _ _ (reverse_args_fresh k) 0 (by omega) (by decide)]
    simp [σ,P02A2.LoopPrimrec.extend]
  have h1 : τ 1 = encodeHistory h.reverse := by
    dsimp only [τ]
    rw [call_value _ _ _ _ (reverse_args_fresh k)]
    have ha : (fun i => evalExpr (reverseArgs i) σ) = ![encodeHistory h] := by
      funext i
      have he : i = 0 := Subsingleton.elim _ _
      subst i
      simp [reverseArgs,σ,evalExpr,P02A2.LoopPrimrec.extend]
    rw [ha,reverse_source_exact]
  have hm := hi (encodeHistory h) h.reverse τ h0 h1
  have hl := loop_exact step rep hs (encodeHistory h) (h.reverse,[]) (exec init τ) hm (encodeHistory h)
  rw [consume_complete h.reverse [] (encodeHistory h) (by simpa using length_le_code h)] at hl
  simp only [List.reverse_reverse,List.append_nil] at hl
  change exec (call readout (k+4) (dataArgs k) (k+3))
    (runLoop (exec (foldBody step)) 2 ((exec init τ) 0) (exec init τ)) (k+3) = _
  rw [hm.1,call_value _ _ _ _ (data_args_fresh k)]
  have ha : (fun i => evalExpr (dataArgs k i)
      (runLoop (exec (foldBody step)) 2 (encodeHistory h) (exec init τ))) = rep h := by
    funext i
    exact hl.2.2 i
  rw [ha,ho h]

end Orthemology.RuntimeBridge.PhaseUpdate.HistoryFold
