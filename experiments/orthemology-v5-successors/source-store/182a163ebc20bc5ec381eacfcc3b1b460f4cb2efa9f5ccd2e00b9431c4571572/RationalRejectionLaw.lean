import FairBlockConstraints

/-! Literal rational rejection on the fair infinite bit tape. -/
namespace Orthemology.RationalLaw
open MeasureTheory Set
open scoped ENNReal BigOperators
open Orthemology.Frontier Orthemology.Frontier.MealyMeasure
open P02A2.Q8Measure (fairCantor)

/-- The first acquired bit is the most significant bit. This is an executable equivalence. -/
def code (L : ℕ) : Mealy.Block L ≃ Fin (2^L) :=
  (Equiv.arrowCongr Fin.revPerm finTwoEquiv.symm).trans finFunctionFinEquiv

def acceptedBlocks (L D : ℕ) (hDB : D ≤ 2^L) : Finset (Mealy.Block L) :=
  Finset.univ.image (fun i : Fin D => (code L).symm (Fin.castLE hDB i))

def rejectedBlocks (L D : ℕ) (hDB : D ≤ 2^L) : Finset (Mealy.Block L) :=
  Finset.univ \ acceptedBlocks L D hDB

variable {Y : Type*} [DecidableEq Y]

/-- A finite deterministic allocation table; no distribution is supplied as a premise. -/
def receiptBlocks (L D : ℕ) (hDB : D ≤ 2^L) (decode : Fin D → Y) (y : Y) :
    Finset (Mealy.Block L) :=
  (Finset.univ.filter (fun i => decode i = y)).image
    (fun i : Fin D => (code L).symm (Fin.castLE hDB i))

def weight (D : ℕ) (decode : Fin D → Y) (y : Y) : ℕ :=
  (Finset.univ.filter (fun i => decode i = y)).card

theorem mem_acceptedBlocks (L D : ℕ) (hDB : D ≤ 2^L) (w : Mealy.Block L) :
    w ∈ acceptedBlocks L D hDB ↔ (code L w).val < D := by
  simp only [acceptedBlocks, Finset.mem_image, Finset.mem_univ, true_and]
  constructor
  · rintro ⟨i, rfl⟩
    simpa using i.isLt
  · intro h
    refine ⟨⟨(code L w).val,h⟩, ?_⟩
    exact (code L).symm_apply_eq.mpr (Fin.ext rfl)

theorem mem_rejectedBlocks (L D : ℕ) (hDB : D ≤ 2^L) (w : Mealy.Block L) :
    w ∈ rejectedBlocks L D hDB ↔ D ≤ (code L w).val := by
  simp [rejectedBlocks, mem_acceptedBlocks]

theorem card_acceptedBlocks (L D : ℕ) (hDB : D ≤ 2^L) :
    (acceptedBlocks L D hDB).card = D := by
  rw [acceptedBlocks, Finset.card_image_of_injective]
  · exact Finset.card_fin D
  · exact (code L).symm.injective.comp (Fin.castLE_injective hDB)

theorem card_rejectedBlocks (L D : ℕ) (hDB : D ≤ 2^L) :
    (rejectedBlocks L D hDB).card = 2^L-D := by
  rw [rejectedBlocks, Finset.card_sdiff (Finset.subset_univ _), card_acceptedBlocks]
  simp [Mealy.Block, Fintype.card_fun]

theorem card_receiptBlocks (L D : ℕ) (hDB : D ≤ 2^L) (decode : Fin D → Y) (y : Y) :
    (receiptBlocks L D hDB decode y).card = weight D decode y := by
  apply Finset.card_image_of_injective
  exact (code L).symm.injective.comp (Fin.castLE_injective hDB)

theorem receiptBlocks_subset (L D : ℕ) (hDB : D ≤ 2^L) (decode : Fin D → Y) (y : Y) :
    receiptBlocks L D hDB decode y ⊆ acceptedBlocks L D hDB := by
  exact Finset.image_subset_image (Finset.filter_subset _ _)


