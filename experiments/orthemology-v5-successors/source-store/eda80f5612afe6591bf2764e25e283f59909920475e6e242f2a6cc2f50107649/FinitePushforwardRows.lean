import FiniteChainHitting

noncomputable section
open scoped BigOperators
namespace HiddenParity.Cost.FiniteChainHitting
variable {Q Y : Type*} [Fintype Q] [DecidableEq Q] [Fintype Y]

def pushRows (w : Q → Y → ℝ) (hw : ∀ q y, 0 ≤ w q y)
    (hn : ∀ q, ∑ y, w q y=1) (next : Q → Y → Q) : Rows Q where
  row q q' := ∑ y, if next q y=q' then w q y else 0
  nonneg q q' := Finset.sum_nonneg (fun y _ => by change 0 ≤ (if next q y=q' then w q y else 0); split_ifs <;> [exact hw q y; exact le_rfl])
  normalized q := by
    rw [Finset.sum_comm]
    simpa only [Finset.sum_ite_eq,Finset.mem_univ,if_true] using hn q

/-- Positive mass in a deterministic finite update is exactly a positive
receipt mapped to that successor; multiple receipts may merge. -/
theorem pushRows_positive_iff (w : Q → Y → ℝ) (hw : ∀ q y, 0 ≤ w q y)
    (hn : ∀ q, ∑ y, w q y=1) (next : Q → Y → Q) (q q' : Q) :
    0 < (pushRows w hw hn next).row q q' ↔ ∃ y, 0 < w q y ∧ next q y=q' := by
  change 0 < ∑ y, (if next q y=q' then w q y else 0) ↔ _
  constructor
  · intro hpos
    by_contra hnone
    push_neg at hnone
    have hsum : (∑ y, if next q y=q' then w q y else 0) ≤ 0 := by
      apply Finset.sum_nonpos
      intro y _
      by_cases he : next q y=q'
      · rw [if_pos he]
        by_contra h
        exact hnone y (by linarith) he
      · rw [if_neg he]
    linarith
  · rintro ⟨y,hy,he⟩
    have hle : (if next q y=q' then w q y else 0) ≤ ∑ y, if next q y=q' then w q y else 0 :=
      Finset.single_le_sum (f:=fun y => if next q y=q' then w q y else 0)
        (fun y _ => by change 0 ≤ (if next q y=q' then w q y else 0); split_ifs <;> [exact hw q y; exact le_rfl]) (Finset.mem_univ y)
    rw [if_pos he] at hle
    exact hy.trans_le hle

/-- Merging positive receipts never lowers the least positive edge mass. -/
theorem pushRows_min_positive (w : Q → Y → ℝ) (hw : ∀ q y, 0 ≤ w q y)
    (hn : ∀ q, ∑ y, w q y=1) (next : Q → Y → Q) (p : ℝ)
    (hmin : ∀ q y, 0 < w q y → p ≤ w q y) :
    ∀ q q', 0 < (pushRows w hw hn next).row q q' → p ≤ (pushRows w hw hn next).row q q' := by
  intro q q' hpos
  obtain ⟨y,hy,he⟩ := (pushRows_positive_iff w hw hn next q q').mp hpos
  apply (hmin q y hy).trans
  change w q y ≤ ∑ y, if next q y=q' then w q y else 0
  have hterm : w q y = if next q y=q' then w q y else 0 := by rw [if_pos he]
  rw [hterm]
  exact Finset.single_le_sum (f:=fun y => if next q y=q' then w q y else 0)
    (fun y _ => by change 0 ≤ (if next q y=q' then w q y else 0); split_ifs <;> [exact hw q y; exact le_rfl]) (Finset.mem_univ y)

theorem pushRows_constant (w : Q → Y → ℝ) (hw : ∀ q y, 0 ≤ w q y)
    (hn : ∀ q, ∑ y, w q y=1) (next : Q → Y → Q) (q q' : Q)
    (hnext : ∀ y, next q y=q') : (pushRows w hw hn next).row q q'=1 := by
  change (∑ y, if next q y=q' then w q y else 0)=1
  simpa only [hnext,ite_true] using hn q

end HiddenParity.Cost.FiniteChainHitting
