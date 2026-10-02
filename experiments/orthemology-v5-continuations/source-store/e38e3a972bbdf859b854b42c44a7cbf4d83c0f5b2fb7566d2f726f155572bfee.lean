import ActualTargetPolicy
import ObservedEmpiricalRows

noncomputable section
open MeasureTheory Filter
open Orthemology.Tranche2.PolicyEmbedding Orthemology.Tranche2.RecurrentSupport

namespace HiddenParity.Sufficiency
open HiddenParity.Stochastic HiddenParity.Adaptive HiddenParity.Empirical
universe u v w
variable {State Action : Type u} {R : Type v} {Model : Type w}
variable [Fintype State] [Fintype Action] [DecidableEq State] [DecidableEq Action] [Inhabited State]
variable [DecidableEq Model]

/-- One fixed positive tolerance separates all distinct full rows in a finite
initial model family. The harmless all-identical case needs no separation. -/
theorem finite_row_separation (P : RationalKernel Model (State × Action) State) (B : Finset Model) :
    ∃ ε : ℝ, 0 < ε ∧ ∀ θ ∈ B, ∀ σ ∈ B, ∀ e, P.row θ e ≠ P.row σ e →
      ∃ y, ε < |realRows P σ e y - realRows P θ e y| := by
  classical
  let gaps : Finset ℝ := (B ×ˢ B ×ˢ (Finset.univ : Finset (State × Action)) ×ˢ
    (Finset.univ : Finset State)).image (fun z =>
      |realRows P z.2.1 z.2.2.1 z.2.2.2 - realRows P z.1 z.2.2.1 z.2.2.2|)
  let positive := gaps.filter (fun t => 0 < t)
  by_cases hp : positive.Nonempty
  · let ε := positive.min' hp / 2
    have hmin : 0 < positive.min' hp := (Finset.mem_filter.mp (Finset.min'_mem positive hp)).2
    refine ⟨ε,by dsimp [ε]; positivity,?_⟩
    intro θ hθ σ hσ e hRow
    have hex : ∃ y, P.row θ e y ≠ P.row σ e y := Function.ne_iff.mp hRow
    obtain ⟨y,hy⟩ := hex
    have hd : 0 < |realRows P σ e y - realRows P θ e y| := by
      apply abs_pos.mpr
      apply sub_ne_zero.mpr
      intro heq
      apply hy
      change (P.row σ e y : ℝ) = (P.row θ e y : ℝ) at heq
      exact_mod_cast heq.symm
    have hg : |realRows P σ e y - realRows P θ e y| ∈ positive := by
      apply Finset.mem_filter.mpr
      refine ⟨?_,hd⟩
      apply Finset.mem_image.mpr
      exact ⟨(θ,σ,e,y),by simp [hθ,hσ],rfl⟩
    have hb := Finset.min'_le positive _ hg
    exact ⟨y,by dsimp [ε]; linarith⟩
  · refine ⟨1,by norm_num,?_⟩
    intro θ hθ σ hσ e hRow
    obtain ⟨y,hy⟩ := Function.ne_iff.mp hRow
    exfalso
    apply hp
    refine ⟨|realRows P σ e y - realRows P θ e y|,Finset.mem_filter.mpr ⟨?_,?_⟩⟩
    · exact Finset.mem_image.mpr ⟨(θ,σ,e,y),by simp [gaps,hθ,hσ],rfl⟩
    · apply abs_pos.mpr
      apply sub_ne_zero.mpr
      intro heq
      apply hy
      change (P.row σ e y : ℝ) = (P.row θ e y : ℝ) at heq
      exact_mod_cast heq.symm

/-- Literal causal row test on acquired observed pair/receipt history. Stale
small-count deviations cannot reject arbitrarily late candidate phases. -/
def empiricalReject (P : RationalKernel Model (State × Action) State) (ε : ℝ)
    (θ : Model) (k : ℕ) (h : History (State × Action) State) : Bool :=
  decide (∃ e : State × Action, ∃ y : State,
    k < actionCount e h ∧ ε ≤ |historyFrequency e y h - realRows P θ e y|)

@[simp] theorem empiricalReject_iff (P : RationalKernel Model (State × Action) State) (ε : ℝ)
    (θ : Model) (k : ℕ) (h : History (State × Action) State) :
    empiricalReject P ε θ k h = true ↔ ∃ e : State × Action, ∃ y : State,
      k < actionCount e h ∧ ε ≤ |historyFrequency e y h - realRows P θ e y| := by
  simp [empiricalReject]

end HiddenParity.Sufficiency
