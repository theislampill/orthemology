import HiddenChangeFinite

open HiddenChange HiddenParity
namespace HiddenChangeTests

def one (p0 p1 : Nat) : HiddenChange.Input 1 1 where
  rows := #[1, 1]
  priorities := #[p0, p1]
  menus := [⟨[0,1],0,[0]⟩]
  interpretation := ⟨["zero","one"],["s"],["a"],"v1","state","exact","common"⟩

example : Admissible (one 0 0) := by decide +kernel
example : KnownGood (one 0 0) Finset.univ := by decide +kernel
example : ¬ KnownGood (one 0 1) Finset.univ := by decide +kernel
example : UncertainGood (one 0 0) 0 Finset.univ := by decide +kernel
example : ¬ UncertainGood (one 0 1) 0 Finset.univ := by decide +kernel
example : knownRegion (one 0 0) = Finset.univ := by decide +kernel
example : uncertainRegion (one 0 0) = Finset.univ := by decide +kernel
example : knownRegion (one 1 1) = ∅ := by decide +kernel
example : uncertainRegion (one 1 1) = ∅ := by decide +kernel
example : knownAllowed (one 0 0) ∅ = ∅ := by decide +kernel
example : uncertainAllowed (one 0 0) ∅ Finset.univ = Finset.univ := by decide +kernel
example : ¬ KnownGood (one 0 0) ∅ := by decide +kernel
example : ¬ KnownGood ({one 0 0 with rows := #[0,0]} : HiddenChange.Input 1 1) Finset.univ := by decide +kernel

-- Same supports, different complete rows: odd rival is not a matching rival.
def differentRows : HiddenChange.Input 2 1 where
  rows := #[1/3,2/3,1/3,2/3,2/3,1/3,2/3,1/3]
  priorities := #[0,0,1,1]
  menus := [⟨[0,1],0,[0]⟩,⟨[0,1],1,[0]⟩]
  interpretation := ⟨["zero","one"],["s","t"],["a"],"v1","state","exact","common"⟩
example : Admissible differentRows := by decide +kernel
example : UncertainGood differentRows 0 Finset.univ := by decide +kernel
example : ¬ Match differentRows.row 0 1 Finset.univ := by decide +kernel
example : ¬ KnownGood differentRows {(0,0)} := by decide +kernel

-- Two disconnected self-loops do not form one end component.
def disconnected : HiddenChange.Input 2 1 :=
  { differentRows with rows := #[1,0,0,1,1,0,0,1], priorities := #[0,0,0,0] }
example : ¬ KnownGood disconnected Finset.univ := by decide +kernel

-- A candidate-1-positive/P0-zero branch must land in K.
def reveal : HiddenChange.Input 2 1 :=
  { differentRows with rows := #[1,0,0,1,0,1,0,1], priorities := #[0,0,0,0] }
example : (0,0) ∉ uncertainAllowed reveal ∅ {0} := by decide +kernel
example : (0,0) ∈ uncertainAllowed reveal {1} {0} := by decide +kernel
example : UncertainProgress reveal {1} {(0,0)} 1 0 := by decide +kernel
example : ¬ UncertainGood reveal 1 {(0,0)} := by decide +kernel
end HiddenChangeTests
namespace HiddenChangeTests
-- An outside-source action with all successors inside still cannot enter D1 or D.
def outsideSource : HiddenChange.Input 2 1 :=
  { disconnected with rows := #[1,0,1,0,1,0,1,0] }
example : (1,0) ∉ knownAllowed outsideSource {0} := by decide +kernel
example : (1,0) ∉ uncertainAllowed outsideSource {0} {0} := by decide +kernel
end HiddenChangeTests
