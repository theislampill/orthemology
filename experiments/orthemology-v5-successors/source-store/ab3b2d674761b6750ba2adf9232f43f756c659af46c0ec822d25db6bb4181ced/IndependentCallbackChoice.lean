import LookaheadBoundary
import RuntimeAudit
open EffectiveRenewal EffectiveRenewal.Lookahead
noncomputable def independentChoiceDemand (s : Word) : Nat :=
  Classical.choice (show Nonempty Nat from ⟨s.length⟩)
theorem independentChoiceDemand_computable : Computable independentChoiceDemand :=
  Computable.const (Classical.choice (show Nonempty Nat from ⟨0⟩))
noncomputable def independentChoicePlan : Nat → Word := lookaheadPlan independentChoiceDemand
theorem independentChoicePlan_computable : Computable independentChoicePlan :=
  lookaheadPlan_computable independentChoiceDemand independentChoiceDemand_computable
#audit_renewal_runtime independentChoicePlan
