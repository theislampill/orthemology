import Mathlib.Algebra.MvPolynomial.Funext

namespace P01AC.RestrictedIdentityV2
open MvPolynomial

private theorem integer_polynomial_zero_of_positive_nat_eval (p : Polynomial ℤ)
    (h : ∀ n : ℕ, 0 < n → p.eval (n : ℤ) = 0) : p = 0 := by
  apply Polynomial.eq_zero_of_infinite_isRoot
  have hinj : Function.Injective (fun n : ℕ => ((n + 1 : ℕ) : ℤ)) := by
    intro a b hab
    exact Nat.add_right_cancel (Int.ofNat.inj hab)
  apply Set.Infinite.mono ?_ (Set.infinite_range_of_injective hinj)
  rintro z ⟨n, rfl⟩
  exact h (n+1) (Nat.zero_lt_succ n)

private theorem integer_mvpolynomial_zero_of_positive_nat_eval {r : ℕ}
    (p : MvPolynomial (Fin r) ℤ)
    (h : ∀ v : Fin r → ℕ, (∀ i, 0 < v i) →
      MvPolynomial.eval (fun i => (v i : ℤ)) p = 0) : p = 0 := by
  induction r with
  | zero =>
    apply MvPolynomial.funext
    intro x
    rw [map_zero]
    have hx : x = (fun i : Fin 0 => (Fin.elim0 i : ℕ) : Fin 0 → ℤ) := by
      funext i
      exact Fin.elim0 i
    rw [hx]
    exact h Fin.elim0 (by intro i; exact Fin.elim0 i)
  | succ n ih =>
    apply (MvPolynomial.finSuccEquiv ℤ n).injective
    rw [map_zero]
    apply Polynomial.ext
    intro k
    rw [Polynomial.coeff_zero]
    apply ih
    intro v hv
    let ev : MvPolynomial (Fin n) ℤ →+* ℤ :=
      MvPolynomial.eval₂Hom (RingHom.id ℤ) (fun i => (v i : ℤ))
    have hp : Polynomial.map ev (MvPolynomial.finSuccEquiv ℤ n p) = 0 := by
      apply integer_polynomial_zero_of_positive_nat_eval
      intro m hm
      rw [Polynomial.eval_map]
      have heval : ev (MvPolynomial.C (m : ℤ)) = (m : ℤ) := by simp [ev]
      rw [← heval, Polynomial.eval₂_at_apply]
      change MvPolynomial.eval (fun i => (v i : ℤ))
        (Polynomial.eval (MvPolynomial.C (m : ℤ)) (MvPolynomial.finSuccEquiv ℤ n p)) = 0
      rw [MvPolynomial.eval_polynomial_eval_finSuccEquiv]
      have hc : (fun i => ((Fin.cases m v i : ℕ) : ℤ)) =
          Fin.cases (m : ℤ) (fun i => (v i : ℤ)) := by
        funext i
        exact Fin.cases rfl (fun _ => rfl) i
      simpa only [MvPolynomial.eval_C, ← hc] using
        h (Fin.cases m v) (fun i => Fin.cases hm hv i)
    have hk := congrArg (fun P : Polynomial ℤ => P.coeff k) hp
    simpa [Polynomial.coeff_map, ev] using hk

private theorem cast_nat_mvpolynomial_eval {r : ℕ} (p : MvPolynomial (Fin r) ℕ)
    (v : Fin r → ℕ) :
    MvPolynomial.eval (fun i => (v i : ℤ)) (MvPolynomial.map (Nat.castRingHom ℤ) p) =
      (MvPolynomial.eval v p : ℤ) := by
  rw [MvPolynomial.eval_map]
  change MvPolynomial.eval₂ (Nat.castRingHom ℤ) (fun i => (v i : ℤ)) p =
    (Nat.castRingHom ℤ) (MvPolynomial.eval₂ (RingHom.id ℕ) v p)
  rw [MvPolynomial.eval₂_comp_left]
  rfl

/-- Positive natural tuples separate natural-coefficient multivariate polynomials,
including the empty tuple at arity zero. -/
theorem nat_polynomial_eq_of_positive_eval {r : ℕ}
    {p q : MvPolynomial (Fin r) ℕ}
    (h : ∀ v : Fin r → ℕ, (∀ i, 0 < v i) →
      MvPolynomial.eval v p = MvPolynomial.eval v q) : p = q := by
  apply MvPolynomial.map_injective (Nat.castRingHom ℤ) (fun _ _ he => Int.ofNat.inj he)
  apply sub_eq_zero.mp
  apply integer_mvpolynomial_zero_of_positive_nat_eval
  intro v hv
  rw [map_sub, cast_nat_mvpolynomial_eval, cast_nat_mvpolynomial_eval, h v hv, sub_self]

#print axioms nat_polynomial_eq_of_positive_eval
end P01AC.RestrictedIdentityV2
