import FinitePrefixBoundary
import Mathlib.MeasureTheory.Constructions.Projective

open Set MeasureTheory
open scoped NNReal ENNReal
namespace OrthemologyTagged
open P02A2.Q8Measure OrthemologyMeasure

def dropBits (N : ℕ) (x : Cantor) : Cantor := fun k => x (N+k)
def prefixSet (N : ℕ) (w : Fin N → Bool) : Set Cantor := prefixBits N ⁻¹' {w}

theorem dropBits_measurable (N : ℕ) : Measurable (dropBits N) :=
  measurable_pi_lambda _ fun k => measurable_pi_apply (N+k)

theorem prefixSet_measurable (N : ℕ) (w : Fin N → Bool) : MeasurableSet (prefixSet N w) :=
  (prefixBits_measurable N) (measurableSet_singleton w)

noncomputable def fillFinite (I : Finset ℕ) (v : I → Bool) : Cantor :=
  fun k => if h : k ∈ I then v ⟨k,h⟩ else false

def appendPrefix (N : ℕ) (w : Fin N → Bool) (y : Cantor) : Cantor :=
  fun k => if h : k < N then w ⟨k,h⟩ else y (k-N)

theorem finite_tail_prefix_event (N : ℕ) (w : Fin N → Bool)
    (I : Finset ℕ) (v : I → Bool) :
    (dropBits N ⁻¹' (I.restrict ⁻¹' {v})) ∩ prefixSet N w =
      Set.pi (↑(Finset.range N ∪ I.image (fun k => N+k)) : Set ℕ)
        (fun k => {appendPrefix N w (fillFinite I v) k}) := by
  classical
  ext x
  change ((I.restrict (dropBits N x) = v) ∧ prefixBits N x = w) ↔ _
  constructor
  · rintro ⟨hv, hw⟩ k hk
    rcases Finset.mem_union.mp hk with hk | hk
    · have hkn := Finset.mem_range.mp hk
      have he := congrFun hw ⟨k,hkn⟩
      simpa [prefixBits, appendPrefix, hkn] using he
    · obtain ⟨j,hj,rfl⟩ := Finset.mem_image.mp hk
      have he := congrFun hv ⟨j,hj⟩
      simpa [Finset.restrict_def, dropBits, appendPrefix, fillFinite, hj,
        show ¬N+j<N by omega] using he
  · intro hx
    constructor
    · funext i
      have he := hx (N+i.val) (Finset.mem_union_right _ (Finset.mem_image.mpr ⟨i.val,i.property,rfl⟩))
      simpa [Finset.restrict_def, dropBits, appendPrefix, fillFinite, i.property,
        show ¬N+i.val<N by omega] using he
    · funext i
      have he := hx i.val (Finset.mem_union_left _ (Finset.mem_range.mpr i.isLt))
      simpa [prefixBits, appendPrefix, i.isLt] using he

theorem combined_card (N : ℕ) (I : Finset ℕ) :
    (Finset.range N ∪ I.image (fun k => N+k)).card = N + I.card := by
  classical
  have hd : Disjoint (Finset.range N) (I.image (fun k => N+k)) := by
    apply Finset.disjoint_left.mpr
    intro k hk hi
    obtain ⟨j,hj,rfl⟩ := Finset.mem_image.mp hi
    have hkn := Finset.mem_range.mp hk
    omega
  rw [Finset.card_union_of_disjoint hd, Finset.card_range,
    Finset.card_image_of_injective _ (fun a b h => Nat.add_left_cancel h)]

theorem restricted_tail_singleton (N : ℕ) (w : Fin N → Bool)
    (I : Finset ℕ) (v : I → Bool) :
    ((fairCantor.restrict (prefixSet N w)).map (dropBits N)).map I.restrict {v}
      = (1/2 : ℝ≥0∞)^(N+I.card) := by
  rw [Measure.map_apply (Finset.measurable_restrict I) (measurableSet_singleton v),
      Measure.map_apply (dropBits_measurable N)
        ((Finset.measurable_restrict I) (measurableSet_singleton v)),
      Measure.restrict_apply ((dropBits_measurable N)
        ((Finset.measurable_restrict I) (measurableSet_singleton v))),
      finite_tail_prefix_event, fairCantor_cylinder, combined_card]

theorem fair_restrict_singleton (I : Finset ℕ) (v : I → Bool) :
    (fairCantor.map I.restrict) {v} = (1/2 : ℝ≥0∞)^I.card := by
  classical
  rw [Measure.map_apply (Finset.measurable_restrict I) (measurableSet_singleton v)]
  have he : (I.restrict (π := fun _ : ℕ => Bool)) ⁻¹' {v} = Set.pi (I : Set ℕ) (fun k => {fillFinite I v k}) := by
    ext x
    change (I.restrict x = v) ↔ _
    constructor
    · intro hv k hk
      have hki : k ∈ I := hk
      have h := congrFun hv ⟨k,hki⟩
      simpa [Finset.restrict_def, fillFinite, hki] using h
    · intro hx
      funext i
      have h := hx i.val i.property
      simpa [Finset.restrict_def, fillFinite, i.property] using h
  rw [he, fairCantor_cylinder]

/-- Exact unnormalised disintegration: a fixed prefix costs 2^-N, while the
untouched tail retains the full fair infinite-product law. -/
theorem restricted_tail_law (N : ℕ) (w : Fin N → Bool) :
    (fairCantor.restrict (prefixSet N w)).map (dropBits N) =
      ((1/2 : ℝ≥0)^N) • fairCantor := by
  let rhs : Measure Cantor := ((1/2 : ℝ≥0)^N) • fairCantor
  have hproj : IsProjectiveLimit
      ((fairCantor.restrict (prefixSet N w)).map (dropBits N))
      (fun I : Finset ℕ => rhs.map I.restrict) := by
    intro I
    apply Measure.ext_of_singleton
    intro v
    change _ = ((((1/2 : ℝ≥0)^N) • fairCantor).map I.restrict) {v}
    rw [restricted_tail_singleton, Measure.map_smul, Measure.coe_nnreal_smul_apply,
        fair_restrict_singleton, pow_add]
    norm_num [ENNReal.inv_pow]
  exact hproj.unique (fun _ => rfl)

end OrthemologyTagged
#print axioms OrthemologyTagged.restricted_tail_singleton

#print axioms OrthemologyTagged.restricted_tail_law
