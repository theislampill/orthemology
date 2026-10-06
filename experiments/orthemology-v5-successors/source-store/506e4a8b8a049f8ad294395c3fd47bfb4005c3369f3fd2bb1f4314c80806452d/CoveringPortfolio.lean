import Mathlib

/-! Generic finite-universe covering/portfolio correspondence. No physical
success, mapping discovery, or probabilistic conclusion is hidden in definitions. -/
namespace CoveringKernel
open Finset
variable {α : Type*} [Fintype α] [DecidableEq α]

def Uniform (q : ℕ) (F : Finset (Finset α)) : Prop :=
  ∀ P ∈ F, P.card = q

def Available (k : ℕ) (F : Finset (Finset α)) : Prop :=
  ∀ T : Finset α, T.card = k → ∃ P ∈ F, Disjoint P T

def Covers (k : ℕ) (G : Finset (Finset α)) : Prop :=
  ∀ T : Finset α, T.card = k → ∃ A ∈ G, T ⊆ A

def complements (F : Finset (Finset α)) : Finset (Finset α) :=
  F.image (fun P => Pᶜ)

theorem disjoint_iff_subset_compl (P T : Finset α) :
    Disjoint P T ↔ T ⊆ Pᶜ := by
  simp only [Finset.disjoint_left, subset_iff, mem_compl]
  constructor
  · intro h i hiT hiP
    exact h hiP hiT
  · intro h i hiP hiT
    exact h hiT hiP

theorem complement_portfolio_iff (k : ℕ) (F : Finset (Finset α)) :
    Available k F ↔ Covers k (complements F) := by
  constructor
  · intro hav T hT
    obtain ⟨P, hP, hd⟩ := hav T hT
    exact ⟨Pᶜ, mem_image.mpr ⟨P, hP, rfl⟩,
      (disjoint_iff_subset_compl P T).mp hd⟩
  · intro hcov T hT
    obtain ⟨A, hA, hsub⟩ := hcov T hT
    obtain ⟨P, hP, rfl⟩ := mem_image.mp hA
    exact ⟨P, hP, (disjoint_iff_subset_compl P T).mpr hsub⟩

theorem complement_involutive (F : Finset (Finset α)) :
    complements (complements F) = F := by
  simp [complements, image_image, Function.comp_def]

theorem complement_card (F : Finset (Finset α)) :
    (complements F).card = F.card := by
  exact card_image_of_injective F (fun _ _ h => compl_injective h)

theorem complement_uniform (q : ℕ) (F : Finset (Finset α))
    (hu : Uniform q F) : Uniform (Fintype.card α - q) (complements F) := by
  intro A hA
  obtain ⟨P, hP, rfl⟩ := mem_image.mp hA
  simpa [hu P hP] using card_compl P

theorem portfolio_cover_sizes_iff (q k t : ℕ) (hq : q ≤ Fintype.card α) :
    (∃ F : Finset (Finset α), Uniform q F ∧ Available k F ∧ F.card = t) ↔
    (∃ G : Finset (Finset α), Uniform (Fintype.card α-q) G ∧
      Covers k G ∧ G.card = t) := by
  constructor
  · rintro ⟨F, hu, ha, ht⟩
    exact ⟨complements F, complement_uniform q F hu,
      (complement_portfolio_iff k F).mp ha, (complement_card F).trans ht⟩
  · rintro ⟨G, hu, hc, ht⟩
    have huni := complement_uniform (Fintype.card α-q) G hu
    have hqq : Fintype.card α - (Fintype.card α-q) = q := by omega
    rw [hqq] at huni
    refine ⟨complements G, huni, ?_, (complement_card G).trans ht⟩
    apply (complement_portfolio_iff k (complements G)).mpr
    simpa [complement_involutive] using hc

/-- Covering number on a labelled finite universe. Infeasible parameters use
Nat's empty infimum convention; all attainment/optimality theorems state feasibility. -/
noncomputable def coveringNumber (α : Type*) [Fintype α] [DecidableEq α]
    (b k : ℕ) : ℕ :=
  sInf {t | ∃ G : Finset (Finset α), Uniform b G ∧ Covers k G ∧ G.card = t}

noncomputable def leastPortfolioSize (α : Type*) [Fintype α] [DecidableEq α]
    (q k : ℕ) : ℕ :=
  sInf {t | ∃ F : Finset (Finset α), Uniform q F ∧ Available k F ∧ F.card = t}

