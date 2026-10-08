import HiddenChangeBinding
import CertificateControls
import GreatestRegionControls
open HiddenChange HiddenChangeTests
namespace HiddenChangeReview
-- Shape, row stochasticity, raw menu validity and common-menu nonemptiness gates.
example : positiveCheck ({one 0 0 with rows := #[]} : HiddenChange.Input 1 1) 0 evenBody = false := by decide +kernel
example : negativeCheck ({one 1 1 with rows := #[]} : HiddenChange.Input 1 1) 0 (canonicalNegative (one 1 1)) = false := by decide +kernel
example : positiveCheck ({one 0 0 with rows := #[2,1]} : HiddenChange.Input 1 1) 0 evenBody = false := by decide +kernel
example : positiveCheck ({one 0 0 with rows := #[-1,1]} : HiddenChange.Input 1 1) 0 evenBody = false := by decide +kernel
example : positiveCheck ({one 0 0 with priorities := #[]} : HiddenChange.Input 1 1) 0 evenBody = false := by decide +kernel
example : positiveCheck ({one 0 0 with menus := [⟨[0,1],0,[0]⟩,⟨[1,0],0,[0]⟩]} : HiddenChange.Input 1 1) 0 evenBody = false := by decide +kernel
example : positiveCheck ({one 0 0 with menus := [⟨[0,1],0,[0,0]⟩]} : HiddenChange.Input 1 1) 0 evenBody = false := by decide +kernel
example : positiveCheck ({one 0 0 with menus := [⟨[0,1],0,[1]⟩]} : HiddenChange.Input 1 1) 0 evenBody = false := by decide +kernel
example : negativeCheck ({one 1 1 with menus := []} : HiddenChange.Input 1 1) 0 (canonicalNegative (one 1 1)) = false := by decide +kernel
-- The minimum is of used departure pairs and must actually be a lower bound.
example : ¬ EvenMinimum separator 0 {(1,0)} := by decide +kernel
example : EvenMinimum separator 0 Finset.univ := by decide +kernel
example : ¬ EvenMinimum (one 0 0) 0 ∅ := by decide +kernel
-- Component endpoint mismatch, despite a valid zero-length source route.
example : positiveCheck reveal 0
  {revealBody with uncertain := [⟨0,0,.component ⟨0,[]⟩ {(1,0)}⟩,⟨0,1,.reveal ⟨0,[]⟩ 0 1⟩]} = false := by decide +kernel
-- Negative submissions bind both the raw rows and the initial state.
example : boundNegativeCheck separator 0 ⟨separator,0,canonicalNegative separator⟩ = true := by decide +kernel
example : boundNegativeCheck separator 1 ⟨separator,0,canonicalNegative separator⟩ = false := by decide +kernel
example : boundNegativeCheck ({separator with rows := reveal.rows} : HiddenChange.Input 2 1) 0
  ⟨separator,0,canonicalNegative separator⟩ = false := by decide +kernel
-- Binding compares even irrelevant sparse menu entries, not only interpreted common menus.
example : boundPositiveCheck
  ({one 0 0 with menus := (one 0 0).menus ++ [⟨[1],0,[0]⟩]} : HiddenChange.Input 1 1)
  0 ⟨one 0 0,0,evenBody⟩ = false := by decide +kernel
-- Contracting trace: n strict removals plus initial point and terminal repeat.
example : ValidTrace removeMinimum [Finset.univ,{1},∅,∅] := by decide +kernel
example : ¬ ValidTrace removeMinimum [Finset.univ,∅,∅] := by decide +kernel
example : ¬ ValidTrace removeMinimum [Finset.univ,{1},∅] := by decide +kernel
end HiddenChangeReview
