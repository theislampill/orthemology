import SamplerClockMarginals
import LiteralSamplerExecution
import ReceiptProjectionDefect
import FairBitSubsequence
import StutteringClock
import ObservationChannels

/-! Random positive stuttering preserves parity but need not preserve nonatomic defect.
This counterexample has no extra acknowledgment or random payload in its output. -/
namespace Orthemology.RationalLaw.HeldStateControl
open MeasureTheory Set
open Orthemology.Frontier Orthemology.Frontier.MealyMeasure Orthemology.RuntimeBridge
open Orthemology.CertifiedObserver
open P02A2.Q8Measure (fairCantor)
open Orthemology.RuntimeBridge.Clock
open Orthemology.Tranche2.RecurrentSupport

/-- Zero accepts and toggles the logical state; one holds the pre-receipt state. -/
def heldMachine : Mealy Bool where
  next q b := if b then q else !q
  out q _ := q

def alternating : ℕ → Bool
  | 0 => false
  | n+1 => !(alternating n)

/-- Number of accepted zeros strictly before physical tick n. -/
def receiptCount (x : Cantor) : ℕ → ℕ
  | 0 => 0
  | n+1 => receiptCount x n + if x n then 0 else 1

theorem state_exact (x : Cantor) (n : ℕ) :
    state heldMachine false x n = alternating (receiptCount x n) := by
  induction n with
  | zero => rfl
  | succ n ih =>
      simp only [state, ih]
      cases hx : x n <;> simp [heldMachine, receiptCount, hx, alternating]

theorem output_exact (x : Cantor) (n : ℕ) :
    output heldMachine false x n = alternating (receiptCount x n) := state_exact x n

theorem held_nondeterministic (q : Bool) : ¬ heldMachine.infiniteRel q q := by
  rw [← deterministicBit_spec]
  cases q <;> decide

/-- Every physical singleton has zero mass, although the logical path is deterministic. -/
theorem held_atomic_mass_zero : P02A2.mass (law heldMachine false) = 0 := by
  apply (atomic_mass_zero_iff_unreachable heldMachine false).mpr
  intro u
  exact held_nondeterministic _

theorem held_defect_one : P02A2.defect (law heldMachine false) = 1 := by
  simp [P02A2.defect, held_atomic_mass_zero]

theorem logical_defect_zero : P02A2.defect (Measure.dirac alternating) = 0 := by
  have hm : P02A2.mass (Measure.dirac alternating) = 1 := by
    apply P02A2.countable_carrier_mass_one _ (Set.countable_singleton alternating)
    · simp
    · simp
  simp [P02A2.defect, hm]

theorem receiptCount_monotone (x : Cantor) : Monotone (receiptCount x) := by
  apply monotone_nat_of_le_succ
  intro n
  simp only [receiptCount]
  omega

/-- Every natural is reached by a zero-count clock if zeros occur beyond every horizon. -/
theorem receiptCount_onto (x : Cantor) (hx : ∀ r, ∃ k, r ≤ k ∧ x k = false) :
    Function.Surjective (receiptCount x) := by
  intro n
  induction n with
  | zero => exact ⟨0,rfl⟩
  | succ n ih =>
      obtain ⟨r,hr⟩ := ih
      obtain ⟨k,hkr,hk⟩ := hx r
      have hn : n < receiptCount x (k+1) := by
        have hh := receiptCount_monotone x hkr
        simp only [receiptCount, hk, Bool.false_eq_true, ↓reduceIte] at *
        omega
      have hex : ∃ t, n < receiptCount x t := ⟨k+1,hn⟩
      let t := Nat.find hex
      have ht : n < receiptCount x t := Nat.find_spec hex
      have hpos : 0 < t := by
        by_contra h
        have he : t = 0 := by omega
        simp [he,receiptCount] at ht
      obtain ⟨u,hu⟩ := Nat.exists_eq_succ_of_ne_zero (Nat.ne_of_gt hpos)
      have hprev : receiptCount x u ≤ n := by
        have := Nat.find_min hex (show u < Nat.find hex by change u < t; omega)
        omega
      refine ⟨t, ?_⟩
      rw [hu,receiptCount] at ht ⊢
      cases hx : x u <;> simp only [hx, Bool.false_eq_true, ↓reduceIte] at ht ⊢ <;> omega

end Orthemology.RationalLaw.HeldStateControl

namespace Orthemology.RationalLaw.HeldStateControl
open MeasureTheory Set
open Orthemology.Frontier Orthemology.Frontier.MealyMeasure Orthemology.RuntimeBridge
open Orthemology.CertifiedObserver
open P02A2.Q8Measure (fairCantor)
open Orthemology.RuntimeBridge.Clock
open Orthemology.Tranche2.RecurrentSupport

