import AdaptiveMarkovRecurrentGraph
import SafeSetTailTransfer
import SeededPolicyNecessity
import CheckedTargetOperation

noncomputable section
open MeasureTheory ProbabilityTheory Filter Set
open Orthemology.Tranche2 Orthemology.Tranche2.PolicyEmbedding Orthemology.Tranche2.RecurrentSupport
open Orthemology.Tranche3.RelativeTransfer

namespace HiddenParity.Adaptive
open HiddenParity.Stochastic HiddenParity.Recurrence
universe u v w
variable {State Action : Type u} {R : Type v} {Model : Type w}
variable [Fintype State] [Fintype Action] [DecidableEq State] [DecidableEq Action] [Inhabited State]
variable [MeasurableSpace R] [MeasurableSpace State] [MeasurableSingletonClass State]
variable [MeasurableSpace Action] [MeasurableSingletonClass Action]

/-- Actual state-consistent policy law on the state/action-pair sequence. -/
def markovPairLaw (P : RationalKernel Model (State × Action) State) (θ : Model)
    (s₀ : State) (π : R → History Action State → Action) (ρ : Measure R) (d : State × Action) :
    Measure (ℕ → State × Action) :=
  actionLaw (pairPolicy s₀ π) ρ (realRows P θ) (realRows_nonnegative P θ) (realRows_normalized P θ) d

/-- Stable-support hidden-parity necessity for arbitrary common causal policies.
The end component, row-matching parity condition and probability transfer are
derived. Stability is the explicit concrete positive-support condition on the
lawful always-used pair set; no all-history law-equivalence premise is assumed. -/
theorem stable_support_parity_qualifying_component
    (P : RationalKernel Model (State × Action) State) (B : Finset Model)
    (priority : Model → (State × Action) → ℕ) (θ : Model) (hθ : θ ∈ B)
    (allowed : Finset (State × Action))
    (s₀ : State) (π : R → History Action State → Action)
    (hπ : Measurable (fun z : R × History Action State => π z.1 z.2))
    (ρ : Measure R) [IsProbabilityMeasure ρ] (d : State × Action)
    (hAS : ∀ σ ∈ B, ∀ᵐ x ∂markovPairLaw P σ s₀ π ρ d, ParitySuccess (priority σ) x)
    (hLawful : ∀ᵐ x ∂markovPairLaw P θ s₀ π ρ d, ∀ n, x n ∈ allowed)
    (hStable : ∀ σ ∈ B, ∀ e ∈ allowed, ∀ y, 0 < P.row θ e y → 0 < P.row σ e y) :
    ∃ E, MarkovQualifying P Prod.fst B priority θ allowed E ∧
      0 < markovPairLaw P θ s₀ π ρ d (exactRecurrentEvent id E) := by
  let μ := fun σ => markovPairLaw P σ s₀ π ρ d
  have hPairπ := pairPolicy_measurable s₀ π hπ
  haveI : ∀ σ, IsProbabilityMeasure (μ σ) := fun σ =>
    actionLaw_isProbability (pairPolicy s₀ π) hPairπ ρ (realRows P σ)
      (realRows_nonnegative P σ) (realRows_normalized P σ) d
  have hEventually : ∀ᵐ x ∂μ θ, ∀ᶠ n in atTop, x n ∈ allowed :=
    hLawful.mono (fun _ h => Eventually.of_forall h)
  obtain ⟨E, _, hEA, hPos⟩ := exists_positive_recurrent_support (μ θ) id allowed hEventually
  have hGraphAE := canonical_markov_recurrent_end_component s₀ π hπ ρ (realRows P θ)
    (realRows_nonnegative P θ) (realRows_normalized P θ) d
  obtain ⟨x, hx, hGraph⟩ := Measure.exists_mem_of_measure_ne_zero_of_ae hPos.ne'
    (ae_restrict_of_ae hGraphAE)
  have hRec : recurrentSet x = E := hx
  have hActualEC : IsEndComponent Prod.fst (supportSuccessors (realRows P θ)) E := by
    simpa only [hRec] using hGraph
  have hNo : ∀ e ∈ E, NoExit P B θ e := by
    intro e he y hy
    apply (mem_internalSuccessors P B e y).mpr
    intro σ hσ
    exact hStable σ hσ e (hEA he) y hy
  have hEC : IsEndComponent Prod.fst (internalSuccessors P B) E := by
    apply endComponent_successor_congr Prod.fst (supportSuccessors (realRows P θ))
      (internalSuccessors P B) E hActualEC
    intro e he
    rw [noExit_internal_eq_candidate_support P B θ hθ e (hNo e he)]
    ext y
    simp [supportSuccessors, realRows]
  refine ⟨E, ⟨hEA, hNo, hEC, ?_⟩, hPos⟩
  intro σ hσ hMatch
  obtain ⟨N, hTail⟩ := exists_positive_tail_index (μ θ) id E hPos
  have hSafeEq : (tailEvent id E N ∩ alwaysIn allowed : Set (ℕ → State × Action)) =ᵐ[μ θ]
      (tailEvent id E N : Set (ℕ → State × Action)) := by
    filter_upwards [hLawful] with x hx
    apply propext
    exact ⟨fun h => h.1, fun h => ⟨h, hx⟩⟩
  have hPosSafe : 0 < μ θ (tailEvent id E N ∩ alwaysIn allowed) := by
    rwa [measure_congr hSafeEq]
  have hRelative : ∀ e ∈ allowed, ∀ y, 0 < realRows P θ e y → 0 < realRows P σ e y := by
    intro e he y hy
    change (0 : ℝ) < (P.row θ e y : ℝ) at hy
    have hp : 0 < P.row θ e y := by exact_mod_cast hy
    have hq := hStable σ hσ e he y hp
    change (0 : ℝ) < (P.row σ e y : ℝ)
    exact_mod_cast hq
  have hTransfer := canonical_positive_tail_on_safe_actions allowed E hEA (pairPolicy s₀ π) hPairπ
    ρ (realRows P θ) (realRows P σ) (realRows_nonnegative P θ) (realRows_normalized P θ)
    (realRows_nonnegative P σ) (realRows_normalized P σ) hRelative (realRows_match P hMatch) d N hPosSafe
  have hExactPos : 0 < μ σ (exactRecurrentEvent id E) :=
    hTransfer.trans_le (measure_mono (Set.inter_subset_left.trans Set.inter_subset_left))
  obtain ⟨xσ, hxσ, hParity⟩ := Measure.exists_mem_of_measure_ne_zero_of_ae hExactPos.ne'
    (ae_restrict_of_ae (hAS σ hσ))
  have hRecσ : recurrentSet xσ = E := hxσ
  simpa only [ParitySuccess, hRecσ] using hParity

