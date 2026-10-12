import Catalogue
import Mathlib.Data.Finset.Max

namespace GuardedTree
variable {J E R : Type*} [DecidableEq E] (G : Grammar J E R)
open Tree

/-- A valid exact state has a nonempty explicitly constructed bounded family. -/
theorem exactCatalogue_nonempty [Fintype J] [Fintype R]
    (hw : ∀ r, 0 ≤ G.price r) (t : Tree G) (ht : Valid G t) :
    (exactCatalogue G (Fintype.card J * ((support G t).card + 1))
      (judgement G t) (support G t)).Nonempty := by
  obtain ⟨u, hu, hq, hs, _, hb⟩ := exists_bounded_representative_exact G hw t ht
  exact ⟨u, (mem_exactCatalogue_iff G _ _ _ _).mpr ⟨hb, hu, hq, hs⟩⟩

/-- An actual valid same-judgement, exact-support tree attains the least price
among all finite trees in that exact state. The minimum is derived from the
finite bounded syntax family; no minimum or admitted catalogue is a premise.
The evidence universe E may be infinite. -/
theorem exists_minimum_exact [Fintype J] [Fintype R]
    (hw : ∀ r, 0 ≤ G.price r) (t : Tree G) (ht : Valid G t) :
    ∃ u : Tree G, Valid G u ∧ judgement G u = judgement G t ∧
      support G u = support G t ∧
      Bounded G (Fintype.card J * ((support G t).card + 1)) u ∧
      ∀ v : Tree G, Valid G v → judgement G v = judgement G t →
        support G v = support G t → cost G u ≤ cost G v := by
  classical
  let A := exactCatalogue G (Fintype.card J * ((support G t).card + 1))
    (judgement G t) (support G t)
  obtain ⟨u, hu, hmin⟩ := Finset.exists_min_image A (cost G)
    (exactCatalogue_nonempty G hw t ht)
  obtain ⟨hb, hv, hq, hs⟩ := (mem_exactCatalogue_iff G _ _ _ _).mp hu
  refine ⟨u, hv, hq, hs, hb, ?_⟩
  intro v hv hqv hsv
  obtain ⟨w, hwv, hwq, hws, hwc, hwb⟩ := exists_bounded_representative_exact G hw v hv
  have hmem : w ∈ A := (mem_exactCatalogue_iff G _ _ _ _).mpr
    ⟨by simpa only [hsv] using hwb, hwv, hwq.trans hqv, hws.trans hsv⟩
  exact (hmin w hmem).trans hwc

/-- Finite R also bounds all used evidence, even if the ambient evidence type
is infinite. Unused external tokens do not enlarge this fixed grammar. -/
def grammarSupport [Fintype R] : Finset E :=
  Finset.univ.biUnion G.localSupport

theorem support_subset_grammarSupport [Fintype R] (t : Tree G) :
    support G t ⊆ grammarSupport G := by
  induction t with
  | node r child ih =>
    intro e he
    rcases Finset.mem_union.mp he with hlocal | hchild
    · exact Finset.mem_biUnion.mpr ⟨r, Finset.mem_univ _, hlocal⟩
    · obtain ⟨i, _, hi⟩ := Finset.mem_biUnion.mp hchild
      exact ih i hi

/-- A single uniform height for the fixed finite grammar, without Fintype E. -/
def grammarBound [Fintype J] [Fintype R] : ℕ :=
  Fintype.card J * ((grammarSupport G).card + 1)

theorem exists_bounded_representative_grammar [Fintype J] [Fintype R]
    (hw : ∀ r, 0 ≤ G.price r) (t : Tree G) (ht : Valid G t) :
    ∃ u : Tree G, Valid G u ∧ judgement G u = judgement G t ∧
      support G u = support G t ∧ cost G u ≤ cost G t ∧
      Bounded G (grammarBound G) u := by
  obtain ⟨u, hu, hq, hs, hc, hb⟩ := exists_bounded_representative_exact G hw t ht
  refine ⟨u, hu, hq, hs, hc, fun p hp => (hb p hp).trans ?_⟩
  exact Nat.mul_le_mul_left _ (Nat.add_le_add_right
    (Finset.card_le_card (support_subset_grammarSupport G t)) 1)

/-- The finite collection is generated from grammar syntax and actual validity. -/
noncomputable def validCatalogue [Fintype J] [Fintype R] : Finset (Tree G) := by
  classical
  exact (boundedCatalogue G (grammarBound G)).filter (Valid G)

theorem mem_validCatalogue_iff [Fintype J] [Fintype R] (t : Tree G) :
    t ∈ validCatalogue G ↔ Bounded G (grammarBound G) t ∧ Valid G t := by
  classical
  simp only [validCatalogue, Finset.mem_filter, mem_boundedCatalogue_iff]

theorem validCatalogue_cover [Fintype J] [Fintype R]
    (hw : ∀ r, 0 ≤ G.price r) (t : Tree G) (ht : Valid G t) :
    ∃ u ∈ validCatalogue G, judgement G u = judgement G t ∧
      support G u = support G t ∧ cost G u ≤ cost G t := by
  obtain ⟨u, hu, hq, hs, hc, hb⟩ := exists_bounded_representative_grammar G hw t ht
  exact ⟨u, (mem_validCatalogue_iff G u).mpr ⟨hb, hu⟩, hq, hs, hc⟩

#print axioms exists_minimum_exact
#print axioms support_subset_grammarSupport
#print axioms validCatalogue_cover
end GuardedTree
