import RecordedTransition
import StoppedActionCost

noncomputable section
namespace Orthemology.Tranche2
variable {Phase Θ A Y : Type*}

lemma stoppedActions_nonempty (acts : List A) (hne : acts ≠ []) (w : StopObs Y acts.length) :
    stoppedActions acts w ≠ [] := by
  cases acts with
  | nil => exact (hne rfl).elim
  | cons a as => cases w <;> simp [stoppedActions]

/-- Only the actually executed stopped prefix is exported as a physical block.
The initial placeholder is empty, and no post-exit actions or symbols appear. -/
def executedRecordBlock (acts : Phase → Θ → List A)
    (s : RecordedState (Obs := fun p σ => StopObs Y (acts p σ).length)) : List A :=
  match s.2 with
  | none => []
  | some ⟨p,σ,w⟩ => stoppedActions (acts p σ) w

lemma executedRecordBlock_update (acts : Phase → Θ → List A)
    (stay : (p : Phase) → (σ : Θ) → StopObs Y (acts p σ).length → Bool)
    (next : (p : Phase) → (σ : Θ) → StopObs Y (acts p σ).length → Phase)
    (π : (p : Phase) → PhaseHistory (Obs := fun p σ => StopObs Y (acts p σ).length) p → Θ)
    (s : RecordedState (Obs := fun p σ => StopObs Y (acts p σ).length))
    (y : StopObs Y (acts s.1.1 (π s.1.1 s.1.2)).length) :
    executedRecordBlock acts (recordedUpdate stay next π s y) =
      stoppedActions (acts s.1.1 (π s.1.1 s.1.2)) y := rfl

lemma executedRecordBlock_nonempty_on_update (acts : Phase → Θ → List A)
    (hne : ∀ p σ, acts p σ ≠ [])
    (stay : (p : Phase) → (σ : Θ) → StopObs Y (acts p σ).length → Bool)
    (next : (p : Phase) → (σ : Θ) → StopObs Y (acts p σ).length → Phase)
    (π : (p : Phase) → PhaseHistory (Obs := fun p σ => StopObs Y (acts p σ).length) p → Θ)
    (s : RecordedState (Obs := fun p σ => StopObs Y (acts p σ).length))
    (y : StopObs Y (acts s.1.1 (π s.1.1 s.1.2)).length) :
    executedRecordBlock acts (recordedUpdate stay next π s y) ≠ [] :=
  stoppedActions_nonempty _ (hne _ _) y

end Orthemology.Tranche2
