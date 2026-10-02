import RationalRejectionLaw
import FourBitFraming

namespace Orthemology.RationalLaw.ProjectionControl
open MeasureTheory Set
open Orthemology.Frontier Orthemology.Frontier.MealyMeasure Orthemology.RuntimeBridge
open Orthemology.CertifiedObserver
open P02A2.Q8Measure (fairCantor)
open scoped ENNReal BigOperators

/-- D=1,L=1: accept the sampled zero bit, then serialize three constant fields. -/
def ackMachine : Mealy (Fin 4) where
  next q _ := ![1,2,3,0] q
  out q b := if q=0 then !b else false

def frame (_ : Unit) (b : Bool) : Fin 4 → Bool := ![!b,false,false,false]

theorem local_frame (q : Unit) (w : Fin 4 → Bool) :
    ackMachine.finalState 0 (List.ofFn w) = (0 : Fin 4) ∧
      ackMachine.outputWord 0 (List.ofFn w) = List.ofFn (frame q (w 0)) := by
  have hw : w = ![w 0,w 1,w 2,w 3] := by funext i; fin_cases i <;> rfl
  rw [hw]
  exact ⟨rfl,rfl⟩

theorem exact_frames (x : Cantor) (n : ℕ) (j : Fin 4) :
    output ackMachine 0 x (4*n+j) = frame () (x (4*n)) j := by
  exact four_frame_output ackMachine (fun (_ : Unit) _ => ()) frame (fun _ => 0)
    local_frame () x n j

theorem ack_nondeterministic (q : Fin 4) : ¬ ackMachine.infiniteRel q q := by
  rw [← deterministicBit_spec]
  fin_cases q <;> decide

/-- The physical Boolean stream is atomless, despite constant accepted receipts. -/
theorem physical_atomic_mass_zero : P02A2.mass (law ackMachine 0) = 0 := by
  apply (atomic_mass_zero_iff_unreachable ackMachine 0).mpr
  intro u
  exact ack_nondeterministic _

theorem compiled_physical_defect_one :
    P02A2.defect (fairCantor.map (Indexed.runtimeOutput (index ackMachine 0))) = 1 := by
  rw [compiled_runtime_law]
  simp [P02A2.defect, physical_atomic_mass_zero]

/-- Number of complete accepted frames up to and including frame m. -/
def acknowledgments (z : Cantor) (m : ℕ) : ℕ :=
  ∑ k : Fin (m+1), if z (4*k) then 1 else 0

/-- Genuine acknowledgment-indexed receipt readout. A missing receipt uses false only
for the total mathematical map, never as a runtime-generated receipt. -/
noncomputable def decodeReceipts (z : Cantor) : Cantor := by
  classical
  exact fun n => if h : ∃ m, acknowledgments z m = n+1 then z (4*Nat.find h+3) else false

theorem measurable_acknowledgments (m : ℕ) : Measurable (fun z => acknowledgments z m) := by
  unfold acknowledgments
  apply Finset.measurable_sum
  intro k hk
  have hp : MeasurableSet {z : Cantor | z (4*k) = true} :=
    (measurable_pi_apply (4*(k : ℕ)) : Measurable (fun z : Cantor => z (4*k)))
      (measurableSet_singleton true)
  exact Measurable.ite hp measurable_const measurable_const

