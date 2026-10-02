import PolicyTranscriptFiber
import Mathlib.Probability.Kernel.IonescuTulcea.Traj

noncomputable section
open MeasureTheory ProbabilityTheory Finset Preorder

namespace Orthemology.Tranche2.PolicyEmbedding
variable {R A Y : Type*} [DecidableEq A]

theorem observedHistory_drop (U : Finset A) (π : R → History A Y → A) (oracle : ℕ → A → Y)
    (seed : R) (X : Stack A Y) (n m : ℕ) (hm : m ≤ n) :
    (observedHistory U π oracle seed X n).drop (n-m) = observedHistory U π oracle seed X m := by
  induction n generalizing m with
  | zero =>
    have he : m = 0 := by omega
    subst m
    rfl
  | succ n ih =>
    by_cases he : m = n+1
    · subst m; simp
    · have hm' : m ≤ n := by omega
      have hsub : n+1-m = (n-m)+1 := by omega
      simp only [observedHistory,hsub,List.drop_succ_cons]
      exact ih m hm'

def reconstructPrefix (N : ℕ) (h : History A Y) : (i : Iic N) → History A Y :=
  fun i => h.drop (N-i.val)

theorem observedHistory_prefix_from_last (U : Finset A) (π : R → History A Y → A) (oracle : ℕ → A → Y)
    (seed : R) (X : Stack A Y) (N : ℕ) :
    frestrictLe N (observedHistory U π oracle seed X) =
      reconstructPrefix N (observedHistory U π oracle seed X N) := by
  funext i
  exact (observedHistory_drop U π oracle seed X N i.val (Finset.mem_Iic.mp i.property)).symm

section MeasureExtension
variable {E Ω : Type*} [MeasurableSpace E] [MeasurableSpace Ω]

/-- Finite prefix marginals determine an infinite sequence measure. -/
theorem measure_eq_of_prefix_maps (μ ν : Measure (ℕ → E)) [IsFiniteMeasure ν]
    (h : ∀ N, μ.map (frestrictLe N) = ν.map (frestrictLe N)) : μ = ν := by
  classical
  let P := fun I : Finset ℕ => ν.map I.restrict
  have hp : IsProjectiveLimit μ P := by
    intro I
    let N := I.sup id
    have hs : I ⊆ Iic N := I.subset_Iic_sup_id
    calc
      μ.map I.restrict = (μ.map (frestrictLe N)).map (Finset.restrict₂ (π := fun _ : ℕ => E) hs) := by
        rw [Measure.map_map (Finset.measurable_restrict₂ hs) (measurable_frestrictLe N)]
        rfl
      _ = (ν.map (frestrictLe N)).map (Finset.restrict₂ (π := fun _ : ℕ => E) hs) := by rw [h N]
      _ = P I := by
        rw [Measure.map_map (Finset.measurable_restrict₂ hs) (measurable_frestrictLe N)]
        rfl
  exact hp.unique (fun _ => rfl)

end MeasureExtension
end Orthemology.Tranche2.PolicyEmbedding
