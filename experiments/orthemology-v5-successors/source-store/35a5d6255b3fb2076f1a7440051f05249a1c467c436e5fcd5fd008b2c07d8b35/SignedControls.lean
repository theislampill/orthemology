import SmallFixtures
open OrthemicCertificate OrthemicCertificate.Signed OrthemicCertificate.Signed.Fixtures
#guard evenInput.inputCheck
#guard oddInput.inputCheck
#guard resultTag (solve evenInput {0} 0) = 2
#guard resultTag (solve oddInput {0} 0) = 3
#guard resultTag (solve oddInput ∅ 0) = 1
#guard resultTag (solve ({oddInput with rows := #[]} : Input 1 1 1) {0} 0) = 0
private def negativeOdd := negativeCandidate oddInput {0} 0
#guard negativeCheck oddInput {0} 0 negativeOdd
#guard negativeOdd.entries.length = 49
#guard !(negativeCheck evenInput {0} 0 negativeOdd)
#guard !(negativeCheck oddInput ∅ 0 negativeOdd)
private def sourceChanged : Input 1 1 1 := {oddInput with interpretation := {oddInput.interpretation with occurrenceSource := "changed"}}
#guard sourceChanged.inputCheck
#guard !(negativeCheck sourceChanged {0} 0 negativeOdd)
#guard !(negativeCheck oddInput {0} 0 {negativeOdd with entries := negativeOdd.entries.drop 1})
#guard !(negativeCheck oddInput {0} 0 {negativeOdd with entries := negativeOdd.entries ++ [(49,.leaf)]})
#guard !(negativeCheck oddInput {0} 0 {negativeOdd with entries := negativeOdd.entries.map (fun (_,r) => (0,r))})
#guard !(negativeCheck oddInput {0} 0 {negativeOdd with entries := negativeOdd.entries.map (fun (i,r) => (i+1,r))})
#guard !(negativeCheck oddInput {0} 0 {negativeOdd with entries := negativeOdd.entries.reverse})
#eval (resultTag (solve evenInput {0} 0), resultTag (solve oddInput {0} 0),
  negativeOdd.entries.length, negativeCheck oddInput {0} 0 negativeOdd)
-- Binding guards reject before constructing these deliberately enormous domains.
private def twoStateOdd : Input 1 2 1 where
  rows := #[1,0,0,1]
  priorities := #[1,1]
  menus := []
  interpretation := ⟨["m"],["s0","s1"],["a"],"r1","observed","declared","declared"⟩
#guard twoStateOdd.inputCheck
#guard !(negativeCheck twoStateOdd {0} 1 ⟨twoStateOdd,{0},0,[]⟩)
private def twoModelOdd : Input 2 1 1 where
  rows := #[1,1]
  priorities := #[1,1]
  menus := []
  interpretation := ⟨["m0","m1"],["s"],["a"],"r1","observed","declared","declared"⟩
#guard twoModelOdd.inputCheck
#guard !(negativeCheck twoModelOdd {1} 0 ⟨twoModelOdd,{0},0,[]⟩)
-- The general binding theorem excludes every transcript with a mutated start.
example (d : Negative 1 2 1) (hd : d.start = 0) :
    negativeCheck twoStateOdd {0} 1 d = false := by
  cases h : negativeCheck twoStateOdd {0} 1 d with
  | false => rfl
  | true =>
    have hs := (negativeCheck_binding h).2.2
    rw [hd] at hs
    contradiction
