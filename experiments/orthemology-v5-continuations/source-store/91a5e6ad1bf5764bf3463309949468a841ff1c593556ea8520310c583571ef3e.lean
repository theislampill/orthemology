import AuditedBitControlLaw
import RecursiveCanonicalEquivalence

noncomputable section
set_option linter.unusedSectionVars false
attribute [local instance] Classical.propDecidable
open MeasureTheory ProbabilityTheory Filter Finset
open scoped BigOperators ENNReal
namespace Orthemology.Tranche3.FiniteAuditRepair
open Orthemology.Tranche2 Orthemology.Tranche2.PolicyEmbedding
open AuditControlBridge CanonicalMicro

/-- The hidden source/score weight has exactly two declared possibilities. -/
def weight (θ : Bool) : ℝ := if θ then 3/4 else 1/4
/-- The two finite control actions are literal coherent repair reports. -/
def report (a : Bool) : ℝ := if a then 11/16 else 9/16

def kernels (θ : Bool) : Bool → Bool → ℝ := actionBlindKernel (weight θ)

def literalGood (θ : Bool) : Finset Bool :=
  Finset.univ.filter (fun a => LiteralRepairGood (weight θ) (1/4) (report a))

def publicMenu (_ : Finset Bool) : Finset Bool := Finset.univ

lemma weight_nonneg (θ : Bool) : 0 ≤ weight θ := by cases θ <;> norm_num [weight]
lemma weight_le_one (θ : Bool) : weight θ ≤ 1 := by cases θ <;> norm_num [weight]
lemma kernels_pos : ∀ θ a y, 0 < kernels θ a y := by
  intro θ a y
  cases θ <;> cases y <;> norm_num [kernels,actionBlindKernel,coinMass,weight]
lemma kernels_nonneg : ∀ θ a y, 0 ≤ kernels θ a y := fun θ a y => (kernels_pos θ a y).le
lemma kernels_normalized : ∀ θ a, ∑ y, kernels θ a y = 1 := fun θ => actionBlindKernel_normalized (weight θ)

/-- Both target sets are computed from literal squared-loss inequalities; they
are not assumed model labels. Each opposite report fails one true-state score. -/
theorem literalGood_exact (θ : Bool) : literalGood θ = {θ} := by
  ext a
  cases θ <;> cases a <;> norm_num [literalGood,LiteralRepairGood,weight,report,excessZero,excessOne]

/-- The matching finite action has strictly negative loss excess at BOTH truth
vertices, in the original fixed score units. -/
theorem matching_report_losses (θ : Bool) :
    0 ≤ report θ ∧ report θ ≤ 1 ∧
      excessZero (weight θ) (1/4) (report θ) = -(3/256) ∧
      excessOne (weight θ) (1/4) (report θ) = -(3/256) := by
  cases θ <;> norm_num [weight,report,excessZero,excessOne]

/-- The wrong finite reports fail actual loss inequalities by fixed positive
amounts; hidden-model labels are not substituted for the score test. -/
theorem crossed_report_losses :
    excessZero (weight false) (1/4) (report true) = 37/256 ∧
      excessOne (weight true) (1/4) (report false) = 21/256 := by
  norm_num [weight,report,excessZero,excessOne]

/-- No single real coherent report weakly repairs both declared standards.
The later adaptive success therefore uses information in a load-bearing way. -/
theorem no_static_common_literal_repair :
    ¬ ∃ q : ℝ, LiteralRepairGood (weight false) (1/4) q ∧
      LiteralRepairGood (weight true) (1/4) q := by
  rintro ⟨q,h0,h1⟩
  have hh := robustValue_le_max (1/4) (3/4) (1/4) q (by norm_num) (by norm_num)
    (by norm_num) (by norm_num) (by norm_num) h0.1 h0.2.1
  have hm : max (excessZero (1/4) (1/4) q) (excessOne (3/4) (1/4) q) ≤ 0 :=
    max_le h0.2.2.1 h1.2.2.2
  have hv : robustValue (1/4) (3/4) (1/4) = 177/4096 := by
    norm_num [robustValue,robustReport,excessZero]
  rw [hv] at hh
  linarith

lemma all_reports_coherent (a : Bool) : 0 ≤ report a ∧ report a ≤ 1 := by
  cases a <;> norm_num [report]

lemma kernels_identify (θ η a : Bool) (h : kernels θ a = kernels η a) : θ = η := by
  have hh := congrFun h true
  cases θ <;> cases η <;> norm_num [kernels,actionBlindKernel,coinMass,weight] at hh ⊢

lemma support_stays (B : Finset Bool) (a y : Bool) : supportUpdate kernels B a y = B := by
  ext θ
  simp only [mem_supportUpdate]
  exact ⟨fun h => h.1,fun h => ⟨h,kernels_pos θ a y⟩⟩

