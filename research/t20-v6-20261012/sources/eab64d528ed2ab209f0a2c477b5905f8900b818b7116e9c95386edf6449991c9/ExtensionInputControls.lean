import ClosedChurchReviewControls
namespace ClosedChurchReview
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC P01AC.ExtensionalRepair
open P01AC.EffectiveCompleteness (N NBody inputNumeral iterationPoly)
open P01AC.ExtensionalRepair.ExactScalarFusion (i)
open P01AC.Intensional.Plus (PolyConvPlus)
open ClosedChurchIdentity ClosedChurchIdentity.Controls
open OpenDevelopments OpenDevelopments.DomainControls

-- This input's actual derivation uses J on the extensional I=SKK identity.
-- It is not merely an old-Has proof embedded at the top level.
def transported : Poly := jPoly (padded 2) (.atom P01R.skk) i

theorem transported_has : HasE [] transported N := by
  have cN : Ctx [N] := .ext .nil (EffectiveCompleteness.N_form .nil)
  have hi : HasE [N] i N := Structural.has_closed iTyping (ctx_inclusion cN)
  have hv : HasE [N] (.var 0) N := .var (formN cN) .zero
  have htheta : CtxE (theta [] N i) :=
    .ext (ctx_inclusion cN) (.identity (formN cN) hi hv)
  have hB : FormE (theta [] N i) N :=
    ClosedProofCanonicalisation.formed (Structural.has_closed (padded_has 2) htheta)
  exact .j (formN .nil) hB (ClosedProofCanonicalisation.formed ext_has)
    (formN .nil) (formN .nil) iTyping skkTyping ext_has (padded_has 2)

theorem transported_conversion : PolyConvPlus transported (padded 2) :=
  (PolyConvPlus.app (PolyConvPlus.k (.app (.atom .k) (padded 2)) (.atom P01R.skk))
    (.refl i)).trans (PolyConvPlus.k (padded 2) i)

theorem transported_observation :
    PolyConvPlus (ClosedScalarInstances.scalarLeft transported) (iterationPoly 2) :=
  (PolyConvPlus.app (PolyConvPlus.app transported_conversion (.refl (.var 1)))
    (.refl (.var 0))).trans (padded_observation 2)

theorem transported_identity : HasE [] i (.identity N transported (inputNumeral 2)) :=
  canonicity_at_count transported_has transported_observation

theorem transported_actual_lift : HasE [proofIdentity] transported N :=
  Structural.has_closed transported_has richCtx

theorem extracted_count_proof_independent {n : Poly} (h h' : HasE [] n N) :
    (extractIteration n h).val = (extractIteration n h').val := rfl

#guard @decide _ (EffectiveChurchIdentity.decideTypedIdentity transported_has (packed_has 2))
#guard !(@decide _ (EffectiveChurchIdentity.decideTypedIdentityExists transported_has (packed_has 3)))
#eval (extractIteration transported transported_has).val
#print axioms transported_has
#print axioms transported_identity
#print axioms transported_actual_lift
end ClosedChurchReview
