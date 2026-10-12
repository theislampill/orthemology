import Attainment
import CertificateFrontier

/-! Bridge to the inherited terminal support/cost frontier. All support-sensitive
guards have already been discharged in the represented valid trees. -/
namespace GuardedTree
variable {J E R : Type*} [DecidableEq E] [Fintype J] [Fintype R]
    (G : Grammar J E R)
open Tree

/-- Each terminal pair is backed by an actual valid bounded tree, separately
for its scoped judgement. It is not supplied as an admitted catalogue. -/
noncomputable def terminalCatalogue (q : J) : Finset (CertificateFrontier.Pair E ℚ) := by
  classical
  exact ((validCatalogue G).filter (fun t => judgement G t = q)).image
    (fun t => (support G t, cost G t))

theorem mem_terminalCatalogue_iff (q : J) (p : CertificateFrontier.Pair E ℚ) :
    p ∈ terminalCatalogue G q ↔
      ∃ t ∈ validCatalogue G, judgement G t = q ∧
        support G t = p.1 ∧ cost G t = p.2 := by
  classical
  constructor
  · intro hp
    obtain ⟨t, ht, heq⟩ := Finset.mem_image.mp hp
    obtain ⟨hm, hq⟩ := Finset.mem_filter.mp ht
    exact ⟨t, hm, hq, congrArg Prod.fst heq, congrArg Prod.snd heq⟩
  · rintro ⟨t, ht, hq, hs, hc⟩
    exact Finset.mem_image.mpr ⟨t, Finset.mem_filter.mpr ⟨ht, hq⟩,
      Prod.ext hs hc⟩

/-- Exact agreement between the finite terminal cost observation and existence
of an unrestricted finite valid proof under a finite price threshold. -/
theorem terminal_cost_le_iff (hw : ∀ r, 0 ≤ G.price r)
    (q : J) (U : Finset E) (c : ℚ) :
    CertificateFrontier.cost (terminalCatalogue G q) U ≤ (c : WithTop ℚ) ↔
      ∃ t : Tree G, Valid G t ∧ judgement G t = q ∧
        support G t ⊆ U ∧ cost G t ≤ c := by
  rw [CertificateFrontier.cost_le_iff]
  constructor
  · rintro ⟨p, hp, hsub, hc⟩
    obtain ⟨t, ht, hq, hs, hcost⟩ := (mem_terminalCatalogue_iff G q p).mp hp
    exact ⟨t, ((mem_validCatalogue_iff G t).mp ht).2, hq,
      hs ▸ hsub, hcost ▸ hc⟩
  · rintro ⟨t, ht, hq, hsub, hc⟩
    obtain ⟨u, hu, hqu, hsu, hcu⟩ := validCatalogue_cover G hw t ht
    refine ⟨(support G u, cost G u), ?_, ?_, hcu.trans hc⟩
    · exact (mem_terminalCatalogue_iff G q _).mpr ⟨u, hu, hqu.trans hq, rfl, rfl⟩
    · exact hsu ▸ hsub

/-- Every retained Pareto pair still has an actual original tree witness.
This is an existence theorem, not an extracted reconstruction algorithm. -/
theorem terminal_frontier_witness (q : J) (p : CertificateFrontier.Pair E ℚ)
    (hp : p ∈ CertificateFrontier.frontier (terminalCatalogue G q)) :
    ∃ t ∈ validCatalogue G, Valid G t ∧ judgement G t = q ∧
      support G t = p.1 ∧ cost G t = p.2 := by
  obtain ⟨t, ht, hq, hs, hc⟩ := (mem_terminalCatalogue_iff G q p).mp
    (CertificateFrontier.frontier_subset _ hp)
  exact ⟨t, ht, ((mem_validCatalogue_iff G t).mp ht).2, hq, hs, hc⟩

