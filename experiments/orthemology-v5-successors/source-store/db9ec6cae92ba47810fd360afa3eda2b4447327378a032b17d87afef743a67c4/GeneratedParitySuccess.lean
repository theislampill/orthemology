import GeneratedPhaseStability

noncomputable section
set_option maxHeartbeats 800000
open MeasureTheory Filter
open Orthemology.Tranche2.PolicyEmbedding Orthemology.Tranche2.RecurrentSupport

namespace HiddenParity.Sufficiency
open HiddenParity.Stochastic HiddenParity.Adaptive HiddenParity.Necessity HiddenParity.Stage
universe u w
variable {State Action : Type u} {Model : Type w}
variable [Fintype State] [Fintype Action] [DecidableEq State] [DecidableEq Action] [Inhabited State]
variable [DecidableEq Model]
variable [MeasurableSpace State] [MeasurableSingletonClass State]
variable [MeasurableSpace Action] [MeasurableSingletonClass Action]
variable (P : RationalKernel Model (State × Action) State)
variable (menu : Finset Model → State → Finset Action) (priority : Model → (State × Action) → ℕ)
variable (B₀ : Finset Model) (s₀ : State) (fallback : Model) (fallbackAction : Action) (ε : ℝ)
local notation "reject" => empiricalReject P ε
local notation "π" => generatedPhasePolicy P menu priority B₀ s₀ fallback fallbackAction reject
local notation "H" => runHistory P menu priority B₀ s₀ fallback fallbackAction reject
local notation "x" => runAction P menu priority B₀ s₀ fallback fallbackAction reject
local notation "b" => runSupport P menu priority B₀ s₀ fallback fallbackAction reject
local notation "m" => runMemory P menu priority B₀ s₀ fallback fallbackAction reject

theorem run_navigation_avoids_target (z : Unit × FlatStack (State × Action) State) (n : ℕ)
    (hNone : (m z n).retained = none) :
    (x z n).1 ∉ stageTargets P menu priority (b z n) (phaseCandidate (b z n) fallback (m z n)) := by
  have ha := normalizeMemory_none_avoids P menu priority fallback
    (liveHistory P B₀ (augmentHistory s₀ (erasePairSources (H z n))))
    (observedState s₀ (erasePairSources (H z n)))
    (phaseMemory P menu priority B₀ s₀ fallback reject (erasePairSources (H z n))) hNone
  have hi : (phaseMemory P menu priority B₀ s₀ fallback reject (erasePairSources (H z n))).index =
      (m z n).index := (normalizeMemory_index P menu priority fallback _ _ _).symm
  simp only [runHistory_augment,observedState_erase,phaseCandidate,hi] at ha
  exact ha

