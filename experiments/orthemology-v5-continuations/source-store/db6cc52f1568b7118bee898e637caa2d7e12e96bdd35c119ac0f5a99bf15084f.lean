import PrefixTail
import P02A2.Mixture

open Set MeasureTheory Filter
open scoped NNReal ENNReal
namespace OrthemologyTagged
open P02A2.Q8Measure OrthemologyMeasure

def tagWord (i : ℕ) : Fin (i+1) → Bool := fun j => decide (j.val < i)
def tag (i : ℕ) (y : Cantor) : Cantor := appendPrefix (i+1) (tagWord i) y
def tail (i : ℕ) := dropBits (i+1)
def tagEvent (i : ℕ) : Set Cantor := prefixSet (i+1) (tagWord i)
def allTrue : Cantor := fun _ => true

theorem tagEvent_measurable (i : ℕ) : MeasurableSet (tagEvent i) :=
  prefixSet_measurable _ _

theorem tagEvent_spec (i : ℕ) (x : Cantor) :
    x ∈ tagEvent i ↔ (∀ j < i, x j = true) ∧ x i = false := by
  change (OrthemologyMeasure.prefixBits (i+1) x = tagWord i) ↔ _
  constructor
  · intro h
    constructor
    · intro j hj
      have he := congrFun h ⟨j, by omega⟩
      simpa [OrthemologyMeasure.prefixBits, tagWord, hj] using he
    · have he := congrFun h ⟨i, by omega⟩
      simpa [OrthemologyMeasure.prefixBits, tagWord] using he
  · rintro ⟨hp,hz⟩
    funext j
    by_cases hj : j.val < i
    · simpa [OrthemologyMeasure.prefixBits, tagWord, hj] using hp j.val hj
    · have he : j.val = i := by have := j.isLt; omega
      simpa [OrthemologyMeasure.prefixBits, tagWord, he] using hz

theorem tag_measurable (i : ℕ) : Measurable (tag i) := by
  apply measurable_pi_lambda
  intro n
  by_cases hn : n < i+1
  · simpa [tag, appendPrefix, hn] using
      (measurable_const : Measurable (fun _ : Cantor => tagWord i ⟨n,hn⟩))
  · simpa [tag, appendPrefix, hn] using
      (measurable_pi_apply (n-(i+1)) : Measurable (fun y : Cantor => y (n-(i+1))))

theorem tail_measurable (i : ℕ) : Measurable (tail i) := dropBits_measurable _

theorem tail_tag (i : ℕ) (y : Cantor) : tail i (tag i y) = y := by
  funext n
  simp [tail, dropBits, tag, appendPrefix, show ¬ (i+1+n < i+1) by omega]

theorem tag_injective (i : ℕ) : Function.Injective (tag i) := by
  intro x y h
  have he := congrArg (tail i) h
  simpa only [tail_tag] using he

theorem tag_mem (i : ℕ) (y : Cantor) : tag i y ∈ tagEvent i := by
  rw [tagEvent_spec]
  constructor
  · intro j hj
    simp [tag, appendPrefix, tagWord, show j < i+1 by omega, hj]
  · simp [tag, appendPrefix, tagWord]

noncomputable def tagged (rows : ℕ → Cantor → Cantor) (x : Cantor) : Cantor := by
  classical
  exact if h : ∃ n, x n = false then tag (Nat.find h) (rows (Nat.find h) (tail (Nat.find h) x))
    else allTrue

theorem tagged_on (rows : ℕ → Cantor → Cantor) {i : ℕ} {x : Cantor}
    (hx : x ∈ tagEvent i) : tagged rows x = tag i (rows i (tail i x)) := by
  classical
  obtain ⟨hp,hz⟩ := (tagEvent_spec i x).mp hx
  have he : ∃ n, x n = false := ⟨i,hz⟩
  have hi : Nat.find he = i := (Nat.find_eq_iff he).mpr ⟨hz, fun j hj => by rw [hp j hj]; decide⟩
  simp [tagged, he, hi]

theorem tagged_allTrue (rows : ℕ → Cantor → Cantor) : tagged rows allTrue = allTrue := by
  simp [tagged, allTrue]

theorem exists_tag_or_allTrue (x : Cantor) : (∃ i, x ∈ tagEvent i) ∨ x = allTrue := by
  classical
  by_cases h : ∃ n, x n = false
  · left
    refine ⟨Nat.find h, (tagEvent_spec _ _).mpr ⟨?_,Nat.find_spec h⟩⟩
    intro j hj
    have hn := Nat.find_min h hj
    cases hx : x j <;> simp_all
  · right
    funext n
    have hn : x n ≠ false := fun hn => h ⟨n,hn⟩
    cases hx : x n <;> simp_all [allTrue]

theorem tagEvents_disjoint : Pairwise (fun i j => Disjoint (tagEvent i) (tagEvent j)) := by
  intro i j hij
  apply Set.disjoint_left.mpr
  intro x hi hj
  obtain ⟨hip,hiz⟩ := (tagEvent_spec i x).mp hi
  obtain ⟨hjp,hjz⟩ := (tagEvent_spec j x).mp hj
  rcases lt_or_gt_of_ne hij with h | h
  · have he := hjp i h
    rw [hiz] at he
    cases he
  · have he := hip j h
    rw [hjz] at he
    cases he

