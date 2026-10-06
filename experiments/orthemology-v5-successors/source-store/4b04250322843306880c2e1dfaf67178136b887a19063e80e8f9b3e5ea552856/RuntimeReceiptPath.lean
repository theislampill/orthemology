import RuntimeRationalBinding
import ReceiptPathDecoder

namespace Orthemology.RationalLaw.RuntimeBinding
open MeasureTheory Set
open Orthemology.Frontier.MealyMeasure Orthemology.RuntimeBridge
open Orthemology.CertifiedObserver
open P02A2.Q8Measure (fairCantor)
open Orthemology.RuntimeBridge.HistoryRuntime

/-- Variable-length receipt extraction as a total mathematical path. The fallback
at an unavailable coordinate is used only on the explicitly null noncompletion set. -/
noncomputable def runtimeReceiptPath (p : P02A2.PRProgram.Program 1) (σ : Bool) (x : Cantor) : Cantor :=
  decodeReports (runtimeProposal p σ x)

theorem runtimeProposal_event_measurable (p : P02A2.PRProgram.Program 1) (σ : Bool)
    (k : ℕ) (y : Option Bool) : MeasurableSet {x | runtimeProposal p σ x k = y} := by
  have hm (j : ℕ) : Measurable (fun x : Cantor => Indexed.runtimeOutput (runtimeIndex p σ) x j) :=
    (measurable_pi_apply j).comp (Indexed.runtime_output_measurable _)
  cases y with
  | none =>
      have he : {x | runtimeProposal p σ x k = none} =
          {x | Indexed.runtimeOutput (runtimeIndex p σ) x (8*k+4) = false} := by
        ext x
        cases hh : Indexed.runtimeOutput (runtimeIndex p σ) x (8*k+4) <;> simp [runtimeProposal,hh]
      rw [he]
      exact (hm _) (measurableSet_singleton false)
  | some y =>
      have he : {x | runtimeProposal p σ x k = some y} =
          {x | Indexed.runtimeOutput (runtimeIndex p σ) x (8*k+4) = true} ∩
          {x | Indexed.runtimeOutput (runtimeIndex p σ) x (8*k+7) = y} := by
        ext x
        cases hh : Indexed.runtimeOutput (runtimeIndex p σ) x (8*k+4) <;> simp [runtimeProposal,hh]
      rw [he]
      exact ((hm _) (measurableSet_singleton true)).inter ((hm _) (measurableSet_singleton y))

theorem runtimeReceiptPath_measurable (p : P02A2.PRProgram.Program 1) (σ : Bool) :
    Measurable (runtimeReceiptPath p σ) :=
  measurable_decodeReports _ (runtimeProposal_event_measurable p σ)

/-- Every finite cylinder of the total decoded path has the exact adaptive rational
mass, derived from actual P02 output and original fair-bit cylinder measures. -/
theorem runtime_receipt_path_cylinder_probability (p : P02A2.PRProgram.Program 1) (a : ℕ → Bool)
    (hp : PolicyImplements p a) (σ : Bool) (n : ℕ) (ys : Fin n → Bool) :
    (fairCantor.map (runtimeReceiptPath p σ)) (receiptCylinder n ys) =
      historyMass 3 (adaptiveRow σ a) (update a) n [] ys := by
  unfold runtimeReceiptPath
  rw [decoded_cylinder_eq_report_event fairCantor (runtimeProposal p σ)
    (runtimeProposal_event_measurable p σ) (runtime_infinitely_many_reports p a hp σ)]
  exact runtime_accepted_history_probability p a hp σ n ys

/-- A complete sequence law is uniquely characterized by these derived cylinders.
The target hypothesis describes the target law; it is not a sampler-law premise. -/
theorem runtime_receipt_path_law_unique (p : P02A2.PRProgram.Program 1) (a : ℕ → Bool)
    (hp : PolicyImplements p a) (σ : Bool) (ν : Measure Cantor) [IsFiniteMeasure ν]
    (hν : ∀ n ys, ν (receiptCylinder n ys) = historyMass 3 (adaptiveRow σ a) (update a) n [] ys) :
    fairCantor.map (runtimeReceiptPath p σ) = ν := by
  apply receipt_law_ext
  intro n ys
  rw [runtime_receipt_path_cylinder_probability p a hp, hν]

end Orthemology.RationalLaw.RuntimeBinding
