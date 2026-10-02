import StableSupportParityNecessity

noncomputable section
open MeasureTheory ProbabilityTheory Filter
open Orthemology.Tranche2.PolicyEmbedding

namespace HiddenParity.Stage
open HiddenParity.Stochastic HiddenParity.Adaptive
universe u v w
variable {State Action : Type u} {R : Type v} {Model : Type w}
variable [Fintype State] [Fintype Action] [DecidableEq State] [DecidableEq Action] [Inhabited State]
variable [DecidableEq Model]
variable [MeasurableSpace R] [MeasurableSpace State] [MeasurableSingletonClass State]
variable [MeasurableSpace Action] [MeasurableSingletonClass Action]

/-- Exact live support after one observed successor under a retained pair. -/
def liveUpdate (P : RationalKernel Model (State × Action) State)
    (B : Finset Model) (e : State × Action) (y : State) : Finset Model :=
  B.filter (fun σ => 0 < P.row σ e y)

@[simp] theorem mem_liveUpdate (P : RationalKernel Model (State × Action) State)
    (B : Finset Model) (e : State × Action) (y : State) (σ : Model) :
    σ ∈ liveUpdate P B e y ↔ σ ∈ B ∧ 0 < P.row σ e y := by
  simp [liveUpdate]

theorem liveUpdate_eq_iff_internal (P : RationalKernel Model (State × Action) State)
    (B : Finset Model) (e : State × Action) (y : State) :
    liveUpdate P B e y = B ↔ y ∈ internalSuccessors P B e := by
  simp [liveUpdate, Finset.filter_eq_self, mem_internalSuccessors]

theorem liveUpdate_nonempty_of_true_positive
    (P : RationalKernel Model (State × Action) State)
    (B : Finset Model) (θ : Model) (hθ : θ ∈ B) (e : State × Action) (y : State)
    (hy : 0 < P.row θ e y) : (liveUpdate P B e y).Nonempty :=
  ⟨θ, (mem_liveUpdate P B e y θ).mpr ⟨hθ, hy⟩⟩

theorem liveUpdate_strict_of_noninternal
    (P : RationalKernel Model (State × Action) State)
    (B : Finset Model) (e : State × Action) (y : State)
    (hy : y ∉ internalSuccessors P B e) : liveUpdate P B e y ⊂ B := by
  apply Finset.ssubset_iff_subset_ne.mpr
  exact ⟨Finset.filter_subset _ _, fun he => hy ((liveUpdate_eq_iff_internal P B e y).mp he)⟩

/-- An exit witness uses an allowed pair reachable by same-support edges and a
candidate-positive actual observation giving nonempty proper surviving support. -/
def ReachableExit (P : RationalKernel Model (State × Action) State)
    (B : Finset Model) (θ : Model) (allowed : Finset (State × Action)) (s₀ : State) : Prop :=
  ∃ e ∈ allowed, Reach Prod.fst (internalSuccessors P B) allowed s₀ e.1 ∧
    ∃ y, 0 < P.row θ e y ∧ (liveUpdate P B e y).Nonempty ∧ liveUpdate P B e y ⊂ B

/-- Observable same-support prefix; no condition is imposed after the first exit. -/
def SameSupportPrefix (P : RationalKernel Model (State × Action) State)
    (B : Finset Model) (x : ℕ → State × Action) (n : ℕ) : Prop :=
  ∀ k < n, liveUpdate P B (x k) (x (k+1)).1 = B

/-- The actual one-stage necessity alternative for arbitrary common seeded
policies. There is no global stability or post-exit legality assumption. -/
theorem winning_policy_target_or_exit
    (P : RationalKernel Model (State × Action) State) (B : Finset Model)
    (priority : Model → (State × Action) → ℕ) (θ : Model) (hθ : θ ∈ B)
    (allowed : Finset (State × Action))
    (s₀ : State) (π : R → History Action State → Action)
    (hπ : Measurable (fun z : R × History Action State => π z.1 z.2))
    (ρ : Measure R) [IsProbabilityMeasure ρ] (d : State × Action)
    (hAS : ∀ σ ∈ B, ∀ᵐ x ∂markovPairLaw P σ s₀ π ρ d, ParitySuccess (priority σ) x)
    (hLegal : ∀ᵐ x ∂markovPairLaw P θ s₀ π ρ d,
      ∀ n, SameSupportPrefix P B x n → x n ∈ allowed) :
    ReachableExit P B θ allowed s₀ ∨
      ∃ t ∈ markovTargetStates P Prod.fst B priority θ allowed,
        Reach Prod.fst (internalSuccessors P B) allowed s₀ t := by
  classical
  by_cases hExit : ReachableExit P B θ allowed s₀
  · exact Or.inl hExit
  · right
    have hNo : ∀ e ∈ allowed, Reach Prod.fst (internalSuccessors P B) allowed s₀ e.1 → NoExit P B θ e := by
      intro e he hReach y hy
      by_contra hNot
      exact hExit ⟨e, he, hReach, y, hy,
        liveUpdate_nonempty_of_true_positive P B θ hθ e y hy,
        liveUpdate_strict_of_noninternal P B e y hNot⟩
    have hPath := canonical_markov_supported_path s₀ π hπ ρ (realRows P θ)
      (realRows_nonnegative P θ) (realRows_normalized P θ) d
    have hNoExitPolicy : ∀ᵐ x ∂markovPairLaw P θ s₀ π ρ d,
        ∀ n, x n ∈ allowed ∧ NoExit P B θ (x n) := by
      filter_upwards [hLegal, hPath] with x hL hP
      have hPrefix : ∀ n, SameSupportPrefix P B x n ∧
          Reach Prod.fst (internalSuccessors P B) allowed s₀ (x n).1 := by
        intro n
        induction n with
        | zero =>
            refine ⟨fun k hk => (Nat.not_lt_zero k hk).elim, ?_⟩
            rw [hP.1]
            exact Relation.ReflTransGen.refl
        | succ n ih =>
            have hAllowed := hL n ih.1
            have hn := hNo (x n) hAllowed ih.2
            have hPositive := hP.2 n
            change (0 : ℝ) < (P.row θ (x n) (x (n+1)).1 : ℝ) at hPositive
            have hInternal := hn (x (n+1)).1 (by exact_mod_cast hPositive)
            refine ⟨?_, ih.2.tail ⟨x n, hAllowed, rfl, hInternal⟩⟩
            intro k hk
            rcases Nat.lt_or_eq_of_le (Nat.le_of_lt_succ hk) with hkn | hkn
            · exact ih.1 k hkn
            · subst k
              exact (liveUpdate_eq_iff_internal P B (x n) (x (n+1)).1).mpr hInternal
      intro n
      exact ⟨hL n (hPrefix n).1, hNo (x n) (hL n (hPrefix n).1) (hPrefix n).2⟩
    exact support_preserving_policy_path_to_target P B priority θ hθ allowed s₀ π hπ ρ d hAS hNoExitPolicy

end HiddenParity.Stage
