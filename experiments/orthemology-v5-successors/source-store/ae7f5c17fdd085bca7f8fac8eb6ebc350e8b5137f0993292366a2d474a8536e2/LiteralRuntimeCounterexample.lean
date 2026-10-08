import LiteralSelectorFamily
import ExactRuntimeCounterexample
set_option autoImplicit false

namespace Orthemology.Eighth.SemanticControls.LiteralAssessment
open MeasureTheory
open scoped ENNReal
open HiddenParity HiddenParity.Sufficiency HiddenParity.Necessity HiddenParity.Stage HiddenParity.Stochastic HiddenParity.Adaptive
open Orthemology.Tranche2.PolicyEmbedding
open Orthemology.RuntimeBridge.PhaseUpdate.FullController
open Orthemology.RationalLaw.CanonicalBinding
open Orthemology.RuntimeBridge
open P02A2.Q8Measure (fairCantor)

/-- Executable rational row copy; equality to the accepted kernel is definitional. -/
def literalKernel : RationalKernel Bool (Bool × Bool) Bool where
  row σ e y := if y then (if e.2 = σ then 1/3 else 2/3) else (if e.2 = σ then 2/3 else 1/3)
  nonnegative := by intro σ e y; rcases e with ⟨s,a⟩; cases σ <;> cases s <;> cases a <;> cases y <;> norm_num
  normalized := by intro σ e; rcases e with ⟨s,a⟩; cases σ <;> cases s <;> cases a <;> norm_num [Fintype.sum_bool]

theorem literalKernel_eq : literalKernel = fixtureKernel := rfl

/-- Both configurations are fully specified executable records. No selector
field contains Classical.choose or an unevaluated table packing expression. -/
def literalConfig (orientation : Bool) : Config where
  selectors := literalData orientation
  kernel := literalKernel
  toleranceNumerator := 2
  toleranceDenominator := 1
  rowDenominator := 3
  rowNumerator θ e y := if y then (if e.2 = θ then 1 else 2) else (if e.2 = θ then 2 else 1)
  initialSupport := Finset.univ
  initialState := false
  fallbackModel := false
  fallbackAction := false

noncomputable section

theorem literalConfig_certificate (orientation : Bool) (hO : initialCandidate = orientation) :
    Orthemology.RuntimeBridge.PhaseUpdate.FullController.Certificate (literalConfig orientation) sparseMenu actionPriority := by
  refine ⟨literal_certificate orientation hO,(by change 0 < 1;decide),(by change 0 < 3;decide),?_⟩
  intro θ e y
  rcases e with ⟨s,a⟩
  cases θ <;> cases s <;> cases a <;> cases y <;>
    norm_num [literalConfig,literalKernel]

theorem literalConfig_winning (orientation : Bool) : (literalConfig orientation).initialState ∈
    winningRegion (literalConfig orientation).kernel sparseMenu actionPriority (literalConfig orientation).initialSupport := by
  change false ∈ winningRegion fixtureKernel sparseMenu actionPriority Finset.univ
  rw [sparse_winningRegion _ Finset.univ_nonempty]
  simp

/-- Every normalization on full support agrees, even for arbitrary retained memory. -/
theorem sparse_normalize_full (s : Bool) (m : PhaseMemory Bool Bool) :
    normalizeMemory fixtureKernel sparseMenu actionPriority false Finset.univ s m =
      normalizeMemory fixtureKernel bothMenu actionPriority false Finset.univ s m := by
  rcases m with ⟨k,t⟩
  cases t with
  | some E => rfl
  | none =>
    simp only [normalizeMemory,phaseCandidate]
    rw [if_pos (sparse_target_full _ s),if_pos (by rw [fixture_stageTargets _ Finset.univ_nonempty];simp),
      sparse_choose_full,fixture_chooseTarget _ _ (Finset.mem_univ _) s]

theorem sparse_active_full (m : PhaseMemory Bool Bool) :
    activePairs fixtureKernel sparseMenu actionPriority Finset.univ m =
      activePairs fixtureKernel bothMenu actionPriority Finset.univ m := by
  unfold activePairs
  rw [sparse_stageActions _ Finset.univ_nonempty,sparse_allowed_full,
    fixture_stageActions _ Finset.univ_nonempty]

/-- All finite acquired histories preserve full support; no on-path certificate
is substituted for the required global selector certificate. -/
theorem sparse_phaseMemory_full
    (reject : Bool → ℕ → History (Bool × Bool) Bool → Bool) (h : History Bool Bool) :
    phaseMemory fixtureKernel sparseMenu actionPriority Finset.univ false false reject h =
      phaseMemory fixtureKernel bothMenu actionPriority Finset.univ false false reject h := by
  induction h with
  | nil => rfl
  | cons ay h ih =>
    rcases ay with ⟨a,y⟩
    simp only [phaseMemory,fixture_liveHistory,ih,sparse_normalize_full]

theorem sparse_currentMemory_full
    (reject : Bool → ℕ → History (Bool × Bool) Bool → Bool) (h : History Bool Bool) :
    currentMemory fixtureKernel sparseMenu actionPriority Finset.univ false false reject h =
      currentMemory fixtureKernel bothMenu actionPriority Finset.univ false false reject h := by
  simp only [currentMemory,fixture_liveHistory,sparse_phaseMemory_full,sparse_normalize_full]

/-- The menu change preserves the complete generated decision on every finite
acquired history for any common rejection predicate, including both tolerances. -/
theorem sparse_generated_full
    (reject : Bool → ℕ → History (Bool × Bool) Bool → Bool) (h : History Bool Bool) :
    generatedPhasePolicy fixtureKernel sparseMenu actionPriority Finset.univ false false false reject () h =
      generatedPhasePolicy fixtureKernel bothMenu actionPriority Finset.univ false false false reject () h := by
  simp only [generatedPhasePolicy,fixture_liveHistory,sparse_currentMemory_full,sparse_active_full]

