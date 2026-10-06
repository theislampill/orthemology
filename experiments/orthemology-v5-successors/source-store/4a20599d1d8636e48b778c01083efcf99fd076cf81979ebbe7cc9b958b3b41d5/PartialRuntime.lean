import RuntimeAudit
partial def partialPolicyNumber (n : Nat) : Nat := partialPolicyNumber (n+1)
def wrappedPartialPolicyNumber (n : Nat) : Nat := partialPolicyNumber n
#audit_policy_runtime wrappedPartialPolicyNumber
