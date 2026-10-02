import NaturalStateCompiler
set_option linter.unnecessarySeqFocus false

/-! A source-programmable rational environment wrapper around an unbounded
encoded observed-history policy. The policy program is common across models;
only the environment threshold is model-indexed. -/
namespace Orthemology.RuntimeBridge.HistoryRuntime
set_option linter.unnecessarySeqFocus false
open Orthemology.Frontier Orthemology.Frontier.MealyMeasure
open P02A2.ObserverCore P02A2.PRProgram P02.Codec
open Orthemology.CertifiedObserver

/-- Base-four sentinel encodes chronological action/receipt pairs. -/
def appendHistory (h : ℕ) (a y : Bool) : ℕ := 4*h + 2*bitNat a + bitNat y

def observedState (h : ℕ) : Bool := if h = 1 then false else decide (h % 2 = 1)
def policyHistory (q : ℕ) : ℕ := q / 64 / 3

def corePhase (q : ℕ) : ℕ := q / 64 % 3
def framePhase (q : ℕ) : ℕ := q % 4
def storedFrame (q : ℕ) : ℕ := q / 4 % 16

def proposal (q : ℕ) (b : Bool) : ℕ := 2*(corePhase q-1) + bitNat b

def accepts (q : ℕ) (b : Bool) : Bool := decide (corePhase q ≠ 0 ∧ proposal q b ≤ 2)
def receipt (σ a : Bool) (q : ℕ) (b : Bool) : Bool := decide (1+bitNat (decide (a=σ)) ≤ proposal q b)

def eventCode (σ : Bool) (a : ℕ → Bool) (q : ℕ) (b : Bool) : ℕ :=
  8*bitNat (accepts q b) + 4*bitNat (observedState (policyHistory q)) +
  2*bitNat (a (policyHistory q)) + bitNat (accepts q b)*bitNat (receipt σ (a (policyHistory q)) q b)

def coreNext (σ : Bool) (a : ℕ → Bool) (q : ℕ) (b : Bool) : ℕ :=
  if corePhase q = 0 then 3*policyHistory q + 1 + bitNat b
  else if accepts q b then 3*appendHistory (policyHistory q) (a (policyHistory q)) (receipt σ (a (policyHistory q)) q b)
  else 3*policyHistory q

def machine (σ : Bool) (a : ℕ → Bool) : Mealy ℕ where
  next q b := if framePhase q = 0 then 64*coreNext σ a q b + 4*eventCode σ a q b + 1
    else if framePhase q = 3 then 64*(q/64) else q+1
  out q b := if framePhase q = 0 then decide (eventCode σ a q b / 8 % 2 = 1)
    else decide (storedFrame q / 2^(3-framePhase q) % 2 = 1)

/-- A fixed positive initial history and zero sampler/frame phase. -/
def initial : ℕ := 64*3

-- Actual P02 expression compilation. Caller inputs are config 0 and bit 1;
-- only register 6 receives the policy's result from a reset private call.
def histExpr : Expr := .div (.div (.reg 0) (.constant 64)) (.constant 3)
def phaseExpr : Expr := .mod (.div (.reg 0) (.constant 64)) (.constant 3)
def frameExpr : Expr := .mod (.reg 0) (.constant 4)
def storedExpr : Expr := .mod (.div (.reg 0) (.constant 4)) (.constant 16)
def propExpr : Expr := .add (.mul (.constant 2) (.sub phaseExpr (.constant 1))) (.reg 1)
def startExpr : Expr := .eq phaseExpr (.constant 0)
def acceptExpr : Expr := .mul (.sub (.constant 1) startExpr) (.le propExpr (.constant 2))
def receiptExpr (σ : Bool) : Expr := .le (.add (.constant 1) (.eq (.reg 6) (.constant (bitNat σ)))) propExpr
def sourceExpr : Expr := .mul (.sub (.constant 1) (.eq histExpr (.constant 1))) (.mod histExpr (.constant 2))
def eventExpr (σ : Bool) : Expr :=
  .add (.add (.add (.mul (.constant 8) acceptExpr) (.mul (.constant 4) sourceExpr))
    (.mul (.constant 2) (.reg 6))) (.mul acceptExpr (receiptExpr σ))
