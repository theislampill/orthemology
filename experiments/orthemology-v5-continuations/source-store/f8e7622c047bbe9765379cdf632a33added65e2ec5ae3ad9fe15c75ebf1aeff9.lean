import HeldStateProjectionDefect
import ReceiptPathDecoder

namespace Orthemology.RationalLaw.HeldStateControl
open MeasureTheory Set
open Orthemology.Frontier Orthemology.Frontier.MealyMeasure
open Orthemology.CertifiedObserver
open P02A2.Q8Measure (fairCantor)

noncomputable def compressHeld (z : Cantor) : Cantor
  | 0 => z 0
  | n+1 => decodeReports (changeReports z) n

theorem changeReports_event_measurable (k : ℕ) (y : Option Bool) :
    MeasurableSet {z : Cantor | changeReports z k = y} := by
  have hm : Measurable (fun z : Cantor => (z k,z (k+1))) :=
    (measurable_pi_apply k).prodMk (measurable_pi_apply (k+1))
  exact hm ((Set.toFinite {p : Bool × Bool | (if p.2=p.1 then none else some p.2) = y}).measurableSet)

theorem compressHeld_measurable : Measurable compressHeld := by
  have hm := measurable_decodeReports changeReports changeReports_event_measurable
  apply measurable_pi_lambda
  intro n
  cases n with
  | zero => exact measurable_pi_apply 0
  | succ n => exact (measurable_pi_apply n).comp hm

theorem receiptAlternating_eq_iterate (q : Bool) (n : ℕ) :
    receiptAlternating q n = (Bool.not^[n+1]) q := by
  induction n generalizing q with
  | zero => rfl
  | succ n ih => simpa [receiptAlternating, Function.iterate_succ_apply] using ih (!q)

theorem alternating_eq_iterate (n : ℕ) : alternating n = (Bool.not^[n]) false := by
  induction n with
  | zero => rfl
  | succ n ih => simpa [alternating, Function.iterate_succ_apply',ih]

theorem compressed_held_alternating :
    ∀ᵐ x ∂fairCantor, compressHeld (output heldMachine false x) = alternating := by
  filter_upwards [held_infinitely_many_reports] with x hx
  funext n
  cases n with
  | zero => rfl
  | succ n =>
      obtain ⟨ys,hy⟩ := hx (n+1)
      change decodeReports (changeReports (output heldMachine false x)) n = alternating (n+1)
      have h1 := decodeReports_of_reports (n+1) ys _ hy (Fin.last n)
      have h2 := held_reports_alternating (n+1) ys x hy (Fin.last n)
      exact h1.trans (h2.trans (by rw [receiptAlternating_eq_iterate,alternating_eq_iterate]; rfl))

/-- Measurable deletion of repeated held states turns the actual atomless output
law into the deterministic logical law, even though parity is preserved a.s. -/
theorem compressed_held_law : (law heldMachine false).map compressHeld = Measure.dirac alternating := by
  rw [law,Measure.map_map compressHeld_measurable (MealyMeasure.output_measurable heldMachine false),
    Function.comp_def, Measure.map_congr compressed_held_alternating,Measure.map_const]
  simp

theorem compressed_held_defect_zero : P02A2.defect ((law heldMachine false).map compressHeld) = 0 := by
  rw [compressed_held_law]
  exact logical_defect_zero

theorem compiled_compressed_held_law :
    (fairCantor.map (Indexed.runtimeOutput heldIndex)).map compressHeld = Measure.dirac alternating := by
  rw [compiled_held_output]
  exact compressed_held_law

end Orthemology.RationalLaw.HeldStateControl