/-- The full generated controller wins pathwise on the proved common raw-tape
regularity event. Navigation cannot persist, and an eternal operation either
matches the true recurrent rows or is rejected by the actual observed test. -/
theorem generated_stack_parity
    (hs₀ : s₀ ∈ winningRegion P menu priority B₀) (σ : Model) (hσ : σ ∈ B₀)
    (z : Unit × FlatStack (State × Action) State)
    (hSupported : ∀ e k, 0 < realRows P σ e (z.2 (e,k)))
    (hTape : ∀ e y, 0 < realRows P σ e y → ∃ᶠ k in atTop, z.2 (e,k) = y)
    (hTrue : ∃ K : ℕ, ∀ k, K ≤ k → ∀ n, reject σ k (H z n) = false)
    (hFalse : ∀ θ ∈ B₀, ∀ e ∈ recurrentSet (x z), P.row θ e ≠ P.row σ e →
      ∀ k, ∀ᶠ n in atTop, reject θ k (H z n) = true) :
    ParitySuccess (priority σ) (x z) := by
  obtain ⟨B,j,hσB,hSub,hB,hj,hMode⟩ :=
    generated_phase_and_mode_stable P menu priority B₀ s₀ fallback fallbackAction ε hs₀ σ hσ z hSupported hTrue
  let θ := cycleAction B fallback j
  have hθ : θ ∈ B := cycleAction_mem B fallback ⟨σ,hσB⟩ j
  obtain ⟨N,hN⟩ := eventually_atTop.mp (hB.and hj)
  have hSame : ∀ᶠ n in atTop, b z (n+1) = b z n ∧ (m z (n+1)).index = (m z n).index := by
    refine eventually_atTop.mpr ⟨N,?_⟩
    intro n hn
    exact ⟨(hN (n+1) (by omega)).1.trans (hN n hn).1.symm,
      (hN (n+1) (by omega)).2.trans (hN n hn).2.symm⟩
  have hCandidate : ∀ᶠ n in atTop, phaseCandidate (b z n) fallback (m z n) = θ := by
    filter_upwards [hB,hj] with n hn hjn
    simp only [phaseCandidate,hn,hjn,θ]
  have hNoTest : ∀ᶠ n in atTop, reject θ j (H z (n+1)) = false := by
    filter_upwards [hSame,hCandidate,hj] with n hn hθn hjn
    have ht := run_constant_phase_test_false P menu priority B₀ s₀ fallback fallbackAction reject z n hn.1 hn.2
    simpa only [hθn,hjn] using ht
  have hMatch : ∀ e ∈ recurrentSet (x z), P.row θ e = P.row σ e := by
    intro e he
    by_contra hNe
    obtain ⟨K,hK⟩ := eventually_atTop.mp (hFalse θ (hSub hθ) e he hNe j)
    obtain ⟨n,hn,hLarge⟩ := (hNoTest.and (eventually_ge_atTop K)).exists
    have ht := hK (n+1) (by omega)
    rw [hn] at ht
    cases ht
  have hActual := stack_actual_recurrent_component P σ s₀ π z hSupported hTape
  have hSuccessors := stack_positive_successors_recur P σ s₀ π z hTape
  have hStable : ∀ᶠ n in atTop, liveUpdate P B (x z n) (x z (n+1)).1 = B := by
    refine eventually_atTop.mpr ⟨N,?_⟩
    intro n hn
    have hb := runSupport_succ P menu priority B₀ s₀ fallback fallbackAction reject z n
    rw [(hN n hn).1,(hN (n+1) (by omega)).1] at hb
    exact hb.symm
  have hRegion : ∀ᶠ n in atTop, (x z n).1 ∈ winningRegion P menu priority B := by
    filter_upwards [hB] with n hn
    have hInv := run_invariant P menu priority B₀ s₀ fallback fallbackAction reject hs₀ σ hσ z hSupported n
    simpa only [hn] using hInv.2.1
  rcases hMode with hNav | ⟨E,hE⟩
  · have hCycle : ∀ᶠ n in atTop, (x z n).2 = cycleAction
        (retainedActions (stageActions P menu priority B) (x z n).1) fallbackAction
        (visitsBefore (fun k => (x z k).1) (x z n).1 n) := by
      filter_upwards [hB,hNav] with n hn hNone
      have hc := runAction_cycle P menu priority B₀ s₀ fallback fallbackAction reject z n
      simpa only [activePairs,hNone,Option.getD_none,hn] using hc
    have hAvoid : ∀ᶠ n in atTop, (x z n).1 ∉ stageTargets P menu priority B θ := by
      filter_upwards [hB,hCandidate,hNav] with n hn hcn hnn
      have ha := run_navigation_avoids_target P menu priority B₀ s₀ fallback fallbackAction ε z n hnn
      rw [hcn,hn] at ha
      exact ha
    obtain ⟨e,he,hNe⟩ := eventual_navigation_has_recurrent_mismatch P menu priority B θ σ hθ
      (x z) fallbackAction hActual hSuccessors hStable hRegion hCycle hAvoid
    exact (hNe (hMatch e he)).elim
  · have hQ : MarkovQualifying P Prod.fst B priority θ (stageActions P menu priority B) E := by
      obtain ⟨n,hn,hcn,hen⟩ := (hB.and (hCandidate.and hE)).exists
      have hi := run_invariant P menu priority B₀ s₀ fallback fallbackAction reject hs₀ σ hσ z hSupported n
      have hq := (hi.2.2 E hen).1
      rw [hcn,hn] at hq
      exact hq
    have hRetain : ∀ᶠ n in atTop, x z n ∈ E := by
      filter_upwards [hE] with n hen
      have h := runAction_mem_active P menu priority B₀ s₀ fallback fallbackAction reject hs₀ σ hσ z hSupported n
      simpa only [activePairs,hen,Option.getD_some] using h
    have hCycle : ∀ᶠ n in atTop, (x z n).2 = cycleAction (retainedActions E (x z n).1) fallbackAction
        (visitsBefore (fun k => (x z k).1) (x z n).1 n) := by
      filter_upwards [hE] with n hen
      have hc := runAction_cycle P menu priority B₀ s₀ fallback fallbackAction reject z n
      simpa only [activePairs,hen,Option.getD_some] using hc
    rcases eventual_operation_parity_or_mismatch P B priority θ σ hθ hσB
      (stageActions P menu priority B) E hQ (x z) fallbackAction hActual hRetain hCycle with hWin | ⟨e,he,hNe⟩
    · exact hWin
    · exact (hNe (hMatch e he)).elim

end HiddenParity.Sufficiency
