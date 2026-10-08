import FullControllerRuntime
import RuntimeReceiptPath

/-! Source-bound rational receipt laws for the complete Boolean phase controller.
This composes two separately frozen source frontiers. The row-environment and
initial-state equalities remain explicit; no arbitrary finite or arbitrary
rational environment compiler is inferred from the binary fixture wrapper. -/
namespace Orthemology.RuntimeBridge.PhaseUpdate.FullController
open MeasureTheory
open scoped ENNReal
open Orthemology.Frontier.MealyMeasure
open Orthemology.RuntimeBridge.HistoryRuntime
open Orthemology.RationalLaw Orthemology.RationalLaw.RuntimeBinding
open P02A2.Q8Measure (fairCantor)
open HiddenParity HiddenParity.Sufficiency

/-- The ordinary chronological kernel product, using the actual generated
controller and only its acquired action/receipt history at every factor. -/
noncomputable def kernelReceiptMass (c : Config) (menu : Finset Bool → Bool → Finset Bool)
    (priority : Bool → (Bool × Bool) → ℕ) (σ : Bool) :
    (n : ℕ) → HistoryFold.History → (Fin n → Bool) → ℝ≥0∞
  | 0, _, _ => 1
  | n+1, h, ys =>
      ENNReal.ofReal (c.kernel.row σ (observedState c.initialState h,policy c menu priority h) (ys 0)) *
      kernelReceiptMass c menu priority σ n ((policy c menu priority h,ys 0)::h) (fun i => ys i.succ)

theorem generated_kernel_mass_exact (c : Config) (menu : Finset Bool → Bool → Finset Bool)
    (priority : Bool → (Bool × Bool) → ℕ) (hc : Certificate c menu priority)
    (hkernel : c.kernel = Controller.Fixture.kernel) (σ : Bool) (n : ℕ)
    (h : HistoryFold.History) (ys : Fin n → Bool) :
    historyMass 3 (adaptiveRow σ (sourcePolicy c)) (RuntimeBinding.update (sourcePolicy c)) n h ys =
      kernelReceiptMass c menu priority σ n h ys := by
  induction n generalizing h with
  | zero => rfl
  | succ n ih =>
      rw [historyMass,kernelReceiptMass]
      simp only [adaptiveRow,historyPolicy,source_policy_retained_exact c menu priority hc]
      simp only [Nat.cast_ofNat]
      rw [weight_div_three_eq_kernel σ (observedState c.initialState h)]
      rw [ih]
      simp only [RuntimeBinding.update,historyPolicy,source_policy_retained_exact c menu priority hc,hkernel]

/-- Exact finite cylinders of the total measurable decoded path, obtained from
literal indexed stack output under the original fair input law. -/
theorem full_phase_runtime_receipt_cylinders (c : Config)
    (menu : Finset Bool → Bool → Finset Bool) (priority : Bool → (Bool × Bool) → ℕ)
    (hc : Certificate c menu priority) (hkernel : c.kernel = Controller.Fixture.kernel)
    (σ : Bool) (n : ℕ) (ys : Fin n → Bool) :
    (fairCantor.map (runtimeReceiptPath (policyProgram c) σ)) (receiptCylinder n ys) =
      kernelReceiptMass c menu priority σ n [] ys := by
  rw [runtime_receipt_path_cylinder_probability (policyProgram c) (sourcePolicy c) (policy_program_implements c),
    generated_kernel_mass_exact c menu priority hc hkernel]

/-- Complete path law is fixed by the derived cylinders. The supplied measure
is specified by the usual kernel products, never by an assumed sampler law. -/
theorem full_phase_runtime_law_unique (c : Config)
    (menu : Finset Bool → Bool → Finset Bool) (priority : Bool → (Bool × Bool) → ℕ)
    (hc : Certificate c menu priority) (hkernel : c.kernel = Controller.Fixture.kernel)
    (σ : Bool) (ν : Measure Cantor) [IsFiniteMeasure ν]
    (hν : ∀ n ys, ν (receiptCylinder n ys) = kernelReceiptMass c menu priority σ n [] ys) :
    fairCantor.map (runtimeReceiptPath (policyProgram c) σ) = ν := by
  apply receipt_law_ext
  intro n ys
  rw [full_phase_runtime_receipt_cylinders c menu priority hc hkernel,hν]

/-- The logical histories and common-denominator rejection clock factorize in
the actual runtime. This is not a wall-clock or a P02 instruction-count bound. -/
theorem full_phase_runtime_joint_clock (c : Config)
    (menu : Finset Bool → Bool → Finset Bool) (priority : Bool → (Bool × Bool) → ℕ)
    (hc : Certificate c menu priority) (hkernel : c.kernel = Controller.Fixture.kernel)
    (σ : Bool) (n : ℕ) (ys : Fin n → Bool) (rs : Fin n → ℕ) :
    fairCantor {x | reportsWithCounts n ys rs (runtimeProposal (policyProgram c) σ x)} =
      kernelReceiptMass c menu priority σ n [] ys * clockMass 2 3 n rs := by
  rw [runtime_joint_probability (policyProgram c) (sourcePolicy c) (policy_program_implements c),
    generated_kernel_mass_exact c menu priority hc hkernel]

/-- No false receipt is inserted by a timeout; actual logical completion holds
almost surely, with explicit null forever-rejection still possible. -/
theorem full_phase_runtime_receipts_complete (c : Config) (σ : Bool) :
    ∀ᵐ x ∂fairCantor, ∀ n, ∃ ys : Fin n → Bool, reports n ys (runtimeProposal (policyProgram c) σ x) :=
  runtime_infinitely_many_reports (policyProgram c) (sourcePolicy c) (policy_program_implements c) σ

end Orthemology.RuntimeBridge.PhaseUpdate.FullController
