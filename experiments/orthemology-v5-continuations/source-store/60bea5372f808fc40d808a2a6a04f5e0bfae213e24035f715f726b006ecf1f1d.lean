import ObservedEmpiricalRows

noncomputable section
open Orthemology.Tranche2.PolicyEmbedding HiddenParity.Adaptive
open HiddenParity.Empirical

namespace HiddenParity.Empirical.Controls

def constantPolicy (_ : Unit) (_ : History Bool Bool) : Bool := false

def allTrueInput : Unit × FlatStack Bool Bool := ((), fun _ => true)

theorem unused_pair_count_zero (n : ℕ) :
    countBefore constantPolicy allTrueInput true n = 0 := by
  induction n with
  | zero => rfl
  | succ n ih => simp [countBefore_succ, stackActionTrajectory, constantPolicy, ih]

/-- Even a perfectly regular unused raw tape does not identify an unvisited row
from acquired history. The recurrence/count-growth premise is indispensable. -/
theorem unused_pair_empirical_zero (n : ℕ) :
    historyFrequency true true (stackHistoryTrajectory constantPolicy allTrueInput n) = 0 := by
  rw [historyFrequency_eq_rawFrequency, unused_pair_count_zero]
  simp [rawFrequency]

theorem positive_raw_frequency_one (a : Bool) (n : ℕ) :
    rawFrequency a true (n+1) allTrueInput = 1 := by
  simp only [rawFrequency, seededStackCoordinate, allTrueInput, symbolIndicator, if_pos rfl,
    Finset.sum_const, Finset.card_range, nsmul_eq_mul, ite_true, mul_one]
  apply div_self
  positivity

theorem unused_observed_differs_from_positive_raw :
    historyFrequency true true (stackHistoryTrajectory constantPolicy allTrueInput 3) ≠
      rawFrequency true true 3 allTrueInput := by
  rw [unused_pair_empirical_zero]
  change (0 : ℝ) ≠ rawFrequency true true (2+1) allTrueInput
  rw [positive_raw_frequency_one]
  exact zero_ne_one

/-- Counts use both the selected action and its receipt, not pooled outcomes. -/
theorem action_specific_history_frequency :
    historyFrequency false true [(false,true),(true,false),(false,false)] = (1/2 : ℝ) ∧
    historyFrequency true true [(false,true),(true,false),(false,false)] = 0 := by
  have h0 : actionCount false [(false,true),(true,false),(false,false)] = 2 := by decide
  have h1 : actionCount true [(false,true),(true,false),(false,false)] = 1 := by decide
  norm_num [historyFrequency, historySymbolMass, symbolIndicator, h0, h1]

/-- The first received symbol is included; an empty prefix is a different count. -/
theorem positive_prefix_differs_from_zero :
    rawFrequency false true 0 allTrueInput = 0 ∧
      rawFrequency false true 1 allTrueInput = 1 := by
  constructor
  · simp [rawFrequency]
  · exact positive_raw_frequency_one false 0

end HiddenParity.Empirical.Controls
