import RegionControls
import ReviewerAdaptiveControls

noncomputable section
namespace HiddenParity.IndependentGlobal
open MeasureTheory ProbabilityTheory Filter
open Orthemology.Tranche2.PolicyEmbedding
open HiddenParity.Necessity HiddenParity.Stage HiddenParity.Adaptive HiddenParity.Stochastic
open HiddenParity.IndependentAdaptive
set_option maxRecDepth 100000
set_option maxHeartbeats 8000000
local instance : MeasurableSpace Two := ⊤
local instance : MeasurableSingletonClass Two := by infer_instance
local instance : MeasurableSpace Unit := ⊤
local instance : MeasurableSingletonClass Unit := by infer_instance

def allMenu (_ : Finset Two) (_ : Two) : Finset Two := Finset.univ

theorem revealing_initial_target_empty (m : Two) :
    markovTargetStates revealKernel Prod.fst Finset.univ revealPriority m Finset.univ = ∅ :=
  reveal_computed_target_empty m

theorem revealing_exit (m : Two) :
    ReachableExit revealKernel Finset.univ m Finset.univ (0 : Two) := by
  fin_cases m <;> decide

theorem revealing_lawful :
    Lawful revealKernel allMenu Finset.univ 0 revealPolicy (Measure.dirac ()) := by
  intro h hh
  exact ae_of_all _ (fun r hc => Finset.mem_univ _)

def revealingWinning : WinningPolicy (R := Unit)
    revealKernel allMenu revealPriority (0,0) Finset.univ 0 where
  nonempty := Finset.univ_nonempty
  seedLaw := Measure.dirac ()
  probability := inferInstance
  policy := revealPolicy
  measurable := reveal_policy_measurable
  lawful := revealing_lawful
  parity := by
    intro m hm
    exact (ae_map_iff (historyAction_measurable (0,0)).aemeasurable
      (paritySuccess_measurable (revealPriority m))).mp (reveal_policy_almost_sure_parity m)

theorem revealing_actual_global_necessity :
    (0 : Two) ∈ winningRegion revealKernel allMenu revealPriority Finset.univ :=
  winning_policy_mem_winningRegion _ _ _ _ _ _ revealingWinning

/-- A two-state, one-action revealing fixture isolates the support-fuel boundary. -/
def fuelPriority (_ : Fin 2) (_ : Fin 2 × Fin 1) : Nat := 2

theorem revealing_fuel_one_insufficient :
    computedRegion Controls.branchKernel Controls.allMenu fuelPriority 1 Finset.univ = ({1} : Finset (Fin 2)) := by decide

theorem revealing_fuel_two_sufficient :
    computedRegion Controls.branchKernel Controls.allMenu fuelPriority 2 Finset.univ = Finset.univ := by decide

theorem revealing_excess_fuel (n : Nat) :
    computedRegion Controls.branchKernel Controls.allMenu fuelPriority (n+2) Finset.univ = Finset.univ := by
  rw [computedRegion_fuel_irrelevant Controls.branchKernel Controls.allMenu fuelPriority Finset.univ (n+2) 2
    (by simp) (by simp)]
  exact revealing_fuel_two_sufficient

def constantSeedPolicy (r : Two) (_ : History Two Two) : Two := r

def zeroMenu (_ : Finset Two) (_ : Two) : Finset Two := {0}

/-- A null private seed may violate the hard menu without violating actual lawfulness. -/
theorem null_seed_lawful :
    Lawful revealKernel zeroMenu Finset.univ 0 constantSeedPolicy (Measure.dirac (0 : Two)) := by
  intro h hh
  apply (ae_dirac_iff (Set.toFinite _).measurableSet).mpr
  intro hc
  simp [pairPolicy, constantSeedPolicy, zeroMenu]

theorem null_seed_pointwise_illegal :
    (pairPolicy 0 constantSeedPolicy (1 : Two) []).2 ∉ zeroMenu Finset.univ 0 := by decide

/-- A null seed is still compatible with the empty history. -/
theorem null_seed_empty_history_compatible :
    ActionCompatible (pairPolicy 0 constantSeedPolicy) (1 : Two) [] := True.intro

/-- An illegal initial action is already illegal before its next receipt. -/
theorem illegal_initial_probability_one :
    HiddenParity.ResidualSeed.CanonicalInput (Measure.dirac (1 : Two))
      (realRows revealKernel (0 : Two)) (realRows_nonnegative revealKernel 0)
      (realRows_normalized revealKernel 0)
      (IllegalPrefixEvent revealKernel zeroMenu Finset.univ 0 constantSeedPolicy []) = 1 := by
  rw [illegal_prefix_factorization]
  simp [pairPolicy, constantSeedPolicy, zeroMenu, ActionCompatible,
    HiddenParity.ResidualSeed.RowLikelihood]

end HiddenParity.IndependentGlobal
