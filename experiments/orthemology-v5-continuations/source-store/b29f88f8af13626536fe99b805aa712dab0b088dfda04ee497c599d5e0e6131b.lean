import Mathlib

/-!
# An existence-aware audit of a bounded backwards history

The affine-history mechanism is a transparent reconstruction of a contractive
example, not a formalization of all of Billon's explanatory theory. It establishes
genuine infinite property determination. The Option lift then distinguishes an
absent bearer from a present bearer having a numerical value.

The empty fixed point is not asserted to be the actual state or a metaphysically
possible world. No least-fixed-point or causal-foundation axiom is assumed.
-/

namespace Orthemology.Tranche3.ExistenceAwareHistory

noncomputable section

def HalfHistory (c : ℝ) (x : ℕ → ℝ) : Prop :=
  ∀ n, x n = (x (n + 1) + c) / 2

theorem backwards_deviation (c : ℝ) (x : ℕ → ℝ) (h : HalfHistory c x)
    (n k : ℕ) : x (n + k) - c = 2 ^ k * (x n - c) := by
  induction k with
  | zero => simp
  | succ k ih =>
      have hs : x (n + k + 1) - c = 2 * (x (n + k) - c) := by
        have hh := h (n + k)
        linarith
      simpa [Nat.add_assoc, pow_succ, ih, mul_comm, mul_left_comm, mul_assoc] using hs

/-- Infinite bounded backwards histories really determine their state values.
This grants the property-explanation mechanism, rather than assuming that an
infinite arrangement can never add explanatory restrictions. -/
theorem bounded_history_constant (c M : ℝ) (x : ℕ → ℝ)
    (h : HalfHistory c x) (bounded : ∀ n, |x n - c| ≤ M) :
    ∀ n, x n = c := by
  intro n
  by_contra hn
  have hd : 0 < |x n - c| := abs_pos.mpr (sub_ne_zero.mpr hn)
  obtain ⟨k, hk⟩ := pow_unbounded_of_one_lt (M / |x n - c|) (by norm_num : (1 : ℝ) < 2)
  have hlarge : M < 2 ^ k * |x n - c| := (div_lt_iff₀ hd).mp hk
  have hb := bounded (n + k)
  rw [backwards_deviation c x h n k, abs_mul,
    abs_of_nonneg (pow_nonneg (by norm_num : (0 : ℝ) ≤ 2) k)] at hb
  linarith

/-- Without the bound every real deviation generates a backwards history. -/
theorem unbounded_family (c d : ℝ) :
    HalfHistory c (fun n => c + 2 ^ n * d) := by
  intro n
  simp only [pow_succ]
  ring

theorem nonconstant_unbounded_control (c : ℝ) :
    HalfHistory c (fun n => c + 2 ^ n) ∧
      (fun n => c + 2 ^ n) ≠ (fun _ => c) := by
  constructor
  · simpa using unbounded_family c 1
  · intro heq
    have hh := congrFun heq 0
    norm_num at hh

def liftHalf (c : ℝ) : Option ℝ → Option ℝ :=
  Option.map (fun x => (x + c) / 2)

def LiftedHistory (c : ℝ) (h : ℕ → Option ℝ) : Prop :=
  ∀ n, h n = liftHalf c (h (n + 1))

def ConditionallyBounded (c M : ℝ) (h : ℕ → Option ℝ) : Prop :=
  ∀ n x, h n = some x → |x - c| ≤ M

theorem absent_history (c : ℝ) :
    LiftedHistory c (fun _ => none) ∧
      ConditionallyBounded c 0 (fun _ => none) := by
  simp [LiftedHistory, liftHalf, ConditionallyBounded]

theorem present_history (c : ℝ) :
    LiftedHistory c (fun _ => some c) ∧
      ConditionallyBounded c 0 (fun _ => some c) := by
  constructor
  · intro n
    change some c = some ((c + c) / 2)
    congr 1
    ring
  · intro n x hx
    have hcx : c = x := Option.some.inj hx
    subst x
    simp

theorem absence_iff_next (c : ℝ) (h : ℕ → Option ℝ)
    (hr : LiftedHistory c h) (n : ℕ) :
    h n = none ↔ h (n + 1) = none := by
  rw [hr n]
  cases h (n + 1) <;> simp [liftHalf]

