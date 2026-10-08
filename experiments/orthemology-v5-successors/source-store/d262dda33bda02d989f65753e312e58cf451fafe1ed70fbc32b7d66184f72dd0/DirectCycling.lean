import DirectController
import PhaseStabilization

noncomputable section
open MeasureTheory Filter
open Orthemology.Tranche2.PolicyEmbedding Orthemology.Tranche2.RecurrentSupport
namespace OrthemicCertificate.Direct
open HiddenParity HiddenParity.Sufficiency HiddenParity.Stochastic HiddenParity.Adaptive
open HiddenParity.Necessity HiddenParity.Stage HiddenParity.PhaseArithmetic

/-- Fairness follows from the executable sorted cycle and actual departure
counts; it is not a supplied scheduler or fairness oracle. -/
theorem cycle_every_action_recurrent {S A : Type*} [DecidableEq S] [LinearOrder A]
    (x : ℕ → S) (s : S) (F : Finset A) (fallback : A)
    (hRec : ∃ᶠ n in atTop, x n = s) (a : F) :
    ∃ᶠ n in atTop, x n = s ∧ cycleAction F fallback (visitsBefore x s n) = a.val := by
  apply frequently_atTop.mpr
  intro N
  let j := (N+1) * F.card + ((F.orderIsoOfFin rfl).symm a).val
  obtain ⟨n,hn,hc⟩ := recurrent_state_consumes_visit x s hRec j
  have hpos : 0 < F.card := Finset.card_pos.mpr ⟨a.val,a.property⟩
  have hj : N ≤ j := by
    dsimp [j]
    exact (Nat.le_succ N).trans ((Nat.le_mul_of_pos_right _ hpos).trans (Nat.le_add_right _ _))
  have hjn : j ≤ n := hc ▸ visitsBefore_le_time x s n
  refine ⟨n,hj.trans hjn,hn,?_⟩
  rw [hc]
  exact cycleAction_at_index F fallback a (N+1)

/-- Zero/one phase increments cannot cross an accurate true-model phase. -/
theorem cycling_phase_eventually_constant {Model : Type*} [LinearOrder Model]
    (p : ℕ → ℕ) (N K : ℕ) (B : Finset Model) (fallback σ : Model) (hσ : σ ∈ B)
    (hStep : ∀ n, N ≤ n → p (n+1) = p n ∨ p (n+1) = p n+1)
    (hStop : ∀ n, N ≤ n → K ≤ p n → cycleAction B fallback (p n) = σ → p (n+1) = p n) :
    ∃ j, ∀ᶠ n in atTop, p n = j := by
  obtain ⟨b,hb,hcycle⟩ := exists_cycle_barrier B fallback σ hσ (max K (p N))
  have hB : ∀ n, N ≤ n → p n ≤ b := by
    intro n hn
    induction n,hn using Nat.le_induction with
    | base => exact (le_max_right _ _).trans hb
    | succ n hn ih =>
      by_cases he : p n = b
      · have hK : K ≤ p n := by omega
        have hC : cycleAction B fallback (p n) = σ := by simpa [he] using hcycle
        have hs := hStop n hn hK hC
        omega
      · have hs := hStep n hn
        omega
  apply bounded_tail_eventually_constant p N b hB
  intro n hn
  have hs := hStep n hn
  omega

universe u v w
variable {State Action : Type u} {R : Type v} {Model : Type w}
variable [Fintype State] [Fintype Action] [DecidableEq State] [DecidableEq Action] [LinearOrder Action]
variable [Inhabited State] [LinearOrder Model]
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
    (priority : Model → (State × Action) → ℕ)
    (F : StageData Model State Action) [hF : CertifiedStageFamily P menu priority F]
    (B : Finset Model)
    (θ σ : Model) (hθ : θ ∈ B)
    (x : ℕ → State × Action) (fallback : Action)
    (hActual : IsEndComponent Prod.fst (supportSuccessors (realRows P σ)) (recurrentSet x))
    (hSuccessors : ∀ e ∈ recurrentSet x, ∀ y, 0 < P.row σ e y →
      ∃ᶠ n in atTop, x n = e ∧ (x (n+1)).1 = y)
    (hStable : ∀ᶠ n in atTop, liveUpdate P B (x n) (x (n+1)).1 = B)
    (hRegion : ∀ᶠ n in atTop, (x n).1 ∈ F.states B)
    (hCycle : ∀ᶠ n in atTop, (x n).2 =
      cycleAction (retainedActions (stageActions P menu priority F B) (x n).1) fallback
        (visitsBefore (fun k => (x k).1) (x n).1 n))
    (hAvoid : ∀ᶠ n in atTop, (x n).1 ∉ stageTargets P menu priority F B θ) :
    ∃ e ∈ recurrentSet x, P.row θ e ≠ P.row σ e := by
  classical
  by_contra hNoMismatch
  have hm : ∀ e ∈ recurrentSet x, P.row θ e = P.row σ e := by
    simpa only [not_exists,_root_.not_and,not_not] using hNoMismatch
  let W := F.states B
  let D := stageActions P menu priority F B
  let T := stageTargets P menu priority F B θ
  have hCW : usedStates Prod.fst (recurrentSet x) ⊆ W := by
    intro s hs
    obtain ⟨e,he,hes⟩ := Finset.mem_image.mp hs
    obtain ⟨n,hn,hW⟩ := (((mem_recurrentSet x e).mp he).and_eventually hRegion).exists
    simpa [hn,hes] using hW
  have hReach : ∀ s ∈ W, ReachableExit P B θ D s ∨
      ∃ t ∈ T, Reach Prod.fst (internalSuccessors P B) D s t := hF.reach B θ hθ
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

end OrthemicCertificate.Direct
