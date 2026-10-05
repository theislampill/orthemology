import IndexedCompletionCompact

set_option autoImplicit false

namespace IndexedCompletion

open Set Filter
open scoped Topology

universe u
variable {X : ℕ → Type u}
variable [∀ i, MetricSpace (X i)] [∀ i, CompactSpace (X i)] [∀ i, Nonempty (X i)]

/-- Below i the range is set to univ solely to index a decreasing sequence by every natural.
    At every relevant j >= i it is exactly the actual finite-composite range. -/
def extensionRange (f : Bonding X) (i j : ℕ) : Set (X i) :=
  if h : i ≤ j then Set.range (transport f i j h) else Set.univ

omit [∀ i, MetricSpace (X i)] [∀ i, CompactSpace (X i)] [∀ i, Nonempty (X i)] in
@[simp] theorem extensionRange_of_le (f : Bonding X) (i j : ℕ) (h : i ≤ j) :
    extensionRange f i j = Set.range (transport f i j h) := by simp [extensionRange, h]

omit [∀ i, MetricSpace (X i)] [∀ i, CompactSpace (X i)] [∀ i, Nonempty (X i)] in
theorem range_step (f : Bonding X) (i j : ℕ) :
    extensionRange f i (j + 1) ⊆ extensionRange f i j := by
  by_cases hij : i ≤ j
  · rw [extensionRange_of_le f i j hij, extensionRange_of_le f i (j + 1) (by omega)]
    rintro y ⟨z, rfl⟩
    exact ⟨f j z, (transport_succ f i j hij z).symm⟩
  · simp [extensionRange, hij]

omit [∀ i, MetricSpace (X i)] [∀ i, CompactSpace (X i)] [∀ i, Nonempty (X i)] in
theorem ranges_antitone (f : Bonding X) (i : ℕ) : Antitone (extensionRange f i) :=
  antitone_nat_of_succ_le (range_step f i)

omit [∀ i, Nonempty (X i)] in
theorem extensionRange_closed (f : Bonding X) (hf : ∀ i, Continuous (f i)) (i j : ℕ) :
    IsClosed (extensionRange f i j) := by
  by_cases h : i ≤ j
  · rw [extensionRange_of_le f i j h]
    exact (isCompact_range (transport_continuous f hf i j h)).isClosed
  · simp [extensionRange, h]

omit [∀ i, MetricSpace (X i)] [∀ i, CompactSpace (X i)] [∀ i, Nonempty (X i)] in
theorem survival_iff_all_ranges (f : Bonding X) (i : ℕ) (x : X i) :
    Survives f i x ↔ ∀ j, x ∈ extensionRange f i j := by
  constructor
  · intro hx j
    by_cases h : i ≤ j
    · rw [extensionRange_of_le f i j h]
      exact hx j h
    · simp [extensionRange, h]
  · intro hx j h
    simpa only [extensionRange_of_le f i j h] using hx j

/-- Pairwise epsilon shrinkage of the whole finite-extension range, separately for each i. -/
def CoordinateForgetting (f : Bonding X) : Prop :=
  ∀ i (ε : ℝ), 0 < ε → ∃ N : ℕ, ∀ j ≥ N, ∀ h : i ≤ j, ∀ u v : X j,
    dist (transport f i j h u) (transport f i j h v) < ε

/-- One bound covers all coordinates in each fixed finite horizon. H does not vary after N is chosen. -/
def HorizonForgetting (f : Bonding X) : Prop :=
  ∀ H (ε : ℝ), 0 < ε → ∃ N : ℕ, ∀ j ≥ N, ∀ hH : H ≤ j,
    ∀ i (hi : i ≤ H), ∀ u v : X j,
      dist (transport f i j (hi.trans hH) u) (transport f i j (hi.trans hH) v) < ε

/-- Uniformity over remote boundary values at each fixed coordinate, with a varying target b_i. -/
def CoordinateAttraction (f : Bonding X) (b : ∀ i, X i) : Prop :=
  ∀ i (ε : ℝ), 0 < ε → ∃ N : ℕ, ∀ j ≥ N, ∀ h : i ≤ j, ∀ z : X j,
    dist (transport f i j h z) (b i) < ε

