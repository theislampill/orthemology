import RecursiveCanonicalEquivalence

noncomputable section
namespace IndependentRecursiveNecessityControls
open Orthemology.Tranche2 Orthemology.Tranche3
open PolicyEmbedding RelativeTransfer
open MeasureTheory Filter Finset
open scoped BigOperators ENNReal

def P (a y : Bool) : ℝ := if a then (if y then 0 else 1) else 1/2
def Q (a y : Bool) : ℝ := if a then (if y then 1 else 0) else 1/2
lemma P_nonneg : ∀ a y, 0≤P a y := by intro a y; cases a <;> cases y <;> norm_num [P]
lemma Q_nonneg : ∀ a y, 0≤Q a y := by intro a y; cases a <;> cases y <;> norm_num [Q]
lemma P_norm : ∀ a, ∑ y, P a y=1 := by intro a; cases a <;> norm_num [P]
lemma Q_norm : ∀ a, ∑ y, Q a y=1 := by intro a; cases a <;> norm_num [Q]

theorem unsafe_coordinate_support_disagrees : 0<P true false ∧ Q true false=0 := by norm_num [P,Q]

theorem full_rows_are_not_dominated : ¬ rowMeasure P P_nonneg P_norm ≪ rowMeasure Q Q_nonneg Q_norm := by
  intro h
  have hz : rowMeasure Q Q_nonneg Q_norm {w | w true=false}=0 := by
    rw [rowMeasure_coordinate]
    norm_num [Q]
  have hp := h hz
  rw [rowMeasure_coordinate] at hp
  norm_num [P] at hp

def constantPolicy (_ : Unit) (_ : History Bool Bool) : Bool := false
lemma constantPolicy_measurable : Measurable (fun z : Unit × History Bool Bool => constantPolicy z.1 z.2) := measurable_const

theorem unused_unsafe_rows_do_not_change_guarded_event :
    actionLaw constantPolicy (Measure.dirac ()) P P_nonneg P_norm false (alwaysIn {false}) =
      actionLaw constantPolicy (Measure.dirac ()) Q Q_nonneg Q_norm false (alwaysIn {false}) := by
  apply canonical_event_eq_on_visited {false} constantPolicy constantPolicy_measurable (Measure.dirac ())
    P Q P_nonneg P_norm Q_nonneg Q_norm
  · intro a ha
    have h : a=false := by simpa using ha
    subst a
    rfl
  · exact measurable_alwaysIn _
  · exact Set.Subset.rfl

theorem one_sided_support_is_not_symmetric :
    (∀ y : Bool, 0<(if y then (0:ℝ) else 1) → 0<(1/2:ℝ)) ∧
    ¬ (∀ y : Bool, 0<(1/2:ℝ) → 0<(if y then (0:ℝ) else 1)) := by
  constructor
  · intro y h; norm_num
  · intro h
    have hx:=h true (by norm_num)
    norm_num at hx

def seedPolicy (r : Bool) (_ : History Bool Bool) : Bool := r
lemma seedPolicy_measurable : Measurable (fun z : Bool × History Bool Bool => seedPolicy z.1 z.2) := measurable_fst

theorem model_coded_seeds_win_without_information (θ : Bool) :
    ∀ᵐ x ∂actionLaw seedPolicy (Measure.dirac θ) P P_nonneg P_norm false,
      ∀ᶠ n in atTop, x n ∈ ({θ} : Finset Bool) := by
  rw [actionLaw_dirac_eq_rowLaw seedPolicy seedPolicy_measurable θ]
  apply (ae_map_iff (rowActions_measurable seedPolicy seedPolicy_measurable false θ).aemeasurable
    (measurableSet_eventually_mem {θ})).mpr
  exact Filter.Eventually.of_forall (fun ω => Filter.Eventually.of_forall (fun n => by simp [rowActions,seedPolicy]))

theorem disjoint_good_sets_have_no_common_support :
    ¬ ∃ U : Finset Bool, U.Nonempty ∧ U ⊆ {false} ∧ U ⊆ {true} := by
  rintro ⟨U,⟨a,ha⟩,hf,ht⟩
  have h0 : a=false := Finset.mem_singleton.mp (hf ha)
  have h1 : a=true := Finset.mem_singleton.mp (ht ha)
  cases h0.symm.trans h1

theorem impossible_observation_cannot_be_conditioned : Q true false=0 := by norm_num [Q]

theorem newest_first_continuation_order (π : Unit → History Bool Bool → Bool)
    (f h : History Bool Bool) :
    continuePolicy (continuePolicy π h) f = continuePolicy π (f++h) :=
  continuePolicy_continue π h f

theorem empty_support_stays_empty (h : History Bool Bool) :
    historySupport (fun (_ : Bool) => P) ∅ h = ∅ := by
  induction h with
  | nil => rfl
  | cons ay h ih => simp [historySupport,ih,supportUpdate]

theorem no_recursive_witness_for_empty_support :
    ¬ RecursiveWinning (fun (_ : Bool) => P) (fun θ => {θ}) (fun _ => Finset.univ) ∅ := by
  intro h
  exact Finset.not_nonempty_empty (recursiveWinning_nonempty _ _ _ h)

theorem licence_contract_is_vacuous_on_empty_initial_support :
    ∀ r h, ActionCompatible seedPolicy r h →
      (historySupport (fun (_ : Bool) => P) ∅ h).Nonempty →
      seedPolicy r h ∈ (∅ : Finset Bool) := by
  intro r h hc hn
  rw [empty_support_stays_empty] at hn
  exact (Finset.not_nonempty_empty hn).elim

end IndependentRecursiveNecessityControls