theorem tagged_measurable {rows : ℕ → Cantor → Cantor}
    (hrows : ∀ i, Measurable (rows i)) : Measurable (tagged rows) := by
  intro S hS
  have he : tagged rows ⁻¹' S =
      ({allTrue} ∩ (fun _ : Cantor => allTrue) ⁻¹' S) ∪
      ⋃ i, tagEvent i ∩ (fun x => tag i (rows i (tail i x))) ⁻¹' S := by
    ext x
    constructor
    · intro hx
      rcases exists_tag_or_allTrue x with ⟨i,hi⟩ | rfl
      · exact Or.inr (mem_iUnion.mpr ⟨i,hi,by simpa only [mem_preimage, tagged_on rows hi] using hx⟩)
      · exact Or.inl ⟨rfl,by simpa only [mem_preimage, tagged_allTrue] using hx⟩
    · rintro (⟨rfl,hx⟩ | hx)
      · simpa only [mem_preimage, tagged_allTrue] using hx
      · obtain ⟨i,hi,hx⟩ := mem_iUnion.mp hx
        simpa only [mem_preimage, tagged_on rows hi] using hx
  rw [he]
  exact ((measurableSet_singleton _).inter (measurable_const hS)).union
    (MeasurableSet.iUnion fun i => (tagEvent_measurable i).inter
      (((tag_measurable i).comp ((hrows i).comp (tail_measurable i))) hS))

theorem allTrue_not_tag (i : ℕ) : allTrue ∉ tagEvent i := by
  intro h
  have hz := ((tagEvent_spec i allTrue).mp h).2
  simp [allTrue] at hz

theorem selector_cover_ae : ∀ᵐ x ∂fairCantor, x ∈ ⋃ i, tagEvent i := by
  rw [ae_iff]
  have he : {x | ¬x ∈ ⋃ i, tagEvent i} = {allTrue} := by
    ext x
    constructor
    · intro hx
      rcases exists_tag_or_allTrue x with ⟨i,hi⟩ | he
      · exact False.elim (hx (mem_iUnion.mpr ⟨i,hi⟩))
      · exact he
    · rintro rfl hx
      obtain ⟨i,hi⟩ := mem_iUnion.mp hx
      exact allTrue_not_tag i hi
  rw [he]
  exact fairCantor_singleton_zero allTrue

theorem fairCantor_sum_restrict :
    fairCantor = Measure.sum (fun i => fairCantor.restrict (tagEvent i)) := by
  have h := Measure.restrict_iUnion (μ := fairCantor) tagEvents_disjoint tagEvent_measurable
  rw [Measure.restrict_eq_self_of_ae_mem selector_cover_ae] at h
  exact h

theorem tagged_branch_law {rows : ℕ → Cantor → Cantor}
    (hrows : ∀ i, Measurable (rows i)) (i : ℕ) :
    (fairCantor.restrict (tagEvent i)).map (tagged rows) =
      ((1/2 : ℝ≥0)^(i+1)) • ((fairCantor.map (rows i)).map (tag i)) := by
  have he : tagged rows =ᵐ[fairCantor.restrict (tagEvent i)]
      (tag i ∘ rows i ∘ tail i) := by
    filter_upwards [ae_restrict_mem (tagEvent_measurable i)] with x hx
    exact tagged_on rows hx
  rw [Measure.map_congr he,
      ← Measure.map_map (tag_measurable i) ((hrows i).comp (tail_measurable i)),
      ← Measure.map_map (hrows i) (tail_measurable i)]
  change (((fairCantor.restrict (prefixSet (i+1) (tagWord i))).map (dropBits (i+1))).map
    (rows i) |>.map (tag i)) = _
  rw [restricted_tail_law, Measure.map_smul, Measure.map_smul]

/-- The actual unary-selector observer has exactly the tagged countable mixture
law. The all-true input branch remains defined and is discarded only as null. -/
theorem tagged_mixture_law {rows : ℕ → Cantor → Cantor}
    (hrows : ∀ i, Measurable (rows i)) :
    fairCantor.map (tagged rows) = Measure.sum (fun i =>
      ((1/2 : ℝ≥0)^(i+1)) • ((fairCantor.map (rows i)).map (tag i))) := by
  calc
    fairCantor.map (tagged rows) =
        (Measure.sum (fun i => fairCantor.restrict (tagEvent i))).map (tagged rows) :=
      congrArg (fun μ : Measure Cantor => μ.map (tagged rows)) fairCantor_sum_restrict
    _ = Measure.sum (fun i => (fairCantor.restrict (tagEvent i)).map (tagged rows)) :=
      Measure.map_sum (tagged_measurable hrows).aemeasurable
    _ = _ := by
      congr 1
      funext i
      exact tagged_branch_law hrows i

end OrthemologyTagged
#print axioms OrthemologyTagged.tagged_measurable

#print axioms OrthemologyTagged.tagged_mixture_law
