import LawCompletionCore

set_option autoImplicit false

namespace LawCompletion

open Set Filter
open scoped Topology

variable {X : Type*}

/-- Successive iterate ranges decrease for every self-map, without topology. -/
theorem range_succ_subset (f : X → X) (n : ℕ) :
    Set.range (f^[n + 1]) ⊆ Set.range (f^[n]) := by
  rintro y ⟨x, rfl⟩
  exact ⟨f x, (Function.iterate_succ_apply f n x).symm⟩

theorem range_antitone (f : X → X) : Antitone (fun n : ℕ => Set.range (f^[n])) :=
  antitone_nat_of_succ_le (range_succ_subset f)

section Compact
variable [MetricSpace X] [CompactSpace X]

private theorem range_compact (f : X → X) (hf : Continuous f) (n : ℕ) :
    IsCompact (Set.range (f^[n])) := isCompact_range (hf.iterate n)

private theorem range_closed (f : X → X) (hf : Continuous f) (n : ℕ) :
    IsClosed (Set.range (f^[n])) := (range_compact f hf n).isClosed

/-- Compactness earns a predecessor that itself survives every finite depth. -/
theorem compact_surviving_predecessor (f : X → X) (hf : Continuous f)
    (y : X) (hy : Survives f y) : ∃ x, Survives f x ∧ f x = y := by
  let A : ℕ → Set X := fun n => Set.range (f^[n]) ∩ {x | f x = y}
  have hclosed (n : ℕ) : IsClosed (A n) :=
    (range_closed f hf n).inter (isClosed_eq hf continuous_const)
  have hnonempty (n : ℕ) : (A n).Nonempty := by
    obtain ⟨z, hz⟩ := hy (n + 1)
    refine ⟨f^[n] z, ⟨⟨z, rfl⟩, ?_⟩⟩
    exact (Function.iterate_succ_apply' f n z).symm.trans hz
  obtain ⟨x, hx⟩ := IsCompact.nonempty_iInter_of_sequence_nonempty_isCompact_isClosed A
    (fun n => Set.inter_subset_inter_left _ (range_succ_subset f n)) hnonempty
    (hclosed 0).isCompact hclosed
  have hx' : ∀ n, x ∈ A n := Set.mem_iInter.mp hx
  exact ⟨x, fun n => (hx' n).1, (hx' 0).2⟩

/-- Classical predecessor choice yields one compatible infinite sequence from any survivor. -/
theorem compact_survivor_realized (f : X → X) (hf : Continuous f)
    (y : X) (hy : Survives f y) : ∃ b, Backward f b ∧ b 0 = y := by
  classical
  let S := {x : X // Survives f x}
  have hp (x : S) : ∃ z : S, f z.val = x.val := by
    obtain ⟨z, hz, hzy⟩ := compact_surviving_predecessor f hf x.val x.property
    exact ⟨⟨z, hz⟩, hzy⟩
  let p : S → S := fun x => Classical.choose (hp x)
  have hpf (x : S) : f (p x).val = x.val := Classical.choose_spec (hp x)
  let yS : S := ⟨y, hy⟩
  refine ⟨fun n => (p^[n] yS).val, ?_, rfl⟩
  intro i
  change (p^[i] yS).val = f (p^[i + 1] yS).val
  rw [Function.iterate_succ_apply']
  exact (hpf _).symm

/-- Exact agreement of finite-depth survivors and starts of compatible infinite realizations. -/
theorem compact_survival_iff_realized (f : X → X) (hf : Continuous f) (y : X) :
    Survives f y ↔ ∃ b, Backward f b ∧ b 0 = y := by
  constructor
  · exact compact_survivor_realized f hf y
  · rintro ⟨b, hb, rfl⟩
    exact backward_survives f b hb 0

/-- No nonemptiness premise is needed here: exact uniqueness already includes existence. -/
theorem compact_unique_backward_singleton (f : X → X) (hf : Continuous f)
    (hu : UniqueBackward f) : ∃ e, SingletonSurvival f e := by
  obtain ⟨e, he, hconst⟩ := unique_backward_constant f hu
  refine ⟨e, fun x => ⟨?_, ?_⟩⟩
  · intro hx
    obtain ⟨b, hb, hb0⟩ := compact_survivor_realized f hf x hx
    exact hb0.symm.trans (congrFun (hconst b hb) 0)
  · intro hxe
    subst x
    exact fixed_survives f e he

/-- Nested compact ranges with singleton intersection shrink uniformly to that point. -/
theorem compact_singleton_uniform (f : X → X) (hf : Continuous f)
    (e : X) (hs : SingletonSurvival f e) : UniformAttraction f e := by
  intro ε hε
  have hN : ∃ N : ℕ, ∀ y ∈ Set.range (f^[N]), dist y e < ε := by
    by_contra h
    push_neg at h
    let A : ℕ → Set X := fun n => Set.range (f^[n]) ∩ {y | ε ≤ dist y e}
    have hclosed (n : ℕ) : IsClosed (A n) :=
      (range_closed f hf n).inter (isClosed_le continuous_const (continuous_id.dist continuous_const))
    have hnonempty (n : ℕ) : (A n).Nonempty := by
      obtain ⟨y, hy, hd⟩ := h n
      exact ⟨y, hy, hd⟩
    obtain ⟨y, hy⟩ := IsCompact.nonempty_iInter_of_sequence_nonempty_isCompact_isClosed A
      (fun n => Set.inter_subset_inter_left _ (range_succ_subset f n)) hnonempty
      (hclosed 0).isCompact hclosed
    have hy' : ∀ n, y ∈ A n := Set.mem_iInter.mp hy
    have hye : y = e := (hs y).mp (fun n => (hy' n).1)
    have hd : ε ≤ dist y e := (hy' 0).2
    rw [hye, dist_self] at hd
    exact (not_le_of_gt hε) hd
  obtain ⟨N, hN⟩ := hN
  refine ⟨N, fun n hn x => ?_⟩
  exact hN _ (range_antitone f hn ⟨x, rfl⟩)

/-- The first equivalence in the compact repair. -/
theorem compact_singleton_iff_unique_backward (f : X → X) (hf : Continuous f) :
    (∃ e, SingletonSurvival f e) ↔ UniqueBackward f := by
  constructor
  · rintro ⟨e, he⟩
    exact singleton_unique_backward f e he
  · exact compact_unique_backward_singleton f hf

/-- The second equivalence uses uniform, not merely pointwise, attraction. -/
theorem compact_singleton_iff_uniform_fixed (f : X → X) (hf : Continuous f) :
    (∃ e, SingletonSurvival f e) ↔ ∃ e, f e = e ∧ UniformAttraction f e := by
  constructor
  · rintro ⟨e, he⟩
    exact ⟨e, singleton_fixed f e he, compact_singleton_uniform f hf e he⟩
  · rintro ⟨e, he, hu⟩
    exact ⟨e, uniform_fixed_singleton f e he hu⟩

/-- Universal compact-metric repair stated with standard uniform convergence. -/
theorem compact_completion_equivalences [Nonempty X] (f : X → X) (hf : Continuous f) :
    ((∃ e, SingletonSurvival f e) ↔ UniqueBackward f) ∧
    (UniqueBackward f ↔ ∃ e, f e = e ∧
      TendstoUniformly (fun n : ℕ => f^[n]) (fun _ => e) atTop) := by
  refine ⟨compact_singleton_iff_unique_backward f hf, ?_⟩
  rw [← compact_singleton_iff_unique_backward f hf, compact_singleton_iff_uniform_fixed f hf]
  exact exists_congr (fun e => and_congr_right (fun _ => uniform_iff_tendstoUniformly f e))

end Compact
end LawCompletion