def coreExpr (σ : Bool) : Expr :=
  .add (.mul startExpr (.add (.add (.mul (.constant 3) histExpr) (.constant 1)) (.reg 1)))
    (.mul (.sub (.constant 1) startExpr)
      (.add (.mul (.constant 3) histExpr)
        (.mul acceptExpr (.add (.add (.mul (.constant 9) histExpr) (.mul (.constant 6) (.reg 6)))
          (.mul (.constant 3) (receiptExpr σ))))))

def nextBody (σ : Bool) : Stmt :=
  .branch (.eq frameExpr (.constant 0))
    (.set 2 (.add (.add (.mul (.constant 64) (coreExpr σ)) (.mul (.constant 4) (eventExpr σ))) (.constant 1)))
    (.branch (.eq frameExpr (.constant 3))
      (.set 2 (.mul (.constant 64) (.div (.reg 0) (.constant 64))))
      (.set 2 (.add (.reg 0) (.constant 1))))

def outputBody (σ : Bool) : Stmt :=
  .branch (.eq frameExpr (.constant 0))
    (.set 2 (.mod (.div (eventExpr σ) (.constant 8)) (.constant 2)))
    (.set 2 (.mod (.div storedExpr (.pow2 (.sub (.constant 3) frameExpr))) (.constant 2)))

def policyArgs : Fin 1 → Expr := ![.reg 3]
theorem policy_args_fresh : ∀ i r, r ∈ P02A2.LoopRenaming.exprRegs (policyArgs i) → r < 16 := by
  intro i r hr
  fin_cases i
  simp [policyArgs,P02A2.LoopRenaming.exprRegs] at hr
  omega

def prepare (p : Program 1) : Stmt := .seq (.set 3 histExpr) (call p 16 policyArgs 6)
def nextProgram (p : Program 1) (σ : Bool) : Program 2 :=
  ⟨.branch (.eq frameExpr (.constant 0)) (.seq (prepare p) (nextBody σ)) (nextBody σ),2⟩
def outputProgram (p : Program 1) (σ : Bool) : Program 2 :=
  ⟨.branch (.eq frameExpr (.constant 0)) (.seq (prepare p) (outputBody σ)) (outputBody σ),2⟩

def PolicyImplements (p : Program 1) (a : ℕ → Bool) : Prop := ∀ h, denote p ![h] = bitNat (a h)

theorem prepare_values (p : Program 1) (a : ℕ → Bool) (ha : PolicyImplements p a) (σ : Store) :
    exec (prepare p) σ 0 = σ 0 ∧ exec (prepare p) σ 1 = σ 1 ∧
    exec (prepare p) σ 6 = bitNat (a (policyHistory (σ 0))) := by
  simp only [prepare,exec]
  constructor
  · rw [call_frame _ _ _ _ policy_args_fresh 0 (by decide) (by decide)]
    simp
  constructor
  · rw [call_frame _ _ _ _ policy_args_fresh 1 (by decide) (by decide)]
    simp
  · rw [call_value _ _ _ _ policy_args_fresh]
    have he : (fun i => evalExpr (policyArgs i) (Function.update σ 3 (evalExpr histExpr σ))) =
        ![policyHistory (σ 0)] := by
      funext i
      fin_cases i
      simp [policyArgs,evalExpr,histExpr,policyHistory]
    rw [he,ha]

end Orthemology.RuntimeBridge.HistoryRuntime

namespace Orthemology.RuntimeBridge.HistoryRuntime
open Orthemology.Frontier Orthemology.Frontier.MealyMeasure
open P02A2.ObserverCore P02A2.PRProgram P02.Codec
open Orthemology.CertifiedObserver

