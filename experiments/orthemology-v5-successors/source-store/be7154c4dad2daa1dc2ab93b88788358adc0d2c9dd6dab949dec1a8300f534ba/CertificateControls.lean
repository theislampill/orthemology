import CertificateFixtures
open OrthemicCertificate OrthemicCertificate.Fixtures

#guard reveal.inputCheck
#guard bodyCheck reveal [child₀]
#guard bodyCheck reveal [child₁]
#guard check reveal [child₀] {0,1} 1
#guard check reveal [child₁] {0,2} 2
#guard bodyCheck reveal [child₀,child₁]
#guard !(check reveal [child₀,child₁] {0,1,2} 0)
#guard check reveal revealedBody {0,1,2} 0
#guard check reveal [child₀,child₁,parent 2] {0,1,2} 0
#guard !(bodyCheck reveal [child₀,parent])
#guard !(bodyCheck reveal [child₁,parent])
#guard !(bodyCheck reveal [parent])
#guard !(bodyCheck reveal [child₀,child₀,child₁,parent])
#guard !(bodyCheck reveal [child₁,child₀,parent])
#guard !(queryLookup revealedBody ∅ 0)
#guard !(check reveal [] {0,1,2} 0)
-- Every node is validated even when a different child is queried.
#guard !(check reveal [child₀, {child₁ with obligations := []}] {0,1} 1)
#guard !(bodyCheck reveal [child₀,child₁,{parent with obligations := parent.obligations.drop 1}])
#guard !(bodyCheck reveal [child₀,child₁,{parent with obligations := parent.obligations ++ parent.obligations.take 1}])
-- The reveal is a separate exit; it cannot be smuggled into an internal path.
private def wrongRevealPath : Node 3 3 3 :=
  {parent with obligations := [⟨0,0,.exit ⟨0,[(0,1)]⟩ (0,0) 1⟩,
    ⟨0,1,.exit (emptyPath 0) (0,0) 1⟩,⟨0,2,.exit (emptyPath 0) (0,0) 2⟩]}
#guard !(bodyCheck reveal [child₀,child₁,wrongRevealPath])
-- Used permission removal rejects on fresh rechecking.
private def usedPermissionRemoved : Input 3 3 3 :=
  {reveal with menus := [⟨[0,1,2],0,[]⟩,⟨[0,1],1,[1]⟩,⟨[0,2],2,[2]⟩]}
#guard !(check usedPermissionRemoved revealedBody {0,1,2} 0)
-- An unrelated new sparse cell changes identity but may pass fresh checking.
private def freshExtraGrant : Input 3 3 3 :=
  {reveal with menus := reveal.menus ++ [⟨[0],0,[1]⟩]}
#guard freshExtraGrant.inputCheck
#guard check freshExtraGrant revealedBody {0,1,2} 0
#guard !(Input.sameInput reveal freshExtraGrant)
private def declaredSourceChanged : Input 3 3 3 :=
  {reveal with interpretation := {reveal.interpretation with occurrenceSource := "another declared occurrence"}}
#guard check declaredSourceChanged revealedBody {0,1,2} 0
#guard !(Input.sameInput reveal declaredSourceChanged)
-- Distinct choices both pass without any retained selector equality.
#guard check choices [choicesNode 1 0] {0} 0
#guard check choices [choicesNode 2 1] {0} 0
#guard choicesNode 1 0 ≠ choicesNode 2 1
-- Unequal numerical rows with identical supports permit unmatched odd rivals.
#guard latent.inputCheck
#guard check latent [latentNode] {0,1} 0
#guard decide ((latentComponent 0).Valid latent {0,1} 0 Finset.univ 0)
#guard !(decide ((latentComponent 0).Valid latentEqualRows {0,1} 0 Finset.univ 0))
#guard latentEqualRows.inputCheck
#guard !(check latentEqualRows [latentNode] {0,1} 0)
-- Incomplete component closure and false candidate zero-exit are rejected.
#guard !(decide ((singletonComponent (0 : Fin 2) (0 : Fin 2)).Valid latent {0,1} 0 Finset.univ 0))
#guard !(bodyCheck latent [{latentNode with obligations := latentNode.obligations.drop 1}])
#eval (check reveal revealedBody {0,1,2} 0, check latent [latentNode] {0,1} 0,
  check latentEqualRows [latentNode] {0,1} 0)

-- A separately valid wrongly keyed child does not satisfy an exact computed support.
private def wrongSupportInput : Input 3 3 3 :=
  {reveal with menus := reveal.menus ++ [⟨[0],1,[1]⟩]}
private def wrongSupportChild : Node 3 3 3 :=
  ⟨{0},{1},{(1,1)},[⟨1,0,.target (emptyPath 1) (singletonComponent 1 1) 1⟩]⟩
#guard bodyCheck wrongSupportInput [wrongSupportChild]
#guard !(bodyCheck wrongSupportInput [wrongSupportChild,child₁,parent])
#guard !(check reveal [child₀,child₁,parent 0] {0,1,2} 0)
-- Candidate-zero-exit is independent of nonempty/closed internal support here.
private def zeroExitInput : Input 2 2 1 where
  rows := rows 2 2 1 fun m s _ y => if s = 0 then
    (if m = 0 then 1/2 else if y = 0 then 1 else 0)
    else if y = s then 1 else 0
  priorities := priorities 2 2 1 fun _ _ _ => 2
  menus := [⟨[0,1],0,[0]⟩]
  interpretation := interpretation 2 2 1
#guard zeroExitInput.inputCheck
#guard !(decide ((singletonComponent (0 : Fin 2) (0 : Fin 1)).Valid zeroExitInput {0,1} 0 {(0,0)} 0))
#guard decide ((singletonComponent (0 : Fin 2) (0 : Fin 1)).Valid zeroExitInput {0,1} 1 {(0,0)} 0)
-- A same-support state transition must close inside the same record. A second
-- record cannot be used as a cyclic same-support child, and duplicate supports reject.
private def sameSupportOpen : Node 2 2 2 := {latentNode with states := {0}}
#guard !(bodyCheck latent [sameSupportOpen,latentNode])
#guard !(bodyCheck latent [sameSupportOpen])
