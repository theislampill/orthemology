import LiteralSamplerExecution
import FairBitSubsequence
import HistorySamplingSemantics
import AcceptedFixtureController

namespace Orthemology.RationalLaw.RuntimeBinding
open MeasureTheory Set
open scoped ENNReal BigOperators
open Orthemology.Frontier Orthemology.Frontier.MealyMeasure Orthemology.RuntimeBridge
open Orthemology.RuntimeBridge.HistoryRuntime
open Orthemology.Tranche2.PolicyEmbedding
open Orthemology.CertifiedObserver
open P02A2.Q8Measure (fairCantor)

/-- Literal allocation table for the existing binary runtime, with D=3 and width 2. -/
def row (σ a : Bool) (v : Fin 3) : Bool := decide (1+(if a=σ then 1 else 0) ≤ v.val)

def adaptiveRow (σ : Bool) (a : ℕ → Bool) (h : History Bool Bool) : Fin 3 → Bool :=
  row σ (historyPolicy a () h)

def update (a : ℕ → Bool) (h : History Bool Bool) (y : Bool) : History Bool Bool :=
  (historyPolicy a () h,y)::h

theorem code_two (w : Fin 2 → Bool) :
    (code 2 w).val = 2*(if w 0 then 1 else 0) + (if w 1 then 1 else 0) := by
  have hw : w = ![w 0,w 1] := by funext i; fin_cases i <;> rfl
  rw [hw]
  generalize w 0 = b
  generalize w 1 = c
  cases b <;> cases c <;> decide

theorem sample_reject_iff (σ act : Bool) (w : Fin 2 → Bool) :
    sample 2 3 (row σ act) w = none ↔ w 0 = true ∧ w 1 = true := by
  rw [sample_none_iff 2 3 (by decide)]
  rw [mem_rejectedBlocks, code_two]
  cases h0 : w 0 <;> cases h1 : w 1 <;> simp [h0,h1]

/-- The actual frozen historyStep twice is exactly the literal sampler proposal,
including unchanged history on rejection and phase zero on every block boundary. -/
theorem two_bit_historyStep (σ : Bool) (a : ℕ → Bool) (h : History Bool Bool) (w : Fin 2 → Bool) :
    historyStep σ a (historyStep σ a (h,0) (w 0)) (w 1) =
      (match sample 2 3 (adaptiveRow σ a h) w with
       | none => h
       | some y => update a h y, 0) := by
  have hw : w = ![w 0,w 1] := by funext i; fin_cases i <;> rfl
  rw [hw]
  generalize w 0 = b
  generalize w 1 = c
  generalize hh : historyPolicy a () h = act
  cases σ <;> cases act <;> cases b <;> cases c <;>
    simp only [sample,code_two] <;>
    simp [historyStep,proposalAt,receiptAt,adaptiveRow,row,update,hh,bitNat]

theorem row_weight (σ act y : Bool) :
    weight 3 (row σ act) y = if y then (if act=σ then 1 else 2) else (if act=σ then 2 else 1) := by
  cases σ <;> cases act <;> cases y <;> decide

/-- The probability table is bound to the literal accepted fixture kernel. -/
theorem weight_div_three_eq_kernel (σ s act y : Bool) :
    (weight 3 (row σ act) y : ℝ≥0∞)/3 =
      ENNReal.ofReal (Orthemology.RuntimeBridge.Controller.Fixture.kernel.row σ (s,act) y) := by
  rw [row_weight]
  cases σ <;> cases s <;> cases act <;> cases y <;>
    norm_num [Orthemology.RuntimeBridge.Controller.Fixture.kernel, ENNReal.ofReal_div_of_pos]

/-- Accepted-prefix event on the original physical tape, with the exact retained
four-acquisition framing decimation. The predicate uses the explicit bit sampler. -/
def physicalAccepted (σ : Bool) (a : ℕ → Bool) (n : ℕ) (ys : Fin n → Bool) : Set Cantor :=
  {x | delivers 2 3 (adaptiveRow σ a) (update a) n [] ys (decimateFour x)}

theorem physical_accepted_probability (σ : Bool) (a : ℕ → Bool) (n : ℕ) (ys : Fin n → Bool) :
    fairCantor (physicalAccepted σ a n ys) = historyMass 3 (adaptiveRow σ a) (update a) n [] ys := by
  have he : physicalAccepted σ a n ys = decimateFour ⁻¹'
      acceptedHistory 2 3 (by decide) (adaptiveRow σ a) (update a) n [] ys := by
    ext x
    exact delivers_iff_acceptedHistory 2 3 (by decide) _ _ _ _ _ _
  rw [he, fair_decimateFour_preimage _ (measurableSet_acceptedHistory _ _ _ _ _ _ _ _)]
  exact accepted_history_probability 2 3 (by decide) (by decide) _ _ _ _ _


