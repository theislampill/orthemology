import ControlTests
open HiddenParity HiddenParity.Controls
set_option maxRecDepth 100000
set_option maxHeartbeats 8000000

-- Incorrect mutation: recompute graph components, but always match rows on the original set.
def frozenBad (U : Finset Three) (e : Three) : Prop :=
  ∃ D ∈ executableMECs zeroSource zeroSucc U, e ∈ D ∧ ∃ σ ∈ (Finset.univ : Finset Three),
    Match revealRow 0 σ (Finset.univ : Finset Three) ∧
    IsMinimum (revealPriority σ) D (revealPriority σ e) ∧ revealPriority σ e % 2 = 1
instance (U : Finset Three) (e : Three) : Decidable (frozenBad U e) := by
  unfold frozenBad
  infer_instance
def frozenStep (U : Finset Three) : Finset Three :=
  ((executableMECs zeroSource zeroSucc U).biUnion id).filter (fun e => ¬ frozenBad U e)
def frozenIter : ℕ → Finset Three → Finset Three
  | 0, U => U
  | n + 1, U => frozenIter n (frozenStep U)

example : executableOutput zeroSource zeroSucc Finset.univ revealRow revealPriority 0 Finset.univ =
    ({({2} : Finset Three)} : Finset (Finset Three)) := rival_output
example : executableMECs zeroSource zeroSucc (frozenIter 3 Finset.univ) =
    ({({2} : Finset Three)} : Finset (Finset Three)) := by decide
