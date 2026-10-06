import SmallFixtures
open OrthemicCertificate OrthemicCertificate.Signed OrthemicCertificate.Signed.Fixtures
#guard (pathDomain 1 1).length = 1
#guard (linkDomain 1 1).length = 1
#guard (componentDomain 1 1).length = 4
#guard (witnessDomain 1 1).length = 5
#guard (obligationDomain 1 1 1).length = 5
#guard (nodeDomain 1 1 1).length = 48
#guard (astDomain 1 1 1).length = 49
#guard decide (Path.Valid {(0,0)} (fun _ => {(0 : Fin 1)}) 0 0 emptyPath)
#guard !(decide (Path.Valid {(0,0)} (fun _ => {(0 : Fin 1)}) 0 0 oneStepPath))
#guard check evenInput singletonBody {0} 0
#guard !(check evenInput [singletonNode,singletonNode] {0} 0)
#guard !(check evenInput [{singletonNode with obligations := singletonNode.obligations ++ singletonNode.obligations}] {0} 0)
#guard !(check evenInput [] {0} 0)
#guard !(check evenInput singletonBody ∅ 0)
example (hc : check evenInput singletonBody {0} 0 = true) :
    singletonBody ∈ astDomain 1 1 1 := accepted_mem_astDomain hc
#eval ((pathDomain 1 1).length, (componentDomain 1 1).length, (nodeDomain 1 1 1).length, (astDomain 1 1 1).length)
-- An extra valid, unqueried node must still be represented, not discarded.
private def twoModels : Input 2 1 1 where
  rows := #[1,1]
  priorities := #[0,0]
  menus := [⟨[0],0,[0]⟩,⟨[1],0,[0]⟩]
  interpretation := ⟨["m0","m1"],["s"],["a"],"r1","observed","declared","declared"⟩
private def singletonAt (θ : Fin 2) : Node 2 1 1 :=
  ⟨{θ},{0},{(0,0)},[⟨0,θ,.target emptyPath singletonComponent 0⟩]⟩
private def unusedBody : Body 2 1 1 := [singletonAt 0,singletonAt 1]
#guard check twoModels unusedBody {0} 0
example (hc : check twoModels unusedBody {0} 0 = true) :
    unusedBody ∈ astDomain 2 1 1 := accepted_mem_astDomain hc
-- Altering the unused node to malformed syntax rejects the entire positive body.
#guard !(check twoModels [singletonAt 0,{singletonAt 1 with obligations := []}] {0} 0)
-- The zero-dimension input gate precedes finite body search.
private def zeroModelInput : Input 0 1 1 where
  rows := #[]
  priorities := #[]
  menus := []
  interpretation := ⟨[],["s"],["a"],"r1","observed","declared","declared"⟩
#guard !(zeroModelInput.inputCheck)
#guard resultTag (solve zeroModelInput ∅ 0) = 0
