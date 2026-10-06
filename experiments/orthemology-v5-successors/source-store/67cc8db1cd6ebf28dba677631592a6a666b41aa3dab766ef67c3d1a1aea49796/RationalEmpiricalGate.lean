import ObservedRowTest

/-! An executable rational-arithmetic specialization of the retained literal
empirical guard. This does not compile the entire phase policy to P02. -/
namespace Orthemology.RuntimeBridge.RationalGate
set_option linter.unusedSectionVars false
open Orthemology.Tranche2.PolicyEmbedding
open HiddenParity HiddenParity.Stochastic HiddenParity.Empirical HiddenParity.Sufficiency
universe u w
variable {State Action : Type u} {Model : Type w}
variable [DecidableEq Model]
variable [Fintype State] [Fintype Action] [DecidableEq State] [DecidableEq Action] [Inhabited State]

def symbolCount (e : State × Action) (y : State) (h : History (State × Action) State) : ℕ :=
  h.countP (fun z => z.1 = e ∧ z.2 = y)

def frequency (e : State × Action) (y : State) (h : History (State × Action) State) : ℚ :=
  (symbolCount e y h : ℚ) / actionCount e h

def reject (P : RationalKernel Model (State × Action) State) (ε : ℚ)
    (θ : Model) (k : ℕ) (h : History (State × Action) State) : Bool :=
  decide (∃ e : State × Action, ∃ y : State,
    k < actionCount e h ∧ ε ≤ |frequency e y h - P.row θ e y|)

theorem count_eq_mass (e : State × Action) (y : State) (h : History (State × Action) State) :
    (symbolCount e y h : ℝ) = historySymbolMass e y h := by
  induction h with
  | nil => simp [symbolCount]
  | cons z h ih =>
      rcases z with ⟨f,t⟩
      by_cases he : f = e <;> by_cases hy : t = y <;>
        simp [symbolCount,List.countP_cons,historySymbolMass_cons,symbolIndicator,he,hy,← ih,add_comm]

theorem frequency_cast (e : State × Action) (y : State) (h : History (State × Action) State) :
    (frequency e y h : ℝ) = historyFrequency e y h := by
  simp [frequency,historyFrequency, count_eq_mass]

/-- Exact equality of Boolean decisions, including empty counts, the phase
count gate and equality at the tolerance boundary. -/
theorem reject_exact (P : RationalKernel Model (State × Action) State) (ε : ℚ)
    (θ : Model) (k : ℕ) (h : History (State × Action) State) :
    reject P ε θ k h = empiricalReject P (ε : ℝ) θ k h := by
  apply Bool.eq_iff_iff.mpr
  rw [empiricalReject_iff]
  simp only [reject,decide_eq_true_eq]
  constructor
  · rintro ⟨e,y,hk,hd⟩
    refine ⟨e,y,hk,?_⟩
    rw [← frequency_cast]
    change (ε : ℝ) ≤ |(frequency e y h : ℝ) - (P.row θ e y : ℝ)|
    exact_mod_cast hd
  · rintro ⟨e,y,hk,hd⟩
    refine ⟨e,y,hk,?_⟩
    rw [← frequency_cast] at hd
    change (ε : ℝ) ≤ |(frequency e y h : ℝ) - (P.row θ e y : ℝ)| at hd
    exact_mod_cast hd

end Orthemology.RuntimeBridge.RationalGate

namespace Orthemology.RuntimeBridge.RationalGate
open Orthemology.Tranche2.PolicyEmbedding
open HiddenParity HiddenParity.Stochastic HiddenParity.Empirical HiddenParity.Sufficiency
universe u w
variable {State Action : Type u} {Model : Type w}
variable [Fintype State] [Fintype Action] [DecidableEq State] [DecidableEq Action] [Inhabited State]
variable [DecidableEq Model]

def gaps (P : RationalKernel Model (State × Action) State) (B : Finset Model) : Finset ℚ :=
  (B ×ˢ B ×ˢ (Finset.univ : Finset (State × Action)) ×ˢ (Finset.univ : Finset State)).image
    (fun z => |P.row z.2.1 z.2.2.1 z.2.2.2 - P.row z.1 z.2.2.1 z.2.2.2|)

def positiveGaps (P : RationalKernel Model (State × Action) State) (B : Finset Model) : Finset ℚ :=
  (gaps P B).filter (fun q => 0 < q)

/-- One literal computable rational tolerance from the finite input rows. -/
def tolerance (P : RationalKernel Model (State × Action) State) (B : Finset Model) : ℚ :=
  if hp : (positiveGaps P B).Nonempty then (positiveGaps P B).min' hp / 2 else 1

theorem positive_gap_member (P : RationalKernel Model (State × Action) State) (B : Finset Model)
    (θ σ : Model) (hθ : θ ∈ B) (hσ : σ ∈ B) (e : State × Action) (y : State)
    (hy : P.row θ e y ≠ P.row σ e y) :
    |P.row σ e y - P.row θ e y| ∈ positiveGaps P B := by
  apply Finset.mem_filter.mpr
  constructor
  · exact Finset.mem_image.mpr ⟨(θ,σ,e,y),by simp [hθ,hσ],rfl⟩
  · exact abs_pos.mpr (sub_ne_zero.mpr hy.symm)

theorem tolerance_spec (P : RationalKernel Model (State × Action) State) (B : Finset Model) :
    0 < tolerance P B ∧ ∀ θ ∈ B, ∀ σ ∈ B, ∀ e, P.row θ e ≠ P.row σ e →
      ∃ y, tolerance P B < |P.row σ e y - P.row θ e y| := by
  by_cases hp : (positiveGaps P B).Nonempty
  · have hmin : 0 < (positiveGaps P B).min' hp :=
      (Finset.mem_filter.mp (Finset.min'_mem (positiveGaps P B) hp)).2
    constructor
    · simp only [tolerance,hp,↓reduceDIte]
      positivity
    · intro θ hθ σ hσ e hrow
      obtain ⟨y,hy⟩ := Function.ne_iff.mp hrow
      have hg := positive_gap_member P B θ σ hθ hσ e y hy
      have hle := Finset.min'_le (positiveGaps P B) _ hg
      refine ⟨y,?_⟩
      simp only [tolerance,hp,↓reduceDIte]
      linarith
  · constructor
    · simp [tolerance,hp]
    · intro θ hθ σ hσ e hrow
      obtain ⟨y,hy⟩ := Function.ne_iff.mp hrow
      exact (hp ⟨_,positive_gap_member P B θ σ hθ hσ e y hy⟩).elim

/-- The executable rational choice satisfies exactly the real separation
contract used by the accepted global sufficiency theorem. -/
theorem tolerance_real_spec (P : RationalKernel Model (State × Action) State) (B : Finset Model) :
    0 < (tolerance P B : ℝ) ∧ ∀ θ ∈ B, ∀ σ ∈ B, ∀ e, P.row θ e ≠ P.row σ e →
      ∃ y, (tolerance P B : ℝ) < |realRows P σ e y - realRows P θ e y| := by
  constructor
  · exact_mod_cast (tolerance_spec P B).1
  · intro θ hθ σ hσ e hrow
    obtain ⟨y,hy⟩ := (tolerance_spec P B).2 θ hθ σ hσ e hrow
    refine ⟨y,?_⟩
    unfold realRows
    exact_mod_cast hy

end Orthemology.RuntimeBridge.RationalGate
