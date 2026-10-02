import GeneratedLiveController
import StoppedNoExit

noncomputable section
open MeasureTheory ProbabilityTheory Filter Finset
open scoped BigOperators ENNReal

namespace Orthemology.Tranche2.ZeroSupportFixture

def P (θ a y : Bool) : ℝ :=
  if θ = false ∧ a = true then (if y then 0 else 1)
  else if y then (if θ then 16/25 else 9/25) else (if θ then 9/25 else 16/25)

def good (θ : Bool) : Finset Bool := {θ}
def live (p : Bool) : Finset Bool := if p then {true} else univ

def acts (p σ : Bool) : List Bool :=
  if p then [true] else if σ then [true,false] else [false]

def stay (p a y : Bool) : Bool := if p then true else if a then !y else true

def next (p σ : Bool) (w : StopObs Bool (acts p σ).length) : Bool :=
  if stopCompleted w then p else true

def rank (p : Bool) : ℕ := if p then 0 else 1

def initial (_p : Bool) : Bool := true

def allowed (p : Bool) : Finset Bool := if p then {true} else univ

lemma law_nonneg : ∀ θ a y, 0 ≤ P θ a y := by
  intro θ a y
  cases θ <;> cases a <;> cases y <;> norm_num [P]

lemma law_normalized : ∀ θ a, ∑ y, P θ a y = 1 := by
  intro θ a
  cases θ <;> cases a <;> norm_num [P, Fintype.sum_bool]

lemma initial_live : ∀ p, initial p ∈ live p := by
  intro p
  cases p <;> simp [initial,live]

lemma phase_certificate : ∀ p σ, σ ∈ live p →
    (∃ a ∈ acts p σ, ∃ y, stay p a y = false ∧ 0 < P σ a y) ∨
    LiveSelfVerifying P good (live p) σ (acts p σ) := by
  intro p σ hσ
  cases p
  · cases σ
    · right
      constructor
      · simp [acts, good]
      · intro η hη heq
        cases η
        · simp [acts, good]
        · have h := congrFun (heq false (by simp [acts])) true
          norm_num [P] at h
    · left
      exact ⟨true, by simp [acts], true, by simp [stay], by norm_num [P]⟩
  · have hs : σ = true := by simpa [live] using hσ
    subst σ
    right
    constructor
    · simp [acts,good]
    · intro η hη _
      have he : η = true := by simpa [live] using hη
      subst η
      simp [acts,good]

lemma zero_model_never_exits : ∀ a y, stay false a y = false → P false a y = 0 := by
  intro a y
  cases a <;> cases y <;> norm_num [stay,P]

lemma final_phase_never_exits (θ : Bool) : ∀ a y, stay true a y = false → P θ a y = 0 := by
  simp [stay]

lemma preserves_true (θ : Bool) : ∀ p σ w, θ ∈ live p → stopCompleted w = false →
    0 < stoppedFullKernel P (acts p) (stay p) θ σ w → θ ∈ live (next p σ w) := by
  intro p σ w hθ hw hp
  cases θ
  · cases p
    · have hz := stoppedMass_zero_of_no_exit (P false) (stay false) zero_model_never_exits
        (acts false σ) w hw
      change 0 < stoppedMass (P false) (stay false) (acts false σ) w at hp
      rw [hz] at hp
      exact (lt_irrefl 0 hp).elim
    · simp [live] at hθ
  · cases hn : next p σ w <;> simp [live]

lemma exit_rank_decreases (θ : Bool) : ∀ p σ w, θ ∈ live p → stopCompleted w = false →
    0 < stoppedFullKernel P (acts p) (stay p) θ σ w → rank (next p σ w) < rank p := by
  intro p σ w _ hw hp
  cases p
  · simp [next,hw,rank]
  · have hz := stoppedMass_zero_of_no_exit (P θ) (stay true) (final_phase_never_exits θ)
      (acts true σ) w hw
    change 0 < stoppedMass (P θ) (stay true) (acts true σ) w at hp
    rw [hz] at hp
    exact (lt_irrefl 0 hp).elim

/-- The same planned block can contain an action forbidden after revelation.
Interruption is required before a new phase, rather than a cosmetic encoding. -/
theorem permission_change_control :
    false ∈ (acts false true).toFinset ∧ false ∉ allowed true := by
  simp [acts,allowed]

theorem all_planned_actions_licensed : ∀ p σ, σ ∈ live p → (acts p σ).toFinset ⊆ allowed p := by
  intro p σ _
  cases p <;> cases σ <;> simp [acts,allowed]

def K (p : Bool) := stoppedFullKernel P (acts p) (stay p)
def keep (p σ : Bool) (w : StopObs Bool (acts p σ).length) := stopCompleted w

def policy (p : Bool) := liveTreeMLE (Obs := fun p σ => StopObs Bool (acts p σ).length) (p := p)
  (continuingKernel K keep p) (live p) (initial p)

lemma full_nonneg : ∀ p η σ y, 0 ≤ K p η σ y := fun p η σ y =>
  stoppedMass_nonneg (P η) (stay p) (law_nonneg η) (acts p σ) y
lemma full_normalized : ∀ p η σ, ∑ y, K p η σ y = 1 := fun p η σ =>
  stoppedMass_normalized (P η) (stay p) (law_normalized η) (acts p σ)

def experiment (θ : Bool) :=
  markovTrajectory (resetTransitionKernel K keep next policy full_nonneg full_normalized θ) ⟨false,[]⟩

/-- Literal zero-support instance with a permission-changing mid-block exit.
The complete infinite observation law is constructed, not postulated. -/
theorem generated_zero_support_eventually_good (θ : Bool) :
    ∀ᵐ x ∂experiment θ, ∀ᶠ n in atTop,
      (acts (x n).1 (policy (x n).1 (x n).2)).toFinset ⊆ good θ := by
  exact generated_live_controller_eventually_good P good live acts stay initial next
    law_nonneg law_normalized initial_live phase_certificate θ rank
    (preserves_true θ) (exit_rank_decreases θ) false (by simp [live])

end Orthemology.Tranche2.ZeroSupportFixture
