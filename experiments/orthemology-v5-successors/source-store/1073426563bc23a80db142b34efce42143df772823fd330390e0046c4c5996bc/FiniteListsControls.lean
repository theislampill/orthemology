import FiniteLists
open OrthemicCertificate.Signed
-- Both list orders occur. Repetitions are not silently normalised away.
example : [0,1] ∈ boundedLists [0,1] 2 := by decide
example : [1,0] ∈ boundedLists [0,1] 2 := by decide
example : [0,0] ∈ boundedLists [0,1] 2 := by decide
example : [0,1,0] ∉ boundedLists [0,1] 2 := by decide
example : ([] : List Nat) ∈ boundedLists [] 0 := by decide
example : ({0,1} : Finset Nat) ∈ subsetList [0,1] := by decide
example : ({1} : Finset Nat) ∈ subsetList [0,1] := by decide
example : ({2} : Finset Nat) ∉ subsetList [0,1] := by decide
#print axioms mem_boundedLists
#print axioms mem_subsetList
