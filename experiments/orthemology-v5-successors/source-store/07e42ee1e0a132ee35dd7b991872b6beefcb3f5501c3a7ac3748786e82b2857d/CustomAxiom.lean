import LookaheadAudit
axiom forgedLookahead : False
theorem fakeLookahead : False := forgedLookahead
#audit_renewal_closure fakeLookahead
