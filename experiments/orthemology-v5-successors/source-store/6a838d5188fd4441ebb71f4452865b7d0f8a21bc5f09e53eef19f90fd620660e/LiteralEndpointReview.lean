import LiteralRuntimeCounterexample
set_option autoImplicit false
noncomputable section
namespace LiteralControlIndependentReview
open MeasureTheory
open HiddenParity HiddenParity.Sufficiency HiddenParity.Stochastic HiddenParity.Necessity
open Orthemology.Tranche2.PolicyEmbedding
open Orthemology.RuntimeBridge
open Orthemology.RuntimeBridge.PhaseUpdate.FullController
open Orthemology.RationalLaw.CanonicalBinding
open Orthemology.Eighth.SemanticControls
open P02A2.Q8Measure (fairCantor)

open Orthemology.Eighth.SemanticControls.LiteralAssessment
def ExtractedMutantStatement : Prop :=
∀ (c : Config)
    (menu : Finset Bool → Bool → Finset Bool) (priority : Bool → (Bool × Bool) → ℕ)
    (hc : Certificate c menu priority) (hkernel : c.kernel = Controller.Fixture.kernel)
    (hinit : c.initialState = false)
    (hs : c.initialState ∈ winningRegion c.kernel menu priority c.initialSupport)
    (σ : Bool) (hσ : σ ∈ c.initialSupport) (d : Bool × Bool),
    ∀ᵐ x ∂fairCantor,
      ParitySuccess (priority σ) (historyAction d
        (decodedHistory (policyProgram c) (sourcePolicy (withComputedTolerance c)) σ x))

theorem literal_extracted_statement_exact : ExtractedMutantStatement = MutatedRuntimeClaim := rfl

-- Use all exact inherited hypotheses from each certified literal branch.
-- The conclusion remains old program / computed decoder under one fixed model.
theorem literal_endpoint_refutes_extracted : ¬ ExtractedMutantStatement := by
  intro h
  have reject_branch (orientation : Bool) (hf : CertifiedLiteralFailure orientation) : False := by
    rcases hf with ⟨hc, hk, hi, hw, hm, hfail⟩
    exact (hfail (false,false)).ne' (ae_iff.mp
      (h (literalConfig orientation) sparseMenu actionPriority hc hk hi hw orientation hm (false,false)))
  rcases explicit_two_literal_counterexamples with hf | ht
  · exact reject_branch false hf
  · exact reject_branch true ht

#print axioms literal_extracted_statement_exact
#print axioms literal_endpoint_refutes_extracted
end LiteralControlIndependentReview
