import Mathlib.Data.Set.Finite.Basic
import Mathlib.Data.Finset.Lattice.Fold
import Mathlib.Data.Finset.SDiff
import Mathlib.Order.WithBot
import Mathlib.Tactic.Tauto

/-! The finite weighted residual-certificate theorem, independently of any
semantic or epistemic interpretation. Costs are finite elements of a linear
order; only the output cost type adds a top element for infeasibility. -/
namespace CertificateFrontier

variable {E C : Type*} [DecidableEq E] [LinearOrder C]
abbrev Pair (E C : Type*) := Finset E × C

/-- Product-order minimal support/cost pairs. Repeated pairs are already
identified by the finite-set representation. -/
def frontier (A : Finset (Pair E C)) : Finset (Pair E C) :=
  A.filter fun p => ∀ q ∈ A, q ≤ p → p ≤ q

@[simp] theorem mem_frontier {A : Finset (Pair E C)} {p : Pair E C} :
    p ∈ frontier A ↔ p ∈ A ∧ ∀ q ∈ A, q ≤ p → p ≤ q := by
  simp [frontier]

/-- An actual original pair realizes every retained frontier pair. -/
theorem frontier_subset (A : Finset (Pair E C)) : frontier A ⊆ A := by
  intro p hp
  exact (mem_frontier.mp hp).1

/-- Finiteness, rather than any assumption of a pre-normalized catalogue,
ensures that each pair has a retained pair weakly dominating it. -/
theorem exists_frontier_le {A : Finset (Pair E C)} {p : Pair E C} (hp : p ∈ A) :
    ∃ q ∈ frontier A, q ≤ p := by
  let B := A.filter (fun q => q ≤ p)
  have hpB : p ∈ B := by simp [B, hp]
  obtain ⟨q, hqB, hmin⟩ := B.finite_toSet.exists_minimal_wrt id B ⟨p, hpB⟩
  have hq := Finset.mem_filter.mp hqB
  refine ⟨q, mem_frontier.mpr ⟨hq.1, ?_⟩, hq.2⟩
  intro r hr hrq
  have hrB : r ∈ B := Finset.mem_filter.mpr ⟨hr, le_trans hrq hq.2⟩
  exact le_of_eq (hmin r hrB hrq)

/-- Least finite terminal cost among pairs whose missing support is supplied;
the top value means there is no eligible pair. -/
def cost (A : Finset (Pair E C)) (U : Finset E) : WithTop C :=
  A.inf fun p => if p.1 ⊆ U then (p.2 : WithTop C) else ⊤

/-- Exact attainment at every finite price threshold. -/
theorem cost_le_iff {A : Finset (Pair E C)} {U : Finset E} {c : C} :
    cost A U ≤ (c : WithTop C) ↔ ∃ p ∈ A, p.1 ⊆ U ∧ p.2 ≤ c := by
  rw [cost, Finset.inf_le_iff (WithTop.coe_lt_top c)]
  constructor
  · rintro ⟨p, hp, hle⟩
    by_cases hsub : p.1 ⊆ U
    · rw [if_pos hsub] at hle
      exact ⟨p, hp, hsub, WithTop.coe_le_coe.mp hle⟩
    · rw [if_neg hsub] at hle
      exact False.elim ((not_le_of_gt (WithTop.coe_lt_top c)) hle)
  · rintro ⟨p, hp, hsub, hle⟩
    exact ⟨p, hp, by simpa [hsub] using hle⟩

/-- Removing dominated pairs preserves the entire future cost function. -/
theorem cost_frontier (A : Finset (Pair E C)) (U : Finset E) :
    cost (frontier A) U = cost A U := by
  apply le_antisymm
  · apply Finset.le_inf
    intro p hp
    by_cases hsub : p.1 ⊆ U
    · simp only [if_pos hsub]
      obtain ⟨q, hq, hqp⟩ := exists_frontier_le hp
      exact cost_le_iff.mpr ⟨q, hq, hqp.1.trans hsub, hqp.2⟩
    · simp only [if_neg hsub]
      exact le_top
  · apply Finset.le_inf
    intro p hp
    by_cases hsub : p.1 ⊆ U
    · simp only [if_pos hsub]
      exact cost_le_iff.mpr ⟨p, frontier_subset A hp, hsub, le_rfl⟩
    · simp only [if_neg hsub]
      exact le_top

