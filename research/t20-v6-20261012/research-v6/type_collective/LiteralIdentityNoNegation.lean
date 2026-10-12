import Application

/-- Direct application of soundness to the semantic inhabitant of the literal
identity. No internal bridge from identity to W is assumed. -/
theorem literal_identity_has_no_internal_negation (p : P01D.Poly) :
    ¬ P01AC.ExtensionalRepair.HasE [] p
      (P01AC.arr FullPER.Application.originalIdentity P01AC.Ty.bottom) := by
  intro h
  have hp := FullPER.fundamental h FullPER.Application.emptyEnv
    FullPER.zeroEnv FullPER.zeroEnv FullPER.Application.emptyEnv_admissible ⟨rfl, rfl⟩
  rw [FullPER.F_arr] at hp
  exact hp _ _ (FullPER.Application.original_identity_inhabited
    FullPER.Application.emptyEnv FullPER.zeroEnv)
