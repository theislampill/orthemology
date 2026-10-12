import Candidates

/-! Height induction for the actual synchronous numeric recurrence. -/
namespace GuardedTree.Saturation
open Tree
variable {J E R : Type*} [DecidableEq E] (G : Grammar J E R) [Fintype R]

noncomputable def round : ℕ → Table (J := J) (E := E)
  | 0 => fun _ _ => none
  | h + 1 => step G (round h)

/-- Sound entries have actual bounded witnesses. Every bounded proof has a
reachable entry no dearer than that proof. Together these are exact minima. -/
def Correct (D : Table (J := J) (E := E)) (h : ℕ) : Prop :=
  (∀ q S c, D q S = some c →
    ∃ t : Tree G, Bounded G h t ∧ Valid G t ∧
      judgement G t = q ∧ support G t = S ∧ cost G t = c) ∧
  (∀ t : Tree G, Bounded G h t → Valid G t →
    ∃ c, D (judgement G t) (support G t) = some c ∧ c ≤ cost G t)

omit [DecidableEq E] [Fintype R] in
theorem bounded_mono {h k : ℕ} (hk : h ≤ k) {t : Tree G}
    (ht : Bounded G h t) : Bounded G k t :=
  fun p hp => (ht p hp).trans hk

omit [DecidableEq E] [Fintype R] in
theorem bounded_node (h : ℕ) (r : R) (child : Fin (G.arity r) → Tree G)
    (hc : ∀ i, Bounded G h (child i)) : Bounded G (h + 1) (.node r child) := by
  intro p hp
  cases hp with
  | root => simp
  | down _ _ i p hp => exact Nat.succ_le_succ (hc i p hp)

omit [DecidableEq E] [Fintype R] in
theorem bounded_child (h : ℕ) (r : R) (child : Fin (G.arity r) → Tree G)
    (hb : Bounded G (h + 1) (.node r child)) (i : Fin (G.arity r)) :
    Bounded G h (child i) := by
  intro p hp
  exact Nat.le_of_succ_le_succ (hb (.node r child :: p) (.down r child i p hp))

/-- Each price candidate, including a retained old price, has a real bounded
witness. Rule candidates assemble witnesses with equal ordered supports. -/
theorem candidate_sound (h : ℕ) (D : Table (J := J) (E := E))
    (hD : Correct G D h) (q : J) (S : Finset E) (c : ℚ)
    (hc : c ∈ candidates G D q S) :
    ∃ t : Tree G, Bounded G (h + 1) t ∧ Valid G t ∧
      judgement G t = q ∧ support G t = S ∧ cost G t = c := by
  classical
  rcases (mem_candidates_iff G D q S c).mp hc with hold | hnew
  · obtain ⟨t, hb, hv, hq, hs, hp⟩ := hD.1 q S c hold
    exact ⟨t, bounded_mono G (Nat.le_succ h) hb, hv, hq, hs, hp⟩
  · obtain ⟨r, s, p, _, hp, hg, hq, hs, hc⟩ := hnew
    choose child hb hv hj hsup hcost using
      (fun i => hD.1 (G.premise r i) (s i) (p i) (hp i))
    have heq : (fun i => support G (child i)) = s := funext hsup
    refine ⟨.node r child, bounded_node G h r child hb,
      ⟨fun i => ⟨hv i, hj i⟩, ?_⟩, hq, ?_, ?_⟩
    · simpa only [heq] using hg
    · simpa only [support, heq] using hs
    · simpa only [cost, hcost] using hc

