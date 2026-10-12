import ImportedCompilerTransport

namespace IndependentTransportReview
open OpenTermStandardness ImportedOpenTermTransport

-- Explicit signatures rule out hidden local hypotheses on the bridge.
example : Function.Injective embed := embed_injective
example (t u : OrthemologyV2.Term) :
    Conv (embed t) (embed u) ↔ OrthemologyV3.Conv t u := embed_conversion_iff t u
example (p : P01D.Poly) : poly (P01D.abstract p) = abstract (poly p) := map_abstract p
example (p r : P01D.Poly) (h : P01AC.Intensional.Plus.PolyConvPlus p r)
    (η : Nat → T) : Conv (interp p η) (interp r η) := source_plus_sound h η

-- The literal closed compiler output is independent even of arbitrary OPEN valuations.
theorem original_q_open_interp_exact (η : Nat → T) :
    interp P01AC.UnaryIdentity.IntensionalBoundary.redundantExpr.closed η = q := by
  unfold interp
  rw [original_q_poly_exact]
  exact q_eval_independent η

theorem original_p_open_interp_exact (η : Nat → T) :
    interp P01AC.UnaryIdentity.IntensionalBoundary.variableExpr.closed η = .i := by
  unfold interp
  rw [original_p_poly_exact]
  rfl

-- Heterogeneous valuations do not weaken the actual endpoint relation.
theorem endpoints_across_open_valuations (η θ : Nat → T) :
    (arrowPER churchPER churchPER).rel
      (interp P01AC.UnaryIdentity.IntensionalBoundary.variableExpr.closed η)
      (interp P01AC.UnaryIdentity.IntensionalBoundary.redundantExpr.closed θ) := by
  rw [original_p_open_interp_exact, original_q_open_interp_exact]
  exact identity_q_related

-- Typed relation and raw nonconversion genuinely coexist in the same new carrier.
theorem mirror_raw_separation : ¬ Conv .i q := by
  have h := original_raw_endpoints_still_distinct
  simpa only [original_p_eval_exact, original_q_eval_exact] using h

theorem typed_agreement_without_raw_conversion :
    (arrowPER churchPER churchPER).rel .i q ∧ ¬ Conv .i q :=
  ⟨identity_q_related, mirror_raw_separation⟩

#print axioms ImportedOpenTermTransport.erase_embed
#print axioms ImportedOpenTermTransport.embed_injective
#print axioms ImportedOpenTermTransport.map_psub
#print axioms ImportedOpenTermTransport.map_freeZero
#print axioms ImportedOpenTermTransport.map_drop
#print axioms ImportedOpenTermTransport.map_abstract
#print axioms ImportedOpenTermTransport.map_eval
#print axioms ImportedOpenTermTransport.interp_abstraction_beta
#print axioms ImportedOpenTermTransport.source_step_sound
#print axioms ImportedOpenTermTransport.source_conv_sound
#print axioms ImportedOpenTermTransport.erase_conv
#print axioms ImportedOpenTermTransport.embed_conversion_iff
#print axioms ImportedOpenTermTransport.source_plus_sound
#print axioms ImportedOpenTermTransport.original_q_poly_exact
#print axioms ImportedOpenTermTransport.original_p_poly_exact
#print axioms ImportedOpenTermTransport.q_eval_independent
#print axioms ImportedOpenTermTransport.original_q_eval_exact
#print axioms ImportedOpenTermTransport.original_p_eval_exact
#print axioms ImportedOpenTermTransport.original_endpoints_related
#print axioms ImportedOpenTermTransport.original_raw_endpoints_still_distinct
#print axioms original_q_open_interp_exact
#print axioms endpoints_across_open_valuations
#print axioms typed_agreement_without_raw_conversion
end IndependentTransportReview