/-- Absence cannot be mixed with presence along this particular backwards law. -/
theorem same_absence_profile (c : ℝ) (h : ℕ → Option ℝ)
    (hr : LiftedHistory c h) (n : ℕ) : h n = none ↔ h 0 = none := by
  induction n with
  | zero => rfl
  | succ n ih =>
      exact (absence_iff_next c h hr n).symm.trans ih

/-- There are exactly two bounded profiles after an explicit absence lift:
all absent, or all present at the uniquely determined property value. -/
theorem bounded_lifted_classification (c M : ℝ) (h : ℕ → Option ℝ)
    (hr : LiftedHistory c h) (hm : 0 ≤ M)
    (hb : ConditionallyBounded c M h) :
    (∀ n, h n = none) ∨ (∀ n, h n = some c) := by
  let x : ℕ → ℝ := fun n => (h n).getD c
  have hx : HalfHistory c x := by
    intro n
    change (h n).getD c = ((h (n + 1)).getD c + c) / 2
    rw [hr n]
    cases hh : h (n + 1) with
    | none =>
        change c = (c + c) / 2
        ring
    | some y => rfl
  have hxb : ∀ n, |x n - c| ≤ M := by
    intro n
    cases hh : h n with
    | none => simpa [x, hh] using hm
    | some y => simpa [x, hh] using hb n y hh
  have hxc := bounded_history_constant c M x hx hxb
  by_cases hz : h 0 = none
  · exact Or.inl (fun n => (same_absence_profile c h hr n).mpr hz)
  · right
    intro n
    cases hh : h n with
    | none => exact False.elim (hz ((same_absence_profile c h hr n).mp hh))
    | some y =>
        have hy : y = c := by simpa [x, hh] using hxc n
        exact congrArg some hy

/-- Exact existential separation: both candidates obey the same lifted law and
conditional bound. This does not say that the absent one is actual. -/
theorem two_existence_profiles (c : ℝ) :
    ∃ h₀ h₁ : ℕ → Option ℝ,
      LiftedHistory c h₀ ∧ ConditionallyBounded c 0 h₀ ∧
      LiftedHistory c h₁ ∧ ConditionallyBounded c 0 h₁ ∧
      (∀ n, h₀ n = none) ∧ (∀ n, h₁ n = some c) ∧ h₀ ≠ h₁ := by
  refine ⟨(fun _ => none), (fun _ => some c),
    (absent_history c).1, (absent_history c).2,
    (present_history c).1, (present_history c).2, ?_, ?_, ?_⟩
  · intro n; rfl
  · intro n; rfl
  · intro hh
    have hn := congrFun hh 0
    cases hn

/-- The general audit has no assumption that the configuration is finite,
discrete, singly borne, or described by a well-founded dependency graph. -/
theorem absence_preserving_not_unique_active {H : Type*}
    (T : H → H) (empty active : H)
    (preserves : T empty = empty) (realized : T active = active)
    (different : active ≠ empty) :
    ¬ ∃! h, T h = h := by
  rintro ⟨h, _, unique⟩
  exact different ((unique active realized).trans (unique empty preserves).symm)

/-- Adding a distinct preserved absence state cannot retain global strict
contractivity in an ordinary metric. Thus the audit does not pretend to preserve
every premise of a Banach argument when it changes the state space. -/
theorem no_global_contraction_with_preserved_absence {H : Type*} [MetricSpace H]
    (T : H → H) (empty active : H)
    (preserves : T empty = empty) (realized : T active = active)
    (different : active ≠ empty) (K : NNReal) :
    ¬ ContractingWith K T := by
  intro hc
  exact different (hc.fixedPoint_unique' realized preserves)

/-- Selecting the active profile by a separate existential constraint is
consistent; it does not convert the constraint into a consequence of the law. -/
theorem active_profile_satisfies_existence (c : ℝ) :
    LiftedHistory c (fun _ => some c) ∧
      ConditionallyBounded c 0 (fun _ => some c) ∧
      ∃ n : ℕ, ∃ x, (fun _ : ℕ => (some c : Option ℝ)) n = some x := by
  exact ⟨(present_history c).1, (present_history c).2, 0, c, rfl⟩

#print axioms backwards_deviation
#print axioms bounded_history_constant
#print axioms nonconstant_unbounded_control
#print axioms two_existence_profiles
#print axioms bounded_lifted_classification
#print axioms absence_preserving_not_unique_active
#print axioms no_global_contraction_with_preserved_absence
#print axioms active_profile_satisfies_existence

end
end Orthemology.Tranche3.ExistenceAwareHistory
