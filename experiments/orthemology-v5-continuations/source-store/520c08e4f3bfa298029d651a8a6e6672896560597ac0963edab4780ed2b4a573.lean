import Mathlib

namespace Orthemology.Tranche2.FiniteAlphabetQuery
variable {Y : Type*} [Inhabited Y]

/-- A total causal evaluator. The state may contain an arbitrary
private random seed. Only an `ask = true` step consults the parameter oracle. -/
def advance {S : Type*} (ask : S → Bool) (next : S → Y → S)
    (oracle : ℕ → Y) (x : S × ℕ) : S × ℕ :=
  if ask x.1 then (next x.1 (oracle x.2), x.2+1)
  else (next x.1 default, x.2)

def run {S : Type*} (ask : S → Bool) (next : S → Y → S)
    (oracle : ℕ → Y) (initial : S) : ℕ → S × ℕ
  | 0 => (initial,0)
  | n+1 => advance ask next oracle (run ask next oracle initial n)

def Bounded {S : Type*} (ask : S → Bool) (next : S → Y → S)
    (oracle : ℕ → Y) (initial : S) (N : ℕ) : Prop :=
  ∀ n, (run ask next oracle initial n).2 ≤ N

/-- One bounded run suffices: neither boundedness of the second run nor a
stopping-time assumption is smuggled into prefix locality. -/
theorem bounded_prefix_locality {S : Type*}
    (ask : S → Bool) (next : S → Y → S)
    (oracle other : ℕ → Y) (initial : S) (N : ℕ)
    (hprefix : ∀ k < N, oracle k = other k)
    (hbound : Bounded ask next oracle initial N) :
    ∀ n, run ask next oracle initial n = run ask next other initial n := by
  intro n
  induction n with
  | zero => rfl
  | succ n ih =>
    rw [run,run,← ih]
    unfold advance
    split_ifs with h
    · have hk : (run ask next oracle initial n).2 < N := by
        have hn := hbound (n+1)
        simp only [run,advance,h,ite_true] at hn
        exact Nat.lt_of_succ_le hn
      rw [hprefix _ hk]
    · rfl

theorem bounded_prefix_equivalence {S : Type*}
    (ask : S → Bool) (next : S → Y → S)
    (oracle other : ℕ → Y) (initial : S) (N : ℕ)
    (hprefix : ∀ k < N, oracle k = other k) :
    Bounded ask next oracle initial N ↔ Bounded ask next other initial N := by
  constructor
  · intro hb n
    rw [← bounded_prefix_locality ask next oracle other initial N hprefix hb n]
    exact hb n
  · intro hb n
    rw [← bounded_prefix_locality ask next other oracle initial N
      (fun k hk => (hprefix k hk).symm) hb n]
    exact hb n

def prefixOracle (N : ℕ) (word : Fin N → Y) (k : ℕ) : Y :=
  if h : k < N then word ⟨k,h⟩ else default

lemma prefixOracle_agrees (oracle : ℕ → Y) (N : ℕ) :
    ∀ k < N, oracle k = prefixOracle N (fun i => oracle i) k := by
  intro k hk
  simp [prefixOracle,hk]

