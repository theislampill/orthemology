import StoppedSupportUpdate

noncomputable section
open Finset

namespace Orthemology.Tranche2
variable {Θ A Y : Type*} [DecidableEq Θ] [DecidableEq A]
    (P : Θ → A → Y → ℝ) (good : Θ → Finset A) (menu : Finset Θ → Finset A)

abbrev WinningPhase := {B : Finset Θ // RecursiveWinning P good menu B}

instance winningPhaseFintype [Fintype Θ] : Fintype (WinningPhase P good menu) := Fintype.ofFinite _

def phaseInitial (p : WinningPhase P good menu) : Θ :=
  (recursiveWinning_nonempty P good menu p.property).choose

lemma phaseInitial_mem (p : WinningPhase P good menu) : phaseInitial P good menu p ∈ p.val :=
  (recursiveWinning_nonempty P good menu p.property).choose_spec

def phaseCandidate (p : WinningPhase P good menu) (σ : Θ) : Θ :=
  if σ ∈ p.val then σ else phaseInitial P good menu p

lemma phaseCandidate_mem (p : WinningPhase P good menu) (σ : Θ) : phaseCandidate P good menu p σ ∈ p.val := by
  unfold phaseCandidate
  split_ifs with h
  · exact h
  · exact phaseInitial_mem P good menu p

def phaseActs (p : WinningPhase P good menu) (σ : Θ) : List A :=
  Classical.choose (recursiveWinning_witness P good menu p.property
    (phaseCandidate P good menu p σ) (phaseCandidate_mem P good menu p σ))

lemma phaseActs_spec (p : WinningPhase P good menu) (σ : Θ) :
    phaseActs P good menu p σ ≠ [] ∧
    (phaseActs P good menu p σ).toFinset ⊆ menu p.val ∧
    (∀ a ∈ phaseActs P good menu p σ, ∀ y, (supportUpdate P p.val a y).Nonempty →
      supportUpdate P p.val a y ≠ p.val → RecursiveWinning P good menu (supportUpdate P p.val a y)) ∧
    ((∃ a ∈ phaseActs P good menu p σ, ∃ y, supportStay P p.val a y = false ∧
        0 < P (phaseCandidate P good menu p σ) a y) ∨
      LiveSelfVerifying P good p.val (phaseCandidate P good menu p σ) (phaseActs P good menu p σ)) :=
  Classical.choose_spec (recursiveWinning_witness P good menu p.property
    (phaseCandidate P good menu p σ) (phaseCandidate_mem P good menu p σ))

lemma phaseActs_certificate (p : WinningPhase P good menu) (σ : Θ) (hσ : σ ∈ p.val) :
    (∃ a ∈ phaseActs P good menu p σ, ∃ y, supportStay P p.val a y = false ∧ 0 < P σ a y) ∨
      LiveSelfVerifying P good p.val σ (phaseActs P good menu p σ) := by
  have h := (phaseActs_spec P good menu p σ).2.2.2
  simpa only [phaseCandidate, if_pos hσ] using h

def phaseNext (p : WinningPhase P good menu) (σ : Θ)
    (w : StopObs Y (phaseActs P good menu p σ).length) : WinningPhase P good menu := by
  classical
  exact if h : RecursiveWinning P good menu (stoppedSupport P p.val (phaseActs P good menu p σ) w)
  then ⟨stoppedSupport P p.val (phaseActs P good menu p σ) w,h⟩ else p

/-- The successor is licensed by the recursion whenever the actual exit has
positive probability. Impossible records may use a harmless fallback phase. -/
theorem phaseNext_actual_support (hP : ∀ θ a y, 0 ≤ P θ a y)
    (θ : Θ) (p : WinningPhase P good menu) (σ : Θ)
    (w : StopObs Y (phaseActs P good menu p σ).length)
    (hθ : θ ∈ p.val) (hw : stopCompleted w = false)
    (hp : 0 < stoppedMass (P θ) (supportStay P p.val) (phaseActs P good menu p σ) w) :
    (phaseNext P good menu p σ w).val = stoppedSupport P p.val (phaseActs P good menu p σ) w ∧
    θ ∈ (phaseNext P good menu p σ w).val ∧
    (phaseNext P good menu p σ w).val ⊂ p.val := by
  obtain ⟨a,ha,y,hy,hpos,heq⟩ := stopped_exit_witness P p.val hP θ (phaseActs P good menu p σ) w hw hp
  have hmem : θ ∈ supportUpdate P p.val a y := (mem_supportUpdate P p.val a y θ).mpr ⟨hθ,hpos⟩
  have hne : supportUpdate P p.val a y ≠ p.val := (supportStay_false P p.val a y).mp hy
  have hwin := (phaseActs_spec P good menu p σ).2.2.1 a ha y ⟨θ,hmem⟩ hne
  have hdec : RecursiveWinning P good menu (stoppedSupport P p.val (phaseActs P good menu p σ) w) := by
    rw [heq]
    exact hwin
  have hn : (phaseNext P good menu p σ w).val = supportUpdate P p.val a y := by
    simp only [phaseNext, dif_pos hdec, heq]
  refine ⟨by simpa only [heq] using hn, ?_, ?_⟩
  · simpa only [hn] using hmem
  · rw [hn]
    exact Finset.ssubset_iff_subset_ne.mpr ⟨supportUpdate_subset P p.val a y, hne⟩

def phaseRank (p : WinningPhase P good menu) : ℕ := p.val.card - 1

lemma phaseNext_rank_decreases (hP : ∀ θ a y, 0 ≤ P θ a y)
    (θ : Θ) (p : WinningPhase P good menu) (σ : Θ)
    (w : StopObs Y (phaseActs P good menu p σ).length)
    (hθ : θ ∈ p.val) (hw : stopCompleted w = false)
    (hp : 0 < stoppedMass (P θ) (supportStay P p.val) (phaseActs P good menu p σ) w) :
    phaseRank P good menu (phaseNext P good menu p σ w) < phaseRank P good menu p := by
  have hs := (phaseNext_actual_support P good menu hP θ p σ w hθ hw hp).2.2
  have hc := Finset.card_lt_card hs
  have hn := Finset.card_pos.mpr (recursiveWinning_nonempty P good menu (phaseNext P good menu p σ w).property)
  dsimp [phaseRank]
  omega

end Orthemology.Tranche2
