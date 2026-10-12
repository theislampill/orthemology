import FoldNaturality
namespace IndependentFoldReview
open P01AC P01D P01AC.ExtensionalRepair
open RigidityPolymorphicTransfer SourceRigidity

-- Exact compatibility with the existing premise-free meta-contract is
-- conditional on an actual closed R proof; none is asserted to exist.
theorem closed_R_yields_original_contract {r : Poly} (hr : HasE [] r Rigidity) :
    SourceFoldContract.SourceNaturality := by
  intro Γ X Y n f g h a square hc hX hY hn hf hg hh ha hsquare
  exact source_naturality_from_rigidity hc hX hY hn hf hg hh ha
    (Structural.has_closed hr (ctx_inclusion hc)) hsquare

-- No hidden restriction to type parameters: literal arbitrary formed X and Y,
-- and an arbitrary HasE square in precisely X::Γ.
theorem exact_contract {Γ X Y r n f g h a square}
    (hc : Ctx Γ) (hX : Form Γ X) (hY : Form Γ Y)
    (hn : Has Γ n EffectiveCompleteness.N) (hf : Has Γ f (arr X X))
    (hg : Has Γ g (arr Y Y)) (hh : Has Γ h (arr X Y)) (ha : Has Γ a X)
    (hr : HasE Γ r Rigidity)
    (hs : HasE (X :: Γ) square (SourceFoldContract.squareType Y f g h)) :
    ∃ e, HasE Γ e (SourceFoldContract.foldType Y n f g h a) :=
  conditional_source_naturality hc hX hY hn hf hg hh ha hr hs

#print axioms closed_R_yields_original_contract
#print axioms exact_contract
#print axioms Structural.has_closed
#print axioms Structural.has_wk
#check SourceFoldContract.SourceNaturality
end IndependentFoldReview
