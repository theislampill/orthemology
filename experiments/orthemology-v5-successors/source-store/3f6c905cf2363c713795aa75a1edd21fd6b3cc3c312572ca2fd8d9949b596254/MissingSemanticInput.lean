/- Expected rejection: interface control, not a mathematical independence proof. -/
import EffectiveRuleBoundary
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC P01AC.EffectiveCompleteness

example (t : Term) (ρ : OEnv) (η : Env) :
    ∃ n, ∀ f x, Conv (.app (.app t f) x) (iterateTerm f n x) := by
  exact @semantic_church_standardness t ρ η
