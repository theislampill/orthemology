import P02A2.Fibres
import P02A2.Refinement
import Mathlib

/-! UNEXECUTED: dependent coordinate spaces and full countable histories.
This is the actual U05 -> CV-R measurable-event bridge, not a formal atom axiom. -/
namespace P02A2.Observation
open Set MeasureTheory
variable {Ω : Type*} [MeasurableSpace Ω]
variable {Q : ℕ → Type*} [∀ n, MeasurableSpace (Q n)]
  [∀ n, MeasurableSingletonClass (Q n)]
variable (μ : Measure Ω) [IsFiniteMeasure μ]

def history (Y : ∀ n, Ω → Q n) (ω : Ω) : ∀ n, Q n := fun n => Y n ω
noncomputable def event (Y : ∀ n, Ω → Q n) (n : ℕ) : Set Ω :=
  Y n ⁻¹' positive (μ.map (Y n))
noncomputable def fullEvent (Y : ∀ n, Ω → Q n) : Set Ω :=
  history Y ⁻¹' positive (μ.map (history Y))

theorem history_measurable {Y : ∀ n, Ω → Q n} (hY : ∀ n, Measurable (Y n)) :
    Measurable (history Y) := measurable_pi_lambda _ hY

theorem event_measurable {Y : ∀ n, Ω → Q n} (hY : ∀ n, Measurable (Y n)) (n : ℕ) :
    MeasurableSet (event μ Y n) := (positive_measurable (μ.map (Y n))).preimage (hY n)

theorem fullEvent_measurable {Y : ∀ n, Ω → Q n} (hY : ∀ n, Measurable (Y n)) :
    MeasurableSet (fullEvent μ Y) :=
  (positive_measurable (μ.map (history Y))).preimage (history_measurable hY)

theorem event_step {Y : ∀ n, Ω → Q n} (hY : ∀ n, Measurable (Y n))
    (h : ∀ n, Q (n+1) → Q n) (coh : ∀ n ω, Y n ω = h n (Y (n+1) ω)) (n : ℕ) :
    event μ Y (n+1) ⊆ event μ Y n := by
  intro ω hω
  change 0 < μ.map (Y n) {Y n ω}
  change 0 < μ.map (Y (n+1)) {Y (n+1) ω} at hω
  rw [Measure.map_apply (hY n) (measurableSet_singleton _)]
  rw [Measure.map_apply (hY (n+1)) (measurableSet_singleton _)] at hω
  apply lt_of_lt_of_le hω (measure_mono ?_)
  intro ω' hω'
  change Y n ω' = Y n ω
  change Y (n+1) ω' = Y (n+1) ω at hω'
  rw [coh n ω', coh n ω, hω']

theorem events_antitone {Y : ∀ n, Ω → Q n} (hY : ∀ n, Measurable (Y n))
    (h : ∀ n, Q (n+1) → Q n) (coh : ∀ n ω, Y n ω = h n (Y (n+1) ω)) :
    Antitone (event μ Y) := antitone_nat_of_succ_le (event_step μ hY h coh)

theorem full_subset_event {Y : ∀ n, Ω → Q n} (hY : ∀ n, Measurable (Y n)) (n : ℕ) :
    fullEvent μ Y ⊆ event μ Y n := by
  intro ω hω
  change 0 < μ.map (Y n) {Y n ω}
  change 0 < μ.map (history Y) {history Y ω} at hω
  rw [Measure.map_apply (hY n) (measurableSet_singleton _)]
  rw [Measure.map_apply (history_measurable hY) (measurableSet_singleton _)] at hω
  apply lt_of_lt_of_le hω (measure_mono ?_)
  intro ω' hω'
  exact congrFun hω' n

theorem full_subset_persist {Y : ∀ n, Ω → Q n} (hY : ∀ n, Measurable (Y n)) :
    fullEvent μ Y ⊆ Refinement.persist (event μ Y) := by
  intro ω hω
  exact mem_iInter.mpr (fun n => full_subset_event μ hY n hω)