theorem bitNat_mod (n : ℕ) : bitNat (decide (n % 2 = 1)) = n % 2 := by
  have h : n%2=0 ∨ n%2=1 := by omega
  rcases h with h | h <;> simp [bitNat,h]

theorem source_value (τ : Store) : evalExpr sourceExpr τ = bitNat (observedState (policyHistory (τ 0))) := by
  change (1 - if policyHistory (τ 0) = 1 then 1 else 0) * (policyHistory (τ 0) % 2) = _
  by_cases h : policyHistory (τ 0) = 1
  · simp [observedState,h,bitNat]
  · simp [observedState,h,bitNat_mod]

theorem proposal_value (τ : Store) (b : Bool) (hb : τ 1 = bitNat b) :
    evalExpr propExpr τ = proposal (τ 0) b := by
  simp [propExpr,phaseExpr,evalExpr,proposal,corePhase,hb]

theorem accept_value (τ : Store) (b : Bool) (hb : τ 1 = bitNat b) :
    evalExpr acceptExpr τ = bitNat (accepts (τ 0) b) := by
  change (1 - if corePhase (τ 0) = 0 then 1 else 0) * (if evalExpr propExpr τ ≤ 2 then 1 else 0) = _
  rw [proposal_value τ b hb]
  by_cases hp : corePhase (τ 0) = 0 <;> by_cases hv : proposal (τ 0) b ≤ 2 <;>
    simp [accepts,bitNat,hp,hv]

theorem receipt_value (σ a : Bool) (τ : Store) (b : Bool) (hb : τ 1 = bitNat b) (ha : τ 6 = bitNat a) :
    evalExpr (receiptExpr σ) τ = bitNat (receipt σ a (τ 0) b) := by
  cases σ <;> cases a <;>
    simp [receiptExpr,evalExpr,ha,proposal_value τ b hb,receipt,bitNat]

theorem event_value (σ : Bool) (a : ℕ → Bool) (τ : Store) (b : Bool)
    (hb : τ 1 = bitNat b) (ha : τ 6 = bitNat (a (policyHistory (τ 0)))) :
    evalExpr (eventExpr σ) τ = eventCode σ a (τ 0) b := by
  simp only [eventExpr,evalExpr,accept_value τ b hb,source_value,
    receipt_value σ _ τ b hb ha,ha,eventCode]

theorem core_value (σ : Bool) (a : ℕ → Bool) (τ : Store) (b : Bool)
    (hb : τ 1 = bitNat b) (ha : τ 6 = bitNat (a (policyHistory (τ 0)))) :
    evalExpr (coreExpr σ) τ = coreNext σ a (τ 0) b := by
  change (if corePhase (τ 0) = 0 then 1 else 0) * (3*policyHistory (τ 0)+1+τ 1) +
    (1-if corePhase (τ 0) = 0 then 1 else 0) *
      (3*policyHistory (τ 0) + evalExpr acceptExpr τ *
        (9*policyHistory (τ 0)+6*τ 6+3*evalExpr (receiptExpr σ) τ)) = _
  rw [accept_value τ b hb,receipt_value σ _ τ b hb ha,ha,hb]
  by_cases hp : corePhase (τ 0) = 0
  · simp [coreNext,hp]
  · cases hx : accepts (τ 0) b <;> simp [coreNext,hp,hx,bitNat,appendHistory] <;> split_ifs <;> omega

theorem next_body_value (σ : Bool) (a : ℕ → Bool) (τ : Store) (b : Bool)
    (hb : τ 1 = bitNat b) (ha : τ 6 = bitNat (a (policyHistory (τ 0)))) :
    exec (nextBody σ) τ 2 = (machine σ a).next (τ 0) b := by
  simp only [nextBody,exec,evalExpr,frameExpr,evalExpr,framePhase,
    core_value σ a τ b hb ha,event_value σ a τ b hb ha,machine]
  split_ifs <;> simp_all

