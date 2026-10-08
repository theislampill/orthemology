import RuntimeAudit
noncomputable def counterfeitEffectiveChoice : Nat := Classical.choice (show Nonempty Nat from ⟨0⟩)
#audit_renewal_runtime counterfeitEffectiveChoice