/-- An available terminal proof has an attained least price across all its
eligible exact supports, not just among trees of one chosen support. -/
theorem terminal_minimum_when_reachable (hw : ∀ r, 0 ≤ G.price r)
    (q : J) (U : Finset E)
    (hex : ∃ t : Tree G, Valid G t ∧ judgement G t = q ∧ support G t ⊆ U) :
    ∃ u ∈ validCatalogue G, Valid G u ∧ judgement G u = q ∧ support G u ⊆ U ∧
      CertificateFrontier.cost (terminalCatalogue G q) U = (cost G u : WithTop ℚ) ∧
      ∀ t : Tree G, Valid G t → judgement G t = q → support G t ⊆ U →
        cost G u ≤ cost G t := by
  classical
  let A := (validCatalogue G).filter (fun t => judgement G t = q ∧ support G t ⊆ U)
  have hA : A.Nonempty := by
    obtain ⟨t, ht, hq, hs⟩ := hex
    obtain ⟨u, hu, hqu, hsu, _⟩ := validCatalogue_cover G hw t ht
    exact ⟨u, Finset.mem_filter.mpr ⟨hu, hqu.trans hq, hsu ▸ hs⟩⟩
  obtain ⟨u, hu, hmin⟩ := Finset.exists_min_image A (cost G) hA
  obtain ⟨hum, huq, hus⟩ := Finset.mem_filter.mp hu
  have huv := ((mem_validCatalogue_iff G u).mp hum).2
  have hglobal : ∀ t : Tree G, Valid G t → judgement G t = q → support G t ⊆ U →
      cost G u ≤ cost G t := by
    intro t ht hq hs
    obtain ⟨v, hv, hvq, hvs, hvc⟩ := validCatalogue_cover G hw t ht
    exact (hmin v (Finset.mem_filter.mpr ⟨hv, hvq.trans hq, hvs ▸ hs⟩)).trans hvc
  refine ⟨u, hum, huv, huq, hus, ?_, hglobal⟩
  apply le_antisymm
  · exact (terminal_cost_le_iff G hw q U _).mpr ⟨u, huv, huq, hus, le_rfl⟩
  · apply Finset.le_inf
    intro p hp
    by_cases hsub : p.1 ⊆ U
    · simp only [if_pos hsub, WithTop.coe_le_coe]
      obtain ⟨t, ht, hq, hs, hc⟩ := (mem_terminalCatalogue_iff G q p).mp hp
      rw [← hc]
      exact hglobal t ((mem_validCatalogue_iff G t).mp ht).2 hq (hs ▸ hsub)
    · simp only [if_neg hsub]
      exact le_top

/-- Future terminal feasibility/price is exactly recovered by the old checked
inventory frontier, now fed by a derived guarded-tree catalogue. -/
theorem inventory_frontier_cost_le_iff (hw : ∀ r, 0 ≤ G.price r)
    (q : J) (K U : Finset E) (c : ℚ) :
    CertificateFrontier.cost
      (CertificateFrontier.inventoryFrontier (terminalCatalogue G q) K) U ≤
        (c : WithTop ℚ) ↔
      ∃ t : Tree G, Valid G t ∧ judgement G t = q ∧
        support G t ⊆ K ∪ U ∧ cost G t ≤ c := by
  rw [CertificateFrontier.inventory_cost_recovery, CertificateFrontier.futureCost]
  exact terminal_cost_le_iff G hw q (K ∪ U) c

/-- A residual frontier pair retains an original tree witness; only its missing
support, not its original proof support, equals the residual pair support. -/
theorem inventory_frontier_witness (q : J) (K : Finset E)
    (p : CertificateFrontier.Pair E ℚ)
    (hp : p ∈ CertificateFrontier.inventoryFrontier (terminalCatalogue G q) K) :
    ∃ t ∈ validCatalogue G, Valid G t ∧ judgement G t = q ∧
      support G t \ K = p.1 ∧ cost G t = p.2 := by
  have hm := CertificateFrontier.frontier_subset
    (CertificateFrontier.residual (terminalCatalogue G q) K) hp
  obtain ⟨s, hs, heq⟩ := Finset.mem_image.mp hm
  obtain ⟨t, ht, hq, hsupport, hcost⟩ := (mem_terminalCatalogue_iff G q s).mp hs
  refine ⟨t, ht, ((mem_validCatalogue_iff G t).mp ht).2, hq, ?_, ?_⟩
  · exact (congrArg (fun x => x \ K) hsupport).trans (congrArg Prod.fst heq)
  · have hprice := congrArg (fun x : CertificateFrontier.Pair E ℚ => x.2) heq
    exact hcost.trans hprice

#print axioms terminal_cost_le_iff
#print axioms terminal_minimum_when_reachable
#print axioms terminal_frontier_witness
#print axioms inventory_frontier_cost_le_iff
#print axioms inventory_frontier_witness
end GuardedTree
