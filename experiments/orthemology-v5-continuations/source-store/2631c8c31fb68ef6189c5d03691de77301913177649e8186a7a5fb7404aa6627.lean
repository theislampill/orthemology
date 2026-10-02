import CommonSeedDerandomization
import IIDHeadTail

noncomputable section
set_option linter.unusedSectionVars false
open MeasureTheory ProbabilityTheory Filter Set Finset
open scoped BigOperators ENNReal
namespace Orthemology.Tranche3
open Orthemology.Tranche2
open Orthemology.Tranche2.PolicyEmbedding
open Orthemology.Tranche2.FiniteAlphabetQuery
universe u v
variable {A Y : Type u} {R : Type v} [Fintype A] [Fintype Y] [DecidableEq A] [Inhabited Y]
    [MeasurableSpace R] [MeasurableSpace A] [MeasurableSingletonClass A]
    [MeasurableSpace Y] [MeasurableSingletonClass Y]

def rowHistory (π : R → History A Y → A) (r : R) (ω : RowOracle A Y) : ℕ → History A Y
  | 0 => []
  | n+1 => let h := rowHistory π r ω n
           let a := π r h
           (a,ω n a)::h

def rowActions (π : R → History A Y → A) (r : R) (ω : RowOracle A Y) (n : ℕ) : A :=
  π r (rowHistory π r ω n)

/-- All-query evaluation ignores the unused stacks and queries precisely the
next fresh row at physical time n. -/
lemma observedHistory_empty_eq_rowHistory (π : R → History A Y → A)
    (r : R) (ω : RowOracle A Y) (X : Stack A Y) (n : ℕ) :
    observedHistory ∅ π ω r X n = rowHistory π r ω n := by
  induction n with
  | zero => rfl
  | succ n ih =>
    simp only [observedHistory,ih,rowHistory]
    congr 2
    simp only [feedback,Finset.not_mem_empty,↓reduceIte,outsideCount]
    have hl := observedHistory_length (∅ : Finset A) π ω r X n
    rw [ih] at hl
    simp [hl]

lemma rawActionPath_eq_rowActions (π : R → History A Y → A) (d : A)
    (r : R) (X : FlatStack A Y) (ω : RowOracle A Y) :
    rawActionPath π d (r,(X,ω)) = rowActions π r ω := by
  funext n
  simp only [rawActionPath,historyAction,historyTrajectory,observedHistory_empty_eq_rowHistory,rowHistory,List.headD_cons,Prod.fst,rowActions]

lemma rowActions_measurable (π : R → History A Y → A)
    (hπ : Measurable (fun z : R × History A Y => π z.1 z.2)) (d : A) (r : R) : Measurable (rowActions π r) := by
  have hh : Measurable (fun ω : RowOracle A Y => rawActionPath π d (r,((fun _ => default),ω))) :=
    (rawActionPath_measurable π hπ d).comp (measurable_const.prodMk (measurable_const.prodMk measurable_id))
  simpa only [rawActionPath_eq_rowActions] using hh

/-- Exact deterministic-seed action law on fresh rows alone. -/
theorem actionLaw_dirac_eq_rowLaw (π : R → History A Y → A)
    (hπ : Measurable (fun z : R × History A Y => π z.1 z.2))
    (r : R) (P : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y)
    (hN : ∀ a, ∑ y, P a y = 1) (d : A) :
    actionLaw π (Measure.dirac r) P hP hN d =
      (iidOracle (rowMeasure P hP hN)).map (rowActions π r) := by
  rw [actionLaw_dirac_seed π hπ]
  have he : (fun ω : FlatStack A Y × RowOracle A Y => rawActionPath π d (r,ω)) = rowActions π r ∘ Prod.snd := by
    funext ω
    exact rawActionPath_eq_rowActions π d r ω.1 ω.2
  rw [he,feedbackLaw,← Measure.map_map (rowActions_measurable π hπ d r) measurable_snd,
    Measure.map_snd_prod,measure_univ,one_smul]

def continuePolicy (π : R → History A Y → A) (h : History A Y) (r : R) (future : History A Y) : A :=
  π r (future ++ h)