theorem fair_singleton_zero (y : Cantor) : fairCantor {y} = 0 := by
  have h := P02A2.Q8Measure.eventually_singleton_zero (fun _ => true) 0 (by simp) y
  have he : P02A2.Q8Measure.law (fun _ => true) = fairCantor := by
    have hs : P02A2.Q8Measure.switched (fun _ => true) = id := by
      funext x n
      rfl
    rw [P02A2.Q8Measure.law, hs, Measure.map_id]
  rwa [he] at h

/-- There are zeros after every horizon almost surely; the all-one tape still exists. -/
theorem infinitely_many_zeros :
    ∀ᵐ x ∂fairCantor, ∀ r, ∃ k, r ≤ k ∧ x k = false := by
  rw [ae_all_iff]
  intro r
  rw [ae_iff]
  have he : {x : Cantor | ¬∃ k, r ≤ k ∧ x k = false} =
      (fun x n => x (r+n)) ⁻¹' {fun (_ : ℕ) => true} := by
    ext x
    simp only [Set.mem_setOf_eq, Set.mem_preimage, Set.mem_singleton_iff]
    constructor
    · intro h
      funext n
      cases hx : x (r+n)
      · exact False.elim (h ⟨r+n,by omega,hx⟩)
      · rfl
    · intro h ⟨k,hkr,hk⟩
      have hh := congrFun h (k-r)
      rw [Nat.add_sub_of_le hkr, hk] at hh
      cases hh
  rw [he, ← Measure.map_apply (measurable_pi_lambda _ (fun n => measurable_pi_apply (r+n)))
    (measurableSet_singleton _), fair_reindex_law _ (by intro i j h; omega), fair_singleton_zero]

/-- The physically held output is an actual positive finite stuttering of a fixed
alternating path, almost surely. Infinite rejection tapes are excluded only here. -/
theorem almost_sure_positive_stutter :
    ∀ᵐ x ∂fairCantor, ∃ c : PositiveStutter,
      output heldMachine false x = fun t => alternating (c.logicalAt t) := by
  filter_upwards [infinitely_many_zeros] with x hx
  exact ⟨⟨receiptCount x,receiptCount_monotone x,receiptCount_onto x hx⟩,funext (output_exact x)⟩

/-- Thus parity is preserved for every priority assignment while defect changes 0→1. -/
theorem almost_sure_parity_exact (priority : Bool → ℕ) :
    ∀ᵐ x ∂fairCantor,
      HiddenParity.Stochastic.ParitySuccess priority (output heldMachine false x) ↔
        HiddenParity.Stochastic.ParitySuccess priority alternating := by
  filter_upwards [almost_sure_positive_stutter] with x hx
  obtain ⟨c,hc⟩ := hx
  rw [hc]
  exact parity_exact c priority alternating

/-- Effective two-state numbering gives a literal P02 source, with no trace premise. -/
def heldIndex : ℕ := index (numberMachine finTwoEquiv.symm heldMachine) (finTwoEquiv.symm false)

theorem compiled_held_output : Indexed.runtimeOutput heldIndex = output heldMachine false :=
  numbered_runtime_output finTwoEquiv.symm heldMachine false

theorem compiled_held_defect_one :
    P02A2.defect (fairCantor.map (Indexed.runtimeOutput heldIndex)) = 1 := by
  rw [compiled_held_output]
  exact held_defect_one

theorem compiled_held_parity_exact (priority : Bool → ℕ) :
    ∀ᵐ x ∂fairCantor,
      HiddenParity.Stochastic.ParitySuccess priority (Indexed.runtimeOutput heldIndex x) ↔
        HiddenParity.Stochastic.ParitySuccess priority alternating := by
  rw [compiled_held_output]
  exact almost_sure_parity_exact priority

end Orthemology.RationalLaw.HeldStateControl

namespace Orthemology.RationalLaw.HeldStateControl
open MeasureTheory Set
open Orthemology.Frontier Orthemology.Frontier.MealyMeasure Orthemology.RuntimeBridge
open Orthemology.CertifiedObserver
open P02A2.Q8Measure (fairCantor)
open scoped ENNReal BigOperators

def toggleRow (q : Bool) (_ : Fin 1) : Bool := !q

def changeReports (z : Cantor) (k : ℕ) : Option Bool :=
  if z (k+1) = z k then none else some (z (k+1))

theorem code_one (w : Fin 1 → Bool) : (code 1 w).val = if w 0 then 1 else 0 := by
  have he : w = fun _ => w 0 := by funext i; fin_cases i; rfl
  rw [he]
  cases w 0 <;> decide

theorem toggle_sample (q : Bool) (w : Fin 1 → Bool) :
    sample 1 1 (toggleRow q) w = if w 0 then none else some (!q) := by
  cases hw : w 0 <;> simp only [sample,code_one,hw,Bool.false_eq_true,↓reduceIte] <;> norm_num [toggleRow]

