import RotorClosedClass

/-! Source-bound instantiation of the finite rotor class argument. All supplied
fields are local graph/transition/counter equations. Fair action coverage and
the target/operation consequences are derived, not stored as assumptions. -/
noncomputable section
namespace HiddenParity.Cost
open HiddenParity.Sufficiency HiddenParity.Stochastic HiddenParity.Adaptive
open HiddenParity.Necessity HiddenParity.Stage FiniteChainHitting
universe u v w
variable {State Action : Type u} {Model : Type w} {Q : Type v}
variable [Fintype State] [Fintype Action] [DecidableEq State] [DecidableEq Action] [Inhabited State]
variable [Fintype Q] [DecidableEq Q] [DecidableEq Model]
variable [MeasurableSpace State] [MeasurableSingletonClass State]
variable [MeasurableSpace Action] [MeasurableSingletonClass Action]

/-- Local realization data for a closed class in a frozen actual-σ rotor graph.
`positive_lift` means each actual positive receipt has an augmented successor;
when the graph is killed, this record applies to a class avoiding the kill goal.
The record does not assume fairness, matching, parity, or eventual hitting. -/
structure RotorClassWitness (P : RationalKernel Model (State × Action) State)
    (σ : Model) (F : Finset (State × Action)) (fallback : Action) where
  source : Q → State
  action : Q → Action
  residue : Q → State → ℕ
  edge : Q → Q → Prop
  C : Finset Q
  closed : ClosedClass edge C
  source_used : ∀ q ∈ C, source q ∈ usedStates Prod.fst F
  action_cycle : ∀ q ∈ C, action q = cycleAction (retainedActions F (source q)) fallback (residue q (source q))
  rotor_step : ∀ q ∈ C, ∀ q', edge q q' → ∀ s,
    residue q' s = (residue q s + if source q=s then 1 else 0)%(retainedActions F s).card
  positive_lift : ∀ q ∈ C, ∀ y, 0 < P.row σ (source q,action q) y →
    ∃ q', edge q q' ∧ source q'=y

namespace RotorClassWitness
variable {P : RationalKernel Model (State × Action) State} {σ : Model}
variable {F : Finset (State × Action)} {fallback : Action}
variable (R : RotorClassWitness (Q:=Q) P σ F fallback)

def project : Finset (State × Action) := R.C.image (fun q => (R.source q,R.action q))

omit [Inhabited State] [Fintype Q] [DecidableEq Q] [DecidableEq Model] [MeasurableSpace State] [MeasurableSingletonClass State] [MeasurableSpace Action] [MeasurableSingletonClass Action] in
theorem project_nonempty : R.project.Nonempty := R.closed.1.image _

omit [Fintype Q] [DecidableEq Q] [DecidableEq Model] in
theorem selected_mem (q : Q) (hq : q ∈ R.C) : (R.source q,R.action q) ∈ F := by
  have hmem := cycleAction_mem (retainedActions F (R.source q)) fallback
    (retainedActions_nonempty F (R.source q) (R.source_used q hq)) (R.residue q (R.source q))
  rw [← R.action_cycle q hq] at hmem
  exact (mem_retainedActions F (R.source q) (R.action q)).mp hmem

theorem project_subset : R.project ⊆ F := by
  intro e he
  obtain ⟨q,hq,rfl⟩ := Finset.mem_image.mp he
  exact R.selected_mem q hq

omit [Inhabited State] [Fintype Q] [DecidableEq Q] [DecidableEq Model] [MeasurableSpace State] [MeasurableSingletonClass State] [MeasurableSpace Action] [MeasurableSingletonClass Action] in
theorem next_exists (q : Q) (hq : q ∈ R.C) : ∃ q', R.edge q q' := by
  have hex : ∃ y, 0 < P.row σ (R.source q,R.action q) y := by
    by_contra h
    push_neg at h
    have hs : (∑ y, P.row σ (R.source q,R.action q) y) ≤ 0 := Finset.sum_nonpos (fun y _ => h y)
    rw [P.normalized] at hs
    norm_num at hs
  obtain ⟨y,hy⟩ := hex
  obtain ⟨q',he,_⟩ := R.positive_lift q hq y hy
  exact ⟨q',he⟩

/-- Exact action coverage of the projected class is derived from its source
counter transition equation, for the actual retained-action menu. -/
theorem project_fair : ∀ e ∈ F, e.1 ∈ usedStates Prod.fst R.project → e ∈ R.project := by
  classical
  intro e he hs
  obtain ⟨f,hf,hfs⟩ := Finset.mem_image.mp hs
  obtain ⟨q₀,hq₀,hqf⟩ := Finset.mem_image.mp hf
  have hsrc : R.source q₀=e.1 := (congrArg Prod.fst hqf).trans hfs
  have ha : e.2 ∈ retainedActions F (R.source q₀) := by
    rw [hsrc]
    exact (mem_retainedActions F e.1 e.2).mpr he
  obtain ⟨q,hq,hsource,haction⟩ := rotor_closed_class_covers_menu R.edge R.source R.action
    (retainedActions F) fallback R.residue R.C R.closed (R.next_exists)
    R.action_cycle R.rotor_step q₀ hq₀ e.2 ha
  apply Finset.mem_image.mpr
  refine ⟨q,hq,?_⟩
  exact Prod.ext (hsource.trans hsrc) haction

