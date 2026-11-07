import CertificateFrontier

/-! Positive kernel-checked counterexamples to tempting false strengthenings.
These use ordinary kernel reduction (`decide`), not `native_decide`. -/
namespace CertificateFrontier.Controls

def priced : Finset (Pair Bool Nat) := {({false}, 10), ({false, true}, 1)}
def costBlind : Finset (Pair Bool Nat) := {({false}, 10)}

/-- Smaller support alone does not dominate a larger but cheaper certificate. -/
theorem cost_blind_counterexample :
    ({false} : Finset Bool) ⊆ {false, true} ∧
    cost priced {false, true} = ((↑(1 : Nat)) : WithTop Nat) ∧
    cost costBlind {false, true} = ((↑(10 : Nat)) : WithTop Nat) ∧
    cost priced {false, true} ≠ cost costBlind {false, true} := by
  decide

/-- Both cost/support tradeoffs really survive Pareto normalization. -/
theorem priced_frontier : frontier priced = priced := by decide

def jointProof : Finset (Pair Bool Nat) := {({false, true}, 7)}

/-- Equal present licence and present least cost do not preserve future costs. -/
theorem current_cost_counterexample :
    futureCost jointProof {false} ∅ = (⊤ : WithTop Nat) ∧
    futureCost jointProof {true} ∅ = (⊤ : WithTop Nat) ∧
    futureCost jointProof {false} {true} = ((↑(7 : Nat)) : WithTop Nat) ∧
    futureCost jointProof {true} {true} = (⊤ : WithTop Nat) ∧
    inventoryFrontier jointProof {false} ≠ inventoryFrontier jointProof {true} := by
  decide

/-- A deliberately changed cost semantics allows a certificate's own price to
be the same infinity used for infeasibility. This is NOT `cost`: its output
has no fresh top beyond the catalogue price type. -/
def collapsedInfinityCost (A : Finset (Pair Bool (WithTop Nat))) (U : Finset Bool) :
    WithTop Nat := A.inf fun p => if p.1 ⊆ U then p.2 else ⊤

/-- Under that changed semantics, cost equality no longer implies equal
frontiers: an infinite-cost certificate is invisible to all cost observations. -/
theorem infinite_price_counterexample :
    (∀ U, collapsedInfinityCost {(∅, ⊤)} U = collapsedInfinityCost ∅ U) ∧
    frontier ({(∅, ⊤)} : Finset (Pair Bool (WithTop Nat))) ≠ frontier ∅ := by
  constructor
  · intro U
    simp [collapsedInfinityCost]
  · decide

#print axioms cost_blind_counterexample
#print axioms priced_frontier
#print axioms current_cost_counterexample
#print axioms infinite_price_counterexample
end CertificateFrontier.Controls
