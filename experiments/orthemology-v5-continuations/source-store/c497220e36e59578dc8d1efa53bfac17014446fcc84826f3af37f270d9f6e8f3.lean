import ActualTargetPolicy

noncomputable section
open MeasureTheory Filter
open Orthemology.Tranche2.PolicyEmbedding Orthemology.Tranche2.RecurrentSupport

namespace HiddenParity.Sufficiency
open HiddenParity.Stochastic HiddenParity.Adaptive HiddenParity.Necessity HiddenParity.Stage
universe u v w
variable {State Action : Type u} {R : Type v} {Model : Type w}
variable [Fintype State] [Fintype Action] [DecidableEq State] [DecidableEq Action] [Inhabited State]
variable [DecidableEq Model]
variable [MeasurableSpace R] [MeasurableSpace State] [MeasurableSingletonClass State]
variable [MeasurableSpace Action] [MeasurableSingletonClass Action]

/-- Observable completion of navigation: enter the candidate's target states or
observe a nonempty proper live-support change. The latter nonemptiness is
supplied by actual supported transitions and candidate membership. -/
def NavigationGoal (P : RationalKernel Model (State × Action) State) (B : Finset Model)
    (T : Finset State) (x : ℕ → State × Action) : Prop :=
  ∃ n, (x n).1 ∈ T ∨ liveUpdate P B (x n) (x (n+1)).1 ≠ B

theorem navigationGoal_measurable (P : RationalKernel Model (State × Action) State)
    (B : Finset Model) (T : Finset State) :
    MeasurableSet {x : ℕ → State × Action | NavigationGoal P B T x} := by
  simp only [NavigationGoal,Set.setOf_exists]
  apply MeasurableSet.iUnion
  intro n
  have hm : Measurable (fun x : ℕ → State × Action => (x n, x (n+1))) :=
    (measurable_pi_apply n).prodMk (measurable_pi_apply (n+1))
  exact (Set.toFinite {z : (State × Action) × (State × Action) |
    z.1.1 ∈ T ∨ liveUpdate P B z.1 z.2.1 ≠ B}).measurableSet.preimage hm

/-- Same-support paths propagate through a fair closed recurrent subset. -/
theorem fair_recurrent_reachable_closed
    (P : RationalKernel Model (State × Action) State) (B : Finset Model) (θ : Model) (hθ : θ ∈ B)
    (D C : Finset (State × Action))
    (hClosed : ∀ e ∈ C, supportSuccessors (realRows P θ) e ⊆ usedStates Prod.fst C)
    (hFair : ∀ e ∈ D, e.1 ∈ usedStates Prod.fst C → e ∈ C)
    (s : State) (hs : s ∈ usedStates Prod.fst C) :
    ∀ t, Reach Prod.fst (internalSuccessors P B) D s t → t ∈ usedStates Prod.fst C := by
  intro t ht
  induction ht with
  | refl => exact hs
  | @tail y z hPath hyz ih =>
      obtain ⟨e,he,hey,hz⟩ := hyz
      apply hClosed e (hFair e he (by simpa [hey] using ih))
      have hp := (mem_internalSuccessors P B e z).mp hz θ hθ
      simp only [supportSuccessors, Finset.mem_filter, Finset.mem_univ, true_and]
      change (0 : ℝ) < (P.row θ e z : ℝ)
      exact_mod_cast hp

/-- A fair recurrent subset with no possible support exit cannot avoid all
candidate targets when every current state has a target-or-exit path. -/
theorem fair_recurrent_hits_target
    (P : RationalKernel Model (State × Action) State) (B : Finset Model) (θ : Model) (hθ : θ ∈ B)
    (D C : Finset (State × Action)) (W T : Finset State)
    (hC : C.Nonempty) (hCW : usedStates Prod.fst C ⊆ W)
    (hClosed : ∀ e ∈ C, supportSuccessors (realRows P θ) e ⊆ usedStates Prod.fst C)
    (hFair : ∀ e ∈ D, e.1 ∈ usedStates Prod.fst C → e ∈ C)
    (hNo : ∀ e ∈ C, NoExit P B θ e)
    (hReach : ∀ s ∈ W, ReachableExit P B θ D s ∨ ∃ t ∈ T, Reach Prod.fst (internalSuccessors P B) D s t) :
    ∃ t ∈ T, t ∈ usedStates Prod.fst C := by
  obtain ⟨e,he⟩ := hC
  have hs : e.1 ∈ usedStates Prod.fst C := Finset.mem_image.mpr ⟨e,he,rfl⟩
  have hp := fair_recurrent_reachable_closed P B θ hθ D C hClosed hFair e.1 hs
  rcases hReach e.1 (hCW hs) with ⟨f,hf,hpath,y,hy,hLive,hProper⟩ | ⟨t,ht,hpath⟩
  · have hfC := hFair f hf (hp f.1 hpath)
    have hEq := (liveUpdate_eq_iff_internal P B f y).mpr (hNo f hfC y hy)
    exact False.elim ((Finset.ssubset_iff_subset_ne.mp hProper).2 hEq)
  · exact ⟨t,ht,hp t hpath⟩

end HiddenParity.Sufficiency
