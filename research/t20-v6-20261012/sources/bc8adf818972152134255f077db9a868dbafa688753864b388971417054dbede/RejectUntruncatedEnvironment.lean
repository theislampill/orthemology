import StructuredContextControls
open StructuredContextUniformity
open OpenTermStandardness (T)
-- Neither positive opacity nor generic reflexivity removes the zero-tail obligation.
example : FullPER.E [P01AC.Ty.raw] FullPER.Application.emptyEnv T.var T.var := by
  exact ⟨⟨rfl,rfl⟩,.refl _⟩
