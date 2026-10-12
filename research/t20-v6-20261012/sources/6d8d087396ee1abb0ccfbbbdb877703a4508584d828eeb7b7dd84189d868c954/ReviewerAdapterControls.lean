import MarkovSupportAdapter
import AdapterTests
namespace HiddenParity.ReviewerAdapter
open HiddenParity.Controls
set_option maxRecDepth 100000
set_option maxHeartbeats 8000000

/-- The candidate-live premise is necessary for equality of graph support and
candidate-positive support, although the generic target equality allows any B. -/
theorem absent_candidate_no_exit :
    NoExit exitKernel ({1} : Finset Two) 0 (0 : One) := by decide

theorem absent_candidate_internal_has_extra_state :
    internalSuccessors exitKernel ({1} : Finset Two) (0 : One) =
      (Finset.univ : Finset Two) := by decide

theorem absent_candidate_support_equality_false :
    internalSuccessors exitKernel ({1} : Finset Two) (0 : One) ≠
      Finset.univ.filter (fun y => 0 < exitKernel.row 0 0 y) := by decide

def small : ℚ := ⟨1, 1000000, by decide, by decide⟩
theorem small_eq : small = (1 / 1000000 : ℚ) := by
  simpa [small] using (Rat.num_div_den small).symm

def large : ℚ := ⟨999999, 1000000, by decide, by decide⟩
theorem large_eq : large = (999999 / 1000000 : ℚ) := by
  simpa [large] using (Rat.num_div_den large).symm

def perturbedRow (left right : ℚ) (m : Two) (_ : One) (y : Two) : ℚ :=
  if m = 0 then if y = 0 then 1 else 0 else if y = 0 then left else right

def perturbedKernel (left right : ℚ) (hl : 0 ≤ left) (hr : 0 ≤ right)
    (hn : left + right = 1) : RationalKernel Two One Two where
  row := perturbedRow left right
  nonnegative := by
    intro m e y
    fin_cases m <;> fin_cases e <;> fin_cases y <;>
      simp [perturbedRow] <;> assumption
  normalized := by
    intro m e
    fin_cases m <;> fin_cases e <;>
      simp [perturbedRow, Fin.sum_univ_two, hn]

def exactZero := perturbedKernel 1 0 (by norm_num) (by norm_num) (by norm_num)
def exactPositive := perturbedKernel large small (by rw [large_eq]; norm_num)
  (by rw [small_eq]; norm_num) (by rw [large_eq, small_eq]; norm_num)
def evenPriority (_ : Two) (_ : One) : Nat := 2

theorem exact_zero_has_no_exit :
    NoExit exactZero (Finset.univ : Finset Two) 1 (0 : One) := by decide

theorem small_positive_has_exit :
    ¬ NoExit exactPositive (Finset.univ : Finset Two) 1 (0 : One) := by decide

theorem zero_kernel_target_nonempty :
    markovTargetStates exactZero singleSource Finset.univ evenPriority 1 Finset.univ =
      ({0} : Finset Two) := by decide

theorem positive_kernel_target_empty :
    markovTargetStates exactPositive singleSource Finset.univ evenPriority 1 Finset.univ =
      (∅ : Finset Two) := by decide

theorem allowed_input_is_enforced :
    markovTargetStates exactZero singleSource Finset.univ evenPriority 1 ∅ =
      (∅ : Finset Two) := by decide

section General
variable {S A M : Type*} [Fintype S] [DecidableEq S] [DecidableEq A]

omit [DecidableEq S] [DecidableEq A] in
/-- Explicit live-support-update bridge, independent of pruning. -/
theorem exact_support_update_iff
    (P : RationalKernel M A S) (B : Finset M) (e : A) (y : S) :
    y ∈ internalSuccessors P B e ↔ B.filter (fun m => 0 < P.row m e y) = B := by
  rw [mem_internalSuccessors, Finset.filter_eq_self]

omit [DecidableEq S] [DecidableEq A] in
/-- Every positive candidate transition preserves the entire declared live set. -/
theorem noExit_exact_support_update
    (P : RationalKernel M A S) (B : Finset M) (theta : M) (e : A) :
    NoExit P B theta e ↔
      ∀ y, 0 < P.row theta e y → B.filter (fun m => 0 < P.row m e y) = B := by
  simp only [NoExit, exact_support_update_iff]

/-- Independent assembly of the normalized-row maximal-component endpoint,
which is stated in the README and follows from its two main proved adapters. -/
theorem normalized_maximal_components_exact
    (P : RationalKernel M A S) (src : A → S) (B : Finset M)
    (priority : M → A → Nat) (theta : M) (allowed D : Finset A) :
    D ∈ executableOutput src (internalSuccessors P B) B P.row priority theta
      (zeroExitPairs P B theta allowed) ↔
    MarkovQualifying P src B priority theta allowed D ∧
      ∀ E, MarkovQualifying P src B priority theta allowed E → D ⊆ E → E = D := by
  rw [executable_output_iff_maximal_valid]
  constructor
  · rintro ⟨hV,hU,hmax⟩
    refine ⟨(markovQualifying_iff P src B priority theta allowed D).mpr ⟨hU,hV⟩, ?_⟩
    intro E hE hDE
    obtain ⟨hEU,hEV⟩ := (markovQualifying_iff P src B priority theta allowed E).mp hE
    exact hmax E hEV hEU hDE
  · rintro ⟨hD,hmax⟩
    obtain ⟨hDU,hDV⟩ := (markovQualifying_iff P src B priority theta allowed D).mp hD
    refine ⟨hDV,hDU,?_⟩
    intro E hEV hEU hDE
    exact hmax E ((markovQualifying_iff P src B priority theta allowed E).mpr ⟨hEU,hEV⟩) hDE
end General
end HiddenParity.ReviewerAdapter
