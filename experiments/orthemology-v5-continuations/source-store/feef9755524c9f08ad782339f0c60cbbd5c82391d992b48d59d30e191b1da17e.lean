import LawfulRestart

noncomputable section
open MeasureTheory ProbabilityTheory Filter Set
open scoped ENNReal
open Orthemology.Tranche2.PolicyEmbedding

namespace HiddenParity.Necessity
open HiddenParity.Stochastic HiddenParity.ResidualSeed
universe u v w
variable {State Action : Type u} {R : Type v} {Model : Type w}
variable [Fintype State] [Fintype Action] [DecidableEq State] [DecidableEq Action] [Inhabited State]
variable [DecidableEq Model]
variable [MeasurableSpace R] [MeasurableSpace State] [MeasurableSingletonClass State]
variable [MeasurableSpace Action] [MeasurableSingletonClass Action]

/-- The actual finite-history event followed by an illegal selected next action.
The receipt for that next action is not queried or conditioned upon. -/
def IllegalPrefixEvent (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action) (B : Finset Model) (s₀ : State)
    (π : R → History Action State → Action) (h : History (State × Action) State) :
    Set (Input R (State × Action) State) :=
  {z | z ∈ PrefixEvent (pairPolicy s₀ π) h ∧
    (pairPolicy s₀ π z.1 h).2 ∉ menu (liveHistory P B h) (currentState s₀ h)}

/-- The illegal finite-history probability is derived from the actual private
seed/feedback cylinder factorization. -/
theorem illegal_prefix_factorization
    (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action) (B : Finset Model) (s₀ : State)
    (π : R → History Action State → Action) (ρ : Measure R) [IsProbabilityMeasure ρ]
    (θ : Model) (h : History (State × Action) State) :
    CanonicalInput ρ (realRows P θ) (realRows_nonnegative P θ) (realRows_normalized P θ)
      (IllegalPrefixEvent P menu B s₀ π h) =
      ρ {r | (pairPolicy s₀ π r h).2 ∉ menu (liveHistory P B h) (currentState s₀ h) ∧
        ActionCompatible (pairPolicy s₀ π) r h} * RowLikelihood (realRows P θ) h := by
  have hh := seed_history_joint_probability (pairPolicy s₀ π) ρ (realRows P θ)
    (realRows_nonnegative P θ) (realRows_normalized P θ) h
    {r | (pairPolicy s₀ π r h).2 ∉ menu (liveHistory P B h) (currentState s₀ h)}
  simpa only [IllegalPrefixEvent, CompatibleSeeds, Set.mem_setOf_eq, Set.mem_inter_iff, and_comm] using hh

theorem live_model_rowLikelihood_positive
    (P : RationalKernel Model (State × Action) State) (B : Finset Model)
    (h : History (State × Action) State) (θ : Model) (hθ : θ ∈ liveHistory P B h) :
    0 < RowLikelihood (realRows P θ) h := by
  apply rowLikelihood_pos
  intro i
  have hp := liveHistory_survives P B h θ hθ i
  change (0 : ℝ) < (P.row θ h[i].1 h[i].2 : ℝ)
  exact_mod_cast hp

/-- A positive actual prefix cannot have empty live support. -/
theorem positive_prefix_mem_live
    (P : RationalKernel Model (State × Action) State) (B : Finset Model)
    (s₀ : State) (π : R → History Action State → Action) (ρ : Measure R) [IsProbabilityMeasure ρ]
    (θ : Model) (hθ : θ ∈ B) (h : History (State × Action) State)
    (hPos : 0 < CanonicalInput ρ (realRows P θ) (realRows_nonnegative P θ) (realRows_normalized P θ)
      (PrefixEvent (pairPolicy s₀ π) h)) : θ ∈ liveHistory P B h := by
  rw [prefix_probability] at hPos
  have hRow := (ENNReal.mul_pos_iff.mp hPos).2.ne'
  unfold RowLikelihood at hRow
  refine (mem_liveHistory P B h θ).mpr ⟨hθ, ?_⟩
  intro ey hey
  obtain ⟨i, hi⟩ := List.mem_iff_get.mp hey
  have hTerm := (Finset.prod_ne_zero_iff.mp hRow) i (Finset.mem_univ i)
  have hReal := ENNReal.ofReal_pos.mp (pos_iff_ne_zero.mpr hTerm)
  have hRat : 0 < P.row θ h[i].1 h[i].2 := by
    change (0 : ℝ) < (P.row θ h[i].1 h[i].2 : ℝ) at hReal
    exact_mod_cast hReal
  change h[i] = ey at hi
  simpa only [hi] using hRat

