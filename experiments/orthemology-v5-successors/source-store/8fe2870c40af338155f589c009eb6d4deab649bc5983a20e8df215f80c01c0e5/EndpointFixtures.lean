import HiddenChangeSemanticEndpoint
open HiddenChange
namespace HiddenChangeEndpointTests

def one (priority : Nat) : Input 1 1 where
  rows := #[1,1]
  priorities := #[priority,priority]
  menus := [⟨[0,1],0,[0]⟩]
  interpretation := ⟨["zero","one"],["s"],["a"],"v1","state","exact","common"⟩

def evenBody : PositiveBody 1 1 where
  K := Finset.univ
  W := Finset.univ
  D1 := Finset.univ
  D := Finset.univ
  known := [⟨0,⟨0,[]⟩,Finset.univ⟩]
  uncertain := [⟨0,0,.component ⟨0,[]⟩ Finset.univ⟩,⟨0,1,.component ⟨0,[]⟩ Finset.univ⟩]

def evenSubmission : SubmittedPositive 1 1 := ⟨one 0,0,evenBody⟩
def oddSubmission : SubmittedNegative 1 1 := ⟨one 1,0,canonicalNegative (one 1)⟩

def mixed : Input 2 1 where
  rows := #[1/2,1/2,1/2,1/2,1/2,1/2,1/2,1/2]
  priorities := #[0,0,0,0]
  menus := [⟨[0,1],0,[0]⟩,⟨[0,1],1,[0]⟩]
  interpretation := ⟨["zero","one"],["q","r"],["a"],"v1","state","exact","common"⟩
def mixedBody : PositiveBody 2 1 where
  K := Finset.univ
  W := Finset.univ
  D1 := Finset.univ
  D := Finset.univ
  known := [⟨0,⟨0,[]⟩,Finset.univ⟩,⟨1,⟨1,[]⟩,Finset.univ⟩]
  uncertain := [⟨0,0,.component ⟨0,[]⟩ Finset.univ⟩,⟨0,1,.component ⟨0,[]⟩ Finset.univ⟩,
    ⟨1,0,.component ⟨1,[]⟩ Finset.univ⟩,⟨1,1,.component ⟨1,[]⟩ Finset.univ⟩]
def changedRows : Input 2 1 := {mixed with rows := #[1/3,2/3,1/3,2/3,1/3,2/3,1/3,2/3]}
def separator : Input 2 1 := {mixed with rows := #[0,1,1,0,1,0,0,1], priorities := #[0,1,0,1]}
def separatorSubmission : SubmittedNegative 2 1 := ⟨separator,0,canonicalNegative separator⟩
end HiddenChangeEndpointTests
