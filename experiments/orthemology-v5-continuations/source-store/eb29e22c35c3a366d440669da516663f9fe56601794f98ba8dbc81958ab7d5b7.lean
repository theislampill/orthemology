import FairStageNavigation

noncomputable section
open MeasureTheory Filter
open Orthemology.Tranche2.PolicyEmbedding Orthemology.Tranche2.RecurrentSupport

namespace HiddenParity.Sufficiency
open HiddenParity.Stochastic HiddenParity.Adaptive HiddenParity.Necessity HiddenParity.Stage
universe u v w
variable {State Action : Type u} {R : Type v} {Model : Type w}
variable [Fintype State] [Fintype Action] [DecidableEq State] [DecidableEq Action]
variable [Inhabited State] [DecidableEq Model]
variable [MeasurableSpace State] [MeasurableSingletonClass State]
variable [MeasurableSpace Action] [MeasurableSingletonClass Action]

/-- A fixed mode reached after any finite prefix retains full action fairness;
the global visit counter may have any finite offset when that mode begins. -/
theorem eventual_cycle_fair (x : ℕ → State × Action) (E : Finset (State × Action))
    (fallback : Action)
    (hCycle : ∀ᶠ n in atTop, (x n).2 = cycleAction (retainedActions E (x n).1) fallback
      (visitsBefore (fun k => (x k).1) (x n).1 n)) :
    ∀ e ∈ E, e.1 ∈ usedStates Prod.fst (recurrentSet x) → e ∈ recurrentSet x := by
  intro e he hs
  obtain ⟨f,hf,hfs⟩ := Finset.mem_image.mp hs
  have hRec : ∃ᶠ n in atTop, (x n).1 = e.1 :=
    ((mem_recurrentSet x f).mp hf).mono (fun n hn => by simpa [hn] using hfs)
  have hBoth := cycle_every_action_recurrent (fun k => (x k).1) e.1
    (retainedActions E e.1) fallback hRec ⟨e.2,(mem_retainedActions E e.1 e.2).mpr he⟩
  apply (mem_recurrentSet x e).mpr
  apply (hBoth.and_eventually hCycle).mono
  intro n hn
  apply Prod.ext hn.1.1
  rw [hn.2,hn.1.1]
  exact hn.1.2

/-- Recurring actual positive successors turn eventual observed support stability
into zero-exit rows on the exact recurrent pair set. -/
theorem eventual_support_noExit
    (P : RationalKernel Model (State × Action) State) (B : Finset Model) (θ : Model)
    (x : ℕ → State × Action)
    (hSuccessors : ∀ e ∈ recurrentSet x, ∀ y, 0 < P.row θ e y →
      ∃ᶠ n in atTop, x n = e ∧ (x (n+1)).1 = y)
    (hStable : ∀ᶠ n in atTop, liveUpdate P B (x n) (x (n+1)).1 = B) :
    ∀ e ∈ recurrentSet x, NoExit P B θ e := by
  intro e he y hy
  obtain ⟨n,hn,hSame⟩ := ((hSuccessors e he y hy).and_eventually hStable).exists
  apply (liveUpdate_eq_iff_internal P B e y).mp
  simpa only [hn.1,hn.2] using hSame

/-- Matching actual recurrent rows transport closure to the candidate kernel. -/
theorem recurrent_closed_transfer
    (P : RationalKernel Model (State × Action) State) (θ σ : Model)
    (C : Finset (State × Action))
    (hClosed : ∀ e ∈ C, supportSuccessors (realRows P σ) e ⊆ usedStates Prod.fst C)
    (hMatch : ∀ e ∈ C, P.row θ e = P.row σ e) :
    ∀ e ∈ C, supportSuccessors (realRows P θ) e ⊆ usedStates Prod.fst C := by
  intro e he y hy
  apply hClosed e he
  simpa only [supportSuccessors,realRows,hMatch e he] using hy