theorem historyStep_even_state (σ : Bool) (a : ℕ → Bool) (h : History Bool Bool) (x : Cantor) (k : ℕ) :
    state (coreMachine (historyStep σ a)) (h,0) x (2*k) =
      (proposalState 2 3 (adaptiveRow σ a) (update a) h x k,0) := by
  induction k with
  | zero => rfl
  | succ k ih =>
      rw [Nat.mul_add, Nat.mul_one, state_add, ih]
      have hh := two_bit_historyStep σ a (proposalState 2 3 (adaptiveRow σ a) (update a) h x k)
        (block 2 k x)
      have hmul : 2*k = k*2 := Nat.mul_comm _ _
      cases hs : sample 2 3 (adaptiveRow σ a (proposalState 2 3 (adaptiveRow σ a) (update a) h x k))
        (block 2 k x) <;>
        simpa only [state, coreMachine, shift, block, Fin.val_zero, Fin.val_one, Nat.add_zero,
          hmul, proposalState, hs] using hh

/-- The second complete serialized frame contains exactly the proposal's acknowledgment
and accepted receipt; the first frame of every two-bit proposal never acknowledges. -/
theorem second_frame_sample (σ : Bool) (a : ℕ → Bool) (h : History Bool Bool) (w : Fin 2 → Bool) :
    (if historyObservation σ a (historyStep σ a (h,0) (w 0)) (w 1) 0 then
      some (historyObservation σ a (historyStep σ a (h,0) (w 0)) (w 1) 3) else none) =
      sample 2 3 (adaptiveRow σ a h) w := by
  have hw : w = ![w 0,w 1] := by funext i; fin_cases i <;> rfl
  rw [hw]
  generalize w 0 = b
  generalize w 1 = c
  generalize hh : historyPolicy a () h = act
  cases σ <;> cases act <;> cases b <;> cases c <;>
    simp only [sample,code_two] <;>
    simp [historyStep,historyObservation,proposalAt,receiptAt,adaptiveRow,row,hh,bitNat]

theorem first_frame_no_ack (σ : Bool) (a : ℕ → Bool) (h : History Bool Bool) (b : Bool) :
    historyObservation σ a (h,0) b 0 = false := by simp [historyObservation]

/-- This readout uses actual indexed-runtime output bits, not a mathematical sampler oracle. -/
def runtimeProposal (p : P02A2.PRProgram.Program 1) (σ : Bool) (x : Cantor) (k : ℕ) : Option Bool :=
  if Indexed.runtimeOutput (runtimeIndex p σ) x (8*k+4) then
    some (Indexed.runtimeOutput (runtimeIndex p σ) x (8*k+7)) else none

theorem runtime_first_frame_no_ack (p : P02A2.PRProgram.Program 1) (a : ℕ → Bool)
    (hp : PolicyImplements p a) (σ : Bool) (x : Cantor) (k : ℕ) :
    Indexed.runtimeOutput (runtimeIndex p σ) x (8*k) = false := by
  have hh := runtime_observed_history_frames p a hp σ x (2*k) (0 : Fin 4)
  have he : 4*(2*k)+(0 : Fin 4).val = 8*k := by omega
  rw [he, historyStep_even_state] at hh
  exact hh.trans (first_frame_no_ack _ _ _ _)

/-- Complete proposal-by-proposal binding to the frozen P02 source wrapper. -/
theorem runtime_proposal_exact (p : P02A2.PRProgram.Program 1) (a : ℕ → Bool)
    (hp : PolicyImplements p a) (σ : Bool) (x : Cantor) (k : ℕ) :
    runtimeProposal p σ x k = proposalReceipt 2 3 (adaptiveRow σ a) (update a) [] (decimateFour x) k := by
  have h0 := runtime_observed_history_frames p a hp σ x (2*k+1) (0 : Fin 4)
  have h3 := runtime_observed_history_frames p a hp σ x (2*k+1) (3 : Fin 4)
  have e0 : 4*(2*k+1)+(0 : Fin 4).val = 8*k+4 := by omega
  have e3 : 4*(2*k+1)+(3 : Fin 4).val = 8*k+7 := by omega
  rw [e0] at h0
  rw [e3] at h3
  unfold runtimeProposal
  rw [h0,h3]
  rw [show state (coreMachine (historyStep σ a)) ([],0) (decimateFour x) (2*k+1) =
      historyStep σ a (state (coreMachine (historyStep σ a)) ([],0) (decimateFour x) (2*k))
        (decimateFour x (2*k)) from rfl, historyStep_even_state]
  have hh := second_frame_sample σ a
    (proposalState 2 3 (adaptiveRow σ a) (update a) [] (decimateFour x) k)
    (block 2 k (decimateFour x))
  simpa [proposalReceipt, block, decimateFour, Nat.mul_comm, Nat.mul_add] using hh

