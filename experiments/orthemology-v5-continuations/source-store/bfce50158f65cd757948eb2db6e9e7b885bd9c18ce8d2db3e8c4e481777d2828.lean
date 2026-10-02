import Mathlib.Data.Finset.Lattice.Fold
import Mathlib.Tactic

/-!
# Conservative rank transport across relational continuation fibres

Source: `frontier-programme.md`, §11, derived in the 2026-09-30 research packet.
`src` and `dst` below are the selected-policy successor relations, not free choices.
Coverage quantifies over every alternative in the successor fibre; it is not an
existential simulation witness. All successor branches of the destination are covered.
-/

namespace Orthemology.Frontier

variable {P Q : Type*}

def liftedRank (fibre : Q → Finset P) (rank : P → ℕ) (q : Q) : ℕ :=
  (fibre q).sup rank

/-- Full successor-fibre coverage transports one-step rank contraction. -/
theorem liftedRank_step
    (fibre : Q → Finset P) (rank : P → ℕ)
    (src : P → P → Prop) (dst : Q → Q → Prop)
    (source_contract : ∀ p p', src p p' → rank p' ≤ rank p - 1)
    (coverage : ∀ q q', dst q q' → ∀ p' ∈ fibre q',
      ∃ p ∈ fibre q, src p p')
    {q q' : Q} (step : dst q q') :
    liftedRank fibre rank q' ≤ liftedRank fibre rank q - 1 := by
  unfold liftedRank
  apply Finset.sup_le
  intro p' hp'
  obtain ⟨p, hp, hstep⟩ := coverage q q' step p' hp'
  exact (source_contract p p' hstep).trans
    (Nat.sub_le_sub_right (Finset.le_sup hp) 1)

/-- Exact finite-horizon bound along any selected-policy run. -/
theorem liftedRank_run_bound
    (fibre : Q → Finset P) (rank : P → ℕ)
    (src : P → P → Prop) (dst : Q → Q → Prop)
    (source_contract : ∀ p p', src p p' → rank p' ≤ rank p - 1)
    (coverage : ∀ q q', dst q q' → ∀ p' ∈ fibre q',
      ∃ p ∈ fibre q, src p p')
    (run : ℕ → Q) (run_step : ∀ n, dst (run n) (run (n+1)))
    (n : ℕ) :
    liftedRank fibre rank (run n) ≤ liftedRank fibre rank (run 0) - n := by
  induction n with
  | zero => simp
  | succ n ih =>
    have h := liftedRank_step fibre rank src dst source_contract coverage (run_step n)
    have h' := Nat.sub_le_sub_right ih 1
    omega

/-- Conservative rank zero implies that every represented alternative has rank zero. -/
theorem liftedRank_zero_iff (fibre : Q → Finset P) (rank : P → ℕ) (q : Q) :
    liftedRank fibre rank q = 0 ↔ ∀ p ∈ fibre q, rank p = 0 := by
  constructor
  · intro h p hp
    have : rank p ≤ liftedRank fibre rank q := Finset.le_sup hp
    omega
  · intro h
    apply Nat.eq_zero_of_le_zero
    apply Finset.sup_le
    intro p hp
    exact Nat.le_of_eq (h p hp)

/-- Full target persistence by the initial maximum rank, without singleton fibres. -/
theorem target_after_liftedRank
    (fibre : Q → Finset P) (rank : P → ℕ)
    (src : P → P → Prop) (dst : Q → Q → Prop) (target : Q → Prop)
    (source_contract : ∀ p p', src p p' → rank p' ≤ rank p - 1)
    (coverage : ∀ q q', dst q q' → ∀ p' ∈ fibre q',
      ∃ p ∈ fibre q, src p p')
    (target_transfer : ∀ q, (∀ p ∈ fibre q, rank p = 0) → target q)
    (run : ℕ → Q) (run_step : ∀ n, dst (run n) (run (n+1)))
    (n : ℕ) (hn : liftedRank fibre rank (run 0) ≤ n) : target (run n) := by
  apply target_transfer
  apply (liftedRank_zero_iff fibre rank (run n)).mp
  have h := liftedRank_run_bound fibre rank src dst source_contract coverage run run_step n
  omega

/-- Alternating matching constructs a related source run for every destination run.
The destination action is already selected in `dst`; witnesses do not choose another action. -/
theorem matched_run
    (fibre : Q → Finset P) (src : P → P → Prop) (dst : Q → Q → Prop)
    (matching : ∀ q q', dst q q' → ∀ p ∈ fibre q,
      ∃ p' ∈ fibre q', src p p')
    (run : ℕ → Q) (run_step : ∀ n, dst (run n) (run (n+1)))
    (p₀ : P) (hp₀ : p₀ ∈ fibre (run 0)) :
    ∃ path : ℕ → P, path 0 = p₀ ∧
      (∀ n, path n ∈ fibre (run n)) ∧
      ∀ n, src (path n) (path (n+1)) := by
  classical
  let advance (n : ℕ) (p : {p : P // p ∈ fibre (run n)}) :
      {p : P // p ∈ fibre (run (n+1))} :=
    ⟨Classical.choose (matching _ _ (run_step n) p.val p.property),
      (Classical.choose_spec (matching _ _ (run_step n) p.val p.property)).1⟩
  let path : (n : ℕ) → {p : P // p ∈ fibre (run n)} :=
    Nat.rec ⟨p₀, hp₀⟩ advance
  refine ⟨fun n => (path n).val, rfl, fun n => (path n).property, ?_⟩
  intro n
  exact (Classical.choose_spec
    (matching _ _ (run_step n) (path n).val (path n).property)).2

/-- An explicit relational migration contract for one selected destination policy.
`Q` is the admitted closed destination domain, so every `next` successor here is
already in that domain. Applications must check that no physical branch was omitted. -/
structure ContinuationContract (P Q A : Type*) where
  fibre : Q → Finset P
  fibre_nonempty : ∀ q, (fibre q).Nonempty
  rank : P → ℕ
  src : P → P → Prop
  next : Q → A → Q → Prop
  policy : Q → A
  licensed : Q → A → Prop
  safe : Q → Prop
  target : Q → Prop
  readout : P → Q → Prop
  source_contract : ∀ p p', src p p' → rank p' ≤ rank p - 1
  safe_all : ∀ q, safe q
  policy_licensed : ∀ q, licensed q (policy q)
  nonblocking : ∀ q, ∃ q', next q (policy q) q'
  target_transfer : ∀ q, (∀ p ∈ fibre q, rank p = 0) → target q
  matching : ∀ q q', next q (policy q) q' → ∀ p ∈ fibre q,
    ∃ p' ∈ fibre q', src p p'
  coverage : ∀ q q', next q (policy q) q' → ∀ p' ∈ fibre q',
    ∃ p ∈ fibre q, src p p'
  readout_agreement : ∀ q p, p ∈ fibre q → readout p q

/-- C0-C4 jointly transfer licensed safe eventual target persistence and a matching source run.
The convergence horizon is computed from the actual entire initial fibre. -/
theorem restoration_transport {A : Type*} (C : ContinuationContract P Q A)
    (run : ℕ → Q) (run_step : ∀ n, C.next (run n) (C.policy (run n)) (run (n+1))) :
    (∀ n, C.safe (run n) ∧ C.licensed (run n) (C.policy (run n))) ∧
    (∀ n, liftedRank C.fibre C.rank (run 0) ≤ n → C.target (run n)) ∧
    (∀ p₀ ∈ C.fibre (run 0), ∃ path : ℕ → P,
      path 0 = p₀ ∧ (∀ n, C.readout (path n) (run n)) ∧
      ∀ n, C.src (path n) (path (n+1))) := by
  refine ⟨fun n => ⟨C.safe_all _, C.policy_licensed _⟩, ?_, ?_⟩
  · intro n hn
    exact target_after_liftedRank C.fibre C.rank C.src
      (fun q q' => C.next q (C.policy q) q') C.target
      C.source_contract C.coverage C.target_transfer run run_step n hn
  · intro p₀ hp₀
    obtain ⟨path, hzero, hmem, hstep⟩ := matched_run C.fibre C.src
      (fun q q' => C.next q (C.policy q) q') C.matching run run_step p₀ hp₀
    exact ⟨path, hzero, fun n => C.readout_agreement _ _ (hmem n), hstep⟩

/-- Every admitted initial state has an infinite selected-policy run, excluding dead-end vacuity. -/
theorem exists_policy_run {A : Type*} (C : ContinuationContract P Q A) (q₀ : Q) :
    ∃ run : ℕ → Q, run 0 = q₀ ∧
      ∀ n, C.next (run n) (C.policy (run n)) (run (n+1)) := by
  classical
  let advance : Q → Q := fun q => Classical.choose (C.nonblocking q)
  let run : ℕ → Q := fun n => advance^[n] q₀
  refine ⟨run, rfl, ?_⟩
  intro n
  have h := Classical.choose_spec (C.nonblocking (run n))
  simpa [run, advance, Function.iterate_succ_apply'] using h

namespace RankFixtures

/-- Stale alternatives defeat convergence despite an alternating source match. -/
def staleFibre (_ : Unit) : Finset Bool := {false, true}
def staleRank (p : Bool) : ℕ := if p then 0 else 1
def staleSource (_ p' : Bool) : Prop := p' = true
def staleDestination (_ _ : Unit) : Prop := True

theorem stale_source_contract : ∀ p p', staleSource p p' → staleRank p' ≤ staleRank p - 1 := by
  unfold staleSource staleRank
  decide

theorem stale_matching : ∀ q q', staleDestination q q' → ∀ p ∈ staleFibre q,
    ∃ p' ∈ staleFibre q', staleSource p p' := by
  unfold staleDestination staleFibre staleSource
  decide

theorem stale_coverage_fails : ¬ (∀ q q', staleDestination q q' → ∀ p' ∈ staleFibre q',
    ∃ p ∈ staleFibre q, staleSource p p') := by
  unfold staleDestination staleFibre staleSource
  decide

theorem stale_rank_stays_one : liftedRank staleFibre staleRank () = 1 := by
  decide

/-- A five-state source and three-state destination with overlapping non-singleton fibres. -/
def overlapRank (p : Fin 5) : ℕ := ![2, 1, 0, 2, 1] p
def overlapNext (p : Fin 5) : Fin 5 := ![1, 2, 2, 4, 2] p
def overlapFibre (q : Fin 3) : Finset (Fin 5) := ![{2}, {1, 4, 2}, {0, 3, 1}] q
def overlapDestination (q : Fin 3) : Fin 3 := ![0, 0, 1] q

theorem overlap_source_contract : ∀ p, overlapRank (overlapNext p) ≤ overlapRank p - 1 := by
  decide

theorem overlap_matching : ∀ q p, p ∈ overlapFibre q →
    overlapNext p ∈ overlapFibre (overlapDestination q) := by
  decide

theorem overlap_coverage : ∀ q p', p' ∈ overlapFibre (overlapDestination q) →
    ∃ p ∈ overlapFibre q, overlapNext p = p' := by
  decide

theorem overlap_lifted_ranks : ∀ q, liftedRank overlapFibre overlapRank q = q.val := by
  decide

end RankFixtures
end Orthemology.Frontier
