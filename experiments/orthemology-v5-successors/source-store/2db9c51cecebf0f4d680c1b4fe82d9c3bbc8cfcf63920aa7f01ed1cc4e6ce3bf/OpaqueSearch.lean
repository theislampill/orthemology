import CoveringPortfolio

/-! Adaptive opaque search at the fixed prepared-family interface.
A policy may inspect the entire selected-path/observation history. The only
restriction used for the lower bound is a world-independent failed macro reply.
The reply can contain preparation, cancellation, all allowed timings and nonce.
The physical success predicate is explicitly disjointness from the bad set. -/
namespace CoveringKernel
open Finset
variable {α : Type*} [Fintype α] [DecidableEq α]

abbrev Path (F : Finset (Finset α)) := {P : Finset α // P ∈ F}
abbrev Policy (F : Finset (Finset α)) (O : Type*) :=
  List (Path F × O) → Path F

/-- New attempts have a fresh ordinal n. Histories contain full selected paths
and replies; extending after success is harmless because the cap tests the first hit. -/
def history {F : Finset (Finset α)} {O : Type*} (π : Policy F O)
    (reply : ℕ → Path F → O) : ℕ → List (Path F × O)
  | 0 => []
  | n+1 => let h := history π reply n; (π h, reply n (π h)) :: h

def spine {F : Finset (Finset α)} {O : Type*} (π : Policy F O)
    (failedReply : ℕ → Path F → O) (n : ℕ) : Path F :=
  π (history π failedReply n)

def spinePortfolio {F : Finset (Finset α)} {O : Type*} (π : Policy F O)
    (failedReply : ℕ → Path F → O) (N : ℕ) : Finset (Finset α) :=
  (range N).image (fun i => (spine π failedReply i).val)

/-- Homogeneity is only required on failed paths in candidate maximal worlds.
It does not restrict the reply produced by a successful attempt. -/
def Opaque {F : Finset (Finset α)} {O : Type*} (k : ℕ)
    (observe : Finset α → ℕ → Path F → O) (failedReply : ℕ → Path F → O) : Prop :=
  ∀ T, T.card = k → ∀ n P, ¬Disjoint P.val T → observe T n P = failedReply n P

def SuccessWithin {F : Finset (Finset α)} {O : Type*} (π : Policy F O)
    (observe : Finset α → ℕ → Path F → O) (T : Finset α) (N : ℕ) : Prop :=
  ∃ i < N, Disjoint (π (history π (observe T) i)).val T

omit [Fintype α] [DecidableEq α] in
theorem history_length {F : Finset (Finset α)} {O : Type*} (π : Policy F O)
    (reply : ℕ → Path F → O) (n : ℕ) : (history π reply n).length = n := by
  induction n with
  | zero => rfl
  | succ n ih => simp [history, ih]

omit [Fintype α] [DecidableEq α] in
theorem common_history_of_spine_failure {F : Finset (Finset α)} {O : Type*}
    (π : Policy F O) (observe : Finset α → ℕ → Path F → O)
    (failedReply : ℕ → Path F → O) (T : Finset α)
    (hop : ∀ n P, ¬Disjoint P.val T → observe T n P = failedReply n P)
    (N : ℕ) (hbad : ∀ i < N, ¬Disjoint (spine π failedReply i).val T) :
    history π (observe T) N = history π failedReply N := by
  induction N with
  | zero => rfl
  | succ N ih =>
    have heq := ih (fun i hi => hbad i (by omega))
    simp only [history, heq]
    have hr := hop N _ (hbad N (by omega))
    change observe T N (π (history π failedReply N)) = _ at hr
    rw [hr]
    rfl

omit [Fintype α] [DecidableEq α] in
theorem common_history_of_actual_failure {F : Finset (Finset α)} {O : Type*}
    (π : Policy F O) (observe : Finset α → ℕ → Path F → O)
    (failedReply : ℕ → Path F → O) (T : Finset α)
    (hop : ∀ n P, ¬Disjoint P.val T → observe T n P = failedReply n P)
    (N : ℕ) (hbad : ∀ i < N,
      ¬Disjoint (π (history π (observe T) i)).val T) :
    history π (observe T) N = history π failedReply N := by
  induction N with
  | zero => rfl
  | succ N ih =>
    have heq := ih (fun i hi => hbad i (by omega))
    simp only [history]
    rw [hop N _ (hbad N (by omega)), heq]

omit [Fintype α] in
theorem successWithin_iff_spine {F : Finset (Finset α)} {O : Type*}
    (π : Policy F O) (observe : Finset α → ℕ → Path F → O)
    (failedReply : ℕ → Path F → O) (T : Finset α)
    (hop : ∀ n P, ¬Disjoint P.val T → observe T n P = failedReply n P)
    (N : ℕ) :
    SuccessWithin π observe T N ↔ ∃ P ∈ spinePortfolio π failedReply N, Disjoint P T := by
  classical
  constructor
  · intro hs
    by_contra hn
    have hbad : ∀ i < N, ¬Disjoint (spine π failedReply i).val T := by
      intro i hi hd
      exact hn ⟨_, mem_image.mpr ⟨i, mem_range.mpr hi, rfl⟩, hd⟩
    obtain ⟨i, hi, hd⟩ := hs
    have heq := common_history_of_spine_failure π observe failedReply T hop i
      (fun j hj => hbad j (by omega))
    rw [heq] at hd
    exact hbad i hi hd
  · intro hs
    by_contra hn
    have hbad : ∀ i < N, ¬Disjoint (π (history π (observe T) i)).val T := by
      intro i hi hd
      exact hn ⟨i, hi, hd⟩
    obtain ⟨P, hP, hd⟩ := hs
    obtain ⟨i, hi, rfl⟩ := mem_image.mp hP
    have hiN := mem_range.mp hi
    have heq := common_history_of_actual_failure π observe failedReply T hop i
      (fun j hj => hbad j (by omega))
    apply hbad i hiN
    simpa [heq, spine] using hd

omit [Fintype α] in
theorem cap_iff_spine_available {F : Finset (Finset α)} {O : Type*}
    (π : Policy F O) (observe : Finset α → ℕ → Path F → O)
    (failedReply : ℕ → Path F → O) (k N : ℕ) (hop : Opaque k observe failedReply) :
    (∀ T : Finset α, T.card = k → SuccessWithin π observe T N) ↔
      Available k (spinePortfolio π failedReply N) := by
  constructor
  · intro h T hT
    exact (successWithin_iff_spine π observe failedReply T (hop T hT) N).mp (h T hT)
  · intro h T hT
    exact (successWithin_iff_spine π observe failedReply T (hop T hT) N).mpr (h T hT)

omit [Fintype α] in
theorem spinePortfolio_uniform {F : Finset (Finset α)} {O : Type*}
    (π : Policy F O) (failedReply : ℕ → Path F → O) (q N : ℕ)
    (hu : Uniform q F) : Uniform q (spinePortfolio π failedReply N) := by
  intro P hP
  obtain ⟨i, _, rfl⟩ := mem_image.mp hP
  exact hu _ (spine π failedReply i).property

omit [Fintype α] in
theorem spinePortfolio_card_le {F : Finset (Finset α)} {O : Type*}
    (π : Policy F O) (failedReply : ℕ → Path F → O) (N : ℕ) :
    (spinePortfolio π failedReply N).card ≤ N := by
  simpa [spinePortfolio] using card_image_le (s := range N)
    (f := fun i => (spine π failedReply i).val)

theorem deterministic_cap_lower_bound {F : Finset (Finset α)} {O : Type*}
    (π : Policy F O) (observe : Finset α → ℕ → Path F → O)
    (failedReply : ℕ → Path F → O) (q k N : ℕ)
    (hu : Uniform q F) (hop : Opaque k observe failedReply)
    (hcap : ∀ T : Finset α, T.card = k → SuccessWithin π observe T N) :
    coveringNumber α (Fintype.card α-q) k ≤ N := by
  have hav := (cap_iff_spine_available π observe failedReply k N hop).mp hcap
  exact (coveringNumber_le_portfolio_card q k _
    (spinePortfolio_uniform π failedReply q N hu) hav).trans
      (spinePortfolio_card_le π failedReply N)

/- An available family is nonempty whenever maximal worlds exist. -/
omit [DecidableEq α] in
theorem available_nonempty (k : ℕ) (F : Finset (Finset α))
    (hk : k ≤ Fintype.card α) (ha : Available k F) : F.Nonempty := by
  obtain ⟨T, _, hT⟩ := exists_subset_card_eq
    (show k ≤ (univ : Finset α).card by simpa using hk)
  obtain ⟨P, hP, _⟩ := ha T hT
  exact ⟨P, hP⟩

/-- A prepared portfolio is enumerated once, then repeats an arbitrary member.
This policy has no access to the bad set and ignores all observations. -/
noncomputable def enumeratePolicy (F : Finset (Finset α)) (hne : F.Nonempty)
    (O : Type*) : Policy F O := fun h =>
  if hi : h.length < F.card then F.equivFin.symm ⟨h.length, hi⟩
  else ⟨hne.choose, hne.choose_spec⟩

omit [Fintype α] [DecidableEq α] in
theorem enumeratePolicy_at (F : Finset (Finset α)) (hne : F.Nonempty)
    {O : Type*} (reply : ℕ → Path F → O) (i : Fin F.card) :
    enumeratePolicy F hne O (history (enumeratePolicy F hne O) reply i.val) =
      F.equivFin.symm i := by
  simp [enumeratePolicy, history_length, i.isLt]

omit [Fintype α] [DecidableEq α] in
theorem enumerating_policy_hit (F : Finset (Finset α))
    (hne : F.Nonempty) {O : Type*} (observe : Finset α → ℕ → Path F → O)
    (T : Finset α) (hhit : ∃ P ∈ F, Disjoint P T) :
    SuccessWithin (enumeratePolicy F hne O) observe T F.card := by
  obtain ⟨P, hP, hd⟩ := hhit
  let i : Fin F.card := F.equivFin ⟨P, hP⟩
  refine ⟨i.val, i.isLt, ?_⟩
  rw [enumeratePolicy_at F hne (observe T) i]
  simpa [i] using hd

omit [Fintype α] [DecidableEq α] in
theorem enumerating_policy_cap (k : ℕ) (F : Finset (Finset α))
    (hne : F.Nonempty) (ha : Available k F) {O : Type*}
    (observe : Finset α → ℕ → Path F → O) :
    ∀ T : Finset α, T.card = k →
      SuccessWithin (enumeratePolicy F hne O) observe T F.card := by
  intro T hT
  obtain ⟨P, hP, hd⟩ := ha T hT
  let i : Fin F.card := F.equivFin ⟨P, hP⟩
  refine ⟨i.val, i.isLt, ?_⟩
  rw [enumeratePolicy_at F hne (observe T) i]
  simpa [i] using hd

/-- The covering number is attained by a fixed finite prepared family and a
non-adaptive enumeration, independently of what observations successes return. -/
theorem deterministic_cap_attained (q k : ℕ) (hq : q ≤ Fintype.card α)
    (hk : k ≤ Fintype.card α-q) (O : Type*) :
    ∃ F : Finset (Finset α), Uniform q F ∧
      ∃ π : Policy F O, ∀ observe : Finset α → ℕ → Path F → O,
        ∀ T : Finset α, T.card = k →
          SuccessWithin π observe T (coveringNumber α (Fintype.card α-q) k) := by
  obtain ⟨F, hu, ha, hsize⟩ := minimal_portfolio_attained q k hq hk
  have hne := available_nonempty k F (by omega) ha
  refine ⟨F, hu, enumeratePolicy F hne O, ?_⟩
  intro observe T hT
  rw [← hsize]
  exact enumerating_policy_cap k F hne ha observe T hT

/-- At q=m-k each block is a k-set; no block can cover two distinct maximal worlds. -/
theorem complementary_threshold_exact_cap (k : ℕ) (hk : k ≤ Fintype.card α) :
    coveringNumber α (Fintype.card α-(Fintype.card α-k)) k =
      (Fintype.card α).choose k := by
  rw [Nat.sub_sub_self hk]
  exact coveringNumber_self k hk

/-- Accepted minimum-label specialization, m=3k+1 and q=2k+1. -/
theorem minimum_labels_exact_cap (k : ℕ) (hm : Fintype.card α = 3*k+1) :
    coveringNumber α (Fintype.card α-(2*k+1)) k = (3*k+1).choose k := by
  have hb : Fintype.card α-(2*k+1) = k := by omega
  rw [hb, coveringNumber_self k (by omega), hm]

#print axioms successWithin_iff_spine
#print axioms cap_iff_spine_available
#print axioms deterministic_cap_lower_bound
#print axioms deterministic_cap_attained
#print axioms minimum_labels_exact_cap
end CoveringKernel
