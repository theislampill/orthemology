import Saturation

namespace GuardedTree.Saturation
open Tree
variable {J E R : Type*} [DecidableEq E] (G : Grammar J E R) [Fintype R]

/-- Unrestricted finite-proof minimum correctness. -/
def GlobalCorrect (D : Table (J := J) (E := E)) : Prop :=
  (∀ q S c, D q S = some c →
    ∃ t : Tree G, Valid G t ∧ judgement G t = q ∧
      support G t = S ∧ cost G t = c) ∧
  (∀ t : Tree G, Valid G t →
    ∃ c, D (judgement G t) (support G t) = some c ∧ c ≤ cost G t)

/-- Nonnegative prices are needed here, when the frozen pruning theorem
transfers height-bounded correctness to all finite proofs. -/
theorem round_global [Fintype J] (hw : ∀ r, 0 ≤ G.price r)
    (h : ℕ) (hH : grammarBound G ≤ h) : GlobalCorrect G (round G h) := by
  constructor
  · intro q S c hc
    obtain ⟨t, _, hv, hq, hs, hp⟩ := (round_correct G h).1 q S c hc
    exact ⟨t, hv, hq, hs, hp⟩
  · intro t hv
    obtain ⟨u, hu, hq, hs, hp, hb⟩ := exists_bounded_representative_grammar G hw t hv
    obtain ⟨c, hc, hle⟩ := (round_correct G h).2 u (bounded_mono G hH hb) hu
    exact ⟨c, by simpa only [hq, hs] using hc, hle.trans hp⟩

omit [Fintype R] in
theorem global_unique (D D' : Table (J := J) (E := E))
    (hD : GlobalCorrect G D) (hD' : GlobalCorrect G D') : D = D' := by
  funext q S
  cases hd : D q S with
  | none =>
    cases hd' : D' q S with
    | none => rfl
    | some c =>
      obtain ⟨t, hv, hq, hs, _⟩ := hD'.1 q S c hd'
      obtain ⟨d, hdd, _⟩ := hD.2 t hv
      rw [hq, hs, hd] at hdd
      contradiction
  | some c =>
    obtain ⟨t, hv, hq, hs, hp⟩ := hD.1 q S c hd
    obtain ⟨d, hd', hdc⟩ := hD'.2 t hv
    rw [hq, hs] at hd'
    obtain ⟨u, huv, huq, hus, hup⟩ := hD'.1 q S d hd'
    obtain ⟨e, he, hed⟩ := hD.2 u huv
    rw [huq, hus, hd] at he
    have hec : c = e := Option.some.inj he
    have hcd : c ≤ d := by simpa only [← hec, hup] using hed
    have hdc' : d ≤ c := by simpa only [hp] using hdc
    have hcd' := le_antisymm hcd hdc'
    rw [hd', hcd']

/-- Every later round has exactly the same reachable keys and numeric prices. -/
theorem round_stable [Fintype J] (hw : ∀ r, 0 ≤ G.price r) (k : ℕ) :
    round G (grammarBound G + k) = round G (grammarBound G) :=
  global_unique G _ _ (round_global G hw _ (Nat.le_add_right _ _))
    (round_global G hw _ le_rfl)

theorem step_fixed [Fintype J] (hw : ∀ r, 0 ≤ G.price r) :
    step G (round G (grammarBound G)) = round G (grammarBound G) :=
  round_stable G hw 1

/-- Full table equality at consecutive rounds is a valid permanent stopping
condition. Equality of key sets alone is deliberately not its hypothesis. -/
theorem early_stopping (h : ℕ) (heq : round G (h + 1) = round G h) (k : ℕ) :
    round G (h + k) = round G h := by
  induction k with
  | zero => simp
  | succ k ih =>
    change step G (round G (h + k)) = round G h
    rw [ih]
    exact heq

theorem early_stopping_global [Fintype J] (hw : ∀ r, 0 ≤ G.price r)
    (h : ℕ) (heq : round G (h + 1) = round G h) : GlobalCorrect G (round G h) := by
  have hg := round_global G hw (h + grammarBound G) (Nat.le_add_left _ _)
  rw [early_stopping G h heq (grammarBound G)] at hg
  exact hg

/-- Retention can lower an existing price, but never loses an old key. -/
theorem round_retains (h : ℕ) (q : J) (S : Finset E) (c : ℚ)
    (hc : round G h q S = some c) :
    ∃ d, round G (h + 1) q S = some d ∧ d ≤ c := by
  apply minimum_le
  exact (mem_candidates_iff G _ q S c).mpr (Or.inl hc)

/-- On generated tables, finite grammar-support enumeration drops no reachable
premise state. This is exactly the unrestricted ordered-support candidate rule. -/
theorem round_mem_candidates_iff (h : ℕ) (q : J) (S : Finset E) (c : ℚ) :
    c ∈ candidates G (round G h) q S ↔
      round G h q S = some c ∨
      ∃ (r : R) (s : Fin (G.arity r) → Finset E) (p : Fin (G.arity r) → ℚ),
        (∀ i, round G h (G.premise r i) (s i) = some (p i)) ∧
        G.guard r s ∧ G.head r = q ∧
        G.localSupport r ∪ Finset.univ.biUnion s = S ∧
        G.price r + ∑ i, p i = c := by
  rw [mem_candidates_iff]
  constructor
  · rintro (ho | ⟨r, s, p, _, hp, hg, hq, hs, hc⟩)
    · exact Or.inl ho
    · exact Or.inr ⟨r, s, p, hp, hg, hq, hs, hc⟩
  · rintro (ho | ⟨r, s, p, hp, hg, hq, hs, hc⟩)
    · exact Or.inl ho
    · refine Or.inr ⟨r, s, p, ?_, hp, hg, hq, hs, hc⟩
      intro i
      obtain ⟨t, _, _, _, ht, _⟩ := (round_correct G h).1 _ _ _ (hp i)
      rw [← ht]
      exact support_subset_grammarSupport G t

/-- The original ambient-universe bound is also sufficient when E is finite.
The grammar-local bound may be smaller and does not require finite E. -/
theorem round_global_uniform [Fintype J] [Fintype E] (hw : ∀ r, 0 ≤ G.price r) :
    GlobalCorrect G (round G (Fintype.card J * (Fintype.card E + 1))) := by
  apply round_global G hw
  exact Nat.mul_le_mul_left _ (Nat.add_le_add_right (Finset.card_le_univ _) 1)

theorem round_stable_uniform [Fintype J] [Fintype E]
    (hw : ∀ r, 0 ≤ G.price r) (k : ℕ) :
    round G (Fintype.card J * (Fintype.card E + 1) + k) =
      round G (Fintype.card J * (Fintype.card E + 1)) := by
  apply global_unique G _ _
  · apply round_global G hw
    exact (Nat.mul_le_mul_left _
      (Nat.add_le_add_right (Finset.card_le_univ _) 1)).trans (Nat.le_add_right _ _)
  · exact round_global_uniform G hw

#print axioms round_global
#print axioms round_stable
#print axioms early_stopping_global
#print axioms round_mem_candidates_iff
end GuardedTree.Saturation