/-- For every height-(h+1) tree, the actual generator has a no-dearer candidate.
This substitutes least-price children at exactly their old supports. -/
theorem candidate_complete (h : ℕ) (D : Table (J := J) (E := E))
    (hD : Correct G D h) (t : Tree G) (hb : Bounded G (h + 1) t)
    (hv : Valid G t) :
    ∃ c ∈ candidates G D (judgement G t) (support G t), c ≤ cost G t := by
  classical
  cases t with
  | node r child =>
    choose p hp hle using (fun i => hD.2 (child i)
      (bounded_child G h r child hb i) (hv.1 i).1)
    refine ⟨G.price r + ∑ i, p i, ?_, ?_⟩
    · apply (mem_candidates_iff G D _ _ _).mpr
      refine Or.inr ⟨r, fun i => support G (child i), p,
        fun i => support_subset_grammarSupport G (child i), ?_, hv.2, rfl, rfl, rfl⟩
      intro i
      simpa only [(hv.1 i).2] using hp i
    · exact add_le_add_left (Finset.sum_le_sum (fun i _ => hle i)) _

theorem step_correct (h : ℕ) (D : Table (J := J) (E := E))
    (hD : Correct G D h) : Correct G (step G D) (h + 1) := by
  constructor
  · intro q S c hc
    exact candidate_sound G h D hD q S c ((step_some_iff G D q S c).mp hc).1
  · intro t hb hv
    obtain ⟨c, hc, hle⟩ := candidate_complete G h D hD t hb hv
    obtain ⟨d, hd, hdc⟩ := minimum_le (candidates G D (judgement G t) (support G t)) c hc
    exact ⟨d, hd, hdc.trans hle⟩

/-- Proved by height induction from an all-unreachable numeric table. The
recurrence is not defined as a minimum over bounded trees. -/
theorem round_correct (h : ℕ) : Correct G (round G h) h := by
  induction h with
  | zero =>
    constructor
    · intro q S c hc
      simp [round] at hc
    · intro t hb _
      have hz := hb [t] (.root t)
      simp at hz
  | succ h ih => exact step_correct G h (round G h) ih

/-- Exact bounded-height minimum semantics, including a realizing witness. -/
theorem round_some_iff (h : ℕ) (q : J) (S : Finset E) (c : ℚ) :
    round G h q S = some c ↔
      (∃ t : Tree G, Bounded G h t ∧ Valid G t ∧
        judgement G t = q ∧ support G t = S ∧ cost G t = c) ∧
      (∀ t : Tree G, Bounded G h t → Valid G t →
        judgement G t = q → support G t = S → c ≤ cost G t) := by
  constructor
  · intro hc
    refine ⟨(round_correct G h).1 q S c hc, ?_⟩
    intro t hb hv hq hs
    obtain ⟨d, hd, hle⟩ := (round_correct G h).2 t hb hv
    rw [hq, hs, hc] at hd
    exact Option.some.inj hd ▸ hle
  · rintro ⟨⟨t, hb, hv, hq, hs, hp⟩, hmin⟩
    obtain ⟨d, hd, hle⟩ := (round_correct G h).2 t hb hv
    rw [hq, hs] at hd
    obtain ⟨u, hub, huv, huq, hus, hup⟩ := (round_correct G h).1 q S d hd
    have hcd : c ≤ d := by simpa only [hup] using hmin u hub huv huq hus
    have hdc : d ≤ c := by simpa only [hp] using hle
    exact (le_antisymm hdc hcd) ▸ hd

/-- No entry is equivalent to no valid tree below this round's height. -/
theorem round_none_iff (h : ℕ) (q : J) (S : Finset E) :
    round G h q S = none ↔
      ¬ ∃ t : Tree G, Bounded G h t ∧ Valid G t ∧
        judgement G t = q ∧ support G t = S := by
  constructor
  · intro hn ⟨t, hb, hv, hq, hs⟩
    obtain ⟨c, hc, _⟩ := (round_correct G h).2 t hb hv
    rw [hq, hs, hn] at hc
    contradiction
  · intro hnone
    cases hc : round G h q S with
    | none => rfl
    | some c =>
      obtain ⟨t, hb, hv, hq, hs, _⟩ := (round_correct G h).1 q S c hc
      exact False.elim (hnone ⟨t, hb, hv, hq, hs⟩)

#print axioms round_correct
#print axioms round_some_iff
#print axioms round_none_iff
end GuardedTree.Saturation
