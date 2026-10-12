import Witness
import Controls

namespace GuardedTree.Witness.Controls
open Tree Executable.Controls

def unitRules : RuleList Unit := ⟨[()], by intro r; cases r; simp⟩
def boolRules : RuleList Bool := ⟨[false, true], by intro r; cases r <;> simp⟩
def reversedBoolRules : RuleList Bool := ⟨[true, false], by intro r; cases r <;> simp⟩
def finRules (n : ℕ) : RuleList (Fin n) := ⟨List.finRange n, by intro r; simp⟩

def outline {J E R : Type*} (G : Grammar J E R) [Repr R] : Tree G → String
  | .node r child => reprStr r ++ "(" ++
      String.intercalate "," (List.ofFn fun i => outline G (child i)) ++ ")"

def checkWitness {J E R : Type*} [DecidableEq J] [DecidableEq E]
    (G : Grammar J E R) [Fintype J] [Fintype R] [Repr R]
    [∀ r s, Decidable (G.guard r s)]
    (label : String) (rs : RuleList R) (h : ℕ) (q : J) (S : Finset E)
    (expected : Option ℚ) (expectedNodes : ℕ := 0) : IO Unit := do
  let actual := extractRound G rs h q S
  unless actual.map (cost G) == expected do
    throw (IO.userError s!"{label}: incorrect returned-tree cost")
  match actual with
  | none => IO.println s!"PASS {label}: no tree"
  | some t =>
    unless accept G q S (cost G t) t do
      throw (IO.userError s!"{label}: verifier rejected returned tree")
    unless nodes G t == expectedNodes do
      throw (IO.userError s!"{label}: incorrect occurrence count")
    IO.println s!"PASS {label}: cost {cost G t}, nodes {nodes G t}, tree {outline G t}"

def orderedLeaf (r : Fin 5) (hr : r.val < 3) : Tree ordered :=
  .node r (fun i => False.elim (by have hi := i.isLt; simp [ordered, hr] at hi))

def reversedTree : Tree ordered :=
  .node 3 (fun i => if i.val = 0 then orderedLeaf 1 (by decide) else orderedLeaf 0 (by decide))

def repeatedTree : Tree ordered :=
  .node 4 (fun _ => orderedLeaf 0 (by decide))

def wrongChildTree : Tree priceDrop :=
  .node 2 (fun _ => .node 1 Fin.elim0)

def checkReject (label : String) (b : Bool) : IO Unit := do
  if b then throw (IO.userError s!"{label}: corrupted certificate accepted")
  IO.println s!"PASS reject {label}"

def runChecks : IO Unit := do
  checkWitness cycle "unsupported zero cycle" unitRules 4 () ∅ none
  checkWitness seeded "global nullary seed" boolRules (grammarBound seeded) () ∅ (some 0) 1
  checkWitness seeded "seeded zero cycle same-order early tie" reversedBoolRules 1 () ∅ (some 0) 1
  checkWitness seeded "seeded zero cycle tie" reversedBoolRules 4 () ∅ (some 0) 4
  checkWitness blocked "blocked nullary" unitRules 1 () ∅ none
  checkWitness ordered "ordered supports" (finRules 5) 2 1 {0,1} (some 1) 3
  checkWitness ordered "repeated charged occurrences" (finRules 5) 2 2 {0} (some (7/6)) 3
  checkWitness ordered "unavailable shrunken support" (finRules 5) 2 1 ∅ none
  checkWitness ordered "external evidence" (finRules 5) 2 0 {999} none
  checkWitness ordered "cheap empty support retained" (finRules 5) 2 0 ∅ (some 0) 1
  checkWitness ordered "dearer required support retained" (finRules 5) 2 0 {0} (some (1/2)) 1
  checkWitness priceDrop "old expensive proof" (finRules 3) 1 1 ∅ (some 10) 1
  checkWitness priceDrop "global improved proof" (finRules 3) (grammarBound priceDrop) 1 ∅ (some 1) 2
  checkWitness decreasing "negative bounded one" boolRules 1 () ∅ (some 0) 1
  checkWitness decreasing "negative bounded two" boolRules 2 () ∅ (some (-1)) 2
  checkWitness seeded "zero rounds" boolRules 0 () ∅ none
  checkReject "reversed premise order" (accept ordered 1 {0,1} 1 reversedTree)
  checkReject "wrong repeated cost" (accept ordered 2 {0} (2/3) repeatedTree)
  checkReject "wrong exact support" (accept ordered 2 ∅ (7/6) repeatedTree)
  checkReject "wrong root judgement" (accept ordered 1 {0} (7/6) repeatedTree)
  checkReject "wrong child judgement" (accept priceDrop 1 ∅ 11 wrongChildTree)
  let blockedTree : Tree blocked := .node () Fin.elim0
  checkReject "false nullary guard" (accept blocked () ∅ 0 blockedTree)
  unless (tuples ([] : List Nat) 0).length == 1 do
    throw (IO.userError "empty cartesian tuple missing")
  unless (tuples ([] : List Nat) 1).isEmpty do
    throw (IO.userError "unsupported positive-arity tuple")
  IO.println "PASS empty-product boundary"

#eval runChecks
end GuardedTree.Witness.Controls