/-- Consequently the executable target set cannot be empty under a stable-support
common almost-sure parity-winning policy. -/
theorem stable_support_computed_targets_nonempty
    (P : RationalKernel Model (State × Action) State) (B : Finset Model)
    (priority : Model → (State × Action) → ℕ) (θ : Model) (hθ : θ ∈ B)
    (allowed : Finset (State × Action))
    (s₀ : State) (π : R → History Action State → Action)
    (hπ : Measurable (fun z : R × History Action State => π z.1 z.2))
    (ρ : Measure R) [IsProbabilityMeasure ρ] (d : State × Action)
    (hAS : ∀ σ ∈ B, ∀ᵐ x ∂markovPairLaw P σ s₀ π ρ d, ParitySuccess (priority σ) x)
    (hLawful : ∀ᵐ x ∂markovPairLaw P θ s₀ π ρ d, ∀ n, x n ∈ allowed)
    (hStable : ∀ σ ∈ B, ∀ e ∈ allowed, ∀ y, 0 < P.row θ e y → 0 < P.row σ e y) :
    (markovTargetStates P Prod.fst B priority θ allowed).Nonempty := by
  obtain ⟨E, hQ, _⟩ := stable_support_parity_qualifying_component P B priority θ hθ allowed s₀ π hπ ρ d hAS hLawful hStable
  obtain ⟨e, he⟩ := hQ.2.2.1.nonempty
  refine ⟨e.1, (markovTargetStates_exact P Prod.fst B priority θ allowed e.1).mpr ?_⟩
  exact ⟨E, hQ, Finset.mem_image.mpr ⟨e, he, rfl⟩⟩