theorem output_body_value (σ : Bool) (a : ℕ → Bool) (τ : Store) (b : Bool)
    (hb : τ 1 = bitNat b) (ha : τ 6 = bitNat (a (policyHistory (τ 0)))) :
    exec (outputBody σ) τ 2 = bitNat ((machine σ a).out (τ 0) b) := by
  simp only [outputBody,exec,evalExpr,frameExpr,storedExpr,evalExpr,framePhase,
    storedFrame,event_value σ a τ b hb ha,machine]
  by_cases h : τ 0 % 4 = 0 <;> simp [h,bitNat_mod]

/-- Exact natural-state implementation certificate for the actual wrapper.
The sole policy assumption is a one-call source-program contract on history. -/
theorem wrapper_implemented (p : Program 1) (a : ℕ → Bool) (ha : PolicyImplements p a) (σ : Bool) :
    Natural.Implements (nextProgram p σ) (outputProgram p σ) (machine σ a) := by
  constructor
  · intro q b
    let τ := exec (prepare p) (P02A2.LoopPrimrec.extend ![q,bitNat b])
    have ht := prepare_values p a ha (P02A2.LoopPrimrec.extend ![q,bitNat b])
    have h0 : τ 0 = q := by simpa [τ,P02A2.LoopPrimrec.extend] using ht.1
    have h1 : τ 1 = bitNat b := by simpa [τ,P02A2.LoopPrimrec.extend] using ht.2.1
    have h6 : τ 6 = bitNat (a (policyHistory (τ 0))) := by simpa [τ,h0,P02A2.LoopPrimrec.extend] using ht.2.2
    by_cases hf : q % 4 = 0
    · change (if (if q % 4 = 0 then 1 else 0) = 0 then
        exec (nextBody σ) (P02A2.LoopPrimrec.extend ![q,bitNat b]) else exec (nextBody σ) τ) 2 = _
      simp only [hf,↓reduceIte,Nat.one_ne_zero]
      rw [next_body_value σ a τ b h1 h6,h0]
    · by_cases h3 : q % 4 = 3 <;>
        simp [denote,nextProgram,exec,evalExpr,frameExpr,P02A2.LoopPrimrec.extend,hf,h3,nextBody,machine,framePhase]
  · intro q b
    let τ := exec (prepare p) (P02A2.LoopPrimrec.extend ![q,bitNat b])
    have ht := prepare_values p a ha (P02A2.LoopPrimrec.extend ![q,bitNat b])
    have h0 : τ 0 = q := by simpa [τ,P02A2.LoopPrimrec.extend] using ht.1
    have h1 : τ 1 = bitNat b := by simpa [τ,P02A2.LoopPrimrec.extend] using ht.2.1
    have h6 : τ 6 = bitNat (a (policyHistory (τ 0))) := by simpa [τ,h0,P02A2.LoopPrimrec.extend] using ht.2.2
    by_cases hf : q % 4 = 0
    · change (if (if q % 4 = 0 then 1 else 0) = 0 then
        exec (outputBody σ) (P02A2.LoopPrimrec.extend ![q,bitNat b]) else exec (outputBody σ) τ) 2 = _
      simp only [hf,↓reduceIte,Nat.one_ne_zero]
      rw [output_body_value σ a τ b h1 h6,h0]
    · simp [denote,outputProgram,exec,evalExpr,frameExpr,P02A2.LoopPrimrec.extend,hf,outputBody,machine,
        framePhase,storedExpr,storedFrame,bitNat_mod]

/-- One common history-policy source is inserted unchanged in both environments. -/
def runtimeIndex (p : Program 1) (σ : Bool) : ℕ := Natural.index (nextProgram p σ) (outputProgram p σ) initial

theorem actual_history_runtime (p : Program 1) (a : ℕ → Bool) (ha : PolicyImplements p a) (σ : Bool) :
    Indexed.runtimeOutput (runtimeIndex p σ) = MealyMeasure.output (machine σ a) initial :=
  Natural.compiled_runtime_output _ _ _ (wrapper_implemented p a ha σ) initial

end Orthemology.RuntimeBridge.HistoryRuntime
