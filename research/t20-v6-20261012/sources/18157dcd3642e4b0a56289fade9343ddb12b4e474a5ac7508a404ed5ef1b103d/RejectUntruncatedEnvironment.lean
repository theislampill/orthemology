import RawContextUniformity
open OpenTermStandardness
open RawContextUniformity
-- The invalid direct generic valuation omits the finite zero tail.
example : FullPER.E (rawTel 1) FullPER.Application.emptyEnv T.var T.var := by
  exact ⟨⟨rfl, rfl⟩, .refl _⟩
