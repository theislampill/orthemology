import CertificateData
import EmpiricalTestLaw

/-! Exact rational empirical testing and a computed positive separation. -/
namespace OrthemicCertificate.Direct
open HiddenParity HiddenParity.Sufficiency HiddenParity.Empirical HiddenParity.Stochastic
open Orthemology.Tranche2.PolicyEmbedding
variable {q n k : ℕ}

/-- Integer acquired count; history is never truncated or reset. -/
def symbolCount (e : Pair n k) (y : Fin n) : History (Pair n k) (Fin n) → ℕ
  | [] => 0
  | (f,z) :: h => (if f = e ∧ z = y then 1 else 0) + symbolCount e y h

def rationalFrequency (e : Pair n k) (y : Fin n) (h : History (Pair n k) (Fin n)) : ℚ :=
  (symbolCount e y h : ℚ) / (actionCount e h : ℚ)

def rationalReject (I : Input q n k) (ε : ℚ) (θ : Fin q) (r : ℕ)
    (h : History (Pair n k) (Fin n)) : Bool :=
  decide (∃ e : Pair n k, ∃ y : Fin n,
    r < actionCount e h ∧ ε ≤ |rationalFrequency e y h - I.row θ e y|)

@[simp] theorem rationalReject_iff (I : Input q n k) (ε : ℚ) (θ : Fin q) (r : ℕ)
    (h : History (Pair n k) (Fin n)) : rationalReject I ε θ r h = true ↔
    ∃ e : Pair n k, ∃ y : Fin n,
      r < actionCount e h ∧ ε ≤ |rationalFrequency e y h - I.row θ e y| := by
  simp [rationalReject]

/-- Only actual positive coordinate gaps from the initial live support occur. -/
def positiveGaps (I : Input q n k) (B : Support q) : Finset ℚ :=
  ((B ×ˢ B ×ˢ (Finset.univ : Finset (Pair n k)) ×ˢ (Finset.univ : Finset (Fin n))).image
    (fun z => |I.row z.2.1 z.2.2.1 z.2.2.2 - I.row z.1 z.2.2.1 z.2.2.2|)).filter (fun x => 0 < x)

def tolerance (I : Input q n k) (B : Support q) : ℚ :=
  if h : (positiveGaps I B).Nonempty then (positiveGaps I B).min' h / 2 else 1

theorem tolerance_positive (I : Input q n k) (B : Support q) : 0 < tolerance I B := by
  unfold tolerance
  split_ifs with hp
  · have hmin := (Finset.mem_filter.mp (Finset.min'_mem (positiveGaps I B) hp)).2
    positivity
  · norm_num

theorem tolerance_separates (I : Input q n k) (B : Support q) :
    ∀ θ ∈ B, ∀ σ ∈ B, ∀ e, I.row θ e ≠ I.row σ e →
      ∃ y, tolerance I B < |I.row σ e y - I.row θ e y| := by
  intro θ hθ σ hσ e hrow
  obtain ⟨y,hy⟩ := Function.ne_iff.mp hrow
  have hd : 0 < |I.row σ e y - I.row θ e y| := abs_pos.mpr (sub_ne_zero.mpr (Ne.symm hy))
  have hg : |I.row σ e y - I.row θ e y| ∈ positiveGaps I B := by
    apply Finset.mem_filter.mpr
    refine ⟨?_,hd⟩
    exact Finset.mem_image.mpr ⟨(θ,σ,e,y),by simp [hθ,hσ],rfl⟩
  have hp : (positiveGaps I B).Nonempty := ⟨_,hg⟩
  have hmin : 0 < (positiveGaps I B).min' hp :=
    (Finset.mem_filter.mp (Finset.min'_mem (positiveGaps I B) hp)).2
  have hb := Finset.min'_le (positiveGaps I B) _ hg
  refine ⟨y,?_⟩
  rw [tolerance,dif_pos hp]
  linarith

section Correspondence
variable [NeZero n]

theorem symbolCount_cast (e : Pair n k) (y : Fin n) (h : History (Pair n k) (Fin n)) :
    (symbolCount e y h : ℝ) = historySymbolMass e y h := by
  induction h with
  | nil => simp [symbolCount]
  | cons z h ih =>
    rcases z with ⟨f,z⟩
    simp only [symbolCount,Nat.cast_add,historySymbolMass_cons,← ih,symbolIndicator]
    by_cases he : f = e <;> by_cases hz : z = y <;> simp [he,hz]

theorem rationalFrequency_cast (e : Pair n k) (y : Fin n) (h : History (Pair n k) (Fin n)) :
    (rationalFrequency e y h : ℝ) = historyFrequency e y h := by
  simp only [rationalFrequency,Rat.cast_div,Rat.cast_natCast,historyFrequency,symbolCount_cast]

/-- Pointwise equality for every history, including zero counts and malformed
unreachable histories. There is no hidden-model or real-comparison oracle. -/
theorem rationalReject_eq_empiricalReject (I : Input q n k) (hI : I.Valid) (ε : ℚ)
    (θ : Fin q) (r : ℕ) (h : History (Pair n k) (Fin n)) :
    rationalReject I ε θ r h = empiricalReject (I.kernel hI) (ε : ℝ) θ r h := by
  apply Bool.eq_iff_iff.mpr
  rw [rationalReject_iff,empiricalReject_iff]
  constructor
  · rintro ⟨e,y,hc,hd⟩
    refine ⟨e,y,hc,?_⟩
    rw [← rationalFrequency_cast]
    change (ε : ℝ) ≤ |(rationalFrequency e y h : ℝ) - (I.row θ e y : ℝ)|
    exact_mod_cast hd
  · rintro ⟨e,y,hc,hd⟩
    refine ⟨e,y,hc,?_⟩
    rw [← rationalFrequency_cast] at hd
    change (ε : ℝ) ≤ |(rationalFrequency e y h : ℝ) - (I.row θ e y : ℝ)| at hd
    exact_mod_cast hd

theorem tolerance_real_separates (I : Input q n k) (hI : I.Valid) (B : Support q)
    (σ : Fin q) (hσ : σ ∈ B) : ∀ θ ∈ B, ∀ e,
    (I.kernel hI).row θ e ≠ (I.kernel hI).row σ e →
      ∃ y, (tolerance I B : ℝ) <
        |realRows (I.kernel hI) σ e y - realRows (I.kernel hI) θ e y| := by
  intro θ hθ e hrow
  obtain ⟨y,hy⟩ := tolerance_separates I B θ hθ σ hσ e hrow
  refine ⟨y,?_⟩
  change (tolerance I B : ℝ) < |(I.row σ e y : ℝ) - (I.row θ e y : ℝ)|
  exact_mod_cast hy

end Correspondence
end OrthemicCertificate.Direct
