import FiniteControls
open HiddenChange HiddenParity
namespace HiddenChangeTests
-- Jointly minimal separator: q=0, r=1, one action; identical priorities.
def separator : HiddenChange.Input 2 1 where
  rows := #[0,1,1,0, 1,0,0,1]
  priorities := #[0,1,0,1]
  menus := [⟨[0,1],0,[0]⟩,⟨[0,1],1,[0]⟩]
  interpretation := ⟨["zero","one"],["q","r"],["a"],"v1","state","exact","common"⟩
example : Admissible separator := by decide +kernel
example : knownRegion separator = {0} := by decide +kernel
example : uncertainRegion separator = ∅ := by decide +kernel

-- A contracting finite operator genuinely uses two strict removals.
def removeMinimum (W : Region 2) : Region 2 :=
  if 0 ∈ W then W.erase 0 else W.erase 1
example : HiddenParity.Necessity.descend removeMinimum 0 Finset.univ = Finset.univ := by decide +kernel
example : HiddenParity.Necessity.descend removeMinimum 1 Finset.univ = {1} := by decide +kernel
example : HiddenParity.Necessity.descend removeMinimum 2 Finset.univ = ∅ := by decide +kernel
example : HiddenParity.Necessity.descend removeMinimum 3 Finset.univ = ∅ := by decide +kernel
end HiddenChangeTests
