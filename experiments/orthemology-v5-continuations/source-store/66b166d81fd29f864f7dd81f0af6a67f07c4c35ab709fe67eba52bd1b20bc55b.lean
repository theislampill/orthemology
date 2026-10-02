import SemanticWinning

noncomputable section
open MeasureTheory ProbabilityTheory Filter Set
open Orthemology.Tranche2.PolicyEmbedding

namespace HiddenParity.Necessity
open HiddenParity.Stochastic HiddenParity.Stage HiddenParity.ResidualSeed
universe u v w
variable {State Action : Type u} {R : Type v} {Model : Type w}
variable [Fintype State] [Fintype Action] [DecidableEq State] [DecidableEq Action] [Inhabited State]
variable [DecidableEq Model]
variable [MeasurableSpace R] [MeasurableSpace State] [MeasurableSingletonClass State]
variable [MeasurableSpace Action] [MeasurableSingletonClass Action]

/-- All-branch semantic safety: the actual hard menu, a current winning state,
and a common lawful winning continuation at every nonempty observed support update. -/
def SemanticSafe (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action) (priority : Model → (State × Action) → ℕ)
    (d : State × Action) (B : Finset Model) (e : State × Action) : Prop :=
  e.2 ∈ menu B e.1 ∧ e.1 ∈ semanticRegion (R := R) P menu priority d B ∧
    ∀ y, (liveUpdate P B e y).Nonempty →
      y ∈ semanticRegion (R := R) P menu priority d (liveUpdate P B e y)

noncomputable def semanticAllowed (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action) (priority : Model → (State × Action) → ℕ)
    (d : State × Action) (B : Finset Model) : Finset (State × Action) := by
  classical
  exact Finset.univ.filter (SemanticSafe (R := R) P menu priority d B)

@[simp] theorem mem_semanticAllowed (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action) (priority : Model → (State × Action) → ℕ)
    (d : State × Action) (B : Finset Model) (e : State × Action) :
    e ∈ semanticAllowed (R := R) P menu priority d B ↔ SemanticSafe (R := R) P menu priority d B e := by
  classical
  simp [semanticAllowed]

/-- Each positive compatible-seed action branch at a same-support finite history
has a genuine lawful winning continuation at every positive successor. -/
theorem positive_action_branch_safe
    {P : RationalKernel Model (State × Action) State}
    {menu : Finset Model → State → Finset Action} {priority : Model → (State × Action) → ℕ}
    {d : State × Action} {B : Finset Model} {s₀ : State}
    (w : WinningPolicy (R := R) P menu priority d B s₀)
    (h : History (State × Action) State) (hSame : liveHistory P B h = B) (e : State × Action)
    (hPos : 0 < w.seedLaw {r | ActionCompatible (pairPolicy s₀ w.policy) r h ∧
      pairPolicy s₀ w.policy r h = e}) :
    e ∈ semanticAllowed (R := R) P menu priority d B := by
  letI := w.probability
  have hNE : (liveHistory P B h).Nonempty := hSame.symm ▸ w.nonempty
  obtain ⟨r, hr, hLegal⟩ := Measure.exists_mem_of_measure_ne_zero_of_ae hPos.ne'
    (ae_restrict_of_ae (w.lawful h hNE))
  have hMenu := hLegal hr.1
  have hSource : e.1 = currentState s₀ h := by
    rw [← hr.2]
    rfl
  have hMenu' : e.2 ∈ menu B e.1 := by
    simpa only [hr.2, hSame, ← hSource] using hMenu
  have hCompat : 0 < w.seedLaw (CompatibleSeeds (pairPolicy s₀ w.policy) h) :=
    hPos.trans_le (measure_mono (fun _ hx => hx.1))
  obtain ⟨θ, hθ⟩ := w.nonempty
  have hθLive : θ ∈ liveHistory P B h := hSame.symm ▸ hθ
  have hPrefix : 0 < markovHistoryLaw P θ s₀ w.policy w.seedLaw {H | H h.length = h} := by
    rw [markov_observed_prefix_mass P θ s₀ w.policy w.measurable w.seedLaw h, prefix_probability]
    exact ENNReal.mul_pos_iff.mpr ⟨hCompat, live_model_rowLikelihood_positive P B h θ hθLive⟩
  have hCurrent := semanticWinning_at_positive_history w θ hθ h hPrefix
  refine (mem_semanticAllowed P menu priority d B e).mpr ⟨hMenu', ?_, ?_⟩
  · simpa only [hSame, ← hSource] using hCurrent
  · intro y hC
    obtain ⟨σ, hσ⟩ := hC
    have hσB := ((mem_liveUpdate P B e y σ).mp hσ).1
    have hσLive : σ ∈ liveHistory P B ((e,y)::h) := by
      rw [liveHistory_cons, hSame]
      exact hσ
    have hCompEq : CompatibleSeeds (pairPolicy s₀ w.policy) ((e,y)::h) =
        {r | ActionCompatible (pairPolicy s₀ w.policy) r h ∧ pairPolicy s₀ w.policy r h = e} := rfl
    have hExtended : 0 < markovHistoryLaw P σ s₀ w.policy w.seedLaw
        {H | H ((e,y)::h).length = ((e,y)::h)} := by
      rw [markov_observed_prefix_mass P σ s₀ w.policy w.measurable w.seedLaw ((e,y)::h), prefix_probability,
        hCompEq]
      exact ENNReal.mul_pos_iff.mpr ⟨hPos, live_model_rowLikelihood_positive P B ((e,y)::h) σ hσLive⟩
    have hWin := semanticWinning_at_positive_history w σ hσB ((e,y)::h) hExtended
    simpa only [liveHistory_cons, hSame, currentState] using hWin

/-- Safety of the actual selected action is derived for almost every compatible
seed, including when the whole prefix or a particular action branch has probability zero. -/
theorem winning_policy_safe_at_same_support_history
    {P : RationalKernel Model (State × Action) State}
    {menu : Finset Model → State → Finset Action} {priority : Model → (State × Action) → ℕ}
    {d : State × Action} {B : Finset Model} {s₀ : State}
    (w : WinningPolicy (R := R) P menu priority d B s₀)
    (h : History (State × Action) State) (hSame : liveHistory P B h = B) :
    ∀ᵐ r ∂w.seedLaw, ActionCompatible (pairPolicy s₀ w.policy) r h →
      pairPolicy s₀ w.policy r h ∈ semanticAllowed (R := R) P menu priority d B := by
  classical
  have hEach : ∀ e : State × Action, ∀ᵐ r ∂w.seedLaw,
      (ActionCompatible (pairPolicy s₀ w.policy) r h ∧ pairPolicy s₀ w.policy r h = e) →
        e ∈ semanticAllowed (R := R) P menu priority d B := by
    intro e
    by_cases hs : e ∈ semanticAllowed (R := R) P menu priority d B
    · exact ae_of_all _ (fun _ _ => hs)
    · have hZero : w.seedLaw {r | ActionCompatible (pairPolicy s₀ w.policy) r h ∧
          pairPolicy s₀ w.policy r h = e} = 0 := by
        by_contra hn
        exact hs (positive_action_branch_safe w h hSame e (pos_iff_ne_zero.mpr hn))
      rw [ae_iff]
      simpa only [hs, imp_false, not_not] using hZero
  filter_upwards [ae_all_iff.mpr hEach] with r hr
  intro hc
  exact hr (pairPolicy s₀ w.policy r h) ⟨hc, rfl⟩

end HiddenParity.Necessity
