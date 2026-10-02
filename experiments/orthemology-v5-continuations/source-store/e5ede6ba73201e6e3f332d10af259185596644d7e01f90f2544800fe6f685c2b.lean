import RankTransport

/-!
# Concrete-simulation bad-visit budgets use the lower envelope

Companion to the conservative upper-envelope theorem. Here bad labels reflect
pairwise along the relation. Every source alternative has a matching continuation
for every destination step. One minimum witness therefore suffices, without C4
successor-fibre coverage. This does NOT validate minimum rank under the weaker
universal-information target-transfer condition used by RankTransport.
-/

namespace Orthemology.Frontier
variable {P Q : Type*}

noncomputable def badIndicator {S : Type*} (bad : S → Prop) (s : S) : ℕ := by
  classical
  exact if bad s then 1 else 0

noncomputable def lowerRank (fibre : Q → Finset P) (nonempty : ∀ q, (fibre q).Nonempty)
    (rank : P → ℕ) (q : Q) : ℕ := (fibre q).inf' (nonempty q) rank

/-- The minimum source witness transfers a concrete bad-visit budget without fibre coverage. -/
theorem lowerRank_step
    (fibre : Q → Finset P) (nonempty : ∀ q, (fibre q).Nonempty) (rank : P → ℕ)
    (src : P → P → Prop) (dst : Q → Q → Prop) (badA : P → Prop) (badB : Q → Prop)
    (source_budget : ∀ p p', src p p' → badIndicator badA p + rank p' ≤ rank p)
    (matching : ∀ q q', dst q q' → ∀ p ∈ fibre q, ∃ p' ∈ fibre q', src p p')
    (reflection : ∀ q p, p ∈ fibre q → badB q → badA p)
    {q q' : Q} (step : dst q q') :
    badIndicator badB q + lowerRank fibre nonempty rank q' ≤ lowerRank fibre nonempty rank q := by
  classical
  obtain ⟨p, hp, hmin⟩ := (fibre q).exists_mem_eq_inf' (nonempty q) rank
  obtain ⟨p', hp', hsrc⟩ := matching q q' step p hp
  have hsource := source_budget p p' hsrc
  have hnext : lowerRank fibre nonempty rank q' ≤ rank p' := Finset.inf'_le rank hp'
  have hbad : badIndicator badB q ≤ badIndicator badA p := by
    by_cases hb : badB q
    · simp [badIndicator, hb, reflection q p hp hb]
    · simp [badIndicator, hb]
  change lowerRank fibre nonempty rank q = rank p at hmin
  omega

noncomputable def badVisits (bad : Q → Prop) (run : ℕ → Q) (n : ℕ) : ℕ :=
  ∑ i ∈ Finset.range n, badIndicator bad (run i)

/-- The rank bounds the total number of bad visits, not the time of the last visit. -/
theorem badVisits_add_rank_le (bad : Q → Prop) (rank : Q → ℕ) (run : ℕ → Q)
    (budget : ∀ n, badIndicator bad (run n) + rank (run (n+1)) ≤ rank (run n))
    (n : ℕ) : badVisits bad run n + rank (run n) ≤ rank (run 0) := by
  induction n with
  | zero => simp [badVisits]
  | succ n ih =>
    have hstep := budget n
    unfold badVisits at *
    rw [Finset.sum_range_succ]
    omega

/-- A natural-valued bad-visit budget implies eventual absence of bad states.
The cutoff may be arbitrarily later than the initial rank. -/
theorem eventually_no_bad_of_budget (bad : Q → Prop) (rank : Q → ℕ) (run : ℕ → Q)
    (budget : ∀ n, badIndicator bad (run n) + rank (run (n+1)) ≤ rank (run n)) :
    ∃ N, ∀ n, N ≤ n → ¬ bad (run n) := by
  classical
  have hex : ∃ k, ∃ n, rank (run n) = k := ⟨rank (run 0), 0, rfl⟩
  obtain ⟨N, hN⟩ := Nat.find_spec hex
  have hmin : ∀ n, Nat.find hex ≤ rank (run n) := fun n => Nat.find_min' hex ⟨n, rfl⟩
  have hmono : ∀ a k, rank (run (a+k)) ≤ rank (run a) := by
    intro a k
    induction k with
    | zero => simp
    | succ k ih =>
      have hstep := budget (a+k)
      rw [show a + (k+1) = (a+k)+1 by omega]
      omega
  refine ⟨N, ?_⟩
  intro n hn hb
  have hle := hmono N (n-N)
  rw [Nat.add_sub_of_le hn, hN] at hle
  have hstep := budget n
  have hlow := hmin (n+1)
  simp only [badIndicator, if_pos hb] at hstep
  omega

/-- Concrete relational simulation preserves co-Büchi success under pairwise bad reflection. -/
theorem lowerRank_preserves_eventual_good
    (fibre : Q → Finset P) (nonempty : ∀ q, (fibre q).Nonempty) (rank : P → ℕ)
    (src : P → P → Prop) (dst : Q → Q → Prop) (badA : P → Prop) (badB : Q → Prop)
    (source_budget : ∀ p p', src p p' → badIndicator badA p + rank p' ≤ rank p)
    (matching : ∀ q q', dst q q' → ∀ p ∈ fibre q, ∃ p' ∈ fibre q', src p p')
    (reflection : ∀ q p, p ∈ fibre q → badB q → badA p)
    (run : ℕ → Q) (run_step : ∀ n, dst (run n) (run (n+1))) :
    (∀ n, badVisits badB run n ≤ lowerRank fibre nonempty rank (run 0)) ∧
      ∃ N, ∀ n, N ≤ n → ¬ badB (run n) := by
  have hbudget := fun n => lowerRank_step fibre nonempty rank src dst badA badB
    source_budget matching reflection (run_step n)
  constructor
  · intro n
    have h := badVisits_add_rank_le badB (lowerRank fibre nonempty rank) run hbudget n
    omega
  · exact eventually_no_bad_of_budget badB (lowerRank fibre nonempty rank) run hbudget

namespace LowerBudgetFixtures

/-- One budgeted bad visit can occur at any chosen time, despite initial rank one. -/
def delayedRank (delay n : ℕ) : ℕ := if n ≤ delay then 1 else 0
def delayedBad (delay n : ℕ) : Prop := n = delay

theorem delayed_budget (delay n : ℕ) :
    badIndicator (delayedBad delay) n + delayedRank delay (n+1) ≤ delayedRank delay n := by
  classical
  unfold badIndicator delayedBad delayedRank
  split_ifs <;> omega

theorem arbitrarily_late_bad_visit (B : ℕ) :
    ∃ delay > B, delayedRank delay 0 = 1 ∧ delayedBad delay delay ∧
      (∀ n, badIndicator (delayedBad delay) n + delayedRank delay (n+1) ≤ delayedRank delay n) := by
  refine ⟨B+1, by omega, ?_, rfl, delayed_budget (B+1)⟩
  simp [delayedRank]

/-- The stale-fibre non-target example does not satisfy the stronger pairwise bad reflection.
Thus the new minimum theorem cannot be misapplied to rescue that failed contract. -/
theorem stale_bad_reflection_fails :
    ¬ (∀ q : Unit, ∀ p ∈ RankFixtures.staleFibre q, True → p = false) := by
  unfold RankFixtures.staleFibre
  decide

end LowerBudgetFixtures
end Orthemology.Frontier