/-- The stable-support necessity conclusion includes the actual internal path
from the initial observed state to a state returned by the executable target
solver. The path is extracted from a positive-probability actual policy event. -/
theorem stable_support_path_to_computed_target
    (P : RationalKernel Model (State × Action) State) (B : Finset Model)
    (priority : Model → (State × Action) → ℕ) (θ : Model) (hθ : θ ∈ B)
    (allowed : Finset (State × Action))
    (s₀ : State) (π : R → History Action State → Action)
    (hπ : Measurable (fun z : R × History Action State => π z.1 z.2))
    (ρ : Measure R) [IsProbabilityMeasure ρ] (d : State × Action)
    (hAS : ∀ σ ∈ B, ∀ᵐ x ∂markovPairLaw P σ s₀ π ρ d, ParitySuccess (priority σ) x)
    (hLawful : ∀ᵐ x ∂markovPairLaw P θ s₀ π ρ d, ∀ n, x n ∈ allowed)
    (hStable : ∀ σ ∈ B, ∀ e ∈ allowed, ∀ y, 0 < P.row θ e y → 0 < P.row σ e y) :
    ∃ t ∈ markovTargetStates P Prod.fst B priority θ allowed,
      Reach Prod.fst (internalSuccessors P B) allowed s₀ t := by
  obtain ⟨E, hQ, hPos⟩ := stable_support_parity_qualifying_component
    P B priority θ hθ allowed s₀ π hπ ρ d hAS hLawful hStable
  have hPath := canonical_markov_supported_path s₀ π hπ ρ (realRows P θ)
    (realRows_nonnegative P θ) (realRows_normalized P θ) d
  have hBoth := hLawful.and hPath
  obtain ⟨x, hx, hSafe, hInitial, hPositive⟩ := Measure.exists_mem_of_measure_ne_zero_of_ae hPos.ne'
    (ae_restrict_of_ae hBoth)
  have hRec : recurrentSet x = E := hx
  obtain ⟨e, he⟩ := hQ.2.2.1.nonempty
  have heRec : Recurs x e := (mem_recurrentSet x e).mp (hRec.symm ▸ he)
  obtain ⟨n, hn⟩ := heRec.exists
  have hStep : ∀ k, (x (k+1)).1 ∈ internalSuccessors P B (x k) := by
    intro k
    apply (mem_internalSuccessors P B (x k) (x (k+1)).1).mpr
    intro σ hσ
    have hp := hPositive k
    change (0 : ℝ) < (P.row θ (x k) (x (k+1)).1 : ℝ) at hp
    exact hStable σ hσ (x k) (hSafe k) (x (k+1)).1 (by exact_mod_cast hp)
  have hReach := retained_segment_reachable Prod.fst (internalSuccessors P B) x allowed 0 n
    (Nat.zero_le _) (fun k _ => hSafe k) hStep
  refine ⟨e.1, (markovTargetStates_exact P Prod.fst B priority θ allowed e.1).mpr
    ⟨E, hQ, Finset.mem_image.mpr ⟨e, he, rfl⟩⟩, ?_⟩
  simpa only [hInitial, hn] using hReach

/-- A natural no-exit-policy specialization discharges global stability by
filtering to the actual normalized candidate-zero-exit pairs. The target solver
already performs exactly this filter, so its returned target set is unchanged. -/
theorem support_preserving_policy_path_to_target
    (P : RationalKernel Model (State × Action) State) (B : Finset Model)
    (priority : Model → (State × Action) → ℕ) (θ : Model) (hθ : θ ∈ B)
    (allowed : Finset (State × Action))
    (s₀ : State) (π : R → History Action State → Action)
    (hπ : Measurable (fun z : R × History Action State => π z.1 z.2))
    (ρ : Measure R) [IsProbabilityMeasure ρ] (d : State × Action)
    (hAS : ∀ σ ∈ B, ∀ᵐ x ∂markovPairLaw P σ s₀ π ρ d, ParitySuccess (priority σ) x)
    (hNoExitPolicy : ∀ᵐ x ∂markovPairLaw P θ s₀ π ρ d,
      ∀ n, x n ∈ allowed ∧ NoExit P B θ (x n)) :
    ∃ t ∈ markovTargetStates P Prod.fst B priority θ allowed,
      Reach Prod.fst (internalSuccessors P B) allowed s₀ t := by
  let D := zeroExitPairs P B θ allowed
  have hLawful : ∀ᵐ x ∂markovPairLaw P θ s₀ π ρ d, ∀ n, x n ∈ D :=
    hNoExitPolicy.mono (fun x hx n => (mem_zeroExitPairs P B θ allowed (x n)).mpr (hx n))
  have hStable : ∀ σ ∈ B, ∀ e ∈ D, ∀ y, 0 < P.row θ e y → 0 < P.row σ e y := by
    intro σ hσ e he y hy
    have hNo := ((mem_zeroExitPairs P B θ allowed e).mp he).2
    exact (mem_internalSuccessors P B e y).mp (hNo y hy) σ hσ
  obtain ⟨t, ht, hPath⟩ := stable_support_path_to_computed_target P B priority θ hθ D s₀ π hπ ρ d hAS hLawful hStable
  have hId : zeroExitPairs P B θ D = D := by
    ext e
    simp only [D, mem_zeroExitPairs]
    tauto
  have hTarget : markovTargetStates P Prod.fst B priority θ D =
      markovTargetStates P Prod.fst B priority θ allowed := by
    unfold markovTargetStates
    rw [hId]
  refine ⟨t, hTarget ▸ ht, ?_⟩
  exact reach_mono (fun e he => ((mem_zeroExitPairs P B θ allowed e).mp he).1) hPath

end HiddenParity.Adaptive
