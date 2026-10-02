import RecursivePhysicalDecoder

noncomputable section
open MeasureTheory ProbabilityTheory Filter Finset
open scoped BigOperators ENNReal

namespace Orthemology.Tranche3.PhysicalCost
open Orthemology.Tranche2.PhysicalFlattening
variable {A : Type*}

/-- Exact placement of an executed action, including arbitrary earlier empty
blocks. Only unbounded total physical length is required. -/
lemma blockIndex_at_offset (blocks : ℕ → List A) (hu : Unbounded blocks)
    (n : ℕ) (i : Fin (blocks n).length) :
    blockIndex blocks hu (prefixLength blocks n + i.val) = n := by
  apply le_antisymm
  · apply Nat.find_min'
    rw [prefixLength_succ]
    exact Nat.add_lt_add_left i.isLt _
  · exact late_index blocks hu n _ (Nat.le_add_right _ _)

/-- Every physical position is uniquely indexed by its block and local offset. -/
lemma physicalPosition_bijective (blocks : ℕ → List A) (hu : Unbounded blocks) :
    Function.Bijective (fun ni : Σ n, Fin (blocks n).length =>
      prefixLength blocks ni.1 + ni.2.val) := by
  constructor
  · intro ni mj he
    rcases ni with ⟨n,i⟩
    rcases mj with ⟨m,j⟩
    have hm : n = m := by
      have hh := congrArg (blockIndex blocks hu) he
      simpa only [blockIndex_at_offset] using hh
    subst m
    have hij : i = j := by
      apply Fin.ext
      dsimp at he
      omega
    exact congrArg (Sigma.mk n) hij
  · intro t
    refine ⟨⟨blockIndex blocks hu t,
      ⟨t - prefixLength blocks (blockIndex blocks hu t), offset_lt_length blocks hu t⟩⟩, ?_⟩
    have h := blockIndex_lower blocks hu t
    dsimp
    omega

/-- Physical time is in bijection with actual positions of executed blocks. -/
def positionEquiv (blocks : ℕ → List A) (hu : Unbounded blocks) :
    (Σ n, Fin (blocks n).length) ≃ ℕ :=
  Equiv.ofBijective _ (physicalPosition_bijective blocks hu)

lemma flatten_at_offset (blocks : ℕ → List A) (hu : Unbounded blocks)
    (n : ℕ) (i : Fin (blocks n).length) :
    flatten blocks hu (prefixLength blocks n + i.val) = (blocks n).get i := by
  unfold flatten
  rw [List.get_of_eq (congrArg blocks (blockIndex_at_offset blocks hu n i))]
  congr 1
  apply Fin.ext
  simp [blockIndex_at_offset]

/-- The nonnegative cost of one finite executed list. -/
def listCost (c : A → ℝ≥0∞) (as : List A) : ℝ≥0∞ := (as.map c).sum

lemma listCost_eq_sum_get (c : A → ℝ≥0∞) (as : List A) :
    listCost c as = ∑ i : Fin as.length, c (as.get i) := by
  have hm : as.map c = List.ofFn (fun i : Fin as.length => c (as.get i)) := by
    simpa only [List.map_ofFn, Function.comp_def, List.ofFn_get] using
      (List.map_ofFn (f := as.get) (g := c))
  rw [listCost, hm, List.sum_ofFn]

/-- Pathwise conservation of total nonnegative cost under physical flattening.
This is an equality, not a one-sided comparison of block and action clocks. -/
theorem flatten_total_cost (c : A → ℝ≥0∞) (blocks : ℕ → List A)
    (hu : Unbounded blocks) :
    (∑' t, c (flatten blocks hu t)) = ∑' n, listCost c (blocks n) := by
  calc
    _ = ∑' ni : Σ n, Fin (blocks n).length, c ((blocks ni.1).get ni.2) :=
      by
        simpa only [positionEquiv, Equiv.ofBijective_apply, flatten_at_offset] using
          ((positionEquiv blocks hu).tsum_eq (fun t => c (flatten blocks hu t))).symm
    _ = ∑' n, ∑' i : Fin (blocks n).length, c ((blocks n).get i) := ENNReal.tsum_sigma (fun n (i : Fin (blocks n).length) => c ((blocks n).get i))
    _ = _ := by
      apply tsum_congr
      intro n
      rw [tsum_fintype, listCost_eq_sum_get]

/-- The total finite-prefix decoder conserves cost on non-stalling runs. -/
theorem decode_total_cost (c : A → ℝ≥0∞) (d : A) (blocks : ℕ → List A)
    (hne : ∀ n, blocks n ≠ []) :
    (∑' t, c (decode d blocks t)) = ∑' n, listCost c (blocks n) := by
  simp_rw [decode_eq_flatten d blocks hne]
  exact flatten_total_cost c blocks _

end Orthemology.Tranche3.PhysicalCost