theorem literal_old_policy_constant (orientation : Bool) (h : History Bool Bool) :
    policy (literalConfig orientation) sparseMenu actionPriority h = initialCandidate := by
  change generatedPhasePolicy fixtureKernel sparseMenu actionPriority Finset.univ false false false
    (RationalGate.reject fixtureKernel ((2:ℚ)/1)) () h = initialCandidate
  rw [div_one,sparse_generated_full]
  exact old_generated_constant h

theorem literal_old_source_constant (orientation : Bool) (hO : initialCandidate = orientation)
    (h : History Bool Bool) :
    HistoryRuntime.historyPolicy (sourcePolicy (literalConfig orientation)) () h = orientation := by
  rw [HistoryRuntime.historyPolicy,source_policy_retained_exact (literalConfig orientation) sparseMenu
    actionPriority (literalConfig_certificate orientation hO),literal_old_policy_constant,hO]

theorem literal_computed_policy_exact (orientation : Bool) (h : History Bool Bool) :
    policy (withComputedTolerance (literalConfig orientation)) sparseMenu actionPriority h =
      policy (withComputedTolerance oldConfig) bothMenu actionPriority h := by
  unfold policy
  exact sparse_generated_full _ h

theorem literal_computed_decoder_exact (orientation : Bool) (hO : initialCandidate = orientation) :
    HistoryRuntime.historyPolicy (sourcePolicy (withComputedTolerance (literalConfig orientation))) =
      computedDecoder := by
  funext u h
  cases u
  change sourcePolicy (withComputedTolerance (literalConfig orientation)) (HistoryRuntime.encodeHistory h) =
    sourcePolicy (withComputedTolerance oldConfig) (HistoryRuntime.encodeHistory h)
  rw [source_policy_retained_exact (withComputedTolerance (literalConfig orientation)) sparseMenu
      actionPriority (computed_tolerance_certificate _ _ _ (literalConfig_certificate orientation hO)),
    source_policy_retained_exact (withComputedTolerance oldConfig) bothMenu actionPriority
      (computed_tolerance_certificate _ _ _ oldConfig_certificate)]
  exact literal_computed_policy_exact orientation h

/-- Exact positive-measure failure of each explicit candidate whose orientation
matches the retained cycle, with all off-path certificate cells discharged. -/
theorem literal_runtime_positive_failure (orientation : Bool) (hO : initialCandidate = orientation)
    (d : Bool × Bool) :
    0 < fairCantor {x | ¬ ParitySuccess (actionPriority orientation) (historyAction d
      (decodedHistory (policyProgram (literalConfig orientation))
        (sourcePolicy (withComputedTolerance (literalConfig orientation))) orientation x))} := by
  have hp := positive_opposite_failure orientation blindKernel blindKernel_positive
    (fixture_blind_agree orientation) d
  have hl := mixed_runtime_blind_history_law (policyProgram (literalConfig orientation))
    (sourcePolicy (literalConfig orientation)) (sourcePolicy (withComputedTolerance (literalConfig orientation)))
    (policy_program_implements _) orientation (literal_old_source_constant orientation hO)
  rw [literal_computed_decoder_exact orientation hO] at hl
  change 0 < ((markovHistoryLaw blindKernel orientation false computedDecoder
    (Measure.dirac ())).map (historyAction d)) {x | ¬ ParitySuccess (actionPriority orientation) x} at hp
  have hm : MeasurableSet {x : ℕ → Bool × Bool | ¬ ParitySuccess (actionPriority orientation) x} :=
    (paritySuccess_measurable (actionPriority orientation)).compl
  rw [← hl,Measure.map_map (historyAction_measurable d)
    (decodedHistory_measurable _ _ _),Measure.map_apply
      ((historyAction_measurable d).comp (decodedHistory_measurable _ _ _)) hm] at hp
  exact hp

def CertifiedLiteralFailure (orientation : Bool) : Prop :=
  Orthemology.RuntimeBridge.PhaseUpdate.FullController.Certificate (literalConfig orientation) sparseMenu actionPriority ∧
  (literalConfig orientation).kernel = Controller.Fixture.kernel ∧
  (literalConfig orientation).initialState = false ∧
  (literalConfig orientation).initialState ∈ winningRegion (literalConfig orientation).kernel
    sparseMenu actionPriority (literalConfig orientation).initialSupport ∧
  orientation ∈ (literalConfig orientation).initialSupport ∧
  ∀ d : Bool × Bool, 0 < fairCantor {x | ¬ ParitySuccess (actionPriority orientation) (historyAction d
    (decodedHistory (policyProgram (literalConfig orientation))
      (sourcePolicy (withComputedTolerance (literalConfig orientation))) orientation x))}

theorem certified_literal_failure (orientation : Bool) (hO : initialCandidate = orientation) :
    CertifiedLiteralFailure orientation :=
  ⟨literalConfig_certificate orientation hO,rfl,rfl,literalConfig_winning orientation,
    Finset.mem_univ _,literal_runtime_positive_failure orientation hO⟩

/-- An exhaustive literal list refutes the universal mutant. The disjunction
does not claim that the opaque retained orientation was evaluated. -/
theorem explicit_two_literal_counterexamples : CertifiedLiteralFailure false ∨ CertifiedLiteralFailure true := by
  cases h : initialCandidate
  · exact Or.inl (certified_literal_failure false h)
  · exact Or.inr (certified_literal_failure true h)

end
end Orthemology.Eighth.SemanticControls.LiteralAssessment
