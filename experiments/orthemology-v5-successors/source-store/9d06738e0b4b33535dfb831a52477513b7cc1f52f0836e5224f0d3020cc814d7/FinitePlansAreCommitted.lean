import EffectiveRenewalBoundary
open EffectiveRenewal EffectiveRenewal.Pruning
-- Dropping the negation would silently conflate separate horizons with commitment.
example : Committed finitePlan := finitePlans_not_committed