/-- Recover the unique frontier from the cost at a support and its immediate
one-token deletions. This includes empty supports (the deletion test is then
vacuous). No catalogue membership premise is assumed on the right. -/
theorem frontier_inverse {A : Finset (Pair E C)} {p : Pair E C} :
    p ∈ frontier A ↔
      cost A p.1 = (p.2 : WithTop C) ∧
      ∀ d ∈ p.1, (p.2 : WithTop C) < cost A (p.1.erase d) := by
  constructor
  · intro hp
    obtain ⟨hpA, hmin⟩ := mem_frontier.mp hp
    constructor
    · apply le_antisymm
      · exact cost_le_iff.mpr ⟨p, hpA, Finset.Subset.refl _, le_rfl⟩
      · apply Finset.le_inf
        intro q hq
        by_cases hsub : q.1 ⊆ p.1
        · simp only [if_pos hsub, WithTop.coe_le_coe]
          by_cases hcost : q.2 ≤ p.2
          · exact (hmin q hq ⟨hsub, hcost⟩).2
          · exact le_of_lt (lt_of_not_ge hcost)
        · simp only [if_neg hsub]
          exact le_top
    · intro d hd
      apply lt_of_not_ge
      intro hle
      obtain ⟨q, hq, hsub, hcost⟩ := cost_le_iff.mp hle
      have hpq := hmin q hq ⟨hsub.trans (Finset.erase_subset _ _), hcost⟩
      exact (Finset.not_mem_erase d p.1) (hsub (hpq.1 hd))
  · rintro ⟨heq, hdel⟩
    have support_eq : ∀ q ∈ A, q ≤ p → q.1 = p.1 := by
      intro q hq hqp
      apply Finset.Subset.antisymm hqp.1
      intro d hd
      apply Classical.byContradiction
      intro hn
      have hsub : q.1 ⊆ p.1.erase d := by
        intro x hx
        refine Finset.mem_erase.mpr ⟨?_, hqp.1 hx⟩
        intro hxd
        subst x
        exact hn hx
      have hle := cost_le_iff.mpr ⟨q, hq, hsub, hqp.2⟩
      exact (not_le_of_gt (hdel d hd)) hle
    have cost_ge : ∀ q ∈ A, q.1 ⊆ p.1 → p.2 ≤ q.2 := by
      intro q hq hsub
      have hle : cost A p.1 ≤ (q.2 : WithTop C) :=
        cost_le_iff.mpr ⟨q, hq, hsub, le_rfl⟩
      rw [heq] at hle
      exact WithTop.coe_le_coe.mp hle
    obtain ⟨q, hq, hsub, hcost⟩ := cost_le_iff.mp (le_of_eq heq)
    have hqeq : q = p := Prod.ext (support_eq q hq ⟨hsub, hcost⟩)
      (le_antisymm hcost (cost_ge q hq hsub))
    subst q
    apply mem_frontier.mpr
    refine ⟨hq, ?_⟩
    intro r hr hrp
    exact ⟨(support_eq r hr hrp).ge, cost_ge r hr hrp.1⟩

/-- Canonical necessity and sufficiency, across arbitrary finite catalogues.
Equality of all least-cost observations is exactly equality of frontiers. -/
theorem frontier_eq_iff_cost {A B : Finset (Pair E C)} :
    frontier A = frontier B ↔ ∀ U, cost A U = cost B U := by
  constructor
  · intro h U
    rw [← cost_frontier A U, h, cost_frontier B U]
  · intro h
    ext p
    simp only [frontier_inverse, h]

/-- The normalized representation is an antichain, derived rather than assumed. -/
theorem frontier_antichain {A : Finset (Pair E C)} {p q : Pair E C}
    (hp : p ∈ frontier A) (hq : q ∈ frontier A) (hpq : p ≤ q) : p = q := by
  exact le_antisymm hpq ((mem_frontier.mp hq).2 p (frontier_subset A hp) hpq)

/-- Repeated normalization has no effect. -/
theorem frontier_idempotent (A : Finset (Pair E C)) :
    frontier (frontier A) = frontier A :=
  frontier_eq_iff_cost.mpr (cost_frontier A)

/-- Subtract an acquired token set from each missing support. -/
def residual (A : Finset (Pair E C)) (T : Finset E) : Finset (Pair E C) :=
  A.image fun p => (p.1 \ T, p.2)

/-- Elementary support eligibility, with all acquisition sets explicit. -/
theorem residual_eligible (D T U : Finset E) :
    D \ T ⊆ U ↔ D ⊆ T ∪ U := by
  constructor
  · intro h d hd
    by_cases hdT : d ∈ T
    · exact Finset.mem_union.mpr (Or.inl hdT)
    · exact Finset.mem_union.mpr (Or.inr (h (Finset.mem_sdiff.mpr ⟨hd, hdT⟩)))
  · intro h d hd
    obtain ⟨hdD, hdT⟩ := Finset.mem_sdiff.mp hd
    exact (Finset.mem_union.mp (h hdD)).resolve_left hdT

/-- Exact residual cost law: future observation after T is old observation
under the union of T with the future evidence. -/
theorem cost_residual (A : Finset (Pair E C)) (T U : Finset E) :
    cost (residual A T) U = cost A (T ∪ U) := by
  simp only [cost, residual, Finset.inf_image, Function.comp_def, residual_eligible]

/-- Persistent acquisitions compose by union, independently of their order. -/
theorem residual_residual (A : Finset (Pair E C)) (K T : Finset E) :
    residual (residual A K) T = residual A (K ∪ T) := by
  simp only [residual, Finset.image_image]
  congr 1
  funext p
  apply Prod.ext
  · ext d
    simp only [Function.comp_apply, Finset.mem_sdiff, Finset.mem_union]
    tauto
  · rfl

