import RoundRobinSchedule

noncomputable section
open Filter
open HiddenParity.Sufficiency

namespace HiddenParity.PhaseArithmetic

/-- A bounded nondecreasing natural-valued tail attains a greatest value and
then remains there. This is a pathwise arithmetic statement. -/
theorem bounded_tail_eventually_constant (p : ℕ → ℕ) (N b : ℕ)
    (hBound : ∀ n, N ≤ n → p n ≤ b)
    (hStep : ∀ n, N ≤ n → p n ≤ p (n+1)) :
    ∃ j, ∀ᶠ n in atTop, p n = j := by
  classical
  let P : ℕ → Prop := fun j => ∃ n, N ≤ n ∧ p n = j
  let j := Nat.findGreatest P b
  have hj : P j := Nat.findGreatest_spec (hBound N le_rfl) ⟨N,le_rfl,rfl⟩
  obtain ⟨n,hn,hpn⟩ := hj
  refine ⟨j,eventually_atTop.mpr ⟨n,?_⟩⟩
  intro m hnm
  have hl : p n ≤ p m := by
    induction m, hnm using Nat.le_induction with
    | base => exact le_rfl
    | succ m hnm ih => exact ih.trans (hStep m (hn.trans hnm))
  have hNm : N ≤ m := hn.trans hnm
  have hu : p m ≤ j := Nat.le_findGreatest (hBound m hNm) ⟨m,hNm,rfl⟩
  omega

/-- A cyclic enumeration supplies a true-model barrier above every requested
phase bound. This imports the exact frozen cycleAction definition and theorem. -/
theorem exists_cycle_barrier {Model : Type*} [DecidableEq Model]
    (B : Finset Model) (fallback σ : Model) (hσ : σ ∈ B) (M : ℕ) :
    ∃ j, M ≤ j ∧ cycleAction B fallback j = σ := by
  let i : B := ⟨σ,hσ⟩
  let j := (M+1) * Fintype.card B + (Fintype.equivFin B i).val
  have hcard : 0 < Fintype.card B := by
    simpa using Finset.card_pos.mpr (show B.Nonempty from ⟨σ,hσ⟩)
  refine ⟨j,?_,?_⟩
  · dsimp [j]
    nlinarith
  · exact cycleAction_at_index B fallback i (M+1)

/-- With only zero/one phase increments, a non-rejectable true-model phase
cannot be crossed. The stated transition premises must be supplied by the
actual controller; they are not a stochastic or global sufficiency assumption. -/
theorem cycling_phase_eventually_constant {Model : Type*} [DecidableEq Model]
    (p : ℕ → ℕ) (N K : ℕ) (B : Finset Model) (fallback σ : Model) (hσ : σ ∈ B)
    (hStep : ∀ n, N ≤ n → p (n+1) = p n ∨ p (n+1) = p n+1)
    (hStop : ∀ n, N ≤ n → K ≤ p n → cycleAction B fallback (p n) = σ →
      p (n+1) = p n) :
    ∃ j, ∀ᶠ n in atTop, p n = j := by
  obtain ⟨b,hb,hcycle⟩ := exists_cycle_barrier B fallback σ hσ (max K (p N))
  have hB : ∀ n, N ≤ n → p n ≤ b := by
    intro n hn
    induction n, hn using Nat.le_induction with
    | base => exact (le_max_right _ _).trans hb
    | succ n hn ih =>
        by_cases he : p n = b
        · have hK : K ≤ p n := by omega
          have hC : cycleAction B fallback (p n) = σ := by simpa [he] using hcycle
          have hs := hStop n hn hK hC
          omega
        · have hs := hStep n hn
          omega
  apply bounded_tail_eventually_constant p N b hB
  intro n hn
  have hs := hStep n hn
  omega

/-- An option-valued tail that never loses a present value either remains empty
forever or eventually keeps the first present value. No finite E assumption is
needed, and the result does not rely on a probabilistic fairness premise. -/
theorem persistent_option_eventually_stable {E : Type*} (q : ℕ → Option E) (N : ℕ)
    (hKeep : ∀ n, N ≤ n → ∀ e, q n = some e → q (n+1) = some e) :
    (∀ᶠ n in atTop, q n = none) ∨ ∃ e, ∀ᶠ n in atTop, q n = some e := by
  classical
  by_cases hex : ∃ n, N ≤ n ∧ ∃ e, q n = some e
  · obtain ⟨n,hn,e,he⟩ := hex
    right
    refine ⟨e,eventually_atTop.mpr ⟨n,?_⟩⟩
    intro m hnm
    induction m, hnm using Nat.le_induction with
    | base => exact he
    | succ m hnm ih => exact hKeep m (hn.trans hnm) e ih
  · left
    refine eventually_atTop.mpr ⟨N,?_⟩
    intro n hn
    cases hq : q n with
    | none => rfl
    | some e => exact (hex ⟨n,hn,e,hq⟩).elim

/-- Combined interface when retention is only known to persist across
unchanged phase indices. Eventual phase constancy discharges that guard. -/
theorem eventual_phase_and_mode_stable {E : Type*}
    (p : ℕ → ℕ) (q : ℕ → Option E) (N : ℕ)
    (hp : ∃ j, ∀ᶠ n in atTop, p n = j)
    (hKeep : ∀ n, N ≤ n → p (n+1) = p n →
      ∀ e, q n = some e → q (n+1) = some e) :
    ∃ j, (∀ᶠ n in atTop, p n = j) ∧
      ((∀ᶠ n in atTop, q n = none) ∨ ∃ e, ∀ᶠ n in atTop, q n = some e) := by
  obtain ⟨j,hj⟩ := hp
  obtain ⟨M,hM⟩ := eventually_atTop.mp hj
  refine ⟨j,hj,persistent_option_eventually_stable q (max N M) ?_⟩
  intro n hn e he
  have hpn := hM n (by omega)
  have hpn' := hM (n+1) (by omega)
  exact hKeep n (by omega) (by omega) e he

end HiddenParity.PhaseArithmetic