/-- Exact bounded-event and whole-run factorisation through the finite prefix.
The event that no query beyond N is ever requested is local to the prefix too. -/
theorem bounded_trace_factorisation {S : Type*}
    (ask : S → Bool) (next : S → Y → S)
    (oracle : ℕ → Y) (initial : S) (N : ℕ)
    (P : (ℕ → S × ℕ) → Prop) :
    (Bounded ask next oracle initial N ∧ P (run ask next oracle initial)) ↔
    (Bounded ask next (prefixOracle N (fun i => oracle i)) initial N ∧
      P (run ask next (prefixOracle N (fun i => oracle i)) initial)) := by
  have hp := prefixOracle_agrees oracle N
  constructor
  · rintro ⟨hb,hP⟩
    have heq := funext (bounded_prefix_locality ask next oracle _ initial N hp hb)
    exact ⟨(bounded_prefix_equivalence ask next oracle _ initial N hp).mp hb, heq ▸ hP⟩
  · rintro ⟨hb,hP⟩
    have hb' := (bounded_prefix_equivalence ask next oracle _ initial N hp).mpr hb
    have heq := funext (bounded_prefix_locality ask next oracle _ initial N hp hb')
    exact ⟨hb', heq.symm ▸ hP⟩

end Orthemology.Tranche2.FiniteAlphabetQuery

#print axioms Orthemology.Tranche2.FiniteAlphabetQuery.bounded_prefix_locality
#print axioms Orthemology.Tranche2.FiniteAlphabetQuery.bounded_prefix_equivalence
#print axioms Orthemology.Tranche2.FiniteAlphabetQuery.bounded_trace_factorisation
#check Orthemology.Tranche2.FiniteAlphabetQuery.bounded_trace_factorisation

namespace Orthemology.Tranche2.FiniteAlphabetQuery
variable {Y : Type*} [Inhabited Y]
open Filter

lemma counter_monotone {S : Type*} (ask : S → Bool) (next : S → Y → S)
    (oracle : ℕ → Y) (initial : S) :
    Monotone (fun n => (run ask next oracle initial n).2) := by
  apply monotone_nat_of_le_succ
  intro n
  simp only [run,advance]
  split_ifs <;> simp_all

/-- Bounded read count is exactly eventual absence of probing, not merely a
syntactic bound on an unrelated counter. -/
theorem bounded_iff_eventually_no_query {S : Type*}
    (ask : S → Bool) (next : S → Y → S)
    (oracle : ℕ → Y) (initial : S) :
    (∃ N, Bounded ask next oracle initial N) ↔
      ∀ᶠ n in atTop, ask (run ask next oracle initial n).1 = false := by
  classical
  have hmono := counter_monotone ask next oracle initial
  constructor
  · rintro ⟨N,hN⟩
    let P : ℕ → Prop := fun k => ∃ n, (run ask next oracle initial n).2 = k
    have hzero : P 0 := ⟨0,rfl⟩
    have hex := Nat.findGreatest_spec (Nat.zero_le N) hzero
    obtain ⟨n0,hn0⟩ := hex
    have hmax : ∀ n, (run ask next oracle initial n).2 ≤
        (run ask next oracle initial n0).2 := by
      intro n
      rw [hn0]
      exact Nat.le_findGreatest (hN n) ⟨n,rfl⟩
    have hconst : ∀ n ≥ n0, (run ask next oracle initial n).2 =
        (run ask next oracle initial n0).2 :=
      fun n hn => le_antisymm (hmax n) (hmono hn)
    apply eventually_atTop.mpr
    refine ⟨n0,fun n hn => ?_⟩
    cases hq : ask (run ask next oracle initial n).1 with
    | false => rfl
    | true =>
      have hnext := hconst (n+1) (hn.trans (Nat.le_succ n))
      have hnow := hconst n hn
      simp only [run,advance,hq,ite_true,Prod.snd] at hnext
      omega
  · intro h
    obtain ⟨N,hN⟩ := eventually_atTop.mp h
    have hstable : ∀ n ≥ N, (run ask next oracle initial n).2 =
        (run ask next oracle initial N).2 := by
      intro n hn
      induction n, hn using Nat.le_induction with
      | base => rfl
      | succ n hn ih => simp [run,advance,hN n hn,ih]
    refine ⟨(run ask next oracle initial N).2,fun n => ?_⟩
    rcases le_total n N with hle | hge
    · exact hmono hle
    · exact (hstable n hge).le

end Orthemology.Tranche2.FiniteAlphabetQuery

#print axioms Orthemology.Tranche2.FiniteAlphabetQuery.bounded_iff_eventually_no_query