/-- An eternal component operation either has a recurrent row mismatching the
candidate, or actually wins the true model's parity objective. Wrong global
candidates whose retained rows match the true model are correctly permitted. -/
theorem eventual_operation_parity_or_mismatch
    (P : RationalKernel Model (State × Action) State) (B : Finset Model)
    (priority : Model → (State × Action) → ℕ) (θ σ : Model) (hθ : θ ∈ B) (hσ : σ ∈ B)
    (allowed E : Finset (State × Action))
    (hQ : MarkovQualifying P Prod.fst B priority θ allowed E)
    (x : ℕ → State × Action) (fallback : Action)
    (hActual : IsEndComponent Prod.fst (supportSuccessors (realRows P σ)) (recurrentSet x))
    (hRetain : ∀ᶠ n in atTop, x n ∈ E)
    (hCycle : ∀ᶠ n in atTop, (x n).2 = cycleAction (retainedActions E (x n).1) fallback
      (visitsBefore (fun k => (x k).1) (x n).1 n)) :
    ParitySuccess (priority σ) x ∨ ∃ e ∈ recurrentSet x, P.row θ e ≠ P.row σ e := by
  classical
  by_cases hm : ∀ e ∈ recurrentSet x, P.row θ e = P.row σ e
  · have hCandidate := qualifying_matching_actual_component P B priority θ θ hθ allowed E hQ
      (fun _ _ => rfl)
    have hEq : recurrentSet x = E := fair_closed_subset_eq (supportSuccessors (realRows P θ))
      (recurrentSet x) E hCandidate hActual.nonempty
      (recurrentSet_subset_of_eventually_mem x E hRetain)
      (recurrent_closed_transfer P θ σ _ hActual.closed hm) (eventual_cycle_fair x E fallback hCycle)
    have hMatch : Match P.row θ σ E := by
      intro e he
      exact (hm e (hEq.symm ▸ he)).symm
    exact Or.inl (by simpa only [ParitySuccess,hEq] using hQ.2.2.2 σ hσ hMatch)
  · push_neg at hm
    exact Or.inr hm

/-- On the genuine computed stage region, an eternal target-avoiding navigation
with stable support must contain an actual recurrent row mismatch. -/
theorem eventual_navigation_has_recurrent_mismatch
    (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action)
    (priority : Model → (State × Action) → ℕ) (B : Finset Model)
    (θ σ : Model) (hθ : θ ∈ B)
    (x : ℕ → State × Action) (fallback : Action)
    (hActual : IsEndComponent Prod.fst (supportSuccessors (realRows P σ)) (recurrentSet x))
    (hSuccessors : ∀ e ∈ recurrentSet x, ∀ y, 0 < P.row σ e y →
      ∃ᶠ n in atTop, x n = e ∧ (x (n+1)).1 = y)
    (hStable : ∀ᶠ n in atTop, liveUpdate P B (x n) (x (n+1)).1 = B)
    (hRegion : ∀ᶠ n in atTop, (x n).1 ∈ winningRegion P menu priority B)
    (hCycle : ∀ᶠ n in atTop, (x n).2 =
      cycleAction (retainedActions (regionAllowed P menu B (winningRegion P menu priority)
        (winningRegion P menu priority B)) (x n).1) fallback
        (visitsBefore (fun k => (x k).1) (x n).1 n))
    (hAvoid : ∀ᶠ n in atTop, (x n).1 ∉ markovTargetStates P Prod.fst B priority θ
      (regionAllowed P menu B (winningRegion P menu priority) (winningRegion P menu priority B))) :
    ∃ e ∈ recurrentSet x, P.row θ e ≠ P.row σ e := by
  classical
  by_contra hNoMismatch
  have hm : ∀ e ∈ recurrentSet x, P.row θ e = P.row σ e := by
    simpa only [not_exists,_root_.not_and,not_not] using hNoMismatch
  let W := winningRegion P menu priority B
  let D := regionAllowed P menu B (winningRegion P menu priority) W
  let T := markovTargetStates P Prod.fst B priority θ D
  have hCW : usedStates Prod.fst (recurrentSet x) ⊆ W := by
    intro s hs
    obtain ⟨e,he,hes⟩ := Finset.mem_image.mp hs
    obtain ⟨n,hn,hW⟩ := (((mem_recurrentSet x e).mp he).and_eventually hRegion).exists
    simpa [hn,hes] using hW
  have hReach : ∀ s ∈ W, ReachableExit P B θ D s ∨
      ∃ t ∈ T, Reach Prod.fst (internalSuccessors P B) D s t := by
    intro s hs
    have hFix := winningRegion_fixed P menu priority B ⟨θ,hθ⟩
    have hStep : s ∈ regionStep P menu priority B (winningRegion P menu priority) W := hFix.symm ▸ hs
    exact ((mem_regionStep P menu priority B _ W s).mp hStep).2 θ hθ
  have hNoσ := eventual_support_noExit P B σ x hSuccessors hStable
  have hNoθ : ∀ e ∈ recurrentSet x, NoExit P B θ e := by
    intro e he y hy
    exact hNoσ e he y (by simpa only [hm e he] using hy)
  obtain ⟨t,ht,htC⟩ := fair_recurrent_hits_target P B θ hθ D (recurrentSet x) W T
    hActual.nonempty hCW (recurrent_closed_transfer P θ σ _ hActual.closed hm)
    (eventual_cycle_fair x D fallback hCycle) hNoθ hReach
  obtain ⟨e,he,het⟩ := Finset.mem_image.mp htC
  obtain ⟨n,hn,hNot⟩ := (((mem_recurrentSet x e).mp he).and_eventually hAvoid).exists
  apply hNot
  simpa only [hn,het] using ht

end HiddenParity.Sufficiency
