import LookaheadBoundary

namespace EffectiveRenewal.Lookahead.Examples
open EffectiveRenewal EffectiveRenewal.Lookahead

def zeroDemand (_ : Word) : Nat := 0
def oneDemand (_ : Word) : Nat := 1
def growingDemand (s : Word) : Nat := s.length + 1

def oneCheck : Word → Bool := lookaheadCheck oneDemand
def onePlan : Nat → Word := lookaheadPlan oneDemand
def growingCheck : Word → Bool := lookaheadCheck growingDemand
def growingPlan : Nat → Word := lookaheadPlan growingDemand

theorem zeroDemand_computable : Computable zeroDemand := Computable.const 0
theorem oneDemand_computable : Computable oneDemand := Computable.const 1
theorem growingDemand_computable : Computable growingDemand :=
  Computable.succ.comp Computable.list_length

-- These interfaces must accept general Computable h, without a Primrec premise.
example (h : Word → Nat) (hc : Computable h) : Computable (lookaheadCheck h) :=
  lookaheadCheck_computable h hc
example (h : Word → Nat) (hc : Computable h) : Computable (lookaheadPlan h) :=
  lookaheadPlan_computable h hc
example (h : Word → Nat) (hc : Computable h) :
    ¬ Pruning.RootedPruned (lookaheadTree h) := lookahead_not_rooted_pruned h hc
example (s : Word) : lookaheadTree zeroDemand s ↔ diagonalTree s := zero_lookahead_iff_base s
example (h : Word → Nat) : lookaheadTree h [] := lookahead_root h
example (h : Word → Nat) (s : Word) (hs : lookaheadTree h s) :
    ∃ w, supplement h s = some w ∧ BaseWitness h s w := supplement_total_of_lookahead h s hs
example : ¬ ∀ s, lookaheadTree oneDemand s →
    ∃ w, BaseWitness oneDemand s w ∧ lookaheadTree oneDemand w := one_step_recursive_witness_failure
example (h : Word → Nat) (n k : Nat) : lookaheadTree h ((lookaheadPlan h n).take k) :=
  lookaheadPlan_prefixes h n k

-- Native executions are concrete instances, not reification of arbitrary
-- Computable proofs and not replacements for the quantified kernel theorems.
def exercise (h : Word → Nat) (maxHorizon : Nat) : IO Unit := do
  for n in List.range (maxHorizon + 1) do
    let s := lookaheadPlan h n
    unless s.length == n && lookaheadCheck h s do
      throw (IO.userError "finite-lookahead horizon check failed")
    for k in List.range (n + 1) do
      let t := s.take k
      match supplement h t with
      | none => throw (IO.userError "missing supplementary witness")
      | some w =>
        unless t.isPrefixOf w && w.length == t.length + h t && treeCheck w do
          throw (IO.userError "invalid base-tree supplementary witness")
  IO.println s!"native finite-lookahead controls passed through horizon {maxHorizon}"

#eval exercise zeroDemand 5
#eval exercise oneDemand 5
#eval exercise growingDemand 4
#eval (List.range 5).map growingPlan
end EffectiveRenewal.Lookahead.Examples
