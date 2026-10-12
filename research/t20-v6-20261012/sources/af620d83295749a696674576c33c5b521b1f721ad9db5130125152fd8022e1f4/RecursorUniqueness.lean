import GenericFoldTransport

namespace GenericFoldTransport
open OpenTermStandardness (T SatPER Conv Arrow arrowPER churchPER iter
  zeroTerm succTerm successorNumeral UniformIter)

/-- Church equality to a numeral, not raw equality of their un-applied terms. -/
theorem church_related_numeral {n : T} (nn : churchPER.rel n n) :
    ∃ k, churchPER.rel n (successorNumeral k) := by
  obtain ⟨k, count⟩ := OpenTermStandardness.church_standard n nn
  refine ⟨k, ?_⟩
  intro R f g fg a b ab
  exact R.saturated (count f a).symm
    (OpenTermStandardness.successorNumeral_application k g b).symm
    (OpenTermStandardness.iter_related R fg ab k)

/-- Independent semantic recursor-uniqueness contract. Its premises mention
    only zero, successor, u and the scalar algebra; neither q nor fusion. -/
theorem recursor_unique (A : SatPER) {n f a u : T}
    (nn : churchPER.rel n n) (ff : Arrow A.rel A.rel f f) (aa : A.rel a a)
    (uu : Arrow churchPER.rel A.rel u u)
    (at_zero : A.rel (u ⬝ zeroTerm) a)
    (at_succ : ∀ t, churchPER.rel t t →
      A.rel (u ⬝ (succTerm ⬝ t)) (f ⬝ (u ⬝ t))) :
    A.rel (u ⬝ n) (n ⬝ f ⬝ a) := by
  obtain ⟨k, nk⟩ := church_related_numeral nn
  have un := uu n (successorNumeral k) nk
  have numeral : ∀ j, A.rel (u ⬝ successorNumeral j) (iter f a j) := by
    intro j
    induction j with
    | zero => exact at_zero
    | succ j ih =>
      exact A.trans (at_succ _ (OpenTermStandardness.successorNumeral_church j)) (ff _ _ ih)
  have niter : A.rel (n ⬝ f ⬝ a) (iter f a k) :=
    A.saturated (.refl _) (OpenTermStandardness.successorNumeral_application k f a)
      (nk A f f ff a a aa)
  exact A.trans un (A.trans (numeral k) (A.symm niter))

/-- The uniqueness equation is PER-extensional in its Church input. -/
theorem recursor_unique_related (A : SatPER) {n m f a u : T}
    (nm : churchPER.rel n m) (ff : Arrow A.rel A.rel f f) (aa : A.rel a a)
    (uu : Arrow churchPER.rel A.rel u u)
    (at_zero : A.rel (u ⬝ zeroTerm) a)
    (at_succ : ∀ t, churchPER.rel t t →
      A.rel (u ⬝ (succTerm ⬝ t)) (f ⬝ (u ⬝ t))) :
    A.rel (u ⬝ n) (m ⬝ f ⬝ a) := by
  exact A.trans
    (recursor_unique A (churchPER.trans nm (churchPER.symm nm)) ff aa uu at_zero at_succ)
    (nm A f f ff a a aa)

#print axioms church_related_numeral
#print axioms recursor_unique
#print axioms recursor_unique_related
end GenericFoldTransport