theorem least_portfolio_eq_coveringNumber (q k : ℕ) (hq : q ≤ Fintype.card α) :
    leastPortfolioSize α q k = coveringNumber α (Fintype.card α-q) k := by
  unfold leastPortfolioSize coveringNumber
  congr 1
  ext t
  exact portfolio_cover_sizes_iff q k t hq

omit [DecidableEq α] in
theorem all_blocks_cover (b k : ℕ) (hb : b ≤ Fintype.card α) (hk : k ≤ b) :
    Uniform b ((univ : Finset α).powersetCard b) ∧
      Covers k ((univ : Finset α).powersetCard b) := by
  constructor
  · intro A hA
    exact (mem_powersetCard.mp hA).2
  · intro T hT
    obtain ⟨A, hTA, hAU, hAb⟩ := exists_subsuperset_card_eq
      (subset_univ T) (show T.card ≤ b by omega)
      (show b ≤ (univ : Finset α).card by simpa using hb)
    exact ⟨A, mem_powersetCard.mpr ⟨hAU, hAb⟩, hTA⟩

theorem coveringNumber_attained (b k : ℕ) (hb : b ≤ Fintype.card α)
    (hk : k ≤ b) :
    ∃ G : Finset (Finset α), Uniform b G ∧ Covers k G ∧
      G.card = coveringNumber α b k := by
  change sInf {t | ∃ G : Finset (Finset α), Uniform b G ∧ Covers k G ∧ G.card = t} ∈
    {t | ∃ G : Finset (Finset α), Uniform b G ∧ Covers k G ∧ G.card = t}
  apply Nat.sInf_mem
  obtain ⟨hu, hc⟩ := all_blocks_cover (α := α) b k hb hk
  exact ⟨_, ⟨_, hu, hc, rfl⟩⟩

theorem coveringNumber_le_card (b k : ℕ) (G : Finset (Finset α))
    (hu : Uniform b G) (hc : Covers k G) :
    coveringNumber α b k ≤ G.card :=
  Nat.sInf_le ⟨G, hu, hc, rfl⟩

theorem coveringNumber_le_portfolio_card (q k : ℕ) (F : Finset (Finset α))
    (hu : Uniform q F) (ha : Available k F) :
    coveringNumber α (Fintype.card α-q) k ≤ F.card := by
  simpa [complement_card] using coveringNumber_le_card
    (Fintype.card α-q) k (complements F) (complement_uniform q F hu)
    ((complement_portfolio_iff k F).mp ha)

theorem minimal_portfolio_attained (q k : ℕ) (hq : q ≤ Fintype.card α)
    (hk : k ≤ Fintype.card α-q) :
    ∃ F : Finset (Finset α), Uniform q F ∧ Available k F ∧
      F.card = coveringNumber α (Fintype.card α-q) k := by
  apply (portfolio_cover_sizes_iff q k _ hq).mpr
  exact coveringNumber_attained _ _ (Nat.sub_le _ _) hk

omit [DecidableEq α] in
theorem self_blocks_forced (k : ℕ) (G : Finset (Finset α))
    (hu : Uniform k G) (hc : Covers k G) :
    G = (univ : Finset α).powersetCard k := by
  apply Subset.antisymm
  · intro A hA
    exact mem_powersetCard.mpr ⟨subset_univ A, hu A hA⟩
  · intro T hT
    have hTk := (mem_powersetCard.mp hT).2
    obtain ⟨A, hA, hTA⟩ := hc T hTk
    have heq : T = A := eq_of_subset_of_card_le hTA (by rw [hu A hA, hTk])
    simpa [heq] using hA

theorem coveringNumber_self (k : ℕ) (hk : k ≤ Fintype.card α) :
    coveringNumber α k k = (Fintype.card α).choose k := by
  obtain ⟨G, hu, hc, hsize⟩ := coveringNumber_attained k k hk le_rfl
  rw [self_blocks_forced k G hu hc] at hsize
  simpa using hsize.symm

#print axioms complement_portfolio_iff
#print axioms portfolio_cover_sizes_iff
#print axioms least_portfolio_eq_coveringNumber
#print axioms coveringNumber_attained
#print axioms coveringNumber_le_portfolio_card
#print axioms coveringNumber_self
end CoveringKernel
