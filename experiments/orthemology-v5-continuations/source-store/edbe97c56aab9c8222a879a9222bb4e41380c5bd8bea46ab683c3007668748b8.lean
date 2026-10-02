import DeterministicContinuation
import StableSupportNecessity

noncomputable section
set_option linter.unusedSectionVars false
open MeasureTheory ProbabilityTheory Filter Set Finset
open scoped BigOperators ENNReal
namespace Orthemology.Tranche3
open Orthemology.Tranche2
open Orthemology.Tranche2.PolicyEmbedding
universe u v
variable {Θ A Y : Type u} {R : Type v}
    [Fintype Θ] [Fintype A] [Fintype Y] [DecidableEq Θ] [DecidableEq A] [Inhabited Y]
    [MeasurableSpace R] [MeasurableSpace A] [MeasurableSingletonClass A]
    [MeasurableSpace Y] [MeasurableSingletonClass Y]

lemma rowHistory_congr_fixed_seed (π π' : R → History A Y → A) (r : R)
    (he : ∀ h, π r h = π' r h) (ω : RowOracle A Y) (n : ℕ) :
    rowHistory π r ω n = rowHistory π' r ω n := by
  induction n with
  | zero => rfl
  | succ n ih => simp only [rowHistory,ih,he]

lemma actionLaw_congr_fixed_seed (π π' : R → History A Y → A)
    (hπ : Measurable (fun z : R × History A Y => π z.1 z.2))
    (hπ' : Measurable (fun z : R × History A Y => π' z.1 z.2))
    (r : R) (he : ∀ h, π r h = π' r h) (P : A → Y → ℝ)
    (hP : ∀ a y, 0 ≤ P a y) (hN : ∀ a, ∑ y, P a y = 1) (d : A) :
    actionLaw π (Measure.dirac r) P hP hN d = actionLaw π' (Measure.dirac r) P hP hN d := by
  rw [actionLaw_dirac_eq_rowLaw π hπ,actionLaw_dirac_eq_rowLaw π' hπ']
  congr 1
  funext ω n
  simp only [rowActions,rowHistory_congr_fixed_seed π π' r he,he]

lemma historySupport_append (P : Θ → A → Y → ℝ) (B : Finset Θ) (f h : History A Y) :
    historySupport P B (f ++ h) = historySupport P (historySupport P B h) f := by
  induction f with
  | nil => rfl
  | cons ay f ih => simp only [List.cons_append,historySupport,ih]

lemma actionCompatible_append (π : R → History A Y → A) (r : R) (f h : History A Y) :
    ActionCompatible π r (f ++ h) ↔
      ActionCompatible π r h ∧ ActionCompatible (continuePolicy π h) r f := by
  induction f with
  | nil => simp only [List.nil_append,ActionCompatible,and_true]
  | cons ay f ih =>
    simp only [List.cons_append,ActionCompatible,continuePolicy,ih,and_assoc]

/-- Deterministic-seed winning in the literal policy-law interface. Safety is
pointwise on feasible consistent histories, independently of target goodness. -/
def FixedSeedWinning (P : Θ → A → Y → ℝ) (good : Θ → Finset A)
    (menu : Finset Θ → Finset A) (hP : ∀ θ a y, 0 ≤ P θ a y)
    (hN : ∀ θ a, ∑ y, P θ a y = 1) (d : A) (B : Finset Θ)
    (π : R → History A Y → A) (r : R) : Prop :=
  Measurable (fun z : R × History A Y => π z.1 z.2) ∧
  (∀ h, ActionCompatible π r h → (historySupport P B h).Nonempty →
    π r h ∈ menu (historySupport P B h)) ∧
  (∀ θ ∈ B, ∀ᵐ x ∂actionLaw π (Measure.dirac r) (P θ) (hP θ) (hN θ) d,
    ∀ᶠ n in atTop, x n ∈ good θ)

/-- All positive successor branches inherit one common winning continuation.
No separate continuation is chosen according to hidden θ. -/
theorem fixedSeedWinning_one_step
    (P : Θ → A → Y → ℝ) (good : Θ → Finset A) (menu : Finset Θ → Finset A)
    (hP : ∀ θ a y, 0 ≤ P θ a y) (hN : ∀ θ a, ∑ y, P θ a y = 1)
    (d : A) (B : Finset Θ) (π : R → History A Y → A) (r : R)
    (hw : FixedSeedWinning P good menu hP hN d B π r) (y : Y) :
    FixedSeedWinning P good menu hP hN d (supportUpdate P B (π r []) y)
      (continuePolicy π [(π r [],y)]) r := by
  refine ⟨continuePolicy_measurable π hw.1 _,?_,?_⟩
  · intro f hf hne
    have hprefix : ActionCompatible π r [(π r [],y)] := ⟨True.intro,rfl⟩
    have hcomp := (actionCompatible_append π r f [(π r [],y)]).mpr ⟨hprefix,hf⟩
    have hsupport : historySupport P B (f ++ [(π r [],y)]) =
        historySupport P (supportUpdate P B (π r []) y) f := by
      rw [historySupport_append]
      rfl
    have hh := hw.2.1 (f ++ [(π r [],y)]) hcomp (by rwa [hsupport])
    simpa only [hsupport,continuePolicy] using hh
  · intro θ hθ
    obtain ⟨hb,hy⟩ := (mem_supportUpdate P B (π r []) y θ).mp hθ
    exact deterministic_one_step_continuation π hw.1 r (P θ) (hP θ) (hN θ) d (good θ)
      (hw.2.2 θ hb) y hy

lemma continuePolicy_continue (π : R → History A Y → A) (h f : History A Y) :
    continuePolicy (continuePolicy π h) f = continuePolicy π (f ++ h) := by
  funext r k
  simp only [continuePolicy,List.append_assoc]

/-- Every feasible public finite history of a deterministic winning policy
has a common winning continuation for every model remaining in its exact support. -/
theorem fixedSeedWinning_at_history
    (P : Θ → A → Y → ℝ) (good : Θ → Finset A) (menu : Finset Θ → Finset A)
    (hP : ∀ θ a y, 0 ≤ P θ a y) (hN : ∀ θ a, ∑ y, P θ a y = 1)
    (d : A) (B : Finset Θ) (π : R → History A Y → A) (r : R)
    (hw : FixedSeedWinning P good menu hP hN d B π r)
    (h : History A Y) (hc : ActionCompatible π r h) (hne : (historySupport P B h).Nonempty) :
    FixedSeedWinning P good menu hP hN d (historySupport P B h) (continuePolicy π h) r := by
  induction h with
  | nil =>
    have he : continuePolicy π [] = π := by funext r h; simp [continuePolicy]
    simpa only [historySupport,he] using hw
  | cons ay h ih =>
    rcases ay with ⟨a,y⟩
    obtain ⟨hc,ha⟩ := hc
    have htail : (historySupport P B h).Nonempty :=
      hne.mono (supportUpdate_subset P (historySupport P B h) a y)
    have hh := fixedSeedWinning_one_step P good menu hP hN d (historySupport P B h)
      (continuePolicy π h) r (ih hc htail) y
    have he : continuePolicy π h r [] = a := by simpa only [continuePolicy,List.nil_append] using ha
    rw [he,continuePolicy_continue] at hh
    simpa only [historySupport,List.singleton_append] using hh
end Orthemology.Tranche3
