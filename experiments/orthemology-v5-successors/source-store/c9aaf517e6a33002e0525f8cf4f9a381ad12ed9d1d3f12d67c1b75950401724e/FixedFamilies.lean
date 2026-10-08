import Availability

namespace AttributionKernel
open Finset
variable {α : Type*} [Fintype α] [DecidableEq α]

def FixedFamilyContract (B c : ℕ) (F G : Set (Finset α)) : Prop :=
  Available B c F ∧ Available B c G ∧
    ∀ P ∈ F, ∀ R ∈ G, Robust B c P R

def LabelFamilyContract (k : ℕ) (F G : Set (Finset α)) : Prop :=
  LabelAvailable k F ∧ LabelAvailable k G ∧
    ∀ P ∈ F, ∀ R ∈ G, k < (P ∩ R).card

omit [DecidableEq α] in
theorem label_available_at_most (k : ℕ) (hk : k ≤ Fintype.card α)
    (F : Set (Finset α)) (hav : LabelAvailable k F)
    (T : Finset α) (hT : T.card ≤ k) :
    ∃ P ∈ F, Disjoint P T := by
  obtain ⟨U, hTU, _hU, hUk⟩ := exists_subsuperset_card_eq
    (subset_univ T) hT (by simpa using hk : k ≤ (univ : Finset α).card)
  obtain ⟨P, hPF, hd⟩ := hav U hUk
  exact ⟨P, hPF, hd.mono_right hTU⟩

theorem label_fixed_family_lower (k : ℕ) (hk : k ≤ Fintype.card α)
    (F G : Set (Finset α)) (h : LabelFamilyContract k F G) :
    3*k+1 ≤ Fintype.card α := by
  obtain ⟨T, _hTU, hTk⟩ := exists_subset_card_eq
    (by simpa using hk : k ≤ (univ : Finset α).card)
  obtain ⟨P, hPF, hPT⟩ := h.1 T hTk
  have hPm : P.card + k ≤ Fintype.card α := by
    have hm := card_le_univ (s := P ∪ T)
    rw [card_union_of_disjoint hPT, hTk] at hm
    exact hm
  obtain ⟨U, hUP, hUcard⟩ := exists_subset_card_eq (min_le_right k P.card)
  obtain ⟨R, hRG, hRU⟩ := label_available_at_most k hk G h.2.1 U (by omega)
  have hsmall : P ∩ R ⊆ P \ U := by
    intro i hi
    obtain ⟨hiP, hiR⟩ := mem_inter.mp hi
    exact mem_sdiff.mpr ⟨hiP, fun hiU => disjoint_left.mp hRU hiR hiU⟩
  have hiCard := card_le_card hsmall
  rw [card_sdiff hUP, hUcard] at hiCard
  have hsafe := h.2.2 P hPF R hRG
  omega

def thresholdFamily (q : ℕ) : Set (Finset α) := {P | P.card = q}

theorem label_threshold_upper (k : ℕ) (hm : 3*k+1 ≤ Fintype.card α) :
    LabelFamilyContract k
      (thresholdFamily (α := α) (Fintype.card α-k)) (thresholdFamily (α := α) (Fintype.card α-k)) := by
  have hav : LabelAvailable k (thresholdFamily (Fintype.card α-k) : Set (Finset α)) := by
    intro T hTk
    refine ⟨univ \ T, ?_, ?_⟩
    · change (univ \ T).card = Fintype.card α-k
      rw [card_sdiff (subset_univ T), card_univ, hTk]
    · exact sdiff_disjoint
  refine ⟨hav, hav, ?_⟩
  intro P hP R hR
  change P.card = Fintype.card α-k at hP
  change R.card = Fintype.card α-k at hR
  have hunion := card_le_univ (s := P ∪ R)
  have hsum := card_union_add_card_inter P R
  omega

theorem label_fixed_family_feasible_iff (k : ℕ) (hk : k ≤ Fintype.card α) :
    (∃ F G : Set (Finset α), LabelFamilyContract k F G) ↔
      3*k+1 ≤ Fintype.card α := by
  constructor
  · rintro ⟨F, G, h⟩
    exact label_fixed_family_lower k hk F G h
  · intro hm
    exact ⟨_, _, label_threshold_upper k hm⟩

theorem fixed_contract_iff (B c : ℕ) (hB : 1 ≤ B) (hc : 1 ≤ c)
    (hcm : c ≤ Fintype.card α) (hk : B+c-1 ≤ Fintype.card α)
    (F G : Set (Finset α)) :
    FixedFamilyContract B c F G ↔ LabelFamilyContract (B+c-1) F G := by
  simp only [FixedFamilyContract, LabelFamilyContract,
    available_iff B c hB hc hcm hk, robust_iff B c hB hc hcm]
  have hsum : B+c-1+1 = B+c := by omega
  simp only [← Nat.succ_le_iff, Nat.succ_eq_add_one, hsum]

theorem fixed_family_feasible_iff (B c : ℕ) (hB : 1 ≤ B) (hc : 1 ≤ c)
    (hcm : c ≤ Fintype.card α) (hBn : B < Fintype.card α-c+1) :
    (∃ F G : Set (Finset α), FixedFamilyContract B c F G) ↔
      3*(B+c-1)+1 ≤ Fintype.card α := by
  have hk : B+c-1 ≤ Fintype.card α := by omega
  simp only [fixed_contract_iff B c hB hc hcm hk]
  exact label_fixed_family_feasible_iff (B+c-1) hk

#print axioms label_fixed_family_lower
#print axioms label_threshold_upper
#print axioms fixed_contract_iff
#print axioms fixed_family_feasible_iff

end AttributionKernel