theorem measurable_decodeReceipts : Measurable decodeReceipts := by
  classical
  apply measurable_pi_lambda
  intro n
  let P : Cantor → Prop := fun z => ∃ m, acknowledgments z m = n+1
  have hm (m : ℕ) : MeasurableSet {z : Cantor | acknowledgments z m = n+1} :=
    (measurable_acknowledgments m) (measurableSet_singleton _)
  have hP : MeasurableSet {z | P z} := by
    simpa [P,Set.setOf_exists] using MeasurableSet.iUnion (fun m => hm m)
  have hfind : Measurable (fun z : {z : Cantor // P z} =>
      z.val (4*Nat.find z.property+3)) := by
    exact Measurable.find (f := fun m (z : {z : Cantor // P z}) => z.val (4*m+3))
      (p := fun m z => acknowledgments z.val m = n+1)
      (fun m => (measurable_pi_apply (4*m+3)).comp measurable_subtype_coe)
      (fun m => (hm m).preimage measurable_subtype_coe)
      (fun z => z.property)
  exact hfind.dite measurable_const hP

theorem decoded_output_constant (x : Cantor) :
    decodeReceipts (output ackMachine 0 x) = fun _ => false := by
  funext n
  unfold decodeReceipts
  split
  · exact exact_frames x _ (3 : Fin 4)
  · rfl

theorem decoded_runtime_constant :
    (fun x => decodeReceipts (Indexed.runtimeOutput (index ackMachine 0) x)) =
      fun (_ : Cantor) (_ : ℕ) => false := by
  rw [compiled_runtime_output]
  funext x
  exact decoded_output_constant x

theorem decoded_runtime_law :
    fairCantor.map (fun x => decodeReceipts (Indexed.runtimeOutput (index ackMachine 0) x)) =
      Measure.dirac (fun (_ : ℕ) => false) := by
  rw [decoded_runtime_constant, Measure.map_const]
  simp

theorem decoded_runtime_defect_zero :
    P02A2.defect (fairCantor.map (fun x => decodeReceipts
      (Indexed.runtimeOutput (index ackMachine 0) x))) = 0 := by
  rw [decoded_runtime_law]
  have hm : P02A2.mass (Measure.dirac (fun (_ : ℕ) => false)) = 1 := by
    apply P02A2.countable_carrier_mass_one _ (Set.countable_singleton (fun (_ : ℕ) => false))
    · simp
    · simp
  simp [P02A2.defect, hm]

/-- Measurable deterministic projection cannot increase nonatomic defect. -/
theorem defect_map_le {X Y : Type*} [MeasurableSpace X] [MeasurableSingletonClass X]
    [MeasurableSpace Y] [MeasurableSingletonClass Y] (μ : Measure X) [IsProbabilityMeasure μ]
    (f : X → Y) (hf : Measurable f) : P02A2.defect (μ.map f) ≤ P02A2.defect μ := by
  have hh := P02A2.mass_map_mono μ hf
  have hm : P02A2.mass (μ.map f) ≠ ⊤ := measure_ne_top _ _
  have hreal := ENNReal.toReal_mono hm hh
  simp only [P02A2.defect]
  linarith


/-- Countable fibres are a sufficient exact defect-safe observation criterion.
Random rejection serialization need not have countable fibres. -/
theorem mass_map_eq_of_countable_fibres {X Y : Type*}
    [MeasurableSpace X] [MeasurableSingletonClass X]
    [MeasurableSpace Y] [MeasurableSingletonClass Y] (μ : Measure X) [IsFiniteMeasure μ]
    (f : X → Y) (hf : Measurable f) (hc : ∀ y, (f ⁻¹' {y}).Countable) :
    P02A2.mass (μ.map f) = P02A2.mass μ := by
  have he : f ⁻¹' P02A2.positive (μ.map f) =
      ⋃ y ∈ P02A2.positive (μ.map f), f ⁻¹' {y} := by ext x; simp
  have hcount : (f ⁻¹' P02A2.positive (μ.map f)).Countable := by
    rw [he]
    exact (P02A2.positive_countable _).biUnion (fun y _ => hc y)
  have hm := P02A2.mass_eq_countable_superset μ hcount (P02A2.positive_subset_preimage μ hf)
  unfold P02A2.mass at hm ⊢
  rw [Measure.map_apply hf (P02A2.positive_measurable _)]
  exact hm.symm

theorem defect_map_eq_of_countable_fibres {X Y : Type*}
    [MeasurableSpace X] [MeasurableSingletonClass X]
    [MeasurableSpace Y] [MeasurableSingletonClass Y] (μ : Measure X) [IsFiniteMeasure μ]
    (f : X → Y) (hf : Measurable f) (hc : ∀ y, (f ⁻¹' {y}).Countable) :
    P02A2.defect (μ.map f) = P02A2.defect μ := by
  simp only [P02A2.defect, mass_map_eq_of_countable_fibres μ f hf hc]

end Orthemology.RationalLaw.ProjectionControl
