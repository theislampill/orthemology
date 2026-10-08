import RationalFixtures
open TraceControls

-- Retention 1/4 is not deletion 1/4.
example : tv (mass word00) (mass word01) = (3/4 : ℚ) := by
  rw [one_trace_tv]
  norm_num

-- The positive-copy theorem cannot include zero observations.
example : (copiedTV 0 : ℚ) = 1/4 := by
  rw [zero_data_tv]
  norm_num

-- Observing the single zero does not force retention of the first position.
example : emit word00 (false,true) ≠ zero := by
  decide

-- Different historical labels alone do not alter this content-only channel.
example : (worldMass (false,word00) : Trace → ℚ) ≠ worldMass (true,word00) := by
  change ¬((mass word00 : Trace → ℚ) = mass word00)
  simp
