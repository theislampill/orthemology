import HiddenChangePhaseArithmetic

-- Intentionally false literal-residue mutation. The barrier for mode one
-- must not be accepted as a mode-zero barrier. Expected kernel-checked failure.
example : ((2 * 7 + (1 : Fin 2).val) % 2 : ℕ) = (0 : Fin 2).val := by
  decide +kernel
