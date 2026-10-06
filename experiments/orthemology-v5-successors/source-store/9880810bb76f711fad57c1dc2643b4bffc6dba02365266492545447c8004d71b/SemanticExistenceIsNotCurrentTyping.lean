/- Expected rejection: interface control, not a mathematical independence proof. -/
import EffectiveRuleBoundary
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC P01AC.EffectiveCompleteness

example (p q : Poly) (h : IdentityValid p q) :
    ∃ e : Poly, Has [] e (.identity C p q) := by
  exact (semantic_proof_exists_iff_valid p q).mpr h
