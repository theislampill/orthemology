import HiddenChangeTaggedLaw
import ParityTailInvariance

noncomputable section
open MeasureTheory ProbabilityTheory Filter
open Orthemology.Tranche2.PolicyEmbedding
open HiddenParity.Stochastic

namespace HiddenChange
variable {n k : ℕ} [NeZero n] [NeZero k] {R Z : Type*}

/-- Generic countable selection, not itself the one-change law reduction. -/
theorem ae_of_countable_selector {Ω X J : Type*} [MeasurableSpace Ω] [Countable J]
    (μ : Measure Ω) (actual : Ω → X) (fixed : J → Ω → X) (pick : Ω → J)
    (heq : ∀ ω, actual ω = fixed (pick ω) ω) (good : X → Prop)
    (hfixed : ∀ j, ∀ᵐ ω ∂μ, good (fixed j ω)) : ∀ᵐ ω ∂μ, good (actual ω) := by
  filter_upwards [ae_all_iff.mpr hfixed] with ω hω
  rw [heq ω]
  exact hω (pick ω)

/-- A first-one index for a binary sequence, with a genuine never-change case. -/
def firstOne (m : ℕ → Mode) : ChangeIndex := by
  classical
  exact if h : ∃ t, m t = 1 then some (Nat.find h) else none

theorem fixedMode_firstOne (m : ℕ → Mode)
    (hpersist : ∀ t, m t = 1 → m (t+1) = 1) (t : ℕ) :
    fixedMode (firstOne m) t = m t := by
  classical
  have hzero (j : ℕ) (hj : m j ≠ 1) : m j = 0 := by
    have hb := (m j).isLt
    apply Fin.ext
    have hn : (m j).val ≠ 1 := by intro he; apply hj; exact Fin.ext he
    simp only [Fin.val_zero]
    omega
  unfold firstOne
  split_ifs with h
  · simp only [fixedMode]
    split_ifs with ht
    · exact (hzero t (Nat.find_min h ht)).symm
    · have hle : Nat.find h ≤ t := Nat.le_of_not_gt ht
      have hall : ∀ j, Nat.find h ≤ j → m j = 1 := by
        intro j hj
        induction j, hj using Nat.le_induction with
        | base => exact Nat.find_spec h
        | succ j _ ih => exact hpersist j ih
      exact (hall t hle).symm
  · exact (hzero t (fun ht => h ⟨t,ht⟩)).symm

def adaptiveMode [MeasurableSpace Z] (s : State n) (π : Policy R n k)
    (α : Adversary Z n k) (z : (R × Z) × FlatStack (TaggedPair n k) (State n))
    (t : ℕ) : Mode :=
  (adaptivePolicy s π α z.1 (stackHistoryTrajectory (adaptivePolicy s π α) z t)).1

theorem adaptiveMode_persistent [MeasurableSpace Z] (s : State n) (π : Policy R n k)
    (α : Adversary Z n k) (z : (R × Z) × FlatStack (TaggedPair n k) (State n)) :
    ∀ t, adaptiveMode s π α z t = 1 → adaptiveMode s π α z (t+1) = 1 := by
  intro t ht
  apply adaptivePolicy_irreversible
  exact ht

/-- The actual adaptive trajectory equals the fixed-index trajectory selected
by its first governing tag1, on the same complete iid input. The equality is
proved from the evaluator recursion and is not an assumed coupling field. -/
theorem actual_eq_selected_fixed [MeasurableSpace Z] (s : State n) (π : Policy R n k)
    (α : Adversary Z n k) (z : (R × Z) × FlatStack (TaggedPair n k) (State n)) :
    stackHistoryTrajectory (adaptivePolicy s π α) z =
      stackHistoryTrajectory (fixedPolicy (firstOne (adaptiveMode s π α z)) s π)
        (z.1.1,z.2) := by
  funext t
  induction t with
  | zero => rfl
  | succ t ih =>
    have hmode := fixedMode_firstOne (adaptiveMode s π α z)
      (adaptiveMode_persistent s π α z) t
    have hlen : (stackHistoryTrajectory (adaptivePolicy s π α) z t).length = t :=
      observedHistory_length _ _ _ _ _ _
    have hact : adaptivePolicy s π α z.1 (stackHistoryTrajectory (adaptivePolicy s π α) z t) =
        fixedPolicy (firstOne (adaptiveMode s π α z)) s π z.1.1
          (stackHistoryTrajectory (adaptivePolicy s π α) z t) := by
      apply Prod.ext
      · simpa only [fixedPolicy, hlen] using hmode.symm
      · rfl
    change (_, _) :: stackHistoryTrajectory (adaptivePolicy s π α) z t =
      (_, _) :: stackHistoryTrajectory (fixedPolicy (firstOne (adaptiveMode s π α z)) s π)
        (z.1.1,z.2) t
    simp only [stackHistoryTrajectory] at ih hact
    simp only [stackHistoryTrajectory, ← ih, ← hact]

