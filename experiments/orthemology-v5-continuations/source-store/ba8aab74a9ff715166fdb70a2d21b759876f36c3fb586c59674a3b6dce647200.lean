import MarkovKilledBridge

namespace HiddenParity.Stochastic.Controls
open Orthemology.Tranche2.PolicyEmbedding

abbrev A := Fin 2
abbrev Y := Fin 2

/-- Both paths agree before choosing outside pair 1; its receipt differs. -/
def pathP : ℕ → History A Y
  | 0 => []
  | 1 => [(0, 0)]
  | _ => [(1, 0), (0, 0)]

def pathQ : ℕ → History A Y
  | 0 => []
  | 1 => [(0, 0)]
  | _ => [(1, 1), (0, 0)]

/-- There is real un-killed observational disagreement. -/
theorem outside_receipt_differs : pathP 2 ≠ pathQ 2 := by decide

/-- The first outside receipt is erased at the correct boundary. -/
theorem killed_outside_receipt_equal :
    killedHistory ({0} : Finset A) 0 pathP 2 = killedHistory ({0} : Finset A) 0 pathQ 2 := by decide

theorem active_prefix_retained :
    killedHistory ({0} : Finset A) 0 pathP 1 = (true, [(0, 0)]) := by decide

theorem killed_flag_visible :
    killedHistory ({0} : Finset A) 0 pathP 2 = (false, []) := by decide

def validReceiptDifference : ℕ → History A Y
  | 0 => []
  | _ => [(0, 1)]

/-- Valid retained-pair receipts are not silently discarded. -/
theorem retained_receipt_not_erased :
    killedHistory ({0} : Finset A) 0 pathP 1 ≠
      killedHistory ({0} : Finset A) 0 validReceiptDifference 1 := by decide

/-- Readout of the complete observed history records the chosen action. -/
theorem action_history_preserved : historyAction (0 : A) pathP 0 = 0 ∧
    historyAction (0 : A) pathP 1 = 1 := by decide

/-- The zero-query killed law cannot be strengthened to un-killed state equality. -/
def queryEverywhere (_ : Y) : Bool := true
def takeReceipt (_ : Y) (y : Y) : Y := y

theorem queried_unstopped_states_differ :
    (Orthemology.Tranche2.FiniteAlphabetQuery.run queryEverywhere takeReceipt
      (fun _ => (0 : Y)) 0 1).1 ≠
    (Orthemology.Tranche2.FiniteAlphabetQuery.run queryEverywhere takeReceipt
      (fun _ => (1 : Y)) 0 1).1 := by decide

theorem queried_stopped_readout_equal :
    killedReadout id (0 : Y)
      (Orthemology.Tranche2.FiniteAlphabetQuery.run queryEverywhere takeReceipt
        (fun _ => (0 : Y)) 0) =
    killedReadout id (0 : Y)
      (Orthemology.Tranche2.FiniteAlphabetQuery.run queryEverywhere takeReceipt
        (fun _ => (1 : Y)) 0) :=
  killedReadout_oracle_independent queryEverywhere takeReceipt _ _ 0 id 0

end HiddenParity.Stochastic.Controls
