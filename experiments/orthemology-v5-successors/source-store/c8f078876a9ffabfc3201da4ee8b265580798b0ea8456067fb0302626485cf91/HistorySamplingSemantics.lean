import HistoryRuntimeFraming

namespace Orthemology.RuntimeBridge.HistoryRuntime
open Orthemology.Frontier Orthemology.Frontier.MealyMeasure
open Orthemology.Tranche2.PolicyEmbedding
open Orthemology.CertifiedObserver
open P02A2.PRProgram

abbrev HistoryConfig := History Bool Bool × Fin 3

def encodeConfig (c : HistoryConfig) : ℕ := 3*encodeHistory c.1 + c.2.val

def historyPolicy (a : ℕ → Bool) (_ : Unit) (h : History Bool Bool) : Bool := a (encodeHistory h)

def proposalAt (phase : Fin 3) (b : Bool) : ℕ := 2*(phase.val-1) + bitNat b

def receiptAt (σ a : Bool) (phase : Fin 3) (b : Bool) : Bool :=
  decide (1+bitNat (decide (a=σ)) ≤ proposalAt phase b)

def historyStep (σ : Bool) (a : ℕ → Bool) (c : HistoryConfig) (b : Bool) : HistoryConfig :=
  if c.2.val = 0 then (c.1,if b then 2 else 1)
  else if proposalAt c.2 b ≤ 2 then
    ((historyPolicy a () c.1,receiptAt σ (historyPolicy a () c.1) c.2 b)::c.1,0)
  else (c.1,0)

def historyObservation (σ : Bool) (a : ℕ → Bool) (c : HistoryConfig) (b : Bool) : Fin 4 → Bool :=
  let accepted := decide (c.2.val ≠ 0 ∧ proposalAt c.2 b ≤ 2)
  ![accepted,HiddenParity.Sufficiency.observedState false c.1,historyPolicy a () c.1,
    accepted && receiptAt σ (historyPolicy a () c.1) c.2 b]

theorem encoded_fields (c : HistoryConfig) :
    policyHistory (64*encodeConfig c) = encodeHistory c.1 ∧ corePhase (64*encodeConfig c) = c.2.val := by
  have hp := c.2.isLt
  simp only [policyHistory,corePhase,Nat.mul_div_right]
  unfold encodeConfig
  constructor <;> omega

theorem encoded_proposal (c : HistoryConfig) (b : Bool) :
    proposal (64*encodeConfig c) b = proposalAt c.2 b := by
  simp [proposal,proposalAt,(encoded_fields c).2]

theorem encoded_receipt (σ : Bool) (a : ℕ → Bool) (c : HistoryConfig) (b : Bool) :
    receipt σ (a (policyHistory (64*encodeConfig c))) (64*encodeConfig c) b =
      receiptAt σ (historyPolicy a () c.1) c.2 b := by
  simp [receipt,receiptAt,historyPolicy,(encoded_fields c).1,encoded_proposal]

theorem encoded_receipt_value (σ : Bool) (a : ℕ → Bool) (c : HistoryConfig) (b : Bool) :
    receipt σ (a (encodeHistory c.1)) (64*encodeConfig c) b =
      receiptAt σ (a (encodeHistory c.1)) c.2 b := by
  simp [receipt,receiptAt,encoded_proposal]

/-- Exact acquired-history successor. A rejected proposal never changes history. -/
theorem encoded_history_next (σ : Bool) (a : ℕ → Bool) (c : HistoryConfig) (b : Bool) :
    coreNext σ a (64*encodeConfig c) b = encodeConfig (historyStep σ a c b) := by
  simp only [coreNext,(encoded_fields c).1,(encoded_fields c).2,
    accepts,encoded_proposal,encoded_receipt_value,historyStep]
  by_cases h0 : c.2.val = 0
  · cases b <;> simp [h0,encodeConfig,bitNat]
  · by_cases hv : proposalAt c.2 b ≤ 2 <;>
      simp [h0,hv,encodeConfig,encodeHistory,historyPolicy]

/-- The serialized frame matches the explicit receipt machine. Its action field
comes only from the acquired history; acknowledgment/receipt are environment
outputs, and rejected symbols or timing are never appended to policy history. -/
theorem encoded_history_observation (σ : Bool) (a : ℕ → Bool) (c : HistoryConfig) (b : Bool) :
    frameBits σ a (64*encodeConfig c) b = historyObservation σ a c b := by
  simp [frameBits,historyObservation,accepts,(encoded_fields c).1,(encoded_fields c).2,
    encoded_proposal,encoded_receipt_value,historyPolicy,observed_history_exact]

theorem history_state_exact (σ : Bool) (a : ℕ → Bool) (x : Cantor) (n : ℕ) :
    state (coreMachine (fun q b => coreNext σ a (64*q) b)) 3 x n =
      encodeConfig (state (coreMachine (historyStep σ a)) ([],0) x n) := by
  induction n with
  | zero => rfl
  | succ n ih =>
      rw [state,state]
      change coreNext σ a (64*state (coreMachine (fun q b => coreNext σ a (64*q) b)) 3 x n) (x n) = _
      rw [ih]
      exact encoded_history_next σ a _ _

/-- Complete all-tape runtime/frame refinement to a machine whose only policy
input is the literal retained newest-first action/receipt history. -/
theorem runtime_observed_history_frames (p : Program 1) (a : ℕ → Bool) (hp : PolicyImplements p a)
    (σ : Bool) (x : Cantor) (n : ℕ) (j : Fin 4) :
    Indexed.runtimeOutput (runtimeIndex p σ) x (4*n+j) =
      historyObservation σ a
        (state (coreMachine (historyStep σ a)) ([],0) (decimateFour x) n) (x (4*n)) j := by
  rw [actual_history_frames p a hp σ x n j,history_state_exact,encoded_history_observation]

end Orthemology.RuntimeBridge.HistoryRuntime
