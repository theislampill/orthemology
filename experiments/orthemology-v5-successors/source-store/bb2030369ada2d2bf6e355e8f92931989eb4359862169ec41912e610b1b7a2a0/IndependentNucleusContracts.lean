import TypedNegativeControls
import IndependentEndpointControls
namespace TypedNucleusIndependentReview
open OrthemologyV2 OrthemologyV3 P01D P01R P01TC
open P01F (cons)

/-- A malformed identity family cannot bypass endpoint typing. -/
theorem malformed_raw_identity_unformable :
    ¬ Form [.param 0] (.identity .raw (.var 0) (.atom .i)) := by
  intro h
  cases h with
  | identity hA hp hq => exact P01TC.Negative.no_universal_raw_variable hp

/-- Scoping holds for any result type, not only Raw. -/
theorem empty_variable_untypable (A : P01TC.Ty) : ¬ Has [] (.var 0) A := by
  intro h
  exact Nat.not_lt_zero 0 (has_scoped h)

/-- This checks the actual universal diagonal theorem at related unequal values. -/
theorem strong_diagonal_distinct_valuation_contract (ρ : OEnv) (t u : Term) :
    G typedPairType (diagEnv (identityParameters ρ))
      (cons .i zeroEnv) (cons P01DF.skk zeroEnv) t u ↔
    F typedPairType (identityParameters ρ) (cons .i zeroEnv) t u :=
  strong_diagonal typed_pair_form (ρ := identityParameters ρ)
    (η := cons .i zeroEnv) (ξ := cons P01DF.skk zeroEnv)
    ⟨⟨rfl,rfl⟩,identity_parameters_I_SKK ρ⟩ t u

/-- Distinct endpoint objects and distinct valuations are both exercised. -/
theorem pair_genuinely_heterogeneous :
    G typedPairType P01TC.Negative.rightSeparating
      (cons .i zeroEnv) (cons P01DF.skk zeroEnv)
      (pairTerm .i .i) (pairTerm P01DF.skk .i) :=
  typed_pair_related _ _ _ True.intro

/-- Finite substitution into the empty context is exactly zero padded. -/
theorem empty_substitution_padding_contract (η : Env) :
    subEnv [] η = zeroEnv := rfl

theorem literal_substitution_contract {Δ Γ σ p A}
    (hs : TypedSub Δ Γ σ) (hp : Has Γ p A) :
    Has Δ (psub (images σ) p) (P01TC.subst (images σ) A) := hs.has hp

#print axioms malformed_raw_identity_unformable
#print axioms empty_variable_untypable
#print axioms strong_diagonal_distinct_valuation_contract
#print axioms pair_genuinely_heterogeneous
#print axioms empty_substitution_padding_contract
#print axioms literal_substitution_contract
#print P01TC.Ty
#print P01TC.Ctx
#print P01TC.Form
#print P01TC.Has
#print P01TC.F
#print P01TC.G
#print P01TC.TypeLaws
#print P01TC.fundamental
#print P01TC.unary_fundamental
#print P01TC.strong_diagonal
#print P01TC.two_sided_invariance
#print P01TC.TypedSub
#print P01TC.TypedSub.has
#print P01TC.representedTerm_code
#print P01TC.represented_substitution_code
#print P01TC.represented_substitution_type
#print P01TC.representedContextualJ
#print P01TC.representedContextualJ_code
#print P01TC.contextual_target_exact
#print axioms P01TC.form_sound
#print axioms P01TC.has_sound
#print axioms P01TC.fundamental
#print axioms P01TC.TypedSub.has
#print axioms P01TC.representedTerm
#print axioms P01TC.representedSub
#print axioms P01TC.representedContextualJ
#print axioms P01TC.typed_pair_abstraction_has
#print axioms P01TC.literal_j_has
#print axioms P01TC.raw_fibres_nonempty_and_vary
#print axioms P01TC.Negative.no_universal_raw_variable
#print axioms P01TC.Negative.right_cross_links_without_equality
#print axioms P01TC.Negative.left_cross_links_without_equality
#print axioms P01TC.Negative.j_endpoint_omission_fails
#print axioms P01TC.Negative.j_proof_coordinate_omission_fails
end TypedNucleusIndependentReview
