import EndComponents
import RecurrentSupport

namespace HiddenParity.Adaptive
open Filter
open Orthemology.Tranche2.RecurrentSupport

variable {State Pair : Type*} [Fintype Pair] [DecidableEq Pair] [DecidableEq State]

omit [Fintype Pair] [DecidableEq Pair] [DecidableEq State] in
/-- A supported finite segment made entirely from E-pairs is an actual directed
path inside E, regardless of how the pairs were selected. -/
theorem retained_segment_reachable (source : Pair → State) (succ : Pair → Finset State)
    (x : ℕ → Pair) (E : Finset Pair) (n m : ℕ) (hnm : n ≤ m)
    (hRetain : ∀ k ≥ n, x k ∈ E)
    (hStep : ∀ k, source (x (k+1)) ∈ succ (x k)) :
    Reach source succ E (source (x n)) (source (x m)) := by
  induction m, hnm using Nat.le_induction with
  | base => exact Relation.ReflTransGen.refl
  | succ k hnk ih =>
      exact ih.tail ⟨x k, hRetain k hnk, rfl, hStep k⟩

omit [DecidableEq Pair] in
/-- Deterministic recurrence-to-graph theorem. Supported steps and recurrent
positive successors are concrete path properties; the probabilistic source
of those properties is established separately from raw iid tapes. -/
theorem recurrent_pairs_form_end_component
    (source : Pair → State) (succ : Pair → Finset State) (x : ℕ → Pair)
    (hStep : ∀ n, source (x (n+1)) ∈ succ (x n))
    (hSuccessors : ∀ e ∈ recurrentSet x, ∀ y ∈ succ e,
      ∃ᶠ n in atTop, x n = e ∧ source (x (n+1)) = y) :
    IsEndComponent source succ (recurrentSet x) := by
  obtain ⟨N, hN⟩ := eventually_atTop.mp (eventually_mem_recurrentSet x)
  refine ⟨recurrentSet_nonempty x, ?_, ?_, ?_⟩
  · intro e he
    obtain ⟨n, hn⟩ := ((mem_recurrentSet x e).mp he).exists
    exact ⟨source (x (n+1)), by simpa [hn] using hStep n⟩
  · intro e he y hy
    obtain ⟨n, hn, _, hny⟩ := frequently_atTop.mp (hSuccessors e he y hy) N
    exact Finset.mem_image.mpr ⟨x (n+1), hN (n+1) (by omega), hny⟩
  · intro s hs t ht
    obtain ⟨e, he, hes⟩ := Finset.mem_image.mp hs
    obtain ⟨f, hf, hft⟩ := Finset.mem_image.mp ht
    obtain ⟨n, hn, hne⟩ := frequently_atTop.mp ((mem_recurrentSet x e).mp he) N
    obtain ⟨m, hnm, hmf⟩ := frequently_atTop.mp ((mem_recurrentSet x f).mp hf) n
    have hpath := retained_segment_reachable source succ x (recurrentSet x) n m hnm
      (fun k hk => hN k (hn.trans hk)) hStep
    simpa [hne, hmf, hes, hft] using hpath

section Measurable
open MeasureTheory Set
variable [MeasurableSpace Pair] [MeasurableSingletonClass Pair]

omit [DecidableEq Pair] in
/-- Every predicate on the exact finite recurrent pair set is a measurable path
event. This permits transfer of the concrete end-component conclusion. -/
theorem measurable_recurrent_predicate (property : Finset Pair → Prop) :
    MeasurableSet {x : ℕ → Pair | property (recurrentSet x)} := by
  classical
  have heq : {x : ℕ → Pair | property (recurrentSet x)} =
      ⋃ (E : Finset Pair) (_ : property E), exactRecurrentEvent id E := by
    ext x
    simp only [Set.mem_setOf_eq, Set.mem_iUnion, exactRecurrentEvent, id_eq]
    constructor
    · intro h
      exact ⟨recurrentSet x, h, rfl⟩
    · rintro ⟨E, h, hE⟩
      exact hE ▸ h
  rw [heq]
  exact MeasurableSet.iUnion (fun E => MeasurableSet.iUnion (fun _ =>
    measurable_exactRecurrentEvent id (fun n => measurable_pi_apply n) E))

end Measurable
end HiddenParity.Adaptive
