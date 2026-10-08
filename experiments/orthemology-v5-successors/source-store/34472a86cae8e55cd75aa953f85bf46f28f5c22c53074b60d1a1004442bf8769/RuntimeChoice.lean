import RuntimeAudit
noncomputable def chosenPolicyNumber : Nat := Classical.choose (show ∃ n : Nat, n = 0 from ⟨0,rfl⟩)
#audit_policy_runtime chosenPolicyNumber
