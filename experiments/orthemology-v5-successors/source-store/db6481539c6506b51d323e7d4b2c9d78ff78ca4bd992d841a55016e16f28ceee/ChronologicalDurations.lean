import ChronologicalIntervals
import GeometricIntervalMoment

noncomputable section
attribute [local instance] Classical.propDecidable
open scoped BigOperators
namespace HiddenParity.Cost

/-- Length of one dangerous chronological slot in a finite physical horizon.
Safe slots have length zero, however long their physical residence. -/
def slotLength (progress danger : ℕ → Prop) (T j : ℕ) : ℕ :=
  ((Finset.range T).filter (fun t => progressCount progress t=j ∧ danger t)).card

theorem progressCount_at_lastStart (progress : ℕ → Prop) (t : ℕ) :
    progressCount progress (lastIntervalStart progress t)=progressCount progress t := by
  induction t with
  | zero => rfl
  | succ t ih =>
      by_cases h : progress t
      · simp only [lastIntervalStart,if_pos h]
      · simpa only [lastIntervalStart,if_neg h,progressCount_succ,add_zero] using ih

/-- At a genuine chronological start, all earlier action times have strictly
smaller indices. This is what makes previous slot lengths known at the start. -/
theorem progressCount_lt_at_start (progress : ℕ → Prop) (s t : ℕ)
    (hs : s=0 ∨ progress (s-1)) (ht : t < s) : progressCount progress t < progressCount progress s := by
  cases s with
  | zero => omega
  | succ s =>
      have hp : progress s := by simpa using hs
      have hm := progressCount_mono progress (show t ≤ s by omega)
      rw [progressCount_succ,if_pos hp]
      omega

theorem slot_member_after_start (progress danger : ℕ → Prop) (T j s t : ℕ)
    (hs : s=0 ∨ progress (s-1)) (hj : progressCount progress s=j)
    (ht : t ∈ (Finset.range T).filter (fun t => progressCount progress t=j ∧ danger t)) : s ≤ t := by
  by_contra h
  have hh := progressCount_lt_at_start progress s t hs (by omega)
  have he := (Finset.mem_filter.mp ht).2.1
  omega

/-- A long finite slot contains a time at least n steps after its genuine start;
no bound on the preceding physical time or safe skipped residence is used. -/
theorem far_time_of_slotLength_gt (progress danger : ℕ → Prop) (T j s n : ℕ)
    (hs : s=0 ∨ progress (s-1)) (hj : progressCount progress s=j)
    (hl : n < slotLength progress danger T j) :
    ∃ t,t < T ∧ progressCount progress t=j ∧ danger t ∧ s+n ≤ t := by
  by_contra hn
  push_neg at hn
  have hsub : (Finset.range T).filter (fun t => progressCount progress t=j ∧ danger t)⊆Finset.Ico s (s+n) := by
    intro t ht
    obtain ⟨htT,hidx,hd⟩ := Finset.mem_filter.mp ht
    exact Finset.mem_Ico.mpr ⟨slot_member_after_start progress danger T j s t hs hj ht,
      hn t (Finset.mem_range.mp htT) hidx hd⟩
  have hc := Finset.card_le_card hsub
  simp only [Nat.card_Ico,Nat.add_sub_cancel_left] at hc
  exact (not_lt_of_ge hc) hl

/-- A preceding slot's whole truncated length is already determined by the
history at a later start, provided that start is within the truncation. -/
theorem preceding_slotLength_eq_prefix (progress danger : ℕ → Prop) (T j s i : ℕ)
    (hsT : s ≤ T) (hj : progressCount progress s=j) (hij : i < j) :
    slotLength progress danger T i=slotLength progress danger s i := by
  unfold slotLength
  congr 1
  ext t
  simp only [Finset.mem_filter,Finset.mem_range]
  constructor
  · rintro ⟨ht,hidx,hd⟩
    refine ⟨?_,hidx,hd⟩
    by_contra hn
    have hm := progressCount_mono progress (show s ≤ t by omega)
    omega
  · rintro ⟨ht,hidx,hd⟩
    exact ⟨lt_of_lt_of_le ht hsT,hidx,hd⟩

/-- The long-slot witness has no progress over the required first block, ready
to be bound to the literal generated continuing-slice predicate. -/
theorem no_progress_of_long_slot (progress danger : ℕ → Prop) (T j s n : ℕ)
    (hs : s=0 ∨ progress (s-1)) (hj : progressCount progress s=j)
    (hl : n < slotLength progress danger T j) :
    s+n < T ∧ ∀ i,s ≤ i → i < s+n → ¬progress i := by
  obtain ⟨t,ht,hidx,hd,hfar⟩ := far_time_of_slotLength_gt progress danger T j s n hs hj hl
  have hst : s ≤ t := by omega
  have he := progressCount_eq_implies_same_start progress hst (hj.trans hidx.symm)
  rw [lastIntervalStart_eq_self_of_start progress s hs] at he
  refine ⟨by omega,?_⟩
  intro i his hin
  apply no_progress_since_start progress t i
  · rw [← he];exact his
  · omega

end HiddenParity.Cost
