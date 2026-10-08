import HiddenChangeControllerEndpoint
namespace HiddenChangeControllerTests
open HiddenChange

def one : Input 1 2 where
  rows := #[1,1,1,1]
  priorities := #[0,0,0,0]
  menus := [⟨[0,1],0,[0,1]⟩]
  interpretation := ⟨["zero","one"],["s"],["a","b"],"v1","state","exact","common"⟩

def oneBody : PositiveBody 1 2 where
  K := Finset.univ
  W := Finset.univ
  D1 := Finset.univ
  D := Finset.univ
  known := [⟨0,⟨0,[]⟩,Finset.univ⟩]
  uncertain := [⟨0,0,.component ⟨0,[]⟩ Finset.univ⟩,⟨0,1,.component ⟨0,[]⟩ Finset.univ⟩]

def oneAdmissible : Admissible one := by decide +kernel

def reveal : Input 2 1 where
  rows := #[1,0,0,1,0,1,0,1]
  priorities := #[0,0,0,0]
  menus := [⟨[0,1],0,[0]⟩,⟨[0,1],1,[0]⟩]
  interpretation := ⟨["zero","one"],["s","t"],["a"],"v1","state","exact","common"⟩

def revealBody : PositiveBody 2 1 where
  K := {1}
  W := {0}
  D1 := {(1,0)}
  D := {(0,0)}
  known := [⟨1,⟨1,[]⟩,{(1,0)}⟩]
  uncertain := [⟨0,0,.component ⟨0,[]⟩ {(0,0)}⟩,⟨0,1,.reveal ⟨0,[]⟩ 0 1⟩]

def revealAdmissible : Admissible reveal := by decide +kernel

def fullSupport : Input 2 1 :=
  { reveal with rows := #[1/3,2/3,1/3,2/3,2/3,1/3,2/3,1/3] }

end HiddenChangeControllerTests