/-- Adjoining and then forgetting an independent adversary seed preserves the
original controller seed and full tape law. -/
theorem forget_adversary_seed [MeasurableSpace R] [MeasurableSpace Z]
    {T : Type*} [MeasurableSpace T] (ρ : Measure R) [IsProbabilityMeasure ρ]
    (η : Measure Z) [IsProbabilityMeasure η] (τ : Measure T) [IsProbabilityMeasure τ] :
    ((ρ.prod η).prod τ).map (fun z => (z.1.1,z.2)) = ρ.prod τ := by
  have he := Measure.map_prod_map (ρ.prod η) τ
    (measurable_fst : Measurable (fun z : R × Z => z.1)) measurable_id
  simpa only [Measure.map_fst_prod, measure_univ, one_smul, Measure.map_id, Prod.map_def, id_eq]
    using he.symm

theorem taggedParity_measurable (I : Input n k) (d : Pair n k) :
    MeasurableSet {H : TaggedTrace n k | TaggedParity I d H} :=
  (paritySuccess_measurable (fun g : TaggedPair n k => I.priority g.1 g.2)).preimage
    (historyAction_measurable (0,d))

theorem adaptive_wins_of_fixed_indices [MeasurableSpace R] [MeasurableSpace Z]
    (I : Input n k) (hI : I.Valid) (s : State n)
    (ρ : Measure R) [IsProbabilityMeasure ρ] (π : Policy R n k)
    (hπ : Measurable (fun z : R × PublicHistory n k => π z.1 z.2))
    (η : Measure Z) [IsProbabilityMeasure η] (α : Adversary Z n k) (d : Pair n k)
    (hfixed : ∀ κ : ChangeIndex, ∀ᵐ H ∂fixedLaw I hI κ s ρ π, TaggedParity I d H) :
    ∀ᵐ H ∂adaptiveLaw I hI s ρ π η α, TaggedParity I d H := by
  let τ := stackMeasure (taggedRows I) (taggedRows_nonnegative I hI) (taggedRows_normalized I hI)
  have hall : ∀ κ : ChangeIndex, ∀ᵐ z ∂((ρ.prod η).prod τ),
      TaggedParity I d (stackHistoryTrajectory (fixedPolicy κ s π) (z.1.1,z.2)) := by
    intro κ
    have hf := hfixed κ
    rw [fixedLaw_eq_stack I hI κ s ρ π hπ] at hf
    have hb := (ae_map_iff (stackHistoryTrajectory_measurable _
      (fixedPolicy_measurable κ s π hπ)).aemeasurable (taggedParity_measurable I d)).mp hf
    have hforget := forget_adversary_seed ρ η τ
    rw [← hforget] at hb
    exact (ae_map_iff (measurable_fst.fst.prodMk measurable_snd).aemeasurable
      ((taggedParity_measurable I d).preimage (stackHistoryTrajectory_measurable _
        (fixedPolicy_measurable κ s π hπ)))).mp hb
  have ha := ae_of_countable_selector ((ρ.prod η).prod τ)
    (stackHistoryTrajectory (adaptivePolicy s π α))
    (fun κ z => stackHistoryTrajectory (fixedPolicy κ s π) (z.1.1,z.2))
    (fun z => firstOne (adaptiveMode s π α z)) (actual_eq_selected_fixed s π α)
    (TaggedParity I d) hall
  rw [adaptiveLaw_eq_stack I hI s ρ π hπ η α]
  exact (ae_map_iff (stackHistoryTrajectory_measurable _
    (adaptivePolicy_measurable s π hπ α)).aemeasurable (taggedParity_measurable I d)).mpr ha

/-- A deterministic legal adversary switching at exactly the requested index. -/
def fixedAdversary [MeasurableSpace Z] (κ : ChangeIndex) : Adversary Z n k where
  choose := fun _ h _ => decide (fixedMode κ h.length = 1)
  measurable_choose := (measurable_of_countable
    (fun h : TaggedHistory n k => decide (fixedMode κ h.length = 1))).comp measurable_snd.fst

theorem fixedMode_persistent (κ : ChangeIndex) (t : ℕ)
    (h : fixedMode κ t = 1) : fixedMode κ (t+1) = 1 := by
  cases κ with
  | none => simp [fixedMode] at h
  | some N =>
    simp only [fixedMode] at h ⊢
    split_ifs at h ⊢ <;> simp_all <;> omega