/-- Normalize before or after acquisition; the final canonical frontier is
identical. This proves retained frontiers can be updated without old pairs. -/
theorem frontier_residual_normalize (A : Finset (Pair E C)) (T : Finset E) :
    frontier (residual (frontier A) T) = frontier (residual A T) := by
  apply frontier_eq_iff_cost.mpr
  intro U
  rw [cost_residual, cost_residual, cost_frontier]

/-- Equal frontier states remain equal after every common acquisition. -/
theorem residual_congruence {A B : Finset (Pair E C)}
    (h : frontier A = frontier B) (T : Finset E) :
    frontier (residual A T) = frontier (residual B T) := by
  rw [← frontier_residual_normalize A T, h, frontier_residual_normalize B T]

/-- Any decoder that recovers every future cost must distinguish different
canonical frontiers. No uniqueness of the decoder's encoding is asserted. -/
theorem summary_necessity {S : Type*}
    (summary : Finset (Pair E C) → S)
    (decode : S → Finset E → WithTop C)
    (correct : ∀ A U, decode (summary A) U = cost A U)
    {A B : Finset (Pair E C)} (h : summary A = summary B) :
    frontier A = frontier B := by
  apply frontier_eq_iff_cost.mpr
  intro U
  rw [← correct A U, h, correct B U]

/-- The paper's R_v(K), with one fixed scoped-verdict catalogue. -/
def inventoryFrontier (Γ : Finset (Pair E C)) (K : Finset E) : Finset (Pair E C) :=
  frontier (residual Γ K)

/-- The paper's F_{K,v}(U); finite minima are attained and empty minima are top. -/
def futureCost (Γ : Finset (Pair E C)) (K U : Finset E) : WithTop C :=
  cost Γ (K ∪ U)

/-- Theorem 1.1: canonical residual pairs recover the exact future minimum. -/
theorem inventory_cost_recovery (Γ : Finset (Pair E C)) (K U : Finset E) :
    cost (inventoryFrontier Γ K) U = futureCost Γ K U := by
  rw [inventoryFrontier, cost_frontier, cost_residual, futureCost]

/-- Theorem 1.2, including necessity, for two actual evidence inventories. -/
theorem inventory_canonical {Γ : Finset (Pair E C)} {K L : Finset E} :
    inventoryFrontier Γ K = inventoryFrontier Γ L ↔
      ∀ U, futureCost Γ K U = futureCost Γ L U := by
  simp only [inventoryFrontier, frontier_eq_iff_cost, cost_residual, futureCost]

/-- Theorem 1.3: recover the updated frontier using only the old frontier. -/
theorem inventory_update (Γ : Finset (Pair E C)) (K T : Finset E) :
    inventoryFrontier Γ (K ∪ T) = frontier (residual (inventoryFrontier Γ K) T) := by
  rw [inventoryFrontier, inventoryFrontier, frontier_residual_normalize, residual_residual]

/-- Theorem 1.3: equal inventory summaries remain equal under common additions. -/
theorem inventory_congruence {Γ : Finset (Pair E C)} {K L : Finset E}
    (h : inventoryFrontier Γ K = inventoryFrontier Γ L) (T : Finset E) :
    inventoryFrontier Γ (K ∪ T) = inventoryFrontier Γ (L ∪ T) := by
  rw [inventory_update, inventory_update, h]

/-- The exact per-verdict equivalence: verdict identity is retained, rather than
silently minimizing across different scoped conclusions. -/
theorem per_verdict_canonical {V : Type*} (Γ : V → Finset (Pair E C))
    (K L : Finset E) :
    (∀ v, inventoryFrontier (Γ v) K = inventoryFrontier (Γ v) L) ↔
    (∀ v U, futureCost (Γ v) K U = futureCost (Γ v) L U) := by
  simp only [inventory_canonical]

/-- Theorem 1.4: any exact per-verdict cost decoder must distinguish different
frontier tuples. This is minimality of equivalence classes, not of encodings. -/
theorem inventory_summary_necessity {V S : Type*}
    (Γ : V → Finset (Pair E C)) (summary : Finset E → S)
    (decode : S → V → Finset E → WithTop C)
    (correct : ∀ K v U, decode (summary K) v U = futureCost (Γ v) K U)
    {K L : Finset E} (h : summary K = summary L) :
    ∀ v, inventoryFrontier (Γ v) K = inventoryFrontier (Γ v) L := by
  apply (per_verdict_canonical Γ K L).mpr
  intro v U
  rw [← correct K v U, h, correct L v U]

#print axioms cost_frontier
#print axioms frontier_inverse
#print axioms frontier_eq_iff_cost
#print axioms cost_residual
#print axioms frontier_residual_normalize
#print axioms residual_congruence
#print axioms summary_necessity
#print axioms inventory_cost_recovery
#print axioms inventory_canonical
#print axioms inventory_update
#print axioms inventory_congruence
#print axioms per_verdict_canonical
#print axioms inventory_summary_necessity

end CertificateFrontier
