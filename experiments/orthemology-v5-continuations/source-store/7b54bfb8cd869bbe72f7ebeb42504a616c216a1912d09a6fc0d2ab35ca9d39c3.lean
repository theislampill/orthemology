import HistoryStageSafety
import RegionAlgorithm

noncomputable section
open MeasureTheory ProbabilityTheory Filter
open Orthemology.Tranche2.PolicyEmbedding

namespace HiddenParity.Necessity
open HiddenParity.Stochastic HiddenParity.Stage
universe u v w
variable {State Action : Type u} {R : Type v} {Model : Type w}
variable [Fintype State] [Fintype Action] [DecidableEq State] [DecidableEq Action] [Inhabited State]
variable [DecidableEq Model]
variable [MeasurableSpace R] [MeasurableSpace State] [MeasurableSingletonClass State]
variable [MeasurableSpace Action] [MeasurableSingletonClass Action]

/-- The semantic all-branch safe actions are contained in the actual algorithmic
stage menu once necessity is known for all strictly smaller live supports. -/
theorem semanticAllowed_subset_regionAllowed
    (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action) (priority : Model → (State × Action) → ℕ)
    (d : State × Action) (B : Finset Model) (lower : Finset Model → Finset State)
    (hLower : ∀ C, C ⊂ B → semanticRegion (R := R) P menu priority d C ⊆ lower C) :
    semanticAllowed (R := R) P menu priority d B ⊆
      regionAllowed P menu B lower (semanticRegion (R := R) P menu priority d B) := by
  intro e he
  obtain ⟨hMenu, hSource, hChild⟩ := (mem_semanticAllowed P menu priority d B e).mp he
  refine (mem_regionAllowed P menu B lower _ e).mpr ⟨hSource, hMenu, ?_⟩
  intro y hC
  have hy := hChild y hC
  by_cases hEq : liveUpdate P B e y = B
  · simpa only [hEq, if_true] using hy
  · simp only [if_neg hEq]
    apply hLower (liveUpdate P B e y) (Finset.ssubset_iff_subset_ne.mpr ⟨Finset.filter_subset _ _, hEq⟩)
    exact hy

/-- A real semantic winning region is postfixed by the target/exit region
operator. Positive-prefix continuation and all-branch licensing are derived
upstream from actual policy laws, not assumed as a postfixed-point interface. -/
theorem semanticRegion_postfixed
    (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action) (priority : Model → (State × Action) → ℕ)
    (d : State × Action) (B : Finset Model) (lower : Finset Model → Finset State)
    (hLower : ∀ C, C ⊂ B → semanticRegion (R := R) P menu priority d C ⊆ lower C) :
    semanticRegion (R := R) P menu priority d B ⊆
      regionStep P menu priority B lower (semanticRegion (R := R) P menu priority d B) := by
  intro s hs
  obtain ⟨w⟩ := (mem_semanticRegion P menu priority d B s).mp hs
  refine (mem_regionStep P menu priority B lower _ s).mpr ⟨hs, ?_⟩
  intro θ hθ
  have hA := semanticAllowed_subset_regionAllowed P menu priority d B lower hLower
  rcases semantic_winning_target_or_exit w θ hθ with hExit | ⟨t, ht, hPath⟩
  · exact Or.inl (reachableExit_mono P B θ hA hExit)
  · exact Or.inr ⟨t, targetStates_mono P B priority θ hA ht, reach_mono hA hPath⟩

/-- Full observed-state, support-changing necessity. The proof inducts on finite
support fuel and uses actual same-support descending state iteration, with all
proper successor branches handled by the induction hypothesis. -/
theorem semanticRegion_subset_computedRegion
    (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action) (priority : Model → (State × Action) → ℕ)
    (d : State × Action) (fuel : ℕ) (B : Finset Model) (hFuel : B.card ≤ fuel) :
    semanticRegion (R := R) P menu priority d B ⊆ computedRegion P menu priority fuel B := by
  induction fuel generalizing B with
  | zero =>
      intro s hs
      obtain ⟨w⟩ := (mem_semanticRegion P menu priority d B s).mp hs
      have hCard : 0 < B.card := Finset.card_pos.mpr w.nonempty
      omega
  | succ n ih =>
      intro s hs
      obtain ⟨w⟩ := (mem_semanticRegion P menu priority d B s).mp hs
      have hLower : ∀ C, C ⊂ B → semanticRegion (R := R) P menu priority d C ⊆
          computedRegion P menu priority n C := by
        intro C hC
        have hCard := Finset.card_lt_card hC
        exact ih C (by omega)
      have hPost := semanticRegion_postfixed P menu priority d B (computedRegion P menu priority n) hLower
      rw [computedRegion, if_pos w.nonempty]
      exact postfixed_subset_descend _ (regionStep_mono P menu priority B _) hPost
        (Finset.subset_univ _) (Fintype.card State) hs

/-- Every genuinely common lawful almost-sure hidden-parity winning policy lies
in the explicit finite computed region. This is the necessity direction only. -/
theorem winning_policy_mem_winningRegion
    (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action) (priority : Model → (State × Action) → ℕ)
    (d : State × Action) (B : Finset Model) (s : State)
    (w : WinningPolicy (R := R) P menu priority d B s) :
    s ∈ winningRegion P menu priority B := by
  exact semanticRegion_subset_computedRegion P menu priority d B.card B (le_refl _)
    ((mem_semanticRegion P menu priority d B s).mpr ⟨w⟩)

/-- A negative region result certifies that no common lawful policy with this
arbitrary measurable seed space can win almost surely. The theorem is uniform
in that seed space; it is not a finite-memory-policy check. -/
theorem computed_losing_excludes_common_policy
    (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action) (priority : Model → (State × Action) → ℕ)
    (d : State × Action) (B : Finset Model) (s : State)
    (hLose : s ∉ winningRegion P menu priority B) :
    ¬ SemanticWinning (R := R) P menu priority d B s := by
  rintro ⟨w⟩
  exact hLose (winning_policy_mem_winningRegion P menu priority d B s w)

end HiddenParity.Necessity