theorem fixed_adversary_trajectory [MeasurableSpace Z] (κ : ChangeIndex) (s : State n) (π : Policy R n k)
    (z : (R × Z) × FlatStack (TaggedPair n k) (State n)) :
    stackHistoryTrajectory (adaptivePolicy s π (fixedAdversary κ)) z =
      stackHistoryTrajectory (fixedPolicy κ s π) (z.1.1,z.2) := by
  funext t
  induction t with
  | zero => rfl
  | succ t ih =>
    let h := stackHistoryTrajectory (fixedPolicy κ s π) (z.1.1,z.2) t
    have hlen : h.length = t := observedHistory_length _ _ _ _ _ _
    have hp : previousMode h = 1 → fixedMode κ t = 1 := by
      cases t with
      | zero => simp [h, stackHistoryTrajectory, observedHistory, previousMode]
      | succ j =>
        intro hh
        apply fixedMode_persistent κ j
        simpa [h, stackHistoryTrajectory, observedHistory, previousMode, fixedPolicy,
          observedHistory_length] using hh
    have hact : adaptivePolicy s π (fixedAdversary κ) z.1 h = fixedPolicy κ s π z.1.1 h := by
      apply Prod.ext
      · change (if previousMode h = 1 ∨ decide (fixedMode κ h.length = 1) = true then 1 else 0) = _
        simp only [hlen, decide_eq_true_eq, fixedPolicy]
        by_cases hm : fixedMode κ t = 1
        · simp [hm]
        · have hz : fixedMode κ t = 0 := by
            have hlt := (fixedMode κ t).isLt
            apply Fin.ext
            have hne : (fixedMode κ t).val ≠ 1 := by intro he; exact hm (Fin.ext he)
            simp only [Fin.val_zero]
            omega
          have hn : previousMode h ≠ 1 := fun hh => hm (hp hh)
          simp [hm, hz, hn]
      · rfl
    change (_, _) :: stackHistoryTrajectory (adaptivePolicy s π (fixedAdversary κ)) z t =
      (_, _) :: stackHistoryTrajectory (fixedPolicy κ s π) (z.1.1,z.2) t
    simp only [stackHistoryTrajectory] at ih
    change adaptivePolicy s π (fixedAdversary κ) z.1
        (observedHistory Finset.univ (fixedPolicy κ s π) (fun _ _ => default)
          z.1.1 (fun a n => z.2 (a,n)) t) = _ at hact
    simp only [h, stackHistoryTrajectory] at hact
    simp only [stackHistoryTrajectory, ih, hact]

theorem fixed_adversary_law [MeasurableSpace R] [MeasurableSpace Z]
    (I : Input n k) (hI : I.Valid) (κ : ChangeIndex) (s : State n)
    (ρ : Measure R) [IsProbabilityMeasure ρ] (π : Policy R n k)
    (hπ : Measurable (fun z : R × PublicHistory n k => π z.1 z.2)) :
    ∀ (η : Measure Z) [IsProbabilityMeasure η],
    adaptiveLaw I hI s ρ π η (fixedAdversary κ) = fixedLaw I hI κ s ρ π := by
  intro η _
  rw [adaptiveLaw_eq_stack I hI s ρ π hπ, fixedLaw_eq_stack I hI κ s ρ π hπ]
  have he : stackHistoryTrajectory (adaptivePolicy s π (fixedAdversary (Z := Z) κ)) =
      stackHistoryTrajectory (fixedPolicy κ s π) ∘ (fun z => (z.1.1,z.2)) := by
    funext z
    exact fixed_adversary_trajectory κ s π z
  rw [he, ← Measure.map_map (stackHistoryTrajectory_measurable _
    (fixedPolicy_measurable κ s π hπ)) (measurable_fst.fst.prodMk measurable_snd),
    forget_adversary_seed]

universe uZ
/-- The same physical-history policy and seed law must win against every
measurable legal one-change adversary in the selected universe. -/
def WinsAll [MeasurableSpace R] (I : Input n k) (hI : I.Valid) (s : State n)
    (ρ : Measure R) (π : Policy R n k) (d : Pair n k) : Prop :=
  ∀ (Z : Type uZ) [MeasurableSpace Z] (η : Measure Z) [IsProbabilityMeasure η]
    (α : Adversary Z n k), ∀ᵐ H ∂adaptiveLaw I hI s ρ π η α, TaggedParity I d H

theorem winsAll_iff_fixed_indices [MeasurableSpace R]
    (I : Input n k) (hI : I.Valid) (s : State n)
    (ρ : Measure R) [IsProbabilityMeasure ρ] (π : Policy R n k)
    (hπ : Measurable (fun z : R × PublicHistory n k => π z.1 z.2)) (d : Pair n k) :
    WinsAll.{uZ} I hI s ρ π d ↔
      ∀ κ : ChangeIndex, ∀ᵐ H ∂fixedLaw I hI κ s ρ π, TaggedParity I d H := by
  constructor
  · intro hall κ
    have hf := hall (ULift.{uZ} Unit) (Measure.dirac (ULift.up ())) (fixedAdversary κ)
    rwa [fixed_adversary_law I hI κ s ρ π hπ] at hf
  · intro hf Z _ η _ α
    exact adaptive_wins_of_fixed_indices I hI s ρ π hπ η α d hf

end HiddenChange