lemma continuePolicy_measurable (π : R → History A Y → A)
    (hπ : Measurable (fun z : R × History A Y => π z.1 z.2)) (h : History A Y) :
    Measurable (fun z : R × History A Y => continuePolicy π h z.1 z.2) :=
  hπ.comp (measurable_fst.prodMk ((measurable_of_countable (fun k : History A Y => k ++ h)).comp measurable_snd))

/-- One acquired action/observation is hardcoded into the causal continuation. -/
lemma rowHistory_cons_continuation (π : R → History A Y → A) (r : R)
    (row : A → Y) (ω : RowOracle A Y) (n : ℕ) :
    rowHistory π r (consOracle (row,ω)) (n+1) =
      rowHistory (continuePolicy π [(π r [],row (π r []))]) r ω n ++ [(π r [],row (π r []))] := by
  induction n with
  | zero => rfl
  | succ n ih =>
    rw [rowHistory,ih]
    rfl

lemma rowActions_cons_continuation (π : R → History A Y → A) (r : R)
    (row : A → Y) (ω : RowOracle A Y) (n : ℕ) :
    rowActions π r (consOracle (row,ω)) (n+1) =
      rowActions (continuePolicy π [(π r [],row (π r []))]) r ω n := by
  simp only [rowActions,rowHistory_cons_continuation,continuePolicy]

/-- A positive-probability one-observation branch of a deterministic winning
policy has a winning common continuation. Fresh-tail law equality is proved
from the iid head/tail product, rather than assumed as a conditional-law axiom. -/
theorem deterministic_one_step_continuation
    (π : R → History A Y → A)
    (hπ : Measurable (fun z : R × History A Y => π z.1 z.2))
    (r : R) (P : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y)
    (hN : ∀ a, ∑ y, P a y = 1) (d : A) (G : Finset A)
    (hgood : ∀ᵐ x ∂actionLaw π (Measure.dirac r) P hP hN d, ∀ᶠ n in atTop, x n ∈ G)
    (y : Y) (hy : 0 < P (π r []) y) :
    ∀ᵐ x ∂actionLaw (continuePolicy π [(π r [],y)]) (Measure.dirac r) P hP hN d,
      ∀ᶠ n in atTop, x n ∈ G := by
  rw [actionLaw_dirac_eq_rowLaw π hπ r] at hgood
  have hg := ae_of_ae_map (rowActions_measurable π hπ d r).aemeasurable hgood
  have hc : ∀ᵐ z ∂(rowMeasure P hP hN).prod (iidOracle (rowMeasure P hP hN)),
      ∀ᶠ n in atTop, rowActions π r (consOracle z) n ∈ G := by
    have hl : ((rowMeasure P hP hN).prod (iidOracle (rowMeasure P hP hN))).map consOracle =
        iidOracle (rowMeasure P hP hN) := iid_cons_law _
    rw [← hl] at hg
    exact ae_of_ae_map consOracle_measurable.aemeasurable hg
  have hf := Measure.ae_ae_of_ae_prod hc
  have hp : rowMeasure P hP hN {row | row (π r []) = y} ≠ 0 := by
    rw [rowMeasure_coordinate]
    exact (ENNReal.ofReal_pos.mpr hy).ne'
  obtain ⟨row,hrow,hrowgood⟩ := Measure.exists_mem_of_measure_ne_zero_of_ae hp (ae_restrict_of_ae hf)
  rw [actionLaw_dirac_eq_rowLaw _ (continuePolicy_measurable π hπ _) r]
  apply (ae_map_iff (rowActions_measurable _ (continuePolicy_measurable π hπ _) d r).aemeasurable
    (measurableSet_eventually_mem G)).mpr
  filter_upwards [hrowgood] with ω hω
  obtain ⟨N,hN'⟩ := eventually_atTop.mp hω
  apply eventually_atTop.mpr
  refine ⟨N,fun n hn => ?_⟩
  have hh := hN' (n+1) (by omega)
  rw [rowActions_cons_continuation,hrow] at hh
  exact hh
end Orthemology.Tranche3
