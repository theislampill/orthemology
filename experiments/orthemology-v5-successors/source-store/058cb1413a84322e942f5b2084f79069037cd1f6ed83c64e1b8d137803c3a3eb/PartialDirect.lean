import LookaheadAudit
partial def hiddenLookaheadPartial (n : Nat) : Nat := hiddenLookaheadPartial n
#audit_renewal_closure hiddenLookaheadPartial
#audit_renewal_runtime hiddenLookaheadPartial
