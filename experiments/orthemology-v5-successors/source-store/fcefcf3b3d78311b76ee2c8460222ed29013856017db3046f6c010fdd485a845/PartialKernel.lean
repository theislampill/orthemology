import KernelAudit
partial def partialPolicyEvidence (n : Nat) : Nat := partialPolicyEvidence (n+1)
def wrappedPartialPolicyEvidence (n : Nat) : Nat := partialPolicyEvidence n
#audit_policy_closure wrappedPartialPolicyEvidence
