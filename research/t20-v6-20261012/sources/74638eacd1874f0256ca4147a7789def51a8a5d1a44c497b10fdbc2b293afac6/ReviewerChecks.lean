import FrozenCompilerMirror

namespace OpenTermStandardness.ReviewerChecks
open OpenTermStandardness

/-- Independent reverse direction: the reported uniform behavior is sufficient
    for membership in every ordinary conversion-saturated PER. -/
theorem uniform_implies_church (n : T) (h : UniformIter n) : Church n := by
  obtain ⟨k, hk⟩ := h
  intro R f g hfg x y hxy
  have hi : R.rel (iter f x k) (iter g y k) := by
    clear hk
    induction k with
    | zero => exact hxy
    | succ k ih => exact hfg _ _ ih
  exact R.saturated (hk f x).symm (hk g y).symm hi

theorem exact_characterization (n : T) : Church n ↔ UniformIter n :=
  ⟨church_standard n, uniform_implies_church n⟩

/-- In particular, the full-PER premise has concrete inhabitants. -/
theorem zero_is_church : Church zeroTerm :=
  uniform_implies_church zeroTerm ⟨0, zero_application⟩

theorem successor_numerals_are_church (k : Nat) : Church (successorNumeral k) :=
  uniform_implies_church _ ⟨k, successorNumeral_application k⟩

set_option maxRecDepth 8192
set_option maxHeartbeats 4000000

/-- These source formulas contain no polynomial variables after abstraction,
    so choosing .i for the mirror's default environment does not change q. -/
theorem q_environment_independent (η ξ : Nat → T) : eval qPoly η = eval qPoly ξ := by
  simp [qPoly, literalPairStateBody, diagonalStep, diagonalStepBody, diagonalZero,
    succPoly, succBody, inputNumeral, iterationPoly, sndPoly, fstPoly, pairPoly,
    abstract, freeZero, drop, pren, psub, eval]

/-- A restricted universe containing only the total PER imposes no constraint;
    it is not the hypothesis of the standardness theorem. -/
def totalPER : SatPER where
  rel _ _ := True
  symm := fun _ => True.intro
  trans := fun _ _ => True.intro
  saturated := fun _ _ _ => True.intro

theorem total_test_is_vacuous (n : T) : ChurchAt totalPER n := by
  intro _ _ _ _ _ _
  trivial

#print axioms exact_characterization
#print axioms zero_is_church
#print axioms successor_numerals_are_church
#print axioms q_environment_independent
#print axioms total_test_is_vacuous
end OpenTermStandardness.ReviewerChecks
