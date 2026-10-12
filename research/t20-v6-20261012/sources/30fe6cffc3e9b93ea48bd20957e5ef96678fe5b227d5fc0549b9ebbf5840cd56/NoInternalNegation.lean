import Application

/- Complementary model argument: meta-level absence of a source refutation.
The inherited full-PER model semantically validates W, without deriving W. -/
namespace T20SourceIndependence
open P01AC P01D
open P01AC.ExtensionalRepair (HasE)
open P01AC.ExtensionalRepair.ExactScalarFusion (W c3)

 theorem no_internal_negation (p : Poly) :
    ¬ HasE [] p (arr (W FullPER.Application.originalQ) .bottom) := by
  intro h
  have hp := FullPER.fundamental h FullPER.Application.emptyEnv
    FullPER.zeroEnv FullPER.zeroEnv FullPER.Application.emptyEnv_admissible ⟨rfl,rfl⟩
  rw [FullPER.F_arr] at hp
  exact hp _ _ (FullPER.Application.scalar_target_valid
    FullPER.Application.emptyEnv FullPER.zeroEnv)

#print axioms no_internal_negation
end T20SourceIndependence