/-- The literal proposal operation: reject v≥D, otherwise return the table entry at v. -/
def sample (L D : ℕ) (decode : Fin D → Y) (w : Mealy.Block L) : Option Y :=
  if hv : (code L w).val < D then some (decode ⟨(code L w).val,hv⟩) else none

theorem sample_none_iff (L D : ℕ) (hDB : D ≤ 2^L) (decode : Fin D → Y) (w : Mealy.Block L) :
    sample L D decode w = none ↔ w ∈ rejectedBlocks L D hDB := by
  simp [sample, mem_rejectedBlocks]

theorem sample_some_iff (L D : ℕ) (hDB : D ≤ 2^L) (decode : Fin D → Y)
    (w : Mealy.Block L) (y : Y) :
    sample L D decode w = some y ↔ w ∈ receiptBlocks L D hDB decode y := by
  simp only [receiptBlocks, Finset.mem_image, Finset.mem_filter, Finset.mem_univ, true_and]
  constructor
  · intro hs
    unfold sample at hs
    split at hs
    · rename_i hv
      exact ⟨⟨(code L w).val,hv⟩, Option.some.inj hs,
        (code L).symm_apply_eq.mpr (Fin.ext rfl)⟩
    · contradiction
  · rintro ⟨i,hi,rfl⟩
    simp only [sample, Equiv.apply_symm_apply, Fin.coe_castLE]
    rw [dif_pos i.isLt]
    simpa using hi

theorem receiptBlocks_disjoint (L D : ℕ) (hDB : D ≤ 2^L) (decode : Fin D → Y)
    {y z : Y} (hyz : y ≠ z) :
    Disjoint (receiptBlocks L D hDB decode y) (receiptBlocks L D hDB decode z) := by
  apply Finset.disjoint_left.mpr
  intro w hy hz
  rw [← sample_some_iff] at hy hz
  exact hyz (Option.some.inj (hy.symm.trans hz))

def firstEvent {L : ℕ} (R A : Finset (Mealy.Block L)) (r : ℕ) : Set Cantor :=
  constraintEvent (List.replicate r R ++ [A])

theorem firstEvent_iff {L : ℕ} (R A : Finset (Mealy.Block L)) (r : ℕ) (x : Cantor) :
    x ∈ firstEvent R A r ↔ (∀ i < r, block L i x ∈ R) ∧ block L r x ∈ A := by
  simp only [firstEvent, constraintEvent, Set.mem_setOf_eq]
  constructor
  · intro h
    constructor
    · intro i hi
      have hh := h i (by simp; omega)
      rw [List.getElem_append_left (show i < (List.replicate r R).length by simpa using hi)] at hh
      simpa using hh
    · simpa [List.getElem_append_right (by simp : (List.replicate r R).length ≤ r)]
        using h r (by simp)
  · rintro ⟨hR,hA⟩ i hi
    have hir : i < r+1 := by simpa using hi
    by_cases hr : i < r
    · simpa [List.getElem_append_left (show i < (List.replicate r R).length by simpa using hr)] using hR i hr
    · have he : i = r := by omega
      subst i
      simpa [List.getElem_append_right (by simp : (List.replicate r R).length ≤ r)] using hA

theorem measurableSet_firstEvent {L : ℕ} (R A : Finset (Mealy.Block L)) (r : ℕ) :
    MeasurableSet (firstEvent R A r) := measurableSet_constraintEvent _

theorem firstEvent_disjoint {L : ℕ} (R A : Finset (Mealy.Block L)) (hRA : Disjoint R A) :
    Pairwise (fun r s => Disjoint (firstEvent R A r) (firstEvent R A s)) := by
  intro r s hrs
  apply Set.disjoint_left.mpr
  intro x hr hs
  rw [firstEvent_iff] at hr hs
  have hn := Finset.disjoint_left.mp hRA
  rcases lt_or_gt_of_ne hrs with h | h
  · exact hn (hs.1 r h) hr.2
  · exact hn (hr.1 s h) hs.2

/-- Joint law of the literal receipt and the exact rejection count. -/
theorem measure_firstEvent {L : ℕ} (R A : Finset (Mealy.Block L)) (r : ℕ) :
    fairCantor (firstEvent R A r) =
      ((R.card : ℝ≥0∞) * (1/2 : ℝ≥0∞)^L)^r *
        ((A.card : ℝ≥0∞) * (1/2 : ℝ≥0∞)^L) := by
  rw [firstEvent, measure_constraintEvent_product]
  simp

