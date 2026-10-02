import KilledRecurrentTransfer

namespace HiddenParity.Adaptive
open Filter Orthemology.Tranche2.RecurrentSupport HiddenParity.Stochastic
variable {A : Type*} [Fintype A]

omit [Fintype A] in
/-- Deleting any finite action prefix preserves exactly the recurrent symbols. -/
theorem recurs_shift_iff (x : ℕ → A) (N : ℕ) (a : A) :
    Recurs (fun n => x (n+N)) a ↔ Recurs x a := by
  simp only [Recurs, frequently_atTop]
  constructor
  · intro h M
    obtain ⟨n, hn, ha⟩ := h M
    exact ⟨n+N, by omega, ha⟩
  · intro h M
    obtain ⟨n, hn, ha⟩ := h (M+N)
    refine ⟨n-N, by omega, ?_⟩
    have heq : n-N+N = n := by omega
    simpa only [heq] using ha

theorem recurrentSet_shift (x : ℕ → A) (N : ℕ) :
    recurrentSet (fun n => x (n+N)) = recurrentSet x := by
  classical
  ext a
  simp only [mem_recurrentSet, recurs_shift_iff]

/-- This is the actual minimum-recurrent-priority tail invariance required by
positive-prefix continuation arguments. -/
theorem paritySuccess_shift_iff (priority : A → ℕ) (x : ℕ → A) (N : ℕ) :
    ParitySuccess priority (fun n => x (n+N)) ↔ ParitySuccess priority x := by
  simp only [ParitySuccess, recurrentSet_shift]

end HiddenParity.Adaptive
