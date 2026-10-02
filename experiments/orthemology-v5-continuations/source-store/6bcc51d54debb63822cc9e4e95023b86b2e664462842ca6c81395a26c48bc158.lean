import P02A2.MeasureCore
import Mathlib.MeasureTheory.Measure.MeasureSpace
import Mathlib.Tactic

/-! UNEXECUTED. Core CV-R is proved through disjoint measurable losses.
There is no axiom asserting the target identity and no residual is discarded. -/
namespace P02A2.Refinement
open Set MeasureTheory Function
open scoped BigOperators ENNReal
variable {X : Type*} [MeasurableSpace X]

def loss (A : ℕ → Set X) (n : ℕ) : Set X := A n \ A (n+1)
def persist (A : ℕ → Set X) : Set X := ⋂ n, A n

theorem persist_subset (A : ℕ → Set X) (n : ℕ) : persist A ⊆ A n :=
  iInter_subset A n

theorem loss_measurable {A : ℕ → Set X} (hA : ∀ n, MeasurableSet (A n)) (n : ℕ) :
    MeasurableSet (loss A n) := (hA n).diff (hA (n+1))

theorem persist_measurable {A : ℕ → Set X} (hA : ∀ n, MeasurableSet (A n)) :
    MeasurableSet (persist A) := MeasurableSet.iInter hA

theorem losses_disjoint {A : ℕ → Set X} (hA : Antitone A) :
    Pairwise (Disjoint on loss A) := by
  intro i j hij
  apply Set.disjoint_left.mpr
  intro x hi hj
  rcases lt_or_gt_of_ne hij with h | h
  · exact hi.2 (hA (by omega : i+1 ≤ j) hj.1)
  · exact hj.2 (hA (by omega : j+1 ≤ i) hi.1)

theorem union_losses {A : ℕ → Set X} (hA : Antitone A) :
    (⋃ n, loss A n) = A 0 \ persist A := by
  classical
  ext x
  constructor
  · intro hx
    rcases mem_iUnion.mp hx with ⟨n, hn⟩
    refine ⟨hA (Nat.zero_le n) hn.1, ?_⟩
    intro hp
    exact hn.2 (mem_iInter.mp hp (n+1))
  · rintro ⟨h0, hp⟩
    have hex : ∃ k, x ∉ A k := by simpa only [persist, mem_iInter, not_forall] using hp
    let k := Nat.find hex
    have hk : x ∉ A k := Nat.find_spec hex
    have hk0 : k ≠ 0 := by
      intro he
      apply hk
      simpa [he] using h0
    have hpv : x ∈ A (k-1) := by
      by_contra h
      have ht : k ≤ k-1 := Nat.find_min' hex h
      omega
    apply mem_iUnion.mpr
    refine ⟨k-1, hpv, ?_⟩
    simpa only [Nat.sub_add_cancel (Nat.one_le_iff_ne_zero.mpr hk0)] using hk

theorem complement_partition {A : ℕ → Set X} {B : Set X}
    (hA : Antitone A) (hB : B ⊆ persist A) :
    Bᶜ = (A 0)ᶜ ∪ ((⋃ n, loss A n) ∪ (persist A \ B)) := by
  rw [union_losses hA]
  have hP : persist A ⊆ A 0 := persist_subset A 0
  ext x
  simp only [mem_compl_iff, mem_union, mem_diff]
  constructor
  · intro hb
    by_cases h0 : x ∈ A 0
    · by_cases hp : x ∈ persist A
      · exact Or.inr (Or.inr ⟨hp,hb⟩)
      · exact Or.inr (Or.inl ⟨h0,hp⟩)
    · exact Or.inl h0
  · rintro (h0 | ⟨h0,hp⟩ | ⟨hp,hb⟩) hxb
    · exact h0 (hP (hB hxb))
    · exact hp (hB hxb)
    · exact hb hxb

