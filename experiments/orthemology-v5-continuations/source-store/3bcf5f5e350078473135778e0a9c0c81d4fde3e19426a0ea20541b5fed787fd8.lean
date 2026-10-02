import RecursiveRecordedController
import MarkovZeroEvent
import dependencies.MeasurablePhysicalFlattening

noncomputable section
open MeasureTheory ProbabilityTheory Filter Finset
open scoped BigOperators ENNReal

namespace Orthemology.Tranche2
variable {Θ A Y : Type*} [Fintype Θ] [Fintype Y] [DecidableEq Θ] [DecidableEq A]
    (P : Θ → A → Y → ℝ) (good : Θ → Finset A) (menu : Finset Θ → Finset A)

/-- Every post-initial record is a nonempty actually executed prefix, almost
surely. This is stronger than the eventual non-stalling assertion. -/
theorem recursive_recorded_all_post_nonempty
    (hP : ∀ θ a y, 0 ≤ P θ a y) (hN : ∀ θ a, ∑ y, P θ a y = 1)
    (θ : Θ) (p : WinningPhase P good menu) :
    ∀ᵐ x ∂recursiveRecordedLaw P good menu hP hN θ p, ∀ n,
      recursiveExecuted P good menu (x (n+1)) ≠ [] := by
  classical
  let g : RecursiveRecordState P good menu → ℝ≥0∞ := fun s =>
    if recursiveExecuted P good menu s = [] then 1 else 0
  have hz : ∀ s, (∫⁻ t, g t ∂recordedTransitionKernel (recursiveFullKernel P good menu)
      (recursiveKeep P good menu) (phaseNext P good menu) (recursivePolicy P good menu)
      (recursiveFull_nonneg P good menu hP) (recursiveFull_normalized P good menu hN) θ s) = 0 := by
    intro s
    rw [recordedTransition_lintegral]
    apply Finset.sum_eq_zero
    intro y _
    have hn := executedRecordBlock_nonempty_on_update (phaseActs P good menu)
      (fun p σ => (phaseActs_spec P good menu p σ).1) (recursiveKeep P good menu)
      (phaseNext P good menu) (recursivePolicy P good menu) s y
    simp only [g,recursiveExecuted,if_neg hn,mul_zero]
  have ha := markov_zero_after_initial _ g hz (⟨p,[]⟩,none)
  filter_upwards [ha] with x hx
  intro n
  have hn := hx n
  simpa only [g, ite_eq_right_iff, one_ne_zero, imp_false] using hn

/-- Total decoder of physical actions from the first t+1 post-initial actual
records. The fallback d is never used on the almost-sure nonempty event. -/
def recursivePhysicalAction (d : A) (x : ℕ → RecursiveRecordState P good menu) (t : ℕ) : A :=
  PhysicalFlattening.decode d (fun n => recursiveExecuted P good menu (x (n+1))) t

/-- Literal shared physical-action restoration from the recursive support
criterion and raw observation laws. No external phase, probability-law or
nonempty-block assumption remains. -/
theorem recursive_physical_decoder_eventually_good
    (hP : ∀ θ a y, 0 ≤ P θ a y) (hN : ∀ θ a, ∑ y, P θ a y = 1)
    (θ : Θ) (p : WinningPhase P good menu) (hθ : θ ∈ p.val) (d : A) :
    ∀ᵐ x ∂recursiveRecordedLaw P good menu hP hN θ p, ∀ᶠ t in atTop,
      recursivePhysicalAction P good menu d x t ∈ good θ := by
  filter_upwards [recursive_recorded_bad_eventually_zero P good menu hP hN θ p hθ,
    recursive_recorded_all_post_nonempty P good menu hP hN θ p] with x hb hn
  let blocks := fun n => recursiveExecuted P good menu (x (n+1))
  have hgood : ∀ᶠ n in atTop, ∀ a ∈ blocks n, a ∈ good θ := by
    obtain ⟨N,hN⟩ := eventually_atTop.mp hb
    apply eventually_atTop.mpr
    refine ⟨N,fun n hge a ha => ?_⟩
    have hz := hN (n+1) (by omega)
    have hs : (blocks n).toFinset ⊆ good θ := by
      by_contra hbad
      have hp := (plannedBadCount_pos_iff (good θ) (blocks n)).mpr hbad
      rw [hz] at hp
      exact Nat.lt_irrefl 0 hp
    exact hs (List.mem_toFinset.mpr ha)
  have hf := PhysicalFlattening.eventually_flatten_good blocks
    (PhysicalFlattening.unbounded_of_nonempty blocks hn) (fun a => a ∈ good θ) hgood
  filter_upwards [hf] with t ht
  change PhysicalFlattening.decode d blocks t ∈ good θ
  rw [PhysicalFlattening.decode_eq_flatten d blocks hn]
  exact ht

/-- Each physical action is a measurable finite-prefix function. -/
theorem recursivePhysicalAction_measurable [MeasurableSpace A] [Countable A]
    [MeasurableSingletonClass A] (d : A) (t : ℕ) :
    Measurable (fun x : ℕ → RecursiveRecordState P good menu => recursivePhysicalAction P good menu d x t) := by
  letI : MeasurableSpace (List A) := ⊤
  letI : MeasurableSingletonClass (List A) := ⟨fun _ => trivial⟩
  exact PhysicalFlattening.decode_measurable (Ω := ℕ → RecursiveRecordState P good menu) d
    (fun (n : ℕ) (x : ℕ → RecursiveRecordState P good menu) => recursiveExecuted P good menu (x (n+1)))
    (fun n => (measurable_of_countable (recursiveExecuted P good menu)).comp (measurable_pi_apply (n+1))) t

end Orthemology.Tranche2
