import RuntimeAudit
partial def renewalPartialRuntimeHidden (n : Nat) : Nat := renewalPartialRuntimeHidden n
def renewalRuntimeWrapper (n : Nat) : Nat := renewalPartialRuntimeHidden n
#audit_renewal_runtime renewalRuntimeWrapper
