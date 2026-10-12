import MarkovKilledBridge

namespace StochasticTransferReview
open HiddenParity.Stochastic
open Orthemology.Tranche2.PolicyEmbedding

abbrev S := Fin 2
abbrev A := Fin 2

def adaptive (_ : Unit) (h : History A S) : A := if h = [] then 0 else 1

def oracleP (_ : ℕ) (_ : S × A) : S := 0
def oracleQ (_ : ℕ) (e : S × A) : S := if e.2 = 0 then 0 else 1

def actualP : ℕ → History (S × A) S :=
  observedHistory ∅ (pairPolicy 0 adaptive) oracleP () (fun _ _ => 0)
def actualQ : ℕ → History (S × A) S :=
  observedHistory ∅ (pairPolicy 0 adaptive) oracleQ () (fun _ _ => 0)

def retained : Finset (S × A) := {(0,0)}

theorem actual_markov_receipt_difference : actualP 2 ≠ actualQ 2 := by decide

theorem actual_retained_receipt_visible :
    killedHistory retained (0,0) actualP 1 = (true, [((0,0),0)]) := by decide

theorem actual_outside_receipt_erased :
    killedHistory retained (0,0) actualP 2 = (false, []) ∧
    killedHistory retained (0,0) actualQ 2 = (false, []) := by decide

theorem source_tracks_latest_actual_receipt :
    (pairPolicy 0 adaptive () (actualP 2)).1 = 0 ∧
    (pairPolicy 0 adaptive () (actualQ 2)).1 = 1 := by decide

/-- Deliberately wrong boundary: check only the previous prefix, retaining the
current receipt for one extra step. -/
def delayedKill (H : ℕ → History (S × A) S) (n : ℕ) : Bool × History (S × A) S :=
  if AlivePrefix retained (0,0) H (n-1) then (true,H n) else (false,[])

theorem delayed_kill_leaks_actual_outside_receipt :
    delayedKill actualP 2 ≠ delayedKill actualQ 2 := by decide

/-- Initial killing still keeps the empty history at time zero and suppresses
the first receipt at time one. -/
theorem empty_retained_kills_first_receipt :
    killedHistory (∅ : Finset (S × A)) (0,0) actualP 0 = (true,[]) ∧
    killedHistory (∅ : Finset (S × A)) (0,0) actualP 1 = (false,[]) := by decide

/-- A rejected strengthening: ordinary retained-pair killing cannot reveal the
full receipt at the first outside step. -/
theorem original_kill_is_not_delayed :
    killedHistory retained (0,0) actualQ 2 ≠ delayedKill actualQ 2 := by decide

#print axioms actual_markov_receipt_difference
#print axioms actual_retained_receipt_visible
#print axioms actual_outside_receipt_erased
#print axioms source_tracks_latest_actual_receipt
#print axioms delayed_kill_leaks_actual_outside_receipt
#print axioms empty_retained_kills_first_receipt
#print axioms original_kill_is_not_delayed
end StochasticTransferReview
