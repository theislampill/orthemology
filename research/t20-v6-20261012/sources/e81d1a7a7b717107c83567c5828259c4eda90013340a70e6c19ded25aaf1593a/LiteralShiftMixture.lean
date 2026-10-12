import LiteralShiftPrefix
import PrefixTail
import FiniteOutputTable
import P02A2.Mixture

/-! The actual literal shift law, disintegrated over its actual stopping words.
No output law or defect identity is assumed. The unresolved source event is an
explicit null-set hypothesis, separately discharged by the selector analysis. -/
namespace P02.LiteralShift
open Set MeasureTheory Filter P02A2 P02A2.Q8Measure P02A2.ObserverCore
open OrthemologyTagged OrthemologyMeasure
open scoped NNReal ENNReal

/-- A finite stopping leaf retains the complete copied source prefix. -/
abbrev StopWord := (k : ℕ) × ((Fin k → Bool) × Bool)

def stopCompletion (l : StopWord) : Cantor := appendPrefix l.1 l.2.1 (fun _ => false)

def StopLeaf (a b : ℕ) := {l : StopWord // FirstCut a b (stopCompletion l) l.1 l.2.2}

instance stopLeaf_countable (a b : ℕ) : Countable (StopLeaf a b) := by
  unfold StopLeaf
  infer_instance

def leafEvent {a b : ℕ} (l : StopLeaf a b) : Set Cantor := prefixSet l.1.1 l.1.2.1

noncomputable def leafWeight {a b : ℕ} (l : StopLeaf a b) : ℝ≥0 := (1/2)^l.1.1

theorem appendPrefix_measurable (k : ℕ) (w : Fin k → Bool) :
    Measurable (appendPrefix k w) := by
  apply measurable_pi_lambda
  intro n
  by_cases hn : n < k
  · simpa [appendPrefix, hn] using
      (measurable_const : Measurable (fun _ : Cantor => w ⟨n, hn⟩))
  · simpa [appendPrefix, hn] using
      (measurable_pi_apply (n-k) : Measurable (fun x : Cantor => x (n-k)))

theorem drop_appendPrefix (k : ℕ) (w : Fin k → Bool) (x : Cantor) :
    dropBits k (appendPrefix k w x) = x := by
  funext n
  simp [dropBits, appendPrefix, show ¬ k+n < k by omega]

theorem appendPrefix_mass (μ : Measure Cantor) [IsFiniteMeasure μ]
    (k : ℕ) (w : Fin k → Bool) : mass (μ.map (appendPrefix k w)) = mass μ := by
  have hback : (μ.map (appendPrefix k w)).map (dropBits k) = μ := by
    rw [Measure.map_map (dropBits_measurable k) (appendPrefix_measurable k w)]
    have he : dropBits k ∘ appendPrefix k w = id := by
      funext x
      exact drop_appendPrefix k w x
    rw [he, Measure.map_id]
  apply le_antisymm
  · have h := mass_map_mono (μ.map (appendPrefix k w)) (dropBits_measurable k)
    rw [hback] at h
    exact h
  · exact mass_map_mono μ (appendPrefix_measurable k w)

theorem streamPrefix_eq_of_prefixBits_eq {x y : Cantor} {k j : ℕ}
    (h : prefixBits k x = prefixBits k y) (hj : j ≤ k) :
    streamPrefix x j = streamPrefix y j := by
  unfold streamPrefix
  congr 1
  funext i
  exact congrFun h ⟨i.val, lt_of_lt_of_le i.isLt hj⟩

theorem FirstCut_congr {a b k : ℕ} {x y : Cantor} {side : Bool}
    (hxy : prefixBits k x = prefixBits k y) :
    FirstCut a b x k side ↔ FirstCut a b y k side := by
  have hc (j : ℕ) (hj : j ≤ k) : streamClassify a b x j = streamClassify a b y j := by
    unfold streamClassify
    rw [streamPrefix_eq_of_prefixBits_eq hxy hj]
  unfold FirstCut
  constructor
  · rintro ⟨hk, hs, he⟩
    exact ⟨hk, (hc k le_rfl) ▸ hs, fun j hj hjk => (hc j (le_of_lt hjk)) ▸ he j hj hjk⟩
  · rintro ⟨hk, hs, he⟩
    exact ⟨hk, (hc k le_rfl) ▸ hs, fun j hj hjk => (hc j (le_of_lt hjk)) ▸ he j hj hjk⟩

theorem prefixBits_appendPrefix (k : ℕ) (w : Fin k → Bool) (x : Cantor) :
    prefixBits k (appendPrefix k w x) = w := by
  funext i
  simp [prefixBits, appendPrefix, i.isLt]

theorem leaf_firstCut {a b : ℕ} (l : StopLeaf a b) {x : Cantor}
    (hx : x ∈ leafEvent l) : FirstCut a b x l.1.1 l.1.2.2 := by
  apply (FirstCut_congr (x := x) (y := stopCompletion l.1) ?_).mpr l.2
  exact hx.trans (prefixBits_appendPrefix _ _ _).symm

theorem firstCut_unique {a b k j : ℕ} {x : Cantor} {s t : Bool}
    (hk : FirstCut a b x k s) (hj : FirstCut a b x j t) : k = j ∧ s = t := by
  have he : k = j := by
    rcases lt_trichotomy k j with h | h | h
    · have := hj.2.2 k hk.1 h
      rw [hk.2.1] at this
      contradiction
    · exact h
    · have := hk.2.2 j hj.1 h
      rw [hj.2.1] at this
      contradiction
  subst j
  exact ⟨rfl, Option.some.inj (hk.2.1.symm.trans hj.2.1)⟩

theorem leafEvent_measurable {a b : ℕ} (l : StopLeaf a b) :
    MeasurableSet (leafEvent l) := prefixSet_measurable _ _

theorem leafEvents_disjoint (a b : ℕ) :
    Pairwise (fun l m : StopLeaf a b => Disjoint (leafEvent l) (leafEvent m)) := by
  intro l m hlm
  apply Set.disjoint_left.mpr
  intro x hx hy
  obtain ⟨hk, hs⟩ := firstCut_unique (leaf_firstCut l hx) (leaf_firstCut m hy)
  apply hlm
  apply Subtype.ext
  rcases l with ⟨⟨k, w, s⟩, hl⟩
  rcases m with ⟨⟨j, v, t⟩, hm⟩
  dsimp at hk hs
  subst j
  subst t
  have hw : w = v := hx.symm.trans hy
  subst v
  rfl

theorem exists_leaf_of_firstCut {a b k : ℕ} {x : Cantor} {side : Bool}
    (h : FirstCut a b x k side) : ∃ l : StopLeaf a b, x ∈ leafEvent l ∧ l.1.2.2 = side := by
  let w := prefixBits k x
  let l : StopLeaf a b := ⟨⟨k, w, side⟩, by
    apply (FirstCut_congr (x := x) (y := stopCompletion ⟨k,w,side⟩) ?_).mp h
    exact (prefixBits_appendPrefix k w _).symm⟩
  exact ⟨l, rfl, rfl⟩


def leafTail (body : Stmt) (output : ℕ) {a b : ℕ} (l : StopLeaf a b) : Cantor → Cantor :=
  if l.1.2.2 then P02A2.ObserverCore.output (programValue body output) else id

noncomputable def leafLaw (body : Stmt) (output : ℕ) {a b : ℕ} (l : StopLeaf a b) :
    Measure Cantor := (fairCantor.map (leafTail body output l)).map (appendPrefix l.1.1 l.1.2.1)

instance leafLaw_finite (body : Stmt) (output : ℕ) {a b : ℕ} (l : StopLeaf a b) :
    IsFiniteMeasure (leafLaw body output l) := by
  unfold leafLaw
  infer_instance

theorem leafTail_measurable (body : Stmt) (output : ℕ) {a b : ℕ} (l : StopLeaf a b) :
    Measurable (leafTail body output l) := by
  unfold leafTail
  split
  · exact P02A2.FiniteOutputTable.output_measurable _
  · exact measurable_id

theorem compiledOutput_measurable (body : Stmt) (output a b : ℕ) :
    Measurable (compiledOutput body output a b) :=
  P02A2.FiniteOutputTable.output_measurable _

theorem appendPrefix_drop_of_mem (k : ℕ) (w : Fin k → Bool) {x : Cantor}
    (hx : x ∈ prefixSet k w) : appendPrefix k w (dropBits k x) = x := by
  funext n
  by_cases hn : n < k
  · simpa [appendPrefix, hn, prefixBits] using (congrFun hx ⟨n,hn⟩).symm
  · simp [appendPrefix, hn, dropBits, Nat.add_sub_of_le (Nat.le_of_not_lt hn)]

theorem compiledOutput_on_leaf (body : Stmt) (output : ℕ) {a b : ℕ}
    (l : StopLeaf a b) {x : Cantor} (hx : x ∈ leafEvent l) :
    compiledOutput body output a b x =
      appendPrefix l.1.1 l.1.2.1 (leafTail body output l (dropBits l.1.1 x)) := by
  have hc := leaf_firstCut l hx
  cases hs : l.1.2.2 with
  | false =>
      rw [hs] at hc
      rw [compiledOutput_below body output a b l.1.1 x hc]
      simp only [leafTail, hs, Bool.false_eq_true, ↓reduceIte, id_eq]
      exact (appendPrefix_drop_of_mem _ _ hx).symm
  | true =>
      rw [hs] at hc
      funext n
      by_cases hn : n < l.1.1
      · rw [compiledOutput_copied_prefix body output a b l.1.1 n x true hc hn]
        simpa [appendPrefix, hn] using congrFun hx ⟨n,hn⟩
      · rw [compiledOutput_above_tail body output a b l.1.1 n x hc (Nat.le_of_not_lt hn)]
        simp only [appendPrefix, dif_neg hn, leafTail, hs, Bool.true_eq, ↓reduceIte]
        rfl

theorem literal_leaf_branch_law (body : Stmt) (output : ℕ) {a b : ℕ}
    (l : StopLeaf a b) :
    (fairCantor.restrict (leafEvent l)).map (compiledOutput body output a b) =
      leafWeight l • leafLaw body output l := by
  have he : compiledOutput body output a b =ᵐ[fairCantor.restrict (leafEvent l)]
      (appendPrefix l.1.1 l.1.2.1 ∘ leafTail body output l ∘ dropBits l.1.1) := by
    filter_upwards [ae_restrict_mem (leafEvent_measurable l)] with x hx
    exact compiledOutput_on_leaf body output l hx
  rw [Measure.map_congr he,
    ← Measure.map_map (appendPrefix_measurable _ _)
      ((leafTail_measurable body output l).comp (dropBits_measurable _)),
    ← Measure.map_map (leafTail_measurable body output l) (dropBits_measurable _)]
  change (((fairCantor.restrict (prefixSet l.1.1 l.1.2.1)).map (dropBits l.1.1)).map
    (leafTail body output l) |>.map (appendPrefix l.1.1 l.1.2.1)) = _
  rw [restricted_tail_law, Measure.map_smul, Measure.map_smul]
  rfl

theorem leaves_cover_ae (a b : ℕ)
    (hnull : fairCantor {x | ∀ k, 1 ≤ k → streamClassify a b x k = none} = 0) :
    ∀ᵐ x ∂fairCantor, x ∈ ⋃ l : StopLeaf a b, leafEvent l := by
  rw [ae_iff]
  apply measure_mono_null _ hnull
  intro x hx
  rcases firstCut_or_unresolved a b x with ⟨k, side, hk⟩ | hu
  · obtain ⟨l, hl, _⟩ := exists_leaf_of_firstCut hk
    exact False.elim (hx (mem_iUnion.mpr ⟨l,hl⟩))
  · exact hu

theorem fairCantor_sum_leaf_restrict (a b : ℕ)
    (hnull : fairCantor {x | ∀ k, 1 ≤ k → streamClassify a b x k = none} = 0) :
    fairCantor = Measure.sum (fun l : StopLeaf a b => fairCantor.restrict (leafEvent l)) := by
  have h := Measure.restrict_iUnion (μ := fairCantor) (leafEvents_disjoint a b)
    (@leafEvent_measurable a b)
  rw [Measure.restrict_eq_self_of_ae_mem (leaves_cover_ae a b hnull)] at h
  exact h

/-- Exact countable law for the literal compiler, with every copied stopping
prefix embedded in its own branch. Below leaves have a fair tail; above leaves
have the original inline program's fresh-tail output law. -/
theorem literal_shift_mixture_law (body : Stmt) (output a b : ℕ)
    (hnull : fairCantor {x | ∀ k, 1 ≤ k → streamClassify a b x k = none} = 0) :
    fairCantor.map (compiledOutput body output a b) =
      Measure.sum (fun l : StopLeaf a b => leafWeight l • leafLaw body output l) := by
  calc
    fairCantor.map (compiledOutput body output a b) =
        (Measure.sum (fun l : StopLeaf a b => fairCantor.restrict (leafEvent l))).map
          (compiledOutput body output a b) :=
      congrArg (fun μ : Measure Cantor => μ.map (compiledOutput body output a b))
        (fairCantor_sum_leaf_restrict a b hnull)
    _ = Measure.sum (fun l : StopLeaf a b =>
        (fairCantor.restrict (leafEvent l)).map (compiledOutput body output a b)) :=
      Measure.map_sum (compiledOutput_measurable body output a b).aemeasurable
    _ = _ := by
      congr 1
      funext l
      exact literal_leaf_branch_law body output l

/-- Baseline `mass_mixture`, generalized only from natural numbers to a
countable index, so the indices can retain actual finite stopping words. -/
theorem mass_countable_mixture {ι : Type*} [Countable ι]
    (w : ι → ℝ≥0) (μ : ι → Measure Cantor) [∀ i, IsFiniteMeasure (μ i)] :
    mass (Measure.sum (fun i => w i • μ i)) = ∑' i, (w i : ℝ≥0∞) * mass (μ i) := by
  let C : Set Cantor := ⋃ i, positive (μ i)
  have hC : C.Countable := Set.countable_iUnion (fun i => positive_countable (μ i))
  have hsub : positive (Measure.sum (fun i => w i • μ i)) ⊆ C := by
    intro x hx
    by_contra hnot
    have hz : ∀ i, μ i {x} = 0 := by
      intro i
      apply null_singleton_of_not_positive
      intro hi
      exact hnot (mem_iUnion.mpr ⟨i,hi⟩)
    have hzero : (Measure.sum (fun i => w i • μ i)) {x} = 0 := by
      rw [Measure.sum_apply _ (measurableSet_singleton x)]
      apply ENNReal.tsum_eq_zero.mpr
      intro i
      rw [Measure.coe_nnreal_smul_apply, hz i, mul_zero]
    exact (ne_of_gt hx) hzero
  rw [mass_eq_countable_superset _ hC hsub, Measure.sum_apply _ hC.measurableSet]
  apply tsum_congr
  intro i
  rw [Measure.smul_apply]
  change (w i : ℝ≥0∞) * μ i C = (w i : ℝ≥0∞) * mass (μ i)
  rw [mass_eq_countable_superset (μ i) hC (subset_iUnion (fun j => positive (μ j)) i)]

theorem fairCantor_mass_zero : mass fairCantor = 0 := by
  have hp : positive fairCantor = ∅ := by
    ext x
    change (0 < fairCantor {x}) ↔ False
    rw [fairCantor_singleton_zero]
    exact iff_false_intro (lt_irrefl _)
  rw [mass, hp, measure_empty]

theorem leafLaw_mass (body : Stmt) (output : ℕ) {a b : ℕ} (l : StopLeaf a b) :
    mass (leafLaw body output l) =
      if l.1.2.2 then mass (fairCantor.map (P02A2.ObserverCore.output (programValue body output)))
      else 0 := by
  unfold leafLaw
  rw [appendPrefix_mass]
  unfold leafTail
  split
  · rfl
  · rw [Measure.map_id, fairCantor_mass_zero]


def aboveLeafEvent {a b : ℕ} (l : StopLeaf a b) : Set Cantor :=
  if l.1.2.2 then leafEvent l else ∅

theorem aboveLeafEvent_subset {a b : ℕ} (l : StopLeaf a b) :
    aboveLeafEvent l ⊆ leafEvent l := by
  unfold aboveLeafEvent
  split
  · exact Subset.rfl
  · exact empty_subset _

theorem aboveLeafEvent_measurable {a b : ℕ} (l : StopLeaf a b) :
    MeasurableSet (aboveLeafEvent l) := by
  unfold aboveLeafEvent
  split
  · exact leafEvent_measurable l
  · exact MeasurableSet.empty

theorem above_event_eq_leaf_union (a b : ℕ) :
    {x | ∃ k, FirstCut a b x k true} = ⋃ l : StopLeaf a b, aboveLeafEvent l := by
  ext x
  constructor
  · rintro ⟨k, hk⟩
    obtain ⟨l, hl, hs⟩ := exists_leaf_of_firstCut hk
    exact mem_iUnion.mpr ⟨l, by simpa [aboveLeafEvent, hs] using hl⟩
  · intro hx
    obtain ⟨l, hl⟩ := mem_iUnion.mp hx
    have hs : l.1.2.2 = true := by
      by_contra hn
      simp [aboveLeafEvent, hn] at hl
    exact ⟨l.1.1, hs ▸ leaf_firstCut l (aboveLeafEvent_subset l hl)⟩

theorem leafEvent_probability {a b : ℕ} (l : StopLeaf a b) :
    fairCantor (leafEvent l) = (leafWeight l : ℝ≥0∞) := by
  change fairCantor (AtomicMembership.cylinder l.1.1 l.1.2.1) = _
  rw [P02A2.FiniteOutputTable.fair_cylinder]
  norm_num [leafWeight, ENNReal.coe_pow, ENNReal.inv_pow]

theorem above_event_probability_sum (a b : ℕ) :
    fairCantor {x | ∃ k, FirstCut a b x k true} =
      ∑' l : StopLeaf a b, if l.1.2.2 then (leafWeight l : ℝ≥0∞) else 0 := by
  rw [above_event_eq_leaf_union]
  have hd : Pairwise (fun l m : StopLeaf a b => Disjoint (aboveLeafEvent l) (aboveLeafEvent m)) := by
    intro l m hne
    exact (leafEvents_disjoint a b hne).mono (aboveLeafEvent_subset l) (aboveLeafEvent_subset m)
  rw [measure_iUnion hd (@aboveLeafEvent_measurable a b)]
  apply tsum_congr
  intro l
  unfold aboveLeafEvent
  split
  · exact leafEvent_probability l
  · exact measure_empty

/-- Atomic mass of the actual literal shift output. The coefficient is the
actual fair-source probability of eventually taking an above stopping leaf. -/
theorem literal_shift_atomic_mass (body : Stmt) (output a b : ℕ)
    (hnull : fairCantor {x | ∀ k, 1 ≤ k → streamClassify a b x k = none} = 0) :
    mass (fairCantor.map (compiledOutput body output a b)) =
      fairCantor {x | ∃ k, FirstCut a b x k true} *
        mass (fairCantor.map (P02A2.ObserverCore.output (programValue body output))) := by
  rw [literal_shift_mixture_law body output a b hnull, mass_countable_mixture,
    above_event_probability_sum, ← ENNReal.tsum_mul_right]
  apply tsum_congr
  intro l
  rw [leafLaw_mass]
  split <;> simp

/-- The leaf components expose the retained stopping prefix explicitly. -/
theorem leafLaw_eq_prefix_mixture_component (body : Stmt) (output : ℕ)
    {a b : ℕ} (l : StopLeaf a b) :
    leafLaw body output l =
      if l.1.2.2 then
        (fairCantor.map (P02A2.ObserverCore.output (programValue body output))).map
          (appendPrefix l.1.1 l.1.2.1)
      else fairCantor.map (appendPrefix l.1.1 l.1.2.1) := by
  unfold leafLaw leafTail
  split
  · rfl
  · rw [Measure.map_id]

/-- Affine defect identity in the actual above-event probability. -/
theorem literal_shift_defect_by_above_probability (body : Stmt) (output a b : ℕ)
    (hnull : fairCantor {x | ∀ k, 1 ≤ k → streamClassify a b x k = none} = 0) :
    defect (fairCantor.map (compiledOutput body output a b)) =
      1 - (fairCantor {x | ∃ k, FirstCut a b x k true}).toReal +
        (fairCantor {x | ∃ k, FirstCut a b x k true}).toReal *
          defect (fairCantor.map (P02A2.ObserverCore.output (programValue body output))) := by
  unfold defect
  rw [literal_shift_atomic_mass body output a b hnull, ENNReal.toReal_mul]
  ring

end P02.LiteralShift

#print axioms P02.LiteralShift.literal_shift_mixture_law
#print axioms P02.LiteralShift.literal_shift_atomic_mass

#print axioms P02.LiteralShift.literal_shift_defect_by_above_probability
