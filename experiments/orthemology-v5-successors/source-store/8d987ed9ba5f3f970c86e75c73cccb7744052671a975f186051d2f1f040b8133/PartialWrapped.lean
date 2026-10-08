import LookaheadAudit
partial def hiddenLookaheadLoop (n : Nat) : Nat := hiddenLookaheadLoop n
def wrappedLookaheadLoop (n : Nat) : Nat := hiddenLookaheadLoop n
#audit_renewal_closure wrappedLookaheadLoop
#audit_renewal_runtime wrappedLookaheadLoop