/-- Actual scheduled-stack runtime accepted-receipt cylinder law for every supplied
common history-only policy source and its per-call implementation certificate. -/
theorem runtime_accepted_history_probability (p : P02A2.PRProgram.Program 1) (a : ℕ → Bool)
    (hp : PolicyImplements p a) (σ : Bool) (n : ℕ) (ys : Fin n → Bool) :
    fairCantor {x | reports n ys (runtimeProposal p σ x)} =
      historyMass 3 (adaptiveRow σ a) (update a) n [] ys := by
  have he : {x | reports n ys (runtimeProposal p σ x)} = physicalAccepted σ a n ys := by
    ext x
    have hx : runtimeProposal p σ x = proposalReceipt 2 3 (adaptiveRow σ a) (update a) [] (decimateFour x) := by
      funext k
      exact runtime_proposal_exact p a hp σ x k
    change reports n ys (runtimeProposal p σ x) ↔ _
    rw [hx]
    exact reports_iff_delivers _ _ _ _ _ _ _ _
  rw [he, physical_accepted_probability]


/-- The runtime's exact joint accepted-history/rejection-clock cylinder law. -/
theorem runtime_joint_probability (p : P02A2.PRProgram.Program 1) (a : ℕ → Bool)
    (hp : PolicyImplements p a) (σ : Bool) (n : ℕ) (ys : Fin n → Bool) (rs : Fin n → ℕ) :
    fairCantor {x | reportsWithCounts n ys rs (runtimeProposal p σ x)} =
      historyMass 3 (adaptiveRow σ a) (update a) n [] ys * clockMass 2 3 n rs := by
  have he : {x | reportsWithCounts n ys rs (runtimeProposal p σ x)} = decimateFour ⁻¹'
      historyJoint 2 3 (by decide) (adaptiveRow σ a) (update a) n [] ys rs := by
    ext x
    change reportsWithCounts n ys rs (runtimeProposal p σ x) ↔ _
    have hx : runtimeProposal p σ x = proposalReceipt 2 3 (adaptiveRow σ a) (update a) [] (decimateFour x) := by
      funext k
      exact runtime_proposal_exact p a hp σ x k
    rw [hx]
    exact reportsWithCounts_iff_joint _ _ _ _ _ _ _ _ _ _
  rw [he, fair_decimateFour_preimage _ (show MeasurableSet (historyJoint 2 3 (by decide) (adaptiveRow σ a) (update a) n [] ys rs) from measurableSet_constraintEvent _)]
  exact history_joint_probability 2 3 (by decide) (by decide) _ _ _ _ _ _

/-- All logical reports complete almost surely in the actual scheduled indexed runtime. -/
theorem runtime_infinitely_many_reports (p : P02A2.PRProgram.Program 1) (a : ℕ → Bool)
    (hp : PolicyImplements p a) (σ : Bool) :
    ∀ᵐ x ∂fairCantor, ∀ n, ∃ ys : Fin n → Bool, reports n ys (runtimeProposal p σ x) := by
  have hm : Measurable decimateFour := measurable_pi_lambda _ (fun n => measurable_pi_apply (4*n))
  have hg := infinitely_many_receipts 2 3 (by decide) (by decide) (adaptiveRow σ a) (update a) []
  rw [← fair_decimateFour_law] at hg
  have hh := ae_of_ae_map hm.aemeasurable hg
  filter_upwards [hh] with x hx
  intro n
  obtain ⟨ys,hy⟩ := hx n
  refine ⟨ys, ?_⟩
  have he : runtimeProposal p σ x = proposalReceipt 2 3 (adaptiveRow σ a) (update a) [] (decimateFour x) := by
    funext k
    exact runtime_proposal_exact p a hp σ x k
  rw [he, reports_iff_delivers]
  exact (delivers_iff_acceptedHistory 2 3 (by decide) _ _ _ _ _ _).mpr hy

end Orthemology.RationalLaw.RuntimeBinding

namespace Orthemology.RationalLaw.RuntimeBinding
open MeasureTheory Set
open Orthemology.Frontier.MealyMeasure Orthemology.RuntimeBridge
open Orthemology.RuntimeBridge.HistoryRuntime
open Orthemology.CertifiedObserver
open P02A2.Q8Measure (fairCantor)

/-- The concrete forever-rejecting tape exists; source tick termination does not
turn it into a fabricated receipt or a logical completion. -/
theorem all_one_runtime_never_reports (p : P02A2.PRProgram.Program 1) (a : ℕ → Bool)
    (hp : PolicyImplements p a) (σ : Bool) (k : ℕ) :
    runtimeProposal p σ (fun _ => true) k = none := by
  rw [runtime_proposal_exact p a hp]
  unfold proposalReceipt adaptiveRow
  apply (sample_reject_iff _ _ _).mpr
  exact ⟨rfl,rfl⟩

theorem runtime_never_reports_null (p : P02A2.PRProgram.Program 1) (a : ℕ → Bool)
    (hp : PolicyImplements p a) (σ : Bool) :
    fairCantor {x | ∀ k, runtimeProposal p σ x k = none} = 0 := by
  have ha : ∀ᵐ x ∂fairCantor, ¬∀ k, runtimeProposal p σ x k = none := by
    filter_upwards [runtime_infinitely_many_reports p a hp σ] with x hx
    obtain ⟨ys,hy⟩ := hx 1
    obtain ⟨r,hr,hv,ht⟩ := hy
    intro h
    rw [h r] at hv
    contradiction
  simpa only [ae_iff,not_not] using ha

end Orthemology.RationalLaw.RuntimeBinding