theorem measure_extinction_decomposition (μ : Measure X)
    {A : ℕ → Set X} {B : Set X} (hA : Antitone A)
    (hm : ∀ n, MeasurableSet (A n)) (hBm : MeasurableSet B)
    (hB : B ⊆ persist A) :
    μ Bᶜ = μ (A 0)ᶜ + (∑' n, μ (loss A n)) + μ (persist A \ B) := by
  have hL : MeasurableSet (⋃ n, loss A n) := MeasurableSet.iUnion (loss_measurable hm)
  have hJ : MeasurableSet (persist A \ B) := (persist_measurable hm).diff hBm
  have hdLJ : Disjoint (⋃ n, loss A n) (persist A \ B) := by
    rw [union_losses hA]
    exact Set.disjoint_left.mpr (by intro x hx hy; exact hx.2 hy.1)
  have hd0 : Disjoint (A 0)ᶜ ((⋃ n, loss A n) ∪ (persist A \ B)) := by
    rw [union_losses hA]
    apply Set.disjoint_left.mpr
    intro x hx hy
    rcases hy with hy | hy
    · exact hx hy.1
    · exact hx (persist_subset A 0 hy.1)
  rw [complement_partition hA hB, measure_union hd0 (hL.union hJ),
    measure_union hdLJ hJ, measure_iUnion (losses_disjoint hA) (loss_measurable hm)]
  exact (add_assoc _ _ _).symm

theorem real_extinction_decomposition (μ : Measure X) [IsFiniteMeasure μ]
    {A : ℕ → Set X} {B : Set X} (hA : Antitone A)
    (hm : ∀ n, MeasurableSet (A n)) (hBm : MeasurableSet B)
    (hB : B ⊆ persist A) :
    (μ Bᶜ).toReal = (μ (A 0)ᶜ).toReal + (∑' n, (μ (loss A n)).toReal) +
      (μ (persist A \ B)).toReal := by
  have hsum : (∑' n, μ (loss A n)) ≠ ∞ := by
    rw [← measure_iUnion (losses_disjoint hA) (loss_measurable hm)]
    exact measure_ne_top μ _
  have h := congrArg ENNReal.toReal (measure_extinction_decomposition μ hA hm hBm hB)
  rw [ENNReal.toReal_add (ENNReal.add_ne_top.mpr ⟨measure_ne_top μ _, hsum⟩)
      (measure_ne_top μ _),
    ENNReal.toReal_add (measure_ne_top μ _) hsum,
    ENNReal.tsum_toReal_eq (fun n => measure_ne_top μ (loss A n))] at h
  exact h

theorem losses_real_summable (μ : Measure X) [IsFiniteMeasure μ]
    {A : ℕ → Set X} (hA : Antitone A) (hm : ∀ n, MeasurableSet (A n)) :
    Summable (fun n => (μ (loss A n)).toReal) := by
  apply ENNReal.summable_toReal
  rw [← measure_iUnion (losses_disjoint hA) (loss_measurable hm)]
  exact measure_ne_top μ _

theorem finite_telescope (d inc : ℕ → ℝ)
    (h : ∀ n, d (n+1) = d n + inc n) (N : ℕ) :
    d N = d 0 + ∑ n ∈ Finset.range N, inc n := by
  induction N with
  | zero => simp
  | succ N ih => rw [h, ih, Finset.sum_range_succ]; ring

theorem exact_budget (d0 debt J ε : ℝ) :
    d0 + debt + J ≤ ε ↔ debt + J ≤ ε-d0 := by constructor <;> intro h <;> linarith

theorem exact_residual_budget (L J ε : ℝ) :
    L+J ≤ ε ↔ J ≤ ε-L := by constructor <;> intro h <;> linarith

theorem no_residual_limit (dinf L J : ℝ) (hid : dinf=L+J) :
    dinf=L ↔ J=0 := by constructor <;> intro h <;> linarith

-- The full observation instantiation and uniform small-cell equivalence are
-- separately typed targets; their proof coverage is not silently inferred
-- from the general set-decomposition theorem above.
def UniformSmallCells (μ : Measure X) (m : ℕ → X → ℝ) : Prop :=
  ∀ η : ℝ, 0 < η → ∃ ε : ℝ, 0 < ε ∧
    ∀ n, (μ {x | 0 < m n x ∧ m n x < ε}).toReal < η
end P02A2.Refinement
