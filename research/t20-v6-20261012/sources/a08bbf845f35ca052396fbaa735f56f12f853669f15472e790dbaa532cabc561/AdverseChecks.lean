import WitnessControls

namespace GuardedTree.Witness.Reviewer
open Tree Controls Executable.Controls

/-- No rule constructors exist, despite an inhabited judgement type. -/
def emptyGrammar : Grammar Unit Nat (Fin 0) where
  arity := Fin.elim0
  head := Fin.elim0
  premise := fun r => Fin.elim0 r
  localSupport := Fin.elim0
  price := Fin.elim0
  guard := fun r => Fin.elim0 r
instance : ∀ r s, Decidable (emptyGrammar.guard r s) := fun r => Fin.elim0 r

def duplicateRules : RuleList Bool :=
  ⟨[true, false, true, false], by intro r; cases r <;> simp⟩

/-- This guard accepts empty input support but rejects its strict extension. -/
def anti : Grammar (Fin 2) Nat (Fin 3) where
  arity := fun r => if r.val = 2 then 1 else 0
  head := fun r => if r.val = 2 then 1 else 0
  premise := fun _ _ => 0
  localSupport := fun r => if r.val = 1 then {7} else ∅
  price := fun _ => 0
  guard := fun r s => if h : r.val = 2 then 7 ∉ s ⟨0, by simp [h]⟩ else True
instance : ∀ r s, Decidable (anti.guard r s) := by
  intro r s
  unfold anti
  infer_instance

def antiLeaf (r : Fin 3) (hr : r.val ≠ 2) : Tree anti :=
  .node r (fun i => False.elim (by have hi := i.isLt; simp [anti, hr] at hi))

def antiBad : Tree anti := .node 2 (fun _ => antiLeaf 1 (by decide))

def runAdverse : IO Unit := do
  checkWitness emptyGrammar "review empty rules round zero" (finRules 0) 0 () ∅ none
  checkWitness emptyGrammar "review empty rules round three" (finRules 0) 3 () ∅ none
  unless (extract emptyGrammar (finRules 0) () ∅).isNone do
    throw (IO.userError "empty grammar global extractor returned a tree")
  IO.println "PASS review empty rules global none"
  checkWitness seeded "review first seed tie" boolRules 4 () ∅ (some 0) 1
  checkWitness seeded "review first unary tie" reversedBoolRules 4 () ∅ (some 0) 4
  checkWitness seeded "review duplicated enumeration" duplicateRules 3 () ∅ (some 0) 3
  unless (trees seeded duplicateRules 3).length == 14 do
    throw (IO.userError "duplicate multiplicity unexpectedly removed")
  unless (trees seeded boolRules 3).length == 3 do
    throw (IO.userError "baseline enumeration count wrong")
  IO.println "PASS review duplicate multiplicity: 14 versus 3"
  checkWitness anti "review nonmonotone guard accepts empty" (finRules 3) 2 1 ∅ (some 0) 2
  checkWitness anti "review nonmonotone guard rejects extension" (finRules 3) 2 1 {7} none
  checkReject "review nonmonotone invalid actual tree" (accept anti 1 {7} 0 antiBad)
  checkWitness decreasing "review negative bounded five" reversedBoolRules 5 () ∅ (some (-4)) 5
  unless (extract decreasing reversedBoolRules () ∅).map (cost decreasing) == some 0 do
    throw (IO.userError "negative grammar bound changed unexpectedly")
  IO.println "PASS review negative global output is bounded only, not global minimum"

#print axioms validDecidable
#print axioms accept
#print axioms search
#print axioms extractRound
#print axioms extract
#print axioms extract_cost_eq
#print axioms extract_global
#print axioms extract_none_iff

end GuardedTree.Witness.Reviewer

def main : IO Unit := GuardedTree.Witness.Reviewer.runAdverse
