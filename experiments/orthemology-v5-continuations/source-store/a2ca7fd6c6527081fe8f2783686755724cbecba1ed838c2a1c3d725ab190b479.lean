import ResetExpectation

noncomputable section
open MeasureTheory ProbabilityTheory Finset
open scoped BigOperators ENNReal

namespace Orthemology.Tranche2
variable {Phase Θ : Type*} {Obs : Phase → Θ → Type*}
    [Fintype Phase] [Fintype Θ] [∀ p a, Fintype (Obs p a)]

abbrev ObservationRecord := Σ p : Phase, Σ a : Θ, Obs p a
abbrev RecordedState := ResetState (Obs := Obs) × Option (ObservationRecord (Obs := Obs))
instance recordedStateMeasurableSpace : MeasurableSpace (RecordedState (Obs := Obs)) := ⊤
instance : MeasurableSingletonClass (RecordedState (Obs := Obs)) := ⟨fun _ => trivial⟩
instance : Countable (RecordedState (Obs := Obs)) := inferInstance

def recordedUpdate
    (stay : (p : Phase) → (a : Θ) → Obs p a → Bool)
    (next : (p : Phase) → (a : Θ) → Obs p a → Phase)
    (π : (p : Phase) → PhaseHistory (Obs := Obs) p → Θ)
    (s : RecordedState (Obs := Obs)) (y : Obs s.1.1 (π s.1.1 s.1.2)) : RecordedState (Obs := Obs) :=
  (resetUpdate stay next π s.1 y, some ⟨s.1.1,π s.1.1 s.1.2,y⟩)

def recordedTransitionPMF
    (K : (p : Phase) → (θ a : Θ) → Obs p a → ℝ)
    (stay : (p : Phase) → (a : Θ) → Obs p a → Bool)
    (next : (p : Phase) → (a : Θ) → Obs p a → Phase)
    (π : (p : Phase) → PhaseHistory (Obs := Obs) p → Θ)
    (hK : ∀ p η a y, 0 ≤ K p η a y)
    (hNorm : ∀ p η a, ∑ y, K p η a y = 1)
    (θ : Θ) (s : RecordedState (Obs := Obs)) : PMF (RecordedState (Obs := Obs)) :=
  (observationPMF K hK hNorm θ s.1.1 (π s.1.1 s.1.2)).map (recordedUpdate stay next π s)

def recordedTransitionKernel
    (K : (p : Phase) → (θ a : Θ) → Obs p a → ℝ)
    (stay : (p : Phase) → (a : Θ) → Obs p a → Bool)
    (next : (p : Phase) → (a : Θ) → Obs p a → Phase)
    (π : (p : Phase) → PhaseHistory (Obs := Obs) p → Θ)
    (hK : ∀ p η a y, 0 ≤ K p η a y)
    (hNorm : ∀ p η a, ∑ y, K p η a y = 1)
    (θ : Θ) : Kernel (RecordedState (Obs := Obs)) (RecordedState (Obs := Obs)) where
  toFun s := (recordedTransitionPMF K stay next π hK hNorm θ s).toMeasure
  measurable' := measurable_of_countable _

instance recordedTransitionKernel_markov
    (K : (p : Phase) → (θ a : Θ) → Obs p a → ℝ)
    (stay : (p : Phase) → (a : Θ) → Obs p a → Bool)
    (next : (p : Phase) → (a : Θ) → Obs p a → Phase)
    (π : (p : Phase) → PhaseHistory (Obs := Obs) p → Θ)
    (hK : ∀ p η a y, 0 ≤ K p η a y)
    (hNorm : ∀ p η a, ∑ y, K p η a y = 1) (θ : Θ) :
    IsMarkovKernel (recordedTransitionKernel K stay next π hK hNorm θ) :=
  ⟨fun s => by change IsProbabilityMeasure (recordedTransitionPMF K stay next π hK hNorm θ s).toMeasure; infer_instance⟩

/-- Recorded outcomes remain in the public state even when controller memory
resets. The measure is the pushforward of the full stopped-prefix PMF. -/
theorem recordedTransition_lintegral
    (K : (p : Phase) → (θ a : Θ) → Obs p a → ℝ)
    (stay : (p : Phase) → (a : Θ) → Obs p a → Bool)
    (next : (p : Phase) → (a : Θ) → Obs p a → Phase)
    (π : (p : Phase) → PhaseHistory (Obs := Obs) p → Θ)
    (hK : ∀ p η a y, 0 ≤ K p η a y)
    (hNorm : ∀ p η a, ∑ y, K p η a y = 1)
    (θ : Θ) (s : RecordedState (Obs := Obs)) (f : RecordedState (Obs := Obs) → ℝ≥0∞) :
    (∫⁻ t, f t ∂recordedTransitionKernel K stay next π hK hNorm θ s) =
      ∑ y : Obs s.1.1 (π s.1.1 s.1.2), ENNReal.ofReal (K s.1.1 θ (π s.1.1 s.1.2) y) *
        f (recordedUpdate stay next π s y) := by
  letI : MeasurableSpace (Obs s.1.1 (π s.1.1 s.1.2)) := ⊤
  letI : MeasurableSingletonClass (Obs s.1.1 (π s.1.1 s.1.2)) := ⟨fun _ => trivial⟩
  change (∫⁻ t, f t ∂(recordedTransitionPMF K stay next π hK hNorm θ s).toMeasure) = _
  unfold recordedTransitionPMF
  rw [← PMF.toMeasure_map (recordedUpdate stay next π s)
    (observationPMF K hK hNorm θ s.1.1 (π s.1.1 s.1.2)) (measurable_of_finite _),
    lintegral_map (measurable_of_countable _) (measurable_of_finite _), lintegral_fintype]
  apply Finset.sum_congr rfl
  intro y _
  rw [PMF.toMeasure_apply_singleton _ y (measurableSet_singleton y)]
  exact mul_comm _ _

end Orthemology.Tranche2
