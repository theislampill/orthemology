import AdaptiveRationalCylinders

namespace Orthemology.RationalLaw
open Orthemology.Frontier Orthemology.Frontier.MealyMeasure
variable {H Y : Type*} [DecidableEq Y]

/-- Actual history after k consecutive proposals, including rejected proposals. -/
def proposalState (L D : ℕ) (row : H → Fin D → Y) (update : H → Y → H)
    (h : H) (x : Cantor) : ℕ → H
  | 0 => h
  | k+1 => match sample L D (row (proposalState L D row update h x k)) (block L k x) with
      | none => proposalState L D row update h x k
      | some y => update (proposalState L D row update h x k) y

def proposalReceipt (L D : ℕ) (row : H → Fin D → Y) (update : H → Y → H)
    (h : H) (x : Cantor) (k : ℕ) : Option Y :=
  sample L D (row (proposalState L D row update h x k)) (block L k x)

/-- The first n accepted elements of an actual proposal-output sequence.
Rejects are `none`; they do not extend the observation history. -/
def reports : (n : ℕ) → (Fin n → Y) → (ℕ → Option Y) → Prop
  | 0, _, _ => True
  | n+1, ys, out => ∃ r, (∀ i < r, out i = none) ∧ out r = some (ys 0) ∧
      reports n (fun i => ys i.succ) (fun i => out (r+1+i))

theorem proposalState_add (L D : ℕ) (row : H → Fin D → Y) (update : H → Y → H)
    (h : H) (x : Cantor) (r k : ℕ) :
    proposalState L D row update h x (r+k) =
      proposalState L D row update (proposalState L D row update h x r) (shift (r*L) x) k := by
  induction k with
  | zero => rfl
  | succ k ih =>
      rw [Nat.add_succ, proposalState, proposalState, ih, block_shift]

theorem proposalReceipt_add (L D : ℕ) (row : H → Fin D → Y) (update : H → Y → H)
    (h : H) (x : Cantor) (r k : ℕ) :
    proposalReceipt L D row update h x (r+k) =
      proposalReceipt L D row update (proposalState L D row update h x r) (shift (r*L) x) k := by
  simp only [proposalReceipt, proposalState_add L D row update h x r k, block_shift]

theorem rejected_prefix_state (L D : ℕ) (row : H → Fin D → Y) (update : H → Y → H)
    (h : H) (x : Cantor) (r : ℕ)
    (hr : ∀ i < r, sample L D (row h) (block L i x) = none) :
    ∀ i ≤ r, proposalState L D row update h x i = h := by
  intro i hi
  induction i with
  | zero => rfl
  | succ i ih =>
      have hs := ih (by omega)
      simp only [proposalState, hs, hr i (by omega)]

theorem reported_prefix_state (L D : ℕ) (row : H → Fin D → Y) (update : H → Y → H)
    (h : H) (x : Cantor) (r : ℕ)
    (hr : ∀ i < r, proposalReceipt L D row update h x i = none) :
    ∀ i ≤ r, proposalState L D row update h x i = h := by
  intro i hi
  induction i with
  | zero => rfl
  | succ i ih =>
      have hs := ih (by omega)
      have hh := hr i (by omega)
      change sample L D (row (proposalState L D row update h x i)) (block L i x) = none at hh
      rw [proposalState, hh, hs]