/-- A concrete recursive certificate: singleton target-action plans identify
every rival while all admissible observations retain the full support. -/
theorem full_family_winning : RecursiveWinning kernels literalGood publicMenu Finset.univ := by
  apply RecursiveWinning.intro Finset.univ (by simp) (fun θ => [θ])
  · intro θ hθ; simp
  · intro θ hθ a ha; exact Finset.mem_univ a
  · intro θ hθ a ha y hy hn
    exact (hn (support_stays Finset.univ a y)).elim
  · intro θ hθ
    right
    constructor
    · simp [literalGood_exact]
    · intro η hη heq
      have he : θ = η := kernels_identify θ η θ (heq θ (by simp))
      simp [← he,literalGood_exact]

def initialPhase : WinningPhase kernels literalGood publicMenu := ⟨Finset.univ,full_family_winning⟩

/-- The one shared causal control policy from the checked finite criterion. -/
def policy (h : History Bool Bool) : Bool :=
  recursiveHistoryPolicy (R := Unit) kernels literalGood publicMenu initialPhase () h

def reports (ω : ℕ → Bool) (n : ℕ) : ℝ := report (auditActions policy ω n)

def budget (θ : Bool) : ℝ := recursiveChainBudget kernels literalGood publicMenu kernels_nonneg θ initialPhase

/-- Exact canonical/action-blind audit-source law binding for this instance. -/
theorem actual_audit_control_law (θ : Bool) :
    (auditSourceLaw (weight θ) (weight_nonneg θ) (weight_le_one θ)).map (auditActions policy) =
      actionLaw (recursiveHistoryPolicy (R := Unit) kernels literalGood publicMenu initialPhase)
        (Measure.dirac ()) (kernels θ) (kernels_nonneg θ) (kernels_normalized θ) false := by
  exact auditActions_law_eq_canonical policy (weight θ) (weight_nonneg θ) (weight_le_one θ)
    (Measure.dirac ()) false

/-- Literal empirical-source output reports are coherent at every opportunity,
including the uninformative initial report before any receipt is observed. -/
theorem reports_always_coherent (ω : ℕ → Bool) (n : ℕ) :
    0 ≤ reports ω n ∧ reports ω n ≤ 1 := all_reports_coherent _

/-- For each of the two hidden source weights, this ONE policy eventually
strictly improves both truth-state squared losses under the actual audit law. -/
theorem reports_eventually_strict (θ : Bool) :
    ∀ᵐ ω ∂auditSourceLaw (weight θ) (weight_nonneg θ) (weight_le_one θ), ∀ᶠ n in atTop,
      (reports ω n)^2 < weight θ*(1/2+(1/4))^2+(1-weight θ)*(1/2)^2 ∧
      (1-reports ω n)^2 < weight θ*(1/2-(1/4))^2+(1-weight θ)*(1/2)^2 := by
  have hg := recursiveHistoryPolicy_actionLaw_eventually_good kernels literalGood publicMenu
    kernels_nonneg kernels_normalized θ initialPhase (Finset.mem_univ θ) (Measure.dirac ()) false
  rw [← actual_audit_control_law θ] at hg
  have ha := ae_of_ae_map (auditActions_measurable policy).aemeasurable hg
  filter_upwards [ha] with ω hω
  filter_upwards [hω] with n hn
  have he : auditActions policy ω n = θ := by simpa only [literalGood_exact,Finset.mem_singleton] using hn
  have hl := matching_report_losses θ
  unfold reports
  rw [he]
  unfold excessZero excessOne at hl
  constructor <;> linarith [hl.2.2.1,hl.2.2.2]

/-- Literal failure is equivalent to a bad finite action, proved from the target
set's score definition rather than silently relabeling controller success. -/
lemma literal_failure_cost (θ a : Bool) :
    (if LiteralRepairGood (weight θ) (1/4) (report a) then (0 : ℝ≥0∞) else 1) =
      badActionCost (literalGood θ) a := by
  simp [badActionCost,literalGood]

/-- Expected TOTAL number of literally incorrect repair reports is finite in
the actual Bernoulli audit experiment and bounded by the verified chain budget. -/
theorem reports_expected_literal_failures (θ : Bool) :
    (∫⁻ ω, ∑' n, (if LiteralRepairGood (weight θ) (1/4) (reports ω n)
      then (0 : ℝ≥0∞) else 1)
      ∂auditSourceLaw (weight θ) (weight_nonneg θ) (weight_le_one θ)) ≤ ENNReal.ofReal (budget θ) := by
  have hb := recursiveHistoryPolicy_actionLaw_total_bad_budget kernels literalGood publicMenu
    kernels_nonneg kernels_normalized θ initialPhase (Finset.mem_univ θ) (Measure.dirac ()) false
  rw [← actual_audit_control_law θ,lintegral_map (total_bad_measurable (literalGood θ))
    (auditActions_measurable policy)] at hb
  simpa only [reports,literal_failure_cost,budget] using hb

theorem reports_expected_literal_failures_finite (θ : Bool) :
    (∫⁻ ω, ∑' n, (if LiteralRepairGood (weight θ) (1/4) (reports ω n)
      then (0 : ℝ≥0∞) else 1)
      ∂auditSourceLaw (weight θ) (weight_nonneg θ) (weight_le_one θ)) < ⊤ :=
  lt_of_le_of_lt (reports_expected_literal_failures θ) ENNReal.ofReal_lt_top
end Orthemology.Tranche3.FiniteAuditRepair
