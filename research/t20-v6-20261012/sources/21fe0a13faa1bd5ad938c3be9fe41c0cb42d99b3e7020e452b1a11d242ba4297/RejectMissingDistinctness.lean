import MomentRecovery
-- The distinct-support premise cannot be silently discarded.
example {K : Type*} [Field K] {N : ℕ} (a w : Fin N → K) :
    FiniteMoment.recover a (FiniteMoment.record a w) = w := by
  exact FiniteMoment.recover_record a w
