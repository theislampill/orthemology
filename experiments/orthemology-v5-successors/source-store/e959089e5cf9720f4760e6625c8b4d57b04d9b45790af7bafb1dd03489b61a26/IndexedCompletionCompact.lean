import IndexedCompletionCore

set_option autoImplicit false

namespace IndexedCompletion

open Set Filter
open scoped Topology

universe u
variable {X : ℕ → Type u}
variable [∀ i, TopologicalSpace (X i)] [∀ i, CompactSpace (X i)] [∀ i, T2Space (X i)]
variable [∀ i, Nonempty (X i)]

/-- Closed finite compatibility constraints in the compact product of all coordinate spaces. -/
def PartialCompatible (f : Bonding X) (n : ℕ) : Set (∀ i, X i) :=
  {b | ∀ i < n, b i = f i (b (i + 1))}

omit [∀ i, CompactSpace (X i)] [∀ i, Nonempty (X i)] in
theorem partial_closed (f : Bonding X) (hf : ∀ i, Continuous (f i)) (n : ℕ) :
    IsClosed (PartialCompatible f n) := by
  have heq : PartialCompatible f n = ⋂ i, ⋂ (_ : i < n), {b | b i = f i (b (i + 1))} := by
    ext b
    simp [PartialCompatible]
  rw [heq]
  apply isClosed_iInter
  intro i
  apply isClosed_iInter
  intro _
  exact isClosed_eq (continuous_apply i) ((hf i).comp (continuous_apply (i + 1)))

omit [∀ i, TopologicalSpace (X i)] [∀ i, CompactSpace (X i)] [∀ i, T2Space (X i)] [∀ i, Nonempty (X i)] in
theorem partial_decreasing (f : Bonding X) (n : ℕ) :
    PartialCompatible f (n + 1) ⊆ PartialCompatible f n := by
  intro b hb i hi
  exact hb i (by omega)

omit [∀ i, TopologicalSpace (X i)] [∀ i, CompactSpace (X i)] [∀ i, T2Space (X i)] in
theorem partial_nonempty (f : Bonding X) (n : ℕ) : (PartialCompatible f n).Nonempty := by
  let z : X n := Classical.choice inferInstance
  exact ⟨finitePath f n z, fun i hi => finitePath_compatible f n z i hi⟩

/-- Standard compact inverse-limit existence, earned from compact finite path sets. -/
theorem realization_exists (f : Bonding X) (hf : ∀ i, Continuous (f i)) :
    ∃ b, Compatible f b := by
  obtain ⟨b, hb⟩ := IsCompact.nonempty_iInter_of_sequence_nonempty_isCompact_isClosed
    (PartialCompatible f) (partial_decreasing f) (partial_nonempty f)
    (partial_closed f hf 0).isCompact (partial_closed f hf)
  refine ⟨b, fun i => ?_⟩
  exact (Set.mem_iInter.mp hb (i + 1)) i (by omega)

/-- Every finite-depth surviving coordinate is the projection of an actual full realization. -/
theorem survivor_realized (f : Bonding X) (hf : ∀ i, Continuous (f i))
    (i : ℕ) (y : X i) (hy : Survives f i y) :
    ∃ b, Compatible f b ∧ b i = y := by
  let A : ℕ → Set (∀ k, X k) := fun n => PartialCompatible f n ∩ {b | b i = y}
  have hclosed (n : ℕ) : IsClosed (A n) :=
    (partial_closed f hf n).inter (isClosed_eq (continuous_apply i) continuous_const)
  have hnonempty (n : ℕ) : (A n).Nonempty := by
    obtain ⟨z, hz⟩ := hy (max i n) (le_max_left i n)
    refine ⟨finitePath f (max i n) z, ?_, ?_⟩
    · intro k hk
      exact finitePath_compatible f (max i n) z k (lt_of_lt_of_le hk (le_max_right i n))
    · change finitePath f (max i n) z i = y
      rw [finitePath_at f (max i n) z i (le_max_left i n)]
      exact hz
  obtain ⟨b, hb⟩ := IsCompact.nonempty_iInter_of_sequence_nonempty_isCompact_isClosed A
    (fun n => Set.inter_subset_inter_left _ (partial_decreasing f n)) hnonempty
    (hclosed 0).isCompact hclosed
  have hb' : ∀ n, b ∈ A n := Set.mem_iInter.mp hb
  exact ⟨b, (fun k => (hb' (k + 1)).1 k (by omega)), (hb' 0).2⟩

theorem survival_iff_projection (f : Bonding X) (hf : ∀ i, Continuous (f i))
    (i : ℕ) (y : X i) : Survives f i y ↔ ∃ b, Compatible f b ∧ b i = y := by
  constructor
  · exact survivor_realized f hf i y
  · rintro ⟨b, hb, rfl⟩
    exact compatible_survives f b hb i

theorem survivor_exists (f : Bonding X) (hf : ∀ i, Continuous (f i)) (i : ℕ) :
    ∃ y : X i, Survives f i y := by
  obtain ⟨b, hb⟩ := realization_exists f hf
  exact ⟨b i, compatible_survives f b hb i⟩

/-- All coordinates are essential: the premise is not singleton survival at coordinate zero. -/
theorem all_singleton_iff_unique (f : Bonding X) (hf : ∀ i, Continuous (f i)) :
    AllSingleton f ↔ UniqueRealization f := by
  constructor
  · intro hs
    obtain ⟨b, hb⟩ := realization_exists f hf
    refine ⟨b, hb, fun c hc => ?_⟩
    funext i
    obtain ⟨e, he⟩ := hs i
    exact ((he (c i)).mp (compatible_survives f c hc i)).trans
      ((he (b i)).mp (compatible_survives f b hb i)).symm
  · rintro ⟨b, hb, huniq⟩
    intro i
    refine ⟨b i, fun y => ⟨?_, ?_⟩⟩
    · intro hy
      obtain ⟨c, hc, hci⟩ := survivor_realized f hf i y hy
      exact hci.symm.trans (congrFun (huniq c hc) i)
    · intro hy
      rw [hy]
      exact compatible_survives f b hb i

end IndexedCompletion