/-- Infinite waiting is treated by a countable union, not a timeout or a supplied law. -/
theorem measure_everEvent {L : ℕ} (R A : Finset (Mealy.Block L)) (hRA : Disjoint R A) :
    fairCantor (⋃ r, firstEvent R A r) =
      (1 - (R.card : ℝ≥0∞) * (1/2 : ℝ≥0∞)^L)⁻¹ *
        ((A.card : ℝ≥0∞) * (1/2 : ℝ≥0∞)^L) := by
  rw [measure_iUnion (firstEvent_disjoint R A hRA) (measurableSet_firstEvent R A)]
  simp only [measure_firstEvent, ENNReal.tsum_mul_right, ENNReal.tsum_geometric]


theorem binary_unit (L : ℕ) : (1/2 : ℝ≥0∞)^L = ((2^L : ℕ) : ℝ≥0∞)⁻¹ := by
  simp [ENNReal.inv_pow]

theorem rejected_fraction (L D : ℕ) (hDB : D ≤ 2^L) :
    ((rejectedBlocks L D hDB).card : ℝ≥0∞) * (1/2 : ℝ≥0∞)^L =
      1 - (D : ℝ≥0∞)/(2^L : ℕ) := by
  rw [card_rejectedBlocks, binary_unit, ← div_eq_mul_inv, ENNReal.natCast_sub,
    ENNReal.sub_div (by intros; positivity), ENNReal.div_self (by positivity) (by simp)]

theorem accepted_fraction_le_one (L D : ℕ) (hDB : D ≤ 2^L) :
    (D : ℝ≥0∞)/(2^L : ℕ) ≤ 1 := by
  rw [ENNReal.div_le_iff (by positivity) (by simp), one_mul]
  exact_mod_cast hDB

theorem rejection_receipt_disjoint (L D : ℕ) (hDB : D ≤ 2^L)
    (decode : Fin D → Y) (y : Y) :
    Disjoint (rejectedBlocks L D hDB) (receiptBlocks L D hDB decode y) :=
  Finset.sdiff_disjoint.mono_right (receiptBlocks_subset L D hDB decode y)

theorem first_receipt_unique (L D : ℕ) (hDB : D ≤ 2^L) (decode : Fin D → Y)
    {y z : Y} {r s : ℕ} {x : Cantor}
    (hy : x ∈ firstEvent (rejectedBlocks L D hDB) (receiptBlocks L D hDB decode y) r)
    (hz : x ∈ firstEvent (rejectedBlocks L D hDB) (receiptBlocks L D hDB decode z) s) :
    r = s ∧ y = z := by
  rw [firstEvent_iff] at hy hz
  have he : r = s := by
    by_contra hn
    rcases lt_or_gt_of_ne hn with h | h
    · exact Finset.disjoint_left.mp (rejection_receipt_disjoint L D hDB decode y)
        (hz.1 r h) hy.2
    · exact Finset.disjoint_left.mp (rejection_receipt_disjoint L D hDB decode z)
        (hy.1 s h) hz.2
  refine ⟨he, ?_⟩
  subst s
  rw [← sample_some_iff] at hy hz
  exact Option.some.inj (hy.2.symm.trans hz.2)

/-- Exact first-receipt law for every finite deterministic allocation table.
The weight is computed by counting the table's fibres, not supplied as a sampler law. -/
theorem receipt_probability (L D : ℕ) (hDB : D ≤ 2^L)
    (decode : Fin D → Y) (y : Y) :
    fairCantor (⋃ r, firstEvent (rejectedBlocks L D hDB)
      (receiptBlocks L D hDB decode y) r) = (weight D decode y : ℝ≥0∞)/D := by
  rw [measure_everEvent _ _ (rejection_receipt_disjoint L D hDB decode y),
    rejected_fraction, ENNReal.sub_sub_cancel (by simp) (accepted_fraction_le_one L D hDB),
    card_receiptBlocks, binary_unit,
    ENNReal.inv_div (Or.inl (by simp)) (Or.inl (by positivity))]
  simp only [div_eq_mul_inv]
  calc
    _ = ((weight D decode y : ℝ≥0∞) * (D : ℝ≥0∞)⁻¹) *
      (((2^L : ℕ) : ℝ≥0∞) * ((2^L : ℕ) : ℝ≥0∞)⁻¹) := by simp only [mul_assoc, mul_comm, mul_left_comm]
    _ = _ := by rw [ENNReal.mul_inv_cancel (by positivity) (by simp), mul_one]