theorem observation_extinction_identity {Y : ∀ n, Ω → Q n}
    (hY : ∀ n, Measurable (Y n)) (h : ∀ n, Q (n+1) → Q n)
    (coh : ∀ n ω, Y n ω = h n (Y (n+1) ω)) :
    μ (fullEvent μ Y)ᶜ = μ (event μ Y 0)ᶜ +
      (∑' n, μ (Refinement.loss (event μ Y) n)) +
      μ (Refinement.persist (event μ Y) \ fullEvent μ Y) := by
  exact Refinement.measure_extinction_decomposition μ (events_antitone μ hY h coh)
    (event_measurable μ hY) (fullEvent_measurable μ hY) (full_subset_persist μ hY)

section Probability
variable [IsProbabilityMeasure μ]

theorem mapped_probability {Z : Type*} [MeasurableSpace Z]
    {f : Ω → Z} (hf : Measurable f) : IsProbabilityMeasure (μ.map f) :=
  ⟨by rw [Measure.map_apply hf MeasurableSet.univ]; simp⟩

theorem defect_mapped_complement {Z : Type*} [MeasurableSpace Z]
    [MeasurableSingletonClass Z] {f : Ω → Z} (hf : Measurable f) :
    defect (μ.map f) = (μ (f ⁻¹' positive (μ.map f))ᶜ).toReal := by
  haveI := mapped_probability μ hf
  rw [defect_eq_diffuse_toReal (μ.map f)]
  unfold diffuseMass
  rw [Measure.map_apply hf (positive_measurable (μ.map f)).compl]
  rfl

theorem coarse_law {Y : ∀ n, Ω → Q n} (hY : ∀ n, Measurable (Y n))
    (h : ∀ n, Q (n+1) → Q n) (hh : ∀ n, Measurable (h n))
    (coh : ∀ n ω, Y n ω = h n (Y (n+1) ω)) (n : ℕ) :
    (μ.map (Y (n+1))).map (h n) = μ.map (Y n) := by
  rw [Measure.map_map (hh n) (hY (n+1))]
  congr 1
  funext ω
  exact (coh n ω).symm

noncomputable def increment (Y : ∀ n, Ω → Q n)
    (h : ∀ n, Q (n+1) → Q n) (n : ℕ) : ℝ :=
  ∑' y : positive (μ.map (Y n)), (μ.map (Y n) {y.val}).toReal *
    defect (fibreLaw (μ.map (Y (n+1))) (h n) y.val)

theorem step_fibre {Y : ∀ n, Ω → Q n} (hY : ∀ n, Measurable (Y n))
    (h : ∀ n, Q (n+1) → Q n) (hh : ∀ n, Measurable (h n))
    (coh : ∀ n ω, Y n ω = h n (Y (n+1) ω)) (n : ℕ) :
    defect (μ.map (Y (n+1))) = defect (μ.map (Y n)) + increment μ Y h n := by
  haveI := mapped_probability μ (hY (n+1))
  have he := defect_fibre_identity (μ.map (Y (n+1))) (hh n)
  rw [coarse_law μ hY h hh coh n] at he
  exact he

theorem step_loss {Y : ∀ n, Ω → Q n} (hY : ∀ n, Measurable (Y n))
    (h : ∀ n, Q (n+1) → Q n) (coh : ∀ n ω, Y n ω = h n (Y (n+1) ω)) (n : ℕ) :
    defect (μ.map (Y (n+1))) = defect (μ.map (Y n)) +
      (μ (Refinement.loss (event μ Y) n)).toReal := by
  have hs := event_step μ hY h coh n
  have hp : (event μ Y (n+1))ᶜ = (event μ Y n)ᶜ ∪ Refinement.loss (event μ Y) n := by
    ext x
    simp only [mem_compl_iff, mem_union, Refinement.loss, mem_diff]
    constructor
    · intro hn; by_cases hx : x ∈ event μ Y n
      · exact Or.inr ⟨hx, hn⟩
      · exact Or.inl hx
    · rintro (hx | ⟨_,hn⟩) hy
      · exact hx (hs hy)
      · exact hn hy
  have hd : Disjoint (event μ Y n)ᶜ (Refinement.loss (event μ Y) n) :=
    Set.disjoint_left.mpr (by intro x hx hy; exact hx hy.1)
  rw [defect_mapped_complement μ (hY (n+1)), defect_mapped_complement μ (hY n)]
  change (μ (event μ Y (n+1))ᶜ).toReal = _
  rw [hp, measure_union hd (Refinement.loss_measurable (event_measurable μ hY) n),
    ENNReal.toReal_add (measure_ne_top μ _) (measure_ne_top μ _)]
  rfl

theorem increment_eq_loss {Y : ∀ n, Ω → Q n} (hY : ∀ n, Measurable (Y n))
    (h : ∀ n, Q (n+1) → Q n) (hh : ∀ n, Measurable (h n))
    (coh : ∀ n ω, Y n ω = h n (Y (n+1) ω)) (n : ℕ) :
    increment μ Y h n = (μ (Refinement.loss (event μ Y) n)).toReal := by
  have hf := step_fibre μ hY h hh coh n
  have hl := step_loss μ hY h coh n
  linarith

theorem increments_summable {Y : ∀ n, Ω → Q n} (hY : ∀ n, Measurable (Y n))
    (h : ∀ n, Q (n+1) → Q n) (hh : ∀ n, Measurable (h n))
    (coh : ∀ n ω, Y n ω = h n (Y (n+1) ω)) :
    Summable (increment μ Y h) := by
  have he : increment μ Y h = fun n => (μ (Refinement.loss (event μ Y) n)).toReal :=
    funext (increment_eq_loss μ hY h hh coh)
  rw [he]
  exact Refinement.losses_real_summable μ (events_antitone μ hY h coh) (event_measurable μ hY)

theorem finite_observation_identity {Y : ∀ n, Ω → Q n} (hY : ∀ n, Measurable (Y n))
    (h : ∀ n, Q (n+1) → Q n) (hh : ∀ n, Measurable (h n))
    (coh : ∀ n ω, Y n ω = h n (Y (n+1) ω)) (N : ℕ) :
    defect (μ.map (Y N)) = defect (μ.map (Y 0)) +
      ∑ n ∈ Finset.range N, increment μ Y h n :=
  Refinement.finite_telescope (fun n => defect (μ.map (Y n))) (increment μ Y h)
    (step_fibre μ hY h hh coh) N

theorem full_observation_identity {Y : ∀ n, Ω → Q n} (hY : ∀ n, Measurable (Y n))
    (h : ∀ n, Q (n+1) → Q n) (hh : ∀ n, Measurable (h n))
    (coh : ∀ n ω, Y n ω = h n (Y (n+1) ω)) :
    defect (μ.map (history Y)) = defect (μ.map (Y 0)) +
      (∑' n, increment μ Y h n) +
      (μ (Refinement.persist (event μ Y) \ fullEvent μ Y)).toReal := by
  rw [defect_mapped_complement μ (history_measurable hY), defect_mapped_complement μ (hY 0)]
  have he := Refinement.real_extinction_decomposition μ (events_antitone μ hY h coh)
    (event_measurable μ hY) (fullEvent_measurable μ hY) (full_subset_persist μ hY)
  change (μ (fullEvent μ Y)ᶜ).toReal = _
  rw [he]
  congr 2
  apply tsum_congr
  intro n
  exact (increment_eq_loss μ hY h hh coh n).symm
end Probability
end P02A2.Observation
