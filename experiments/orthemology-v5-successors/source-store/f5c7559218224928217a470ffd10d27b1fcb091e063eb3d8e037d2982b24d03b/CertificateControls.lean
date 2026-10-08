import HiddenChangeCertificate
import FiniteControls
open HiddenChange
namespace HiddenChangeTests

def zeroRoute : PhysicalPath 1 1 := ⟨0, []⟩
def evenBody : PositiveBody 1 1 where
  K := Finset.univ
  W := Finset.univ
  D1 := Finset.univ
  D := Finset.univ
  known := [⟨0, zeroRoute, Finset.univ⟩]
  uncertain := [⟨0,0,.component zeroRoute Finset.univ⟩,
    ⟨0,1,.component zeroRoute Finset.univ⟩]
example : positiveCheck (one 0 0) 0 evenBody = true := by decide +kernel
example : positiveCheck (one 0 0) 0 {evenBody with known := []} = false := by decide +kernel
example : positiveCheck (one 0 0) 0 {evenBody with known := evenBody.known ++ evenBody.known} = false := by decide +kernel
example : positiveCheck (one 0 0) 0 {evenBody with uncertain := evenBody.uncertain.take 1} = false := by decide +kernel
example : positiveCheck (one 0 0) 0 {evenBody with D := ∅} = false := by decide +kernel
example : positiveCheck (one 0 0) 0 {evenBody with D1 := ∅} = false := by decide +kernel
example : positiveCheck (one 0 1) 0 evenBody = false := by decide +kernel
example : positiveCheck (one 0 0) 0
    {evenBody with known := [⟨0,⟨0,[(0,0)]⟩,Finset.univ⟩]} = false := by decide +kernel
end HiddenChangeTests
namespace HiddenChangeTests
-- K may be empty, and overlap of K,W is allowed by evenBody above.
example : positiveCheck (one 0 0) 0
    {evenBody with K := ∅, D1 := ∅, known := []} = true := by decide +kernel
-- Source outside K, illegal/empty common menu, duplicate uncertain key.
example : positiveCheck (one 0 0) 0 {evenBody with K := ∅} = false := by decide +kernel
example : positiveCheck ({one 0 0 with menus := []} : HiddenChange.Input 1 1) 0 evenBody = false := by decide +kernel
example : positiveCheck (one 0 0) 0
    {evenBody with uncertain := evenBody.uncertain ++ evenBody.uncertain} = false := by decide +kernel

def revealBody : PositiveBody 2 1 where
  K := {1}
  W := {0}
  D1 := {(1,0)}
  D := {(0,0)}
  known := [⟨1,⟨1,[]⟩,{(1,0)}⟩]
  uncertain := [⟨0,0,.component ⟨0,[]⟩ {(0,0)}⟩,⟨0,1,.reveal ⟨0,[]⟩ 0 1⟩]
example : positiveCheck reveal 0 revealBody = true := by decide +kernel
-- Omitted P0 successor, forbidden P1-only exit, key and endpoint mutations.
example : positiveCheck disconnected 0 revealBody = false := by decide +kernel
example : positiveCheck differentRows 0 revealBody = false := by decide +kernel
example : positiveCheck reveal 0 {revealBody with K := ∅, D1 := ∅, known := []} = false := by decide +kernel
example : positiveCheck reveal 0
    {revealBody with uncertain := [⟨0,0,.component ⟨1,[]⟩ {(0,0)}⟩,⟨0,1,.reveal ⟨0,[]⟩ 0 1⟩]} = false := by decide +kernel
example : positiveCheck reveal 0
    {revealBody with uncertain := revealBody.uncertain ++ [⟨1,0,.component ⟨1,[]⟩ {(1,0)}⟩]} = false := by decide +kernel
end HiddenChangeTests
namespace HiddenChangeTests
-- Candidate 0 can never give a positive P0-zero revelation witness.
example : positiveCheck reveal 0
    {revealBody with uncertain := [⟨0,0,.reveal ⟨0,[]⟩ 0 1⟩,⟨0,1,.reveal ⟨0,[]⟩ 0 1⟩]} = false := by decide +kernel
-- Both layers use the declared full-support menu, even when singleton menus are absent.
example : (one 0 0).menu {1} 0 = ∅ := by decide +kernel
example : positiveCheck (one 0 0) 0 evenBody = true := by decide +kernel
end HiddenChangeTests
