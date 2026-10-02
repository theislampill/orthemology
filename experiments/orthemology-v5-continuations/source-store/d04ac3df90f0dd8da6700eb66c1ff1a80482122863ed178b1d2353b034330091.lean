import LiteralSamplerExecution

namespace Orthemology.RationalLaw
open MeasureTheory Set
open scoped ENNReal BigOperators
open P02A2.Q8Measure (fairCantor)
open Orthemology.Frontier Orthemology.Frontier.MealyMeasure
variable {H Y : Type*} [DecidableEq Y] [Fintype Y]

def rejectionCounts (L D : ℕ) (hDB : D ≤ 2^L) (row : H → Fin D → Y)
    (update : H → Y → H) (n : ℕ) (h : H) (rs : Fin n → ℕ) : Set Cantor :=
  ⋃ ys : Fin n → Y, historyJoint L D hDB row update n h ys rs

theorem measurableSet_rejectionCounts (L D : ℕ) (hDB : D ≤ 2^L) (row : H → Fin D → Y)
    (update : H → Y → H) (n : ℕ) (h : H) (rs : Fin n → ℕ) :
    MeasurableSet (rejectionCounts L D hDB row update n h rs) :=
  MeasurableSet.iUnion (fun _ => measurableSet_constraintEvent _)

/-- The actual waiting-count marginal is the same product of geometric laws for
all adaptive row choices. This is proved by summing literal fair-bit events. -/
theorem rejectionCounts_probability (L D : ℕ) (hD : 0 < D) (hDB : D ≤ 2^L)
    (row : H → Fin D → Y) (update : H → Y → H) (n : ℕ) (h : H) (rs : Fin n → ℕ) :
    fairCantor (rejectionCounts L D hDB row update n h rs) = clockMass L D n rs := by
  have hd : Pairwise (fun ys zs : Fin n → Y => Disjoint
      (historyJoint L D hDB row update n h ys rs) (historyJoint L D hDB row update n h zs rs)) := by
    intro ys zs hne
    exact Set.disjoint_left.mpr (fun x hy hz => hne (historyJoint_unique L D hDB row update n h hy hz).1)
  rw [rejectionCounts, measure_iUnion hd (fun _ => measurableSet_constraintEvent _), tsum_fintype]
  simp only [history_joint_probability L D hD hDB]
  rw [← Finset.sum_mul, historyMass_total D hD, one_mul]

theorem acceptedHistory_inter_rejectionCounts (L D : ℕ) (hDB : D ≤ 2^L)
    (row : H → Fin D → Y) (update : H → Y → H) (n : ℕ) (h : H)
    (ys : Fin n → Y) (rs : Fin n → ℕ) :
    acceptedHistory L D hDB row update n h ys ∩ rejectionCounts L D hDB row update n h rs =
      historyJoint L D hDB row update n h ys rs := by
  ext x
  constructor
  · rintro ⟨hy,hr⟩
    obtain ⟨ss,hs⟩ := Set.mem_iUnion.mp hy
    obtain ⟨zs,hz⟩ := Set.mem_iUnion.mp hr
    obtain ⟨hyz,hsr⟩ := historyJoint_unique L D hDB row update n h hs hz
    simpa only [← hyz] using hz
  · intro hh
    exact ⟨Set.mem_iUnion.mpr ⟨rs,hh⟩,Set.mem_iUnion.mpr ⟨ys,hh⟩⟩

/-- Finite accepted-history and waiting-count events factor into their actual
marginals. No independent-stopping-time or conditional freshness premise. -/
theorem history_clock_marginal_factorization (L D : ℕ) (hD : 0 < D) (hDB : D ≤ 2^L)
    (row : H → Fin D → Y) (update : H → Y → H) (n : ℕ) (h : H)
    (ys : Fin n → Y) (rs : Fin n → ℕ) :
    fairCantor (acceptedHistory L D hDB row update n h ys ∩
      rejectionCounts L D hDB row update n h rs) =
      fairCantor (acceptedHistory L D hDB row update n h ys) *
      fairCantor (rejectionCounts L D hDB row update n h rs) := by
  rw [acceptedHistory_inter_rejectionCounts, rejectionCounts_probability L D hD hDB,
    history_joint_probability L D hD hDB]
  congr 1
  exact (accepted_history_probability L D hD hDB row update n h ys).symm

end Orthemology.RationalLaw