/-- Lawfulness is equivalent to zero actual probability of an illegal next
selection after every finite observed history. Null prefixes impose no constraint. -/
theorem lawful_iff_illegal_prefix_probability_zero
    (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action) (B : Finset Model) (s₀ : State)
    (π : R → History Action State → Action) (ρ : Measure R) [IsProbabilityMeasure ρ] :
    Lawful P menu B s₀ π ρ ↔
      ∀ θ ∈ B, ∀ h, CanonicalInput ρ (realRows P θ)
        (realRows_nonnegative P θ) (realRows_normalized P θ)
        (IllegalPrefixEvent P menu B s₀ π h) = 0 := by
  constructor
  · intro hL θ hθ h
    by_cases hp : 0 < CanonicalInput ρ (realRows P θ) (realRows_nonnegative P θ) (realRows_normalized P θ)
        (PrefixEvent (pairPolicy s₀ π) h)
    · have hLive : (liveHistory P B h).Nonempty := ⟨θ, positive_prefix_mem_live P B s₀ π ρ θ hθ h hp⟩
      have hZero := (ae_iff.mp (hL h hLive))
      have hz : ρ {r | (pairPolicy s₀ π r h).2 ∉ menu (liveHistory P B h) (currentState s₀ h) ∧
          ActionCompatible (pairPolicy s₀ π) r h} = 0 := by
        simpa only [_root_.not_imp, and_comm] using hZero
      rw [illegal_prefix_factorization, hz, zero_mul]
    · have hz : CanonicalInput ρ (realRows P θ) (realRows_nonnegative P θ) (realRows_normalized P θ)
          (PrefixEvent (pairPolicy s₀ π) h) = 0 := le_antisymm (le_of_not_gt hp) (zero_le _)
      exact measure_mono_null (fun _ h => h.1) hz
  · intro hZero h hNonempty
    obtain ⟨θ, hθ⟩ := hNonempty
    have hz := hZero θ (liveHistory_subset P B h hθ) h
    rw [illegal_prefix_factorization] at hz
    have hRow := (live_model_rowLikelihood_positive P B h θ hθ).ne'
    have hSeed := (mul_eq_zero.mp hz).resolve_right hRow
    rw [ae_iff]
    simpa only [_root_.not_imp, and_comm] using hSeed

/-- Equivalently it suffices to check histories of positive actual probability;
zero-probability histories and null/off-policy seed traces cannot create extra restrictions. -/
theorem lawful_iff_positive_prefix_legal
    (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action) (B : Finset Model) (s₀ : State)
    (π : R → History Action State → Action) (ρ : Measure R) [IsProbabilityMeasure ρ] :
    Lawful P menu B s₀ π ρ ↔
      ∀ θ ∈ B, ∀ h, 0 < CanonicalInput ρ (realRows P θ)
        (realRows_nonnegative P θ) (realRows_normalized P θ) (PrefixEvent (pairPolicy s₀ π) h) →
        CanonicalInput ρ (realRows P θ) (realRows_nonnegative P θ) (realRows_normalized P θ)
          (IllegalPrefixEvent P menu B s₀ π h) = 0 := by
  rw [lawful_iff_illegal_prefix_probability_zero]
  constructor
  · intro h θ hθ hPrefix _
    exact h θ hθ hPrefix
  · intro h θ hθ hPrefix
    by_cases hp : 0 < CanonicalInput ρ (realRows P θ) (realRows_nonnegative P θ) (realRows_normalized P θ)
        (PrefixEvent (pairPolicy s₀ π) hPrefix)
    · exact h θ hθ hPrefix hp
    · have hz : CanonicalInput ρ (realRows P θ) (realRows_nonnegative P θ) (realRows_normalized P θ)
          (PrefixEvent (pairPolicy s₀ π) hPrefix) = 0 := le_antisymm (le_of_not_gt hp) (zero_le _)
      exact measure_mono_null (fun _ h => h.1) hz

end HiddenParity.Necessity