def HorizonAttraction (f : Bonding X) (b : ∀ i, X i) : Prop :=
  ∀ H (ε : ℝ), 0 < ε → ∃ N : ℕ, ∀ j ≥ N, ∀ hH : H ≤ j,
    ∀ i (hi : i ≤ H), ∀ z : X j,
      dist (transport f i j (hi.trans hH) z) (b i) < ε

omit [∀ i, Nonempty (X i)] in
/-- Compactness earns uniform shrinking at one fixed coordinate. -/
theorem singleton_coordinate_attraction (f : Bonding X) (hf : ∀ i, Continuous (f i))
    (i : ℕ) (e : X i) (hs : ∀ x, Survives f i x ↔ x = e) :
    ∀ ε : ℝ, 0 < ε → ∃ N : ℕ, ∀ j ≥ N, ∀ h : i ≤ j, ∀ z : X j,
      dist (transport f i j h z) e < ε := by
  intro ε hε
  have hN : ∃ N, ∀ y ∈ extensionRange f i N, dist y e < ε := by
    by_contra hn
    push_neg at hn
    let A : ℕ → Set (X i) := fun n => extensionRange f i n ∩ {y | ε ≤ dist y e}
    have hclosed (n : ℕ) : IsClosed (A n) :=
      (extensionRange_closed f hf i n).inter
        (isClosed_le continuous_const (continuous_id.dist continuous_const))
    have hnonempty (n : ℕ) : (A n).Nonempty := by
      obtain ⟨y, hy, hd⟩ := hn n
      exact ⟨y, hy, hd⟩
    obtain ⟨y, hy⟩ := IsCompact.nonempty_iInter_of_sequence_nonempty_isCompact_isClosed A
      (fun n => Set.inter_subset_inter_left _ (range_step f i n)) hnonempty
      (hclosed 0).isCompact hclosed
    have hy' : ∀ n, y ∈ A n := Set.mem_iInter.mp hy
    have hye : y = e := (hs y).mp ((survival_iff_all_ranges f i y).mpr (fun n => (hy' n).1))
    have hd : ε ≤ dist y e := (hy' 0).2
    rw [hye, dist_self] at hd
    exact (not_le_of_gt hε) hd
  obtain ⟨N, hN⟩ := hN
  refine ⟨N, fun j hj hij z => ?_⟩
  apply hN
  apply ranges_antitone f i hj
  rw [extensionRange_of_le f i j hij]
  exact ⟨z, rfl⟩

/-- Exact coordinatewise singleton survival gives uniform attraction to its compatible realization. -/
theorem all_singleton_attraction (f : Bonding X) (hf : ∀ i, Continuous (f i))
    (hs : AllSingleton f) : ∃ b, Compatible f b ∧ CoordinateAttraction f b := by
  obtain ⟨b, hb⟩ := realization_exists f hf
  refine ⟨b, hb, fun i => ?_⟩
  obtain ⟨e, he⟩ := hs i
  have hbi : b i = e := (he (b i)).mp (compatible_survives f b hb i)
  rw [hbi]
  exact singleton_coordinate_attraction f hf i e he

omit [∀ i, CompactSpace (X i)] [∀ i, Nonempty (X i)] in
theorem attraction_implies_forgetting (f : Bonding X) (b : ∀ i, X i)
    (ha : CoordinateAttraction f b) : CoordinateForgetting f := by
  intro i ε hε
  obtain ⟨N, hN⟩ := ha i (ε / 2) (half_pos hε)
  refine ⟨N, fun j hj hij u v => ?_⟩
  calc
    dist (transport f i j hij u) (transport f i j hij v) ≤
      dist (transport f i j hij u) (b i) + dist (b i) (transport f i j hij v) := dist_triangle _ _ _
    _ < ε / 2 + ε / 2 := add_lt_add (hN j hj hij u) (by simpa [dist_comm] using hN j hj hij v)
    _ = ε := add_halves ε

/-- Pairwise range shrinking forces at most one survivor; compact inverse-limit existence supplies one. -/
theorem forgetting_implies_all_singleton (f : Bonding X) (hf : ∀ i, Continuous (f i))
    (hd : CoordinateForgetting f) : AllSingleton f := by
  intro i
  obtain ⟨e, he⟩ := survivor_exists f hf i
  refine ⟨e, fun x => ⟨?_, ?_⟩⟩
  · intro hx
    apply eq_of_forall_dist_le
    intro ε hε
    obtain ⟨N, hN⟩ := hd i ε hε
    let j := max i N
    obtain ⟨u, hu⟩ := hx j (le_max_left i N)
    obtain ⟨v, hv⟩ := he j (le_max_left i N)
    rw [← hu, ← hv]
    exact (hN j (le_max_right i N) (le_max_left i N) u v).le
  · intro hxe
    rw [hxe]
    exact he

omit [∀ i, CompactSpace (X i)] [∀ i, Nonempty (X i)] in
theorem coordinate_iff_horizon_forgetting (f : Bonding X) :
    CoordinateForgetting f ↔ HorizonForgetting f := by
  classical
  constructor
  · intro hc H ε hε
    let N : ℕ → ℕ := fun i => Classical.choose (hc i ε hε)
    have hN (i : ℕ) := Classical.choose_spec (hc i ε hε)
    refine ⟨(Finset.range (H + 1)).sup N, fun j hj hH i hi u v => ?_⟩
    have hiF : i ∈ Finset.range (H + 1) := Finset.mem_range.mpr (by omega)
    have hij : N i ≤ j := (Finset.le_sup hiF).trans hj
    exact hN i j hij (hi.trans hH) u v
  · intro hh i ε hε
    obtain ⟨N, hN⟩ := hh i ε hε
    exact ⟨N, fun j hj hij u v => hN j hj hij i le_rfl u v⟩

omit [∀ i, CompactSpace (X i)] [∀ i, Nonempty (X i)] in
theorem coordinate_iff_horizon_attraction (f : Bonding X) (b : ∀ i, X i) :
    CoordinateAttraction f b ↔ HorizonAttraction f b := by
  classical
  constructor
  · intro hc H ε hε
    let N : ℕ → ℕ := fun i => Classical.choose (hc i ε hε)
    have hN (i : ℕ) := Classical.choose_spec (hc i ε hε)
    refine ⟨(Finset.range (H + 1)).sup N, fun j hj hH i hi z => ?_⟩
    have hiF : i ∈ Finset.range (H + 1) := Finset.mem_range.mpr (by omega)
    have hij : N i ≤ j := (Finset.le_sup hiF).trans hj
    exact hN i j hij (hi.trans hH) z
  · intro hh i ε hε
    obtain ⟨N, hN⟩ := hh i ε hε
    exact ⟨N, fun j hj hij z => hN j hj hij i le_rfl z⟩

/-- Four-way nonstationary equivalence, expressed by full-range epsilon bounds. -/
theorem nonuniform_completion_equivalences (f : Bonding X) (hf : ∀ i, Continuous (f i)) :
    (AllSingleton f ↔ UniqueRealization f) ∧
    (AllSingleton f ↔ CoordinateForgetting f) ∧
    (CoordinateForgetting f ↔ HorizonForgetting f) := by
  refine ⟨all_singleton_iff_unique f hf, ⟨?_, forgetting_implies_all_singleton f hf⟩,
    coordinate_iff_horizon_forgetting f⟩
  intro hs
  obtain ⟨b, _, hb⟩ := all_singleton_attraction f hf hs
  exact attraction_implies_forgetting f b hb

/-- Unique completion is equivalent to finite-horizon attraction to one compatible varying path. -/
theorem unique_iff_horizon_attraction (f : Bonding X) (hf : ∀ i, Continuous (f i)) :
    UniqueRealization f ↔ ∃ b, Compatible f b ∧ HorizonAttraction f b := by
  constructor
  · intro hu
    obtain ⟨b, hb, ha⟩ := all_singleton_attraction f hf ((all_singleton_iff_unique f hf).mpr hu)
    exact ⟨b, hb, (coordinate_iff_horizon_attraction f b).mp ha⟩
  · rintro ⟨b, _, ha⟩
    apply (all_singleton_iff_unique f hf).mp
    apply forgetting_implies_all_singleton f hf
    exact attraction_implies_forgetting f b ((coordinate_iff_horizon_attraction f b).mpr ha)

end IndexedCompletion
