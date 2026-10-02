import GlobalParitySufficiency
import RegionControls

noncomputable section
namespace HiddenParity.Sufficiency.ControllerControls
open HiddenParity.Necessity
set_option maxRecDepth 100000
set_option maxHeartbeats 12000000

abbrev S := Fin 2
abbrev A := Fin 2
abbrev M := Fin 2

def quarter : ℚ := ⟨1,4,by decide,by decide⟩
def threeQuarters : ℚ := ⟨3,4,by decide,by decide⟩

theorem quarter_value : quarter = 1/4 := by
  norm_num [quarter,Rat.mk'_eq_divInt,Rat.divInt_eq_div]
theorem threeQuarters_value : threeQuarters = 3/4 := by
  norm_num [threeQuarters,Rat.mk'_eq_divInt,Rat.divInt_eq_div]

/-- Observed state receipts distinguish two hidden models; the correct parity
choice of action is opposite in the two models. Both states remain possible. -/
def coinKernel : RationalKernel M (S × A) S where
  row := fun m _ y => if m = y then threeQuarters else quarter
  nonnegative := by intro m e y; split <;> norm_num [quarter_value,threeQuarters_value]
  normalized := by intro m e; fin_cases m <;> norm_num [Fin.sum_univ_two,quarter_value,threeQuarters_value]

def menu (_ : Finset M) (_ : S) : Finset A := Finset.univ

def oppositePriority (m : M) (e : S × A) : ℕ := if e.2 = m then 2 else 1

theorem coin_full_region :
    winningRegion coinKernel menu oppositePriority Finset.univ = Finset.univ := by decide

/-- Full computed-region sufficiency now constructs a common actual history
policy for a statistical-learning example with opposite hidden objectives. -/
def coinCommonWinningPolicy :
    WinningPolicy (R := Unit) coinKernel menu oppositePriority (0,0) Finset.univ 0 :=
  computedRegionWinningPolicy coinKernel menu oppositePriority Finset.univ (by decide) 0
    (by rw [coin_full_region]; exact Finset.mem_univ _) (0,0)

/-- Equal observational rows cannot resolve opposing hidden parity requirements. -/
def indistinguishableKernel : RationalKernel M (S × A) S where
  row := fun _ _ y => if y = 0 then threeQuarters else quarter
  nonnegative := by intro m e y; split <;> norm_num [quarter_value,threeQuarters_value]
  normalized := by intro m e; norm_num [Fin.sum_univ_two,quarter_value,threeQuarters_value]

theorem indistinguishable_region_empty :
    winningRegion indistinguishableKernel menu oppositePriority Finset.univ = ∅ := by decide

theorem indistinguishable_no_common_policy {R : Type*} [MeasurableSpace R] :
    ¬ SemanticWinning (R := R) indistinguishableKernel menu oppositePriority (0,0) Finset.univ 0 := by
  apply computed_losing_excludes_common_policy
  rw [indistinguishable_region_empty]
  exact Finset.not_mem_empty _

/-- A revealing observed transition may force a support handoff even when no
initial-support target is available. The actual generated policy handles it. -/
theorem revealing_all_even_region :
    winningRegion HiddenParity.Necessity.Controls.branchKernel
      HiddenParity.Necessity.Controls.allMenu (fun _ _ => 2) Finset.univ = Finset.univ := by decide

def revealingCommonWinningPolicy :
    WinningPolicy (R := Unit) HiddenParity.Necessity.Controls.branchKernel
      HiddenParity.Necessity.Controls.allMenu (fun _ _ => 2) (0,0) Finset.univ 0 :=
  computedRegionWinningPolicy HiddenParity.Necessity.Controls.branchKernel
    HiddenParity.Necessity.Controls.allMenu (fun _ _ => 2) Finset.univ (by decide) 0
    (by rw [revealing_all_even_region]; exact Finset.mem_univ _) (0,0)

/-- The new converse retains the existing all-branch negative certificate. -/
theorem losing_child_still_impossible {R : Type*} [MeasurableSpace R] :
    ¬ SemanticWinning (R := R) HiddenParity.Necessity.Controls.branchKernel
      HiddenParity.Necessity.Controls.allMenu HiddenParity.Necessity.Controls.branchPriority
      (0,0) Finset.univ 0 := HiddenParity.Necessity.Controls.no_common_policy_at_bad_branch

end HiddenParity.Sufficiency.ControllerControls
