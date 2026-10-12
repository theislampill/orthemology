import GuardedTree
import Mathlib.Data.Fintype.Powerset
import LocalFintypeProd

namespace GuardedTree
variable {J E R : Type*} [DecidableEq E] (G : Grammar J E R)
open Tree

namespace Context

def comp : Context G → Context G → Context G
  | .hole, D => D
  | .step r i s inner, D => .step r i s (comp inner D)

omit [DecidableEq E] in
theorem fill_comp (C D : Context G) (t : Tree G) :
    (comp G C D).fill G t = C.fill G (D.fill G t) := by
  induction C with
  | hole => rfl
  | step r i s inner ih => simp only [comp, fill, ih]

end Context

inductive Branch : Tree G → List (Tree G) → Prop
  | root (t : Tree G) : Branch t [t]
  | down (r : R) (child : Fin (G.arity r) → Tree G) (i : Fin (G.arity r))
      (p : List (Tree G)) : Branch (child i) p → Branch (.node r child) (.node r child :: p)

omit [DecidableEq E] in
theorem branch_member_context {t : Tree G} {p : List (Tree G)} (h : Branch G t p)
    {d : Tree G} (hd : d ∈ p) : ∃ C : Context G, t = C.fill G d := by
  induction h with
  | root t =>
    have heq : d = t := by simpa using hd
    subst d
    exact ⟨.hole, rfl⟩
  | down r child i p _ ih =>
    rcases List.mem_cons.mp hd with heq | hmem
    · subst d; exact ⟨.hole, rfl⟩
    · obtain ⟨C, hC⟩ := ih hmem
      refine ⟨.step r i child C, ?_⟩
      simp only [Context.fill, ← hC, Function.update_eq_self]

theorem reduced_hole (t d : Tree G) (C : Context G)
    (ht : Reduced G t) (heq : t = C.fill G d) : Reduced G d := by
  intro outer inner leaf hi hd hs
  apply ht (C.comp G outer) inner leaf hi
  · rw [Context.fill_comp, ← hd, ← heq]
  · exact hs

def state (t : Tree G) : J × Finset E := (judgement G t, support G t)

theorem reduced_branch_nodup {t : Tree G} {p : List (Tree G)}
    (h : Branch G t p) (ht : Reduced G t) : (p.map (state G)).Nodup := by
  induction h with
  | root t => simp
  | down r child i p hp ih =>
    apply List.nodup_cons.mpr
    constructor
    · intro hmem
      obtain ⟨d, hd, heq⟩ := List.mem_map.mp hmem
      obtain ⟨C, hC⟩ := branch_member_context G hp hd
      apply ht (.hole) (.step r i child C) d (by intro hf; cases hf)
      · simp only [Context.fill, ← hC, Function.update_eq_self]
      · simpa only [Context.fill, ← hC, Function.update_eq_self] using
          (Prod.mk.inj heq)
    · apply ih
      apply reduced_hole G (.node r child) (child i) (.step r i child .hole) ht
      simp only [Context.fill, Function.update_eq_self]

theorem hole_support_subset (C : Context G) (t : Tree G) :
    support G t ⊆ support G (C.fill G t) := by
  induction C with
  | hole => exact Finset.Subset.refl _
  | step r i siblings inner ih =>
    intro e he
    apply Finset.mem_union.mpr
    right
    apply Finset.mem_biUnion.mpr
    exact ⟨i, Finset.mem_univ i, by simpa using ih he⟩

theorem branch_support_subset {t : Tree G} {p : List (Tree G)} (h : Branch G t p)
    {d : Tree G} (hd : d ∈ p) : support G d ⊆ support G t := by
  obtain ⟨C, heq⟩ := branch_member_context G h hd
  rw [heq]
  exact hole_support_subset G C d

def rankState (t : Tree G) : J × ℕ := (judgement G t, (support G t).card)

/-- Nested finite supports of the same cardinality are equal, so judgement
plus support cardinality is injective along each reduced branch. -/
theorem reduced_branch_rank_nodup {t : Tree G} {p : List (Tree G)}
    (h : Branch G t p) (ht : Reduced G t) : (p.map (rankState G)).Nodup := by
  induction h with
  | root t => simp
  | down r child i p hp ih =>
    apply List.nodup_cons.mpr
    constructor
    · intro hmem
      obtain ⟨d, hd, heq⟩ := List.mem_map.mp hmem
      obtain ⟨C, hC⟩ := branch_member_context G hp hd
      have hsub : support G d ⊆ support G (.node r child) := by
        have hw := hole_support_subset G (.step r i child C) d
        simpa only [Context.fill, ← hC, Function.update_eq_self] using hw
      have hsupport : support G d = support G (.node r child) :=
        Finset.eq_of_subset_of_card_le hsub (Prod.mk.inj heq).2.ge
      apply ht (.hole) (.step r i child C) d (by intro hf; cases hf)
      · simp only [Context.fill, ← hC, Function.update_eq_self]
      · simpa only [Context.fill, ← hC, Function.update_eq_self] using
          And.intro (Prod.mk.inj heq).1 hsupport
    · apply ih
      apply reduced_hole G (.node r child) (child i) (.step r i child .hole) ht
      simp only [Context.fill, Function.update_eq_self]

