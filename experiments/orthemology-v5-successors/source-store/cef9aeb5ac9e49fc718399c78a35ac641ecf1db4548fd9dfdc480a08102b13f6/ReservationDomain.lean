import NegativeControls
open InterlockHistory
namespace InterlockHistory.IndependentReviewV2

/-- The revised premise can preserve the licensed command domain exactly. -/
theorem revised_domain_is_sufficient {n} (c : Config n) :
    Reservation c (fun _ k _ => ValidPath c k) := by
  intro s k requester reachable valid requesterEq authorized
  exact valid

/-- An explicit copy of the V1 predicate, only for testing the correction. -/
def OriginalReservation {n} (c : Config n)
    (externalAllowed : State n → Command n → Nat → Prop) : Prop :=
  ∀ s k requester, Reachable c s → requester = k.recipient →
    Authorized k (c.source s.epoch) → externalAllowed s k requester

def invalidPathCommand : Command 4 := { Controls.command with path := ∅ }

/-- The previous premise forced permission outside the licensed path domain;
    the correction really removes that unused assumption. -/
theorem original_domain_was_stronger :
    ¬OriginalReservation Controls.cfg (fun _ k _ => ValidPath Controls.cfg k) := by
  intro original
  have valid := original Controls.prepared invalidPathCommand 11
    Controls.prepared_reachable rfl (by decide)
  exact (by decide : ¬ValidPath Controls.cfg invalidPathCommand) valid

#print axioms revised_domain_is_sufficient
#print axioms original_domain_was_stronger
end InterlockHistory.IndependentReviewV2