omit [Inhabited State] [Fintype Q] [DecidableEq Q] [DecidableEq Model] [MeasurableSpace State] [MeasurableSingletonClass State] [MeasurableSpace Action] [MeasurableSingletonClass Action] in
/-- Actual positive receipts close the projected class; no iid or recurrence
property is a premise. -/
theorem project_closed : ∀ e ∈ R.project, supportSuccessors (realRows P σ) e ⊆ usedStates Prod.fst R.project := by
  intro e he y hy
  obtain ⟨q,hq,hqe⟩ := Finset.mem_image.mp he
  have hpos : 0 < P.row σ e y := by
    have hp := (Finset.mem_filter.mp hy).2
    change (0 : ℝ) < (P.row σ e y : ℝ) at hp
    exact_mod_cast hp
  obtain ⟨q',hedge,hsource⟩ := R.positive_lift q hq y (by simpa only [hqe] using hpos)
  have hq' := R.closed.2.1 q hq q' hedge
  apply Finset.mem_image.mpr
  exact ⟨(R.source q',R.action q'),Finset.mem_image.mpr ⟨q',hq',rfl⟩,hsource⟩

/-- Instantiation for a qualifying operating component. Every closed rotor
class avoiding component/support exit projects to the whole chosen component.
Notably full-row matching is not needed for this graph fact: internal edges
are positive in every live true model. -/
theorem operation_project_eq (B : Finset Model) (priority : Model → (State × Action) → ℕ)
    (θ : Model) (hσ : σ ∈ B) (allowed : Finset (State × Action))
    (hQ : MarkovQualifying P Prod.fst B priority θ allowed F) : R.project=F := by
  apply fair_closed_subset_eq (internalSuccessors P B) R.project F hQ.2.2.1
    (R.project_nonempty) (R.project_subset) ?_
    (R.project_fair)
  intro e he y hy
  have hp := (mem_internalSuccessors P B e y).mp hy σ hσ
  apply R.project_closed e he
  simp only [supportSuccessors,Finset.mem_filter,Finset.mem_univ,true_and]
  change (0 : ℝ) < (P.row σ e y : ℝ)
  exact_mod_cast hp

/-- Any mismatch in a qualifying selected component is represented in every
closed actual rotor class. It therefore cannot be hidden in a never-sampled
corner of that component. -/
theorem operation_has_mismatch (B : Finset Model) (priority : Model → (State × Action) → ℕ)
    (θ : Model) (hσ : σ ∈ B) (allowed : Finset (State × Action))
    (hQ : MarkovQualifying P Prod.fst B priority θ allowed F)
    (hNe : ¬ Match P.row θ σ F) :
    ∃ q ∈ R.C, P.row θ (R.source q,R.action q) ≠ P.row σ (R.source q,R.action q) := by
  classical
  have heq := R.operation_project_eq B priority θ hσ allowed hQ
  unfold Match at hNe
  push_neg at hNe
  obtain ⟨e,he,hneq⟩ := hNe
  have hep : e ∈ R.project := heq.symm ▸ he
  obtain ⟨q,hq,hqe⟩ := Finset.mem_image.mp hep
  exact ⟨q,hq,by simpa only [hqe] using Ne.symm hneq⟩

/-- Instantiate the actual computed stage target-or-exit certificate. A closed
rotor class with matching candidate rows and no support exit must contain an
actual candidate target; fair coverage was derived from residue equations. -/
theorem navigation_hits_target
    (menu : Finset Model → State → Finset Action) (priority : Model → (State × Action) → ℕ)
    (B : Finset Model) (θ : Model) (hθ : θ ∈ B)
    (hF : F=stageActions P menu priority B)
    (hRegion : ∀ q ∈ R.C, R.source q ∈ winningRegion P menu priority B)
    (hMatch : Match P.row θ σ R.project)
    (hNo : ∀ e ∈ R.project, NoExit P B σ e) :
    ∃ t ∈ stageTargets P menu priority B θ, t ∈ usedStates Prod.fst R.project := by
  have hCW : usedStates Prod.fst R.project ⊆ winningRegion P menu priority B := by
    intro t ht
    obtain ⟨e,he,het⟩ := Finset.mem_image.mp ht
    obtain ⟨q,hq,hqe⟩ := Finset.mem_image.mp he
    have hsrc : R.source q=t := (congrArg Prod.fst hqe).trans het
    simpa only [hsrc] using hRegion q hq
  have hClosed : ∀ e ∈ R.project, supportSuccessors (realRows P θ) e ⊆ usedStates Prod.fst R.project := by
    intro e he y hy
    apply R.project_closed e he
    have heq : realRows P θ e = realRows P σ e := by
      funext y
      change (P.row θ e y : ℝ) = (P.row σ e y : ℝ)
      rw [hMatch e he]
    simpa only [supportSuccessors,heq] using hy
  have hNoθ : ∀ e ∈ R.project, NoExit P B θ e := by
    intro e he y hy
    apply hNo e he y
    rw [hMatch e he]
    exact hy
  have hReach : ∀ s ∈ winningRegion P menu priority B,
      ReachableExit P B θ F s ∨ ∃ t ∈ stageTargets P menu priority B θ,
        Reach Prod.fst (internalSuccessors P B) F s t := by
    intro s hs
    have hFix := winningRegion_fixed P menu priority B ⟨θ,hθ⟩
    have hStep : s ∈ regionStep P menu priority B (winningRegion P menu priority)
        (winningRegion P menu priority B) := hFix.symm ▸ hs
    have hh := ((mem_regionStep P menu priority B _ _ s).mp hStep).2 θ hθ
    simpa only [hF,stageActions,stageTargets] using hh
  exact fair_recurrent_hits_target P B θ hθ F R.project (winningRegion P menu priority B)
    (stageTargets P menu priority B θ) R.project_nonempty hCW hClosed R.project_fair hNoθ hReach

end RotorClassWitness
end HiddenParity.Cost