theorem proposalState_held (x : Cantor) (k : ℕ) :
    proposalState 1 1 toggleRow (fun _ y => y) false x k = state heldMachine false x k := by
  induction k with
  | zero => rfl
  | succ k ih =>
      rw [proposalState,toggle_sample,ih]
      cases hx : x k <;> simp [block,hx,state,heldMachine]

/-- Run changes, recoverable from the held stream alone, are exactly its literal
D=1 fair-bit sampler receipts. No acknowledgment field is present. -/
theorem changeReports_exact (x : Cantor) :
    changeReports (output heldMachine false x) =
      proposalReceipt 1 1 toggleRow (fun _ y => y) false x := by
  funext k
  simp only [changeReports, proposalReceipt, toggle_sample, proposalState_held]
  change (if state heldMachine false x (k+1) = state heldMachine false x k then none
    else some (state heldMachine false x (k+1))) = _
  have hn : state heldMachine false x (k+1) =
      if x k then state heldMachine false x k else !(state heldMachine false x k) := rfl
  rw [hn]
  cases hx : x k <;> cases hs : state heldMachine false x k <;> simp [block,hx,hs]

/-- A clock vector of r rejected bits per run has the iid positive-geometric law.
The event is read from changes in the actual held-state output. -/
theorem held_clock_probability (n : ℕ) (rs : Fin n → ℕ) :
    fairCantor {x | ∃ ys : Fin n → Bool,
      reportsWithCounts n ys rs (changeReports (output heldMachine false x))} =
      ∏ i, ((1/2 : ℝ≥0∞)^(rs i) * (1/2 : ℝ≥0∞)) := by
  have he : {x | ∃ ys : Fin n → Bool,
      reportsWithCounts n ys rs (changeReports (output heldMachine false x))} =
      rejectionCounts 1 1 (by decide) toggleRow (fun _ y => y) n false rs := by
    ext x
    simp only [changeReports_exact, rejectionCounts, Set.mem_setOf_eq, Set.mem_iUnion,
      reportsWithCounts_iff_joint 1 1 (by decide)]
  rw [he,rejectionCounts_probability 1 1 (by decide) (by decide)]
  norm_num [clockMass]

end Orthemology.RationalLaw.HeldStateControl

namespace Orthemology.RationalLaw.HeldStateControl
open MeasureTheory Set
open Orthemology.Frontier Orthemology.Frontier.MealyMeasure
open P02A2.Q8Measure (fairCantor)

def receiptAlternating (q : Bool) : ℕ → Bool
  | 0 => !q
  | n+1 => receiptAlternating (!q) n

theorem toggle_sample_value (q y : Bool) (w : Fin 1 → Bool)
    (h : sample 1 1 (toggleRow q) w = some y) : y = !q := by
  rw [toggle_sample] at h
  split at h
  · contradiction
  · exact (Option.some.inj h).symm

theorem delivered_toggle_receipts (n : ℕ) (q : Bool) (ys : Fin n → Bool) (x : Cantor)
    (h : delivers 1 1 toggleRow (fun _ y => y) n q ys x) :
    ∀ i : Fin n, ys i = receiptAlternating q i := by
  induction n generalizing q x with
  | zero => exact fun i => Fin.elim0 i
  | succ n ih =>
      obtain ⟨r,hr,hy,ht⟩ := h
      have hy' : ys 0 = !q := toggle_sample_value q (ys 0) _ hy
      have hh := ih (ys 0) (fun i => ys i.succ) _ ht
      intro i
      refine Fin.cases hy' (fun j => ?_) i
      simpa only [receiptAlternating,hy'] using hh j

/-- The observed sequence of actual run changes is deterministically alternating,
with no fabricated report on the exceptional finite-completion tapes. -/
theorem held_reports_alternating (n : ℕ) (ys : Fin n → Bool) (x : Cantor)
    (h : reports n ys (changeReports (output heldMachine false x))) :
    ∀ i : Fin n, ys i = receiptAlternating false i := by
  rw [changeReports_exact,reports_iff_delivers] at h
  exact delivered_toggle_receipts _ _ _ _ h

theorem held_infinitely_many_reports :
    ∀ᵐ x ∂fairCantor, ∀ n, ∃ ys : Fin n → Bool,
      reports n ys (changeReports (output heldMachine false x)) := by
  filter_upwards [infinitely_many_receipts 1 1 (by decide) (by decide) toggleRow (fun _ y => y) false] with x hx
  intro n
  obtain ⟨ys,hy⟩ := hx n
  refine ⟨ys, ?_⟩
  rw [changeReports_exact,reports_iff_delivers]
  exact (delivers_iff_acceptedHistory 1 1 (by decide) _ _ _ _ _ _).mpr hy

end Orthemology.RationalLaw.HeldStateControl