/-- Shared-width rejection count has a row-independent geometric law. -/
theorem rejection_count_probability (L D : ℕ) (hDB : D ≤ 2^L) (r : ℕ) :
    fairCantor (firstEvent (rejectedBlocks L D hDB) (acceptedBlocks L D hDB) r) =
      (1-(D : ℝ≥0∞)/(2^L : ℕ))^r * ((D : ℝ≥0∞)/(2^L : ℕ)) := by
  rw [measure_firstEvent, rejected_fraction, card_acceptedBlocks, binary_unit, div_eq_mul_inv]

/-- Every positive-denominator sampler eventually accepts with probability one. -/
theorem eventual_acceptance_probability (L D : ℕ) (hD : 0 < D) (hDB : D ≤ 2^L) :
    fairCantor (⋃ r, firstEvent (rejectedBlocks L D hDB) (acceptedBlocks L D hDB) r) = 1 := by
  rw [measure_everEvent _ _ (show Disjoint (rejectedBlocks L D hDB) (acceptedBlocks L D hDB) from Finset.sdiff_disjoint), rejected_fraction,
    ENNReal.sub_sub_cancel (by simp) (accepted_fraction_le_one L D hDB), card_acceptedBlocks,
    binary_unit, ← div_eq_mul_inv,
    ENNReal.inv_mul_cancel]
  · simp [ne_of_gt hD]
  · exact ENNReal.mul_ne_top (by simp) (ENNReal.inv_ne_top.mpr (by positivity))

/-- Joint first-receipt/clock mass factorizes into its two actual fair-tape marginals. -/
theorem receipt_clock_factorization (L D : ℕ) (hD : 0 < D) (hDB : D ≤ 2^L)
    (decode : Fin D → Y) (y : Y) (r : ℕ) :
    fairCantor (firstEvent (rejectedBlocks L D hDB) (receiptBlocks L D hDB decode y) r) =
      fairCantor (⋃ s, firstEvent (rejectedBlocks L D hDB) (receiptBlocks L D hDB decode y) s) *
      fairCantor (firstEvent (rejectedBlocks L D hDB) (acceptedBlocks L D hDB) r) := by
  rw [measure_firstEvent, rejected_fraction, card_receiptBlocks, binary_unit,
    receipt_probability, rejection_count_probability]
  simp only [div_eq_mul_inv]
  calc
    _ = (weight D decode y : ℝ≥0∞) *
        ((1-(D : ℝ≥0∞)*((2^L : ℕ) : ℝ≥0∞)⁻¹)^r * ((2^L : ℕ) : ℝ≥0∞)⁻¹) := by ac_rfl
    _ = _ := by
      conv_rhs => rw [show (weight D decode y : ℝ≥0∞) * (D : ℝ≥0∞)⁻¹ *
          ((1-(D : ℝ≥0∞)*((2^L : ℕ) : ℝ≥0∞)⁻¹)^r *
          ((D : ℝ≥0∞)*((2^L : ℕ) : ℝ≥0∞)⁻¹)) =
          (weight D decode y : ℝ≥0∞) *
          ((1-(D : ℝ≥0∞)*((2^L : ℕ) : ℝ≥0∞)⁻¹)^r * ((2^L : ℕ) : ℝ≥0∞)⁻¹) *
          ((D : ℝ≥0∞)⁻¹*(D : ℝ≥0∞)) by ac_rfl]
      rw [ENNReal.inv_mul_cancel (by exact_mod_cast ne_of_gt hD) (by simp), mul_one]

end Orthemology.RationalLaw