/-- The source-report upper bound: height counts rule occurrences, and
supports decrease by inclusion along a branch. Finiteness of E is not needed
for this exact-root-support bound because each tree support is a finset. -/
theorem reduced_branch_length_le_exact [Fintype J]
    {t : Tree G} {p : List (Tree G)} (h : Branch G t p) (ht : Reduced G t) :
    p.length ≤ Fintype.card J * ((support G t).card + 1) := by
  classical
  let ranks := (p.map (rankState G)).toFinset
  have hsub : ranks ⊆ (Finset.univ : Finset J) ×ˢ
      Finset.range ((support G t).card + 1) := by
    intro x hx
    obtain ⟨d, hd, rfl⟩ := List.mem_map.mp (List.mem_toFinset.mp hx)
    apply Finset.mem_product.mpr
    refine ⟨Finset.mem_univ _, Finset.mem_range.mpr ?_⟩
    exact Nat.lt_succ_of_le (Finset.card_le_card (branch_support_subset G h hd))
  have hc := Finset.card_le_card hsub
  have hn := List.toFinset_card_of_nodup (reduced_branch_rank_nodup G h ht)
  simpa only [ranks, hn, List.length_map, Finset.card_product, Finset.card_univ,
    Finset.card_range] using hc

/-- Every valid finite tree has a no-dearer exact-state representative satisfying
n(|S|+1), established from structural pruning and support nesting. -/
theorem exists_bounded_representative_exact [Fintype J]
    (hw : ∀ r, 0 ≤ G.price r) (t : Tree G) (ht : Valid G t) :
    ∃ u : Tree G, Valid G u ∧ judgement G u = judgement G t ∧
      support G u = support G t ∧ cost G u ≤ cost G t ∧
      ∀ p, Branch G u p → p.length ≤ Fintype.card J * ((support G t).card + 1) := by
  obtain ⟨u, hu, hq, hs, hc, hr⟩ := exists_reduced_representative G hw t ht
  refine ⟨u, hu, hq, hs, hc, ?_⟩
  intro p hp
  simpa only [hs] using reduced_branch_length_le_exact G hp hr

/-- Uniform finite-evidence corollary n(m+1). -/
theorem exists_bounded_representative_uniform [Fintype J] [Fintype E]
    (hw : ∀ r, 0 ≤ G.price r) (t : Tree G) (ht : Valid G t) :
    ∃ u : Tree G, Valid G u ∧ judgement G u = judgement G t ∧
      support G u = support G t ∧ cost G u ≤ cost G t ∧
      ∀ p, Branch G u p → p.length ≤ Fintype.card J * (Fintype.card E + 1) := by
  obtain ⟨u, hu, hq, hs, hc, hb⟩ := exists_bounded_representative_exact G hw t ht
  refine ⟨u, hu, hq, hs, hc, fun p hp => (hb p hp).trans ?_⟩
  exact Nat.mul_le_mul_left _ (Nat.add_le_add_right (Finset.card_le_univ _) 1)

/-- A first finite bound, directly from the no-repeated-state normal form.
This is intentionally weaker than the sharp n(m+1) support-chain bound. -/
theorem reduced_branch_length_le [Fintype J] [Fintype E]
    {t : Tree G} {p : List (Tree G)} (h : Branch G t p) (ht : Reduced G t) :
    p.length ≤ Fintype.card J * 2 ^ Fintype.card E := by
  have hb := (reduced_branch_nodup G h ht).length_le_card
  simpa only [List.length_map, Fintype.card_prod, Fintype.card_finset] using hb

/-- Every valid finite tree has a no-dearer same-exact-state representative
whose every branch is bounded by the finite number of possible exact states. -/
theorem exists_bounded_representative [Fintype J] [Fintype E]
    (hw : ∀ r, 0 ≤ G.price r) (t : Tree G) (ht : Valid G t) :
    ∃ u : Tree G, Valid G u ∧ judgement G u = judgement G t ∧
      support G u = support G t ∧ cost G u ≤ cost G t ∧
      ∀ p, Branch G u p → p.length ≤ Fintype.card J * 2 ^ Fintype.card E := by
  obtain ⟨u, hu, hq, hs, hc, hr⟩ := exists_reduced_representative G hw t ht
  exact ⟨u, hu, hq, hs, hc, fun _ hp => reduced_branch_length_le G hp hr⟩

#print axioms exists_bounded_representative_uniform
#print axioms exists_bounded_representative_exact
#print axioms reduced_branch_nodup
#print axioms exists_bounded_representative
end GuardedTree