/-- Exact bridge from sequential rejection semantics to the actual proposal outputs. -/
theorem reports_iff_delivers (L D : ℕ) (row : H → Fin D → Y) (update : H → Y → H)
    (n : ℕ) (h : H) (ys : Fin n → Y) (x : Cantor) :
    reports n ys (proposalReceipt L D row update h x) ↔ delivers L D row update n h ys x := by
  induction n generalizing h x with
  | zero => rfl
  | succ n ih =>
      constructor
      · rintro ⟨r,hr,hy,ht⟩
        have hs := reported_prefix_state L D row update h x r hr
        have hr' : ∀ i < r, sample L D (row h) (block L i x) = none := by
          intro i hi
          simpa only [proposalReceipt, hs i (by omega)] using hr i hi
        have hy' : sample L D (row h) (block L r x) = some (ys 0) := by
          simpa only [proposalReceipt, hs r le_rfl] using hy
        have hn : proposalState L D row update h x (r+1) = update h (ys 0) := by
          simp only [proposalState, hs r le_rfl, hy']
        have he : (fun i => proposalReceipt L D row update h x (r+1+i)) =
            proposalReceipt L D row update (update h (ys 0)) (shift ((r+1)*L) x) := by
          funext i
          rw [proposalReceipt_add, hn]
        exact ⟨r,hr',hy',(ih _ _ _).mp (he ▸ ht)⟩
      · rintro ⟨r,hr,hy,ht⟩
        have hs := rejected_prefix_state L D row update h x r hr
        have hn : proposalState L D row update h x (r+1) = update h (ys 0) := by
          simp only [proposalState, hs r le_rfl, hy]
        refine ⟨r, ?_, ?_, ?_⟩
        · intro i hi
          simpa only [proposalReceipt, hs i (by omega)] using hr i hi
        · simpa only [proposalReceipt, hs r le_rfl] using hy
        · have he : (fun i => proposalReceipt L D row update h x (r+1+i)) =
              proposalReceipt L D row update (update h (ys 0)) (shift ((r+1)*L) x) := by
            funext i
            rw [proposalReceipt_add, hn]
          rw [he]
          exact (ih _ _ _).mpr ht


/-- The same report predicate with every exact rejection count retained. -/
def reportsWithCounts : (n : ℕ) → (Fin n → Y) → (Fin n → ℕ) → (ℕ → Option Y) → Prop
  | 0, _, _, _ => True
  | n+1, ys, rs, out => (∀ i < rs 0, out i = none) ∧ out (rs 0) = some (ys 0) ∧
      reportsWithCounts n (fun i => ys i.succ) (fun i => rs i.succ) (fun i => out (rs 0+1+i))

theorem reportsWithCounts_iff_joint (L D : ℕ) (hDB : D ≤ 2^L) (row : H → Fin D → Y)
    (update : H → Y → H) (n : ℕ) (h : H) (ys : Fin n → Y) (rs : Fin n → ℕ) (x : Cantor) :
    reportsWithCounts n ys rs (proposalReceipt L D row update h x) ↔
      x ∈ historyJoint L D hDB row update n h ys rs := by
  induction n generalizing h x with
  | zero => simp [reportsWithCounts, historyJoint, historyConstraints, constraintEvent]
  | succ n ih =>
      rw [historyJoint_succ, firstEvent_iff]
      constructor
      · rintro ⟨hr,hy,ht⟩
        have hs := reported_prefix_state L D row update h x (rs 0) hr
        have hr' : ∀ i < rs 0, sample L D (row h) (block L i x) = none := by
          intro i hi
          simpa only [proposalReceipt, hs i (by omega)] using hr i hi
        have hy' : sample L D (row h) (block L (rs 0) x) = some (ys 0) := by
          simpa only [proposalReceipt, hs (rs 0) le_rfl] using hy
        have hn : proposalState L D row update h x (rs 0+1) = update h (ys 0) := by
          simp only [proposalState, hs (rs 0) le_rfl, hy']
        have he : (fun i => proposalReceipt L D row update h x (rs 0+1+i)) =
            proposalReceipt L D row update (update h (ys 0)) (shift ((rs 0+1)*L) x) := by
          funext i
          rw [proposalReceipt_add, hn]
        refine ⟨⟨fun i hi => (sample_none_iff L D hDB (row h) _).mp (hr' i hi),
          (sample_some_iff L D hDB (row h) _ _).mp hy'⟩, ?_⟩
        exact (ih _ _ _ _).mp (he ▸ ht)
      · rintro ⟨⟨hr,hy⟩,ht⟩
        have hr' : ∀ i < rs 0, sample L D (row h) (block L i x) = none :=
          fun i hi => (sample_none_iff L D hDB (row h) _).mpr (hr i hi)
        have hy' := (sample_some_iff L D hDB (row h) _ _).mpr hy
        have hs := rejected_prefix_state L D row update h x (rs 0) hr'
        have hn : proposalState L D row update h x (rs 0+1) = update h (ys 0) := by
          simp only [proposalState, hs (rs 0) le_rfl, hy']
        refine ⟨?_, ?_, ?_⟩
        · intro i hi
          simpa only [proposalReceipt, hs i (by omega)] using hr' i hi
        · simpa only [proposalReceipt, hs (rs 0) le_rfl] using hy'
        · have he : (fun i => proposalReceipt L D row update h x (rs 0+1+i)) =
              proposalReceipt L D row update (update h (ys 0)) (shift ((rs 0+1)*L) x) := by
            funext i
            rw [proposalReceipt_add, hn]
          rw [he]
          exact (ih _ _ _ _).mpr ht

end Orthemology.RationalLaw
